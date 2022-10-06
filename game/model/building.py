import random
from game import *
import pygame



class building:
    def __init__(self, clock, world):
        #caractéristiques du bâtiment
        self.dimension = (dim_x, dim_y)
        self.sprite = sprite
        self.tiles = world.tiles

        #évènements sur le bâtiment
        self.event = get_event()

        #feu
        self.clock = clock
        self.fire = fire_state(self)


    def fire_on(self):
        i = random.randint(1,500) #Une chance sur x que le bâtiment prenne feu
        if i == 1:
            return True
        return False

    def fire_state(self):

        if fire_on(self):
            state = 1  #état  du feu, si il est à 5, le bâtiment est détruit
        while state in range(1,5): #Si le bâtiment est en feu, son état est modifié au cours du temps
            while self.event == "help":
                pygame.time.wait(1000) #Si le bâtiment est aidé, son état de feu diminue chaque seconde
                state -= 1

            pygame.time.wait(10000)  #sinon, son état de feu augmente toutes les 10sec
            state += 1

        if state == 5:
            destroy(self)
        if state == 0:
            fire_on(self)

    def destroy(self):
        #destruction du bâtiment
        self = None

    def get_event(self):
        #if ###Le préfet aide### :
            #return "help"

        #if ###Clic sur le bâtiment### :
            #return #Truc sur le HUD


