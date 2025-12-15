import pygame
from pygame import mixer
from settings import *
from sprites import *
from spawner import EnemyWave
from audio import *
from objects import *
from assets import load_assets
from highscore import *
from menu_functions import show_pause_menu, show_game_over_menu
from shop import open_shop

def start_game(main_menu):
    pygame.init()
    mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("StarHawk'25")
    clock = pygame.time.Clock()
    dt = clock.tick(FPS)/1000
    #Game music
    play_game_music()
    # Sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    boss = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    assets = load_assets()

    space_objects = SpaceObjects(WIDTH, HEIGHT, assets)
    player = Player()
    all_sprites.add(player)

    bg = BG(WIDTH, HEIGHT, star_count=150)
    wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets, boss, space_objects)
    wave_controller.start_new_wave()

    score = 0
    fragment_score = 0
    game_over = False
    game_won = False
    paused = False
    return_to_menu = False

    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return_to_menu = True
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return_to_menu = True
                    running = False
                if event.key == pygame.K_g:
                    player.max_hp = 9999
                    player.hp = 9999
                    player.speed = 15
                    player.shoot_level3 = True
                    player.armor = 9999
                    player.max_armor = 9999
                    player.shoot_delay = 1
                    #
                    new_width = int(PLAYER_WIDTH * 5)   
                    new_height = int(PLAYER_HEIGHT * 4) 
                    player.scale_ship(new_width, new_height)

                if not game_over and not game_won:
                    if event.key == pygame.K_SPACE and not paused:
                        player.shoot(all_sprites, bullets)
                    if event.key == pygame.K_ESCAPE:
                        paused = True
                    
                if (game_over or game_won) and event.key == pygame.K_r:
                    # Reset Game
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()
                    boss.empty()
                    enemy_bullets.empty()
                    player = Player()
                    all_sprites.add(player)
                    wave_controller = EnemyWave(all_sprites, enemies, player, enemy_bullets, boss, space_objects)
                    wave_controller.start_new_wave()
                    score = 0
                    player.hp = player.max_hp
                    space_objects.stats["fragments"] = 0
                    game_over = False
                    game_won = False

        # Pause-Menü
        if paused and not game_over and not game_won:
            def main_menu_wrapper():
                nonlocal return_to_menu, paused
                return_to_menu = True
                paused = False

            show_pause_menu(
                screen,
                resume_action=lambda: None,
                shop_action=lambda: open_shop(screen, player, space_objects),
                main_menu_action=main_menu_wrapper
            )
            paused = False

        if return_to_menu:
            break

        # Game Update
        if not game_over and not paused and not game_won:
            wave_controller.update()
            died = space_objects.update(dt, player, bullets)
            if died:
                 game_over = True

            if wave_controller.wave_complete and len(enemies)==0:
                wave_controller.start_new_wave()

            all_sprites.update()
            enemy_bullets.update()
            particles.update()
            bg.update(dt)

            # Collisions
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                for bullet in bullet_list:
                    SND_ENEMY_HIT.play()
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.kill()
                        bullet.explode(particles, count=15)
                        score += 10

            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                SND_ENEMY_HIT.play()
                if player.armor == 0:
                    player.hp -= 1
                    if player.hp <= 0:
                        game_over = True
                else:
                    player.armor -=1

            hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
            for hit in hits:
                if player.armor == 0:
                    player.hp -= 1
                    if player.hp <= 0:
                        game_over = True
                else:
                    player.armor -=1

            hits = pygame.sprite.groupcollide(boss, bullets, False, True)
            for enemy, bullet_list in hits.items():
                for bullet in bullet_list:
                    SND_ENEMY_HIT.play()
                    bullet.explode(particles, count=15)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        game_won = True

        # Draw everything
        screen.blit(bg.image, (0,0))
        all_sprites.draw(screen)
        enemy_bullets.draw(screen)
        particles.draw(screen)
        space_objects.draw(screen)
        player.draw_healthbar_player(screen)
        player.draw_armor_player(screen)
        player.draw_reload_bar(screen)
        for sprite in all_sprites:
            if isinstance(sprite, Boss):
                sprite.draw_healthbar_boss(screen)

        fragment_score = space_objects.stats["fragments"]
        highscore = get_highscore()
        fragment_text = font.render(f"Fragments: {fragment_score}", True, WHITE)
        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        wave_text = font.render(f"Wave: {wave_controller.wave_number}", True, WHITE)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
        screen.blit(wave_text, (WIDTH - wave_text.get_width() - 10, 50))
        screen.blit(fragment_text, (WIDTH - fragment_text.get_width() - 10, 90))
        screen.blit(highscore_text, (WIDTH - highscore_text.get_width() - 10, 130))

        # Game Over Menü
        if game_over:
            if score > highscore:
                player_name = ask_player_name()
                save_highscore(score, player_name)

            def main_menu_wrapper_go():
                nonlocal return_to_menu
                return_to_menu = True

            show_game_over_menu(screen, main_menu_action=main_menu_wrapper_go)
            if return_to_menu:
                break

        # Win Screen
        if game_won:
            screen.fill((0,0,0))
            text = big_font.render("YOU WON - PRESS R TO RESTART", True, (255,0,0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

        pygame.display.flip()

    return


