import pygame


class SelectionRect:

    def __init__(self, screen, start):
        self.rect = None
        self.screen = screen
        self.start = start

    def updateRect(self, now):
        x, y = self.start
        mx, my = now

        if mx < x:
            if my < y:
                self.rect = pygame.Rect(mx, my, x - mx, y - my)
            else:
                self.rect = pygame.Rect(mx, y, x - mx, my - y)
        elif my < y:
            self.rect = pygame.Rect(x, my, mx - x, y - my)
        else:
            self.rect = pygame.Rect(x, y, mx - x, my - y)

        return self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 255), self.rect)
