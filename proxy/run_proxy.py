from utils.basic.parser import default_forward_proxy_args
from utils.proxy.connection_proxy import ConnectionProxy

parser = default_forward_proxy_args()

port = parser.port
address = parser.address
port_forwarding = parser.port_forwarding
address_forwarding = parser.address_forwarding

# proxy = ReverseProxy(port)

proxy = ConnectionProxy(address, port, address_forwarding, port_forwarding)

proxy.init_proxy()
