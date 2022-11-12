import pygame
import math

class SelectionRect:

    def __init__(self, start):
        self.start = start
        self.list_grid_pos = {start}


    def add_grid_pos(self,grid_pos):
        list_grid_pos = set()
        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(grid_pos[0],self.start[0]+1):
                for y in range(grid_pos[1],self.start[1]+1):
                    list_grid_pos.add((x,y))
        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(grid_pos[0],self.start[0]+1):
                for y in range(self.start[1],grid_pos[1]):
                    list_grid_pos.add((x,y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(self.start[0],grid_pos[0]+1):
                for y in range(grid_pos[1],self.start[1]+1):
                    list_grid_pos.add((x,y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(self.start[0], grid_pos[0]+1):
                for y in range(self.start[1], grid_pos[1]+1):
                    list_grid_pos.add((x, y))
        self.list_grid_pos = list_grid_pos

    def get_list_grid_pos(self):
        return self.list_grid_pos