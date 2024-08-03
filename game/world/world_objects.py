from enum import Enum, auto


class WorldObjectType(Enum):
    BOTTLE = (0.25, 1.0)
    SEAWEED = (1.0, 1.0)
    CORAL = (1.0, 1.0)
    ROCK = (1.0, 1.0)

    def __init__(self, size: tuple[float, float]):
        self.size = size


class WorldObject:
    object_type: WorldObjectType
    pos: tuple[float, float]

    def __init__(self, object_type: WorldObjectType, pos: tuple[float, float]):
        self.object_type = object_type
        self.pos = pos