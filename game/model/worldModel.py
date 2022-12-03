import pygame as pg
from game.model.case import Case
from game.model.Ressources import Ressources
import pygame.event

class WorldModel:
    
    def __init__(self, world):
        # World
        self.world = world

        # Ressources
        #self.ressources = Ressources(0, 0, 0, 0, 0, 0)

        # list coords Routes
        self.list_grid_pos_road = set()

        # list coords Bulding
        self.list_grid_pos_selection = set()

    def get_case(self, i, j):
        return self.world[i][j]

    def get_list_grid_pos_road(self):
        return self.list_grid_pos_road

    def set_list_grid_pos_road(self,list_grid_pos_road):
        self.list_grid_pos_road = list_grid_pos_road

    def get_list_grid_pos_selection(self):
        return self.list_grid_pos_selection

    def set_list_grid_pos_selection(self,list_grid_pos_selection):
        self.list_grid_pos_selection = list_grid_pos_selection

    def add_list_grid_pos_road(self, grid_pos_road):
        self.list_grid_pos_road.add(grid_pos_road)

    def add_list_grid_pos_selection(self, grid_pos_selection):
        self.list_grid_pos_selection.add(grid_pos_selection)

    def set_case_image_by_coord(self, coord, sprite_name):
        x, y = coord
        self.world[x][y].set_tile(sprite_name)

    def diff_update_road(self,ensemble):
        self.list_grid_pos_road.difference_update(ensemble)
