import threading

import paramiko


class Server(paramiko.ServerInterface):
    event = None

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, channel_id):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'mrrobot' and password == 'eliott':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
