import pygame as pg

from game.render import gradient_renderer
from game.render.camera import Camera
from game.render.gradient import draw_vertical_gradient


def render(screen: pg.Surface, camera: Camera):
    depth = camera.pos[1] / 200.0 * 6000
    depth_proportion = depth / 6000
    surface = pg.Surface((20, 100))
    surface.fill((0, 0, 0), (0, 0, 20, 100))
    draw_vertical_gradient(surface, (32, 98, 155), (5, 15, 100))
    height = depth_proportion * 100
    pg.draw.line(surface, (255, 255, 255), (0, height), (20, height), width=3)
    pg.draw.rect(surface, (0, 0, 0), (0, 0, 20, 100), 3)
    screen.blit(surface, (screen.get_size()[0] - 60, 50))
    txt = f'{int(depth):,}m'
    font = pg.font.Font(None, 36)
    text = font.render(txt, True, (255, 255, 255))
    screen.blit(text, (screen.get_size()[0] - 50 - text.get_size()[0] / 2, 20))


