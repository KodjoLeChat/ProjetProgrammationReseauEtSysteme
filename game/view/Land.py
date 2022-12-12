from PIL import Image
import pygame as pg
tree = [f"C3_sprites/C3/Land1a_000{30 + i}.png" for i in range(32)]
grass = [f"C3_sprites/C3/Land1a_000{62 + i}.png" for i in range(38)] + [f"C3_sprites\C3\Land1a_00{100 + i}.png" for i in range(20)]
water = [f"C3_sprites/C3/Land1a_001{20 + i}.png" for i in range(8)]
left_border = [f"C3_sprites/C3/Land1a_001{23 + i}.png" for i in range(3)]
rock = [f"C3_sprites/C3/Land1a_00{290 + i}.png" for i in range(14)]

map_sprites = {(28,76,27):tree,
                (0,255,0) : grass,
                (0,0,255) : water,
                (0,158,181) : left_border,
                (131, 61,10) : rock,
               }

class Land():

    def __init__(self, screen, image):
        self.screen = screen
        self.image = image


    def draw(self):
        with Image.open(self.image) as im:
            # im.show()
            scale_factor = 0.5
            x, y = im.size
            dx, dy =0, 0
            deltax, deltay =0, 0
            for i in range(x):
                for j in range(y):
                    color = im.getpixel((i, j))
                    if color in map_sprites.keys():
                        image = pg.image.load(map_sprites[color][0])
                    image = pg.transform.scale(image, (20*scale_factor, 10*scale_factor))
                    size_delta = image.get_size()
                    self.screen.blit(image, (dy +20, dx+10))
                    #print(size_delta)
                    dx += size_delta[1]
                dy += size_delta[0]/2
                if i % 2 == 0:
                    dx = size_delta[1]/2
                else:
                    dx = 0






            # size herbe (58,30)
            # print(im.getbands())  # Returns ('R', 'G', 'B')
            # Image.getcolors(maxcolors=256)
