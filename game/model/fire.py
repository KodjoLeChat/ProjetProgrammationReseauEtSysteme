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
            for i in self.world.data:
                x = i["x"]
                y = i["y"]
                print('attention')
                if random.randint(0,100) < 99:
                    self.world.world[x][y].set_tile('fire')