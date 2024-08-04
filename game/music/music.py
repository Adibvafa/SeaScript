import pygame as pg
import os

def initialize_music():
    pg.mixer.init()
    music_file = os.path.join('game/music', 'water.mp3')
    # Music credit: Genshin Impact
    if not os.path.exists(music_file):
        print(f"Warning: {music_file} not found. Music will not play.")
        return

    pg.mixer.music.load(music_file)
    pg.mixer.music.play(-1)  # -1 means loop indefinitely

def stop_music():
    pg.mixer.music.stop()

def set_volume(volume):
    pg.mixer.music.set_volume(volume)  # volume should be between 0.0 and 1.0