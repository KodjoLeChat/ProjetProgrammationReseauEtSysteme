import pygame
from pygame.locals import *

class Button_Menu_paused():
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 220
        self.height = 45
        self.button_rect = Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Constantia', 30) #cambriacambriamath , arialblack,calibri, bahnschrift
        self.clicked = False
        self.space = 30
        self.text_original = (0, 0, 0)
        self.text_click = (255, 255, 255) 
        self.text_base = self.text_original
        self.text_hover = (165, 42, 42)
        self.can_thinking = False
        

    #affichage des bouton 
    def draw(self):
        # Créer la police
        text_img = self.font.render(self.text, True, self.text_base)

        # longueur du texte
        text_len = text_img.get_width()

        #affichage du bouton
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))


    #couleur du bouton selon action souris et l'action est-elle en cours ?
    def check_button(self, event):
        action = False
        pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(pos):
            self.text_base = self.text_hover
        else:
            self.text_base = self.text_original

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rect.collidepoint(pos): self.can_thinking = True
        if self.can_thinking:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.button_rect.collidepoint(pos):
                pygame.draw.rect(self.screen, self.text_click, self.button_rect)
                self.text_base = self.text_click
                action = True

        if action == True:
            self.can_thinking = False
            
        return action
