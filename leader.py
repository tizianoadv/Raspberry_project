#from os import sleep
import socket
import time
import random

myId = "Chaima"
myBattery = "83"
seilBattery = ""
idLeader = ""

#client_socket

def send(client_socket):
    message = "msg_send;"+myId+';'+myBattery
    client_socket.sendall(message.encode())

def comparateurIp(ip1, ip2):
    id1 = ip.split('.')[-1]
    id2 = ip.split('.')[-1]
    return id1<id2
def election(client_socket):
    #duree = random(0.2, 0.8)
    send(client_socket)
    #sleep(duree)
    send
def connection(server_address):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(server_address)
    #client_socket.sendall(message.encode())
    return client_socket

def main():
    #cnx
    server_address = ("10.129.5.220" , 8184)
    client_socket = connection(server_address)
    #election
    election(client_socket)
    

    #receive
    while(True):
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        print(message)
        """receivedId, receivedBattery = message.split(';')
        print(receivedId)
        print(receivedBattery)
        if receivedId>myId and receivedBattery>myBattery:
            idLeader = receivedId
        else:
            pass"""

    #deconection
    client_socket.close()

if __name__=='__main__':
    main()