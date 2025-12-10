import pygame
from pygame import mixer
from settings import *
from sprites import *
from spawner import EnemyWave
from sounds import *


pygame.init()
mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarHawk'25")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()     #Alle Sprites für einfaches Draw/Update
enemies = pygame.sprite.Group()         #Nur Gegner, für Kollisionen
bullets = pygame.sprite.Group()         #Nur Spieler Bullets
enemy_bullets = pygame.sprite.Group()   #Enemy Bullets

player = Player()
all_sprites.add(player)

wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets)
wave_controller.start_new_wave()

score = 0
game_over = False  #True, wenn der Spieler besiegt wurde
paused = False     #True, wenn das Spiel pausiert ist
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

play_game_music()

#Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            

        if event.type == pygame.KEYDOWN:
            #Escape = Spiel beenden
            if event.key == pygame.K_ESCAPE:
                running = False

            #Space = Schießen (nur, wenn nicht Game Over oder Paused)
            if not game_over:
                if event.key == pygame.K_SPACE and not paused:
                    player.shoot(all_sprites, bullets)
                if event.key == pygame.K_p:
                    paused = not paused
            #R = Game Reset (nur, wenn Game Over)
            if game_over:
                if event.key == pygame.K_r:
                    #alles reseten
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()

                    #Player neu erstellen
                    player = Player()
                    all_sprites.add(player)

                    #Waves neu starten
                    wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets)
                    wave_controller.start_new_wave()

                    #Score & HP zurücksetzen
                    score = 0
                    player.hp = player.max_hp
                    game_over = False

    #Update, wenn nicht game over oder paused
    if not game_over and not paused:
        # Enemy Waves aktualisieren
        wave_controller.update()
        

        #neue Welle
        if wave_controller.wave_complete and len(enemies) == 0:
            wave_controller.start_new_wave()

        #Sprites updaten
        all_sprites.update()
        enemy_bullets.update()

        #collision bullets - enemies, player - enemies player - enemy_bullets (Boss)
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                SND_ENEMY_HIT.play()
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10


        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            SND_ENEMY_HIT.play()
            player.hp -= 1  # Jeder Treffer kostet 1 HP
            if player.hp <= 0:
                game_over = True


        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            player.hp -= 1
            if player.hp <= 0:
                game_over = True

    #Draw alle Objekte
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    enemy_bullets.draw(screen)
    player.draw_healthbar_player(screen)


    for sprite in all_sprites:
        if isinstance(sprite, Boss):
            sprite.draw_healthbar_boss(screen)


    #Waves und score anzeigen
    score_text = font.render(f"Score: {score}", True, WHITE)
    wave_text = font.render(f"Wave: {wave_controller.wave_number}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    screen.blit(wave_text, (WIDTH - wave_text.get_width() - 10, 50))

    #Pause + text
    if paused:
        pause_text = big_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))

    #Game over + text
    if game_over:
        text = big_font.render("GAME OVER - PRESS R TO RESTART", True, (255, 0, 0))
        screen.fill((0, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))


    pygame.display.flip()


pygame.quit()

