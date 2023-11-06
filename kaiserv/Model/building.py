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
    
    '''building convert to json all builds'''
    def convert_to_json(self):
        return {
            "name": self.name,
            "can_be_erase": self.can_be_erase,
            "can_constructible_over": self.can_constructible_over,
            "can_be_walk_through": self.can_be_walk_through,
            "square_size": self.square_size,
            "position_reference": self.position_reference,
            "owner": self.owner,
            "id": self.id
        }
    
    def add_to_json(self):
        data = self.convert_to_json()
        with open("transfer.json", 'a') as file:
            file.write(json.dumps(data) + '\n')
    
    def convert_from_json(self, json):
        self.name = json["name"]
        self.can_be_erase = json["can_be_erase"]
        self.can_constructible_over = json["can_constructible_over"]
        self.can_be_walk_through = json["can_be_walk_through"]
        self.square_size = json["square_size"]
        self.position_reference = json["position_reference"]
        self.owner = json["owner"]
        self.id = json["id"]
        return self
    