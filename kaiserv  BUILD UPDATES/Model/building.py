import psutil
import json
import datetime
import random
# représente les bâtiments
# tout ce qui fait partie de la carte, même l'herbe
class Building:
    nbBuilding = 0
    # on affecte des informations permettant d'ajuster le comportement dans le jeu
    def __init__(self, name, can_be_erase, can_constructible_over, can_be_walk_through, square_size):
        self.name                   = name                   # le nom du bâtiment représenté ( herbe, arbre, route, etc.)
        self.can_be_erase           = can_be_erase           # le bâtiment peut-il être effacer, action de clear
        self.can_constructible_over = can_constructible_over # peut-on construire par dessus le bâtiment, ( herbe )
        self.can_be_walk_through    = can_be_walk_through    # peut-on passer à travers ce bâtiments, ( ex: False pour l'eau )
        self.square_size            = square_size            # inutile, pour le moment, anticipation de tuile d'une certaine taille
        self.position_reference = None                       # emplacement sur la carte
        self.id = Building.nbBuilding+1
        Building.nbBuilding = self.id
        self.owner                  = None
        self.current_time = datetime.datetime.now()
        self.check_interval = 10
        self.last_action_time = self.current_time
        self.life = 100                      # la vie du bâtiment
        self.check_fire = False

    def lower_hp(self):
        # Reduce the HP of the building
        self.hp -= 10  # You can adjust the amount by which the HP is lowered
        if self.hp <= 0:
            # Building is destroyed
            self.owner = None
            self.hp = 0

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
    
    def set_mac_address(self):
        interfaces = psutil.net_if_addrs()
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    self.owner = addr.address
                    #print(self.owner)
                    return addr.address
        return None

    def to_json(self):
        building_dict = self.__dict__.copy()
        building_dict['current_time'] = self.current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        building_dict['last_action_time'] = self.last_action_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        return json.dumps(building_dict, indent=4)

    def add_to_json(self):
        # Serialize the current building to JSON
        building_json = self.to_json()

        try:
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
            json.dump(data, file, indent=4)


    @classmethod
    def from_json(cls, json_file="transfer.json", line_number=-1):
        try:
            with open(json_file, "r") as file:
                lines = file.readlines()
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, return None
            return None, -1  # Return -1 to indicate that no line was read

        if line_number < 0:
            # If line_number is negative, start from the end of the file
            line_number = len(lines) + line_number

        if 0 <= line_number < len(lines):
            json_string = lines[line_number]
            json_dict = json.loads(json_string)
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
            
            # Return the building object and the last line number read
            return building, line_number

        # Return None and -1 if the specified line number is out of bounds
        return None, -1
