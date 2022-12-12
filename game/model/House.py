import random


class House():
    def __init__(self, case, citoyen, route_voisine,sprite):
        self.case = case
        self.sprite_name = sprite
        self.citoyen = citoyen
        self.occupant = 0
        self.damage = 0
        self.fire = 0
        self.route_voisine = route_voisine
        self.pillar = {"bottom_pillar":1, "body_pillar":0,"head_pillar":1}
        self.bottom_pillard = "bottom_white_pillar"
        self.body_pillard = "body_white_pillar"
        self.head_pillard = "head_white_pillar"
    def get_citoyen(self):
        return self.citoyen

    def get_pillar(self):
        return self.pillar

    def get_head_pillard(self):
        return self.head_pillard

    def get_body_pillard(self):
        return self.body_pillard

    def get_bottom_pillard(self):
        return self.bottom_pillard

    def get_damage(self):
        return self.damage

    def get_fire(self):
        return self.fire

    def get_route_voisine(self):
        return self.route_voisine

    def get_sprite_name(self):
        return self.sprite_name

    def add_damage(self):
        if random.randint(0, 1):
            self.damage += 2
        if self.damage % 10 == 0:
            self.bottom_pillard = "bottom_white_pillar"
            self.body_pillard = "body_white_pillar"
            self.bottom_pillard = "head_white_pillar"
            self.pillar["body_pillar"] +=1
        if self.damage %30 == 0:
            self.bottom_pillard = "bottom_orange_pillar"
            self.body_pillard = "body_orange_pillar"
            self.bottom_pillard = "head_orange_pillar"
        if self.damage %50 == 0:
            self.bottom_pillard = "bottom_orange_red_pillar"
            self.body_pillard = "body_orange_red_pillar"
            self.bottom_pillard = "head_orange_red_pillar"
        if self.damage %85 == 0:
            self.bottom_pillard = "bottom_red_pillar"
            self.body_pillard = "body_red_pillar"
            self.bottom_pillard = "head_red_pillar"


    def pillard_to_zero(self):
        self.pillar = {"bottom_pillar":0, "body_pillar":0,"head_pillar":0}

    def reset_pillard(self):
        self.pillar = {"bottom_pillar":1, "body_pillar":0,"head_pillar":1}

    def reset_damage(self):
        self.damage = 0

    def set_occupant(self, nb_occupant):
        self.occupant = 5

    def set_sprite(self, sprite):
        self.case.set_tile(sprite)

    def add_fire(self):
        if random.randint(0, 1):
            self.fire += 5
