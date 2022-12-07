class Migrant:

    def __init__(self, pos_x, pos_y, home_x, home_y, path):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.home_x = home_x
        self.home_y = home_y

        self.path = path

    def move_to_home(self):
        if self.path is not None and len(self.path) != 0:
            self.pos_x, self.pos_y = self.path.pop(0)

    def get_pos(self):
        return self.pos_x, self.pos_y
