from game import *
import pygame

class Walker:

    def __init__(self, world, clock):

        self.world = world
        self.sprite = self.world.load_images()["walker"]
        self.clock = clock
        self.roads = self.world.get_list_grid_pos_road()
        self.position = (pos_x, pos_y)

        #self.role =


    def pathfinding(self):

    def move(self):






