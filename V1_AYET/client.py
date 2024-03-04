import socket
import threading


def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(f"Received message from server: {data}")

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5551))  # Replace with the server's IP and port

    # Start a thread to receive and print messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input("Enter a message: ")
        client.send(message.encode())

if __name__ == "__main__":
    main()






































# from random import randint

# from twisted.internet import reactor
# from twisted.internet.protocol import DatagramProtocol


# class Client(DatagramProtocol):
#     def __init__(self,host,port) :
#         if(host == "localhost"):
#             host = "127.0.0.1"
        
#         self.id = host,port
#         self.address = None
#         self.server = '127.0.0.1',9999
#         print("working on id:",self.id)

#     def startProtocol(self):
#         self.transport.write("ready".encode('utf-8'),self.server)
        
    
#     def datagramReceived(self, datagram: bytes, addr):
#         datagram = datagram.decode('utf-8')

#         if addr == self.server:
#             print("Choose a Client from these \n",datagram)
#             self.address = input("write host:"), int(input("write port"))
#             reactor.callInThread(self.send_message)
#         else : 
#             print(addr, ":" , datagram)
    
#     def send_message(self):
#         while True:
#             self.transport.write(input(':::').encode('utf-8'))

# if __name__ == '__main__':
#     port = randint(1000,5000)
#     reactor.listenUDP(port,Client('localhost',port))
#     reactor.run()





