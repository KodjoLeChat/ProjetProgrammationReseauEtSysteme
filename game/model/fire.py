import pygame as pg
import random


class Fire: 
    def __init__(self, world):
        '''probability calculated every second to ignite a random tile'''
        #self.fire = pg.transform.scale(self.fire, (self.world.width, self.world.height))
        #self.fire = pg.transform.rotate(self.fire, random.randint(0, 360))
        #self.fire = pg.transform.flip(self.fire, random.randint(0, 1), random.randint(0, 1))
        '''get world parameters'''
        self.world = world



    def update(self):
        if self.world.data:
                i = random.randint(0, len(self.world.data)-1)
                x = self.world.data[i]["x"]
                y = self.world.data[i]["y"]
                if self.world.world[x][y].get_tile() == 'hud_house_sprite':
                    if random.randint(0,100) < 50:
                        self.world.world[x][y].set_tile('fire')

