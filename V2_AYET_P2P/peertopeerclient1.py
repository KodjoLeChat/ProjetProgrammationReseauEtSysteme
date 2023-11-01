import socket
import threading

# Adresse IP du serveur (joueur 1 en C) et port
server_address = ('localhost', 12346)

# Créer un socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Fonction pour recevoir les messages du serveur
def receive_messages():
    while True:
        data = client_socket.recv(1024)
        print(data)
        if not data:
            break
        print(data)

# Démarrer un thread pour recevoir les messages du serveur
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Envoyer des messages au serveur
while True:
    message = input("Message à envoyer au serveur : ")
    client_socket.send(message.encode('utf-8'))
