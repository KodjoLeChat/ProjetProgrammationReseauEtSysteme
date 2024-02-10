from Vue.menu_settings import *
import pygame
from pygame.locals import *

class Button_Menu():
    def __init__(self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = WIDTH_BUTTON
        self.height = HEIGHT_BUTTON
        self.button_rect = Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Constantia', 30) #cambriacambriamath , arialblack,calibri, bahnschrift
        self.clicked = False
        self.button_col = YELLOW_LIGHT
        self.hover_col = BEIGE
        self.click_col = GREEN_DARK
        self.text_col = BLACK
        self.current_col = self.button_col
        self.can_thinking = False

    def draw(self):
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        pygame.draw.rect(self.screen, self.current_col, self.button_rect)
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))

    def check_button(self, event):
        action = False
        pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(pos):
                self.current_col = self.hover_col
        else:
            self.current_col = self.button_col
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rect.collidepoint(pos): self.can_thinking = True
        if self.can_thinking:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.button_rect.collidepoint(pos):
                pygame.draw.rect(self.screen, self.click_col, self.button_rect)
                self.current_col = self.click_col
                action = True
        

        if action == True:
            self.can_thinking = False
            
        return action
