from game.render import textures
from game.entities.entity import Entity
from game.world.tiles import Tile
import pygame as pg

map_width = 100
map_height = 50

entities: list[Entity] = []
tiles: list[list[Tile]] = [[Tile.THICK_SAND for _ in range(map_height)] for _ in range(map_width)]


def add_entity(entity: Entity):
    entities.append(entity)


def remove_entity(entity: Entity):
    entities.remove(entity)


def tick_entities():
    for entity in entities:
        entity.tick()


def draw_entities(screen, camera):
    for entity in entities:
        entity.draw(screen, camera)


def draw_tiles(screen: pg.Surface, camera):
    camera_width_tiles = int(screen.get_size()[0] // camera.scale) + 2
    camera_height_tiles = int(screen.get_size()[1] // camera.scale) + 2
    top_left = camera.to_world((0, 0))
    print(camera_height_tiles * camera_width_tiles)
    for x in range(camera_width_tiles):
        for y in range(camera_height_tiles):
            real_x = int(top_left[0]) + x
            real_y = int(top_left[1]) + y
            if real_x < 0 or real_y < 0 or real_x >= map_width or real_y >= map_height:
                continue
            tile = tiles[real_x][real_y]
            tile.draw(screen, camera, real_x, real_y)
