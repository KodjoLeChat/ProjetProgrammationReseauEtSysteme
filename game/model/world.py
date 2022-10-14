import pygame as pg
import random
from game.controller.SelectionRect import SelectionRect

import pygame.event

from game.model.case import Case
from game.model.settings import TILE_SIZE


class World:

    def __init__(self, hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.selected_on = False
        self.selection = None

        self.grass_tiles = pg.Surface(
            (grid_length_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()  #
        self.images = self.load_images()
        self.world = self.create_world()

        self.temp_tile = None

    def update(self, camera, screen):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        self.temp_tile = None

        if mouse_action[0]:
            if not self.selected_on:
                self.selected_on = True
                self.selection = SelectionRect(screen, mouse_pos)
        elif mouse_action[2]:
            if self.selected_on:
                rect = self.selection.updateRect(mouse_pos)

        elif mouse_action[1]:
            if self.selected_on:
                self.selected_on = False
                rect = self.selection.updateRect(mouse_pos)
        if self.hud.selected_tile is not None:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if self.can_place_tile(grid_pos):

                if mouse_action[0]:
                    for event in pg.event.get():
                        if event.type == pg.MOUSEMOTION:
                            new_mouse_pos = pg.mouse.get_pos()
                            selection_rect = self.draw_selection(mouse_pos, new_mouse_pos, screen)

                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                case = self.world[grid_pos[0]][grid_pos[1]]
                render_pos = case.get_case_rect().topleft
                iso_poly = case.get_iso_poly()
                collision = case.get_collision()

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision:
                    case.set_tile("farm")
                    case.set_collision(True)
                    self.hud.selected_tile = None

    def draw(self, screen, camera):
        camera_scroll_x = camera.get_scroll().x
        camera_scroll_y = camera.get_scroll().y
        screen.blit(self.grass_tiles, (camera_scroll_x, camera_scroll_y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                case = self.world[x][y]
                render_pos = case.get_case_rect().topleft
                tile = case.get_tile()
                if tile != "":
                    screen.blit(self.images[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera_scroll_x,
                                 render_pos[1] - (self.images[tile].get_height() - TILE_SIZE) + camera_scroll_y))

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera_scroll_x, y + camera_scroll_y) for x, y in
                        iso_poly]

            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pg.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera_scroll_x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera_scroll_y
                )
            )

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
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

                render_pos = world_tile.get_case_rect().topleft
                self.grass_tiles.blit(self.images["block"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

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

        case_rect = pg.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        case_rect.topleft = iso_poly[0]
        case_rect.topleft = iso_poly[1]
        case_rect.topleft = iso_poly[2]
        case_rect.topleft = iso_poly[3]
        collision = False if tile == "" else True

        out = Case([grid_x, grid_y], iso_poly, tile, case_rect, collision)

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def load_images(self):

        block = pg.image.load("C3_sprites/C3/Land1a_00002.png").convert_alpha()
        tree1 = pg.image.load("C3_sprites/C3/Land1a_00045.png").convert_alpha()
        tree2 = pg.image.load("C3_sprites/C3/Land1a_00054.png").convert_alpha()
        tree3 = pg.image.load("C3_sprites/C3/Land1a_00059.png").convert_alpha()
        farm = pg.image.load("C3_sprites/C3/Security_00053.png").convert_alpha()
        building1 = pg.image.load("C3_sprites/C3/paneling_00123.png").convert_alpha()
        building2 = pg.image.load("C3_sprites/C3/paneling_00131.png").convert_alpha()
        tree = pg.image.load("C3_sprites/C3/paneling_00135.png").convert_alpha()

        images = {
            "building1": building1,
            "building2": building2,
            "tree1": tree1,
            "tree2": tree2,
            "tree3": tree3,
            "farm": farm,
            "tree": tree,
            "block": block
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

    def draw_selection(self, top_left, bottom_right, screen):
        selection_rect = pg.Rect(top_left, (bottom_right[0], bottom_right[1]))
        pg.draw.rect(screen, (255, 255, 255), selection_rect)
        return selection_rect
