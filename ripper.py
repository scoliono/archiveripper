# ripper.py
# Copyright (c) 2020  James Shiffer
# This file contains the main application logic.

import argparse, api, getpass, img2pdf, logging, os, sys, tqdm


def main():
    client = api.ArchiveReaderClient()
    logging.basicConfig(level=logging.INFO)

    # Parse book id and credentials
    parser = argparse.ArgumentParser()
    parser.add_argument('id', nargs='?',
        help='Look for the book\'s identifier (the part of the url immediately after "https://archive.org/details/").')
    parser.add_argument('-u', '--username', help='Your archive.org account\'s email.')
    parser.add_argument('-p', '--password', help='Your archive.org account\'s password')
    parser.add_argument('-a', '--all-pages', action='store_true', help='Download every page of the book')
    parser.add_argument('-s', '--page-start', type=int, help='Download pages starting at page number N and ending at the book\'s last page, or a range if --page-end has been specified')
    parser.add_argument('-e', '--page-end', type=int, help='End of the range of page numbers to download')
    parser.add_argument('-f', '--format', choices=['pdf'], help='Converts the individual pages into a single file. Currently only PDF is supported')
    parser.add_argument('-d', '--output-dir', help='Directory you want the pages to be written to. If undefined the directory will be named the book id')
    parser.add_argument('-S', '--scale', default=0, type=int, help='Image resolution of the pages requested, can save bandwidth if the best image quality isn\'t necessary. Higher integers mean smaller resolution, default is 0 (no downscaling)')
    args = parser.parse_args()

    id = args.id
    username = args.username
    password = args.password

    #If any of the credentials isn't specified with cmdline args ask for it interactively
    if not args.id:
        print('Look for the book\'s identifier (the part of the url immediately after "https://archive.org/details/").')
        id = input('Enter it here: ')
        logging.debug('received book ID: %s' % id)
    if not args.username:
        username = input('Enter your archive.org email: ')
    if not args.password:
        password = getpass.getpass('Enter your archive.org password: ')


    logging.debug('attempting login with user-supplied credentials')
    client.login(username, password)

    logging.debug('attempting to start scheduler')
    client.schedule_loan_book(id)

    if not args.output_dir:
        dirname = './' + id
    else:
        dirname = os.path.expanduser(args.output_dir)

    logging.debug('creating output dir "%s"' % dirname)
    if os.path.isdir(dirname):
        response = input('Output folder %s already exists. Continue? ' \
            % dirname)
        if not response.lower().startswith('y'):
            return
    else:
        os.mkdir(dirname)

    page_count = client.fetch_book_metadata()

    start = 0
    end = page_count

    if not args.all_pages:
        if not args.page_start and not args.page_end:
            print('The book is %d pages long. Which pages do you want?' % page_count)
            desired_pages = input('Enter a range (eg. 1-15) or leave blank for all: ')

            if desired_pages:
                [start, end] = desired_pages.split('-')
                start = int(start) - 1
                end = int(end)
        else:
            if args.page_start: start = args.page_start - 1
            if args.page_end: end = args.page_end

    logging.debug('planning on fetching pages %d thru %d' % (start, end))

    total = end - start
    for i in tqdm.tqdm(range(start, end)):
        logging.debug('downloading page %d (index %d)' % (i + 1,
            i))
        contents = client.download_page(i, args.scale)
        with open('%s/%d.jpg' % (dirname, i + 1), 'wb') as file:
            file.write(contents)
        done_count = i + 1 - start

    if args.format == 'pdf':
        print('converting images to pdf')
        img_list = ['%s/%d.jpg' % (dirname, i + 1) for i in range(start, end)]
        with open('%s.pdf' % dirname, 'wb') as pdf:
            pdf_data = img2pdf.convert(img_list)
            pdf.write(pdf_data)
            print('wrote %d pages to %s.pdf' % (total, dirname))
        logging.debug('removing temporary image files')
        for img_name in img_list:
            os.remove(img_name)
        try:
            os.rmdir(dirname)
            print('removed output dir %s' % dirname)
        except OSError:
            logging.warning('unable to remove output dir %s; it may not be empty' % dirname)

    print('done')

if __name__ == '__main__':
    main()
