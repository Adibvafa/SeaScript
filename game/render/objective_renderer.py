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

    from game.objective.objective import ObjectiveInteract
    if isinstance(current_objective, ObjectiveInteract):
        ent = current_objective.entity
        if not ent.interacted_with:
            distance = ((ent.pos[0] - camera.pos[0]) ** 2 + (ent.pos[1] - camera.pos[1]) ** 2) ** 0.5
            if distance < 6 ** 2:
                txt = f'Press "E" to interact with {ent.type().name.lower()}'.replace('_', ' ')
                text = font.render(txt, True, (255, 255, 255))
                ent_screen = camera.to_screen(ent.pos)
                text_pos = (ent_screen[0] - text.get_width() / 2, ent_screen[1] - ent.size[1] * camera.scale - text.get_height() + 150)
                screen.blit(text, text_pos)

    goal_pos = camera.to_screen(goal)
    if 0 <= goal_pos[0] <= screen.get_width() and 0 <= goal_pos[1] <= screen.get_height():
        return

    goal_pos_clamped = (max(0, min(screen.get_width() - 20, goal_pos[0])),
                        max(0, min(screen.get_height() - 20, goal_pos[1])))

    pg.draw.circle(screen, (255, 0, 0), goal_pos_clamped, 10)
