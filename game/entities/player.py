import pygame as pg

from game.render import textures
from game.entities.entity import Entity


class Player(Entity):

    last_move_right: bool = True

    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, (5, 5))

    def type(self) -> str:
        return "player"

    def texture(self) -> pg.Surface:
        return textures.find_texture("player_right" if self.last_move_right else "player_left")

