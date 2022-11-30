import pygame as pg
import random
from game.model.case import Case
from game.model.settings import TILE_SIZE
from game.model.Ressources import Ressources
from game.controller.SelectionRect import SelectionRect
from game.model.road import Road
import pygame.event
import json
import time


class World(pg.sprite.Group):

    def __init__(self, hud, grid_length_x, grid_length_y, width, height, keyboard):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.selected_on = False
        self.selection = None
        self.list_grid_pos_selection = set()

        self.selection_roads = None
        self.list_grid_pos_road = set()

        self.keyboard = keyboard

        self.dim_map = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()  #
        self.images = self.load_images()
        self.world = self.create_world()

        self.temp_cases = []

        self.data = []



        # camera offset
        self.offset = pg.math.Vector2()
        self.half_w = self.width // 2
        self.half_h = self.height // 2

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.2

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pg.Surface(self.internal_surf_size, pg.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pg.math.Vector2(self.internal_surf_size)
        self.internal_offset = pg.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

        self.count = 0

        # Ressources
        self.ressources = Ressources(0, 0, 0, 0, 0, 0)




    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = self.keyboard.get_keyboard_input()
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if self.hud.selected_tile is not None and (0 <= grid_pos[0] <= self.grid_length_x - 1) and (
                0 <= grid_pos[1] <= self.grid_length_y - 1):
            sprite_name = self.hud.selected_tile["name"]

            if mouse_action.get(pg.MOUSEBUTTONDOWN):
                if not self.selected_on:
                    self.selected_on = True
                    if sprite_name == "hud_road_sprite":
                        self.selection_roads = Road(grid_pos, self)
                    else:
                        self.selection = SelectionRect(grid_pos, self)
            elif not mouse_action.get(pg.MOUSEBUTTONDOWN):
                if self.selected_on:
                    self.selected_on = False
                    if sprite_name == "hud_road_sprite":
                        self.selection_roads.add_grid_pos(grid_pos)
                        self.selection_roads.set_image_roads()
                    else:
                        self.selection.add_grid_pos(grid_pos)
                        if sprite_name == "hud_shovel_sprite":
                            self.list_grid_pos_road.difference_update(self.list_grid_pos_selection)
                            self.change_case_sprite_by_image_name(sprite_name)
                        else:
                            self.change_case_sprite_by_image_name(sprite_name)

                    self.temp_cases = []
                    self.list_grid_pos_selection = set()
                    self.selection = None


            if mouse_action.get(pg.MOUSEMOTION):
                for temps_case in self.temp_cases:
                    self.world[temps_case["x"]][temps_case["y"]].set_tile(temps_case["image"])
                if self.selected_on:
                    if sprite_name == "hud_road_sprite":
                        temps_coord = self.selection_roads.add_grid_pos(grid_pos)
                        self.add_temp_case()
                        self.selection_roads.set_image_roads()
                        self.list_grid_pos_road.difference_update(temps_coord)

                    else:
                        self.list_grid_pos_selection = set()
                        self.selection.add_grid_pos(grid_pos)
                        self.add_temp_case()
                        self.change_case_sprite_by_image_name("dirt")
                else:
                    self.temp_cases = []
                    self.add_temp_case(grid_pos)
                    if not self.world[grid_pos[0]][grid_pos[1]].get_collision():
                        self.world[grid_pos[0]][grid_pos[1]].set_tile("sign")
                    else:
                        tile_name = self.world[grid_pos[0]][grid_pos[1]].get_tile()
                        mask = pygame.mask.from_surface(self.images[tile_name])
                        new_surface = mask.to_surface(setcolor=(255,0,0,200), unsetcolor=(0,0,0,0))
                        self.images["temp"] = new_surface
                        self.world[grid_pos[0]][grid_pos[1]].set_tile("temp")
        




    def add_temp_case(self, coord_Case=None):
        """
        ajoute des coordonnées dans la liste des case temporaire pour faire la selection et leurs restituer
        leurs bon sprites
        :return:
        """
        if coord_Case != None:
            x,y = coord_Case
            temp = {
                "image": self.world[x][y].get_tile(),
                "x": x,
                "y": y
            }
            self.temp_cases.append(temp)

            self.data.append(temp)

        else:
            for x, y in self.get_list_grid_pos_road():
                temp = {
                    "image": self.world[x][y].get_tile(),
                    "x": x,
                    "y": y
                }
                self.temp_cases.append(temp)
            for x, y in self.get_list_grid_pos_selection():
                temp = {
                    "image": self.world[x][y].get_tile(),
                    "x": x,
                    "y": y
                }

                if temp not in self.temp_cases:
                    self.temp_cases.append(temp)


    def draw(self, screen, camera):
        camera_scroll_x = camera.get_scroll().x
        camera_scroll_y = camera.get_scroll().y
        screen.blit(self.dim_map, (camera_scroll_x, camera_scroll_y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                case = self.world[x][y]
                rect_case = case.get_render_pos()
                tile = case.get_tile()

                if tile != "":
                    screen.blit(self.images[tile],
                                (rect_case[0] + self.dim_map.get_width() / 2 + camera_scroll_x,
                                 rect_case[1] - (self.images[tile].get_height() - TILE_SIZE) + camera_scroll_y))

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.dim_map.get_width() / 2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile.get_render_pos()
                self.dim_map.blit(self.images["block"],
                                  (render_pos[0] + self.dim_map.get_width() / 2, render_pos[1]))
        return world

    def grid_to_world(self, grid_x, grid_y):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])
        r = random.randint(1, 1000)

        if r <= 50 and r > 5:
            tile = "tree1"
        elif r <= 100 and r >= 50:
            tile = "tree2"
        elif r <= 150 and r >= 100:
            tile = "tree3"
        # elif r <= 1:
        #    tile = "farm"
        else:
            tile = ""
        collision = False if tile == "" else True

        out = Case([grid_x, grid_y], rect, iso_poly, tile, (minx, miny), collision)

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def load_images(self):
        images = {
            "building1": pg.image.load("C3_sprites/C3/paneling_00123.png").convert_alpha(),
            "building2": pg.image.load("C3_sprites/C3/paneling_00131.png"),
            "tree1": pg.image.load("C3_sprites/C3/Land1a_00045.png").convert_alpha(),
            "tree2": pg.image.load("C3_sprites/C3/Land1a_00054.png").convert_alpha(),
            "tree3": pg.image.load("C3_sprites/C3/Land1a_00059.png").convert_alpha(),
            "farm": pg.image.load("C3_sprites/C3/Security_00053.png").convert_alpha(),
            "tree": pg.image.load("C3_sprites/C3/paneling_00135.png").convert_alpha(),
            "block": pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha(),
            "sign": pg.image.load("C3_sprites/C3/Housng1a_00045.png").convert_alpha(),
            "hud_house_sprite": pg.image.load("C3_sprites/C3/Housng1a_00001.png").convert_alpha(),
            "hud_shovel_sprite": pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha(),
            "hud_road_sprite": pg.image.load("C3_sprites/C3/Land1a_00003.png").convert_alpha(),
            "dirt": pg.image.load("C3_sprites/C3/Land2a_00004.png").convert_alpha(),
            # routes
            "road_hover": pygame.image.load("C3_sprites/C3/Land2a_00044.png").convert_alpha(),
            "top_bottom": pygame.image.load("C3_sprites/C3/Land2a_00094.png").convert_alpha(),
            "top_end": pygame.image.load("C3_sprites/C3/Land2a_00104.png").convert_alpha(),
            "bottom_end": pygame.image.load("C3_sprites/C3/Land2a_00102.png").convert_alpha(),
            "right_left": pygame.image.load("C3_sprites/C3/Land2a_00093.png").convert_alpha(),
            "right_end": pygame.image.load("C3_sprites/C3/Land2a_00101.png").convert_alpha(),
            "left_end": pygame.image.load("C3_sprites/C3/Land2a_00101.png").convert_alpha(),
            "turn_right_to_bottom": pygame.image.load("C3_sprites/C3/Land2a_00097.png").convert_alpha(),
            "turn_bottom_to_left": pygame.image.load("C3_sprites/C3/Land2a_00098.png").convert_alpha(),
            "turn_left_to_top": pygame.image.load("C3_sprites/C3/Land2a_00099.png").convert_alpha(),
            "turn_top_to_right": pygame.image.load("C3_sprites/C3/Land2a_00100.png").convert_alpha(),
            "crossroad_left_bottom_right": pygame.image.load("C3_sprites/C3/Land2a_00106.png").convert_alpha(),
            "crossroad_top_bottom_left": pygame.image.load("C3_sprites/C3/Land2a_00107.png").convert_alpha(),
            "crossroad_top_right_left": pygame.image.load("C3_sprites/C3/Land2a_00108.png").convert_alpha(),
            "crossroad_top_right_bottom": pygame.image.load("C3_sprites/C3/Land2a_00109.png").convert_alpha(),
            "cross": pygame.image.load("C3_sprites/C3/Land2a_00110.png").convert_alpha(),
            "fire": pygame.image.load('C3_sprites/C3/Land2a_00190.png').convert_alpha()
        }

        return images

    def get_case(self, i, j):
        return self.world[i][j]

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_y)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

    def get_list_grid_pos_road(self):
        return self.list_grid_pos_road

    def get_list_grid_pos_selection(self):
        return self.list_grid_pos_selection

    def add_list_grid_pos_road(self, grid_pos_road):
        self.list_grid_pos_road.add(grid_pos_road)

    def add_list_grid_pos_selection(self, grid_pos_selection):
        self.list_grid_pos_selection.add(grid_pos_selection)

    def set_case_image_by_coord(self, coord, sprite_name):
        x, y = coord
        self.world[x][y].set_tile(sprite_name)

    def change_case_sprite_by_image_name(self, image_name):
        cases = [self.world[x][y] for x, y in self.get_list_grid_pos_selection() if
                 0 <= x <= self.grid_length_x and 0 <= y <= self.grid_length_y]
        for case in cases:
            case.set_tile(image_name)
            if (image_name == 'hud_house_sprite'):
                self.ressources.sub_dinars(10)


    def __str__(self):
        return f"food: {self.ressources.food} water: {self.ressources.water} pence: {self.ressources.pence} dinars: {self.ressources.dinars} workers: {self.ressources.workers} Population: {self.ressources.population}"

    def can_get_fire(self):
        '''get every sprite of the map'''
        for i in range(self.grid_length_x):
            for j in range(self.grid_length_y):
                continue
                '''if self.world[i][j].on_fire == True:
                    self.world[i][j].fire = Fire(self.world[i][j].get_case_rect().topleft)
                    self.world[i][j].fire.update()
                    self.world[i][j].fire.draw(self.screen) '''
