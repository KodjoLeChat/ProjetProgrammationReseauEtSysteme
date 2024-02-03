import socket
import json
import threading

class UdpClient:
    def __init__(self):
        self.multicast_group = "224.0.0.1"
        self.port = 8888
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def read_config(config_file):
        with open(config_file, 'r') as file:
            address = file.readline().strip()
            port = int(file.readline().strip())
        return address, port
    
    
    def send(self, message):
        if not isinstance(message, str):
            message = json.dumps(message)
        self.client_socket.sendto(message.encode('utf-8'), (self.multicast_group, self.port))
        print(f"{message.strip()}")

    def receive(self):
        try:
            data = self.client_socket.recvfrom(1024)
            try:
                text = data.decode('utf-8')  # Try to decode as UTF-8
                print(f"Received UTF-8 Text: {text}")
                return text
            except UnicodeDecodeError:
                # Handle binary data (file content or serialized data)
                print(f"Received Binary Data: {data}")
                return data
        except socket.error as e:
            return None

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
        receiving_thread = threading.Thread(target=self.receive_forever)
        receiving_thread.daemon = True
        receiving_thread.start()

    def receive_and_store(self):
        data = self.receive()
        if data:
            # Séparer les données reçues et les nettoyer
            data_list = data.split('\n')
            sanitized_data, sanitized_data_adding_building = self.data_sanitize(data_list)
            # Ajouter les données nettoyées aux listes appropriées
            self.received_data.extend(sanitized_data)
            self.received_data_ADDING_BUILDING.extend(sanitized_data_adding_building)
        self.start_receiving_thread()  # Démarrer un nouveau thread pour les prochaines données

    
    
    
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
if __name__ == "__main__":
    client = UdpClient()
    client.start_receiving_thread()

    while True:
        user_input = input("Enter a message: ")
        client.send(user_input)
    # Uncomment the following line if you want to close the client when finished
    # client.close()
