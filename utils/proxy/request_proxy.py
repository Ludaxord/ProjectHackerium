from itertools import cycle

import requests
from lxml.html import fromstring

from utils.proxy.proxy import Proxy


class RequestProxy(Proxy):

    def start_proxy(self, port=None, address=None):
        url = 'https://httpbin.org/ip'

        print("Request default IP")

        response = requests.get(url)
        print(response.json())

        proxies = self.get_proxies()
        proxy_pool = cycle(proxies)

        for i in range(1, 11):
            # Get a proxy from the pool
            proxy = next(proxy_pool)
            print("Request #%d" % i)
            try:
                response = requests.get(url, proxies={"http": proxy, "https": proxy})
                print(response.json())
            except:
                print("Skipping. Connection error")

    def check_proxy(self, proxy):
        url = 'https://httpbin.org/ip'
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            return True
        except:
            return False

    def get_proxies(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies
