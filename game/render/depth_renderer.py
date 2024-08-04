import pygame as pg

from game.render.camera import Camera


def render(screen: pg.Surface, camera: Camera):
    depth = camera.pos[1] / 200.0 * 10_000
