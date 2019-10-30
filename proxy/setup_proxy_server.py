import time
import os
import sys

sys.path.append(os.getcwd())

from utils.basic.parser import default_forward_proxy_args
from utils.proxy.connection_proxy import ConnectionProxy
from utils.proxy.request_proxy import RequestProxy

parser = default_forward_proxy_args()

port = parser.port
address = parser.address
port_forwarding = parser.port_forwarding
address_forwarding = parser.address_forwarding

proxy = RequestProxy()

time.sleep(2)

p = f"{address_forwarding}:{port_forwarding}"

available = proxy.check_proxy(p)
time.sleep(2)
print(f"available: {available}")
if available:
    connection_proxy = ConnectionProxy(address, port, address_forwarding, port_forwarding)
    connection_proxy.init_proxy()
