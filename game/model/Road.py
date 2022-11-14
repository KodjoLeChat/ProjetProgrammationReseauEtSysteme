from settings import *
import pygame


class Road:
    def __init__(self, start):
        self.type = ROAD_TYPE
        self.images = self.load_images()
        self.hover = pygame.image.load("C3_sprites/C3/Land2a_00044.png")
        self.start = start
        self.list_grid_pos = {self.start}

    def load_images(self):
        """
        Load les images en fonction du type de route définie dans les variables globales
        :return: un dictionnaire d'image contenant les routes dans toutes les directions ainsi que les intersections et virage
        """
        images = {
            "top_bottom": pygame.image.load("C3_sprites/C3/Land2a_00094.png"),
            "top_end": pygame.image.load("C3_sprites/C3/Land2a_00102.png"),
            "bottom_end": pygame.image.load("C3_sprites/C3/Land2a_00104.png"),
            "right_left": pygame.image.load("C3_sprites/C3/Land2a_00093.png"),
            "right_end": pygame.image.load("C3_sprites/C3/Land2a_00101.png"),
            "left_end": pygame.image.load("C3_sprites/C3/Land2a_00101.png"),
            "turn_right_to_bottom": pygame.image.load("C3_sprites/C3/Land2a_00097.png"),
            "turn_bottom_to_left": pygame.image.load("C3_sprites/C3/Land2a_00098.png"),
            "turn_left_to_top": pygame.image.load("C3_sprites/C3/Land2a_00099.png"),
            "turn_top_to_right": pygame.image.load("C3_sprites/C3/Land2a_00100.png"),
            "crossroad_left_bottom_right": pygame.image.load("C3_sprites/C3/Land2a_00106.png"),
            "crossroad_top_bottom_left": pygame.image.load("C3_sprites/C3/Land2a_00107.png"),
            "crossroad_top_right_left": pygame.image.load("C3_sprites/C3/Land2a_00108.png"),
            "crossroad_top_right_bottom": pygame.image.load("C3_sprites/C3/Land2a_00109.png"),
            "cross": pygame.image.load("C3_sprites/C3/Land2a_00110.png")
        }
        return images

    def add_grid_pos(self, grid_pos):
        if grid_pos[0] <= self.start[0] and grid_pos[1] <= self.start[1]:  # en haut a gauche
            for x in range(grid_pos[0], self.start[0] + 1):
                self.list_grid_pos.add((x, self.start[1]))
            for y in range(grid_pos[1], self.start[1] + 1):
                self.list_grid_pos.add((grid_pos[0], y))

        elif grid_pos[0] <= self.start[0] and grid_pos[1] >= self.start[1]:  # en haut a droite
            for x in range(grid_pos[0], self.start[0] + 1):
                self.grid_pos.add((x, grid_pos[1]))
            for y in range(self.start[1], grid_pos[1] + 1):
                self.list_grid_pos.add((self.start[0], y))

        elif grid_pos[0] >= self.start[0] and grid_pos[1] <= self.start[1]:  # en bas a gauche
            for x in range(self.start[0], grid_pos[0] + 1):
                self.list_grid_pos.add((x, grid_pos[1]))
            for y in range(grid_pos[1], self.start[1] + 1):
                self.list_grid_pos.add((self.start[0],y))

        elif grid_pos[0] >= self.start[0] and grid_pos[1] >= self.start[1]:  # en en bas a droite
            for x in range(self.start[0], grid_pos[0] + 1):
                self.list_grid_pos.add((x,self.start[1]))
            for y in range(self.start[1], grid_pos[1] + 1):
                self.list_grid_pos.add((grid_pos[0],y))


    def get_voisin(self,coord):
        """
        l'idée esst d'obtenir en temps réel les listes des voisins de chaque coordonnées
        afin de savoir si la route devra se transformer en un virage/interserction/carrefour
        :return: sachant que cette partie de prend que en compte les coordonnes des routes
        la valeur de retour sera un dictionnaire pour chaque type de route (virage/intersection/ligne/carrefour) comme clef
        et comme valeur les coordonnées des routes.
        """
        dico = {
            "top_bottom",
            "right_left",
            "turn_right_to_bottom",
            "turn_bottom_to_left",
            "turn_left_to_top",
            "turn_top_to_right",
            "crossroad_left_bottom_right",
            "crossroad_top_bottom_left",
            "crossroad_top_right_left",
            "crossroad_top_right_bottom",
            "cross"
        }
        x, y = coord
        type = {
            "top":0,
            "right":0,
            "bottom":0,
            "left":0
        }
        if (x+1,y) in self.list_grid_pos:
            type["bottom"] = 1
        if (x-1,y) in self.list_grid_pos:
            type["top"] = 1
        if (x,y+1) in self.list_grid_pos:
            type["right"] = 1
        if (x,y-1) in self.list_grid_pos:
            type["left"] = 1
        #ligne top bottom
        if type["top"] and type["bottom"]:
