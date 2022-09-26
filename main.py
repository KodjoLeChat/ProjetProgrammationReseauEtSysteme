from game.settings import *
from game.game import Game
from menu import *


def main():

    running = True
    playing = False

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menus
    menu = Menu(text_buttons, L_center, H_center, delta_H)
    menu.set()

    # implement game
    game = Game(screen, clock)

    while running:

        # start menu goes here
        menu.display()
        choice = menu.check_state()
        match choice:
            case "Exit":
                running = exit_function(menu.DISPLAY)
            case "Start new career":
                playing = True
        while playing:
            # game loop here
            game.run()

if __name__ == "__main__":
    main()
