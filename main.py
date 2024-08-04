import pygame as pg
import game.game_loop as game_loop
from game.world import world
from game.render.camera import Camera
from game.entities.player import Player

screen: pg.Surface

if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1400, 800))

    player = Player((5, 5))
    world.add_entity(player)
    camera = Camera(screen, (0, 0))

    game_loop.loop(player, screen, camera)
