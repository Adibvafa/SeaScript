import pygame as pg

from game.entities.fish import Fish
from game.entities.jellyfish import JellyFish
from game.world import world
from game.render import gradient
from game.render.camera import Camera
from game.entities.player import Player
from game.world.edit import world_edit_tile

keyboard_state = {
    pg.K_w: False,
    pg.K_s: False,
    pg.K_a: False,
    pg.K_d: False
}

click_state = {
    pg.BUTTON_LEFT: False,
    pg.BUTTON_RIGHT: False
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

    jellyfish1 = JellyFish((2.0, 2.0), 1)
    world.add_entity(jellyfish1)
    jellyfish2 = JellyFish((3.0, 3.0), 2)
    world.add_entity(jellyfish2)

    # add fish
    fish1 = (Fish((3.0, 3.0), 1))
    world.add_entity(fish1)
    fish2 = (Fish((4.0, 4.0), 2))
    world.add_entity(fish2)
    fish3 = (Fish((5.0, 5.0), 3))
    world.add_entity(fish3)
    fish4 = (Fish((6.0, 6.0), 4))
    world.add_entity(fish4)
    fish5 = (Fish((7.0, 7.0), 5))
    world.add_entity(fish5)
    fish6 = (Fish((8.0, 8.0), 6))
    world.add_entity(fish6)

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
                if event.key == pg.K_SPACE:
                    world_edit_tile.cycle_tile()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button in click_state:
                    click_state[event.button] = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button in click_state:
                    click_state[event.button] = False

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
        if click_state[pg.BUTTON_LEFT]:
            world_edit_tile.place_tile(camera, world.map_width, world.map_height)
        world_edit_tile.draw(screen, camera)

        pg.display.flip()

        # Control the frame rate
        clock.tick(50)  # 100 frames per second (every 10ms)

    pg.quit()
