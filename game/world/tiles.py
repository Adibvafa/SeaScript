from enum import Enum

from game.render import textures
import pygame as pg


class Tile(Enum):
    EMPTY = ('', False)
    SAND = ('', True)
    THICK_SAND = ('', True)
    BORDER = ('', True)

    def __init__(self, a: str, solid: bool = False):
        self.solid = solid

    def draw(self, screen, camera, x: int, y: int):
        texture = textures.find_texture(f"tile_{self.name.lower()}")
        print(f'Drawing {self.name} at {x}, {y}')
        texture = pg.transform.scale(texture, (camera.scale + 2, camera.scale + 2))
        screen.blit(texture, camera.to_screen((x, y)))
