
import pygame as pg
from game.game import Game


def main():

    running = True
    playing = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((900, 700))
    clock = pg.time.Clock()

    # implement menus

    # implement game
    game = Game(screen, clock)

    while running:

        # start menu goes here

        while playing:
            # game loop here
            game.run()
            playing = False
        running = False

if __name__ == "__main__":
    main()
