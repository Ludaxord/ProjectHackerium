import sys
import socket
import getopt
import threading
import subprocess


class NetCat:
    listen = False
    command = False
    upload = False
    execute = ""
    target = ""
    upload_destination = ""
    port = 0

    def __usage(self):
        print("BHP Net Tool")
        print("usage:")
        print("-t - target host")
        print("-p - target port")
        print("-l --listen - listen on [host]:[port] upcoming connection")
        print("-e --execute=file to run - run file that get connection")
        print("-c --command initialize command line")
        print("-u --upload=destination when connection will be saved, it send file and save it in [destination]")
        print("Examples:")
        print("NetCat -t 192.168.0.1 -p 5555 -l -c")
        print("NetCat -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
        print("NetCat -t 192.168.0.1 -p 5555 -l -e\"cat /etc/passwd\"")
        print("echo 'ABCDEFGHI' | ./NetCat -t 192.168.11.12 -p 135")
        sys.exit(54)

    # read command line args
    def get_args(self):
        if not len(sys.argv[1:]):
            self.__usage()

        try:
            print(sys.argv)
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                       ["help", "listen", "execute", "target", "port", "command", "upload"])
            return opts, args
        except getopt.GetoptError as err:
            print(str(err))
            self.__usage()

    def __check_args(self, opts):
        for option, action in opts:
            if option in ("-h", "--help"):
                self.__usage()
            elif option in ("-l", "--listen"):
                self.listen = True
            elif option in ("-e", "--execute"):
                self.execute = action
            elif option in ("-c", "--command"):
                self.command = True
            elif option in ("-u", "--upload"):
                self.upload_destination = action
            elif option in ("-t", "--target"):
                self.target = action
            elif option in ("-p", "--port"):
                self.port = int(action)
            else:
                assert False, "unsupported option"

        return self.listen, self.port, self.execute, self.command, self.upload_destination, self.target

    def __load_buffer(self, listen, target, port):
        # listen to data sent over stdin
        if not listen and len(target) and port > 0:
            # load buffer to command line
            # it makes block, use Ctrl + D if you are not sending data to stdin
            buffer = sys.stdin.read()
            #         send data
            self.client_sender(buffer, target, port)
            # listening or sending will be executing commands or turn on shell depends on options from command line
        if listen:
            self.server_loop(target, port)

    def client_sender(self, buffer, target, port):
        global upload
        global execute
        global command
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            #         connect with target host
            client.connect((target, port))
            if len(buffer):
                client.send(buffer)
            while True:
                # waiting to return data
                recv_len = 1
                response = ""
                while recv_len:
                    data = client.recv(4096).decode("utf-8")
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break
                print(response, )

                #         waiting to more data
                buffer = input("")
                buffer += "\n"

                #         sending data
                client.send(str.encode(buffer))
        except socket.error as exc:
            print(f"[*] Exception occurred {exc}")
            client.close()

    def server_loop(self, target, port):
        if not len(target):
            target = "0.0.0.0"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target, port))
        server.listen(5)

        while True:
            client_socket, addr = server.accept()

            #         thread to run new client
            client_thread = threading.Thread(target=self.client_handler, args=(client_socket,))
            client_thread.start()

    def run_command(self, command):
        command = command.rstrip()

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = "Cannot run command \r\n"
        return output

    def client_handler(self, client_socket):
        if len(self.upload_destination):
            file_buffer = ""
            while True:
                data = client_socket.recv(1024)

                if not data:
                    break
                else:
                    file_buffer += data

            try:
                file_descriptor = open(self.upload_destination, "wb")
                file_descriptor.write(str.encode(file_buffer))
                file_descriptor.close()

                client_socket.send(f"file saved in {self.upload_destination}")
            except:
                client_socket.send(f"cannot save file in {self.upload_destination}")
        if len(self.execute):
            output = self.run_command(execute)
            client_socket.send(output)
        if self.command:
            while True:
                client_socket.send(str.encode("<NetCat:#> "))
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024).decode("utf-8")
                response = self.run_command(cmd_buffer)
                client_socket.send(response)

    def main(self):
        opts, args = self.get_args()
        self.listen, self.port, self.execute, self.command, self.upload_destination, self.target = self.__check_args(
            opts)
        self.__load_buffer(self.listen, self.target, self.port)
