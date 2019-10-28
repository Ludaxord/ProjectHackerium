import socket

from utils.proxy.proxy import Proxy


class ForwardProxy(Proxy):

    def __init__(self, address_forwarding, port_forwarding):
        self.address = address_forwarding
        self.port = port_forwarding

    def init_proxy(self):
        forward_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_proxy(self):
        pass
