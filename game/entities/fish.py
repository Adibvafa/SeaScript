import pygame as pg
from game.entities.entity import Entity
import random as rand

from game.entities.entity_types import EntityType
from game.render import textures


class Fish(Entity):
    ticks_till_move: int = 50 + rand.randint(0, 50)

    def __init__(self, pos: tuple[float, float], texture_type: int):
        super().__init__(pos, (2, 1.5))
        self.texture_type = texture_type

    def type(self) -> EntityType:
        return EntityType.FISH

    def tick(self):
        self.ticks_till_move -= 1
        if self.ticks_till_move == 0:
            self.ticks_till_move = 50 + rand.randint(0, 50)
            if rand.random() < 0.3:
                self.velocity = (self.velocity[0] + 0.1, self.velocity[1])
            elif 0.3 < rand.random() < 0.6:
                self.velocity = (self.velocity[0] - 0.1, self.velocity[1])
            else:
                delta = (0.0, 0.05) if rand.random() < 0.5 else (0., -0.05)
                self.velocity = (self.velocity[0] + delta[0], self.velocity[1] + delta[1])
        super().tick()

    def texture(self) -> pg.Surface:
        texture = textures.find_texture(f"fish{self.texture_type}")
        if self.velocity[0] < 0:
            texture = pg.transform.flip(texture, True, False)
        return texture
