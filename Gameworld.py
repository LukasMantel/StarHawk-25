import pygame
from sprites import *
from spawner import Spawner

class GameWorld:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.player = Ship((width // 2 - 25, height - 80))
        self.all_sprites.add(self.player)
        self.boss = None
        self.spawner = Spawner(self)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.input_left = keys[pygame.K_LEFT]
        self.player.input_right = keys[pygame.K_RIGHT]

    def update(self):
        self.handle_input()

        # Player separat updaten
        self.player.update()

        # Alle anderen Sprites
        for sprite in self.all_sprites:
            if sprite is not self.player:
                sprite.update()

        # Bullet-Enemy Kollisionen
        hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
        for enemy in hits:
            enemy.get_hit()
        
        # Enemy spawnen
        self.spawner.update()
        
        # Boss update
        if self.boss:
          self.boss.try_shoot_bullet(self)
          self.boss.try_laser()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
        self.player.bullets.draw(screen)
        self.enemies.draw(screen)
        if self.boss:
          self.boss.draw_laser(screen)

    def shoot(self):
        bullet = Bullet(self.player.rect.midtop)
        self.all_sprites.add(bullet)
        self.player.bullets.add(bullet)
