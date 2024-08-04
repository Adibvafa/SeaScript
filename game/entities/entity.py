import math

import pygame as pg

from game.entities.entity_types import EntityType
from game.math.vectors import Vec2d, Box2d
from game.render.camera import Camera
from game.render.drawable import Drawable
import game.render.textures as textures
from game.world.tiles import Tile


def colliding_tiles(hitbox: Box2d, tiles: list[list[Tile]]) -> list[tuple[int, int]]:
    min_x = int(hitbox.min.x)
    max_x = int(hitbox.max.x)
    min_y = int(hitbox.min.y)
    max_y = int(hitbox.max.y)
    colliding = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if 0 <= x < len(tiles) and 0 <= y < len(tiles[x]):
                tile = tiles[x][y]
                if not tile.is_solid():
                    continue
                colliding.append((x, y))
    return colliding


class Entity(Drawable):
    pos: tuple[float, float]
    size: tuple[float, float]
    velocity: tuple[float, float] = (0, 0)

    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        self.pos = pos
        self.size = size

    def type(self) -> EntityType:
        pass

    def texture(self) -> pg.Surface:
        return textures.find_texture(self.type().name.lower())

    def hitbox(self):
        return Box2d(Vec2d(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2), Vec2d(self.size[0],
                                                                                                  self.size[1]))

    def draw(self, screen: pg.Surface, camera: Camera):
        texture = self.texture()
        # resize image to scale
        size = camera.scale_pos(self.size)
        texture = pg.transform.scale(texture, size)
        # draw image
        pos = (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2)
        screen.blit(texture, camera.to_screen(pos))

    def move(self, dx: float, dy: float):
        if dx == 0 and dy == 0:
            return
        delta = Vec2d(dx, dy)
        pos = Vec2d(self.pos[0], self.pos[1])
        size = Vec2d(self.size[0], self.size[1])
        box = Box2d(pos - size / 2, size)
        expanded_box = Box2d(box.min - Vec2d(1, 1), size + Vec2d(2, 2))
        from game.world import world
        colliding = colliding_tiles(expanded_box, world.tiles)

        min_col_time_x = 1
        min_col_time_y = 1
        for tile in colliding:
            tile_box = Box2d(Vec2d(tile[0], tile[1]), Vec2d(1, 1))
            collides, col_time = box.collision_time(tile_box, delta)
            if not collides:
                continue
            min_col_time_x = min(min_col_time_x, col_time)
            min_col_time_y = min(min_col_time_y, col_time)

        final_dx = min_col_time_x * delta.x - (math.copysign(0.0001, delta.x) if delta.x != 0 else 0)
        final_dy = min_col_time_y * delta.y - (math.copysign(0.0001, delta.y) if delta.y != 0 else 0)

        self.pos = (self.pos[0] + final_dx, self.pos[1] + final_dy)

    def tick(self):
        self.move(self.velocity[0], self.velocity[1])

        # Velocity decay
        self.velocity = (self.velocity[0] * 0.99, self.velocity[1] * 0.99)
        if abs(self.velocity[0]) < 0.01:
            self.velocity = (0, self.velocity[1])
        if abs(self.velocity[1]) < 0.01:
            self.velocity = (self.velocity[0], 0)
