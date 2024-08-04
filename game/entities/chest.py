from game.entities.entity import Entity
from game.entities.entity_types import EntityType
from game.render import textures
import pygame as pg


class Chest(Entity):
    opened: bool = False

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (4, 4))

    def type(self) -> EntityType:
        return EntityType.CHEST

    def texture(self) -> pg.Surface:
        if self.opened:
            return textures.find_texture("chest_opened")
        return textures.find_texture("chest_closed")
