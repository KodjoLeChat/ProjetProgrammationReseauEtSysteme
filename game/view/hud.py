from turtle import back, screensize
import pygame as pg
from game.view.utils import draw_text
from game.model.worldModel import __str__

from game.model.settings import WIDHT, HEIGHT

class Hud:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.hud_colour = (198, 155, 93, 175)

        # resouces top
        self.resources_rect = pg.image.load("C3_sprites/C3/paneling_00010.png")
        self.resouces_surface = pg.Surface((width, self.resources_rect.get_height()), pg.SRCALPHA)
        self.resouces_surface.blit(self.resources_rect, [0, 0])

        # building hud
        self.hudbase = pg.image.load("C3_sprites/C3/paneling_00017.png")
        self.hudbase_below = pg.image.load("C3_sprites/C3/paneling_00018.png")
        self.hudbase_mid = pg.image.load("C3_sprites/C3/paneling_00519.png")
        self.build_surface = pg.Surface((self.hudbase.get_width(), self.height), pg.SRCALPHA)
        self.build_surface.blit(self.hudbase, [0,0])
        self.build_surface.blit(self.hudbase_below, [0, self.height - self.hudbase_below.get_height() - self.resources_rect.get_height()])

        # select hud
        # self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        # self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        # self.select_surface.fill(self.hud_colour)

        self.images = {"house":"hud_house_sprite",
                       "shovel":"hud_shovel_sprite",
                       "road":"hud_road_sprite",
                       "well":"hud_well_sprite",
                       "hospital":"hud_hospital_sprite",
                       "temple" : "hus_temple_sprite",
                       "book": "hus_book_sprite",
                       "face": "hus_face_sprite",
                       "senate": "hus_senate_sprite",
                       "hammer": "hus_hammer_sprite",
                       "cross": "hus_cross_sprite",
                       "parchemin": "hus_parchemin_sprite",
                       "sword": "hus_sword_sprite",
                       "char": "hus_char_sprite",
                       "bell": "hus_bell_sprite",
                       }

        self.info = {
                    "gov_info": pg.image.load("C3_sprites/C3/paneling_00085.png"),
                    "dom_info": pg.image.load("C3_sprites/C3/paneling_00088.png"),
                    "right": pg.image.load("C3_sprites/C3/paneling_00091.png"),
                    "left": pg.image.load("C3_sprites/C3/paneling_00094.png"),
                    }

        self.tiles = self.create_build_hud()

        self.selected_tile = None
        
    def create_build_hud(self):

        render_pos = [WIDHT - self.hudbase_below.get_width() + 12, (HEIGHT - self.hudbase_below.get_height())/3.17 ]
        object_width = self.build_surface.get_width() // 4

        tiles = []
        count = 0

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

            count += 1
            render_pos[0] += image_scale.get_width() + 10

            if count%3 == 0:
                render_pos[0] = WIDHT - self.hudbase_below.get_width() + 12
                render_pos[1] += image_scale.get_height() + 10

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
        
        for height_base in range( self.hudbase.get_height(), self.build_surface.get_height() - self.hudbase_below.get_height() - 30, self.hudbase_mid.get_height()):
            for width_base in range(0, self.build_surface.get_width() - self.hudbase_mid.get_width(), self.hudbase_mid.get_width()):
                if (width_base == 0):
                    if(height_base == self.hudbase.get_height()):
                        self.build_surface.blit(  pg.image.load("C3_sprites/C3/paneling_00479.png") , [ width_base, height_base])
                    else:
                        if(height_base == self.hudbase.get_height()):
                            self.build_surface.blit(  pg.image.load("C3_sprites/C3/paneling_00521.png") , [ width_base, height_base])
                        else:
                            self.build_surface.blit(  pg.image.load("C3_sprites/C3/paneling_00500.png") , [ width_base, height_base])
                else:
                    self.build_surface.blit(  self.hudbase_mid , [ width_base, height_base])

        # build hud
        screen.blit(self.build_surface, (self.width - self.hudbase.get_width(), self.resources_rect.get_height()))

        # resouce hud
        pos_up_hud = 0
        while pos_up_hud < self.width:
            screen.blit(self.resouces_surface, (pos_up_hud, 0))
            pos_up_hud += self.resources_rect.get_width()
            

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"])

        # resources


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


    def get_sprite_by_hud_tile(self,image_name):
        match image_name:
            case "house": return pg.image.load("C3_sprites/C3/paneling_00123.png")
            case "shovel": return pg.image.load("C3_sprites/C3/paneling_00131.png")
            case "road": return pg.image.load("C3_sprites/C3/paneling_00135.png")
            case "well": return pg.image.load("C3_sprites/C3/paneling_00127.png")
            case "hospital": return pg.image.load("C3_sprites/C3/paneling_00166.png")
            case "temple": return pg.image.load("C3_sprites/C3/paneling_00154.png")
            case "book": return pg.image.load("C3_sprites/C3/paneling_00150.png")
            case "face": return pg.image.load("C3_sprites/C3/paneling_00146.png")
            case "senate": return pg.image.load("C3_sprites/C3/paneling_00142.png")
            case "hammer": return pg.image.load("C3_sprites/C3/paneling_00170.png")
            case "cross": return pg.image.load("C3_sprites/C3/paneling_00162.png")
            case "parchemin": return pg.image.load("C3_sprites/C3/paneling_00158.png")
            case "sword": return pg.image.load("C3_sprites/C3/paneling_00174.png")
            case "char": return pg.image.load("C3_sprites/C3/paneling_00118.png")
            case "bell": return pg.image.load("C3_sprites/C3/paneling_00122.png")