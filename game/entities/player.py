import pygame as pg

from game.entities.entity_types import EntityType
from game.math.vectors import Vec2d
from game.render import textures
from game.entities.entity import Entity
import random as rand

from game.world import world
from game.world.particle.particle import BubbleParticle


class Player(Entity):

    last_move_right: bool = True

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
        particle_pos = self.hitbox().random_point()
        world.particles.append(BubbleParticle((particle_pos.x, particle_pos.y), (0, -0.1)))



