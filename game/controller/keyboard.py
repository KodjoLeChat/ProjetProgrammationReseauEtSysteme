import pygame


class keyboard:

    def __init__(self, game):
        self.game = game
        self.pressed = {}

    def notify(self):
        for event in pygame.event.get():
            if self.game.get_state():
                self.key_down_playing(event)

    def key_down_playing(self, event):
        """
        Gère les évenements pendant le jeu
        """
        if event.type == pygame.QUIT:
            self.quit_game()
        elif event.type == pygame.KEYDOWN:
            self.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            self.pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed[pygame.MOUSEBUTTONDOWN] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed[pygame.MOUSEBUTTONDOWN] = False

        elif event.type == pygame.MOUSEMOTION:
            self.pressed[pygame.MOUSEMOTION] = True
        elif event.type != pygame.MOUSEMOTION:
            self.pressed[pygame.MOUSEMOTION] = False

    def key_down_menu(self):
        pass

    def get_keyboard_input(self):
        return self.pressed

    def quit_game(self):
        self.game.set_playing(False)
        self.game.set_state(False)