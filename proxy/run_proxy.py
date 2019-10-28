from utils.basic.parser import default_proxy_args
from utils.proxy.proxy import Proxy
from utils.proxy.reverse_proxy import ReverseProxy

parser = default_proxy_args()

port = parser.port

proxy = ReverseProxy(port)

proxy.init_proxy()
