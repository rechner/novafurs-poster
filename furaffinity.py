#!/usr/bin/env python
#*-* coding: utf8 *-*

import re
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

class FurAffinity:
    ENDPOINT_URL = 'https://www.furaffinity.net/'
    HEADERS = {
        'User-agent' : 'Mozilla/5.0 (Linux x86) Gecko/20100101 Firefox/33.0',
        'Accept' : 'text/html',
        'Referer' : ENDPOINT_URL
    }
    def __init__(self, cookiejar_path):
        # Load cookie jar
        self.cookiejar = cookielib.MozillaCookieJar(cookiejar_path)
        self.cookiejar.load()
        opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookiejar))
        urllib2.install_opener(opener)

    def _GET_request(self, endpoint='', params={}):
        url = "{0}{1}?{2}".format(self.ENDPOINT_URL, endpoint, params)
        req = urllib2.Request(url, None, self.HEADERS)
        return urllib2.urlopen(req)

    def _POST_request(self, endpoint='', params={}):
        url = "{0}{1}".format(self.ENDPOINT_URL, endpoint)
        data = urllib.urlencode(params)
        req = urllib2.Request(url, data, self.HEADERS)
        return urllib2.urlopen(req)

    def logged_in(self):
        # Check to see if the cookies are working
        response = self._GET_request() #Returns index
        document = response.read()
        soup = BeautifulSoup(document)
        if soup.find(id="logout-link") is None:
            return False
        return True

    def post_journal(self, subject, message):
        key = self._new_journal_key()
        params = {
            'id' : '',
            'key' : key,
            'do' : 'update',
            'subject' : subject,
            'message' : message
        }
        # Submit form
        response = self._POST_request('controls/journal', params)
        url = response.geturl()
        journal_id = re.match(r".*/(\d{2,8})/$", url).group(1)
        return journal_id

    def _new_journal_key(self):
        # Fetches the key required for submitting a new journal entry with.
        response = self._GET_request('controls/journal')
        soup = BeautifulSoup(response.read())
        tag = soup.find('input', {'name':'key'})
        if tag is None:
            raise TypeError("Expected form input value not found")
        return tag.get('value')

    @staticmethod
    def convert_markdown(text):
        """Changes markdown to FA's BB code."""

        # Links and image stripping needs to happen before escaping


        # Escape character literals
        text = re.sub(r'\\\*', '%%STRASTERISK%%', text)

        # **Strong tag**
        text = re.sub(r'\*\*(?=\S)(.+?[*_]*)(?<=\S)\*\*',
               r'[b]\1[/b]', text)

        # *emphasis*
        text = re.sub(r'\*(?=\S)(.+?)(?<=\S)\*',
               r'[i]\1[/i]', text)



        # Unescape:
        text = re.sub(r'%%STRASTERISK%%', '*', text)
        return text


if __name__ == '__main__':
    #api = FurAffinity('cookies.txt')
    doc = """This is a test... This is only a [b]test[/b].

    Testing testing 1,2,3.  That is all.

    Woof.
    """
    #print api.post_journal("Hello world!", doc)

    print FurAffinity.convert_markdown("*testing* 123.  This is a test.  This is only a **test**.  That is all*.")
