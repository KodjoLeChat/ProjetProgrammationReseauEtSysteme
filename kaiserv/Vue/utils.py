import pygame as pg

# permet d'afficher du texte à l'écran
def draw_text(screen, text, size, colour, pos):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)
    screen.blit(text_surface, text_rect)