import pygame as pg
from game.entities.entity import Entity
import random as rand
from game.render import textures


class Shark(Entity):
    ticks_till_move: int = 50 + rand.randint(0, 50)

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (5, 3))

    def type(self) -> str:
        return "shark"

    def tick(self):
        self.ticks_till_move -= 1
        if self.ticks_till_move == 0:
            self.ticks_till_move = 50
            self.velocity = (0.0, 0.1) if rand.random() < 0.5 else (0.0, -0.1)
        super().tick()

    def texture(self) -> pg.Surface:
        return textures.find_texture("shark")
