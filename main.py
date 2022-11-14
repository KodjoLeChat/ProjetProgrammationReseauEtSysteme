from game.view.menu import *
from game.model.settings import *
from game.controller.game import Game


def main():

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menus
    menu = Menu(text_buttons, L_center, H_center, delta_H)
    menu.set()

    # implement game
    game = Game(screen, clock)

    while game.get_playing():

        # start menu goes here
        menu.display()
        choice = menu.check_state()
        # match choice:
        #     case "Exit":
        #         running = exit_function(menu.DISPLAY)
        #     case "Start new career":
        #         playing = True
        #         game.set_state(True)

        if (choice == "Exit"):
            running = exit_function(menu.DISPLAY)
        if(choice == "Start new career"):
            playing = True
            game.set_state(True)


        while game.get_state():
            # game loop here
            game.run()

if __name__ == "__main__":
    main()
