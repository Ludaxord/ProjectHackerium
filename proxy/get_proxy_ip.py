from utils.proxy.request_proxy import RequestProxy

proxy = RequestProxy()
proxies = list(proxy.get_proxies())

print(proxies)
