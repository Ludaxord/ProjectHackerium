import socket

from utils.basic.parser import default_udp_client_args


def init_udp_socket_client(host, port, send_data):
    # AF_INET => specify type of addresses that socket can communicate (IPv4 address and port number for INET)
    # SOCK_DGRAM => specify non-connection-oriented UDP protocol

    # Create socket client object
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM)

    encoded_data = str.encode(send_data)

    # Send data with socket client
    client.sendto(encoded_data, (host, port))

    # Receive data
    data, address = client.recvfrom(4096)

    return data, address


parser = default_udp_client_args()

target_host = parser.host
target_port = parser.port
target_data = parser.data

resp, address = init_udp_socket_client(target_host, target_port, target_data)

print(resp)
print(address)
