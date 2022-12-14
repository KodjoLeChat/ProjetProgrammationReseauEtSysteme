from game.view.menu import *
from game.model.settings import *
from game.controller.game import Game

from game.view.utils import *
import tkinter as tk
import easygui
import pickle

def main():

    old_game = False
    gameZ = False
    gama = True

    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock()


    # implement menus
    menu = Menu(text_buttons_menuP, init_pos,screen)
    menu.set()

    newMenu = Menu(text_buttons_Game, init_pos,screen)
    newMenu.set()
    

    # implement game
    game = Game(screen, clock)

    while game.get_playing():

        # start menu goes here
        if gama == True:
            menu.display()
            choice = menu.check_state()
            match choice:
                case "Exit":
                    pg.quit()
                case "Start_new_career":
                    gameZ = True
                    game.set_state(True)

                case "Load_saved_game":
                    newMenu.display()
                    gama = False

        if gama == False:
            newMenu.display()
            choices = newMenu.check_state()

            match choices:
                case "Exit":
                    pg.quit()
                case "Return":
                    gama = True

                case "ChooseFile":
                    path = easygui.fileopenbox()
                    file = open(path, 'rb')
                    game.set_state(True)
                    old_game = True
                    gama = False



                
        while game.get_state():
            # game loop here
            if old_game:
                game.worldController.worldModel = pickle.load(file)
                game.run()

            elif gameZ:
                game.run()

if __name__ == "__main__":
    main()
