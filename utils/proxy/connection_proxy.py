import select
import socket
import sys
import time

from utils.proxy.proxy import Proxy


class ConnectionProxy(Proxy):
    address_forwarding = None
    port_forwarding = -1
    input_list = []
    channel = {}
    forward = ()
    delay = 0.0001

    def __init__(self, address, port, address_forwarding, port_forwarding):
        self.address = address
        self.port = port
        self.address_forwarding = address_forwarding
        self.port_forwarding = port_forwarding
        self.forward = (self.address_forwarding, self.port_forwarding)
        print(self.forward)

    def __start_proxy_server(self, server, port):
        host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host.bind((server, port))
        host.listen(200)
        return host

    def __start_proxy_forward(self, server, port):
        try:
            forward_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            forward_proxy.connect((server, port))
            return forward_proxy
        except Exception as e:
            print(e)
            return False

    def __proxy_server_loop(self, host, delay):
        self.input_list.append(host)
        while True:
            time.sleep(delay)
            ss = select.select
            input_ready, output_ready, except_ready = ss(self.input_list, [], [])
            for s in input_ready:
                if s == host:
                    self.__accept(host)
                    break
                data = s.recv(self.buffer_size)
                if len(data) == 0:
                    self.__close(s)
                else:
                    self.__recv(s, data)

    def __accept(self, host):
        forward_proxy = self.__start_proxy_forward(self.forward[0], int(self.forward[1]))
        client_socket, client_address = host.accept()
        if forward_proxy:
            self.input_list.append(client_socket)
            self.input_list.append(forward_proxy)
            self.channel[client_socket] = forward_proxy
            self.channel[forward_proxy] = client_socket
        else:
            print("cannot establish connection with remote server")
            print(f"clossing connection with client {client_address}")
            client_socket.close()
            sys.exit(1543)

    def __close(self, s):
        print(f"{s.getpeername()} peer has been disconected")
        self.input_list.remove(s)
        self.input_list.remove(self.channel[s])
        out = self.channel[s]
        self.channel[out].close()
        self.channel[s].close()
        del self.channel[out]
        del self.channel[s]

    def __recv(self, s, data):
        print(data)
        self.channel[s].send(data)

    def start_proxy(self, port=-1, address=''):
        server = self.__start_proxy_server(address, port)
        try:
            self.__proxy_server_loop(server, self.delay)
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)
