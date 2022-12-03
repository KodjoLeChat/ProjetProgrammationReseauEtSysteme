import pygame as pg
from game.model.case import Case
from game.model.Ressources import Ressources
import pygame.event
from game.model.settings import GRID_WIDTH, GRID_LENGTH


class WorldModel:

    def __init__(self, world):
        # World
        self.world = world

        # Ressources
        # self.ressources = Ressources(0, 0, 0, 0, 0, 0)

        # list coords Routes
        self.list_grid_pos_road = set()

        # list coords Bulding
        self.list_grid_pos_building = set()

        # list
        # self.matrice_building = [[0 for y in range(GRID_LENGTH)] for x in range(GRID_WIDTH)]

    def get_case(self, i, j):
        return self.world[i][j]

    def get_list_grid_pos_road(self):
        return self.list_grid_pos_road

    def set_list_grid_pos_road(self, list_grid_pos_road):
        self.list_grid_pos_road = list_grid_pos_road

    def get_list_grid_pos_building(self):
        return self.list_grid_pos_building

    def set_list_grid_pos_building(self, list_grid_pos_building):
        self.list_grid_pos_building = list_grid_pos_building

    def add_list_grid_pos_road(self, grid_pos_road):
        self.list_grid_pos_road.add(grid_pos_road)

    def add_list_grid_pos_building(self, grid_pos_selection):
        self.list_grid_pos_building.add(grid_pos_selection)

    def set_case_image_by_coord(self, coord, sprite_name):
        x, y = coord
        self.world[x][y].set_tile(sprite_name)

    def diff_update_road(self, ensemble):
        self.list_grid_pos_road.difference_update(ensemble)

    def diff_update_building(self, ensemble):
        self.list_grid_pos_building.difference_update(ensemble)
