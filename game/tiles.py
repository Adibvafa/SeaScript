from enum import Enum


class Tile(Enum):
    EMPTY = ()
    SAND = ()
    BORDER = ()

    def __init__(self, solid: bool = False):
        self.solid = solid
