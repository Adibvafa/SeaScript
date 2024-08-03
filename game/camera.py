
import pygame as pg


class Camera:
    pos: tuple[float, float]
    scale: float = 20.0
    screen: pg.Surface

    def __init__(self, screen: pg.Surface, pos: tuple[float, float]):
        self.pos = pos
        self.screen = screen

    def to_screen(self, pos: tuple[float, float]) -> tuple[int, int]:
        return (int((pos[0] - self.pos[0]) * self.scale) + self.screen.get_width() // 2,
                int((pos[1] - self.pos[1]) * self.scale) + self.screen.get_height() // 2)

    def scale_pos(self, pos: tuple[float, float]) -> tuple[int, int]:
        return int(pos[0] * self.scale), int(pos[1] * self.scale)
