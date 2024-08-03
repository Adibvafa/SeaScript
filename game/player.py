from camera import Camera
import pygame as pg

from game.entity import Entity


class Player(Entity):

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (1, 1))

    def move(self, dx: float, dy: float):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def type(self) -> str:
        return "player"

