from game.entities.player import Player
from game.render.camera import Camera
from game.world import world
from game.world.tiles import Tile
import pygame as pg

selected_tile: Tile | None = None


history: list[list[list[Tile]]] = []


def cycle_tile():
    global selected_tile
    members = list(Tile)
    if selected_tile is None:
        selected_tile = members[0]
    elif selected_tile == members[-1]:
        selected_tile = None
    else:
        selected_tile = members[members.index(selected_tile) + 1]


def draw(screen: pg.Surface, camera: Camera):
    global selected_tile
    if selected_tile is not None:
        mouse_world_pos = camera.to_world(pg.mouse.get_pos())
        selected_tile.draw(screen, camera, int(mouse_world_pos[0]), int(mouse_world_pos[1]))


def place_tile(camera: Camera, map_width: int, map_height: int):
    global selected_tile
    if selected_tile is not None:
        mouse_world_pos = camera.to_world(pg.mouse.get_pos())
        x = int(mouse_world_pos[0])
        y = int(mouse_world_pos[1])
        if 0 <= x < map_width and 0 <= y < map_height:
            world.tiles[x][y] = selected_tile


def fill_tile(camera: Camera, map_width: int, map_height: int):
    global selected_tile
    if selected_tile is None:
        return

    mouse_world_pos = camera.to_world(pg.mouse.get_pos())
    real_x = int(mouse_world_pos[0])
    real_y = int(mouse_world_pos[1])

    queue = [(real_x, real_y)]

    def fill_next():
        (x, y) = queue.pop()
        if 0 <= x < map_width and 0 <= y < map_height:
            curr_tile = world.tiles[x][y]
            if curr_tile != Tile.EMPTY:
                return
            world.tiles[x][y] = selected_tile
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    history.append([row.copy() for row in world.tiles])

    while len(queue) > 0:
        fill_next()


def undo():
    if history:
        world.tiles = history.pop()
