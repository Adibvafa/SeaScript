from game.render import gradient


def clamp_colour(colour: tuple[int, int, int]) -> tuple[int, int, int]:
    return (max(0, min(255, colour[0])),
            max(0, min(255, colour[1])),
            max(0, min(255, colour[2])))


def render(screen, camera, world):
    top_colour = (32, 98, 155)
    bottom_colour = (5, 15, 40)
    diff = (bottom_colour[0] - top_colour[0], bottom_colour[1] - top_colour[1], bottom_colour[2] - top_colour[2])
    camera_top = camera.to_world((0, 0))[1] / world.map_height
    camera_bottom = camera.to_world((0, screen.get_height()))[1] / world.map_height
    screen_top_colour = (top_colour[0] + diff[0] * camera_top, top_colour[1] + diff[1] * camera_top,
                         top_colour[2] + diff[2] * camera_top)
    screen_bottom_colour = (top_colour[0] + diff[0] * camera_bottom, top_colour[1] + diff[1] * camera_bottom,
                            top_colour[2] + diff[2] * camera_bottom)

    gradient.draw_vertical_gradient(screen, clamp_colour(screen_top_colour), clamp_colour(screen_bottom_colour))
