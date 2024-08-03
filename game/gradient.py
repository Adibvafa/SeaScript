import pygame as pg


def draw_vertical_gradient(surface, color1, color2):
    width, height = surface.get_size()
    for y in range(height):
        ratio = y / height
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio),
        )
        pg.draw.line(surface, color, (0, y), (width, y))
