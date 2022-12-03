class Fire: 
    def __init__(self, world):
        '''get world parameters'''
        self.world = world
        '''list building in fire'''
        self.fire = []




    def update(self):
        if self.world.data:
                i = random.randint(0, len(self.world.data)-1)
                x = self.world.data[i]["x"]
                y = self.world.data[i]["y"]
                if self.world.world[x][y].get_tile() == 'hud_house_sprite':
                    if random.randint(0,100) < 50:
                        self.world.world[x][y].set_tile('fire')
                        temp = {
                            "image": self.world.world[x][y].get_tile(),
                            "x": x,
                            "y": y
                        }
                        self.fire.append(temp)
