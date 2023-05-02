import random
import threading
import time
import socket
import sys

# Récupération de l'ID du noeud en tant que paramètre
if len(sys.argv) < 2:
    print("Usage: python election.py <MyID>")
    sys.exit(1)

MyID = int(sys.argv[1])
BattUsageReceived = 0
MyBattUsage = 80
IDLeader = MyID
IDReceived = 0
PreviousLeader = None
Delta = 5

# Socket
HOST = '127.0.0.1'
PORT = 65432 + MyID
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

# Fonction pour envoyer un message en broadcast
def send_broadcast(msg):
    for i in range(1, 3):  # Envoie à tous les noeuds (ici, 2)
        if i != MyID:
            sock.sendto(msg.encode('utf-8'), (HOST, PORT + i))

# Fonction exécutée par le noeud émetteur
def emitter():
    while True:
        time.sleep(random.randint(0, 60))
        msg = f"MSG {MyID} {MyBattUsage}"
        print(f"[EMITTER-{MyID}] Sending message: {msg}")
        send_broadcast(msg)

# Fonction exécutée par le noeud récepteur
def receiver():
    while True:
        msg, address = sock.recvfrom(1024)
        msg = msg.decode('utf-8')
        print(f"[RECEIVER-{MyID}] Received message: {msg} from {address}")
        tokens = msg.split()
        if tokens[0] == "MSG":
            IDR = int(tokens[1])
            BattUsageReceived = int(tokens[2])
            if BattUsageReceived > MyBattUsage:
                if IDR > IDLeader:
                    IDLeader = IDR
                    print(f"[RECEIVER-{MyID}] New leader: {IDLeader}")
                if IDLeader == MyID:
                    print(f"[RECEIVER-{MyID}] Broadcasting election result")
                    send_broadcast(f"ELECT {MyID}")
            if time.time() >= 3600 and MyID == IDLeader:
                if PreviousLeader == MyID:
                    if BattUsageReceived < MyBattUsage:
                        MyBattUsage -= Delta
                        print(f"[RECEIVER-{MyID}] Decreasing battery usage to {MyBattUsage}")
                        send_broadcast(f"MSG {MyID} {MyBattUsage}")
                msg = f"MSG {IDR} {MyBattUsage}"
                print(f"[RECEIVER-{MyID}] Sending message: {msg}")
                sock.sendto(msg.encode('utf-8'), address)
                if IDR == IDLeader:
                    MyBattUsage = BattUsageReceived
                    print(f"[RECEIVER-{MyID}] Updating battery usage to {MyBattUsage}")
        elif tokens[0] == "ELECT":
            leader_id = int(tokens[1])
            if leader_id == MyID:
                print(f"[RECEIVER-{MyID}] Elected as leader")
            else:
                print(f"[RECEIVER-{MyID}] Node {leader_id} is the leader")

# Lancement des threads émetteur et récepteur
emitter_thread = threading.Thread(target=emitter)
receiver_thread = threading.Thread(target=receiver)
emitter_thread.start()
receiver_thread.start()

