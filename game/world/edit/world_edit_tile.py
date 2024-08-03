from game.entities.player import Player
from game.render.camera import Camera
from game.world.tiles import Tile

selected_tile: Tile | None = None


def cycle_tile():
    global selected_tile
    members = list(Tile)
    if selected_tile is None:
        selected_tile = members[1]
    elif selected_tile == members[-1]:
        selected_tile = None
    else:
        selected_tile = members[members.index(selected_tile) + 1]


def draw(player: Player, camera: Camera):
    from game.world import world
    if selected_tile is not None:
        camera.draw_tile(selected_tile, player.pos)
