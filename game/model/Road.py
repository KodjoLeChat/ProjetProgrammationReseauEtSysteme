from game.model.settings import *


class Road:
    def __init__(self, start, world):
        self.type = ROAD_TYPE
        self.start = start
        self.world = world

    def add_grid_pos(self, grid_pos):
        """
        ajoute par chemin de manathan, toutes les coordonnées des routes
        :param grid_pos: position actuelle de la sourie convertie en coordonnée de la map
        :return: None
        """
        temp_list = set()
        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:  # en haut a gauche
            for x in range(grid_pos[0], self.start[0] + 1):
                self.world.add_list_grid_pos_road((x, self.start[1]))
                temp_list.add((x, self.start[1]))
            for y in range(grid_pos[1], self.start[1] + 1):
                self.world.add_list_grid_pos_road((grid_pos[0], y))
                temp_list.add((grid_pos[0], y))

        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:  # en haut a droite
            for x in range(grid_pos[0], self.start[0] + 1):
                self.world.add_list_grid_pos_road((x, grid_pos[1]))
                temp_list.add((x, grid_pos[1]))
            for y in range(self.start[1], grid_pos[1] + 1):
                self.world.add_list_grid_pos_road((self.start[0], y))
                temp_list.add((self.start[0], y))

        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:  # en bas a gauche
            for x in range(self.start[0], grid_pos[0] + 1):
                self.world.add_list_grid_pos_road((x, grid_pos[1]))
                temp_list.add((x, grid_pos[1]))
            for y in range(grid_pos[1], self.start[1] + 1):
                self.world.add_list_grid_pos_road((self.start[0], y))
                temp_list.add((self.start[0], y))

        elif grid_pos[0] >= self.start[0] and grid_pos[1] >= self.start[1]:  # en en bas a droite
            for x in range(self.start[0], grid_pos[0] + 1):
                self.world.add_list_grid_pos_road((x, self.start[1]))
                temp_list.add((x, self.start[1]))
            for y in range(self.start[1], grid_pos[1] + 1):
                self.world.add_list_grid_pos_road((grid_pos[0], y))
                temp_list.add((grid_pos[0], y))
        return temp_list

    def get_image_key(self, coord):
        """
        l'idée esst d'obtenir en temps réel les listes des voisins de chaque coordonnées
        afin de savoir si la route devra se transformer en un virage/interserction/carrefour ect
        :return: la clée correspondante (un string)
        """
        x, y = coord
        type = {
            "top": False,
            "right": False,
            "bottom": False,
            "left": False
        }
        if (x + 1, y) in self.world.get_list_grid_pos_road():
            type["bottom"] = True
        if (x - 1, y) in self.world.get_list_grid_pos_road():
            type["top"] = True
        if (x, y + 1) in self.world.get_list_grid_pos_road():
            type["left"] = True
        if (x, y - 1) in self.world.get_list_grid_pos_road():
            type["right"] = True
        # ligne top bottom
        if type["top"] and type["bottom"] and not type["right"] and not type["left"]:
            return "top_bottom"
        # ligne left right
        if type["right"] and type["left"] and not type["top"] and not type["bottom"]:
            return "right_left"
        # turn_right_to_bottom
        if type["right"] and type["bottom"] and not type["top"] and not type["left"]:
            return "turn_right_to_bottom"
        # turn_bottom_to_left
        if type["bottom"] and type["left"] and not type["top"] and not type["right"]:
            return "turn_bottom_to_left"
        # turn_left_to_top
        if type["left"] and type["top"] and not type["bottom"] and not type["right"]:
            return "turn_left_to_top"
        # turn_top_to_right
        if type["top"] and type["right"] and not type["bottom"] and not type["left"]:
            return "turn_top_to_right"
        # crossroad_left_bottom_right
        if type["left"] and type["bottom"] and type["right"] and not type["top"]:
            return "crossroad_left_bottom_right"
        # crossroad_top_bottom_left
        if type["top"] and type["bottom"] and type["left"] and not type["right"]:
            return "crossroad_top_bottom_left"
        # crossroad_top_right_left
        if type["top"] and type["right"] and type["left"] and not type["bottom"]:
            return "crossroad_top_right_left"
        # crossroad_top_right_bottom
        if type["top"] and type["right"] and type["bottom"] and not type["left"]:
            return "crossroad_top_right_bottom"
        # cross
        if type["top"] and type["right"] and type["bottom"] and type["left"]:
            return "cross"

        # top_end
        if type["top"] and not type["right"] and not type["bottom"] and not type["left"]:
            return "top_end"
        # bottom_end
        if not type["top"] and not type["right"] and type["bottom"] and not type["left"]:
            return "bottom_end"
        # right_end
        if not type["top"] and not type["right"] and not type["bottom"] and type["left"]:
            return "left_end"
        # left_end
        else:
            return "right_end"

    def set_image_roads(self):
        """
        changes les sprites des cases avec une route en fonction de leurs voisin direct (virage/intersection/ligne/ect...)
        :return:
        """
        for coord in self.world.get_list_grid_pos_road():
            sprite_name = self.get_image_key(coord)
            self.world.set_case_image_by_coord(coord, sprite_name)
