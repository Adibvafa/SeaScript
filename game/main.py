import pygame as pg
import game_loop


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))
    game_loop.loop()
