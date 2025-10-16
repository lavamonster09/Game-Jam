from entity import Entity
from player import Player
import pygame

class Enemy(Entity):
    def __init__(self,app, player):
        super().__init__(app)
        self.player = player
        self.pos = pygame.Vector2(0,0)
        self.speed = 2
        self.damage = 10

    def update(self):
        super().update()
        self.pos.move_towards_ip(self.player.pos, self.speed)

        if self.pos.distance_to(self.player.pos) <= 64:
            self.player.damage(self.damage)
