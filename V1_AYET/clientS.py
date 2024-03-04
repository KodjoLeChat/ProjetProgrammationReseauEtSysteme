import socket
import threading
import uuid

# Store players and their identifiers
players = {}

# Function to generate a unique player ID
def generate_unique_id():
    return str(uuid.uuid4())

# Function to handle a player's connection
def handle_player(player_id, client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        # Broadcast the data to all connected players (except the sender)
        print(f"Received data from player {player_id}: {data}")
        for player in players:
            if player != player_id:
                players[player].send(data.encode())

# Function to authenticate a player
def authenticate_player(client_socket):
    unique_id = generate_unique_id()
    players[unique_id] = client_socket

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5551))  # You can change the IP and port as needed
    server.listen()

    print("Server is listening for incoming connections...")

    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address}")
        
        # Authenticate the player
        authenticate_player(client_socket)

        # Start a thread to handle the player's connection
        player_id = [key for key, value in players.items() if value == client_socket][0]
        player_thread = threading.Thread(target=handle_player, args=(player_id, client_socket))
        player_thread.start()

if __name__ == "__main__":
    main()























# from random import randint

# from twisted.internet import reactor
# from twisted.internet.protocol import DatagramProtocol


# class Server(DatagramProtocol):
#     def __init__(self):
#         self.clients = set()

#     def datagramReceived(self, datagram: bytes, addr):
#         datagram = datagram.decode("utf-8")
#         if datagram == "ready":
#             adresses = "\n".join([str(x) for x in self.clients])
#             self.transport.write(adresses.encode("utf-8"),addr)
#             self.clients.add(addr)

#         # return super().datagramReceived(datagram, addr)
# if __name__ == '__main__':
#     reactor.listenUDP(9999,Server())
#     reactor.run()


