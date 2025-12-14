import os
import pygame
from main import start_game
from highscore import show_highscore
from shop import open_shop

pygame.init()

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "images")

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FONT = pygame.font.SysFont("Arial", 30, True)
BTN_FONT = pygame.font.SysFont("Arial", 20)

WHITE = (255, 255, 255)
GOLD = (132, 106, 26)
BLACK = (0, 0, 0)

title_image = pygame.image.load(os.path.join (images, "sh_titel.png")).convert_alpha()
title_rect = title_image.get_rect(center=(WIDTH // 2, 120))

class Button:
    def __init__(self, text, y, action):
        self.text = text
        self.action = action
        self.rect = pygame.Rect(200, y, 200, 50)

    def draw(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            color = GOLD
        else:
            color = WHITE

        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, color, self.rect, 2)

        txt = BTN_FONT.render(self.text, True, color)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()
    
buttons = [
    Button("Game", 200, lambda: start_game()),
    Button("Highscore", 280, show_highscore),
    Button("Shop", 360, open_shop)
]

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for b in buttons:
                    b.click(mouse_pos)

    screen.fill(BLACK)

    screen.blit(title_image, title_rect)
   
    for b in buttons:
        b.draw(mouse_pos)

    pygame.display.flip()