from game.render import textures
from game.entities.entity import Entity
from game.world.tiles import Tile
import pygame as pg

from game.world.world_objects import WorldObject, WorldObjectType

map_width = 250
map_height = 200

entities: list[Entity] = []
world_objects: list[WorldObject] = []
tiles: list[list[Tile]] = [[Tile.EMPTY for _ in range(map_height)] for _ in range(map_width)]


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


def draw_world_objects(screen, camera):
    for world_object in world_objects:
        world_object.draw(screen, camera)


def draw_tiles(screen: pg.Surface, camera):
    camera_width_tiles = int(screen.get_size()[0] // camera.scale) + 2
    camera_height_tiles = int(screen.get_size()[1] // camera.scale) + 2
    top_left = camera.to_world((0, 0))
    for x in range(camera_width_tiles):
        for y in range(camera_height_tiles):
            real_x = int(top_left[0]) + x
            real_y = int(top_left[1]) + y
            if real_x < 0 or real_y < 0 or real_x >= map_width or real_y >= map_height:
                continue
            tile = tiles[real_x][real_y]
            if tile == Tile.EMPTY:
                continue
            tile.draw(screen, camera, real_x, real_y)


def save_map(file: str):
    with open(file, "w") as f:
        f.write(f"{map_width} {map_height}\n")
        for x in range(map_width):
            for y in range(map_height):
                f.write(f"{tiles[x][y].name} ")
            f.write("\n")

        f.write(f"{len(world_objects)}\n")
        for world_object in world_objects:
            f.write(f"{world_object.object_type.name} {world_object.pos[0]} {world_object.pos[1]}\n")


def load_map(file: str):
    global map_width, map_height, tiles, world_objects
    with open(file, "r") as f:
        map_width, map_height = map(int, f.readline().split())
        tiles = [[Tile.EMPTY for _ in range(map_height)] for _ in range(map_width)]
        for x in range(map_width):
            tile_names = f.readline().split()
            for y, tile_name in enumerate(tile_names):
                tiles[x][y] = Tile[tile_name]

        world_objects = []
        num_objects = int(f.readline())
        for _ in range(num_objects):
            object_type, x, y = f.readline().split()
            world_objects.append(WorldObject(WorldObjectType[object_type], (float(x), float(y))))
