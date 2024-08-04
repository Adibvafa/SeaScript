from game.entities.entity_types import EntityType
from game.entities.fish import Fish
from game.entities.jellyfish import JellyFish
from game.entities.shark import Shark
from game.entities.angler import Angler
from game.entities.spawn_point import SpawnPoint
from game.entities.entity import Entity
from game.world.particle.particle import Particle
from game.world.tiles import Tile
from game.entities.entity import colliding_tiles
import random as rand

from game.world.world_objects import WorldObject, WorldObjectType

map_width = 250
map_height = 200

entities: list[Entity] = []
world_objects: list[WorldObject] = []
tiles: list[list[Tile]] = [[Tile.EMPTY for _ in range(map_height)] for _ in range(map_width)]
spawns: list[SpawnPoint] = []
particles: list[Particle] = []


def add_entity(entity: Entity):
    entities.append(entity)


def remove_entity(entity: Entity):
    entities.remove(entity)


def tick_entities():
    for entity in entities:
        entity.tick()


def tick_particles():
    remove = []
    for particle in particles:
        particle.tick()
        if particle.should_remove:
            remove.append(particle)
    for particle in remove:
        particles.remove(particle)


def spawn_random_fish():
    fish_types_by_sector = [[2, 5, 6, 1, 3, 4], [1, 3, 4]]
    jellyfish_types = [[1, 2]]

    num_fish = 400
    num_jellyfish = 175
    num_sharks = 20
    num_anglers = 10

    for _ in range(num_fish):
        pos = (rand.randint(0, map_width - 1), rand.randint(0, map_height - 1))
        sector = int(0 if pos[1] < 0 else pos[1] / 60.0)
        if sector >= len(fish_types_by_sector):
            continue

        fish_type = rand.choice(fish_types_by_sector[sector])
        fish = Fish((float(pos[0]), float(pos[1])), fish_type)

        tile_list = colliding_tiles(fish.hitbox(), tiles)

        # If any are solid, don't spawn
        if any([tiles[x][y].is_solid() for x, y in tile_list]):
            continue

        add_entity(fish)

    for _ in range(num_jellyfish):
        pos = (rand.randint(0, map_width - 1), rand.randint(0, map_height - 1))
        sector = int(0 if pos[1] < 0 else pos[1] / 60.0)
        if sector >= len(jellyfish_types):
            continue
        jellyfish_type = rand.choice(jellyfish_types[sector])
        jellyfish = JellyFish((float(pos[0]), float(pos[1])), jellyfish_type)

        tile_list = colliding_tiles(jellyfish.hitbox(), tiles)

        # If any are solid, don't spawn
        if any([tiles[x][y].is_solid() for x, y in tile_list]):
            continue

        add_entity(jellyfish)

    for _ in range(num_sharks):
        pos = (rand.randint(0, map_width - 1), rand.randint(90, 120))
        shark = Shark((float(pos[0]), float(pos[1])))
        tile_list = colliding_tiles(shark.hitbox(), tiles)

        if any([tiles[x][y].is_solid() for x, y in tile_list]):
            continue

        add_entity(shark)

    for _ in range(num_anglers):
        pos = (rand.randint(180, map_width - 1), rand.randint(160, 180))
        angler = Angler((float(pos[0]), float(pos[1])))
        tile_list = colliding_tiles(angler.hitbox(), tiles)

        if any([tiles[x][y].is_solid() for x, y in tile_list]):
            continue

        add_entity(angler)


def save_map(file: str):
    with open(file, "w") as f:
        f.write(f"{map_width} {map_height}\n")
        for x in range(map_width):
            for y in range(map_height):
                f.write(f"{tiles[x][y].name} ")
            f.write("\n")

        f.write(f"{len(world_objects)}\n")
        for world_object in world_objects:
            f.write(f"{world_object.object_type.name} {world_object.pos[0]} {world_object.pos[1]}\n")

        f.write(f"{len(spawns)}\n")
        for spawn in spawns:
            f.write(f"{spawn.entity_type.name} {spawn.pos[0]} {spawn.pos[1]}\n")


def load_map(file: str):
    global map_width, map_height, tiles, world_objects
    with open(file, "r") as f:
        map_width, map_height = map(int, f.readline().split())
        tiles = [[Tile.EMPTY for _ in range(map_height)] for _ in range(map_width)]
        for x in range(map_width):
            tile_names = f.readline().split()
            for y, tile_name in enumerate(tile_names):
                tiles[x][y] = Tile[tile_name]

        world_objects = []
        num_objects = int(f.readline())
        for _ in range(num_objects):
            object_type, x, y = f.readline().split()
            world_objects.append(WorldObject(WorldObjectType[object_type], (float(x), float(y))))

        potential_fish_spawn_num = f.readline()
        if len(potential_fish_spawn_num) == 0:
            return

        num_spawns = int(potential_fish_spawn_num)
        for _ in range(num_spawns):
            entity_type, x, y = f.readline().split()
            spawns.append(SpawnPoint(EntityType[entity_type], (float(x), float(y))))
