import os
import pygame

from highscore import show_highscore
from shop import open_shop
from settings import *


screen = pygame.display.set_mode((WIDTH, HEIGHT))
BTN_FONT = pygame.font.SysFont("Impact", 30)


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

def show_pause_menu():
    resume_btn = Button("Resume"(350, 260), (200, 50), BTN_FONT)
    quit_btn = Button("Resume"(350, 260), (200, 50), BTN_FONT)
    #resume_btn = Button("Resume"(350, 260), (200, 50), BTN_FONT)

    screen.fill((0,0,0))

    title = BTN_FONT.render("PAUSE", True, (255,255,255))
    screen.blit(title, title.get_rect(center=(450, 200)))

    resume_btn.draw(screen)
    quit_btn.draw(screen)



