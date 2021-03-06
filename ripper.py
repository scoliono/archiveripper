# ripper.py
# Copyright (c) 2020  James Shiffer
# This file contains the main application logic.

import api, logging, os, sys

def main():
    client = api.ArchiveReaderClient()
    logging.basicConfig(level=logging.INFO)

    print('Look for the book\'s identifier (the part of the url immediately \
after "https://archive.org/details/").')

    id = input('Enter it here: ')
    logging.debug('received book ID: %s' % id)

    print('To check out books, you need an archive.org account.')
    username = input('Enter your archive.org email: ')
    password = input('Enter your archive.org password: ')
    logging.debug('attempting login with user-supplied credentials')
    client.login(username, password)

    logging.debug('attempting to start scheduler')
    client.schedule_loan_book(id)

    dir = './' + id
    logging.debug('creating output dir "%s"' % dir)
    if os.path.isdir(dir):
        response = input('Output folder %s already exists. Continue? ' \
            % dir)
        if not response.lower().startswith('y'):
            return
    else:
        os.mkdir(dir)

    page_count = client.fetch_book_metadata()
    print('The book is %d pages long. Which pages do you want?' % page_count)
    desired_pages = input('Enter a range (eg. 1-15) or leave blank for all: ')
    if desired_pages:
        [start, end] = desired_pages.split('-')
        start = int(start) - 1
        end = int(end) - 1
    else:
        start = 0
        end = page_count
    logging.debug('planning on fetching pages %d thru %d' % (start, end))

    total = end - start
    for i in range(start, end):
        logging.debug('downloading page %d (index %d)' % (i + 1,
            i))
        contents = client.download_page(i)
        open('./%s/%d.jpg' % (id, i + 1), 'wb').write(contents)
        print('%d%% (%d/%d) done' % ((i + 1) / total * 100, i + 1, total))

    print('done')
    sys.exit()

if __name__ == '__main__':
    main()
