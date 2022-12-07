import pygame as pg

from game.view.utils import draw_text
from game.controller.worldController import WorldController
from game.model.zoom import Zoom
from game.model.settings import GRID_LENGTH, GRID_WIDTH
from game.model.settings import TILE_SIZE
from game.controller.keyboard import keyboard
from game.controller.camera import Camera
from game.view.hud import Hud
from game.controller.keyboard import keyboard
from game.model.timer import Timer
from game.model.Ressources import Ressources


class Game:

    def __init__(self, screen, clock):
        self.keyboard = keyboard(self)
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.state = False
        self.playing = True

        # Ressources
        self.ressources = Ressources(0, 0, 3000, 0)

        # hud
        self.hud = Hud(self.width, self.height, self.ressources)

        # world
        self.worldController = WorldController(self.hud, GRID_LENGTH, GRID_WIDTH, self.width, self.height,
                                               self.keyboard, self.ressources)

        # camera
        self.camera = Camera(self.width, self.height)


        



    # build
    def run(self):
        while self.playing:
            self.clock.tick(70)
            self.keyboard.notify()
            self.update()
            self.draw()
            pg.display.flip()

    def update(self):
        self.camera.update()
        self.hud.update()
        self.worldController.update(self.camera)

    def get_state(self):
        return self.state

    def get_playing(self):
        return self.playing

    def set_playing(self, bool):
        self.playing = bool

    def set_state(self, state):
        self.state = state

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.worldController.dim_map, (self.camera.scroll.x, self.camera.scroll.y))
        self.worldController.draw(self.screen, self.camera)

        self.hud.draw(self.screen)
