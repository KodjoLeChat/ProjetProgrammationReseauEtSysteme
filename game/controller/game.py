import pygame as pg

from game.view.utils import draw_text
from game.model.world import World
from game.model.textShow import TextShow
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
        self.width, self.height = self.screen.get_size()
        self.state = False
        self.playing = True

        # hud
        self.hud = Hud(self.width, self.height)

        # world
        self.world = World(self.hud, 65, 65, self.width, self.height, self.keyboard)

        # camera
        self.camera = Camera(self.width, self.height)
        
        # time
        self.time = Timer()
        
        # save
        self.save = Save(self.world)
        
        # zoom
        self.zoom = Zoom(self.width, self.height)
        
        self.world.ressources.add_dinars(3000)
        #textShow
        #self.textShow = TextShow(self.world.grid_length_x, self.world.grid_length_y)
        
        #Ressources
        #self.ressources = Ressources(0,0,0,0,0,0)

    # build
    def run(self):
        while self.playing:
            self.clock.tick(70)
            self.keyboard.notify()
            self.update()
            self.draw()
            pg.display.flip()

    def update(self):
        if self.keyboard.wantToPause != True:
            #print(self.ressources.__str__())
            if self.keyboard.wantToZoom == True:
                self.zoom.zoom_in()
                self.zoom.update()
                self.zoom.draw(self.screen)
            
            self.time.update(self.keyboard.test)
            self.camera.update()
            self.hud.update()
            self.world.update(self.camera) #CLARIFICATION
            #self.textShow.update(self.world)
            if self.keyboard.wantToSave == True:
                print("OK !")
                self.save.save()
                self.keyboard.wantToSave = False
            if self.keyboard.wantToLoad == True:
                print("OK !")
                self.save.load()
                self.keyboard.wantToLoad = False

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
            '{}'.format((self.world.__str__())),
            25,
            (255, 255, 255),
            (10, 10)
        )
        self.hud.draw(self.screen)    
    
