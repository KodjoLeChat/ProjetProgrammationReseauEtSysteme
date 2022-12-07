class House():
    def __init__(self, citoyen,route_voisine):
        self.type = "house"
        self.citoyen = citoyen
        self.occupant = 0
        self.damage = 0
        self.route_voisine = route_voisine

    def get_citoyen(self):
        return self.citoyen

    def add_damage(self):
        self.damage += 5

    def set_occupant(self, nb_occupant):
        self.occupant = 5
    def get_route_voisine(self):
        return self.route_voisine