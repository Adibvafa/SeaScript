import pygame as pg
import math as math
from game.entities.entity import Entity
from game.entities.entity_types import EntityType
from game.objective.objective import ChallengeEntity
from game.render import textures
from game.render.camera import Camera


class BlankChallengeEntity(ChallengeEntity):

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (5.0, 7.5), 2)
        self.original_pos = pos

    def type(self) -> EntityType:
        return EntityType.CORAL_REEF

    def tick(self):
        super().tick()

    def texture(self) -> pg.Surface:
        pass

    def draw(self, screen: pg.Surface, camera: Camera):
        pass
