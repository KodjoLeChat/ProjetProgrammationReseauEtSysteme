import pygame
import sys

from .carriere import Carriere
from .Menu import Menu
from .hud import HUD
from .Paused_menu import *
from .utils import draw_text

class IHM:
    def __init__(self, controleur):
        self.controleur = controleur
        # menu de démarrage
        self.menu = Menu(self.controleur.screen, self.controleur)
        # carriere de jeu actuelle
        self.carriere = Carriere(self.controleur)
        # hud
        self.hud = HUD(self.controleur.screen, self.carriere)

        #Menu pause
        self.pause_menu = Pause_menu(self.controleur.screen, self.controleur)

    # gestion événementielles au clavier
    def events(self):
        for event in pygame.event.get():
            # quitte lors de la combinaison de touche alt+f4
            if event.type == pygame.QUIT:
                self.exit_game()
            if self.controleur.playing == False:
                self.menu.events(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu.displayed = not self.pause_menu.displayed  
                    self.controleur.paused = not self.controleur.paused         
            elif self.controleur.playing:
                self.carriere.events(event)
                self.hud.events(event)
    
            self.pause_menu.events(event)

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def update(self): 
        self.carriere.update()

    def draw(self):
        if self.controleur.should_refresh_from_model():
            self.carriere.reload_board()

        self.carriere.draw_main_components()
        self.hud.draw()
        self.carriere.draw_walker()
        draw_text(self.controleur.screen, "Population: {}".format(self.controleur.get_population()), 20, (0,0,0), (self.controleur.screen.get_width()*0.91, self.controleur.screen.get_height()*0.57))
        self.pause_menu.draw()

        # actualise l'écran
        pygame.display.flip()

    # initialise chaque sprite à afficher 
    def init_sprite(self):
        self.carriere.init_sprite()