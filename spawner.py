import random
from sprites import Enemy, BossGuldan

class Spawner:
    def __init__(self, world):
        self.world = world
        self.spawn_timer = 0
        self.spawn_delay = 300  # alle 5 Sekunden (bei 60 FPS)

        #Formationen - tbd
        self.formations = [
            self.spawn_line,
            self.spawn_v_formation
        ]

        #Anzahl der Wellen
        self.max_waves = 5
        self.waves_spawned = 0

        #Guldan spawned
        self.boss_spawned = False

    def update(self):
        #Wenn Boss da, keine wellen merh
        if self.boss_spawned:
            return

        #wenn alle welleb gespawned sind, erscheint boss
        if self.waves_spawned >= self.max_waves:
            self.spawn_boss()
            return

        # Normales Wave-Spawning
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            formation = random.choice(self.formations)
            formation()
            self.waves_spawned += 1
            self.spawn_timer = 0


    def spawn_line(self):
        count = 6
        spacing = self.world.width // (count + 1)
        for i in range(count):
            x = spacing * (i + 1)
            self._add_enemy(x, -40)

    def spawn_v_formation(self):
        """V-förmige Formation."""
        mid = self.world.width // 2
        offset = 40
        for i in range(5):
            x_left = mid - i * offset
            x_right = mid + i * offset
            y = -40 - i * 20
            self._add_enemy(x_left, y)
            if i > 0:
                self._add_enemy(x_right, y)



    def spawn_boss(self):
        if self.boss_spawned:
            return

        boss = BossGuldan((self.world.width // 2, 120))
        self.world.boss = boss
        self.world.all_sprites.add(boss)

        self.boss_spawned = True

    def _add_enemy(self, x, y):
        enemy = Enemy((x, y))
        self.world.enemies.add(enemy)
        self.world.all_sprites.add(enemy)
