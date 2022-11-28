import pygame

TILE_SIZE = 25

delta_H = 30
ROAD_TYPE = "default"
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1000,800))
WIDHT, HEIGHT = screen.get_size()
# Menu Principal:
text_buttons_menuP = ["ROMULUS", "Start_new_career", "Load_saved_game_", "Exit"]
images_menuP = [None, None, None, None, None]
fonts_menuP = [("white", "Milk"), ("red", "Milk"), ("red", "Milk"), ("red", "Milk")]
delta_Button_menuP = [(60, 2), (15, 2), (15, 2), (60, 2)]  # la differnce entre la pos d un button et pos init
delta_text_menuP = [(10, 2), (20, 2), (20, 2), (10, 2)]  # la difference entre le text et la pos d un boutton
size_bg_button = [(13 * len(txt), 20) for txt in text_buttons_menuP]
init_pos = [WIDHT / 2 - 100, HEIGHT / 2 - 105, 50]
# initial position of the first button (x,y)
# delta_H the last variable.

# Menu Exit
init_pos_exit = [WIDHT / 2 - 150, HEIGHT / 2 - 125, 30]
dim_menu_exit = (300, 250)
pos_button_exit = [(init_pos_exit[0] + 4 * dim_menu_exit[0] / 10, init_pos_exit[1] + dim_menu_exit[1] / 10),
                   (init_pos_exit[0] + 2 * dim_menu_exit[0] / 10, init_pos_exit[1] + 3 * dim_menu_exit[1] / 10),
                   (init_pos_exit[0] + 3 * dim_menu_exit[0] / 10, init_pos_exit[1] + 5 * dim_menu_exit[1] / 10),
                   (init_pos_exit[0] + 5 * dim_menu_exit[0] / 10, init_pos_exit[1] + 5 * dim_menu_exit[1] / 10)]
texts = ["QUIT", "Leave_the_Empire?", "", ""]
size_bg_button_exit = [(10 * len(txt), 20) for txt in texts]
delta_text_menuExit = [(10, 2), (10, 2), (0, 2), (0, 2), (0, 2)]  # la difference entre le text et la pos d un boutton

# Barre
init_pos_barre = [0, 0, 30]
dim_menu_barre = (900, 10)

# Font
dx_car = 10  # distance between caracters
