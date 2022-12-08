import random


class EngeneerPost:
    def __init__(self, case, citoyen, route_voisine):
        self.case = case
        self.citoyen = citoyen
        self.occupant = 0
        self.damage = 0
        self.route_voisine = route_voisine

    def get_citoyen(self):
        return self.citoyen

    def get_damage(self):
        return self.damage

    def get_route_voisine(self):
        return self.route_voisine

    def add_damage(self):
        if (random.randint(0, 1)):
            self.damage += random.randint(0, 5)

    def set_occupant(self, nb_occupant):
        self.occupant = 5

    def set_sprite(self, sprite):
        self.case.set_tile(sprite)
