import pygame
from settings import *
from sprites import *
from sounds import *
from spawner import ENEMY_SPAWN


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#player
player = Player()
all_sprites = pygame.sprite.Group(player)
#enemies
enemy_group = pygame.sprite.Group()
#spwaner tbd
enemy_spawner = ENEMY_SPAWN


play_game_music()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Spieler schießt bei Space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == ENEMY_SPAWN:
            enemy = Enemy()
            enemy_group.add(enemy)
            all_sprites.add(enemy)
    #Tastatur-Input abfragen
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    #Update
    all_sprites.update()
    player.bullets.update()
    #spwaner tbd - enemy_spawner.update()
    
    #Collision
    hits = pygame.sprite.groupcollide(enemy_group, player.bullets, False, True)
    for enemy in hits:
        enemy.get_hit()
    
    player_hits = pygame.sprite.spritecollide(player, enemy_group, True)
    if player_hits:
        player.get_hit()
    
    
    
    
    
    #Rendern
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player.bullets.draw(screen)
    player.draw_healthbar_player(screen)
    for enemy in enemy_group:
        enemy.draw_healthbar_enemy(screen)
    pygame.display.flip()
    #spwaner tbd - enemy_spawner.enemy_group.draw(screen)
    enemy_group.draw(screen)
    for enemy in enemy_group:
        enemy.draw_healthbar_enemy(screen)
    clock.tick(FPS)

pygame.quit()
