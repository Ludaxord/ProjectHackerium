import socket
import sys
from _thread import start_new_thread
from abc import ABC

from utils.proxy.content_filter_proxy import ContentFilterProxy
from utils.proxy.forward_proxy import ForwardProxy
from utils.proxy.i2p_proxy import I2PProxy
from utils.proxy.reverse_proxy import ReverseProxy
from utils.proxy.tor_proxy import TorProxy


class Proxy(ABC):

    def init_proxy(self):
        pass

    def run_proxy(self):
        pass
