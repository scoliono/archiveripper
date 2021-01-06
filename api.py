# api.py
# Copyright (c) 2020  James Shiffer
# This file contains all the API calls made to archive.org.

import logging, re, requests, threading

class ArchiveReaderClient:

    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.book_id = None
        self.book_meta = {}
        self.book_page_urls = []
        self.token = None
        self.URL_FORMAT = 'https://archive.org/%s'


    # Borrows a book. You should use the scheduler instead of calling this
    # method directly.
    def borrow_book(self, book_id):
        logging.debug('attempting to borrow book')

        # borrowing is done in two phases: 'browse_book' and 'grant_access'
        self.book_id = book_id
        url = self.URL_FORMAT % 'services/loans/loan/'
        res = self.session.post(url, {
            'action': 'browse_book',
            'identifier': book_id
        })
        json = res.json()
        if 'success' not in json:
            err = json['error'] if 'error' in json else 'unknown error'
            logging.error('error with action browse_book: %s' % err)
            raise AssertionError

        url = self.URL_FORMAT % 'services/loans/loan/searchInside.php'
        res = self.session.post(url, {
            'action': 'grant_access',
            'identifier': book_id
        })
        json = res.json()
        if 'success' not in json:
            err = json['error'] if 'error' in json else 'unknown error'
            logging.error('error with action grant_access: %s' % err)
            raise AssertionError
        else:
            logging.debug('received book token: %s' % json['value'])
            self.token = json['value']


    # Renews a loaned book, which must be borrowed before calling this method.
    # You should use the scheduler instead of calling this directly.
    def renew_book(self):
        if not self.book_id:
            logging.error('no book_id; you need to borrow a book first.')
            raise AssertionError

        logging.debug('attempting to renew book')
        url = self.URL_FORMAT % 'services/loans/loan/'
        res = self.session.post(url, {
            'action': 'create_token',
            'identifier': self.book_id
        })
        json = res.json()
        if 'success' not in json:
            err = json['error'] if 'error' in json else 'unknown error'
            logging.error('error renewing book: %s' % err)
            raise AssertionError
        else:
            logging.debug('renewed book token: %s' % json['token'])
            self.token = json['token']


    # Borrows a book and then automatically renews it every two minutes.
    def schedule_loan_book(self, book_id):
        # first, borrow & renew the book once
        logging.debug('scheduler running borrow/renew for the first time')
        self.borrow_book(book_id)
        self.renew_book()

        def set_interval(func, delay):
            def callback():
                set_interval(func, delay)
                logging.debug('%ds have passed, time to renew book again' \
                    % delay)
                func()
            t = threading.Timer(delay, callback)
            t.start()
            return t

        # repeat the renewal process
        set_interval(self.renew_book, 120)


    # Finds the book metadata, including book title and page URLs, and
    # returns the page count.
    def fetch_book_metadata(self):
        if not self.book_id:
            logging.error('no book_id; you need to borrow a book first.')
            raise AssertionError

        # archive.org has an endpoint for getting book metadata but its url
        # is hidden in inline js. here, we extract it from html using regex
        # (lol)
        res = self.session.get(self.URL_FORMAT % ('details/' + self.book_id))
        match = re.search(r"'(\S+BookReaderJSIA\.php\S+)'", res.text)
        if not match:
            logging.error('regex found no paths for BookReaderJSIA.php!')
            raise AssertionError

        # call the endpoint and viola, we have all the info we could ever
        # want about our book.
        res = self.session.get('https:' + match.group(1))
        json = res.json()
        if 'data' not in json:
            logging.error('expected data in JSIA response but got none')
            raise AssertionError
        self.book_meta = json['data']
        logging.debug('title: %s, imagecount: %s' % (
            self.book_meta['metadata']['title'],
            self.book_meta['metadata']['imagecount']
        ))

        # we only really need a list of the pages' urls
        flattened = [pages for spreads in \
            self.book_meta['brOptions']['data'] for pages in spreads]
        self.book_page_urls = list(map(lambda p: p['uri'], flattened))
        return len(self.book_page_urls)


    # Downloads a single page of a book. Call fetch_book_metadata() first.
    def download_page(self, i, scale="0"):
        if not self.book_meta:
            logging.error('no book_meta; you must fetch the metadata first.')
            raise AssertionError

        if i < 0 or i >= len(self.book_page_urls):
            logging.error('page index out of range')
            raise IndexError

        res = self.session.get(self.book_page_urls[i] + "&scale=%s" % scale, headers={
            'referer': self.URL_FORMAT % ('details/' + self.book_id)
        })
        return res.content


    # Logs a user in to their archive.org account.
    def login(self, email, password):
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
        json = res.json()
        if json['status'] != 'ok':
            logging.error('login responded with status %s, message %s' % \
                (json['status'], json['message']))
            raise AssertionError
        else:
            logging.debug('user has logged in successfully')
