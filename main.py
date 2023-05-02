import socket
import time
import random

server_address = ("10.129.5.220", 8181)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect(server_address)
message = "C'est Tiziano, the best"
client_socket.sendall(message.encode())

client_socket.close()

