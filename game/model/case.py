class Case:
    def __init__(self, grid,rect, iso_poly, tile, render_pos,collision):
        self.grid = grid
        self.rect = rect
        self.iso_poly = iso_poly
        self.tile = tile
        self.entites = []
        self.render_pos = render_pos
        self.collision = collision
        self.building = None

    def get_grid(self):
        return self.grid

    def get_rect(self):
        return self.rect

    def get_tile(self):
        return self.tile

    def get_entities(self):
        return self.entites

    def get_render_pos(self):
        return self.render_pos

    def get_collision(self):
        return self.collision
    def get_iso_poly(self):
        return self.iso_poly

    def get_building(self):
        return self.building

    def set_collision(self,value):
        self.collision = value

    def set_tile(self, tile):
        self.tile = tile

    def set_building(self,building):
        self.building = building