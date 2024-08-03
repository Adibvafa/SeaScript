import pygame as pg
import game.game_loop as game_loop
from game import world
from game.camera import Camera
from game.entities.player import Player

screen: pg.Surface

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((800, 600))

    player = Player((0, 0))
    world.add_entity(player)
    camera = Camera(screen, (0, 0))

    game_loop.loop(player, screen, camera)
