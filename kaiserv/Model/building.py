import psutil
import json
import datetime
import random
import pytz 
# représente les bâtiments
# tout ce qui fait partie de la carte, même l'herbe
class Building:
    nbBuilding = 0
    # on affecte des informations permettant d'ajuster le comportement dans le jeu
    def __init__(self, name, can_be_erase, can_constructible_over, can_be_walk_through, square_size,owner=None):
        self.name                   = name                   # le nom du bâtiment représenté ( herbe, arbre, route, etc.)
        self.can_be_erase           = can_be_erase           # le bâtiment peut-il être effacer, action de clear
        self.can_constructible_over = can_constructible_over # peut-on construire par dessus le bâtiment, ( herbe )
        self.can_be_walk_through    = can_be_walk_through    # peut-on passer à travers ce bâtiments, ( ex: False pour l'eau )
        self.square_size            = square_size            # inutile, pour le moment, anticipation de tuile d'une certaine taille
        self.position_reference = None                       # emplacement sur la carte
        self.id = Building.nbBuilding+1
        Building.nbBuilding = self.id
        self.current_time = datetime.datetime.now()
        self.check_interval = 1
        self.last_action_time = self.current_time
        self.life = 100                      # la vie du bâtiment
        self.check_fire = False
        self.owner = owner
        if self.owner is None:
            self.owner = "rayaneGamer"


    def lower_hp(self):
        # Reduce the HP of the building
        self.hp -= 10  # You can adjust the amount by which the HP is lowered
        if self.hp <= 0:
            # Building is destroyed
            self.owner = None
            self.hp = 0
    def set_username(self):
        return "rayaneGamer"

    def elapsed_time(self, ressource):
        self.current_time = datetime.datetime.now()
        elapsed_time_s = (self.current_time - self.last_action_time).total_seconds()
        if elapsed_time_s >= self.check_interval:
            self.moneyEarned(ressource)
            self.last_action_time = self.current_time
            random_number = random.randint(1, 10)
            if random_number == 10:
                self.check_fire = True
            

    def moneyEarned(self,ressource):
        ressource.dinars+=100
        
    # permet d'affecter la position de reference
    def set_position_reference(self, position_reference):
        self.position_reference = position_reference

    # utile pour le pathfinding 
    def get_canbewalkthrough_into_integer(self):
        return 0 if self.can_be_walk_through else 1
    

    def to_json(self):
        building_dict = self.__dict__.copy()
        building_dict['current_time'] = self.current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        building_dict['last_action_time'] = self.last_action_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        return json.dumps(building_dict, indent=4)

    def add_to_json(self):
        # Serialize the current building to JSON
        building_json = self.to_json()
        
        ###########################################
        # function commented Philemon         #####
        # and add of print below
        #                             11 fev 2024
        ############################################
        #print(f"building {self.name} to json is: {building_json}")
        return building_json
        ''''try:
            # Load existing data from "transfer.json" if it exists
            with open("transfer.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist yet or is empty, create an empty data structure
            data = []

        # Append the current building data to the list
        data.append(json.loads(building_json))

        # Write the updated data back to "transfer.json"
        with open("transfer.json", "w") as file:
            json.dump(data, file, indent=4)'''


    @classmethod
    def from_json(cls, json_buffer):
        try:
            # Load the JSON data from the provided buffer
            json_dict = json.loads(json_buffer)
            
            # Create a new Building object using the JSON data
            building = Building(
                json_dict['name'],
                json_dict['can_be_erase'],
                json_dict['can_constructible_over'],
                json_dict['can_be_walk_through'],
                json_dict['square_size']
            )
            building.position_reference = json_dict['position_reference']
            building.id = json_dict['id']
            building.owner = json_dict['owner']
            building.current_time = datetime.datetime.strptime(json_dict['current_time'], '%Y-%m-%d %H:%M:%S.%f')
            building.check_interval = json_dict['check_interval']
            building.last_action_time = datetime.datetime.strptime(json_dict['last_action_time'], '%Y-%m-%d %H:%M:%S.%f')
            
            # Return the created building object
            return building
        except json.JSONDecodeError:
            # If there is an error decoding the JSON data, return None
            return None
