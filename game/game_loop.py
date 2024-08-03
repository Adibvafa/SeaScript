import pygame as pg

from game import world, main
from game.camera import Camera


def loop(screen: pg.Surface, camera: Camera):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Draw game state
        world.draw_entities(screen, camera)

        pg.display.flip()
