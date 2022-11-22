'''CREATE CLASS TIMER FOR COUNTING TIME'''
import pygame as pg
import time

class Timer:

    def __init__(self):
        self.start_time = time.time()
        self.time = 0

    def update(self, test):
        if test == 0:
            test = 1
        self.time = (time.time() - self.start_time)*test

    def get_time(self):
        return self.time

    def reset(self):
        self.start_time = time.time()
        
