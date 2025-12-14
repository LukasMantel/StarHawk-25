import pygame
from settings import *
import random
from audio import *
import math




'''

FÜR Kira:
Upgrades aufrufen:
player.upgrade("shoot_level2") z.B.
player.upgrade("hp_up")
player.upgrade("speed_up")
player.upgrade("reload_up")
etc.

Movement speed
Mehrfachschuss
Mehr Leben
Reload speed

Ship2
Ship3
'''
ship1 = True
ship2 = False
ship3 = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #Player image
        if ship1 == True:
            self.image = pygame.image.load("images/kestrel_3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        elif ship2 == True:
            self.image = pygame.image.load("images/pidgeon_2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        else:
            self.image = pygame.image.load("images/seagull_1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)) 

        self.ship1 = True
        self.ship2 = False
        self.ship3 = False

        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-100))
        self.speed = PLAYER_SPEED
        
        self.shoot_level1 = True
        self.shoot_level2 = False
        self.shoot_level3 = False
        
        self.armor = 0
        self.max_armor = 5

        self.hp = PLAYER_HP
        self.max_hp = PLAYER_MAX_HP
        
        self.shoot_delay = 2000  # milliseconds
        self.last_shot = pygame.time.get_ticks()

        self.snd_shoot = SND_SHOOT

#reload?
    def get_reload_progress(self):
        now = pygame.time.get_ticks()
        diff = now - self.last_shot

        # Werte clampen auf 0–1
        progress = min(diff / self.shoot_delay, 1)
        return progress

    def draw_reload_bar(self, surface):
        progress = self.get_reload_progress()

        bar_width = 120
        bar_height = 12

        # RECHTS UNTEN
        x = WIDTH - bar_width - 10
        y = HEIGHT - 25

        # Hintergrund (dunkelgrau)
        pygame.draw.rect(surface, (60, 60, 60), (x, y, bar_width, bar_height))

        # Füllung (grün)
        fill = int(bar_width * progress)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, fill, bar_height))

        # Rahmen
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
    '''
    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.snd_shoot.play()
    '''
    def upgrade(self, upgrade_name):
        if upgrade_name == "shoot_level1":
            self.shoot_level1 = True

        elif upgrade_name == "shoot_level2":
            self.shoot_level2 = True

        elif upgrade_name == "shoot_level3":
            self.shoot_level3 = True

        elif upgrade_name == "hp_up":
            self.max_hp += 1
            
        elif upgrade_name == "speed_up":
            self.speed += 1

        elif upgrade_name == "reload_up":
            self.shoot_delay = max(80, self.shoot_delay - 50)  #Limit, sonst super OP

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.snd_shoot.play()

            #normaler Schuss - level1
            if self.shoot_level1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

            #3fach Schuss - level2
            if self.shoot_level2:
                offsets = [-80, 0, 80]
                for off in offsets:
                    bullet = Bullet(self.rect.centerx + off, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

            #5fach Schuss - level3
            if self.shoot_level3:
                offsets = [-120, -60, 0, 60, 120]
                for off in offsets:
                    bullet = Bullet(self.rect.centerx + off, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

    def draw_healthbar_player(self, surface):
        bar_width = 120
        bar_height = 12
        x = 10
        y = HEIGHT - 20

        #Hintergrund
        pygame.draw.rect(surface, GREY, (x, y, bar_width, bar_height))
        #Füllung (proportional zur HP)
        fill_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(surface, GREEN, (x, y, fill_width, bar_height))
        #Rahmen
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        #HP als Text anzeigen
        font = pygame.font.Font(None, 24)  # Schriftart und -größe
        hp_text = font.render(f"{self.hp}/{self.max_hp}", True, WHITE)
        #Text rechts neben die Leiste setzen
        surface.blit(hp_text, (x + bar_width + 5, y - 2))

    def draw_armor_player(self, surface):
        bar_width = 120
        bar_height = 12
        x = 10
        y = HEIGHT - 40

        #Hintergrund
        pygame.draw.rect(surface, GREY, (x, y, bar_width, bar_height))
        #Füllung (proportional zur HP)
        fill_width = int(bar_width * (self.armor / self.max_armor))
        pygame.draw.rect(surface, BLUE, (x, y, fill_width, bar_height))
        #Rahmen
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        #HP als Text anzeigen
        font = pygame.font.Font(None, 24)  # Schriftart und -größe
        hp_text = font.render(f"{self.armor}/{self.max_armor}", True, WHITE)
        #Text rechts neben die Leiste setzen
        surface.blit(hp_text, (x + bar_width + 5, y - 2))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('images/enemy_red.png').convert_alpha()
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
            self.explode() # neu
    def explode(self, group=None, count=10):
        #Erstellt eine kleine Explosion aus Partikeln.
        #group: pygame.sprite.Group, in die die Partikel kommen
        #count: Anzahl der Partikel
       
        if group is None:
            return  # Keine Gruppe angegeben -> nichts machen

        for _ in range(count):
            p = Particle()
            p.rect.center = self.rect.center
            group.add(p)
# neu
class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = random.randrange(2, 6)
        self.height = self.width
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.color = (random.randrange(0, 255),
                      random.randrange(0, 255),
                      random.randrange(0, 255))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.kill_timer = 30
        self.vel_x = random.randrange(-8, 8)
        self.vel_y = random.randrange(-8, 8)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.kill_timer -= 1
        if self.kill_timer <= 0:
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

        self.health = BOSS_HEALTH
        self.health_max = BOSS_HEALTH_MAX

        
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
        fill_width = int(bar_width * (self.health / self.health_max))
        pygame.draw.rect(window, GREEN, (x, y, fill_width, bar_height))

