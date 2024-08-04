import pygame as pg
import math as math
from game.entities.entity_types import EntityType
from game.objective.objective import ChallengeEntity
from game.render import textures


class QueenJelly(ChallengeEntity):
    original_pos: tuple[float, float]
    tick_num: int = 0

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (5.0, 7.5))
        self.original_pos = pos

    def type(self) -> EntityType:
        return EntityType.QUEEN_JELLYFISH

    def tick(self):
        super().tick()
        self.tick_num += 1
        self.pos = (self.pos[0], self.original_pos[1] + math.sin(self.tick_num * math.pi / 60) * 1.5)

    def texture(self) -> pg.Surface:
        return textures.find_texture("queen_jelly")
