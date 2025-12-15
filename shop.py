''' Wir haben gemeinsam versucht den Shop zu bearbeiten und die Version mit den Json, zur Dateispeicherung
    umzusetzen und dabei traten immer mehr Probleme auf. Schlußendlich haben wir die Grundstrucktur
    des Shops mit dem Aufbau, Design und Buttons übernommen und die Kaufabwicklung mit Hilfe von 
    Chat GPT neu geschrieben, da wir sonst keinen funktionierendes Shopsystem hätten. 
    Wir haben uns daraufhin hiermit auseinandergesetzt um die Logik zu verstehen und anzupassen.
'''

import pygame
from settings import *

def open_shop(screen, player, space_objects):
    FONT_TITLE = pygame.font.SysFont("Impact", 30)
    FONT_BTN = pygame.font.SysFont("Impact", 20)
    
    upgrades = {
        "shoot_level2": 10,   # einmalig
        "shoot_level3": 20,   # einmalig
        "speed_up": 5,         # mehrfach
        "reload_up": 5,        # mehrfach
        "hp_up": 5             # mehrfach
    }

    one_time_upgrades = {"shoot_level2", "shoot_level3"}
    bought_upgrades = set()  #shoot darf nur 1x gekauft werden

    class Button:
        def __init__(self, text, y, upgrade_name=None, price=0):
            self.text = text
            self.upgrade_name = upgrade_name
            self.price = price
            self.rect = pygame.Rect(200, y, 200, 50)
            self.rect.centerx = screen.get_width() // 2

        def draw(self, mouse_pos):
            color = GOLD if self.rect.collidepoint(mouse_pos) else BLACK
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
            pygame.draw.rect(screen, color, self.rect, 2)
           
            # zurück button ist kein upgrade
            if self.upgrade_name:
                txt = FONT_BTN.render(f"{self.text} ({self.price})", True, color)
            else:
                txt = FONT_BTN.render(f"{self.text}", True, color)
            txt_rect = txt.get_rect(center=self.rect.center)
            screen.blit(txt, txt_rect)

        def clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    buttons = [
        Button("Shoot Level 2", 200, "shoot_level2", upgrades["shoot_level2"]),
        Button("Shoot Level 3", 280, "shoot_level3", upgrades["shoot_level3"]),
        Button("Speed Up", 360, "speed_up", upgrades["speed_up"]),
        Button("Reload Speed", 440, "reload_up", upgrades["reload_up"]),
        Button("HP Up", 520, "hp_up", upgrades["hp_up"]),
        Button("Zurück", 600)
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
                        if b.upgrade_name:
                            # Einmalige Upgrades prüfen
                            if b.upgrade_name in one_time_upgrades and b.upgrade_name in bought_upgrades:
                                message = "Schon gekauft!"
                                msg_timer = pygame.time.get_ticks()
                                break

                            price = upgrades[b.upgrade_name]
                            if space_objects.stats["fragments"] < price:
                                message = "Nicht genug Fragmente!"
                                msg_timer = pygame.time.get_ticks()
                                break

                           
                            space_objects.stats["fragments"] -= price

                            
                            if b.upgrade_name == "shoot_level2":
                                player.upgrade("shoot_level2")
                                bought_upgrades.add("shoot_level2")
                            elif b.upgrade_name == "shoot_level3":
                                player.upgrade("shoot_level3")
                                bought_upgrades.add("shoot_level3")
                            elif b.upgrade_name == "speed_up":
                                player.upgrade("speed_up")
                            elif b.upgrade_name == "reload_up":
                                player.upgrade("reload_up")
                            elif b.upgrade_name == "hp_up":
                                player.hp = min(player.hp + 1, player.max_hp)

                            message = f"{b.text} gekauft!"
                            msg_timer = pygame.time.get_ticks()

        screen.fill(BLACK)
        title = FONT_TITLE.render("Shop - Upgrades kaufen", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        frag_text = FONT_BTN.render(f"Fragmente: {space_objects.stats['fragments']}", True, GOLD)
        screen.blit(frag_text, (20, 20))

        for b in buttons:
            b.draw(mouse_pos)

        if message and pygame.time.get_ticks() - msg_timer < 1500:
            msg_txt = FONT_BTN.render(message, True, RED)
            screen.blit(msg_txt, (600//2 - msg_txt.get_width()//2, 680))

        pygame.display.flip()
