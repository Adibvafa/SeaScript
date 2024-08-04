from game.entities.entity_types import EntityType


class SpawnPoint:
    def __init__(self, entity_type: EntityType, pos: tuple[float, float]):
        self.pos = pos
        self.entity_type = entity_type