from game.render import textures
from game.render.camera import Camera
from game.render.drawable import Drawable
import pygame as pg


class Particle(Drawable):

    def __init__(self, size: tuple[float, float], pos: tuple[float, float], vel: tuple[float, float] = (0, 0), lifetime: int = 50) -> None:
        self.size = size
        self.pos = pos
        self.vel = vel
        self.lifetime = lifetime
        self.should_remove = False

    def tick(self):
        if self.should_remove:
            return
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.should_remove = True

    def texture(self) -> pg.Surface:
        pass

    def draw(self, screen: pg.Surface, camera: Camera):
        texture = self.texture()
        # resize image to scale
        size = camera.scale_pos(self.size)
        texture = pg.transform.scale(texture, size)
        # draw image
        pos = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        screen.blit(texture, camera.to_screen(pos))

class BubbleParticle(Particle):

    tick_num: int = 0

    def __init__(self, pos: tuple[float, float], vel: tuple[float, float] = (0, 0)) -> None:
        super().__init__((0.25, 0.25), pos, vel, 100)

    def texture(self) -> pg.Surface:
        texture = textures.find_texture("particle_bubble")
        if (self.tick_num / 25) % 2 == 0:
            texture = pg.transform.rotate(texture, 90)
        return texture

    def tick(self):
        super().tick()
        self.tick_num += 1
