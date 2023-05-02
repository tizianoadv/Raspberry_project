import socket

# Configuration du serveur
server_address = ("127.0.0.1", 8181)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(1)

# Attente de la connexion client
print("En attente de connexion client...")
client_socket, client_address = server_socket.accept()
print("Connexion établie avec :", client_address)

# Réception des messages du client
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    message = data.decode()
    print("Message reçu :", message)

# Fermeture de la connexion
client_socket.close()
server_socket.close()
