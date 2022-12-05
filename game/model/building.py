import pygame


class Building:
    def __init__(self):
        self.damage = 0
        self.occupant = 0

    def get_damage(self):
        return self.damage

    def get_occupant(self):
        return self.occupant

    def add_damage(self,damage):
        self.damage += damage

    def set_occupant(self, nb_occupant):
        self.occupant = nb_occupant
