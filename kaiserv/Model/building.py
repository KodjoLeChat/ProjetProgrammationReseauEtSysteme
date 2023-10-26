import psutil
import pygame
import datetime
import json
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


    def elapsed_time(self, ressource):
        self.current_time = datetime.datetime.now()
        elapsed_time_s = (self.current_time - self.last_action_time).total_seconds()
        if elapsed_time_s >= self.check_interval:
            self.moneyEarned(ressource)
            self.last_action_time = self.current_time

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
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        building = cls.__new__(cls)
        building.__dict__.update(json_dict)
        return building