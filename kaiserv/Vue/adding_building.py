import pygame

from .selectionneur_zone import SelectionneurZone

# classe permettant d'ajouter des bâtiments
class Adding_Building(SelectionneurZone):
    def __init__(self, surface, path):
        SelectionneurZone.__init__(self, surface)
        self.path = path          # chemin de l'image à draw en cas de validation de construction
        self.can_thinking = False # permet de dire, "est-ce que j'ai commencer à faire un click"

    def events(self, event):
        SelectionneurZone.events(self, event)
        # je commence à sélectionner une zone
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: self.can_thinking = True
        # je relève, je valide mon action, je lance la construction de batiment
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.can_thinking:
            last_grid = self.grid_to_draw[len(self.grid_to_draw)-1]
            for grid in self.grid_to_draw:
                self.treat_event(grid, last_grid)
            
            self.is_progress = False

    # permet d'ajouter des tentes et des migrants
    def treat_event(self, grid, last_grid):
        if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1] and \
           self.carriere.controleur.check_if_construction_possible_on_grid(grid) and grid != (20,39) and self.carriere.controleur.check_if_path_exist_from_spawn_walker(grid):
           stop_loop = False
           for num_lig in range(0, len(self.carriere.informations_tiles)):
            for num_col in range(0, len(self.carriere.informations_tiles[num_lig])):
                # si on peux construire sur la zone en question, alors on construit et on ajoute le migrant
                # on ne peux pas construire à moins de deux cases d'une route
                if stop_loop == False and self.carriere.informations_tiles[num_lig][num_col]["building"].name[0:5] == "route" and self.calcul_distance_to_grid(grid, (num_lig, num_col)) <= 2:
                    self.carriere.controleur.add_building_on_point(grid, self.carriere.dictionnaire_reverse_by_path[self.path])
                    self.carriere.controleur.walker_creation((20,39),grid)
                    stop_loop = True
                if stop_loop:
                    if last_grid == grid: self.is_progress = False
                    return
                    
            if last_grid == grid: self.is_progress = False