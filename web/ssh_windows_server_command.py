import os
import sys

sys.path.append(os.getcwd())

from utils.basic.parser import default_tcp_server_args
from utils.webservices.windows_server import WindowsServer

parser = default_tcp_server_args()

ip = parser.ip
port = parser.port

windows_server = WindowsServer()
windows_server.init_windows_server(ip, port)
