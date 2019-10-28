import socket
import sys
from _thread import start_new_thread

from utils.proxy.proxy import Proxy


class ReverseProxy(Proxy):
    port = -1
    max_connection = 5
    buffer_size = 4096

    def __init__(self, port):
        self.port = port

    def init_proxy(self):
        try:
            print(f"listening on port {self.port}")
            self.__start_proxy(self.port)
        except Exception as e:
            print(f"exception occurred: {e}, exit proxy")
            sys.exit(1264)
        except KeyboardInterrupt:
            print("work interrupt exit proxy")
            sys.exit(1265)

    def run_proxy(self, port=None, server=None, connection=None, address=None, data=None):
        global proxy_socket
        try:
            proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_socket.connect((server, self.port))
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
        except socket.error as (value, message):
            print(f"socket error {message} => {value}")
            proxy_socket.close()
            connection.close()
            sys.exit(1464)

    def __start_proxy(self, port):
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind(('', port))
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
            print(data)
            line = data.split("\n")[0]
            print(line)
            url = line.split(' ')[1]
            print(url)

            http_position = url.find("://")
            if http_position == 1:
                temp = url
            else:
                temp = url[(http_position + 3):]
            port_position = temp.find(":")
            server_position = temp.find("/")
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
            print(e)
            pass
