import os
import sys

sys.path.append(os.getcwd())

from utils.basic.parser import default_tcp_proxy_args
from utils.webservices.tcp import TCP

parser = default_tcp_proxy_args()

target_host = parser.host
target_port = parser.port
local_host = parser.localhost
local_port = parser.localport
receive_first = parser.receivefirst

tcp = TCP()

tcp.init_tcp_proxy(local_host=local_host, local_port=local_port, remote_host=target_host, remote_port=target_port,
                   receive_first=receive_first)
