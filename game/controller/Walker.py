class Migrant:
    def __init__(self, pos_x, pos_y, home_x, home_y, path, sprite):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.home_x = home_x
        self.home_y = home_y
        self.sprite = sprite
        self.path = path
        self.path_retour = []

    def move_to_home(self):
        if self.path is not None:
            if len(self.path) != 0:
                coord = self.path.pop(0)
                self.pos_x, self.pos_y = coord
                self.path_retour.insert(0,coord)
            elif self.sprite == "engineer":
                self.path = self.path_retour
                self.path.pop(0)
                self.path_retour = []



    def get_path(self):
        return self.path

    def get_pos(self):
        return self.pos_x, self.pos_y

    def get_home_pos(self):
        return self.home_x, self.home_y

    def get_sprite(self):
        return self.sprite

    def get_time(self):
        return self.time

    def set_path(self,path):
        self.path = path