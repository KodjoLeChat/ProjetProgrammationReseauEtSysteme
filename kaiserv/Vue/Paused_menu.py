import pygame as pg
import sys
from file_reader import reader_bmp_map
from Vue.Buttons_settings_pause import *


class Pause_menu:

    def __init__(self, screen, controleur):
        self.controleur = controleur
        self.displayed = False
        self.screen = screen
        self.center_x = screen.get_width()/2 
        self.center_y = screen.get_height()/2 
        self.font = pg.font.SysFont('Constantia', 75)
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.space = 60
        self.text = "Pause"
        self.menu_principale = False
        self.new_game = False
        self.save = False
        self.quitter = False

        #chargement image menu
        self.fond_menu = pg.image.load("./assets/background_pause_menu.jpg").convert_alpha()

        #Récupération mi-dimension image 
        self.longueur_centre_image_menu = self.fond_menu.get_width()//2
        self.largeur_centre_image_menu = self.fond_menu.get_height()//2

        #mise à l'échelle de l'image de fond du menu
        self.new_longueur_centre_image_menu = self.longueur_centre_image_menu/7
        self.new_largeur_centre_image_menu = self.largeur_centre_image_menu/4
        self.fond_menu = pg.transform.scale(self.fond_menu, (self.new_longueur_centre_image_menu, self.new_largeur_centre_image_menu))
    
        #création bouttons
        self.menu_principale = Button_Menu_paused(self.screen, self.center_x - self.space*1.4, self.center_y - (2*self.space), 'Menu principal')
        self.new_game = Button_Menu_paused(self.screen, self.center_x - self.space*1.4, self.center_y - (1*self.space), 'Nouvelle partie')
        self.save = Button_Menu_paused(self.screen, self.center_x - self.space*1.4, self.center_y, 'Sauvegarder')
        self.quitter = Button_Menu_paused(self.screen, self.center_x - self.space*1.4, self.center_y  - (-1*self.space), 'Quitter le jeu')

        #longueur titre : "Pause"
        self.title_menu = self.font.render(self.text, True, (0, 0, 0))
        self.width_title = self.title_menu.get_width()
      

    def events(self, event):
        if self.displayed :

            # revenir au menu principale 
            if self.menu_principale.check_button(event):
                self.controleur.ihm.carriere.reset()
                self.controleur.playing = False
                self.controleur.paused  = False 

            #
            if self.new_game.check_button(event):
                self.controleur.create_new_game()
                self.controleur.metier.init_board(reader_bmp_map(1, self.controleur))
                self.controleur.ihm.init_sprite()
                self.controleur.play()
                self.controleur.paused = False 
            
            if self.save.check_button(event):
                self.controleur.ihm.carriere.Save_game()


            if self.quitter.check_button(event):
                run = False
                sys.exit()

    # affichage menu pause
    def draw(self):
        if self.displayed :

            self.screen.blit(self.fond_menu,(self.center_x - (self.new_longueur_centre_image_menu*0.42) , self.center_y - (self.new_longueur_centre_image_menu*0.7)))
            self.screen.blit(self.title_menu,((self.center_x - self.width_title/3, self.center_y - (3.5*self.space))))
            
            self.new_game.draw()
            self.save.draw()
            self.menu_principale.draw()
            self.quitter.draw()
        