import pygame
import math

class SelectionRect:

    def __init__(self, screen, start):
        self.square = None
        self.screen = screen
        self.start = start
        self.rect = None

    def updateRect(self, now):
        x, y = self.start
        mx, my = now

        if mx < x:
            if my < y:  # en haut a gauche
                self.rect = pygame.Rect(mx, my, x - mx, y - my)
                self.square = [
                    (mx, my),
                    (mx + (x - mx), my),
                    (mx + (x - mx), my + (y - my)),
                    (mx, my + (y - my))
                ]
            else:  # en bas a gauche
                self.rect = pygame.Rect(mx, y, x - mx, my - y)
                self.square = [
                    (mx, y),
                    (mx + (x - mx), y),
                    (mx + (x - mx), y + (my - y)),
                    (mx, y + (my - y))
                ]
        elif my < y:  # en haut à droite
            self.rect = pygame.Rect(x, my, mx - x, y - my)
            self.square = [
                (x, my),
                (x + (mx - x), my),
                (x + (mx - x), my + (y - my)),
                (x, my + (y - my))
            ]
        else: # en bas a droite
            self.rect = pygame.Rect(x, y, mx - x, my - y)
            self.square = [
                (x, y),
                (x + (mx - x), y),
                (x + (mx - x), y + (my - y)),
                (x, y + (my - y))
            ]


        #self.square = [self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft]
        return self.square

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 0, 255), self.square)

    def cart_to_iso(self,x,y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y