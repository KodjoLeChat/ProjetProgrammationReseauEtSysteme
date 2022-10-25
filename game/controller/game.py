import pygame as pg

from game.view.utils import draw_text
from game.model.world import World
from game.model.settings import TILE_SIZE
from game.controller.camera import Camera
from game.model.hud import Hud

from game.controller.keyboard import keyboard

class Game:

    def __init__(self, screen, clock):
        self.keyboard = keyboard(self)
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.state = False
        self.playing = True

        # hud
        self.hud = Hud(self.width, self.height)

        # world
        self.world = World(self.hud, 65, 65, self.width, self.height,self.keyboard)

        # camera
        self.camera = Camera(self.width, self.height)





    def run(self):
        while self.playing:
            self.clock.tick(60)
            self.keyboard.notify()
            self.draw()
            self.update()
            pg.display.flip()

    def set_playing(self,bool):
        self.playing = bool

    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera,self.screen)

    def get_state(self):
        return self.state

    def get_playing(self):
        return self.playing

    def set_playing(self,bool):
        self.playing = bool

    def set_state(self,state):
        self.state = state

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.world.dim_map, (self.camera.scroll.x, self.camera.scroll.y))
        self.world.draw(self.screen, self.camera)
        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 10)
        )
        self.hud.draw(self.screen)


