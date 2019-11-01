import subprocess

from torpy.http.requests import TorRequests

from utils.proxy.proxy import Proxy


class TorProxy(Proxy):
    def init_proxy(self):
        self.run_proxy()

    def run_proxy(self):
        tor = subprocess.run(["tor"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(tor)
        print(subprocess.PIPE)
