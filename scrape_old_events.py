"""
Quick screen scrape of past events on the old ABCD site at w3.abcd.harvard.edu
"""
import sys
from os.path import dirname, isfile, isdir, join, realpath
import os
from urlparse import urlparse
from dateutil import parser as date_parser
from bs4 import BeautifulSoup
import requests
from slugify import slugify

CURRENT_DIR = dirname(realpath(__file__))
HTML_PAGES_DIR = join(CURRENT_DIR, 'html_pages')
GOOD_URL_PIECES = ['w3.abcd.harvard.edu/ai1ec_event',\
            'w3.abcd.harvard.edu/past-events']

def msg(s): print s
def dashes(): msg('-' * 40)
def msgt(s): dashes(); msg(s); dashes()

class ABCDPageDownloader(object):

    def __init__(self, start_page):
        self.start_page = start_page
        self.err_found = False
        self.err_msgs = []
        self.followed_links = []
        self.download_cnt = 0

    def download_pages(self, follow_links=True):
        self.download_single_page(self.start_page, follow_links=follow_links)
        msgt('Pages downloaded: %d' % self.download_cnt)

    def is_followed_link(self, lnk):
        if lnk in self.followed_links:
            return True
        return False

    def add_followed_link(self, lnk):
        if self.is_followed_link(lnk):
            return
        self.followed_links.append(lnk)

    def add_error(self, error_msg):
        if error_msg is None:
            return
        self.err_found = True
        self.err_msgs.append(error_msg)

    def show_error(self):
        print 'ERROR: %s' % '\n'.join(self.err_msgs)
        sys.exit(0)

    def get_filename_form_url(self, url_str, event_time):
        if url_str is None:
            self.add_error('Bad url: %s' %  url_str)
            return

        parsed = urlparse(url_str)
        url_path = parsed.path
        if url_path.endswith('/'):
            url_path = url_path[:-1]

        # may blow up
        if event_time:
            time_str = event_time.strftime('%Y_%m_%d-')
            fname = time_str + slugify(url_path.split('/')[-1]) + '.html'
        else:
            fname = slugify(url_path.split('/')[-1]) + '.html'

        fullname = join(self.get_html_pages_dir(), fname)
        return fullname

    def get_event_time(self, soup):
        """
        From the soup, grab a datetime.datetime object with Year, Month Date
        <div class="ai1ec-time">
    		<div class="ai1ec-label">When:</div>
            <div class="ai1ec-field-value">March 9, 2016 @ 3:30 pm - 5:00 pm</div>
        </div>
        """
        try:
            time_val = soup.find("div", {"class": "ai1ec-time"}).find('div', {'class':'ai1ec-field-value'}).text
        except AttributeError:
            return None

        time_val = time_val.split('@')[0].strip()
        if time_val:
            return date_parser.parse(time_val)

        return None


    def download_single_page(self, url_str, follow_links=False, event_time=None):
        """
        Actually download a page's html
        """
        msgt('Check page: %s' % url_str)
        if self.err_found:
            self.show_error()

        if not self.is_acceptable_url(url_str):
            return

        #import ipdb; ipdb.set_trace()
        msg('Download: %s' % url_str)
        r = requests.get(url_str)
        if r.status_code != 200:
            self.add_error('Bad status code of %s for %s' % (r.status_code, url_str))
            return

        # Grab the content
        html_content = r.content

        # Don't retrieve this link again
        self.add_followed_link(url_str)

        # Use bsoup to see if there's an event time
        #   Also used further down to check other links in the content
        soup = BeautifulSoup(html_content, 'html.parser')
        event_time = self.get_event_time(soup)

        # Do we already have this file?
        # Bad assumption? pages won't have the same name
        #
        output_filename = self.get_filename_form_url(url_str, event_time)
        if isfile(output_filename): # We have it, move on
            return

        msg('output_filename: %s' % output_filename)
        open(output_filename, 'w').write(html_content)
        self.download_cnt += 1
        print '(%d) file written: %s' % (self.download_cnt, output_filename)

        if follow_links:
            for link in soup.find_all('a'):
                lnk_str = link.get('href')
                lnk_str = lnk_str.replace('hhttp:', 'http:') # fix error
                #print 'Checking', lnk_str
                if self.is_acceptable_url(lnk_str) and\
                    not self.is_followed_link(lnk_str):
                    #msgt('YES')
                    self.download_single_page(lnk_str, follow_links=False)

    def get_html_pages_dir(self):
        if not isdir(HTML_PAGES_DIR):
            os.makedirs(HTML_PAGES_DIR)
        return HTML_PAGES_DIR

    def is_acceptable_url(self, url_str):
        for url_piece in GOOD_URL_PIECES:
            if url_str.find(url_piece) > -1:
                return True
        return False



if __name__ == '__main__':
    # Start with the past events page and download the HTML
    #   for the old events pages -- e.g. the pages on the site
    #
    start_page = 'http://w3.abcd.harvard.edu/past-events/'
    abcd = ABCDPageDownloader(start_page)
    abcd.download_pages()

    # Scrape single event page to make sure date
    # can be pulled out
    #start_page = 'http://w3.abcd.harvard.edu/ai1ec_event/mary-kennedy-ux-toolkit/?instance_id=243'
    #abcd = ABCDPageDownloader(start_page)
    #abcd.download_pages(follow_links=False)
