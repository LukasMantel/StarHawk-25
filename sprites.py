import pygame
from settings import *
import random
from sounds import *


ship1 = False
ship2 = True
ship3 = True

'''
Movement speed
Mehrfachschuss
Mehr Leben
Reload speed

Ship2
Ship3
'''

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #Player image
        if ship1 == True:
            self.image = pygame.image.load("images/Ship (13).png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 40))
        elif ship2 == True:
            self.image = pygame.image.load("images/Ship.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        else:
            self.image = pygame.image.load("images/seagull_1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 80)) 


        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.speed = PLAYER_SPEED

        self.hp = 5
        self.max_hp = 5
        
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()

        self.snd_shoot = SND_SHOOT


    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.snd_shoot.play()
    
    def draw_healthbar_player(self, window):
        bar_width = 100
        bar_height = 10
        x = 10
        y = HEIGHT - 20

        #Hintergrund
        pygame.draw.rect(window, RED, (x, y, bar_width, bar_height))
        #Füllung (proportional zur HP)
        fill_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(window, GREEN, (x, y, fill_width, bar_height))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('images/enemy_red.png').convert()
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(ENEMY_SPEED+1, ENEMY_SPEED+3)
        self.health = 1
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x=0, vel_y=-BULLET_SPEED, color=BLUE):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        #Bewegung in beide Richtungen
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        #Aus Bildschirm entfernen
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, player, bullet_group, x=None, y=None):
        super().__init__()
        self.player = player
        self.bullet_group = bullet_group

        self.image = pygame.image.load("images/Guldan.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()

        self.rect.x = x if x is not None else WIDTH // 2 - self.rect.width // 2
        self.rect.y = y if y is not None else 50

        self.health = 10
        self.max_hp = 10

        # Bewegung
        self.vel_x = 3
        self.direction = 1

        # Timer
        self.shoot_delay = 1000
        self.last_shot = 0
        self.laser_delay = 5000
        self.last_laser = 0

    def update(self):
        self.rect.x += self.vel_x * self.direction
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1

        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()

        if now - self.last_laser > self.laser_delay:
            self.last_laser = now
            self.laser()

    def shoot(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.bottom
        dist = max(1, (dx*dx + dy*dy)**0.5)

        vel_x = dx / dist * 5
        vel_y = dy / dist * 5

        # normale Bullet
        bullet = Bullet(self.rect.centerx, self.rect.bottom, vel_x, vel_y, color=YELLOW)
        self.bullet_group.add(bullet)

    def laser(self):
        for i in range(-1, 2):
            dx = self.player.rect.centerx - (self.rect.centerx + i*20)
            dy = self.player.rect.centery - self.rect.bottom
            dist = max(1, (dx*dx + dy*dy)**0.5)

            vel_x = dx / dist * 8
            vel_y = dy / dist * 8

            bullet = Bullet(self.rect.centerx, self.rect.bottom, vel_x, vel_y, color=YELLOW)
            self.bullet_group.add(bullet)

    def draw_healthbar_boss(self, window):
        bar_width = 100
        bar_height = 10
        x = self.rect.centerx - bar_width // 2
        y = self.rect.top - 15

        #Hintergrund
        pygame.draw.rect(window, RED, (x, y, bar_width, bar_height))
        #Füllung (proportional zur HP)
        fill_width = int(bar_width * (self.health / self.max_hp))
        pygame.draw.rect(window, GREEN, (x, y, fill_width, bar_height))
