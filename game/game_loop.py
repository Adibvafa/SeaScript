import pygame as pg

from game.entities.chest import Chest
from game.entities.QueenJelly import QueenJelly
import game.objective.objective as objective
from game.entities.KingShark import KingShark
from game.objective.objective import init_objectives
from game.qa import qa
from game.world import world
from game.render import world_renderer, gradient_renderer, coord_renderer, depth_renderer
from game.render.camera import Camera
from game.entities.player import Player
from game.world.edit import world_edit_tile, world_edit_wo
from game.music.music import initialize_music, stop_music, set_volume  # Import the new music functions

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
    if player.freeze_movement:
        return
    speed = 0.25
    if keyboard_state[pg.K_w]:
        player.move(0, -speed)
    if keyboard_state[pg.K_s]:
        player.move(0, speed)
    if keyboard_state[pg.K_a]:
        player.move(-speed, 0)
        player.last_move_right = False
    if keyboard_state[pg.K_d]:
        player.move(speed, 0)
        player.last_move_right = True
    camera.pos = player.pos


def loop(player: Player, screen: pg.Surface, camera: Camera):
    running = True

    qa.init_qa()
    # qa.window.hide()

    objective.init_objectives()

    # Initialize music
    initialize_music()
    set_volume(0.5)  # Set initial volume to 50%

    chest = Chest((239.0, 182.0))
    world.add_entity(chest)

    # Create a clock object
    clock = pg.time.Clock()

    # Check if map file map.txt exists
    try:
        world.load_map("map.txt")
    except FileNotFoundError:
        print("Map file not found")

    # add fish
    world.spawn_random_fish()

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
                    world_edit_wo.cycle_wo()
                if event.key == pg.K_u:
                    world.save_map("map.txt")
                if event.key == pg.K_f:
                    world_edit_tile.fill_tile(camera, world.map_width, world.map_height)
                if event.key == pg.K_z:
                    world_edit_wo.undo()
                # Add volume control
                if event.key == pg.K_UP:
                    set_volume(min(pg.mixer.music.get_volume() + 0.1, 1.0))
                if event.key == pg.K_DOWN:
                    set_volume(max(pg.mixer.music.get_volume() - 0.1, 0.0))
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button in click_state:
                    click_state[event.button] = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button in click_state:
                    click_state[event.button] = False
                world_edit_wo.place_wo(camera, world.map_width, world.map_height)

        process_input(player, camera)

        world.tick_entities()
        world.tick_particles()

        objective.check_objectives()

        gradient_renderer.render(screen, camera)
        world_renderer.render(screen, camera)
        world_edit_wo.draw(screen, camera)
        coord_renderer.render(screen, camera)
        depth_renderer.render(screen, camera)

        # Render border
        border_top_left = camera.to_screen((0, 0))
        rect = pg.Rect(border_top_left[0], border_top_left[1], camera.scale * world.map_width, camera.scale *
                       world.map_height)
        pg.draw.rect(screen, (255, 255, 255), rect, 2)

        pg.display.flip()

        # Control the frame rate
        clock.tick(50)  # 50 frames per second

    # Stop the music when the game ends
    stop_music()
    pg.quit()
