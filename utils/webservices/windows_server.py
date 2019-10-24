import socket
import sys

import paramiko

from utils.webservices.server import Server


class WindowsServer:
    host_key = None
    ip = ''
    port = 0

    def __init__(self, ip=ip, port=port, host_key=paramiko.RSAKey(filename='test_rsa.key')):
        self.host_key = host_key
        self.ip = ip
        self.port = port

    def init_windows_server(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((ip, port))
            sock.listen(100)
            print("listening for connection...")
            client, addr = sock.accept()
            print("connected!")
            try:
                bhSession = paramiko.Transport(client)
                bhSession.add_server_key(self.host_key)
                server = Server()
                try:
                    bhSession.start_server(server)
                except paramiko.SSHException as sshEx:
                    print(f"cannot establish ssh connection {str(sshEx)}")
                chan = bhSession.accept(20)
                print("Authenticated!")
                print(chan.recv(1024))
                chan.send("Welcome to windows server ssh")
                while True:
                    try:
                        command = input(f"<{ip}>: ")
                        if command != 'exit':
                            chan.send(command)
                            print(chan.recv(1024)) + "\n"
                        else:
                            chan.send('exit')
                            print('exiting')
                            bhSession.close()
                            raise Exception('exit')
                    except KeyboardInterrupt:
                        bhSession.close()
            except Exception as e:
                print(f"Catched exception {str(e)}")
        except Exception as e:
            print(f"Listen failed: {str(e)}")
            sys.exit(57)
