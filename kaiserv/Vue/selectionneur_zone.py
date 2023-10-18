import pygame
from .basic_action import Basic_Action

# permet de gérer la selection d'une zone, classe mère pour les actions de clear et de adding_building
class SelectionneurZone(Basic_Action):
    OPACITY = 180
    
    def __init__(self, carriere):
        Basic_Action.__init__(self, carriere)
        self.grid_postition_to_place = None
        self.grid_to_draw = [] # les emplacements selectionnés

    def draw(self):
        size_of_original_image = self.original_surface.get_size()
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        self.grid_to_draw = []
        # on affiche pour chaque emplacement sélectionné, la zone choisis
        if self.pos_start is not None:
            for i in range(self.coordinate[0][0], self.coordinate[1][0]+1):
                for j in range(self.coordinate[0][1], self.coordinate[1][1]+1):
                    self.grid_postition_to_place = grid = (round(i), round(j))
                    self.grid_to_draw.append(grid)
        else:
            # sinon on affiche que pour la case survolé
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click)

            self.grid_to_draw.append(self.grid_position_without_first_click)
        for grid in self.grid_to_draw:
            if self.path != "assets/upscale_house/Housng1a_00045.png" or self.carriere.controleur.check_if_construction_possible_on_grid(grid):
                self.draw_for_an_image(grid)
