from game import textures
from game.entity import Entity
from game.tiles import Tile
import pygame as pg

map_width = 100
map_height = 50

entities: list[Entity] = []
tiles: list[list[Tile]] = [[Tile.EMPTY for _ in range(map_height)] for _ in range(map_width)]  # map_width x map_height


def add_entity(entity: Entity):
    entities.append(entity)


def remove_entity(entity: Entity):
    entities.remove(entity)


def draw_entities(screen, camera):
    for entity in entities:
        entity.draw(screen, camera)


def draw_tile(screen, camera, x: int, y: int):
    if x < 0 or y < 0 or x >= map_width or y >= map_height:
        return
    tile = tiles[x][y]
    texture = textures.find_texture(f"tile_{tile.name.lower()}")
    texture = pg.transform.scale(texture, (camera.scale + 2, camera.scale + 2))
    screen.blit(texture, camera.to_screen((x, y)))


def draw_tiles(screen: pg.Surface, camera):
    camera_width_tiles = int(screen.get_size()[0] // camera.scale) + 2
    camera_height_tiles = int(screen.get_size()[1] // camera.scale) + 2
    top_left = camera.to_world((0, 0))
    print(camera_height_tiles * camera_width_tiles)
    for x in range(camera_width_tiles):
        for y in range(camera_height_tiles):
            draw_tile(screen, camera, int(top_left[0]) + x - 1, int(top_left[1]) + y - 1)
