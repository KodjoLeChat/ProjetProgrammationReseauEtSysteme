from turtle import back, screensize
import pygame as pg
from .utils import draw_text


class Hud:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.hudbase = pg.image.load("C3_sprites/C3/paneling_00017.png")
       
        # building hud
        self.build_surface = pg.Surface((width * 0.2, height), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width, self.height*3))
        self.build_surface.blit(self.hudbase, [0,0])

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None

    def create_build_hud(self):

        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5

        tiles = []

        for image_name, image in self.images.items():

            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):

        # build hud
        screen.blit(self.build_surface, (self.width * 0.895, 20))

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"])

        # resources
        pos = self.width 
        for resource in ["wood:", "stone:", "gold:"]:
            draw_text(screen, resource, 30, (255, 255, 255), (pos, 0))
            pos += 100

    def load_images(self):

        # read images
        building1 = pg.image.load("C3_sprites/C3/Citizen01_00022.png")
        building2 = pg.image.load("C3_sprites/C3/Citizen01_00002.png")
        tree = pg.image.load("C3_sprites/C3/Citizen01_00032.png")
        rock = pg.image.load("C3_sprites/C3/Citizen01_00042.png")
        side = pg.image.load("C3_sprites/C3/paneling_00097.png")
        sideMouse = pg.image.load("C3_sprites/C3/paneling_00098.png")

        images = {
            "building1": building1,
            "building2": building2,
            "tree": tree,
            "rock": rock
        }

        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image

