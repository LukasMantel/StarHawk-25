import os
import sys
import pygame
from Gameworld import start_game
from highscore import show_highscore
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarHawk'25")

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "images")
menu_bg = pygame.image.load(os.path.join(ASSETS, "menu_bg.png")).convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

BTN_FONT = pygame.font.SysFont("Impact", 30)

class Button:
    def __init__(self, text, y, action, x=None, width=180, height=50):
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        if x is None:
            x = WIDTH // 2 - width // 2
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, mouse_pos):
        color = GOLD if self.rect.collidepoint(mouse_pos) else BLACK
        txt = BTN_FONT.render(self.text, True, color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()


#game schließen
def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    button_y = HEIGHT * 0.77
    spacing = 95
    total_width = 3 * 180 + 2 * spacing
    offset = 3
    start_x = (WIDTH - total_width)//2 - offset

    buttons = [
        Button("HIGHSCORE", button_y, lambda: show_highscore(), x=start_x),
        Button("GAME", button_y *0.94, lambda: start_game(main_menu), x=start_x + 180 + spacing),
        Button("EXIT GAME", button_y, quit_game, x=start_x + 2*(180 + spacing)
        )
    ]


    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0,0))

        #buttons zeichnen
        for b in buttons:
            b.draw(screen, mouse_pos)

    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    b.click(mouse_pos)
                

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
    pygame.quit()
