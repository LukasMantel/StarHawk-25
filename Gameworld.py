import pygame
from pygame import mixer
from settings import *
from sprites import *
from spawner import EnemyWave
from audio import *
from objects import *
from assets import load_assets


pygame.init()
mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarHawk'25")
clock = pygame.time.Clock()
dt = clock.tick(FPS) / 1000

all_sprites = pygame.sprite.Group()     #Alle Sprites für einfaches Draw/Update
enemies = pygame.sprite.Group()         #Nur Gegner, für Kollisionen
bullets = pygame.sprite.Group()         #Nur Player Bullets
enemy_bullets = pygame.sprite.Group()   #Boss Bullets
boss = pygame.sprite.Group()            #Boss
particles = pygame.sprite.Group()       #neu
assets = load_assets()
space_objects = SpaceObjects(WIDTH, HEIGHT, assets)
player = Player()
all_sprites.add(player)

#background stars
bg = BG(WIDTH, HEIGHT, star_count=150)

wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets, boss, space_objects)
wave_controller.start_new_wave()
 
score = 0
game_over = False  #True, wenn der Spieler besiegt wurde
game_won = False   #neu winning screen
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
            running = False          

        if event.type == pygame.KEYDOWN:
            #Escape = Spiel beenden
            if event.key == pygame.K_ESCAPE: ###Ändern
                running = False
            #godmode test
            if event.key == pygame.K_g:
                player.max_hp = 9999
                player.hp = 9999
                player.speed = 15
                player.shoot_level3 = True
                player.armor = 9999
                player.max_armor = 9999
                player.shoot_delay = 1
                
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
                    boss.empty()
                    enemy_bullets.empty()
                    #Player neu erstellen
                    player = Player()
                    all_sprites.add(player)

                    #Waves neu starten
                    wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets, boss, space_objects)
                    wave_controller.start_new_wave()

                    #Score & HP zurücksetzen
                    score = 0
                    player.hp = player.max_hp
                    game_over = False
                    
            if game_won: ## evtl anpassen, Kopie von game_over
                if event.key == pygame.K_r:
                    #alles reseten
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()
                    boss.empty()
                    enemy_bullets.empty()

                    #Player neu erstellen
                    player = Player()
                    all_sprites.add(player)

                    #Waves neu starten
                    wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets, boss, space_objects)
                    wave_controller.start_new_wave()

                    #Score & HP zurücksetzen
                    score = 0
                    player.hp = player.max_hp
                    game_won = False

    #Update, wenn nicht game over oder paused
    if not game_over and not paused:
        # Enemy Waves aktualisieren
        wave_controller.update() 
        space_objects.update(dt, player, bullets) 
        

        #neue Welle
        if wave_controller.wave_complete and len(enemies) == 0:
            wave_controller.start_new_wave()

        #Sprites updaten
        all_sprites.update()
        enemy_bullets.update()
        particles.update() # neu
        bg.update(dt)

        #collision bullets - enemies, player - enemies player - enemy_bullets (Boss)
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                SND_ENEMY_HIT.play()
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
                    bullet.explode(particles, count=15) #neu
                    score += 10

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            SND_ENEMY_HIT.play()
            if player.armor == 0:
                player.hp -= 1  # Jeder Treffer kostet 1 HP
                if player.hp <= 0:
                    game_over = True
            else:
                player.armor -=1

        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            if player.armor == 0:
                player.hp -= 1  # Jeder Treffer kostet 1 HP
                if player.hp <= 0:
                    game_over = True
            else:
                player.armor -=1


#            player.hp -= 1
#            if player.hp <= 0:
#                game_over = True

        #collision bullets - enemies, player - enemies player - enemy_bullets (Boss)
        hits = pygame.sprite.groupcollide(boss, bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                SND_ENEMY_HIT.play()
                bullet.explode(particles, count=15) #neu
                enemy.health -= 1
                if enemy.health <= 0:
                    game_won = True

    #Draw alle Objekte
    bg.update(dt)
    screen.blit(bg.image, (0, 0))
    all_sprites.draw(screen)
    enemy_bullets.draw(screen)
    player.draw_healthbar_player(screen)
    player.draw_armor_player(screen)
    player.draw_reload_bar(screen)
    particles.draw(screen) #neu
   
    

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
        
    #Win Screen
    if game_won:
        text = big_font.render("YOU WON - PRESS R TO RESTART", True, (255, 0, 0))
        screen.fill((0, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2)) 

    space_objects.draw(screen)

    pygame.display.flip()


pygame.quit()


