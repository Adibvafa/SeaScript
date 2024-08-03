import pygame as pg
from camera import Camera
from game.drawable import Drawable


class Entity(Drawable):
    pos: tuple[float, float]

    def __init__(self, pos: tuple[float, float]):
        self.pos = pos

    def type(self) -> str:
        pass

    def draw(self, screen: pg.Surface, camera: Camera):
        pass
