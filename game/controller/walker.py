
import pygame


def cart_to_iso(x, y):
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y
class Migrant:

    def __init__(self, world, home_x, home_y, sprite):

        self.world = world
        self.sprite = sprite

        self.pos_x = self.world.get_case(0, 32).get_render_pos()[0]
        self.pos_y = self.world.get_case(0, 32).get_render_pos()[1]

        self.home_x = home_x
        self.home_y = home_y

        # self.path = pathfinding(self, self.pos_x, self.pos_y, home_x, home_y)

        # self.role =

    def move_to_home(self):

        move_x = self.home_x - self.pos_x
        move_y = self.home_y - self.pos_y

        if move_x > 0:
            self.pos_x += cart_to_iso(1, 0)[0]
        if move_x < 0:
            self.pos_y -= cart_to_iso(1, 0)[0]

        if move_y > 0:
            self.pos_y += cart_to_iso(0, 1)[1]
        if move_y < 0:
            self.pos_y -= cart_to_iso(0, 1)[1]
