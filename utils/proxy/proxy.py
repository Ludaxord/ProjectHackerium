from abc import ABC


class Proxy(ABC):

    address = None
    port = -1
    max_connection = 5
    buffer_size = 4096

    def init_proxy(self):
        pass

    def run_proxy(self):
        pass
