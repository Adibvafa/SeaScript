import pygame as pg
from game.entities.entity import Entity
from game.entities.entity_types import EntityType
from game.render import textures


class KingJellyFish(Entity):

    def __init__(self, pos: tuple[float, float], texture_type: int):
        super().__init__(pos, (4.0, 8.0))
        self.texture_type = texture_type

    def type(self) -> EntityType:
        return EntityType.KING_JELLYFISH

    def tick(self):
        super().tick()

    def texture(self) -> pg.Surface:
        return textures.find_texture(f"jellyfish{self.texture_type}")
