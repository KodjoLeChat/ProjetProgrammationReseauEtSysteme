import pygame
import pygame as pg

from game.view.utils import draw_text
from game.controller.worldController import WorldController
from game.model.zoom import Zoom
from game.model.settings import TILE_SIZE
from game.model.save import Save
from game.controller.keyboard import keyboard
from game.controller.camera import Camera
from game.view.hud import Hud
from game.model.timer import Timer
from game.controller.keyboard import keyboard


class Game:

    def __init__(self, screen, clock):
        self.keyboard = keyboard(self)
        self.screen = screen
        self.clock = clock
        #self.width, self.height = (self.screen.get_size())
        self.width, self.height = (800,1000)
        self.state = False
        self.playing = True


        # hud
        self.hud = Hud(self.width, self.height)

        # world
        self.worldController = WorldController(self.hud, 65, 65, self.width, self.height, self.keyboard)


        #save
        self.save = Save(self.worldController.get_world_model())

        # camera
        self.camera = Camera(self.width, self.height)

        # time
        self.time = Timer()

        # zoom
        self.zoom = Zoom(self.width, self.height)

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
        if self.keyboard.get_keyboard_input().get(pygame.K_KP_ENTER):
            self.save.saveGame()

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
        draw_text(
            self.screen,
            '{}'.format((self.worldController.__str__())),
            25,
            (255, 255, 255),
            (10, 10)
        )
        self.hud.draw(self.screen)
