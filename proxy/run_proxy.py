import time

import requests

from utils.basic.parser import default_forward_proxy_args
from utils.proxy.connection_proxy import ConnectionProxy
from utils.proxy.request_proxy import RequestProxy

parser = default_forward_proxy_args()

port = parser.port
address = parser.address
port_forwarding = parser.port_forwarding
address_forwarding = parser.address_forwarding

# proxy = ReverseProxy(port)

proxy = RequestProxy()

proxies = list(proxy.get_proxies())

time.sleep(2)

print(proxies)

for p in proxies:
    print(p)
    available = proxy.check_proxy(p)
    time.sleep(2)
    print(f"available: {available}")
    if available:
        splited = p.split(":")
        proxy_address = splited[0]
        proxy_port = splited[1]
        connection_proxy = ConnectionProxy(address, port, proxy_address, proxy_port)
        connection_proxy.init_proxy()
