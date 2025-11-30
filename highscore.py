import pygame

def show_highscore():
    pygame.init()

    WIDTH, HEIGHT = 400, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Highscore")

    FONT_TITLE = pygame.font.SysFont("Arial", 30)
    FONT_LIST = pygame.font.SysFont("Arial", 20)
    BTN_FONT = pygame.font.SysFont("Arial", 20)

    WHITE = (255, 255, 255)
    GOLD = (132, 106, 26)
    BLACK = (0, 0, 0)

    class Button:
        def __init__(self, text, y):
            self.text = text
            self.rect = pygame.Rect(100, y, 200, 50)

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

    # Beispiel-Highscore-Liste, wirs später durch echte eingespeicherte Punktewerte ersetzt
    highscores = [("Anna", 120), ("Ben", 100), ("Clara", 80), ("David", 60)]
    
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
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        y_offset = 150
        for name, score in highscores:
            line = FONT_LIST.render(f"{name}: {score}", True, WHITE)
            screen.blit(line, (WIDTH//2 - line.get_width()//2, y_offset))
            y_offset += 35

        back_button.draw(mouse_pos)

        pygame.display.flip()

    return
