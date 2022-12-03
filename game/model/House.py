from game.model.building import Building

class House(Building):
    def __init__(self):
        super().__init__()
        self.type = "house"