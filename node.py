import time
import random
import socket
import threading

# Variables
MyID = 1
BattUsageReceived = 0.8
MyBattUsage = 0.8
IDLeader = MyID
IDReceived = 0
PreviousLeader = None
Delta = 0.1

# Initialisation des sockets
UDP_IP = '127.255.255.255'  # Adresse IP de broadcast
UDP_PORT = 5005  # Port de communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Fonction pour envoyer un message en broadcast
def MSG(MyID, MyBattUsage=None):
    message = f"{MyID}|{MyBattUsage}"
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))

# Code émetteur
def code_emetteur():
    while True:
        time.sleep(random.randint(0, 60))
        MSG(MyID, MyBattUsage)

# Code réception
def code_reception():
    while True:
        if time.time() >= 60:
            break
        else:
            IDR, BattUsageReceived = None, None
            MSGReceived = False
            # Code pour recevoir un message
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            fields = message.split('|')
            IDR, BattUsageReceived = int(fields[0]), float(fields[1])
            MSGReceived = True
            # ...
            if MSGReceived and BattUsageReceived > MyBattUsage:
                if IDR > IDLeader:
                    IDLeader = IDR
                if IDLeader == MyID:
                    MSG(MyID)
            if time.time() >= 3600 and MyID == IDLeader:
                if PreviousLeader == MyID:
                    if BattUsageReceived < MyBattUsage:
                        MyBattUsage -= Delta
                        MSG(MyID, MyBattUsage)
                message = f"{MyID}|{MyBattUsage}"
                sock.sendto(message.encode('utf-8'), (addr[0], UDP_PORT))
                if IDR == IDLeader:
                    MyBattUsage = BattUsageReceived
            time.sleep(0.1)  # Attente avant de vérifier les messages reçus
            # Affichage du résultat de l'élection en direct
            if MyID == IDLeader and IDLeader == OtherID:
                print(f"Le leader est le nœud {IDLeader}")
            else:
                print(f"Le nœud {MyID} n'est pas le leader")

# Lancement des threads
t1 = threading.Thread(target=code_emetteur)
t2 = threading.Thread(target=code_reception)
t1.start()
t2.start()

