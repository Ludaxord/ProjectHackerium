import sys
from abc import ABC


class Proxy(ABC):

    address = ''
    port = -1
    max_connection = 5
    buffer_size = 4096

    def init_proxy(self):
        try:
            print(f"listening on port {self.port}")
            self.start_proxy(self.port, self.address)
        except Exception as e:
            print(f"exception occurred: {e}, exit proxy")
            sys.exit(1264)
        except KeyboardInterrupt:
            print("work interrupt exit proxy")
            sys.exit(1265)

    def start_proxy(self, port=None, address=None):
        pass

    def run_proxy(self):
        pass
