import pygame
from random import randint

class TextShow:
    '''make move a specific sprite appear on world'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.speed = 3

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, world):
        self.rect.x += self.speed
        if self.rect.x > world.width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = world.width
        if self.rect.y > world.height:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = world.height

    def move(self, x, y, world):
        self.rect.x += x
        self.rect.y += y
        if self.rect.x > world.width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = world.width
        if self.rect.y > world.height:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = world.height

    def set_position(self, x, y, world):
        self.rect.x = x
        self.rect.y = y
        if self.rect.x > world.width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = world.width
        if self.rect.y > world.height:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = world.height

    def set_color(self, color):
        self.color = color

    def set_speed(self, speed):
        self.speed = speed

    def set_size(self, size):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, size, size)

    def get_position(self):
        return self.rect.x, self.rect.y

    def get_size(self):
        return self.rect.width, self.rect.height

    def get_color(self):
        return self.color

    def get_speed(self):
        return self.speed

    def get_rect(self):
        return self.rect

    def get_rect_x(self):
        return self.rect.x