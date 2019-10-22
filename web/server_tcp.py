import socket
import threading

from utils.basic.parser import default_tcp_server_args


def init_tcp_socket_server(ip, port):
    # AF_INET => specify type of addresses that socket can communicate (IPv4 address and port number for INET)
    # SOCK_STREAM => specify connection-oriented TCP protocol

    # Create socket client object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"Listening on port {ip}:{port}")

    while True:
        client, addr = server.accept()
        print(f"received connection from {addr[0]}:{addr[1]}")
        # create client thread to handling received data
        client_handler = threading.Thread(target=__handle_client, args=(client,))
        client_handler.start()


# client exception handling
def __handle_client(client_socket):
    request = client_socket.recv(1024)  # print data sent by client
    print(f"received {request}")
    encoded_packet = str.encode("ACK")
    client_socket.send(encoded_packet)  # send packet back to client
    client_socket.close()  # close client socket


parser = default_tcp_server_args()

bind_ip = parser.ip
bind_port = parser.port

init_tcp_socket_server(bind_ip, bind_port)
