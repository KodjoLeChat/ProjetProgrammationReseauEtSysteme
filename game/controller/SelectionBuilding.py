import pygame
import math


class SelectionBuilding:

    def __init__(self, start, worldModel):
        self.start = start
        self.worldModel = worldModel

    def add_grid_pos(self, grid_pos):
        temp_list = set()
        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(grid_pos[0], self.start[0] + 1):
                for y in range(grid_pos[1], self.start[1] + 1):
                    self.worldModel.add_list_grid_pos_building((x, y))
                    temp_list.add((x, y))
        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(grid_pos[0], self.start[0] + 1):
                for y in range(self.start[1], grid_pos[1]):
                    self.worldModel.add_list_grid_pos_building((x, y))
                    temp_list.add((x, y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(self.start[0], grid_pos[0] + 1):
                for y in range(grid_pos[1], self.start[1] + 1):
                    self.worldModel.add_list_grid_pos_building((x, y))
                    temp_list.add((x, y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(self.start[0], grid_pos[0] + 1):
                for y in range(self.start[1], grid_pos[1] + 1):
                    self.worldModel.add_list_grid_pos_building((x, y))
                    temp_list.add((x, y))
        return temp_list


    def add_grid_pos_to_erase(self, grid_pos):
        temp_list = set()
        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(grid_pos[0], self.start[0] + 1):
                for y in range(grid_pos[1], self.start[1] + 1):
                    temp_list.add((x, y))
        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(grid_pos[0], self.start[0] + 1):
                for y in range(self.start[1], grid_pos[1]):
                    temp_list.add((x, y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(self.start[0], grid_pos[0] + 1):
                for y in range(grid_pos[1], self.start[1] + 1):
                    temp_list.add((x, y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(self.start[0], grid_pos[0] + 1):
                for y in range(self.start[1], grid_pos[1] + 1):
                    temp_list.add((x, y))
        return temp_list

