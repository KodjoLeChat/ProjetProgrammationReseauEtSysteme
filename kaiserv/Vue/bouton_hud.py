import os
import pygame

# boutons présent dans le HUD
# permet de gérer l'evenmentielle
class Button_HUD:
    def __init__(self, screen, x, y, name):
        self.position_top_left = (x,y)
        self.image_hover = None # quand on passe au dessus du bouton l'image doit changer
        self.image_click = None # quand on clik sur le bouton, l'image doit changer 
        self.who_is_visible = "" # dit si nous affichons l'image de clik, hover ou rien
        self.screen = screen
        self.name = name
        self.ratio_x = self.screen.get_width()/1536 # calculées par rapport à un écran en particulier
        self.ratio_y = self.screen.get_height()/864
        self.init_picture() # recupere les bonnes images
        self.rect = pygame.Rect( x,y, 41*self.ratio_x,28*self.ratio_y) # definit un rectangle avec lequel nous pourrons intéragir 

    # recupere les images pour les boutons des HUD
    def init_picture(self):
        image_click = f"./assets/hud/{self.name}_click.png"
        image_hover = f"./assets/hud/{self.name}_hover.png"

        if os.path.exists(image_click) and os.path.exists(image_hover):
            self.image_click = pygame.image.load(image_click).convert_alpha()
            self.image_click = pygame.transform.scale(self.image_click, (self.image_click.get_width()*self.ratio_x, self.image_click.get_height()*self.ratio_y))
            self.image_hover = pygame.image.load(image_hover).convert_alpha()
            self.image_hover = pygame.transform.scale(self.image_hover, (self.image_hover.get_width()*self.ratio_x, self.image_hover.get_height()*self.ratio_y))

    # draw l'image si hover ou click 
    def draw(self):
        if self.who_is_visible == "image_hover" and self.image_hover != None:
            self.screen.blit(self.image_hover, self.position_top_left)
        elif self.who_is_visible == "image_click" and self.image_click != None:
            self.screen.blit(self.image_click, self.position_top_left)