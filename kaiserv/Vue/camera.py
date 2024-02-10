
import pygame

# permet d'aller sur les côtes de la carte
class Camera:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        ratio_x, ratio_y = self.width/1920, self.height/1080

        self.scroll = pygame.Vector2(-550/ratio_x, -200/ratio_y)
        self.dx = 0
        self.dy = 0
        self.speed = 25

    # met à jour la caméra 
    def update(self):
        # récupère la position de la souris sur notre écran en pixel 
        mouse_pos = pygame.mouse.get_pos()

        """
        On considère que nous nous déplaçons sur un coté si nous sommes à moins de 3% par rapport à la bordure
        Chaque axe est traité séparément car nous pouvons avoir le cas particulier des déplacements diagonaux
        """

        # x movement
        if mouse_pos[0] > self.width * 0.99  : self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.01: self.dx = self.speed
        else                                 : self.dx = 0

        # y movement
        if mouse_pos[1] > self.height * 0.99  : self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.01: self.dy = self.speed
        else                                  : self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy
