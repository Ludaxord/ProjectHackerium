import urllib.request as urllib2

from bs4 import BeautifulSoup


class Link:

    def get_all_links(self, url):
        try:
            req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html_page = urllib2.urlopen(req)
            soup = BeautifulSoup(html_page)
            return soup
        except urllib2.HTTPError as e:
            print(e.code)
            print(e.msg)
            print(e.headers)
            soup = BeautifulSoup(e.fp.read())
            return soup
