import pygame as pg

from game.render.camera import Camera


def render(screen: pg.Surface, camera: Camera):
    coordinates = camera.to_world(pg.mouse.get_pos())
    font = pg.font.Font(None, 36)
    text = font.render(f"Mouse: {int(coordinates[0])}, {int(coordinates[1])}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
