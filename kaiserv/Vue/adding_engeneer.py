from .basic_action import Basic_Action
import pygame

class AddingEngeneer(Basic_Action):
    def __init__(self, carriere):
        super().__init__(carriere)
    
    # permet de draw soit une case de pre-build, soit le bâtiment de l'ingénieur
    def draw(self):
        size_of_original_image = self.original_surface.get_size()
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        if self.grid_position_start != None and self.grid_position_end != None and self.carriere.controleur.check_if_construction_possible_on_grid(self.grid_position_start):
            self.image_to_draw = self.carriere.dictionnaire["engeneer"]
            size_image  = (self.image_to_draw.get_width(), self.image_to_draw.get_height())
            self.image_to_draw = pygame.transform.scale(self.image_to_draw, (size_image[0]*self.carriere.zoom.multiplier, size_image[1]*self.carriere.zoom.multiplier))
            self.draw_for_an_image(self.grid_position_start)
        else:
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE * self.carriere.zoom.multiplier, self.pos_without_first_click)
            if self.carriere.controleur.check_if_construction_possible_on_grid(self.grid_position_without_first_click):
                self.draw_for_an_image(self.grid_position_without_first_click)

    def events(self, event):
        super().events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:
            if self.carriere.controleur.check_if_construction_possible_on_grid(self.grid_position_start):
                stop_loop = False
                # si on peux construire sur la zone en question, alors on construit et on ajoute le migrant
                # on ne peux pas construire à moins de deux cases d'une route
                for num_lig in range(0, len(self.carriere.informations_tiles)):
                    for num_col in range(0, len(self.carriere.informations_tiles[num_lig])):
                        if stop_loop == False and self.carriere.informations_tiles[num_lig][num_col]["building"].name[0:5] == "route" and \
                           self.calcul_distance_to_grid(self.grid_position_start, (num_lig, num_col)) <= 2:
                                self.carriere.controleur.add_building_on_point(self.grid_position_start, "engeneer")
                                # ajout de l'ingénieur
                                self.carriere.controleur.add_engeneer(self.grid_position_start)
                                stop_loop = True
                        if stop_loop:
                            self.is_progress = False
                            self.carriere.reload_board()
                            return

            
            self.is_progress = False
            self.carriere.reload_board() # on raffraichit la carte si on à valider l'action
            