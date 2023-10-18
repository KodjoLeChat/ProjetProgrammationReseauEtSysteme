import pygame

from file_reader import set_tile_size
from Model.jeu import Jeu
from Vue.IHM   import IHM
from Model.pathfinding import short_path
import numpy 

class Controleur:
    def __init__(self):
        # démarrage de pygame
        pygame.init()

        # variable locale
        self.playing = False
        running = True
        self.paused = False


        # initialisation des valeurs de paramètre
        self.TILE_SIZE = set_tile_size("./settings.txt")

        # initialisation des attributs
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.clock  = pygame.time.Clock()

        self.metier = None
        self.ihm    = IHM(self)

        self.grid_width = self.grid_height = 0

        # boucle du menu
        self.ihm.menu.display_main()
        while running:
            # boucle du jeu
            self.ihm.events()
            self.ihm.menu.draw()
            self.clock.tick(60)
            while self.playing:
                self.clock.tick(60)
                if self.metier != None:
                    self.ihm.events()
                    if not self.paused:
                        self.metier.update()
                        self.ihm.update()
                
                self.ihm.draw()

        pygame.exit()

    def get_habitations(self):
        return self.metier.monde.habitations

    def play(self):
        self.playing = True
        self.ihm.pause_menu.displayed = False

    def update_paused(self):
        self.paused = not self.paused

    def get_population(self):
        return len(self.metier.walkerlist)

    def check_if_construction_possible_on_grid(self, grid):
        return self.metier.check_if_construction_possible_on_grid(grid)

    def add_building_on_point(self, grid_pos, name):
        self.metier.add_building_on_point(grid_pos, name)

    def clear(self, grid_pos):
        self.metier.clear(grid_pos)

    def get_board(self):
        return self.metier.get_board()

    def add_engeneer(self, grid_start):
        self.metier.add_engeneer(grid_start)

    def create_new_game(self):
        self.metier = Jeu(self, self.TILE_SIZE)
    
    def find_path(self,spawn,end, is_manhatan=True):
        return short_path(numpy.array(self.metier.monde.define_matrix_for_path_finding()),spawn,end, is_manhatan)

    def find_path_for_road(self,spawn,end, is_manhatan=True):
        return short_path(numpy.array(self.metier.monde.define_matrix_for_path_finding_road_without_panneau()),spawn,end, is_manhatan)

    def walker_creation(self,depart,destination):
        self.metier.walker_creation(depart,destination)

    def check_if_path_exist_from_spawn_walker(self, end):
        return True if short_path(numpy.array(self.metier.monde.define_matrix_for_path_finding()), (20,39), end) != False else False

    def get_walker_infos(self):
        citizens = []
        for walker in self.metier.walkerlist:
            citizens.append(walker)

        return citizens

    def manage_for_road(self, file_names):
        return self.metier.monde.manage_for_road(file_names)

    def should_refresh_from_model(self):
        return self.metier.should_refresh

Controleur()
