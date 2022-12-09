#from turtle import back, screensize
import pygame as pg
from game.view.utils import draw_text


class Hud:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.hud_colour = (198, 155, 93, 175)

        # building hud
        self.build_surface = pg.Surface((width, height), pg.SRCALPHA)
        self.hudbase = pg.image.load("C3_sprites/C3/paneling_00017.png")
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.build_surface.blit(self.hudbase, [0, 0])

        # resouces hud
        self.resouces_surface = pg.Surface((width, height * 0.025), pg.SRCALPHA)
        self.resources_rect = self.resouces_surface.get_rect(topleft=(0, 0))
        self.resouces_surface.fill(self.hud_colour)

        # select hud
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        self.images = {"house":"hud_house_sprite",
                       "shovel":"hud_shovel_sprite",
                       "road":"hud_road_sprite"}

        self.tiles = self.create_build_hud()

        self.selected_tile = None

    def create_build_hud(self):

        render_pos = [self.width * 0.901, self.height * 0.343]
        object_width = self.build_surface.get_width() // 35

        tiles = []

        for image_name, sprite_name in self.images.items():
            pos = render_pos.copy()
            image_tmp = self.get_sprite_by_hud_tile(image_name)
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": sprite_name,
                    "icon": image_scale,
                    "rect": rect
                }
            )

            render_pos[0] += image_scale.get_width() + 8

        return tiles

    def update(self):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None
        elif mouse_action[0]:
            for tile in self.tiles:
                if tile["rect"].collidepoint(mouse_pos):
                    self.selected_tile = tile

    def draw(self, screen):

        if self.selected_tile is not None:
            img = self.selected_tile["icon"].copy()
            img.set_alpha(100)
            screen.blit(img, pg.mouse.get_pos())

        # build hud
        screen.blit(self.build_surface, (self.width * 0.895, 20))

        # resouce hud
        screen.blit(self.resouces_surface, (0, 0))

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"])

        # resources
        pos = self.width
        for resource in ["wood:", "stone:", "gold:"]:
            draw_text(screen, resource, 30, (255, 255, 255), (pos, 0))
            pos += 10

    def get_sprite_by_hud_tile(self,image_name):
        match image_name:
            case "house":
                return pg.image.load("C3_sprites/C3/paneling_00123.png")
            case "shovel":
                return pg.image.load("C3_sprites/C3/paneling_00131.png")
            case "road":
                return pg.image.load("C3_sprites/C3/paneling_00135.png")

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
