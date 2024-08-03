import pygame as pg
from game.render.camera import Camera
from game.render.drawable import Drawable
import game.render.textures as textures


class Entity(Drawable):
    pos: tuple[float, float]
    size: tuple[float, float]
    velocity: tuple[float, float] = (0, 0)

    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.pos = pos
        self.size = size

    def type(self) -> str:
        pass

    def texture(self) -> pg.Surface:
        return textures.find_texture(self.type())

    def draw(self, screen: pg.Surface, camera: Camera):
        texture = self.texture()
        # resize image to scale
        size = camera.scale_pos(self.size)
        texture = pg.transform.scale(texture, size)
        # draw image
        pos = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        screen.blit(texture, camera.to_screen(pos))

    def move(self, dx: float, dy: float):
        vec

    def tick(self):
        new_pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        if new_pos[1] < 0:
            new_pos = (new_pos[0], 0)
        if new_pos != self.pos:
            self.pos = new_pos

        # Velocity decay
        self.velocity = (self.velocity[0] * 0.95, self.velocity[1] * 0.95)
        if abs(self.velocity[0]) < 0.01:
            self.velocity = (0, self.velocity[1])
        if abs(self.velocity[1]) < 0.01:
            self.velocity = (self.velocity[0], 0)
