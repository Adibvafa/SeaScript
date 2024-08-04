from enum import Enum, auto

import pygame as pg

from game.render import textures
from game.render.camera import Camera
from game.render.drawable import Drawable


class WorldObjectType(Enum):
    SEAWEED = (1, (1.5, 3.0))
    SEAWEED_FLIPPED = (2, (1.5, 3.0))
    CORAL = (3, (2.0, 3.0))
    CORAL_FLIPPED = (4, (2.0, 3.0))
    ROCK = (5, (1.0, 1.0))
    ROCK_FLIPPED = (6, (1.0, 1.0))
    CRAB = (7, (1.0, 1.0))
    STARFISH1 = (8, (1.0, 1.0))
    STARFISH2 = (9, (1.0, 1.0))

    def __init__(self, idx: int, size: tuple[float, float]):
        self.size = size


class WorldObject(Drawable):
    object_type: WorldObjectType
    pos: tuple[float, float]

    def __init__(self, object_type: WorldObjectType, pos: tuple[float, float]):
        self.object_type = object_type
        self.pos = pos

    def draw(self, screen: pg.Surface, camera: Camera):
        texture = textures.find_texture(f"object_{self.object_type.name.lower()}")
        # resize image to scale
        size = camera.scale_pos(self.object_type.size)
        texture = pg.transform.scale(texture, size)
        # draw image
        pos = (self.pos[0] - self.object_type.size[0] / 2, self.pos[1] - self.object_type.size[1] / 2)
        screen.blit(texture, camera.to_screen(pos))