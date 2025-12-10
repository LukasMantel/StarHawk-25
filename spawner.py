import pygame
from sprites import *
from settings import *


class EnemyWave:
    def __init__(self, all_sprites, enemies, player, enemy_bullets):
        self.enemies = enemies
        self.all_sprites = all_sprites
        self.player = player
        self.enemy_bullets = enemy_bullets

        self.wave_number = 0
        self.enemies_in_wave = 5
        self.enemies_spawned = 0
        self.spawn_delay = 1000  # milliseconds between spawns
        self.last_spawn = 0
        self.wave_complete = False
    
    def start_new_wave(self):
        self.wave_number += 1
        self.enemies_spawned = 0
        self.wave_complete = False

        if self.wave_number ==BOSS_SPAWN: #ein Gegner alle 15 Welle, Boss
            self.enemies_in_wave = 1
            self.spawn_delay = 0
        else:
            self.enemies_in_wave = 5 + self.wave_number
            self.spawn_delay = max(300, 1000 - (self.wave_number * 50))  #Faster spawns as waves progress
    
    def update(self):
        now = pygame.time.get_ticks()
        if (self.enemies_spawned < self.enemies_in_wave and 
            now - self.last_spawn > self.spawn_delay):
            self.last_spawn = now
            self.spawn_enemy()
            self.enemies_spawned += 1
            if self.enemies_spawned >= self.enemies_in_wave:
                self.wave_complete = True
    
    def spawn_enemy(self):
        #Boss
        if self.wave_number==BOSS_SPAWN:
            boss = Boss(self.player, self.enemy_bullets, WIDTH // 2, 50)
            self.all_sprites.add(boss)
            self.enemies.add(boss)
            return
        #Normale Gegner
        x = random.randint(50, WIDTH-50)
        y = -40
        
        enemy = Enemy(x, y)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)
