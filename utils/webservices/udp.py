import socket
import sys

from utils.webservices.protocol import Protocol


class UDP(Protocol):
    host = ""
    port = 0
    data = ""

    def __init__(self, host="", port=0, data=""):
        opts, args = self.get_udp_args()
        temporary_host, temporary_port, temporary_data, temporary_localhost, temporary_localport, temporary_receive_first = self.check_args(
            opts)
        if host == self.host:
            self.host = temporary_host
        if port == self.port:
            self.port = temporary_port
        if data == self.data:
            self.data = temporary_data

    def usage(self):
        print("UDP Tool")
        print("usage:")
        print("-h - target host")
        print("-p - target port")
        print("-d - target data")
        print("UDP -h 192.168.0.1 -p 5555 -d AAACCCDDD")
        sys.exit(52)

    def init_udp_socket_client(self, host=host, port=port, send_data=data):
        # AF_INET => specify type of addresses that socket can communicate (IPv4 address and port number for INET)
        # SOCK_DGRAM => specify non-connection-oriented UDP protocol

        # Create socket client object
        client = socket.socket(socket.AF_INET,
                               socket.SOCK_DGRAM)

        encoded_data = str.encode(send_data)

        # Send data with socket client
        client.sendto(encoded_data, (host, port))

        # Receive data
        data, address = client.recvfrom(4096)

        return data, address
