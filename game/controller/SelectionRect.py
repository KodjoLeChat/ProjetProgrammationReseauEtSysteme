import pygame


class SelectionRect:

    def __init__(self, screen, start):
        self.square = None
        self.screen = screen
        self.start = start

    def updateRect(self, now):
        x, y = self.start
        mx, my = now

        if mx < x:
            if my < y:
                rect = pygame.Rect(mx, my, x - mx, y - my)
            else:
                rect = pygame.Rect(mx, y, x - mx, my - y)
        elif my < y:
            rect = pygame.Rect(x, my, mx - x, y - my)
        else:
            rect = pygame.Rect(x, y, mx - x, my - y)
        self.square = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
        return self.square

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 0, 255), self.square)


    def collision(self,coord2):
        return (self.square[0][0] < coord2[1][0] and
                self.square[1][0] > coord2[0][0] and
                self.square[0][1] < coord2[3][1] and
                self.square[3][1] > coord2[0][1])