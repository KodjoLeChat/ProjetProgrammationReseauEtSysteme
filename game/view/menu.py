import pygame as pg
import pygame.display
from game.view.Button import Button
from game.view.utils import extract_image_path, create_bg
from game.view.utils import *
from game.model.settings import *

class Menu():
    '''
    text_buttons = liste des textes affiché aux buttons from settings
    title : titre affiché au menu
    buttons : liste des bouttons du menu
    L_center
    H_center
    delta_H
    '''
    def __init__(self, text_buttons, init_pos):
        self.text_buttons = text_buttons
        self.buttons = []

        self.init_pos = init_pos
        self.background = pg.image.load("C3_sprites/C3/0_fired_00001.png")

        self.screen = pygame.display.set_mode((1080, 720))
        self.max_l = 0


    def create_buttons(self):
        """title_button = Button(self.screen, None, pos=(self.init_pos[0], self.init_pos[1]),
               dim=size_bg_button, delta=delta_menuP[0], text_input=self.title, font=("white", "Milk"),
               size_bg = size_bg_button)
        self.buttons.append(title_button)"""
        i = 0
        for text in self.text_buttons:
            menu_button = Button(self.screen, images_menuP[i], pos=(self.init_pos[0]+delta_Button_menuP[i][0], self.init_pos[1] + i*self.init_pos[2]),
                                 dim=size_bg_button[i], text_input=self.text_buttons[i], font=fonts_menuP[i], delta_text=delta_text_menuP[i])
            self.buttons.append(menu_button)
            i += 1

    def set(self):
        self.background = pygame.transform.scale(self.background, (1080, 720))
        # Button
        self.create_buttons()

    def display(self):
        self.screen.blit(self.background, (00, 00))
        # Buttons:
        for button in self.buttons:
            button.update()
        # move to Run function
        # barre_function(self.screen)
        ##
        pygame.display.flip()

    def check_state(self):
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Fermeture du Jeu")

            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        return(button.text_input)


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont('Raleway', size, bold=False, italic=False)

def exit_function(display):
    x,y, _ = init_pos_exit
    L, l = dim_menu_exit

    back_symbol = pg.image.load("C3_sprites/C3/paneling_00245.png")# paneling_00243.png")
    exit_symbol = pg.image.load("C3_sprites/C3/paneling_00241.png")

    images = [None , None, back_symbol, exit_symbol]
    texts = ["QUIT", "Leave_the_Empire?", None, None]
    fonts = [("red", "Milk"),("red", "Beige"),None , None]
    bg_block(display, pos=(x,y), dim=(L, l), color="Beige", rescale=True)

    Buttons = [Button(display, images[i], pos=pos_button_exit[i], dim=size_bg_button_exit[i], text_input=texts[i],
               font=fonts[i], delta_text =delta_text_menuExit[i]) for i in range(len(texts))]
    while True:
        for button in Buttons:
            button.update()
        pygame.display.flip()
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Fermeture du Jeu")
            if event.type == pg.MOUSEBUTTONDOWN:
                if Buttons[2].checkForInput(MENU_MOUSE_POS):
                    # back_button
                    return True
                elif Buttons[3].checkForInput(MENU_MOUSE_POS):
                    # exit_button
                    print("Fermeture du Jeu")
                    pygame.quit()

def barre_function(screen):
    x, y, _ = init_pos_barre
    L, l = dim_menu_barre
    # MAJ la longueur de la screen.
    L, _ = screen.get_size()
    bg_block(screen, pos=(x, y), dim=(L, l), color="Beige", rescale=True)
    button = Button(screen, None, pos=(10,2), dim=(40, 10), text_input="Exit",
            font=("red", "Milk"), delta_text=delta_text_menuExit[1])
    button.update()
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if button.checkForInput(MENU_MOUSE_POS):
                exit_function(screen)

    # pygame.display.flip()