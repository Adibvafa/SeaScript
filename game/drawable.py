import pygame as pg
from game.camera import Camera


class Drawable:
    def draw(self, screen: pg.Surface, camera: Camera):
        pass
