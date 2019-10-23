import socket

from utils.basic.parser import default_udp_client_args
from utils.webservices.udp import UDP

parser = default_udp_client_args()

target_host = parser.host
target_port = parser.port
target_data = parser.data

udp = UDP()

resp, address = udp.init_udp_socket_client(target_host, target_port, target_data)

print(resp)
print(address)
