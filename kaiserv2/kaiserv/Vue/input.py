from Vue.menu_settings import *
import pygame
from pygame.locals import *

class InputButton:
    def __init__(self, screen, x, y, text, input_text=""):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = WIDTH_BUTTON
        self.height = HEIGHT_BUTTON
        self.button_rect = Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.input_text = input_text
        self.font = pygame.font.SysFont('Constantia', 30)
        self.clicked = False
        self.button_col = YELLOW_LIGHT
        self.hover_col = BEIGE
        self.click_col = GREEN_DARK
        self.text_col = BLACK
        self.current_col = self.button_col
        self.can_thinking = False  # Separate flag for each input field

    def draw(self):
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        pygame.draw.rect(self.screen, self.current_col, self.button_rect)
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))

        input_text_img = self.font.render(self.input_text, True, BLACK)
        input_text_len = input_text_img.get_width()
        pygame.draw.rect(self.screen, WHITE, (self.x + 10, self.y + self.height + 10, self.width - 20, 30))
        self.screen.blit(input_text_img, (self.x + int(self.width / 2) - int(input_text_len / 2), self.y + self.height + 15))

    def check_button(self, event):
        action = False
        pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(pos):
            self.current_col = self.hover_col
        else:
            self.current_col = self.button_col

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.button_rect.collidepoint(pos):
            self.can_thinking = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.can_thinking = False  # Clear thinking flag if clicking outside the input field

        if self.can_thinking:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.can_thinking = False
                    action = True
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

        return action

