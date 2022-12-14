'''CLass Mouse that if clicked once, it will return True, and if clicked again, it will return False'''
import pygame

class Mouse:
    def notify2(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 1 = left button, 3 = right button
                    return True


    def get_mouse_input(self):
        return self.pressed

    def quit_game(self):
        self.game.set_playing(False)
        self.game.set_state(False)
