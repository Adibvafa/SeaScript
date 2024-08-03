from camera import Camera
import pygame as pg

from game.drawable import Drawable


class Player(Camera, Drawable):

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos)

    def move(self, dx: float, dy: float):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

