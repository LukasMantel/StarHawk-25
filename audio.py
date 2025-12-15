import pygame

pygame.init()
pygame.mixer.init()
#Quelle Game_music: https://opengameart.org/content/space-shooter-music
#MUSIC BY OBLIDIVM http://oblidivmmusic.blogspot.com.es/
SND_VICTORY = pygame.mixer.Sound("sounds/VictoryTune.ogg")
#Quelle Game_music: https://opengameart.org/content/space-shooter-music
#MUSIC BY OBLIDIVM http://oblidivmmusic.blogspot.com.es/
SND_DEFEAT = pygame.mixer.Sound("sounds/Defeated.ogg")
#https://opengameart.org/content/space-shoot-sounds
#Music by Robin Lamb
SND_SHOOT = pygame.mixer.Sound("sounds/alienshoot1.ogg")
#https://opengameart.org/users/qubodup?page=34
#Music by qubodup
SND_ENEMY_HIT = pygame.mixer.Sound("sounds/qubodup-BangShort.ogg")
#Quelle Game_music: https://opengameart.org/content/space-shooter-music
#MUSIC BY OBLIDIVM http://oblidivmmusic.blogspot.com.es/
GAME_MUSIC = "sounds/Battle in the Stars.ogg"

def play_game_music(volume=0.1, loops=-1):
    pygame.mixer.music.load(GAME_MUSIC)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loops)

def stop_game_music():
    pygame.mixer.music.stop()




