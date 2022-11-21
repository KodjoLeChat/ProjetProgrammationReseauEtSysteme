from game import *
import pygame

class Walker:

    def __init__(self, clock, name, sprite, pos_x,pos_y):

        #caractéristiques
        self.name = name
        self.sprite = sprite
        self.clock = clock

        self.position = [pos_x, pos_y]



    def path(self, new_pos_x, new_pos_y):

        deplacement_x = new_pos_x - self.position[0]
        deplacement_y = new_pos_y - self.position[1]

        path_x = deplacement_x // self.position[0]
        path_y = deplacement_y // self.position[1]


