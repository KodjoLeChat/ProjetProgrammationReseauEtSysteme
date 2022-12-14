import pygame as pg

from game.view.utils import draw_text
from game.controller.worldController import WorldController
from game.model.zoom import Zoom
from game.model.settings import *
from game.controller.keyboard import keyboard
from game.controller.Mouse_Once import Mouse

from game.controller.camera import Camera
from game.view.hud import Hud
from game.view.menu import Menu
from game.controller.keyboard import keyboard
from game.model.Ressources import Ressources


class Game:

    def __init__(self, screen, clock):
        self.keyboard = keyboard(self)
        self.mouse = Mouse()

        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.state = False
        self.playing = True

        # Ressources
        self.ressources = Ressources(0, 0, 3000, 0)

        # hud
        self.hud = Hud(self.width, self.height, self.ressources, self.keyboard, self.clock)

        # world
        self.worldController = WorldController(self.hud, GRID_LENGTH, GRID_WIDTH, self.width, self.height,
                                               self.keyboard, self.ressources)

        # camera
        self.camera = Camera(self.width, self.height)

        self.pause = True

        # TIMER
        self.actual_time = pg.time.get_ticks()
        self.newMenu = Menu(text_buttons_Game, init_pos,screen)
        self.newMenu.set()


    # build
    def run(self):
        while self.playing:
            self.clock.tick(60)
            self.keyboard.notify()
            self.draw()
            self.update()
            pg.display.flip()

    def update(self):
        self.camera.update()
        self.hud.update()

        # pause the game if the user wants to pause
        self.pauseFF()

        # only update the world controller if the game is not paused
        if not self.keyboard.wantToPause:
            self.worldController.update(self.camera)
            self.gama = True


    def pauseFF(self):
        now = pg.time.get_ticks()
        if (now - self.actual_time > 100):
            self.actual_time = now
            mouse_action = self.keyboard.get_keyboard_input()
            if mouse_action.get(pg.K_t):
                        if self.keyboard.wantToPause == False:
                            print("ok tu veux pause")
                            self.keyboard.wantToPause = True
                        elif self.keyboard.wantToPause == True:
                            print("Ok je résume le jeu")
                            self.keyboard.wantToPause = False
            if mouse_action.get(pg.K_g):
                self.worldController.ressources.add_dinars(1000)


    def pause(self):
        # get user input
        mouse_action = self.keyboard.get_keyboard_input()

        # check if the user pressed the 't' key
        if mouse_action.get(pg.K_t):
            # pause the game
            self.keyboard.wantToPause = True

            # display the pause menu
            self.newMenu.display()

            # check the current state of the pause menu
            choices = self.newMenu.check_state()

            # check the user's choice
            if choices == "Exit":
                # quit the game
                pg.quit()
            elif choices == "Return":
                # resume the game
                self.keyboard.wantToPause = False


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.worldController.dim_map, (self.camera.scroll.x, self.camera.scroll.y))
        self.worldController.draw(self.screen, self.camera)
        self.worldController.draw_minimapR(self.screen, self.camera)
        self.hud.draw(self.screen)

    def get_state(self):
        return self.state

    def get_playing(self):
        return self.playing

    def set_playing(self, bool):
        self.playing = bool

    def set_state(self, state):
        self.state = state
