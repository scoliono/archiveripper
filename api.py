# api.py
# Copyright (c) 2020  James Shiffer
# This file contains all the API calls made to archive.org.

import logging, re, requests, sched, time
import json

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
        json_response = res.json()
        if 'success' not in json_response:
            err = json_response['error'] if 'error' in json_response else 'unknown error'
            logging.error('error with action browse_book: %s' % err)
            raise AssertionError

        url = self.URL_FORMAT % 'services/loans/loan/searchInside.php'
        res = self.session.post(url, {
            'action': 'grant_access',
            'identifier': book_id
        })
        json_response = res.json()
        if 'success' not in json_response:
            err = json_response['error'] if 'error' in json_response else 'unknown error'
            logging.error('error with action grant_access: %s' % err)
            raise AssertionError
        else:
            logging.debug('received book token: %s' % json_response['value'])
            self.token = json_response['value']


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
        json_response = res.json()
        if 'success' not in json_response:
            err = json_response['error'] if 'error' in json_response else 'unknown error'
            logging.error('error renewing book: %s' % err)
            raise AssertionError
        else:
            logging.debug('renewed book token: %s' % json_response['token'])
            self.token = json_response['token']


    # Performs one renewal and schedules the next one for two minutes in the future.
    def schedule_renew_book(self):
        logging.debug('time is %d, time to renew book again' % time.time())
        self.renew_book()
        self.timer.enter(120, 1, self.schedule_renew_book)


    # Borrows a book and then automatically renews it every two minutes.
    def schedule_loan_book(self, book_id):
        # first, borrow & renew the book once
        logging.debug('scheduler running borrow/renew for the first time')
        self.borrow_book(book_id)
        self.schedule_renew_book()


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

        # fix InvalidURL (No host supplied) error due to updated json response on archive.org
        details_url = json.loads(match.group(1))
        details_url = details_url['url']

        # call the endpoint and viola, we have all the info we could ever
        # want about our book.
        res = self.session.get('https:' + details_url)
        json_response = res.json()
        if 'data' not in json_response:
            logging.error('expected data in JSIA response but got none')
            raise AssertionError
        self.book_meta = json_response['data']
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
    def download_page(self, i, scale=0):
        if not self.book_meta:
            logging.error('no book_meta; you must fetch the metadata first.')
            raise AssertionError

        if i < 0 or i >= len(self.book_page_urls):
            logging.error('page index out of range')
            raise IndexError

        res = self.session.get(self.book_page_urls[i] + "&scale=%d" % scale, headers={
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
        json_response = res.json()
        if json_response['status'] != 'ok':
            logging.error('login responded with status %s, message %s' % \
                (json_response['status'], json_response['message']))
            raise AssertionError
        else:
            logging.debug('user has logged in successfully')
