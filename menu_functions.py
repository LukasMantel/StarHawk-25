import pygame
from settings import *




class Button:
    def __init__(self, text, y, action, x=None, width=200, height=50):
        self.text = text
        self.action = action
        if x is None:
            x = WIDTH // 2 - width // 2
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, mouse_pos, font):
        color = GOLD if self.rect.collidepoint(mouse_pos) else BLACK
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        pygame.draw.rect(surface, GOLD, self.rect, 3) 
        txt = font.render(self.text, True, color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()


def show_pause_menu(screen, resume_action, shop_action, main_menu_action):
    pygame.font.init()
    BTN_FONT = pygame.font.SysFont("Impact", 40)
    paused = True

    def resume_wrapper():
        nonlocal paused
        paused = False
        resume_action()

    def shop_wrapper():
        nonlocal paused
        paused = False
        shop_action()

    def main_menu_wrapper():
        nonlocal paused
        paused = False
        main_menu_action()

    buttons = [
        Button("RESUME", HEIGHT//2 - 60, resume_wrapper),
        Button("SHOP", HEIGHT//2, shop_wrapper),
        Button("MAIN MENU", HEIGHT//2 + 60, main_menu_wrapper)
    ]

    while paused:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    b.click(mouse_pos)

        screen.fill((0,0,0))
        title = BTN_FONT.render("PAUSED", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 120)))
        for b in buttons:
            b.draw(screen, mouse_pos, BTN_FONT)
        pygame.display.flip()


def show_game_over_menu(screen, main_menu_action):
    pygame.font.init()
    BTN_FONT = pygame.font.SysFont("Impact", 40)
    active = True

    def exit_loop():
        nonlocal active
        active = False
        main_menu_action()

    menu_btn = Button("MAIN MENU", HEIGHT // 2 + 60, exit_loop)
    buttons = [menu_btn]

    while active:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    b.click(mouse_pos)

        screen.fill((0,0,0))
        title = BTN_FONT.render("GAME OVER", True, (255,0,0))
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
        for b in buttons:
            b.draw(screen, mouse_pos, BTN_FONT)
        pygame.display.flip()
