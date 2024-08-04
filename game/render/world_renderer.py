from game.render.camera import Camera
from game.world.tiles import Tile
import game.world.world as world
import pygame as pg


def render(screen, camera):
    draw_tiles(screen, camera)
    draw_world_objects(screen, camera)
    draw_entities(screen, camera)
    draw_particles(screen, camera)


def draw_entities(screen, camera):
    for entity in world.entities:
        entity.draw(screen, camera)


def draw_world_objects(screen, camera):
    for world_object in world.world_objects:
        dist = (world_object.pos[0] - camera.pos[0]) ** 2 + (world_object.pos[1] - camera.pos[1]) ** 2
        if dist < (screen.get_size()[0] / camera.scale) ** 2 * 2:
            world_object.draw(screen, camera)


def draw_tiles(screen: pg.Surface, camera):
    camera_width_tiles = int(screen.get_size()[0] // camera.scale) + 2
    camera_height_tiles = int(screen.get_size()[1] // camera.scale) + 2
    top_left = camera.to_world((0, 0))
    for x in range(camera_width_tiles):
        for y in range(camera_height_tiles):
            real_x = int(top_left[0]) + x
            real_y = int(top_left[1]) + y
            if real_x < 0 or real_y < 0 or real_x >= world.map_width or real_y >= world.map_height:
                continue
            tile = world.tiles[real_x][real_y]
            if tile == Tile.EMPTY:
                continue
            tile.draw(screen, camera, real_x, real_y)


def draw_particles(screen: pg.Surface, camera: Camera):
    for particle in world.particles:
        particle.draw(screen, camera)
