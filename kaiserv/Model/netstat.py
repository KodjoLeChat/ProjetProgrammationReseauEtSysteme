import socket
import select
import json
import pickle
import threading
import re

class TcpClient:
    def __init__(self, connecting=False):
        self.server_address = "127.0.0.1"
        self.port = 2027
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.buffer_size = 1024
        self.connecting = connecting
        self.seen = {} # Dictionnaire pour suivre les combinaisons de grid_pos et timestamps déjà vues
        self.clear_data = []
        self.received_data = []  # List to store received data
        self.received_data_ADDING_BUILDING = []  # List to store received data ADDING BUILDING METHOD
        self.receiving_thread = None

    def check_and_send_duplicates(self):
        for item in self.received_data:
            grid_pos = tuple(item['grid_pos'])  # Convertit en tuple pour l'utiliser comme clé de dictionnaire
            timestamp = item['timestamp']  # 

            # Vérifie si la combinaison existe déjà
            if (grid_pos, timestamp) in self.seen:
                # Construit le message d'erreur
                message = {
                    "method": "invalid_action",
                    "grid_pos": grid_pos,
                    "timestamps": timestamp,
                    "Ressources": item['Ressources']  # Prend l'objet Ressources de l'élément actuel
                }
                #self.send(message)  # Appelle la méthode send avec le message
                return False
            else:
                self.seen[(grid_pos, timestamp)] = item  # Ajoute cette combinaison au dictionnaire seen
                return True

    @staticmethod
    def read_config(config_file):
        with open(config_file, 'r') as file:
            address = file.readline().strip()
            port = int(file.readline().strip())
        return address, port

    def connect(self):
        self.client_socket.connect((self.server_address, self.port))
        code_con = 123
        message = f"{code_con}\n"
        self.client_socket.sendall(message.encode())
        print(f"{message.strip()}")

    def send(self, message):
        if not isinstance(message, str):
            message = json.dumps(message)
        self.client_socket.sendall(message.encode('utf-8'))
        print(f"{message.strip()}")


    def receive(self):
        try:
            data = self.client_socket.recv(self.buffer_size)
            try:
                text = data.decode('utf-8')  # Try to decode as UTF-8
                #print(f"Received UTF-8 Text: {text}")
                return text
            except UnicodeDecodeError:
                # Handle binary data (file content or serialized data)
                print(f"Received Binary Data: {data}")
                return data


        except socket.error as e:
            return None


    def send_ready_signal(self):
        ready_signal = "READY_FOR_NEXT"
        self.client_socket.sendall(ready_signal.encode('utf-8'))
        print("Sent ready signal for next message")

    def data_sanitize(self, data_list):
        sanitized_data = []
        sanitized_data_adding_building = []  # Liste pour les données "Adding_Building"

        for item in data_list:
            try:
                start_index = item.find('{')
                end_index = item.rfind('}') + 1
                if start_index != -1 and end_index != -1:
                    # Extraire la sous-chaîne JSON
                    json_str = item[start_index:end_index]
                    json_item = json.loads(json_str)
                    if isinstance(json_item, dict) and "method" in json_item:
                        if json_item["method"] == "Adding_Building":
                            sanitized_data_adding_building.append(json_item)
                        else:
                            sanitized_data.append(json_item)
                else:
                    print(f"Aucun JSON valide trouvé dans l'élément : {item}")
            except json.JSONDecodeError:
                print(f"Erreur de décodage JSON pour l'élément : {item}")
                continue

        return sanitized_data, sanitized_data_adding_building
    def start_receiving_thread(self):
        if self.receiving_thread is not None and self.receiving_thread.is_alive():
            # If there's already a receiving thread running, do nothing
            return

        # Create and start a new thread for receiving data
        self.receiving_thread = threading.Thread(target=self.receive_and_store)
        self.receiving_thread.daemon = True
        self.receiving_thread.start()


    def receive_and_store(self):
        data = self.receive()
        if data:
            data_list = data.split('\n')
            sanitized_data, sanitized_data_adding_building = self.data_sanitize(data_list)
            self.received_data.extend(sanitized_data)
            self.received_data_ADDING_BUILDING.extend(sanitized_data_adding_building)
            #self.send_ready_signal()  # Signaliser prêt pour le prochain message
        self.start_receiving_thread()

                    
    '''def receive_loop(self):
        while True:
            data = self.receive_event()
            if data:
                # Process the data or store it to be processed in the main thread
                print("test")'''
            
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
