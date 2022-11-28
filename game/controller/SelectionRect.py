import pygame
import math


class SelectionRect:

    def __init__(self, start, worldModel):
        self.start = start
        self.worldModel = worldModel
        self.list_grid_pos = {start}

    def add_grid_pos(self, grid_pos):

        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(grid_pos[0], self.start[0] + 1):
                for y in range(grid_pos[1], self.start[1] + 1):
                    self.worldModel.add_list_grid_pos_selection((x, y))
        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(grid_pos[0], self.start[0] + 1):
                for y in range(self.start[1], grid_pos[1]):
                    self.worldModel.add_list_grid_pos_selection((x, y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(self.start[0], grid_pos[0] + 1):
                for y in range(grid_pos[1], self.start[1] + 1):
                    self.worldModel.add_list_grid_pos_selection((x, y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(self.start[0], grid_pos[0] + 1):
                for y in range(self.start[1], grid_pos[1] + 1):
                    self.worldModel.add_list_grid_pos_selection((x, y))

    def get_list_grid_pos(self):
        return self.list_grid_pos
