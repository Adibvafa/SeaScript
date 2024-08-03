import pygame as pg
from camera import Camera
from game.drawable import Drawable
import textures


class Entity(Drawable):
    pos: tuple[float, float]
    size: tuple[float, float]

    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.pos = pos
        self.size = size

    def type(self) -> str:
        pass

    def draw(self, screen: pg.Surface, camera: Camera):
        texture = textures.find_texture(self.type())
        # resize image to scale
        size = camera.scale_pos(self.size)
        texture = pg.transform.scale(texture, size)
        # draw image
        pos = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        screen.blit(texture, camera.to_screen(pos))
