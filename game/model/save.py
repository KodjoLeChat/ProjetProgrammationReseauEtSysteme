import pygame as pg
import time
import json

class Save:
    def __init__(self, world):
        self.world = world
        self.data = {}
        self.data["world"] = []

    def save(self):
        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                self.data["world"].append({
                    "x": x,
                    "y": y,
                    "tile": self.world.world[x][y].tile,
                })
        with open('save.json', 'w') as outfile:
            json.dump(self.data, outfile)
        print("Saved")
        
    def load(self):
        with open('save.json') as json_file:
            self.data = json.load(json_file)
        for i in self.data["world"]:
            self.world.world[i["x"]][i["y"]].tile = i["tile"]
        print("Loaded")