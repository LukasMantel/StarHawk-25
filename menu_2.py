import os
import pygame
from Gameworld import start_game
from highscore import show_highscore
from shop import open_shop
from settings import *

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "images")

menu_bg = pygame.image.load(os.path.join(ASSETS, "menu_bg.png")).convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

BTN_FONT = pygame.font.SysFont("Impact", 30)

WHITE = (255, 255, 255)
GOLD = (132, 106, 26)
BLACK = (0, 0, 0)
'''
def show_pause_menu():
    resume_btn = Button("Resume"(350, 260), (200, 50), BTN_FONT)
    quit_btn = Button("Resume"(350, 260), (200, 50), BTN_FONT)
    #resume_btn = Button("Resume"(350, 260), (200, 50), BTN_FONT)

    screen.fill((0,0,0))

    title = BTN_FONT.render("PAUSE", True, (255,255,255))
    screen.blit(title, title.get_rect(center=(450, 200)))

    resume_btn.draw(screen)
    quit_btn.draw(screen)
'''


class Button:
    def __init__(self, text, y, action,x=None):
        self.text = text
        self.action = action
        if x is None:
            x = WIDTH//2 - 100  
        self.rect = pygame.Rect(x, y, 200, 50)
        
    def draw(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            color = GOLD
        else:
            color = BLACK

        txt = BTN_FONT.render(self.text, True, color)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()

# Höhe für die Buttons
button_y = HEIGHT * 0.78

button_width = 180
button_height = 50
spacing = 50

# Start-X so, dass alle Buttons mittig sind
total_width = 3 * button_width + 2 * spacing
offset = 10
start_x = (WIDTH - total_width) // 2 - offset


buttons = [
    Button("HIGHSCORE", button_y, show_highscore, x=start_x),
    Button("GAME", button_y - 5*offset, lambda: start_game(), x=start_x + button_width + spacing),
    Button("SHOP", button_y, open_shop, x=start_x + 2*(button_width + spacing))
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

    screen.blit(menu_bg, (0, 0))
   
    for b in buttons:
        b.draw(mouse_pos)

    pygame.display.flip()
