from game.render.camera import Camera
from game.world import world
from game.world.world_objects import WorldObjectType, WorldObject
import pygame as pg

selected_wo: None | WorldObjectType = None
placed_wo: list[WorldObject] = []

def cycle_wo():
    global selected_wo
    members = list(WorldObjectType)
    if selected_wo is None:
        selected_wo = members[0]
    elif selected_wo == members[-1]:
        selected_wo = None
    else:
        selected_wo = members[members.index(selected_wo) + 1]


def draw(screen: pg.Surface, camera: Camera):
    global selected_wo
    if selected_wo is not None:
        mouse_world_pos = camera.to_world(pg.mouse.get_pos())
        obj = WorldObject(selected_wo, (mouse_world_pos[0], mouse_world_pos[1]))
        obj.draw(screen, camera)


def place_wo(camera: Camera, map_width: int, map_height: int):
    global selected_wo
    if selected_wo is not None:
        mouse_world_pos = camera.to_world(pg.mouse.get_pos())
        x = mouse_world_pos[0]
        y = mouse_world_pos[1]
        if 0 <= x < map_width and 0 <= y < map_height:
            world_object = WorldObject(selected_wo, mouse_world_pos)
            world.world_objects.append(world_object)
            placed_wo.append(world_object)


def undo():
    if len(placed_wo) > 0:
        world.world_objects.remove(placed_wo.pop())


def erase(camera: Camera):
    mouse_world_pos = camera.to_world(pg.mouse.get_pos())
    closest = None
    closest_dist = float("inf")
    for wo in world.world_objects:
        dist = (wo.pos[0] - mouse_world_pos[0]) ** 2 + (wo.pos[1] - mouse_world_pos[1]) ** 2
        if dist < closest_dist:
            closest = wo
            closest_dist = dist
    if closest is not None:
        world.world_objects.remove(closest)
        placed_wo.remove(closest)
