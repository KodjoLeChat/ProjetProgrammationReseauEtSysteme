from game import *
import pygame

class Migrant:

    def __init__(self, world, home_x, home_y):

        self.world = world
        self.sprite = self.world.load_images()["walker"]

        self.pos_x = self.world.get_case(10,10).get_render_pos()[0]
        self.pos_y = self.world.get_case(10,10).get_render_pos()[1]

        self.home_x = home_x
        self.home_y = home_y

         #self.path = pathfinding(self, self.pos_x, self.pos_y, home_x, home_y)

        #self.role =

    def move_to_home(self, dest_x, dest_y):

        move_x = abs(self.home_x - self.pos_x)
        move_y = abs(self.home_y - self.pos_y)

        if self.pos_x <= move_x:
            self.pos_x += 1

        if self.pos_y <= move_y:
            self.pos_y += 1












