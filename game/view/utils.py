<<<<<<< HEAD

=======
>>>>>>> 115adc2 (creation de HUD)
import pygame as pg


def draw_text(screen, text, size, colour, pos):

    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)

<<<<<<< HEAD
    screen.blit(text_surface, text_rect)
=======
    screen.blit(text_surface, text_rect)
>>>>>>> 115adc2 (creation de HUD)
