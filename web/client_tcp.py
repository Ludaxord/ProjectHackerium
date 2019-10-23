import socket

from utils.basic.parser import default_tcp_client_args
from utils.web.tcp import TCP

parser = default_tcp_client_args()

target_host = parser.host
target_port = parser.port
target_data = parser.data

tcp = TCP()

resp = tcp.init_tcp_socket_client(target_host, target_port, target_data)

print(resp)
