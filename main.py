import os
import math
import pygame
import random
from pygame.locals import *
from objects import SpaceObjects, BG

def start_game():
    pygame.init()
    pygame.mixer.init()

    game_over = False
    game_over_timer = 0
    won = False
    text = None
    hs_text = None


    # Pfade & Screen
    BASE = os.path.dirname(os.path.abspath(__file__))
    ASSETS = os.path.join(BASE,"assets")
    screen = pygame.display.set_mode((900,600))
    pygame.display.set_caption("Space Fragments")
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("Arial",18)

    # Audio
    pygame.mixer.music.load(os.path.join(ASSETS,"stars.ogg"))
    pygame.mixer.music.play(-1)
    bang_sound = pygame.mixer.Sound(os.path.join(ASSETS,"bangshot.ogg"))

    def load(name):
        path = os.path.join(ASSETS,name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset nicht gefunden: {path}")
        return pygame.image.load(path).convert_alpha()

    # Assets
    PLAYER_IMG = pygame.transform.scale(load("player_blue.png"), (64,64))
    ENEMY_IMG = pygame.transform.scale(load("enemy_red.png"), (60,60))
    MET_SMALL = pygame.transform.scale(load("meteor_small.png"), (48,48))
    MET_LARGE = pygame.transform.scale(load("meteor_large.png"), (96,96))
    STAR = pygame.transform.scale(load("star_fragment.png"), (24,24))
    BOSS_IMG = pygame.transform.scale(load("boss_guldan.png"), (180,180))
    JUNK_IMG = pygame.transform.scale(load("space_junk.png"), (32,32))
    JUNK2_IMG = pygame.transform.scale(load("space_junk2.png"), (32,32))

    W,H = screen.get_size()

    # Highscore
    def load_highscore():
        path = os.path.join(BASE,"highscore.txt")
        if os.path.exists(path):
            with open(path,"r") as f: return int(f.read().strip())
        return 0
    def save_highscore(value):
        path = os.path.join(BASE,"highscore.txt")
        with open(path,"w") as f: f.write(str(value))
    highscore = load_highscore()

    # Player & Bullet
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = PLAYER_IMG
            self.rect = self.image.get_rect(center=(W//2,H-80))
            self.speed = 320
            self.cool = 0
            self.lives = 3
            self.armor = 3

        def update(self,dt,keys):
            if keys[K_LEFT] or keys[K_a]: self.rect.x -= int(self.speed*dt)
            if keys[K_RIGHT] or keys[K_d]: self.rect.x += int(self.speed*dt)
            self.rect.x = max(10,min(self.rect.x,W-self.rect.width-10))
            self.cool = max(0,self.cool-dt)

        def shoot(self):
            b = Bullet(self.rect.centerx,self.rect.top+4)
            bullets.add(b)
            bang_sound.play()

    class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super().__init__()
            self.image = pygame.Surface((6,6), pygame.SRCALPHA)
            pygame.draw.circle(self.image,(255,220,120),(3,3),3)
            self.rect = self.image.get_rect(center=(x,y))
            self.vx = 0
            self.vy = -600
        def update(self,dt):
            self.rect.x += int(self.vx*dt)
            self.rect.y += int(self.vy*dt)
            if self.rect.bottom < -50: self.kill()

    # Enemy & Boss
    class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super().__init__()
            self.image = ENEMY_IMG
            self.rect = self.image.get_rect(center=(x,y))
            self.hp = 1
            self._t = random.random()*1000
        def update(self,dt):
            self._t += dt*1000
            self.rect.y += int(math.sin(self._t/400)*50*dt + 200*dt)
            self.rect.x += int(math.sin(self._t/600)*50*dt)
            if self.rect.top > H+100: self.kill()

    class Boss(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = BOSS_IMG
            self.rect = self.image.get_rect(center=(W//2,120))
            self.max_hp = 25
            self.hp = 25
            self.laserCooldown = 7.0
            self.laserTimer = self.laserCooldown
            self.shootCooldown = 1.0
            self.shootTimer = 0
            self.vx = 100
            self.vy = 40
            self.direction_x = 1
            self.direction_y = 1

        def update(self,dt):
            self.rect.x += int(self.vx*dt*self.direction_x)
            self.rect.y += int(self.vy*dt*self.direction_y)
            if self.rect.left <= 10: self.direction_x = 1
            if self.rect.right >= W-10: self.direction_x = -1
            if self.rect.top <= 10: self.direction_y = 1
            if self.rect.bottom >= H//2: self.direction_y = -1

            self.shootTimer -= dt
            if self.shootTimer <= 0:
                self.shootTimer = self.shootCooldown
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                distance = math.hypot(dx,dy) or 1
                vx = dx/distance*300
                vy = dy/distance*300
                boss_bullets.append({"x":self.rect.centerx,"y":self.rect.centery,"vx":vx,"vy":vy,"life":5.0})

            self.laserTimer -= dt
            if self.laserTimer <=0:
                self.laserTimer = self.laserCooldown
                lasers.append({"x":self.rect.centerx,"y":self.rect.centery,"life":1.2})

    # Groups & SpaceObjects
    player = Player()
    players = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    lasers = []
    boss_bullets = []

    assets = {
        "MET_SMALL": MET_SMALL,
        "MET_LARGE": MET_LARGE,
        "FRAGMENT": STAR,
        "JUNK": JUNK_IMG,
        "JUNK2": JUNK2_IMG
    }
    space_objects = SpaceObjects(W,H,assets)

    bg = BG(W,H, star_count=200) 

    # Waves
    def spawn_wave(n):
        for k in range(6+n*2):
            x = 80 + k*(W-160)//max(1,6+n*2)
            enemies.add(Enemy(x,-40-k*30))
        for m in range(3+n):
            space_objects.spawn_meteor(random.randint(40,W-40), random.randint(-300,-60), random.random()>0.8)
            space_objects.spawn_random_junk()

    wave = 0
    score = 0
    wave_cooldown = 0.0
    spawn_wave(wave)

    # Main Loop
    running = True
    game_over = False
    won = False

    while running:
        dt = clock.tick(60)/1000.0
        for ev in pygame.event.get():
            if ev.type == QUIT:
                return
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    if game_over:
                        return
                if ev.key in (K_SPACE,K_UP):
                    if not game_over and player.cool <=0:
                        player.shoot(); player.cool=0.3

        if not game_over:
            keys = pygame.key.get_pressed()
            players.update(dt,keys)
            bullets.update(dt)
            enemies.update(dt)
            bosses.update(dt)
            space_objects.update(dt,player,bullets)
            bg.update(dt)

            # Laser
            for l in lasers: l["life"] -= dt
            lasers = [l for l in lasers if l["life"]>0]

            for b in boss_bullets:
                b["x"] += int(b["vx"]*dt)
                b["y"] += int(b["vy"]*dt)
                b["life"] -= dt
            boss_bullets = [b for b in boss_bullets if b["life"]>0]

            # Bullet collisions
            for b in bullets:
                for bo in bosses:
                    if bo.rect.collidepoint(b.rect.center):
                        bo.hp -= 1; b.kill(); score += 200
                        if bo.hp <=0: bo.kill(); won=True; game_over=True
                hit = pygame.sprite.spritecollideany(b,enemies)
                if hit:
                    hit.hp -=1; b.kill()
                    if hit.hp <=0: hit.kill(); score+=100

            # Player collision
            if pygame.sprite.spritecollideany(player,enemies):
                if player.armor>0: player.armor-=1
                else: player.lives-=1
                for e in enemies:
                    if pygame.sprite.collide_rect(e,player): e.kill()
                player.rect.center=(W//2,H-50)
                if player.lives<=0: game_over=True

            for b in boss_bullets:
                if player.rect.collidepoint(b["x"],b["y"]):
                    if player.armor>0: player.armor-=1
                    else: player.lives-=1
                    b["life"]=0
                    player.rect.center=(W//2,H-50)
                    if player.lives<=0: game_over=True

            # Wave logic
            if wave_cooldown>0: wave_cooldown -= dt
            if len(enemies)==0 and len(space_objects.meteors)==0 and len(bosses)==0 and wave_cooldown<=0:
                wave_cooldown=1.0
                if wave<2: wave+=1; spawn_wave(wave)
                else:
                    if len(bosses)==0: bosses.add(Boss())

        # Draw everything
        screen.blit(bg.image,(0,0))
        players.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        bosses.draw(screen)
        space_objects.draw(screen)

        for l in lasers:
            alpha = max(0,min(255,int(255*(l["life"]/1.2))))
            surf = pygame.Surface((12,H-l["y"]),pygame.SRCALPHA)
            surf.fill((255,40,40,alpha))
            screen.blit(surf,(l["x"]-6,l["y"]))

        for b in boss_bullets:
            pygame.draw.circle(screen,(255,100,0),(int(b["x"]),int(b["y"])),6)

        # HUD
        stats = space_objects.stats
        current_score = score + stats["score"]
        hud = FONT.render(f"Score: {current_score}  Highscore: {highscore}  Lives: {player.lives}  Armor: {player.armor}  Fragments: {stats['fragments']}  Wave: {wave+1}",True,(255,255,255))
        screen.blit(hud,(10,H-30))

        for bo in bosses:
            hp_ratio = bo.hp/bo.max_hp
            pygame.draw.rect(screen,(255,0,0),(bo.rect.left,bo.rect.top-10,bo.rect.width*hp_ratio,5))
            pygame.draw.rect(screen,(255,255,255),(bo.rect.left,bo.rect.top-10,bo.rect.width,5),1)

        if player.lives <= 0:
            game_over = True
            won = False 
            final_score = score + space_objects.stats["score"]
            if final_score > highscore:
                highscore = final_score
                save_highscore(highscore)
            text = FONT.render(f"{'YOU WON!' if won else 'YOU LOST!'}  Score: {final_score}", True, (255,255,255))
            hs_text = FONT.render(f"Highscore: {highscore}", True, (255,255,0))
            game_over_timer = 3.0  

        if game_over:
            screen.fill((0,0,0))
            if text and hs_text:
                screen.blit(text,text.get_rect(center=(W//2,H//2-20)))
                screen.blit(hs_text,hs_text.get_rect(center=(W//2,H//2+20)))
        
            game_over_timer -= dt
            keys = pygame.key.get_pressed()

            if game_over and (keys[K_ESCAPE] or game_over_timer <= 0):
                return

        pygame.display.flip()

if __name__ == "__main__":
    start_game()

