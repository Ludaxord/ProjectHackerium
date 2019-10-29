import socket
import sys
from _thread import start_new_thread

from utils.proxy.proxy import Proxy


class ReverseProxy(Proxy):

    def __init__(self, port, address=''):
        self.port = port
        self.address = address

    def run_proxy(self, port=None, server=None, connection=None, address=None, data=None):
        global proxy_socket
        try:
            proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_socket.connect((server, port))
            while True:
                reply = proxy_socket.recv(self.buffer_size)

                if len(reply) > 0:
                    connection.send(reply)
                    notify = float(len(reply))
                    notify = float(notify / 1024)
                    notify = "%.3s" % (str(notify))
                    notify = "%s KB" % notify
                    print(f"Request done: {str(address[0])} => {str(notify)}")
                else:
                    break
            proxy_socket.close()
            connection.close()
        except socket.error as err:
            print(f"socket error {err}")
            proxy_socket.close()
            connection.close()
            sys.exit(1464)

    def start_proxy(self, port=None, address=None):
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind((address, port))
        proxy_socket.listen(self.max_connection)
        print("[*] initialize socket...")
        print(f"Server started successfully on port {port}")
        while True:
            try:
                connection, address = proxy_socket.accept()
                data = connection.recv(self.buffer_size)
                start_new_thread(self.__connection_string, (connection, data, address))
            except Exception as e:
                print(f"exception occurred: {e}, exit proxy")
                sys.exit(1264)
            except KeyboardInterrupt:
                print("work interrupt exit proxy")
                sys.exit(1265)

    def __connection_string(self, connection, data, address):
        try:
            line = data.split(str.encode("\n"))[0]
            url = line.split(str.encode(' '))[1]

            http_position = url.find((str.encode("://")))
            if http_position == 1:
                temp = url
            else:
                temp = url[(http_position + 3):]
            port_position = temp.find(str.encode(":"))
            server_position = temp.find(str.encode("/"))
            if server_position == 1:
                server_position = len(temp)
            if port_position == -1 or server_position < port_position:
                port = 80
                server = temp[:server_position]
            else:
                port = int((temp[(port_position + 1):])[:server_position - port_position - 1])
                server = temp[:port_position]
            self.run_proxy(port, server, connection, address, data)
        except Exception as e:
            print("exception occurred")
            print(e)
