import pygame

from .basic_action import Basic_Action

# Classe permettant d'ajouter des routes
class Adding_Road(Basic_Action):

    def __init__(self, surface):
        Basic_Action.__init__(self, surface)
        self.can_thinking = False
        self.chemins = None

    def getChemin(self, start, end):
        if start[0] >= 0 and start[1] >= 0 and len(self.carriere.informations_tiles) > start[0] and len(self.carriere.informations_tiles[start[0]]) > start[1] and \
           end  [0] >= 0 and end  [1] >= 0 and len(self.carriere.informations_tiles) > end  [0] and len(self.carriere.informations_tiles[end  [0]]) > end  [1] and \
                self.carriere.controleur.check_if_construction_possible_on_grid(start) and self.carriere.controleur.check_if_construction_possible_on_grid(end):
            self.chemins = self.carriere.controleur.find_path_for_road(start, end, False)

        if type(self.chemins) == bool or self.chemins == None:
            self.chemins = []
            self.chemins.append(start)

    def draw(self):
        size_of_original_image = self.original_surface.get_size()
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        
        if self.grid_position_start != None and self.grid_position_end != None:
            self.getChemin(self.grid_position_start, self.grid_position_end)
            file_names = [[self.carriere.informations_tiles[i][j]["building"].name for j in
                          range(0, len(self.carriere.informations_tiles[i]))] for i in
                          range(0, len(self.carriere.informations_tiles))]
            for grid in self.chemins:
                file_names[grid[0]][grid[1]] = "route"

            file_names = self.carriere.controleur.manage_for_road(file_names)
            for num_lig in range(len(file_names)):
                for num_col in range(len(file_names[num_lig])):
                    if file_names[num_lig][num_col][0:5] == "route":
                        self.image_to_draw = self.carriere.dictionnaire[file_names[num_lig][num_col]]
                        self.image_to_draw = pygame.transform.scale(self.image_to_draw, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
                        self.draw_for_an_image((num_lig,num_col))
        else:
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE * self.carriere.zoom.multiplier, self.pos_without_first_click)
            self.draw_for_an_image(self.grid_position_without_first_click)

    def events(self, event):
        n=1
        #n <= len(self.chemins)
        Basic_Action.events(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:

            file_names = [[self.carriere.informations_tiles[i][j]["building"].name for j in
                          range(0, len(self.carriere.informations_tiles[i]))] for i in
                          range(0, len(self.carriere.informations_tiles))]
            for grid in self.chemins:
                file_names[grid[0]][grid[1]] = "route"

            file_names = self.carriere.controleur.manage_for_road(file_names)
            for num_lig in range(len(file_names)):
                for num_col in range(len(file_names[num_lig])):
                    if file_names[num_lig][num_col][0:5] == "route" and  ( self.carriere.controleur.check_if_construction_possible_on_grid((num_lig,num_col)) or \
                                                                           self.carriere.informations_tiles[num_lig][num_col]["building"].name[0:5] == "route" ):
                        self.carriere.controleur.add_building_on_point((num_lig,num_col), file_names[num_lig][num_col])

            self.is_progress = False
            
            self.carriere.reload_board()