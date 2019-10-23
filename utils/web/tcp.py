import socket
import sys

from utils.web.protocol import Protocol


class TCP(Protocol):
    host = ""
    port = 0
    data = ""

    def __init__(self, host="", port=0, data=""):
        opts, args = self.get_args()
        temporary_host, temporary_port, temporary_data = self.check_args(opts)
        if host == self.host:
            self.host = temporary_host
        if port == self.port:
            self.port = temporary_port
        if data == self.data:
            self.data = temporary_data

    def usage(self):
        print("TCP Tool")
        print("usage:")
        print("-h - target host")
        print("-p - target port")
        print("-d - target data")
        print("TCP -h 192.168.0.1 -p 5555 -d AAACCCDDD")
        sys.exit(53)

    def init_tcp_socket_client(self, host=host, port=port, data=data):
        # AF_INET => specify type of addresses that socket can communicate (IPv4 address and port number for INET)
        # SOCK_STREAM => specify connection-oriented TCP protocol

        # Create socket client object
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)

        # Connect with socket client
        client.connect((host, port))

        # Encode string into bytes representation
        encoded_str = str.encode(data)

        # Send data over TCP
        client.send(encoded_str)

        # Receive data
        response = client.recv(4096)

        return response
