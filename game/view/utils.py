import pygame as pg
CARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!\"%*()-+=:;,?\/'._"
FONT = {"blue1":1, "blue2": 135,"white": 269, "red": 403, "black1": 537, "black2": 671, "nn": 805}

def draw_text(screen, text, size, colour, pos):

    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)

def extract_image_path(car: object, font: object) -> object:
    # Return the path of the letter's sprites
    path = "Caracter is not found!"
    if car in CARS:
        index = CARS.index(car)
        gap = FONT[font]
        var = index+gap
        var_str = str(var)
        if var < 10:
            var_str = "00" + str(var)
        elif var < 100:
            var_str = "0"+str(var)
        path = "C3_sprites/C3/fonts_00"+var_str+".png"
    return path

def create_bg(color):
    # Create a background from some frames:
    # Brown : 00028--> 00036
    # milk : 00037 --> 00045
    # [[top_left   , top_middle   , top_right],
    #  [middle_left, middle       , middle_right],
    #  [bottom_left, bottom_middle, bottom_right]]
    match color:
        case "Brown": backgrounds = [[pg.image.load(f"C3_sprites/C3/paneling_000{28+i+j*3}.png") for i in range(3)] for j in range(3)]
        case "Milk": backgrounds = [[pg.image.load(f"C3_sprites/C3/paneling_000{37+i+j*3}.png") for i in range(3)] for j in range(3)]
        case "White": backgrounds = [[pg.image.load(f"C3_sprites/C3/paneling_00{335 + i + j*12}.png") for i in range(12)] for j in range(12)]
        case "Beige": backgrounds = [[pg.image.load(f"C3_sprites/C3/paneling_00{479 + i + j * 7}.png") for i in range(7)] for j in range(7)]
    return backgrounds

def bg_block(display, pos, dim, color="Milk", rescale= True):
    # Create a block as a background.
    # Rescule : if we want to rescule our block.
    backgrounds = create_bg(color)
    L, l = dim
    x, y = pos
    dx, dy = backgrounds[0][0].get_size()
    n = len(backgrounds)
    N_j, N_i = int(L/dx)+1, int(l/dy)+1

    #
    if not rescale:
        for j in range(n):
            for i in range(n):
                display.blit((backgrounds[i][j]), (x + j*dx, y + i * dy))
    else:
        backgrounds_updated = [[backgrounds[i][j] for j in (0, int(n/2), n-1)] for i in (0, int(n/2), n-1)]
        display.blit(backgrounds_updated[0][0], (x, y))
        for j in range(1, N_j):
            display.blit(backgrounds_updated[0][1], (x +j * dx, y))
        display.blit(backgrounds_updated[0][2], (x + L, y))

        for i in range(1, N_i):
            display.blit(backgrounds_updated[1][0], (x, y+i*dy))
            for j in range(1, N_j):
                display.blit(backgrounds_updated[1][1], (x+j*dx, y+i*dy))
            display.blit(backgrounds_updated[1][2], (x+L, y+i*dy))

        display.blit(backgrounds_updated[2][0], (x, y + l))
        for j in range(1, N_j):
            display.blit(backgrounds_updated[2][1], (x + j * dx, y+l))
        display.blit(backgrounds_updated[2][2], (x+L, y + l))
