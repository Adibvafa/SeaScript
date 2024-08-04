from game.entities.entity_types import EntityType
import pygame as pg

from game.render.camera import Camera

selected_entity: None | EntityType = None


def cycle():
    global selected_entity
    members = list(EntityType)
    if selected_entity is None:
        selected_entity = members[0]
    elif selected_entity == members[-1]:
        selected_entity = None
    else:
        selected_entity = members[members.index(selected_entity) + 1]


def draw(screen: pg.Surface, camera: Camera):
    global selected_entity
    if selected_entity is not None:
        mouse_world_pos = camera.to_world(pg.mouse.get_pos())
        obj = EntityType(selected_entity, (mouse_world_pos[0], mouse_world_pos[1]))
        obj.draw(screen, camera)