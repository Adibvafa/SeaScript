import pygame as pg

from game.entities.jelly_fish import JellyFish
from game.world import world
from game.render import gradient
from game.render.camera import Camera
from game.entities.player import Player

keyboard_state = {
    pg.K_w: False,
    pg.K_s: False,
    pg.K_a: False,
    pg.K_d: False
}


def process_input(player: Player, camera: Camera):
    speed = 0.1
    if keyboard_state[pg.K_w]:
        player.move(0, -speed)
        camera.move(0, -speed)
    if keyboard_state[pg.K_s]:
        player.move(0, speed)
        camera.move(0, speed)
    if keyboard_state[pg.K_a]:
        player.move(-speed, 0)
        camera.move(-speed, 0)
        player.last_move_right = False
    if keyboard_state[pg.K_d]:
        player.move(speed, 0)
        camera.move(speed, 0)
        player.last_move_right = True


def loop(player: Player, screen: pg.Surface, camera: Camera):
    running = True

    jelly_fish = JellyFish((2.0, 2.0), 1)
    world.add_entity(jelly_fish)

    # Create a clock object
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key in keyboard_state:
                    keyboard_state[event.key] = True
            elif event.type == pg.KEYUP:
                if event.key in keyboard_state:
                    keyboard_state[event.key] = False

        process_input(player, camera)

        # Draw game state
        depth = player.pos[1]
        normalized_depth = depth / 100.0
        top_colour = (52, 168, 235)
        bottom_colour = (13, 40, 56)

        gradient.draw_vertical_gradient(screen, top_colour, bottom_colour)
        world.tick_entities()
        world.draw_tiles(screen, camera)
        world.draw_entities(screen, camera)

        pg.display.flip()

        # Control the frame rate
        clock.tick(50)  # 100 frames per second (every 10ms)

    pg.quit()
