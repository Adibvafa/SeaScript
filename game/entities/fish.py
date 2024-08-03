import pygame as pg
from game.entities.entity import Entity
import random as rand
from game.render import textures


class Fish(Entity):
    ticks_till_move: int = 50 + rand.randint(0, 50)

    def __init__(self, pos: tuple[float, float], texture_type: int):
        super().__init__(pos, (1.5, 1.5))
        self.texture_type = texture_type

    def type(self) -> str:
        return "fish"

    def tick(self):
        self.ticks_till_move -= 1
        if self.ticks_till_move == 0:
            self.ticks_till_move = 50 + rand.randint(0, 50)
            if rand.random() < 0.3:
                self.velocity = (0.1, 0.0)
            elif 0.3 < rand.random() < 0.6:
                self.velocity = (-0.1, 0.0)
            else:
                self.velocity = (0.0, 0.05) if rand.random() < 0.5 else (0., -0.05)
        super().tick()

    def texture(self) -> pg.Surface:
        return textures.find_texture(f"fish{self.texture_type}")
