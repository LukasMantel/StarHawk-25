import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

def load_assets():
    return {
        "MET_LARGE": pygame.image.load(os.path.join(IMG_DIR, "meteor_large.png")).convert_alpha(),
        "MET_SMALL": pygame.image.load(os.path.join(IMG_DIR, "meteor_small.png")).convert_alpha(),
        "FRAGMENT": pygame.image.load(os.path.join(IMG_DIR, "star_fragment.png")).convert_alpha(),
        "JUNK": pygame.image.load(os.path.join(IMG_DIR, "space_junk.png")).convert_alpha(),
        "JUNK2": pygame.image.load(os.path.join(IMG_DIR, "space_junk2.png")).convert_alpha(),
    }


