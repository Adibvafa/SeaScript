from enum import Enum, auto

from game.render import textures
import pygame as pg


class Tile(Enum):
    EMPTY = auto()
    SAND = auto()
    THICK_SAND = auto()

    def draw(self, screen: pg.Surface, camera, x: int, y: int):
        if self == Tile.EMPTY:
            top_left = camera.to_screen((x, y))
            rect = pg.Rect(top_left[0], top_left[1], camera.scale, camera.scale)
            screen.fill((255, 255, 255), rect)
            return
        texture = textures.find_texture(f"tile_{self.name.lower()}")
        texture = pg.transform.scale(texture, (camera.scale + 2, camera.scale + 2))
        screen.blit(texture, camera.to_screen((x, y)))

    def is_solid(self) -> bool:
        return self != Tile.EMPTY
