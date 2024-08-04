import pygame as pg
from game.entities.entity import Entity
import random as rand

from game.entities.entity_types import EntityType
from game.render import textures


class Shark(Entity):
    ticks_till_move: int = 200 + rand.randint(0, 50)

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (5, 3))
        self.velocity_decay = 0.999

    def type(self) -> EntityType:
        return EntityType.SHARK

    def tick(self):
        self.ticks_till_move -= 1
        if self.ticks_till_move == 0:
            self.ticks_till_move = 200 + rand.randint(0, 50)
            if rand.random() < 0.4:
                self.velocity = (0.15, 0.0)
            elif 0.4 < rand.random() < 0.8:
                self.velocity = (-0.15, 0.0)
            else:
                self.velocity = (0.0, 0.02) if rand.random() < 0.5 else (0., -0.02)
        super().tick()

    def texture(self) -> pg.Surface:
        texture = textures.find_texture("shark")
        if self.velocity[0] < 0:
            texture = pg.transform.flip(texture, True, False)
        return texture
