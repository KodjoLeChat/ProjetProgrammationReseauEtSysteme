import pygame
from game.model.settings import TILE_SIZE


class Mouse:

    def __init__(self, wigth, height, world):
        self.wigth = wigth
        self.height = height
        self.world = world
        self.mouse_image = pygame.image.load("C3_sprites/C3/Housng1a_00001.png")
        self.image_rect = self.mouse_image.get_rect()


    def update_clicking_selecting(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()
        self.image_rect.x = mouse_pos[0]-TILE_SIZE/2
        self.image_rect.y = mouse_pos[1]-TILE_SIZE/2

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                tile = self.world.world[x][y]
                if mouse_action[0]:
                    if tile.get_case_rect().collidepoint(mouse_pos):
                        pass
