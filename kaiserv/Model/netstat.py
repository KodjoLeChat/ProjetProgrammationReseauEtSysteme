import socket

class TcpClient:
    def __init__(self, connecting=False):
        self.server_address = "127.0.0.1"
        self.port = 2024
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = 1024
        self.connecting = connecting

    @staticmethod
    def read_config(config_file):
        with open(config_file, 'r') as file:
            address = file.readline().strip()
            port = int(file.readline().strip())
        return address, port

    def connect(self):
        self.client_socket.connect((self.server_address, self.port))
        code_con = 123
        message = f"connection established {code_con}\n"
        self.client_socket.sendall(message.encode())
        print(f"{message.strip()}")

    def send(self, message):
        self.client_socket.sendall(message.encode())
        print(f"{message.strip()}")

    def receive(self):
        data = self.client_socket.recv(self.buffer_size)

        try:
            text = data.decode('utf-8')  # Try to decode as UTF-8
            print(f"Received UTF-8 Text: {text}")
            return text
        except UnicodeDecodeError:
            # Handle binary data (file content or serialized data)
            print(f"Received Binary Data: {data}")
            return data

    def receive_forever(self):
        try:
            while True:
                message = self.receive()
                if isinstance(message, str):
                    # If the message is a string, write it as is
                    with open("onlineWorld.txt", "w") as file:
                        file.write(message)
                else:
                    # If the message is binary data, write it in binary mode
                    with open("onlineWorld.sav", "wb") as file:
                        file.write(message)
                break  # Remove this break if you want to keep receiving messages
        except KeyboardInterrupt:
            print("Receiving stopped.")

    def close(self):
        self.client_socket.close()
        print("Connection closed.")

# Example usage
'''
if __name__ == "__main__":
    client = TcpClient(connecting=True)
    client.connect()
    client.send("Hello, server! from player2")
    
    client.receive_forever()
    client.receive()
    
    print("end")
    client.close()
'''
