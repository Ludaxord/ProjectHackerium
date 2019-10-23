import socket
import sys
import threading

from utils.webservices.protocol import Protocol


class TCP(Protocol):
    host = ""
    port = 0
    localhost = ""
    localport = 0
    receive_first = False
    data = ""

    def __init__(self, host="", port=0, data="", localhost="", localport=0, receive_first=False):
        opts, args = self.get_tcp_args()
        temporary_host, temporary_port, temporary_data, temporary_localhost, temporary_localport, temporary_receive_first = self.check_args(
            opts)
        if host == self.host:
            self.host = temporary_host
        if port == self.port:
            self.port = temporary_port
        if localhost == self.localhost:
            self.localhost = temporary_localhost
        if localport == self.localport:
            self.port = temporary_localport
        if receive_first == self.receive_first:
            self.receive_first = temporary_receive_first
        if data == self.data:
            self.data = temporary_data

    def usage(self):
        print("TCP Tool")
        print("usage:")
        print("-h - target host")
        print("-p - target port")
        print("-d - target data")
        print("-w - local host")
        print("-a - local port")
        print("-r - receive first")
        print("TCP -h 192.168.0.1 -p 5555 -d AAACCCDDD")
        print("TCP -h 192.168.0.1 -p 5555 -lh 10.30.123.1 -lp 9000 -r True")
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

    def init_tcp_proxy(self, local_host=localhost, local_port=localport, remote_host=host, remote_port=port,
                       receive_first=receive_first):
        self.__server_loop(local_host, local_port, remote_host, remote_port, receive_first)

    def __server_loop(self, local_host, local_port, remote_host, remote_port, receive_first):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.bind((local_host, local_port))
        except:
            print(f"Cannot establish listening on port {local_host}:{local_port}")
            print(f"Find another socket or get right privileges")
            sys.exit(55)
        print(f"listening on port {local_host}:{local_port}")
        server.listen(5)
        while True:
            client_socket, addr = server.accept()

            print(f"[=>] received incoming connection from {addr[0]}:{addr[1]}")

            proxy_thread = threading.Thread(target=self.__proxy_handler,
                                            args=(client_socket, remote_host, remote_port, receive_first))
            proxy_thread.start()

    def __proxy_handler(self, client_socket, remote_host, remote_port, receive_first):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        if receive_first:
            remote_buffer = self.__receive_from(remote_socket)
            self.__hexdump(remote_buffer)

            remote_buffer = self.__response_handler(remote_buffer)

            if len(remote_buffer):
                print(f"[<==] sending {len(remote_buffer)} bytes to localhost")
                client_socket.send(remote_buffer)

        while True:
            local_buffer = self.__receive_from(client_socket)
            if len(local_buffer):
                print(f"[=>] received {len(local_buffer)} bytes from localhost")
                self.__hexdump(local_buffer)
                local_buffer = self.__request_handler(local_buffer)
                remote_socket.send(str.encode(local_buffer))
                print(f"[==>] sent to remote host")
                remote_buffer = self.__receive_from(remote_socket)
                if len(remote_buffer):
                    print(f"[<==] received {len(remote_buffer)} from remote host")
                    self.__hexdump(remote_buffer)

                    remote_buffer = self.__response_handler(remote_buffer)
                    client_socket.send(remote_buffer)
                    print(f"[<==] sending to localhost")
                if not len(local_buffer) or not len(remote_buffer):
                    client_socket.close()
                    remote_socket.close()
                    print("no more data closing connection")
                    break

    def __response_handler(self, buffer):
        return buffer

    def __receive_from(self, connection):
        buffer = ""
        connection.settimeout(4)
        try:
            while True:
                data = connection.recv(4096)
                if not data:
                    break
                buffer += data
        except:
            pass

        return buffer

    def __hexdump(self, src, length=16):
        result = []
        digits = 4

        s = src[:]
        print(s)
        hexa = " ".join(["%0*X" % (digits, ord(x)) for x in s.decode("ascii")])
        text = "".join([x if 0x20 <= ord(x) < 0x7F else "." for x in s.decode("ascii")])
        result.append("%04X   %-*s   %s" % (1, length * (digits + 1), hexa, text))

        print("\n".join(result))

    def __request_handler(self, buffer):
        return buffer
