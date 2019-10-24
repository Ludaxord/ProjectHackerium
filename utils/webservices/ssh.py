import threading

from paramiko import SSHClient, AutoAddPolicy


class SSH:
    ip = ""
    user = ""
    passwd = ""
    port = 0

    def __init__(self, ip=ip, user=user, passwd=passwd, port=22):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.port = port

    def ssh_command(self, command, ip=ip, user=user, passwd=passwd, port=port):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username=user, password=passwd, port=port)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.exec_command(command)
            print(ssh_session.recv(1024))
        return

    def ssh_command_line(self, ip=ip, user=user, passwd=passwd, port=port):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username=user, password=passwd, port=port)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            print(f"connected with {ip}:{port} as user {user}")
            while True:
                self.__cmd(user, ssh_session, client)
                client.close()
                return

    def __cmd(self, user, ssh_session, client):
        hello_message = f"<{user}:#> "
        while True:
            command = input(hello_message)
            if 'bye bye' in command:
                return
            stdin, stdout, stderr = client.exec_command(command, get_pty=True)
            for line in iter(stdout.readline, ""):
                print(line, end="")
