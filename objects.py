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
    def __init__(self,x,y,image, screen_height, large=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.vx = random.randint(-100,100)
        self.vy = random.randint(100,250)
        self.hp = 2 if large else 1
        self.screen_height = screen_height

    def update(self, dt):
        self.rect.x += int(self.vx*dt)
        self.rect.y += int(self.vy*dt)
        if self.rect.top > self.screen_height + 200:
            self.kill()
#StarFragments
class Fragment(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.vx = random.uniform(-80, 80)
        self.vy = random.uniform(-200, -60)
        self.life = 6.0

    def update(self, dt):
        self.vy += 160 * dt 
        self.rect.x += int(self.vx * dt)
        self.rect.y += int(self.vy * dt)

        self.life -= dt
        if self.life <= 0:
            self.kill()

class SpaceJunk(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(
            center=(random.randint(50, width - 50), random.randint(-200, -50))
        )

        self.vx = random.randint(-2, 2)
        self.vy = random.randint(4, 9)
        self.height = height

    def update(self,dt=None):
        self.rect.x += self.vx 
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
        if random.random() < 0.2:
            self.junk.add(SpaceJunk(self.assets["JUNK"], self.width, self.height))
        if random.random() < 0.2:
            self.junk.add(SpaceJunk(self.assets["JUNK2"], self.width, self.height))


        

