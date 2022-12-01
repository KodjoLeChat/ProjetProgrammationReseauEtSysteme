from game.view.menu import *
from game.model.settings import *
from game.controller.game import Game
from game.view.utils import *
def main():

    running = True
    playing = False
    old_game = False

    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock()


    # implement menus
    menu = Menu(text_buttons_menuP, init_pos,screen)
    menu.set()

    # implement game
    game = Game(screen, clock)

    while game.get_playing():

        # start menu goes here
        menu.display()
        choice = menu.check_state()
        match choice:
            case "Exit":
                running = exit_function(screen)
            case "Start_new_career":
                playing = True
                game.set_state(True)
            case "Load_saved_game":
                old_game = True
                playing = True
                game.set_state(True)
        while game.get_state():
            # game loop here
            if old_game:
                # with saved data
                game.run()
            else:
                game.run()

if __name__ == "__main__":
    main()
