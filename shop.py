import pygame

def open_shop():
    pygame.init()

    WIDTH, HEIGHT = 400, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shop")

    FONT_TITLE = pygame.font.SysFont("Arial", 30, True)
    FONT_BTN = pygame.font.SysFont("Arial", 20)

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

            txt = FONT_BTN.render(self.text, True, color)
            txt_rect = txt.get_rect(center=self.rect.center)
            screen.blit(txt, txt_rect)

        def clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    buttons = [
        Button("Upgrade 1", 200),
        Button("Upgrade 2", 280),
        Button("Upgrade 3", 360),
        Button("Zurück",   480)
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    if b.clicked(mouse_pos):
                        if b.text == "Zurück":
                            running = False
                        else:
                            print(b.text + " gekauft!")  
            'Hier kommt die der richtige Kaufvorgang mit den Punkten hin'
        screen.fill(BLACK)

        title = FONT_TITLE.render("Schiffsupgrades:", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        for b in buttons:
            b.draw(mouse_pos)

        pygame.display.flip()

    return
