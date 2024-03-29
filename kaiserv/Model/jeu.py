import random
from .monde import Monde
from .walker import Walker
from .ingenieur import Ingenieur
from .ressources import Ressources
from .pathfinding import short_path
import numpy

# classe passerelle entre controleur et métier
class Jeu:
    def __init__(self, controleur, size_tile):
        self.width, self.height = controleur.screen.get_size()
        self.monde = Monde(size_tile, controleur.screen.get_size()) # plateau de jeu
        self.walkerlist = []                                        # liste de tous les walkers présents
        self.should_refresh = False                                 # permet de savoir si la carte doit être rechargée
        self.ressources = Ressources(0, 0, 4000, 0, "rayaneGamer")
        self.ressources_local = Ressources(0, 0, 100000, 0, "player2") # pour test, à supprimer
        self.ressources_local_list = [] #list qui contient plusieurs Ressources qui viennent des autres joueurs object

    def trouver_ou_creer_ressource(self, food, water, dinars, population, username):
        # Vérifier si un objet Ressources avec le nom d'utilisateur existe déjà
        for ressource in self.ressources_local_list:
            if ressource.username == username:
                # Update the attributes of the existing Ressources object
                ressource.food = food
                ressource.water = water
                ressource.dinars = dinars
                ressource.population = population
                return ressource  # Retourne l'objet Ressources mis à jour

        # Si le nom d'utilisateur n'existe pas, créer un nouvel objet Ressources
        nouvelle_ressource = Ressources(food, water, dinars, population, username)
        self.ressources_local_list.append(nouvelle_ressource)
        return nouvelle_ressource  # Retourne le nouvel objet Ressources créé



    def add_engeneer(self, grid_start):
        # ajout de l'ingénieur sur la positition du bâtiment d'ingénieur
        if self.ressources.enough_dinars(2000):
            ingenieur = Ingenieur(grid_start, grid_start)
            self.walkerlist.append(ingenieur)
            self.ressources.dinars -= 2000


    def update(self):
        should_refresh = False

        for walker in self.walkerlist:
            self.update_move_walker(walker) # d'abord on met à jour les walkers
            if walker.name == "citizen":    # citizen => migrant qui viennent vers leur future maison
                if walker.actualPosition != walker.destination and walker.chemin != False and walker.nombreDeplacement == 0:
                    if walker.chemin != None :
                        walker.actualPosition = walker.chemin[1]
                        walker.chemin.remove(walker.chemin[0])
                # si le migrant a atteint sa maison
                if walker.actualPosition == walker.destination and self.monde.board[walker.destination[0]][walker.destination[1]]["building"].name == 'panneau':
                    self.monde.board[walker.destination[0]][walker.destination[1]]["building"] = self.monde.craft_building(self.monde.information_for_each_tile['tente'],self.ressources)
                    self.monde.board[walker.destination[0]][walker.destination[1]]["building"].set_position_reference(walker.destination)
                    should_refresh = True
            elif walker.name == "citizen_engeneer":
                walker.heal_around(self.monde)

        self.monde.update()

        # on met à jour l'état d'effondrement des batiments considérés comme habitable
        for habitation in self.monde.habitations:
            if habitation.collapsing_state == 0:
                for walker in self.walkerlist:
                    if walker.destination == habitation.position_reference:
                        # si un bâtiment est effondré on retire le walker associé
                        self.walkerlist.remove(walker)
                        break

        self.should_refresh = should_refresh

        for habitation in self.monde.personnal_Building:
            habitation.elapsed_time(self.ressources)

        for habitation in self.monde.personnal_Building:
            if habitation.name == "destroyed":
                print("destroyed " + habitation.name) 
            


    # permet de changer les positions des walkers
    def update_move_walker(self, walker):
        walker.set_nbdeplacement()
        if walker.name == "citizen":
            walker.set_nextPosition ()
        elif walker.name == "citizen_engeneer":
            walker.find_new_destination(self.monde)

    def check_if_construction_possible_on_grid(self, grid):
        return self.monde.check_if_construction_possible_on_grid(grid)

    def check_if_clear_possible_on_grid(self, grid):
        return self.monde.check_if_clear_possible_on_grid(grid)

    # permet de retirer un bâtiment présent dans le plateau
    def clear(self,grid):
        if self.check_if_clear_possible_on_grid(grid): # on vérifie que l'on peux effacer le bâtiment
            building = self.monde.board[grid[0]][grid[1]]["building"]
            # traitement particulier des tente, panneau, ingenieur
            if building.name == "tente" or building.name == "panneau" or building.name == "destruction" or building.name == "engeneer":
                # on retire des habitations la tente si s'en est une pour ne pas prendre trop de ressource
                if building.name == "tente" or building.name == "destruction" :
                    for habitation in self.monde.habitations:
                        if habitation.id == building.id:
                            self.monde.habitations.remove(habitation)
                            break
                # dans le cas du bâtiment dédié aux ingénieurs, on retire l'ingénieur présent sur le terrain
                elif building.name == "engeneer":
                    for ingenieur in self.monde.ingenieurs:
                        if ingenieur.id == building.id:
                            self.monde.ingenieurs.remove(ingenieur)
                            break

                # si la supression est lié à un walker, on le retire
                walker_tmp = None
                for walker in self.walkerlist:
                    if walker.destination == grid:
                        walker_tmp = walker
                        break
                if walker_tmp != None: self.walkerlist.remove(walker_tmp)

            # on replace de l'herbe à la place du bâtiment
            self.monde.add_building_on_point(grid, 'herbe_{}'.format(random.randint(110,119)),self.ressources)

            # cas particulier des ingénieurs, quand on supprime une route, on supprime potentiellement 
            # l'accès au bâtiment de l'un des ingénieurs présent sur la carte
            # dans ce cas l'ingénieur revient chez lui
            if building.name[0:5] == "route":
                matrix_for_look_around_road = [(-1,0),(1,0),(0,-1),(0,1)]
                #for coord in matrix_for_look_around_road:
                for ingenieur in self.monde.ingenieurs:
                    position_reference = ingenieur.position_reference
                    for walker in self.walkerlist:
                        # si nous avons un ingénieur associés au bâtiment
                        if walker.name == "citizen_engeneer" and position_reference == walker.position_reference:
                            is_conserve_engeneer = False
                            # on regarde s'il y a des chemins allant d'une des routes près du bâtiment jusqu'à l'emplacement de l'ingénieur
                            # si oui alors on laisse l'ingénieur tranquille
                            for coord in matrix_for_look_around_road:
                                new_grid = (position_reference[0]+coord[0], position_reference[1]+coord[1])
                                if new_grid[0] >= 0 and new_grid[1] >= 0 and\
                                new_grid[0] < len(self.monde.board) and new_grid[1] < len(self.monde.board[new_grid[0]]) and\
                                self.monde.board[new_grid[0]][new_grid[1]]["building"].name[0:5] == "route" and self.is_chemin_with_road(walker.actualPosition, new_grid):
                                        is_conserve_engeneer = True

                            if not is_conserve_engeneer:
                                walker.reset_position()  
                                break  

    
    # permet de savoir s'il y a un chemin de route entre deux point
    def is_chemin_with_road(self, grid_src, grid_dst):
        chemins = short_path(numpy.array(self.monde.define_matrix_for_path_finding_road()), grid_src, grid_dst, False)
        if chemins == False: return False
        return True 

    def add_building_on_point(self, grid_pos, path):
        self.monde.add_building_on_point(grid_pos, path,self.ressources)

    ########################################################
    #  get_building_on_point and set_building_on_port
    #  Cette fonction pour recuperer le contenu d'une case
    #  a partir du controleur
    #  Ajout: Philemon                        11 fevrier 
    ########################################################
    def get_building_on_point(self, grid_pos):
        return self.monde.get_building_on_point(grid_pos)
    
    def set_building_on_point(self, grid_pos, building):
        self.monde.set_building_on_point(grid_pos, building)

    def init_board(self, file_name):
        return self.monde.init_board(file_name,self.ressources)

    # devenu inutile
    def get_date(self):
        return self.date

    def get_board(self):
        return self.monde.board

    # permet de créer un walker, utilisé pour les migrants
    def walker_creation(self,depart,destination):
        if self.ressources.enough_dinars(1000):
            walker = Walker(depart,destination)

            self.walkerlist.append(walker)
            self.ressources.dinars -= 1000

            walker.chemin = short_path(numpy.array(self.monde.define_matrix_for_path_finding()),walker.actualPosition,walker.destination)
            walker.set_nextPosition()

    def walker_creation_local(self,depart,destination):
        walker = Walker(depart,destination)
        self.walkerlist.append(walker)

        walker.chemin = short_path(numpy.array(self.monde.define_matrix_for_path_finding()),walker.actualPosition,walker.destination)
        walker.set_nextPosition()