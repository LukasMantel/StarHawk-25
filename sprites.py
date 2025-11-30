import pygame
import random
from settings import *
from sounds import *



class Player(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, speed=PLAYER_SPEED):
        super().__init__()
        self.image = pygame.image.load("images/Ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x if x is not None else WIDTH // 2
        self.rect.bottom = y if y is not None else HEIGHT - 10
        self.hp = 5
        self.max_hp = 5
        #Bewegung
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        #Bullets
        self.bullets = pygame.sprite.Group()
        self.snd_shoot = SND_SHOOT
        #Steuerung
    def handle_input(self, keys):
        self.vel_x = 0
        self.vel_y = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        if keys[pygame.K_UP]:
            self.vel_y = -self.speed
        if keys[pygame.K_DOWN]:
            self.vel_y = self.speed
    def update(self):
        #Bewegung updaten
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        #Bildschirmgrenzen
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

        #Bullets updaten und entfernen, wenn sie oben rausfliegen
        self.bullets.update()
    def shoot(self):
        self.snd_shoot.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)

    #Umgang mit collision
    def get_hit(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            paused = True
            font = pygame.font.SysFont(None, 50)
            text = font.render("GAME OVER - PRESS R TO RESTART", True, (255, 0, 0))

            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: #Neustart
                            paused = False
                            self.hp = self.max_hp

                #Bildschirm füllen und Text anzeigen
                pygame.display.get_surface().fill((0, 0, 0))
                pygame.display.get_surface().blit(text,(WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.Clock().tick(15)  #FPS begrenzen

    def draw_healthbar_player(self, window):
        bar_width = 100
        bar_height = 10
        x = 10
        y = HEIGHT - 20

        #Hintergrund
        pygame.draw.rect(window, ROT, (x, y, bar_width, bar_height))
        #Füllung (proportional zur HP)
        fill_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(window, GRUEN, (x, y, fill_width, bar_height))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('images/ship (13).png').convert()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - 50)
        self.rect.y = -self.rect.height
        self.snd_hit = SND_ENEMY_HIT
        self.hp = 2
        self.max_hp = 2
        self.vel_x = 0
        self.vel_y = 5

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def get_hit(self):
        self.snd_hit.play()
        self.hp -= 1
        if self.hp <= 0:
            self.destroy()

    def draw_healthbar_enemy(self, window):
        bar_width = 50
        bar_height = 5
        x = self.rect.x 
        y = self.rect.y - 10 

        #Hintergrund
        pygame.draw.rect(window, ROT, (x, y, bar_width, bar_height))
        #Füllung (proportional zur HP)
        fill_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(window, GRUEN, (x, y, fill_width, bar_height))

    def destroy(self):
        self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=BULLETS_SPEED):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(HELLES_BLAU)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        #Entfernen, wenn Bullet den oberen Bildschirmrand verlässt
        if self.rect.bottom < 0:
            self.kill()
