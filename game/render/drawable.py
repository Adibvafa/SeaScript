import pygame as pg
from game.render.camera import Camera


class Drawable:
    def draw(self, screen: pg.Surface, camera: Camera):
        pass
