import pygame as pg
import math as math
from game.entities.entity import Entity
from game.entities.entity_types import EntityType
from game.objective.objective import ChallengeEntity
from game.render import textures


class KingShark(ChallengeEntity):
    original_pos: tuple[float, float]
    tick_num: int = 0

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (8.0, 5.0), 1)
        self.original_pos = pos

    def type(self) -> EntityType:
        return EntityType.KING_SHARK

    def tick(self):
        super().tick()
        self.tick_num += 1
        self.pos = (self.original_pos[0] + math.sin(self.tick_num * math.pi / 60) * 1.5, self.pos[1])

    def texture(self) -> pg.Surface:
        texture = textures.find_texture("king_shark")
        if self.velocity[0] < 0:
            texture = pg.transform.flip(texture, True, False)
        return texture
