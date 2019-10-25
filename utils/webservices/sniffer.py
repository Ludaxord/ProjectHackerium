import os
import socket


def set_socket_protocol():
    if os.name == 'nt':
        return socket.IPPROTO_IP
    else:
        return socket.IPPROTO_ICMP


class Sniffer:
    socket_protocol = None
    host = ""

    def __init__(self, host):
        self.socket_protocol = set_socket_protocol()
        self.host = host

    def init_sniffer(self):
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.socket_protocol)
        sniffer.bind((self.host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        #       call for windows to turn on unlimited mode IOCTL
        print(os.name)
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        print(sniffer.recvfrom(65565))
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
