import pygame

from .selectionneur_zone import SelectionneurZone

class Clear(SelectionneurZone):
    def __init__(self, surface, path):
        SelectionneurZone.__init__(self, surface)
        self.path = path
        self.can_thinking = False


    def events(self, event):
        SelectionneurZone.events(self, event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:
            is_road_to_reload = False
            for grid in self.grid_to_draw:
                if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1]:
                    if self.carriere.informations_tiles[grid[0]][grid[1]]["building"].name[0:5] == "route": is_road_to_reload = True
                    self.carriere.controleur.clear(grid)

            if is_road_to_reload:
                file_names = [[self.carriere.informations_tiles[i][j]["building"].name for j in
                            range(0, len(self.carriere.informations_tiles[i]))] for i in
                            range(0, len(self.carriere.informations_tiles))]

                file_names = self.carriere.controleur.manage_for_road(file_names)
                for num_lig in range(len(file_names)):
                    for num_col in range(len(file_names[num_lig])):
                        if file_names[num_lig][num_col][0:5] == "route":
                            self.carriere.controleur.add_building_on_point((num_lig,num_col), file_names[num_lig][num_col])

            self.is_progress = False

    def delete(self):
        pass