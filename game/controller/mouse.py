import pygame


class Mouse:

    def __init__(self,wigth,height,world):
        self.wigth = wigth
        self.height = height
        self.world = world

    def update_clicking_hud(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                tile = self.world.world[x][y]
                print(tile.get_cart_rect())
                if tile.get_cart_rect().collidepoint(mouse_pos):
                    tile.set_tile("block")




