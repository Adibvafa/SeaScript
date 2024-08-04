from game.entities.entity import Entity
from game.entities.entity_types import EntityType
from game.math.vectors import Box2d, Vec2d
from game.objective.objective import ChallengeEntity
from game.render import textures
import pygame as pg
import random as rand

from game.world import world
from game.world.particle.particle import SparkleParticle


class Chest(ChallengeEntity):
    opened: bool = False

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (4, 4), 3)

    def type(self) -> EntityType:
        return EntityType.CHEST

    def texture(self) -> pg.Surface:
        if self.opened:
            return textures.find_texture("chest_opened")
        return textures.find_texture("chest_closed")

    def tick(self):
        if rand.random() > 0.1:
            return

        left_corner = (self.pos[0] - self.size[0] / 2 - 0.5, self.pos[1] - self.size[1] / 2 - 0.5)
        box_size = (self.size[0] + 0.5, self.size[1] + 0.5)
        particle_pos = Box2d(Vec2d(left_corner[0], left_corner[1]), Vec2d(box_size[0], box_size[1])).random_point()
        world.particles.append(SparkleParticle((particle_pos.x, particle_pos.y), (0, 0.0)))

        from game.qa import qa
        if 3 in qa.completed_challenges:
            self.opened = True
