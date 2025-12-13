import pygame
import random

# Starfield
class Star(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        size = random.randint(1, 3)
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - 1)
        self.rect.y = random.randint(-height, height)  
        self.speed_y = random.uniform(30, 150) / size  
        self.screen_width = width
        self.screen_height = height

    def update(self, dt):
        self.rect.y += int(self.speed_y * dt)
        if self.rect.y > self.screen_height:
            self.rect.y = -2
            self.rect.x = random.randint(0, self.screen_width)

#Background
class BG(pygame.sprite.Sprite):
    def __init__(self, width, height, star_count=150):
        super().__init__()
        self.width = width
        self.height = height 
        self.image = pygame.Surface((width, height))
        self.color = (0, 0, 15)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.stars = pygame.sprite.Group(
            Star(width, height) for _ in range(star_count)
        )

    def update(self, dt):
        self.stars.update(dt)
        self.image.fill(self.color)
        self.stars.draw(self.image)

class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y, image, height, large=False):
        super().__init__()
        orig_w, orig_h = image.get_size()
        if large:
            scale = 0.5  
            self.hp = 2
        else:
            scale = 0.8  
            self.hp = 1
        self.image = pygame.transform.scale(image, (int(orig_w*scale), int(orig_h*scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 0
        self.vy = random.randint(100, 250)
        self.height = height

    def update(self, dt):
        self.rect.y += int(self.vy * dt)
        if self.rect.top > self.height:
            self.kill()
#StarFragments
class Fragment(pygame.sprite.Sprite):
    def __init__(self, x, y, image, size=35):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 0
        self.vy = random.uniform(-200, -60)  
        self.life = 6.0

    def update(self, dt):
        self.vy += 160 * dt
        self.rect.y += int(self.vy * dt)
        self.life -= dt
        if self.life <= 0:
            self.kill()


class SpaceJunk(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.image = pygame.transform.scale(image, (35, 35))  # kleinere Größe
        self.rect = self.image.get_rect(center=(random.randint(30, width-30), random.randint(-200, -50)))
        self.vx = 0
        self.vy = random.randint(4, 5)
        self.height = height

    def update(self, dt=None):
        self.rect.y += self.vy
        if self.rect.top > self.height:
            self.kill()

class SpaceObjects:
    def __init__(self, width, height, assets):
        self.width = width
        self.height = height
        self.assets = assets
        self.meteors = pygame.sprite.Group()
        self.fragments = pygame.sprite.Group()
        self.junk = pygame.sprite.Group()
        self.stats = {"fragments": 0, "score": 0}

    def spawn_meteor(self, x, y, large=False):
        img = self.assets["MET_LARGE"] if large else self.assets["MET_SMALL"]
        m = Meteor(x, y, img, self.height, large)
        self.meteors.add(m)

    def spawn_random_junk(self):
        if random.random() < 0.1:  
            self.junk.add(SpaceJunk(self.assets["JUNK"], self.width, self.height))
        if random.random() < 0.1:
            self.junk.add(SpaceJunk(self.assets["JUNK2"], self.width, self.height))
            
    def update(self, dt, player, bullets):
        self.meteors.update(dt)
        self.fragments.update(dt)
        self.junk.update(dt)

    
#Meteorites hit by bullets
        for b in bullets:
            hit = pygame.sprite.spritecollideany(b, self.meteors)
            if hit:
                hit.hp -= 1
                b.kill()
                if hit.hp <= 0:
                    explosion = Explosion(hit.rect.centerx, hit.rect.centery, 60)
                    self.fragments.add(explosion)
                    for _ in range(2 if hit.image.get_width() < 50 else 4):
                        f = Fragment(
                            hit.rect.centerx + random.randint(-12, 12),
                            hit.rect.centery + random.randint(-12, 12),
                            self.assets["FRAGMENT"]
                        )
                        self.fragments.add(f)
                    hit.kill()
                    self.stats["score"] += 20

#collect fragments
        for f in self.fragments:
            if pygame.sprite.collide_rect(f, player):
                self.stats["fragments"] += 1
                f.kill()
  #collect junk              
         for j in self.junk:
            if pygame.sprite.collide_rect(j, player):
                if hasattr(player, "armor"):
                    if player.armor < 3:
                        player.armor += 1
                j.kill()       
        
    def draw(self, screen):
        self.meteors.draw(screen)
        self.fragments.draw(screen)
        self.junk.draw(screen)

