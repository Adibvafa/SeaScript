import pygame as pg

from game.objective import objective
from game.render.camera import Camera


def render(screen: pg.Surface, camera: Camera):
    current_objective = objective.get_current_objective()
    if current_objective is None:
        return
    font = pg.font.Font(None, 36)
    text = font.render(current_objective.description, True, (255, 255, 255))
    surface = pg.Surface((text.get_width() + 40, text.get_height() + 20))
    surface.fill((0, 0, 0))
    surface.blit(text, (20, 10))
    screen.blit(surface, (screen.get_width() / 2 - surface.get_width() / 2, 20))

    goal = current_objective.goal()
    if goal is None:
        return

    goal_pos = camera.to_screen(goal)
