from game.entity import Entity

map_width = 100
map_height = 50

entities: list[Entity] = []
tiles: list[list[int]] = [[0 for _ in range(map_height)] for _ in range(map_width)]  # map_width x map_height


def add_entity(entity: Entity):
    entities.append(entity)


def remove_entity(entity: Entity):
    entities.remove(entity)


def draw_entities(screen, camera):
    for entity in entities:
        entity.draw(screen, camera)
