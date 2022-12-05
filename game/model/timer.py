'''CREATE CLASS TIMER FOR COUNTING TIME'''
import pygame as pg
import time

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.time = 0
        self.temp = 0


    def update(self, test):
        if test == 0:
            test = 1
        self.time = int((time.time() - self.start_time)*test)
        print(self.time)

    '''pause function timer'''
    def pause(self):
        self.start_time = time.time() - self.time

    def resume(self):
        self.start_time = time.time() - self.time

    def get_time(self):
        return self.time

    def reset(self):
        self.start_time = time.time()

    def time_multiple(self):
        if self.time % 100 == 0:
            self.temp = self.time
            return True
        else:
            return False