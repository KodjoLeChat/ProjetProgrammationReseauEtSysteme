# permet d'implémenter la mécanique d'un zoom
class Zoom:

    def __init__(self):
        self.init_level_zoom = 70 # le niveau de zoom initiale 
        self.level_zoom = self.init_level_zoom
        self.multiplier = self.level_zoom/100
        self.should_scale = False

    def update(self, diff):
        # ne peux pas zoomer jusqu'à un certain point
        if (self.level_zoom >= 20 and self.level_zoom <= 150 and diff > 0) or (self.level_zoom >= 20 and self.level_zoom <= 150 and diff < 0): 
            self.level_zoom += diff
            self.multiplier = self.level_zoom/100
            self.should_scale = True
            if self.level_zoom < 20: self.level_zoom = 20
            elif self.level_zoom > 150: self.level_zoom = 150 