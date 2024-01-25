import socket
import selectors
import time

class TcpClient:
    def __init__(self):
        self.server_address = "127.0.0.1"
        self.port = 2024
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.client_socket, selectors.EVENT_READ | selectors.EVENT_WRITE)

    def connect(self):
        self.client_socket.connect((self.server_address, self.port))
        code_con = 123
        message = f"connection established {code_con}\n"
        # the following print message should go to a log file
        # print(f"{message.strip()}")

    def send(self, message):
        self.client_socket.sendall(message.encode())
        print(f"{message.strip()}")

    def receive(self):
        events = self.selector.select(timeout=None)
        
        for key, mask in events:
            if mask & selectors.EVENT_READ:
                data = key.fileobj.recv(self.buffer_size)
                if data:
                    try:
                        text = data.decode('utf-8')  # Try to decode as UTF-8
                        # the following print to go to a log file
                        # print(f"Received UTF-8 Text: {text}")
                        return text
                    except UnicodeDecodeError:
                        # Handle binary data (file content or serialized data)
                        print(f"Received Binary Data: {data}")
                        return data

    def close(self):
        self.selector.unregister(self.client_socket)
        self.client_socket.close()


# Exemple d'utilisation :
client = TcpClient()
client.connect()
count = 0
n = 0
while 1:
    client.send("Hello\n")
    while n < 100:
        print(f"test {n} - ")
        time.sleep(1)
    response = client.receive()
    print(f"Je recois {response}\n")
    count = count + 1
    time.sleep(5)

client.close()
