import pygame
import pygame as pg
import random

from game.model.EngeneerPost import EngeneerPost
from game.model.settings import *
from game.model.road import Road
from game.controller.SelectionBuilding import SelectionBuilding
from game.model.case import Case
from game.controller.Walker import Migrant
from game.model.worldModel import WorldModel
from game.model.House import House
from game.model.timer import Timer
import pickle
import easygui
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from PIL import Image


def load_images():
    images = {
        "building1": pg.image.load("C3_sprites/C3/paneling_00123.png").convert_alpha(),
        "building2": pg.image.load("C3_sprites/C3/paneling_00131.png"),
        "tree1": pg.image.load("C3_sprites/C3/Land1a_00045.png").convert_alpha(),
        "tree2": pg.image.load("C3_sprites/C3/Land1a_00054.png").convert_alpha(),
        "tree3": pg.image.load("C3_sprites/C3/Land1a_00059.png").convert_alpha(),
        "farm": pg.image.load("C3_sprites/C3/Security_00053.png").convert_alpha(),
        "tree": pg.image.load("C3_sprites/C3/paneling_00135.png").convert_alpha(),
        "grass": pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha(),
        "block": pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha(),
        "water_left": pg.image.load("C3_sprites/C3/Land1a_00133.png").convert_alpha(),
        "water_right": pg.image.load("C3_sprites/C3/Land1a_00143.png").convert_alpha(),
        "water": pg.image.load("C3_sprites/C3/Land1a_00120.png").convert_alpha(),
        "rock": pg.image.load("C3_sprites/C3/Land1a_00293.png").convert_alpha(),
        "sign": pg.image.load("C3_sprites/C3/Housng1a_00045.png").convert_alpha(),
        "hud_house_sprite": pg.image.load("C3_sprites/C3/Housng1a_00001.png").convert_alpha(),
        "house_broken": pg.image.load("C3_sprites/C3/Land2a_00115.png").convert_alpha(),
        "hud_shovel_sprite": pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha(),
        "hud_road_sprite": pg.image.load("C3_sprites/C3/Land1a_00003.png").convert_alpha(),
        "dirt": pg.image.load("C3_sprites/C3/Land2a_00004.png").convert_alpha(),
        "migrant": pygame.image.load("C3_sprites/C3/citizen02_00024.png").convert_alpha(),
        "engineer": pygame.image.load("C3_sprites/C3/Citizen01_01141.png").convert_alpha(),
        "hud_hammer_sprite": pygame.image.load("C3_sprites/C3/transport_00056.png").convert_alpha(),

        #pillier pour la jauge
        "head_white_pillar": pygame.image.load("C3_sprites/C3/Sprites_00009.png").convert_alpha(),
        "body_white_pillar": pygame.image.load("C3_sprites/C3/Sprites_00010.png").convert_alpha(),
        "bottom_white_pillar": pygame.image.load("C3_sprites/C3/Sprites_00011.png").convert_alpha(),

        "head_orange_pillar": pygame.image.load("C3_sprites/C3/Sprites_00012.png").convert_alpha(),
        "body_orange_pillar": pygame.image.load("C3_sprites/C3/Sprites_00013.png").convert_alpha(),
        "bottom_orange_pillar": pygame.image.load("C3_sprites/C3/Sprites_00014.png").convert_alpha(),

        "head_orange_red_pillar": pygame.image.load("C3_sprites/C3/Sprites_00015.png").convert_alpha(),
        "body_orange_red_pillar": pygame.image.load("C3_sprites/C3/Sprites_00016.png").convert_alpha(),
        "bottom_orange_red_pillar": pygame.image.load("C3_sprites/C3/Sprites_00017.png").convert_alpha(),

        "head_red_pillar": pygame.image.load("C3_sprites/C3/Sprites_00018.png").convert_alpha(),
        "body_red_pillar": pygame.image.load("C3_sprites/C3/Sprites_00019.png").convert_alpha(),
        "bottom_red_pillar": pygame.image.load("C3_sprites/C3/Sprites_00020.png").convert_alpha(),

        # routes
        "road_hover": pg.image.load("C3_sprites/C3/Land2a_00044.png").convert_alpha(),
        "top_bottom": pg.image.load("C3_sprites/C3/Land2a_00094.png").convert_alpha(),
        "top_end": pg.image.load("C3_sprites/C3/Land2a_00104.png").convert_alpha(),
        "bottom_end": pg.image.load("C3_sprites/C3/Land2a_00102.png").convert_alpha(),
        "right_left": pg.image.load("C3_sprites/C3/Land2a_00093.png").convert_alpha(),
        "right_end": pg.image.load("C3_sprites/C3/Land2a_00101.png").convert_alpha(),
        "left_end": pg.image.load("C3_sprites/C3/Land2a_00101.png").convert_alpha(),
        "turn_right_to_bottom": pg.image.load("C3_sprites/C3/Land2a_00097.png").convert_alpha(),
        "turn_bottom_to_left": pg.image.load("C3_sprites/C3/Land2a_00098.png").convert_alpha(),
        "turn_left_to_top": pg.image.load("C3_sprites/C3/Land2a_00099.png").convert_alpha(),
        "turn_top_to_right": pg.image.load("C3_sprites/C3/Land2a_00100.png").convert_alpha(),
        "crossroad_left_bottom_right": pg.image.load("C3_sprites/C3/Land2a_00106.png").convert_alpha(),
        "crossroad_top_bottom_left": pg.image.load("C3_sprites/C3/Land2a_00107.png").convert_alpha(),
        "crossroad_top_right_left": pg.image.load("C3_sprites/C3/Land2a_00108.png").convert_alpha(),
        "crossroad_top_right_bottom": pg.image.load("C3_sprites/C3/Land2a_00109.png").convert_alpha(),
        "cross": pg.image.load("C3_sprites/C3/Land2a_00110.png").convert_alpha(),

        "speedDown": pg.image.load("C3_sprites/C3/paneling_down.png").convert_alpha(),

        "load_game": pg.image.load("C3_sprites/C3/Screenshot_4.png").convert_alpha(),
        "save_game": pg.image.load("C3_sprites/C3/Screenshot_7.png").convert_alpha(),

        "pause": pg.image.load("C3_sprites/C3/Screenshot_8.png"),

        "speedUp": pg.image.load("C3_sprites/C3/paneling_up.png").convert_alpha(),

        "fire": pygame.image.load('C3_sprites/C3/Land2a_00190.png').convert_alpha(),

    }

    return images


def cart_to_iso(x, y):
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y

def land():
    im = Image.open("land.png")
    px = im.load()
    return px

def grid_to_world(grid_x, grid_y):
    rect = [
        (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
        (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
        (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
        (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
    ]

    iso_poly = [cart_to_iso(x, y) for x, y in rect]

    minx = min([x for x, y in iso_poly])
    miny = min([y for x, y in iso_poly])
    couleurs = land()
    clr_x_y = couleurs[grid_x-1, grid_y-1]
    clr = (clr_x_y[0], clr_x_y[1], clr_x_y[2])

    match clr:
        case (0, 162, 232):
            tile = "water"
        case (34, 177, 76):
            tile = "grass"
        case (20, 102, 44):
            tile = "tree1"
        case (212, 212, 212):
            tile = "rock"
        case (70, 70, 70):
            tile = "water_left"
        case (130, 130, 130):
            tile = "water_right"
        case _:
            tile = "grass"
    collision = False if tile == "grass" else True

    out = Case([grid_x, grid_y], rect, iso_poly, tile, (minx, miny), collision)

    return out


class WorldController:
    def __init__(self, hud, grid_length_x, grid_length_y, width, height, keyboard, ressources):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.speed = 1
        # images
        self.images = load_images()

        # create world
        self.dim_map = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()

        self.worldModel = WorldModel(self.create_world())

        # selection building
        self.selection_building = None
        self.selected_on = False
        self.selection = None

        # selection shovel
        self.selection_shovel = None

        # selection road
        self.selection_roads = None

        # temporary case for selection
        self.temp_cases = []
        self.walkers = []

        # keyboard
        self.keyboard = keyboard

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

        # Ressource
        self.ressources = ressources

        self.hud_w = self.width // 2
        # HUD RECT
        '''declare hud_rect'''
        self.hud_rect = pg.Rect(0, 0, WIDHT - self.hud.hudbase_below.get_width() + 12, HEIGHT)

        # TIMER
        self.actual_time = pygame.time.get_ticks()
        self.time = Timer()

        # FIRE
        self.data = []

        # MINIMAP SCALE
        self.minimap_scale = 0.045

        # TIME
        self.time_Co = 100
        self.speed_Show = 1

    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile.get_render_pos()
                self.dim_map.blit(self.images["grass"],
                                  (render_pos[0] + self.dim_map.get_width() / 2, render_pos[1]))
        return world

    def draw(self, screen, camera):
        camera_scroll_x = camera.get_scroll().x
        camera_scroll_y = camera.get_scroll().y
        screen.blit(self.dim_map, (camera_scroll_x, camera_scroll_y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                case = self.worldModel.get_case(x, y)
                building = case.get_building()
                rect_case = case.get_render_pos()
                tile = case.get_tile()
                if tile != "":
                    screen.blit(self.images[tile],
                                (rect_case[0] + self.dim_map.get_width() / 2 + camera_scroll_x,
                                 rect_case[1] - (self.images[tile].get_height() - TILE_SIZE) + camera_scroll_y))
                    if building:
                        if self.keyboard.get_keyboard_input().get(pygame.K_a):
                            self.draw_jauge_building(case,screen,camera)
        self.draw_walkers(screen, camera_scroll_x, camera_scroll_y)

    def draw_jauge_building(self, case,screen, camera):
        camera_scroll_x = camera.get_scroll().x
        camera_scroll_y = camera.get_scroll().y
        rect_case = case.get_render_pos()
        building = case.get_building()
        if type(building).__name__ == "House":
            jauges = building.get_pillar()
            hauteur_total_pillier = 0
            for pillar_name,count in jauges.items():
                for i in range(1,count+1):
                    if pillar_name == "body_pillar":
                        pillar = building.get_body_pillard()
                        hauteur = (self.images[pillar].get_height() + hauteur_total_pillier)
                        screen.blit(self.images[pillar],
                                    (rect_case[0] + self.dim_map.get_width() /2 + camera_scroll_x + 16,
                                    (rect_case[1] - hauteur) +TILE_SIZE+ camera_scroll_y)
                                    )
                        hauteur_total_pillier = hauteur
                    elif pillar_name == "bottom_pillar":
                        pillar = building.get_bottom_pillard()
                        screen.blit(self.images[pillar],
                                    (rect_case[0] + self.dim_map.get_width() / 2 + camera_scroll_x  + self.images[pillar].get_height() / 4 ,
                                     (rect_case[1] - (self.images[pillar].get_height() - TILE_SIZE)) + camera_scroll_y)
                                    )
                        hauteur_total_pillier = self.images[pillar].get_height()/2
                    else :
                        pillar = building.get_head_pillard()
                        screen.blit(self.images[pillar],
                                    (rect_case[0] + self.dim_map.get_width() / 2 + camera_scroll_x + 4,
                                     (rect_case[1] - (self.images[
                                                          pillar].get_height() + hauteur_total_pillier - TILE_SIZE)) + camera_scroll_y)
                                    )
                        hauteur_total_pillier += self.images[pillar].get_height() + hauteur_total_pillier - TILE_SIZE




    def draw_minimapR(self, screen, camera):
        # Calculate the scale of the minimap relative to the full-size map
        mouse_action = self.keyboard.get_keyboard_input()
        if mouse_action.get(pg.K_b):
            self.minimap_scale += 0.1
        if mouse_action.get(pg.K_c) and self.minimap_scale > 0.1:
            self.minimap_scale -= 0.1

        minimap_width = int(camera.get_scroll().x * self.minimap_scale)
        minimap_height = int(camera.get_scroll().y * self.minimap_scale)

        # Create a new surface to draw the minimap on
        minimap_surface = pygame.Surface((150, 120))

        # Loop through each tile in the full-size map and draw it on the minimap surface
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                case = self.worldModel.get_case(x, y)
                rect_case = case.get_render_pos()
                tile = case.get_tile()
                if tile != "":
                    # Scale the tile image down to fit on the minimap surface
                    scaled_tile = pygame.transform.scale(self.images[tile], (
                    int(self.images[tile].get_width() * self.minimap_scale),
                    int(self.images[tile].get_height() * self.minimap_scale)))
                    # Draw the scaled tile on the minimap surface
                    minimap_surface.blit(scaled_tile,
                                         (rect_case[0] * self.minimap_scale + 74 + minimap_width, rect_case[1] * self.minimap_scale + 30 + minimap_height))

        # Draw the minimap surface on the main screen
        screen.blit(minimap_surface, (WIDHT - self.hud.hudbase.get_width() + 4, 50))

    def update_walkers(self):
        for walker in self.walkers:
            walker.move_to_home()
            if len(walker.get_path()) != 0:
                if walker.get_path()[0] == walker.get_home_pos():
                    if walker.get_reset():
                        pos_x, pos_y = walker.get_path()[0]
                        new_path = self.bad_pathfind(pos_x, pos_y)
                        walker.set_path(new_path)
                        walker.reset_path_retour()
                        walker.set_reset(False)

    def draw_walkers(self, screen, camera_scroll_x, camera_scroll_y):
        for walker in self.walkers:
            if len(walker.get_path()) != 0:
                case = self.worldModel.get_case(walker.get_pos()[0], walker.get_pos()[1])
                rect_case = case.get_render_pos()
                sprite = walker.get_sprite()
                screen.blit(self.images[sprite], (rect_case[0] + self.dim_map.get_width() / 2 + camera_scroll_x,
                                                  rect_case[1] - (self.images[
                                                                      sprite].get_height() - TILE_SIZE) + camera_scroll_y))

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

    def changeTime(self):
        mouse_action = self.keyboard.get_keyboard_input()

        if mouse_action.get(pg.MOUSEBUTTONDOWN):
            if self.hud.selected_button is not None and self.hud.selected_fileList is None and self.hud.selected_tile is None:
                sprite_name = self.hud.selected_button["name"]
                if (sprite_name == "speedDown"):
                    if self.speed >= 1 and self.speed < 5:
                        self.speed += 1
                    if self.speed < 1:
                        self.speed += 0.1
                    self.time_Co = 100 * self.speed * 10
                if (sprite_name == "speedUp"):
                    if self.speed > 1:
                        self.speed -= 1
                    if self.speed <= 1 and self.speed > 0.1:
                        self.speed -= 0.1
                    self.time_Co = 100 * self.speed * 10

                if (sprite_name == "speedUp"):
                    if self.speed_Show >= 1 and self.speed_Show < 5:
                        self.speed_Show += 1
                    if self.speed_Show < 1:
                        self.speed_Show += 0.1
                if (sprite_name == "speedDown"):
                    if self.speed_Show > 1:
                        self.speed_Show -= 1
                    if self.speed_Show <= 1 and self.speed_Show > 0.1:
                        self.speed_Show -= 0.1


        font = pg.font.Font(None, 25)        
        text = font.render('{} %'.format(self.speed_Show*100), 0, (0, 0, 0))
        screen.blit(text, (WIDHT - WIDHT*0.03, HEIGHT //2 +50) )

    def FileSelector(self):
        mouse_action = self.keyboard.get_keyboard_input()
        if mouse_action.get(pg.MOUSEBUTTONDOWN):
            if self.hud.selected_fileList is not None and self.hud.selected_tile is None and self.hud.selected_button is None:
                sprite_name = self.hud.selected_fileList["name"]
                if (sprite_name == "load_game"):
                    path = easygui.fileopenbox()
                    file = open(path, 'rb')
                    self.worldModel = pickle.load(file)

    def FileRegister(self):
        mouse_action = self.keyboard.get_keyboard_input()
        if mouse_action.get(pg.MOUSEBUTTONDOWN):
            if self.hud.selected_fileList is not None and self.hud.selected_tile is None and self.hud.selected_button is None:
                sprite_name = self.hud.selected_fileList["name"]
                if (sprite_name == "save_game"):
                    path = easygui.fileopenbox()
                    self.saveWord(path)

    def update(self, camera):
        self.FileRegister()
        self.FileSelector()
        self.changeTime()
        self.time.update(self.speed)

        now = pygame.time.get_ticks()
        if (now - self.actual_time > self.time_Co):
            self.update_building()
            self.update_walkers()
            self.actual_time = now
        self.update_mouse_action(camera)

    def update_mouse_action(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = self.keyboard.get_keyboard_input()
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        for temps_case in self.temp_cases:
            self.worldModel.get_case(temps_case["x"], temps_case["y"]).set_tile(temps_case["image"])
        if self.hud.selected_tile is not None and (0 <= grid_pos[0] <= self.grid_length_x - 1) and (
                0 <= grid_pos[1] <= self.grid_length_y - 1):
            sprite_name = self.hud.selected_tile["name"]

            if mouse_action.get(pg.MOUSEBUTTONDOWN):
                if not self.selected_on:
                    if sprite_name == "hud_road_sprite" and not self.worldModel.get_case(grid_pos[0],
                                                                                         grid_pos[1]).get_collision():
                        self.selection_roads = Road(grid_pos, self.worldModel)
                        self.selected_on = True
                    elif sprite_name == "hud_shovel_sprite":
                        self.selection_shovel = SelectionBuilding(grid_pos, self.worldModel)
                        self.selected_on = True
                    elif sprite_name and not self.worldModel.get_case(grid_pos[0], grid_pos[
                        1]).get_collision():
                        self.selection_building = SelectionBuilding(grid_pos, self.worldModel)
                        self.selected_on = True

            elif not mouse_action.get(pg.MOUSEBUTTONDOWN):
                if self.selected_on:
                    self.selected_on = False
                    if sprite_name == "hud_road_sprite":
                        cases = self.selection_roads.add_grid_pos(grid_pos)
                        self.selection_roads.set_image_roads()
                        self.change_cases_collision(True, cases)
                    else:
                        if sprite_name == "hud_shovel_sprite":
                            case_to_delete = self.selection_shovel.add_grid_pos_to_erase(grid_pos)
                            self.worldModel.diff_update_road(case_to_delete)
                            self.worldModel.diff_update_building(case_to_delete)
                            self.change_case_sprite_by_image_name(sprite_name, case_to_delete)
                            self.update_case(sprite_name, case_to_delete)
                            self.change_cases_collision(False, case_to_delete)
                        elif sprite_name:
                            coord_cases = self.selection_building.add_grid_pos(grid_pos)
                            cases_without_col = [coord for coord in coord_cases if not self.worldModel.get_case(coord[0],coord[1]).get_collision()]
                            self.change_case_sprite_by_image_name(sprite_name, cases_without_col)
                            self.update_case(sprite_name,cases_without_col)
                            self.change_cases_collision(True, cases_without_col)

                    self.temp_cases = []
                    self.selection_building = None
                    self.selection_shovel = None
                    self.selection_roads = None

            if mouse_action.get(pg.MOUSEMOTION) and mouse_action.get(pg.MOUSEBUTTONDOWN):

                if self.selected_on:
                    if sprite_name == "hud_road_sprite":
                        temps_coord = self.selection_roads.add_grid_pos(grid_pos)
                        self.add_temp_case(temps_coord)
                        self.selection_roads.set_image_roads()
                        self.worldModel.diff_update_road(temps_coord)
                    elif sprite_name == "hud_shovel_sprite":
                        temps_coord = self.selection_shovel.add_grid_pos_to_erase(grid_pos)
                        self.add_temp_case(temps_coord)
                        self.change_case_sprite_by_image_name("dirt", temps_coord)
                    else:
                        temps_coord = self.selection_building.add_grid_pos(grid_pos)
                        new_temps_coord = [coord for coord in temps_coord if not self.worldModel.get_case(coord[0],coord[1]).get_collision()]
                        self.add_temp_case(new_temps_coord)
                        self.change_case_sprite_by_image_name("sign", new_temps_coord)
                        self.worldModel.diff_update_building(new_temps_coord)

            elif mouse_action.get(pg.MOUSEMOTION) and not mouse_action.get(pg.MOUSEBUTTONDOWN):
                self.temp_cases = []
                self.add_temp_case(grid_pos)
                if not self.worldModel.get_case(grid_pos[0], grid_pos[1]).get_collision():
                    self.worldModel.get_case(grid_pos[0], grid_pos[1]).set_tile("sign")
                else:
                    tile_name = self.worldModel.get_case(grid_pos[0], grid_pos[1]).get_tile()
                    mask = pg.mask.from_surface(self.images[tile_name])
                    new_surface = mask.to_surface(setcolor=(255, 0, 0, 200), unsetcolor=(0, 0, 0, 0))
                    self.images["temp"] = new_surface
                    self.worldModel.get_case(grid_pos[0], grid_pos[1]).set_tile("temp")

        if mouse_action.get(pygame.K_KP_ENTER):
            self.saveWord()

    def add_temp_case(self, temps_coord):
        """
        ajoute des coordonnées dans la liste des case temporaire pour faire la selection et leurs restituer
        leurs bon sprites
        :return:
        """
        if type(temps_coord) == tuple:
            x, y = temps_coord
            temp = {
                "image": self.worldModel.get_case(x, y).get_tile(),
                "x": x,
                "y": y
            }
            self.temp_cases.append(temp)
        else:
            for x, y in temps_coord:
                temp = {
                    "image": self.worldModel.get_case(x, y).get_tile(),
                    "x": x,
                    "y": y
                }
                if temp not in self.temp_cases:
                    self.temp_cases.append(temp)

    def can_place_tile(self, grid_pos):
        mouse_on_panel = True
        for rect in [self.hud_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = False

        if not mouse_on_panel:
            return True
        else:
            return False

    def change_case_sprite_by_image_name(self, image_name, list_cases):
        cases = [self.worldModel.get_case(x, y) for x, y in list_cases]
        for case in cases:
            if self.can_place_tile(pg.mouse.get_pos()):
                if image_name != "hud_shovel_sprite" and image_name != "speedDown" and image_name != "load_game" and image_name != "save_game" and image_name != "pause" and image_name != "speedUp":
                    case.set_tile(image_name)
                    if image_name == "hud_house_sprite":
                        self.ressources.sub_dinars(10)
                        
                        self.ressources.add_population(5)

                elif image_name == "hud_shovel_sprite":
                    case.set_tile(image_name)

    def update_case(self, sprite_name,coord_cases):
        """
        Met à jour les cases pour leurs ajouter/supprimer un building :param sprite_name: le nom du sprite
        selectionner pour savoir s'il faut supprimer ou ajouter un building aux cases :return: None
        """
        cases = [self.worldModel.get_case(x, y) for x, y in coord_cases]
        for case in cases:
            if sprite_name == "hud_house_sprite":
                # test
                x, y = case.get_grid()
                voisin = list()
                if (x + 1, y) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x + 1, y))
                if (x - 1, y) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x - 1, y))
                if (x, y + 1) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x, y + 1))
                if (x, y - 1) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x, y - 1))


                if len(voisin) != 0:
                    migrant_posx, migrant_posy = 0, 0
                    migrant_destx, migrant_desty = voisin[0][0], voisin[0][1]
                    matrix = self.create_colision_matrix_migrant()
                    path = self.pathfinding(migrant_posx, migrant_posy, migrant_destx, migrant_desty, matrix)
                    migrant = Migrant(0, 0, migrant_destx, migrant_desty, path, "migrant")
                    self.walkers.append(migrant)
                    house = House(case, migrant, voisin,sprite_name)
                else:
                    house = House(case, None, None,sprite_name)
                case.set_building(house)

            elif sprite_name == "hud_hammer_sprite":
                x, y = case.get_grid()
                voisin = list()
                if (x + 1, y) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x + 1, y))
                if (x - 1, y) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x - 1, y))
                if (x, y + 1) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x, y + 1))
                if (x, y - 1) in self.worldModel.get_list_grid_pos_road():
                    voisin.append((x, y - 1))

                voisin_direct = None if len(voisin) == 0 else voisin[0]
                if voisin_direct is not None:

                    migrant_posx, migrant_posy = voisin_direct[0], voisin_direct[1]
                    migrant_destx, migrant_desty = voisin_direct[0], voisin_direct[1]
                    bad_path = self.bad_pathfind(migrant_posx, migrant_posy)
                    migrant = Migrant(0, 0, migrant_destx, migrant_desty, bad_path, "engineer")
                    self.walkers.append(migrant)
                    Engineer_post = EngeneerPost(case, migrant, voisin_direct,sprite_name)
                else:
                    Engineer_post = EngeneerPost(case, None, None, sprite_name)
                case.set_building(Engineer_post)

            elif sprite_name == "hud_shovel_sprite":
                case.set_building(None)

    def update_building(self):
        """
        Update les buildings
        :param case: la case sur laquel est le building
        :return: None
        """
        for x, y in self.worldModel.get_list_grid_pos_building():
            case = self.worldModel.get_case(x, y)
            building = case.get_building()
            if building:
                route_voisine = building.get_route_voisine()
                sprite_name = building.get_sprite_name()
                if type(building).__name__ == "House": # fait en sorte de ne prendre que les classes de type House (le post d'ingénieur ne prend pas de dégats dans le temps
                    # add fire
                    building.add_fire()
                    # add damage
                    building.add_damage()

                    #reset du des damages quand l'ingénieur est à côté
                    for walker in self.walkers:
                        if route_voisine != None:
                            if walker.get_pos() in route_voisine and walker.get_sprite() == "engineer":
                                building.reset_damage()
                                building.reset_pillard()

                    damage = building.get_damage()
                    fire = building.get_fire()
                    if damage >= 100:
                        building.set_sprite("house_broken")
                        building.pillard_to_zero()
                    elif damage == 0 and sprite_name != case.get_tile():
                        building.set_sprite(sprite_name)
                    if fire > 5000:
                        building.set_sprite("fire")

    def change_cases_collision(self, collision, coord_cases):
        cases = [self.worldModel.get_case(x, y) for x, y in coord_cases]
        for case in cases:
            case.set_collision(collision)

    def get_world_model(self):
        return self.worldModel

    def saveWord(self, path):
        with open(path, "wb") as f1:
            pickle.dump(self.worldModel, f1)
        f1.close()

    def create_colision_matrix(self):
        if len(self.worldModel.list_grid_pos_road) != 0:
            matrix = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_LENGTH)]
            for x, y in self.worldModel.get_list_grid_pos_road():
                matrix[x][y] = 1
            return matrix
        return None

    def create_colision_matrix_migrant(self):
        if len(self.worldModel.list_grid_pos_road) != 0:
            matrix = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_LENGTH)]
            for x, y in self.worldModel.get_list_grid_pos_road():
                matrix[y][x] = 1
            return matrix
        return None

    def pathfinding(self, posx_start, posy_start, posx_end, posy_end, matrix):
        if matrix is not None:
            grid = Grid(matrix=matrix)
            start = grid.node(posx_start, posy_start)
            end = grid.node(posx_end, posy_end)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
            path, run = finder.find_path(start, end, grid)
            return path
        return None

    def bad_pathfind(self, posx_start, posy_start):
        matrix = self.create_colision_matrix()
        path = [(posx_start,posy_start)]
        actual_posx = posx_start
        actual_posy = posy_start
        old_posx_start = None
        old_posy_start = None
        voisin = list()
        if matrix is not None:
            limite = 0
            while (limite < 20):
                if matrix[actual_posx - 1][actual_posy]:
                    if (actual_posx - 1, actual_posy) != (old_posx_start, old_posy_start):
                        if actual_posx - 1 != old_posx_start:
                            voisin.append((actual_posx - 1, actual_posy))

                if matrix[actual_posx + 1][actual_posy]:
                    if (actual_posx + 1, actual_posy) != (old_posx_start, old_posy_start):
                        if actual_posx + 1 != old_posx_start:
                            voisin.append((actual_posx + 1, actual_posy))

                if matrix[actual_posx][actual_posy - 1]:
                    if (actual_posx, actual_posy - 1) != (old_posx_start, old_posy_start):
                        if actual_posy - 1 != old_posy_start:
                            voisin.append((actual_posx, actual_posy - 1))

                if matrix[actual_posx][actual_posy + 1]:
                    if (actual_posx, actual_posy + 1) != (old_posx_start, old_posy_start):
                        if actual_posy + 1 != old_posy_start:
                            voisin.append((actual_posx, actual_posy + 1))

                if (len(voisin) != 0):
                    random_voisin = random.choice(voisin)
                    path.append(random_voisin)
                    old_posx_start = actual_posx
                    old_posy_start = actual_posy
                    actual_posx = random_voisin[0]
                    actual_posy = random_voisin[1]
                voisin = list()
                limite += 1
            return path
