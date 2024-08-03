import pygame as pg

_textures = {}


def _load_texture(name: str) -> pg.Surface:
    if name not in _textures:
        _textures[name] = pg.image.load(f"game/textures/{name}.png")
    return _textures[name]


def find_texture(name: str) -> pg.Surface:
    return _textures[name] if name in _textures else _load_texture(name)
