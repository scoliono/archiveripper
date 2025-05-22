# api.py
# Copyright (c) 2020  James Shiffer
# This file contains all the API calls made to archive.org.

import base64, json, logging, lxml.etree, re, requests, sched, time

from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Util import Counter


class ArchiveReaderClient:

    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.book_id = None
        self.book_meta = {}
        self.book_page_urls = []
        self.token = None
        self.URL_FORMAT = 'https://archive.org/%s'
        self.timer = sched.scheduler(time.time, time.sleep)


    def borrow_book(self, book_id):
        """
        Borrows a book. You should use the scheduler instead of calling this
        method directly.
        """
        logging.debug('attempting to borrow book')

        # borrowing is done in two phases: 'browse_book' and 'grant_access'
        self.book_id = book_id
        url = self.URL_FORMAT % 'services/loans/loan/'
        res = self.session.post(url, {
            'action': 'browse_book',
            'identifier': book_id
        })
        js = res.json()
        if 'success' not in js:
            err = js['error'] if 'error' in js else 'unknown error'
            logging.error('error with action browse_book: %s' % err)
            raise AssertionError

        url = self.URL_FORMAT % 'services/loans/loan/searchInside.php'
        res = self.session.post(url, {
            'action': 'grant_access',
            'identifier': book_id
        })
        js = res.json()
        if 'success' not in js:
            err = js['error'] if 'error' in js else 'unknown error'
            logging.error('error with action grant_access: %s' % err)
            raise AssertionError
        else:
            logging.debug('received book token: %s' % js['value'])
            self.token = js['value']


    def renew_book(self):
        """
        Renews a loaned book, which must be borrowed before calling this method.
        You should use the scheduler instead of calling this directly.
        """
        if not self.book_id:
            logging.error('no book_id; you need to borrow a book first.')
            raise AssertionError

        logging.debug('attempting to renew book')
        url = self.URL_FORMAT % 'services/loans/loan/'
        res = self.session.post(url, {
            'action': 'create_token',
            'identifier': self.book_id
        })
        js = res.json()
        if 'success' not in js:
            err = js['error'] if 'error' in js else 'unknown error'
            logging.error('error renewing book: %s' % err)
            raise AssertionError
        else:
            logging.debug('renewed book token: %s' % js['token'])
            self.token = js['token']


    def schedule_renew_book(self):
        """
        Performs one renewal and schedules the next one for two minutes in the future.
        """
        logging.debug('time is %d, time to renew book again' % time.time())
        self.renew_book()
        self.timer.enter(120, 1, self.schedule_renew_book)


    def schedule_loan_book(self, book_id):
        """
        Borrows a book and then automatically renews it every two minutes.
        """
        # first, borrow & renew the book once
        logging.debug('scheduler running borrow/renew for the first time')
        self.borrow_book(book_id)
        self.schedule_renew_book()


    def fetch_book_metadata(self):
        """
        Finds the book metadata, including book title and page URLs, and
        returns the page count.
        """
        if not self.book_id:
            logging.error('no book_id; you need to borrow a book first.')
            raise AssertionError

        # archive.org has an endpoint for getting book metadata but its url
        # is hidden in inline js
        res = self.session.get(self.URL_FORMAT % ('details/' + self.book_id))
        root = lxml.etree.HTML(res.text)
        reader_data = root.find('.//input[@class="js-bookreader"]').get('value')
        reader = json.loads(reader_data)
        if 'url' not in reader:
            logging.error('bookreader metadata is missing URL field')
            raise AssertionError

        # call the endpoint and voila, we have all the info we could ever
        # want about our book.
        res = self.session.get('https:' + reader['url'])
        js = res.json()
        if 'data' not in js:
            logging.error('expected data in JSIA response but got none')
            raise AssertionError
        self.book_meta = js['data']
        logging.debug('title: %s, imagecount: %s' % (
            self.book_meta['metadata']['title'],
            self.book_meta['metadata']['imagecount']
        ))

        # we only really need a list of the pages' urls
        flattened = [pages for spreads in \
            self.book_meta['brOptions']['data'] for pages in spreads]
        self.book_page_urls = list(map(lambda p: p['uri'], flattened))
        return len(self.book_page_urls)


    def download_page(self, i, scale=0):
        """
        Downloads a single page of a book. Call fetch_book_metadata() first.
        """
        if not self.book_meta:
            logging.error('no book_meta; you must fetch the metadata first.')
            raise AssertionError

        if i < 0 or i >= len(self.book_page_urls):
            logging.error('page index out of range')
            raise IndexError

        img_url = self.book_page_urls[i] + "&scale=%d&rotate=0" % scale
        res = self.session.get(img_url, headers={
            'referer': self.URL_FORMAT % ('details/' + self.book_id)
        })

        image_data = res.content
        obfuscation_key = res.headers.get('x-obfuscate')
        if obfuscation_key:
            version, counter = obfuscation_key.split('|')
            if version != '1':
                raise AssertionError('obfuscation version %s not supported' % version)
            
            counter = base64.b64decode(counter)
            aes_key = re.sub(r'https?:\/\/.*?\/', '/', img_url)

            # decrypt first 1024 bytes of image data
            decrypted_part = self.decrypt(image_data[:1024], aes_key, counter)
            # replace the first 1024 bytes of image data with the decrypted data
            decrypted_buffer = bytearray(image_data)
            decrypted_buffer[:1024] = decrypted_part
            image_data = bytes(decrypted_buffer)

        return image_data


    def decrypt(self, data: bytes, aes_key: str, counter: bytes):
        """
        Decrypts the data with AES-CTR using the given key.
        """
        # hash the AES key using SHA-1
        sha1 = SHA1.new()
        sha1.update(aes_key.encode('utf-8'))
        aes_key_hashed = sha1.digest()[:16]  # use first 16 bytes

        # create a counter of length 64-bit
        ctr = Counter.new(64, prefix=counter[:8], initial_value=int.from_bytes(counter[8:], 'big'))

        # create AES cipher in CTR mode
        cipher = AES.new(aes_key_hashed, AES.MODE_CTR, counter=ctr)

        # decrypt the buffer
        plaintext = cipher.decrypt(data)

        return plaintext


    def login(self, email, password):
        """
        Logs a user in to their archive.org account.
        """
        # get cookies
        self.session.get(self.URL_FORMAT % 'account/login')

        res = self.session.post(self.URL_FORMAT % 'account/login', {
            'username': email,
            'password': password,
            'remember': True,
            'referer': self.URL_FORMAT % '',
            'login': True,
            'submit_by_js': True
        }, headers={
            'referer': self.URL_FORMAT % 'account/login'
        })
        js = res.json()
        if js['status'] != 'ok':
            logging.error('login responded with status %s, message %s' % \
                (js['status'], js['message']))
            raise AssertionError
        else:
            logging.debug('user has logged in successfully')
