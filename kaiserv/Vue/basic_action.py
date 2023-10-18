import pygame
import math

# classe mère de toute action en cours, ces actions sont liées aux intéractions faites avec le HUD
class Basic_Action:
    OPACITY = 180

    def __init__(self, carriere):
        self.is_progress = False # est-ce que l'action est en cours
        self.carriere = carriere 
        self.path = None         # le chemin de l'image à affiché quand l'action est finit

    def initialiser(self, surface):
        self.is_possible = True # est-ce que l'on peux pratiquer l'action
        self.is_progress = True # mise en place de l'action
        self.pos_without_first_click = (0,0) # position de la souris avant le premier appuie
        self.pos_start = None # position de la souris d'origine après un appuie
        self.grid_position_start = None # position start dans la grille relative à la souris
        self.grid_position_end = None   # position end   dans la grille relative à la souris
        self.coordinate = None 
        self.grid_position_without_first_click = None # position dans la grille relative à la souris sans le premier click
        self.original_surface = surface # surface à draw de base
        self.original_surface.set_alpha(Basic_Action.OPACITY) # mise en légère transparence de l'image 
        self.image_to_draw = self.original_surface
    
    # permet de calculer la distance entre deux points
    def calcul_distance_to_grid(self, grid_start, grid_stop):
        return int(math.sqrt((grid_stop[0]-grid_start[0])**2 + (grid_stop[1]-grid_start[1])**2))

    # recupere et traite les evenements à la souris 
    def events(self, event):
        if self.is_progress:
            self.pos_without_first_click = pygame.mouse.get_pos()
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click)
            self.grid_position_without_first_click = (round(self.grid_position_without_first_click[0]), round(self.grid_position_without_first_click[1]))

            # à l'appuie l'action commence
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pos_start = self.pos_without_first_click
                if self.grid_position_start == None:
                    self.grid_position_start = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_start)
            if self.pos_start != None :
                self.grid_position_end = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click )
                self.coordinate = self.get_square_coords_from_top_right(self.grid_position_start, self.grid_position_end)

    # permet de recuperer avec 2 points la coordonnée en haut à droite imaginées par un carré formé par deux point
    # c'est en effet le point d'origine pour draw une image
    def get_square_coords_from_top_right(self, grid_start, grid_end):
        positions = [grid_start, grid_end]
        minim = (min([x for x, y in positions]), min([y for x, y in positions]))
        maxim = (max([x for x, y in positions]), max([y for x, y in positions]))

        return minim, maxim
        
    # convertit la position de souris en position dans le jeu
    def mouse_to_grid(self, surface, scroll, TILE_SIZE, pos):
        world_x = pos[0] - scroll.x - surface.get_width()/2
        world_y = pos[1] - scroll.y
        contrary_iso_y = (2*world_y-world_x)/2 
        contrary_iso_x = contrary_iso_y + world_x

        grid_x = int(contrary_iso_x//TILE_SIZE)
        grid_y = int(contrary_iso_y//TILE_SIZE)

        return grid_x, grid_y

    # draw l'image courante
    def draw_for_an_image(self, grid):
        if grid[0] >= 0 and grid[1] >= 0 and len(self.carriere.informations_tiles) > grid[0] and len(self.carriere.informations_tiles[grid[0]]) > grid[1]:
            position = self.carriere.informations_tiles[grid[0]][grid[1]]["position_rendu"]
            position = (
                ((position[0]*self.carriere.zoom.multiplier + self.carriere.current_surface.get_width()/2 + self.carriere.camera.scroll.x)),
                ((position[1]*self.carriere.zoom.multiplier - (self.image_to_draw.get_height() - self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier )+ self.carriere.camera.scroll.y))
            )

            self.carriere.controleur.screen.blit(self.image_to_draw, position)