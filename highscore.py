import pygame
import os
import json

HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.json")

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("highscore", [])
    return []

def show_highscore():
    pygame.init()

    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Highscore")

    FONT_TITLE = pygame.font.SysFont("Arial", 30)
    FONT_LIST = pygame.font.SysFont("Arial", 20)
    BTN_FONT = pygame.font.SysFont("Arial", 20)

    WHITE = (255, 255, 255)
    GOLD = (132, 106, 26)
    BLACK = (0, 0, 0)

    #Buttoneigenschaften
    class Button:
        def __init__(self, text, y):
            self.text = text
            self.rect = pygame.Rect(WIDTH//2-100, y, 200, 50)

        def draw(self, mouse_pos):
            color = GOLD if self.rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, BLACK, self.rect)
            pygame.draw.rect(screen, color, self.rect, 2)
            txt = BTN_FONT.render(self.text, True, color)
            txt_rect=txt.get_rect(center=self.rect.center)
            screen.blit(txt, txt_rect)

        def clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    back_button = Button("Zurück", 480)

    # Top 5 Highscores aus der JSON laden und sortieren
    highscore_data = load_highscore()
    highscore_data.sort(key=lambda x: x["score"], reverse=True)
    highscore = [(entry["name"], entry["score"]) for entry in highscore_data[:5]]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.clicked(mouse_pos):
                    running = False

        screen.fill(BLACK)

        title = FONT_TITLE.render("Highscore:", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))

        if not highscore:
            msg = FONT_LIST.render("Keine Highscores vorhanden.", True, WHITE)
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))
        else:
            y_offset = 150
            for name, score in highscore:
                line = FONT_LIST.render(f"{name}: {score}", True, WHITE)
                screen.blit(line, line.get_rect(center=(WIDTH//2, y_offset)))
                y_offset += 35

        back_button.draw(mouse_pos)

        pygame.display.flip()

    return
