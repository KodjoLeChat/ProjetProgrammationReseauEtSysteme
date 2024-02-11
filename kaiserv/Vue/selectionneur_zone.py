import pygame
from .basic_action import Basic_Action

# permet de gérer la selection d'une zone, classe mère pour les actions de clear et de adding_building
class SelectionneurZone(Basic_Action):
    OPACITY = 180
    
    def __init__(self, carriere):
        Basic_Action.__init__(self, carriere)
        self.grid_postition_to_place = None
        self.grid_to_draw = [] # les emplacements selectionnés

    def ignore(self):
        try:
            print("" + str(self.original_surface.get_size()))
            size_of_original_image = self.original_surface.get_size()
        except AttributeError as e:
            #print(f"Bringing building in progress: {e}")
            size_of_original_image,self.original_surface = [116, 60]
        '''
        #self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        self.grid_to_draw = []
        # on affiche pour chaque emplacement sélectionné, la zone choisis
        if self.pos_start is not None:
            for i in range(self.coordinate[0][0], self.coordinate[1][0]+1):
                for j in range(self.coordinate[0][1], self.coordinate[1][1]+1):
                    self.grid_postition_to_place = grid = (round(i), round(j))
                    self.grid_to_draw.append(grid)
        else:
            # sinon on affiche que pour la case survolé
            self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click)

            self.grid_to_draw.append(self.grid_position_without_first_click)
        for grid in self.grid_to_draw:
            if self.path != "assets/upscale_house/Housng1a_00045.png" or self.carriere.controleur.check_if_construction_possible_on_grid(grid):
                self.draw_for_an_image(grid)'''

    def draw(self):
        try:
            count = 0
            print("" + str(self.original_surface.get_size()))
            size_of_original_image = self.original_surface.get_size()
        except AttributeError as e:
            #print(f"AttributeError: {e}")
            size_of_original_image,self.original_surface = [116, 60]
            count = 2

        #self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        self.grid_to_draw = []
        # on affiche pour chaque emplacement sélectionné, la zone choisis
        if count!=2:
            if self.pos_start is not None:
                for i in range(self.coordinate[0][0], self.coordinate[1][0]+1):
                    for j in range(self.coordinate[0][1], self.coordinate[1][1]+1):
                        self.grid_postition_to_place = grid = (round(i), round(j))
                        self.grid_to_draw.append(grid)
            else:
                # sinon on affiche que pour la case survolé
                self.grid_position_without_first_click = self.mouse_to_grid(self.carriere.current_surface, self.carriere.camera.scroll, self.carriere.controleur.TILE_SIZE*self.carriere.zoom.multiplier, self.pos_without_first_click)

                self.grid_to_draw.append(self.grid_position_without_first_click)
            for grid in self.grid_to_draw:
                if self.path != "assets/upscale_house/Housng1a_00045.png" or self.carriere.controleur.check_if_construction_possible_on_grid(grid):
                    self.draw_for_an_image(grid)

'''import pygame
from .basic_action import Basic_Action

# permet de gérer la selection d'une zone, classe mère pour les actions de clear et de adding_building
class SelectionneurZone(Basic_Action):
    OPACITY = 180
    
    def __init__(self, carriere):
        Basic_Action.__init__(self, carriere)
        self.grid_postition_to_place = None
        self.grid_to_draw = [] # les emplacements selectionnés

    def draw(self, test, test2):
        count = 0
        try:
            # Attempt to get the size of the original surface
            size_of_original_image = self.original_surface.get_size()
            # Check if size_of_original_image is a tuple right after obtaining it
            if not isinstance(size_of_original_image, tuple):
                raise TypeError("size_of_original_image is not a tuple.")
        except (AttributeError, TypeError) as e:
            # This catches both the AttributeError from the try block and the TypeError from the check
            print(f"Error encountered: {e}")
            # Fall back to using test if self.original_surface.get_size() fails or is not a tuple
            if isinstance(test, tuple):
                print("Using test as size_of_original_image due to error.")
                size_of_original_image = test
                pos_start = test2
                count = 1
        self.image_to_draw = pygame.transform.scale(self.original_surface, (size_of_original_image[0]*self.carriere.zoom.multiplier, size_of_original_image[1]*self.carriere.zoom.multiplier))
        self.grid_to_draw = []

        if count == 0:
            # Standard behavior using self.pos_start
            print("Standard behavior")
            if self.pos_start is not None:
                print("test2")
                for i in range(self.coordinate[0][0], self.coordinate[1][0]+1):
                    for j in range(self.coordinate[0][1], self.coordinate[1][1]+1):
                        self.grid_postition_to_place = grid = (round(i), round(j))
                        self.grid_to_draw.append(grid)
            else:
                # Handle the case without a first click
                self.grid_position_without_first_click = self.mouse_to_grid(
                    self.carriere.current_surface, self.carriere.camera.scroll,
                    self.carriere.controleur.TILE_SIZE * self.carriere.zoom.multiplier, self.pos_without_first_click)
                self.grid_to_draw.append(self.grid_position_without_first_click)
        else:
            # Use pos_start from test2 because getting size of original_surface failed
            print("Fallback behavior due to failure in getting size")
            # Assuming pos_start from test2 affects how you calculate the grid to draw
            # Replace or adjust the following logic based on how pos_start should be used
            if pos_start is not None:
                print("Using pos_start from test2")
                # Example: replicate the logic from above or implement adjusted logic based on pos_start

        for grid in self.grid_to_draw:
            if self.path != "assets/upscale_house/Housng1a_00045.png" or self.carriere.controleur.check_if_construction_possible_on_grid(grid):
                self.draw_for_an_image(grid)
'''