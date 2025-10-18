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
        self.time = 0
        self.wave_cleared = False
        self.attributes["visible"] = False 
        self.SPAWN_DIST = 900

    def spawn_wave(self):
        count = 0
        while count != self.rounds + 10:
            self.spawn_enemy()
            count += 1

    def spawn_enemy(self):
        enemy = Enemy(self.app, self.player)
        rnd_dir = random.randrange(0, 360)
        enemy.pos = self.player.pos + pygame.Vector2(1,0).rotate(rnd_dir) * self.SPAWN_DIST

        self.add_child(enemy)

    def check_children(self):
        kill_list = []
        for child in self.children:
            if not child.alive:
                kill_list.append(child)

        for i in kill_list:
            xp = Xp(self.app, self.player)
            xp.pos = i.pos
            self.app.get_current_scene().add_entity(xp)
            self.remove_child(i)

        if len(self.children) == 0:
            self.wave_cleared = True
        
    def update(self):
        for child in self.children:
            child.update()
        if self.wave_cleared:
            self.spawn_wave()
            self.rounds += 1
            self.wave_cleared = False
        else:
            self.check_children()