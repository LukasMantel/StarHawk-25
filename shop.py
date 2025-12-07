import pygame
from player_data import load_data, save_data

def open_shop():
    pygame.init()

    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shop")

    FONT_TITLE = pygame.font.SysFont("Arial", 30, True)
    FONT_BTN = pygame.font.SysFont("Arial", 20)

    WHITE = (255, 255, 255)
    GOLD = (132, 106, 26)
    BLACK = (0, 0, 0)
    RED = (200, 50, 50)

    data = load_data()

    class Button:
        def __init__(self, text, y):
            self.text = text
            self.rect = pygame.Rect(200, y, 200, 50)

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
        Button("Upgrade 1", 200, 1),
        Button("Upgrade 2", 280, 2),
        Button("Upgrade 3", 360, 3),
        Button("Zurück",   480)
    ]

    message = ""
    msg_timer = 0

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
                            break

                        if b.ship_id is not None:
                            ship = str(b.ship_id)

                            
                            if b.ship_id in data["owned_ships"]:
                                message = "Schon gekauft."
                                msg_timer = pygame.time.get_ticks()
                                break

                           
                            price = data["ships"][ship]["price"]
                            if data["coins"] < price:
                                message = "Zu wenig Coins!"
                                msg_timer = pygame.time.get_ticks()
                                break

                            data["coins"] -= price
                            data["owned_ships"].append(b.ship_id)
                            save_data(data)

                            message = f"Upgrade {ship} gekauft!"
                            msg_timer = pygame.time.get_ticks()

        screen.fill(BLACK)

        title = FONT_TITLE.render("Schiffsupgrades:", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        coins_text = FONT_BTN.render(f"Coins: {data['coins']}", True, GOLD)
        screen.blit(coins_text, (20, 20))

        for b in buttons:
            b.draw(mouse_pos)

        if message and pygame.time.get_ticks() - msg_timer < 1000:
            msg_txt = FONT_BTN.render(message, True, RED)
            screen.blit(msg_txt, (WIDTH//2 - msg_txt.get_width()//2, 450))

        pygame.display.flip()

    return