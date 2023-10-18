import pygame as pg

from .adding_engeneer import AddingEngeneer

from .bouton_hud import Button_HUD
from .adding_building import Adding_Building
from .clear import Clear
from .addingRoad import Adding_Road

# permet de gerer les HUD du haut et de la droite
class HUD:
    def __init__(self, screen, carriere):
        self.screen   = screen
        self.carriere = carriere
        self.longueur = self.screen.get_width() 
        self.hauteur = self.screen.get_height()
        self.action = None

        #dimension image
        REFERENCE_SIZE_X = 1920
        REFERENCE_SIZE_Y = 1080

        # ecart entre chaque action de l'hud de droite 
        HORIZONTAL_GAP = self.longueur*0.032
        VERTICAL_GAP   = self.hauteur *0.0415

        #chargement de l'image
        self.hud_right = pg.image.load("./assets/hud/hud_right.png").convert_alpha()
        size_hud_right = (self.hud_right.get_width()*self.longueur/REFERENCE_SIZE_X, self.hud_right.get_height()*self.hauteur/REFERENCE_SIZE_Y)
        self.hud_right = pg.transform.scale(self.hud_right, size_hud_right)

        self.hud_top = pg.image.load("./assets/hud/hud_top.png").convert_alpha()
        size_hud_top = (self.hud_top.get_width()*self.longueur/REFERENCE_SIZE_X, self.hud_top.get_height()*self.hauteur/REFERENCE_SIZE_Y)
        self.hud_top =  pg.transform.scale(self.hud_top, size_hud_top)

        # double boucle, pour pouvoir rajouter de future action
        # permet de gérer ensuite les evenements
        actions = ["build", "clear", "road", "", "", "", "", "", "", "engeneer", "", ""]
        self.button_hud_right = {}
        for i in range(4):
            for j in range(3):
                if actions[i*3+j] != "":
                    self.button_hud_right[actions[i*3+j]] = Button_HUD(self.screen,
                                                                   self.screen.get_width()*0.905+j*HORIZONTAL_GAP,
                                                                   self.screen.get_height()*0.348+i*VERTICAL_GAP ,
                                                                   actions[i*3+j])

    # traite les evenements
    def events(self, event):
        pos = pg.mouse.get_pos()

        # si nous avons une action en cours alors nous faisons les evenements de cette action
        # tout est au moins basic_action
        if self.action is not None:
            self.action.events(event)
            if self.action.is_progress == False:
                self.carriere.reload_board()
                self.action = None
        
        # s'il y a colision avec l'un des boutons alors on initialise une action si elle n'existe pas 
        for button in self.button_hud_right:
            if self.button_hud_right[button].rect.collidepoint(pos):
                # affichage
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.button_hud_right[button].who_is_visible = "image_click"
                    #interaction 
                elif event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.button_hud_right[button].who_is_visible == "image_click":
                    match button:
                        # si nous voulons rajouter des actions, cela devient donc très simple
                        case "build":
                            if self.action == None: self.action = Adding_Building(self.carriere, "assets/upscale_house/Housng1a_00045.png")
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/Land2a_00001.png")
                                self.action.initialiser(image)
                        case "clear":
                            if self.action == None: self.action = Clear(self.carriere, "assets/upscale_land/red_image.png")
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/red_image.png")
                                self.action.initialiser(image)
                        case "road":
                            if self.action == None: self.action = Adding_Road(self.carriere)
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_road/Land2a_00094.png")
                                self.action.initialiser(image)
                        case "engeneer":
                            if self.action == None: self.action = AddingEngeneer(self.carriere)
                            if not self.action.is_progress:
                                self.action.is_progress = True
                                image = pg.image.load("assets/upscale_land/Land2a_00001.png")
                                self.action.initialiser(image)
                elif self.button_hud_right[button].who_is_visible != "image_click":
                    self.button_hud_right[button].who_is_visible = "image_hover"

            else:
                self.button_hud_right[button].who_is_visible = ""

    # affiche les images et les boutons suite aux evenements
    def draw(self):
        if self.action != None: self.action.draw()

        self.screen.blit(self.hud_right, (self.longueur*0.895, self.hauteur*0.0235))
        self.screen.blit(self.hud_top, (0, 0))
        
        for button in self.button_hud_right:
            self.button_hud_right[button].draw()

