import pygame
import json

from .selectionneur_zone import SelectionneurZone

# classe permettant d'ajouter des bâtiments
class Adding_Building(SelectionneurZone):
    def __init__(self, surface, path, netstat):
        SelectionneurZone.__init__(self, surface)
        self.path = path          # chemin de l'image à draw en cas de validation de construction
        self.can_thinking = False # permet de dire, "est-ce que j'ai commencer à faire un click"
        self.netstat = netstat
        self.test = 0
        self.test2 = 0

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
        if (grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1] and
        self.carriere.controleur.check_if_construction_possible_on_grid(grid) and grid != (20, 39) and self.carriere.controleur.check_if_path_exist_from_spawn_walker(grid)):

            stop_loop = False

            for num_lig in range(0, len(self.carriere.informations_tiles)):
                for num_col in range(0, len(self.carriere.informations_tiles[num_lig])):
                    if stop_loop == False and self.carriere.informations_tiles[num_lig][num_col]["building"].name[0:5] == "route" and self.calcul_distance_to_grid(grid, (num_lig, num_col)) <= 2:
                        # Create a dictionary containing grid_pos and other information
                        method = "treat_event"
                        event_data = {
                            "method": method,
                            "grid_pos": grid,
                            "last_grid": last_grid,
                            "SelectionneurZone": self.original_surface.get_size(),
                            "pos": self.pos_start,
                            "Ressources": self.carriere.controleur.metier.ressources.to_json()  # Conversion en JSON
                        }
  
                        # Convert the dictionary to a JSON string
                        event_json = json.dumps(event_data)

                        # Send the JSON string over the network
                        self.netstat.send(event_json)

                    if stop_loop == False and self.carriere.informations_tiles[num_lig][num_col]["building"].name[0:5] == "route" and self.calcul_distance_to_grid(grid, (num_lig, num_col)) <= 2:
                        self.carriere.controleur.add_building_on_point(grid, self.carriere.dictionnaire_reverse_by_path[self.path])
                        #self.carriere.controleur.walker_creation((20,39),grid)
                        self.carriere.controleur.walker_creation((20, 39), (20, 13))
                        stop_loop = True
                    if stop_loop:
                        if last_grid == grid:
                            self.is_progress = False
                        return

            if last_grid == grid:
                self.is_progress = False



    def treat_event_local(self, grid, ressource,method):
        name = "tente"
        food = ressource.get("food")
        water = ressource.get("water")
        dinars = ressource.get("dinars")
        population = ressource.get("population")
        username = ressource.get("username")

        # Now, call the function with the extracted attributes

        self.carriere.controleur.metier.monde.local_building(grid, name, self.carriere.controleur.metier.trouver_ou_creer_ressource(food, water, dinars, population, username))

        # Check if it's the initial building placement
        if method == "Adding_Building":
            # If it is, create a walker (migrant) by default
            initial_position = (20, 39)  # Replace this with the desired initial position

            self.carriere.controleur.walker_creation(initial_position, grid)
            self.carriere.controleur.walker_creation((20, 39), (20, 13))


        def treat_event_bis(self):
            # Crée le walker uniquement
            self.carriere.controleur.walker_creation((20, 39), (20, 13))

            # Met is_progress à False car le traitement est terminé
            self.is_progress = False
