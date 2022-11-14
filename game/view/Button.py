import pygame as pg
from game.view.utils import extract_image_path, create_bg, bg_block
from game.model.settings import *
class Button():
    '''
    screen : ecran à laquelle le button est lié
    background_button : image du background du button [image]
    button_position [pos]
    text [text_input]
    text_image
    delta_L : pour le déplacement selon l'axe X
    delta_H : pour le déplacement selon l'axe Y
    text_color [base_color]
    font: style d'ecriture + couleur background
    base_color : la couleur du fond du boutton
    delta :
        dx : la distance entre le debut du boutton et le premier lettre
        dy : la distance entre le haut du boutton et le premier lettre (A reformuler)
    size_bg : dimension du background du boutton
    '''
    def __init__(self, screen, image, pos, dim, delta_text, text_input, font):
        self.screen = screen
        self.image = image
        self.x_pos, self.y_pos = pos
        self.lenght, self.width = dim
        self.dx, self.dy = delta_text
        self.rect = ((self.x_pos,self.y_pos),(self.lenght,self.width))
        self.font = font
        self.text_input = text_input

    def update(self):
        # Updating backend and text
        if self.image is not None:
            self.screen.blit(self.image, (self.x_pos, self.y_pos))
            # Updating dimension of the block:
            self.lenght, self.width = self.image.get_size()
        else:
            self.diplay_fonts()


    def checkForInput(self, position):
        """ pour vérifier l'emplacement du curseur par rapport au bouton """
        if ( self.x_pos < position[0] and position[0]  <  self.x_pos +self.lenght ) and (self.y_pos< position[1] and position[1] < self.y_pos + self.width):
            return True
        return False

    def changeColor(self, position):
        if (self.rect.left < position[0] and position[0] < self.rect.right) and (self.rect.top < position[1] and position[1] < self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def diplay_fonts(self):
        # Create the background
        x, y = self.x_pos,  self.y_pos
        L, l = self.lenght, self.width

        bg_block(self.screen, pos=(x, y), dim=(L, l), color=self.font[1], rescale=True)
        #
        dx_car = self.dx
        for car in self.text_input:
            image_car = pg.image.load(extract_image_path(car, self.font[0]))
            self.screen.blit(image_car, (self.x_pos + dx_car, self.y_pos+10))
            dx_car += image_car.get_size()[0]

