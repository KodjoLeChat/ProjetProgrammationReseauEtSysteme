import pygame
import pygame as pg
import random
from game.model.settings import *
from game.model.road import Road
from game.controller.SelectionBuilding import SelectionBuilding
from game.model.case import Case
from game.controller.walker import Migrant
from game.model.worldModel import WorldModel
from game.model.House import House
from game.model.timer import Timer
import pickle
import easygui


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
        "sign": pg.image.load("C3_sprites/C3/Housng1a_00045.png").convert_alpha(),
        "hud_house_sprite": pg.image.load("C3_sprites/C3/Housng1a_00001.png").convert_alpha(),
        "hud_shovel_sprite": pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha(),
        "hud_road_sprite": pg.image.load("C3_sprites/C3/Land1a_00003.png").convert_alpha(),
        "dirt": pg.image.load("C3_sprites/C3/Land2a_00004.png").convert_alpha(),
        "walker": pygame.image.load("C3_sprites/C3/citizen02_00024.png").convert_alpha(),

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
    
        "speedDown" : pg.image.load("C3_sprites/C3/paneling_down.png").convert_alpha(),
                
        "load_game": pg.image.load("C3_sprites/C3/Screenshot_4.png").convert_alpha(),
        "save_game": pg.image.load("C3_sprites/C3/Screenshot_7.png").convert_alpha(),


        "speedUp" : pg.image.load("C3_sprites/C3/paneling_up.png").convert_alpha(),

        "fire": pygame.image.load('C3_sprites/C3/Land2a_00190.png').convert_alpha(),


    }

    return images


def cart_to_iso(x, y):
    iso_x = x - y
    iso_y = (x + y) / 2
    return iso_x, iso_y


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
    r = random.randint(1, 1000)

    if 50 >= r > 5:
        tile = "tree1"
    elif 100 >= r >= 50:
        tile = "tree2"
    elif 150 >= r >= 100:
        tile = "tree3"
    # elif r <= 1:
    #    tile = "farm"
    else:
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
        self.hud_rect = pg.Rect(0, 0, WIDHT-self.hud.hudbase_below.get_width() + 12, HEIGHT)

        # TIMER
        self.time = Timer()

        # FIRE
        self.data = []





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
                rect_case = case.get_render_pos()
                tile = case.get_tile()
                if tile != "":
                    screen.blit(self.images[tile],
                                (rect_case[0] + self.dim_map.get_width() / 2 + camera_scroll_x,
                                 rect_case[1] - (self.images[tile].get_height() - TILE_SIZE) + camera_scroll_y))
        self.draw_walkers(screen, camera_scroll_x, camera_scroll_y)
    
    def update_walkers(self):
        for walker in self.walkers:
            walker.move_to_home()

    def draw_walkers(self, screen, camera_scroll_x, camera_scroll_y):
        for walker in self.walkers:
            screen.blit(self.images["walker"], (walker.pos_x + self.dim_map.get_width() / 2 + camera_scroll_x,
                                                walker.pos_y - (self.images[
                                                                    "walker"].get_height() - TILE_SIZE) + camera_scroll_y))

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
            if self.hud.selected_tile is not None:
                sprite_name = self.hud.selected_tile["name"]
                if (sprite_name =="speedUp"):
                        if self.speed >= 1 and self.speed < 5:
                            print("ok tu changes le tps")
                            self.speed += 1
                        if self.speed < 1:
                            print("ok tu changes le tps")
                            self.speed += 0.1
                if (sprite_name =="speedDown"):
                        if self.speed > 1:
                            self.speed -= 1
                        if self.speed <= 1 and self.speed > 0.1:
                            self.speed -= 0.1
                            
    def FileSelector(self):
        mouse_action = self.keyboard.get_keyboard_input()
        if mouse_action.get(pg.MOUSEBUTTONDOWN):
            if self.hud.selected_tile is not None:
                sprite_name = self.hud.selected_tile["name"]
                if (sprite_name =="load_game"):
                    print("load_game")
                    path = easygui.fileopenbox()
                    file = open(path, 'rb')
                    self.worldModel = pickle.load(file)


    def FileRegister(self):
        mouse_action = self.keyboard.get_keyboard_input()
        if mouse_action.get(pg.MOUSEBUTTONDOWN):
            if self.hud.selected_tile is not None:
                sprite_name = self.hud.selected_tile["name"]
                if (sprite_name =="save_game"):
                    print("save_game")
                    path = easygui.fileopenbox()
                    file = open(path, 'wb')
                    self.saveWordt(path)
                


    def update(self, camera):
        if self.time.time_multiple():
            if self.data:
                i = random.randint(0, len(self.data) - 1)
                x = self.data[i]["x"]
                y = self.data[i]["y"]
                tile_name = self.worldModel.get_case(x, y)
                if tile_name.get_tile() == 'hud_house_sprite':
                    if random.randint(0, 100) < 50:
                        tile_name.set_tile("fire")



        self.FileRegister()
        self.FileSelector()
        self.changeTime()
        self.time.update(self.speed)

        self.update_walkers()
        mouse_pos = pg.mouse.get_pos()
        mouse_action = self.keyboard.get_keyboard_input()
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
        if self.hud.selected_tile is not None and (0 <= grid_pos[0] <= self.grid_length_x - 1) and (
                0 <= grid_pos[1] <= self.grid_length_y - 1):
            sprite_name = self.hud.selected_tile["name"]

            for temps_case in self.temp_cases:
                self.worldModel.get_case(temps_case["x"], temps_case["y"]).set_tile(temps_case["image"])

            if mouse_action.get(pg.MOUSEBUTTONDOWN):
                if not self.selected_on:
                    if sprite_name == "hud_road_sprite" and not self.worldModel.get_case(grid_pos[0], grid_pos[1]).get_collision():
                        self.selection_roads = Road(grid_pos, self.worldModel)
                        self.selected_on = True
                    elif sprite_name == "hud_house_sprite" and not self.worldModel.get_case(grid_pos[0], grid_pos[1]).get_collision():
                        self.selection_building = SelectionBuilding(grid_pos, self.worldModel)
                        self.selected_on = True
                    elif sprite_name == "hud_shovel_sprite":
                        self.selection_shovel = SelectionBuilding(grid_pos, self.worldModel)
                        self.selected_on = True

            elif not mouse_action.get(pg.MOUSEBUTTONDOWN):
                if self.selected_on:
                    self.selected_on = False
                    if sprite_name == "hud_road_sprite":
                        cases = self.selection_roads.add_grid_pos(grid_pos)
                        self.selection_roads.set_image_roads()
                        self.change_cases_collision(True,cases)
                    else:
                        if sprite_name == "hud_shovel_sprite":
                            case_to_delete = self.selection_shovel.add_grid_pos_to_erase(grid_pos)
                            self.worldModel.diff_update_road(case_to_delete)
                            self.worldModel.diff_update_building(case_to_delete)
                            self.change_case_sprite_by_image_name(sprite_name, case_to_delete)
                            self.update_case(sprite_name)
                            self.change_cases_collision(False,case_to_delete)
                        elif sprite_name == "hud_house_sprite":
                            cases = self.selection_building.add_grid_pos(grid_pos)
                            self.change_case_sprite_by_image_name(sprite_name, cases)
                            self.change_cases_collision(True, cases)
                            self.update_case(sprite_name)

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
                        self.add_temp_case(temps_coord)
                        self.change_case_sprite_by_image_name("sign", temps_coord)
                        self.worldModel.diff_update_building(temps_coord)

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
            if (rect.collidepoint(pg.mouse.get_pos())):
                mouse_on_panel = False
               
        if not mouse_on_panel:
            return True
        else:
            return False

    def change_case_sprite_by_image_name(self, image_name, list_cases):
        cases = [self.worldModel.get_case(x, y) for x, y in list_cases]
        for case in cases:
            if self.can_place_tile(pg.mouse.get_pos()):
                if image_name != "hud_shovel_sprite":
                    case.set_tile(image_name)
                    if image_name=='hud_house_sprite':
                        temp = {
                            "image": case.get_tile(),
                            "x": case.get_grid()[0],
                            "y": case.get_grid()[1]
                        }
                        self.data.append(temp)
                        self.ressources.sub_dinars(10)
                        print(self.data)

                elif image_name == "hud_shovel_sprite":
                    case.set_tile(image_name)

    def update_case(self, sprite_name):
        """
        Met à jour les cases pour leurs ajouter/supprimer un building :param sprite_name: le nom du sprite
        selectionner pour savoir s'il faut supprimer ou ajouter un building aux cases :return: None
        """
        cases = [self.worldModel.get_case(x, y) for x, y in self.worldModel.get_list_grid_pos_building()]
        for case in cases:
            self.update_building(case)
            if sprite_name == "hud_house_sprite":
                if not case.get_collision():
                    house = House()
                    case.set_building(house)
            elif sprite_name == "hud_shovel_sprite":
                case.set_building(None)

    def update_building(self, case):
        """
        Update les buildings
        :param case: demande la case sur laquel est le building
        :return: None
        """
        if case.get_building():
            case.get_building().add_damage(5)

    def change_cases_collision(self, collision, coord_cases):
        cases = [self.worldModel.get_case(x, y) for x, y in coord_cases]
        for case in cases:
            case.set_collision(collision)
    def get_world_model(self):
        return self.worldModel

    def saveWord(self):
        with open("worldSave", "wb") as f1:
            pickle.dump(self.worldModel, f1)
        f1.close()

    def saveWordt(self,path):
        with open(path, "wb") as f1:
            pickle.dump(self.worldModel, f1)
        f1.close()