import pygame as pg

from game.entities.entity_types import EntityType
from game.math.vectors import Vec2d, Box2d
from game.render import textures
from game.entities.entity import Entity
import random as rand

from game.world import world
from game.world.particle.particle import BubbleParticle


class Player(Entity):

    last_move_right: bool = True
    freeze_movement: bool = False

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (5, 5))

    def type(self) -> EntityType:
        return EntityType.PLAYER

    def texture(self) -> pg.Surface:
        return textures.find_texture("player_right" if self.last_move_right else "player_left")

    def tick(self):
        super().tick()
        if rand.random() > 0.1:
            return

        left_corner = (self.pos[0] - self.size[0] / 3, self.pos[1] - self.size[1] / 3)
        box_size = (self.size[0] / 3 * 2, self.size[1] / 3 * 2)
        particle_pos = Box2d(Vec2d(left_corner[0], left_corner[1]), Vec2d(box_size[0], box_size[1])).random_point()
        world.particles.append(BubbleParticle((particle_pos.x, particle_pos.y), (0, -0.1)))



