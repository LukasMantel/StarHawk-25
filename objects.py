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
