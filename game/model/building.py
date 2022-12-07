import pygame


class Building:
    def __init__(self, citoyen):
        self.damage = 0
        self.fire = 0
        self.citoyen = citoyen
        self.fire = False

    def get_damage(self):
        return self.damage

    def get_citoyen(self):
        return self.citoyen

    def get_fire(self):
        return self.fire

    def add_damage(self,damage):
        self.damage += damage

    def add_fire(self,fire):
        self.fire += fire

    def set_occupant(self, nb_occupant):
        self.occupant = nb_occupant
