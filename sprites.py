import pygame
import random
from settings import *


class Ship(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("images/ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=position)
        self.vel_x = 0
        self.acc_x = 0
        self.speed = 5
        self.input_left = False
        self.input_right = False
        self.bullets = pygame.sprite.Group()

    def update(self):
        # Input in Acceleration umwandeln
        self.acc_x = 0
        if self.input_left:
            self.acc_x -= PLAYER_ACC
        if self.input_right:
            self.acc_x += PLAYER_ACC

        # Friction
        self.acc_x += self.vel_x * PLAYER_FRICTION

        # Velocity & Position updaten
        self.vel_x += self.acc_x
        self.rect.x += self.vel_x

        # Bildschirmgrenzen
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x = 0

   
    def shoot(self):
        bullet = Bullet(self.rect.midtop)
        self.bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.vel_y = -8

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((40,30))
        self.image = pygame.image.load("images/ship (13).png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=position)
        self.hp = 1
        self.vel_y = 2

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.top > HEIGHT:
            self.kill()

    def get_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.destroy()
        
    def destroy(self):
        self.kill()

class BossGuldan(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("images/guldan.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)
        self.hp = 1

        #movement
        self.speed = 2
        self.direction = 1

        # Bullet Attack
        self.bullet_timer = 0
        self.bullet_delay = 40  # Frames

        # Laser Attack
        self.laser_timer = 0
        self.laser_delay = 240 #alle 4sec bei 60 fps
        self.laser_active = False
        self.laser_time = 60
        self.laser_time_left = 0
        self.laser_width = 12

    def update(self):
        # Horizontal movement
        self.rect.x += self.speed * self.direction

        if self.rect.left < 50 or self.rect.right > 750:
            self.direction *= -1

        # Attack timers
        self.bullet_timer += 1
        self.laser_timer += 1

    def try_shoot_bullet(self, world):
        if self.bullet_timer >= self.bullet_delay:
            bullet = EnemyBullet((self.rect.centerx, self.rect.bottom))
            world.enemy_bullets.add(bullet)
            world.all_sprites.add(bullet)
            self.bullet_timer = 0

    def try_laser(self):
        if not self.laser_active and self.laser_timer >= self.laser_delay:
            self.laser_active = True
            self.laser_timer = 0
            self.laser_time_left = self.laser_time

        if self.laser_active:
            self.laser_time_left -= 1
            if self.laser_time_left <= 0:
                self.laser_active = False

    def draw_laser(self, screen):
        if self.laser_active:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.rect.centerx - self.laser_width // 2,
                 self.rect.bottom,
                 self.laser_width,
                 600)
            )

    def get_hit(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((6, 10))
        self.image.fill((255, 200, 50))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()




