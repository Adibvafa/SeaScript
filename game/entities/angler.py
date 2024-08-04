import pygame as pg
from game.entities.entity import Entity
import random as rand

from game.entities.entity_types import EntityType
from game.render import textures


class Angler(Entity):
    ticks_till_move: int = 50 + rand.randint(0, 50)

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (2, 1.5))
        self.velocity_decay = 0.999

    def type(self) -> EntityType:
        return EntityType.ANGLER

    def tick(self):
        self.ticks_till_move -= 1
        if self.ticks_till_move == 0:
            self.ticks_till_move = 75 + rand.randint(0, 50)
            if rand.random() < 0.4:
                self.velocity = (0.05, 0.0)
            elif 0.4 < rand.random() < 0.8:
                self.velocity = (-0.05, 0.0)
            else:
                self.velocity = (0.0, 0.02) if rand.random() < 0.5 else (0., -0.02)
        super().tick()

    def texture(self) -> pg.Surface:
        texture = textures.find_texture("angler")
        if self.velocity[0] < 0:
            texture = pg.transform.flip(texture, True, False)
        return texture
