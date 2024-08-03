import pygame as pg

from game.entities.entity import Entity
import random as rand

from game.render import textures


class JellyFish(Entity):
    ticks_till_move: int = 50

    def __init__(self, pos: tuple[float, float], texture_type: int):
        super().__init__(pos, (1.0, 1.0))
        self.texture_type = texture_type

    def type(self) -> str:
        return "jellyfish"

    def tick(self):
        self.ticks_till_move -= 1
        if self.ticks_till_move == 0:
            self.ticks_till_move = 50
            self.velocity = (0.0, 0.1) if rand.random() < 0.5 else (0.0, -0.1)
        super().tick()

    def texture(self) -> pg.Surface:
        return textures.find_texture(f"jellyfish{self.texture_type}")
