import pygame
import math

class SelectionRect:

    def __init__(self, start):
        self.start = start
        self.list_grid_pos = {start}


    def add_grid_pos(self,grid_pos):
        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(grid_pos[0],self.start[0]+1):
                self.list_grid_pos.add((x,grid_pos[1]))
            for y in range(grid_pos[1],self.start[1]+1):
                self.list_grid_pos.add((grid_pos[0],y))
        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:
            for x in range(grid_pos[0],self.start[0]+1):
                self.list_grid_pos.add((x,grid_pos[1]))
            for y in range(grid_pos[1],self.start[1]+1,-1):
                self.list_grid_pos.add((grid_pos[0],y))
        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:
            for x in range(grid_pos[0],self.start[0]+1,-1):
                self.list_grid_pos.add((x,grid_pos[1]))
            for y in range(grid_pos[1],self.start[1]+1):
                self.list_grid_pos.add((grid_pos[0],y))
        else:
            for x in range(grid_pos[0], self.start[0]+1,-1):
                self.list_grid_pos.add((x, grid_pos[1]))
            for y in range(grid_pos[1], self.start[1]+1,-1):
                self.list_grid_pos.add((grid_pos[0], y))

    def get_list_grid_pos(self):
        return self.list_grid_pos
