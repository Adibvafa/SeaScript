import pygame as pg

def loop():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Draw game state
        pg.display.flip()
