import pygame as pg

class Zoom:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zoom = 1
        self.min_zoom = 0.5
        self.max_zoom = 2
        self.zoom_speed = 0.1
        self.zoom_rect = pg.Rect(0, 0, self.width, self.height)

    def zoom_in(self):
        if self.zoom < self.max_zoom:
            self.zoom += self.zoom_speed

    def zoom_out(self):
        if self.zoom > self.min_zoom:
            self.zoom -= self.zoom_speed

    def update(self):
        self.zoom_rect.width = self.width * self.zoom
        self.zoom_rect.height = self.height * self.zoom

    def draw(self, screen):
        pg.draw.rect(screen, (255, 0, 0), self.zoom_rect, 2)

    def get_zoom(self):
        return self.zoom

    def get_zoom_rect(self):
        return self.zoom_rect
