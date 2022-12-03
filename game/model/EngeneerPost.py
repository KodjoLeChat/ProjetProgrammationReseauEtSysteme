from game.model.building import Building

class EngineerPost(Building):
    def __init__(self):
        super().__init__()
        self.type = "engineer"