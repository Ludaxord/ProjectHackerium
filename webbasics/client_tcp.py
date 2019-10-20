import socket

from utils.basic.parser import default_tcp_client_args


def init_tcp_socket_client(host, port):
    # AF_INET => specify type of addresses that socket can communicate (IPv4 address and port number for INET)
    # SOCK_STREAM => specify connection-oriented TCP protocol

    # Create socket client object
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)

    # Connect with socket client
    client.connect((host, port))

    # Encode string into bytes representation
    encoded_str = str.encode(f"GET / HTTP/1.1\r\nHOST: {host}\r\n\r\n")

    # Send data over TCP
    client.send(encoded_str)

    # Receive data
    response = client.recv(4096)

    return response


parser = default_tcp_client_args()

target_host = parser.host
target_port = parser.port

resp = init_tcp_socket_client(target_host, target_port)

print(resp)
