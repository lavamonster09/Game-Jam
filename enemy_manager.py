import pygame
import random
from entity import Entity
from enemy import Enemy
from xp import Xp

class EnemyManager(Entity):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player
        self.rounds = 0
        self.time = 600
        self.wave_cleared = False
        self.boss_round = False
        self.boss_dead = False
        self.attributes["visible"] = False
        self.health_mul = 1

        self.ROUND_TIMER = 600
        self.SPAWN_DIST = 1000
        self.BOSS_INTERVAL = 5

    def spawn_wave(self):
        self.spawn_enemy(True)
        count = 0
        if self.rounds > 5:
            while count != self.rounds - 5:
                print("spawned ranged")
                count += 1                
        while count != self.rounds + 10:
            self.spawn_enemy(False)
            count += 1

        if self.rounds % self.BOSS_INTERVAL == 0 and self.rounds > 0:
            self.boss_round = True

    def spawn_enemy(self, ranged: bool):
        enemy = Enemy(self.app, self.player)
        enemy.health *= self.health_mul
        rnd_dir = random.randrange(0, 360)
        enemy.pos = self.player.pos + pygame.Vector2(1, 0).rotate(rnd_dir) * self.SPAWN_DIST
        if ranged:
            enemy.attributes["ranged"] = True
        self.add_child(enemy)

    def spawn_boss(self):
        boss = Enemy(self.app, self.player)
        boss.boss = True
        boss.health *= 3 * self.health_mul
        boss.damage *= 2
        boss.held_xp = 10
        boss.pos = self.player.pos + pygame.Vector2(0, -1) * self.SPAWN_DIST

        self.add_child(boss)

    def check_children(self):
        self.time += 1
        kill_list = []
        for child in self.children:
            if not child.alive:
                if child.boss:
                    self.boss_dead = True
                    self.boss_round = False
                kill_list.append(child)

        for i in kill_list:            
            self.spawn_xp(i.held_xp, i.pos)
            self.remove_child(i)

        if self.time >= self.ROUND_TIMER:
            self.time = 0
            if self.boss_dead or not self.boss_round:
                self.wave_cleared = True
                self.boss_dead = False
            else:
                self.spawn_boss()
                self.health_mul += 0.5

    def spawn_xp(self, count: int, pos: pygame.Vector2):
        for i in range(count):
            xp = Xp(self.app, self.player)
            xp.pos = pos + (random.randint(-16, 16), random.randint(-16, 16))
            self.app.get_current_scene().add_entity(xp)
        
    def update(self):
        for child in self.children:
            child.update()
        if self.wave_cleared:
            self.spawn_wave()
            self.rounds += 1
            self.wave_cleared = False
        else:
            self.check_children()