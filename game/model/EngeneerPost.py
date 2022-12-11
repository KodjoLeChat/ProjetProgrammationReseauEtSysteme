import random


class EngeneerPost:
    def __init__(self, case, citoyen, route_voisine,sprite_name):
        self.case = case
        self.citoyen = citoyen
        self.sprite_name = sprite_name
        self.occupant = 0
        self.route_voisine = route_voisine

    def get_citoyen(self):
        return self.citoyen
    def get_sprite_name(self):
        return self.sprite_name

    def get_route_voisine(self):
        return self.route_voisine
    def set_occupant(self, nb_occupant):
        self.occupant = 5

    def set_sprite(self, sprite):
        self.case.set_tile(sprite)
