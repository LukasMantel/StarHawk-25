import pygame

pygame.mixer.init()
SND_SHOOT = pygame.mixer.Sound('sounds/alienshoot1.ogg')
SND_ENEMY_HIT = pygame.mixer.Sound('sounds/qubodup-BangShort.ogg')
GAME_MUSIC = 'sounds/Battle in the Stars.ogg'

def play_game_music(volume=0.1, loops=-1):
    pygame.mixer.music.load(GAME_MUSIC)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loops)
