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
from game.model.Ressources import Ressources


class Game:

    def __init__(self, screen, clock):
        self.keyboard = keyboard(self)
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.state = False
        self.playing = True

        self.pause = False

        # Ressources
        self.ressources = Ressources(0, 0, 3000, 0)

        # hud
        self.hud = Hud(self.width, self.height, self.ressources, self.keyboard, self.clock)

        # world
        self.worldController = WorldController(self.hud, GRID_LENGTH, GRID_WIDTH, self.width, self.height, self.keyboard, self.ressources)

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
            print(self.PauseR())
            self.Pause()
            self.camera.update()
            self.hud.update()
            if self.pause == False:
                self.worldController.update(self.camera)
            
    def Pause(self):
        mouse_action = self.keyboard.get_keyboard_input()
        
        if mouse_action.get(pg.MOUSEBUTTONDOWN):
            if self.hud.selected_tile is not None:
                sprite_name = self.hud.selected_tile["name"]
                print(sprite_name)
                if (sprite_name =="pause"):
                    if self.pause == False:
                        print("pause")
                        self.pause = True
                        return True
                    else:
                        self.pause = False
                        print("unpause")
                        return False
            
    def PauseR(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                print("mouuuuuuuuuuuuuuuuuse")
            
                return True



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
        self.worldController.draw_minimapR(self.screen, self.camera)
        self.hud.draw(self.screen)
