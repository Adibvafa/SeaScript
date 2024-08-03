
import pygame as pg


class Camera:
    pos: tuple[float, float]
    scale: float = 40.0
    screen: pg.Surface

    def __init__(self, screen: pg.Surface, pos: tuple[float, float]):
        self.pos = pos
        self.screen = screen

    def move(self, dx: float, dy: float):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)

    def to_screen(self, pos: tuple[float, float]) -> tuple[int, int]:
        return (int((pos[0] - self.pos[0]) * self.scale) + self.screen.get_width() // 2,
                int((pos[1] - self.pos[1]) * self.scale) + self.screen.get_height() // 2)

    def to_world(self, screen_pos: tuple[int, int]) -> tuple[float, float]:
        return ((screen_pos[0] - self.screen.get_width() // 2) / self.scale + self.pos[0],
                (screen_pos[1] - self.screen.get_height() // 2) / self.scale + self.pos[1])

    def scale_pos(self, pos: tuple[float, float]) -> tuple[int, int]:
        return int(pos[0] * self.scale), int(pos[1] * self.scale)
