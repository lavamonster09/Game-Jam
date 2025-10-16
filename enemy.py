from entity import Entity
from player import Player
import pygame

class Enemy(Entity):
    def __init__(self,app, player):
        super().__init__(app, sprite= "enemy_placeholder")
        self.player = player
        self.pos = pygame.Vector2(0,0)
        self.speed = 2
        self.MAX_VEL = 3 
        self.damage = 10
        self.velocity = pygame.Vector2(0,0)
        self.attributes["collidable"] = True

    def update(self):
        super().update()
        self.velocity += (self.pos.move_towards(self.player.pos, self.speed) - self.pos).normalize()
        for entity in self.app.get_current_scene().entities:
            if self.pos.distance_to(entity.pos.xy) <= 64 and entity.attributes.get("collidable",False) and entity != self:
                self.velocity -= 2 *(self.pos.move_towards(entity.pos, self.speed) - self.pos).normalize() 
        self.velocity = self.velocity.clamp_magnitude(self.MAX_VEL)
        self.pos += self.velocity
        if self.pos.distance_to(self.player.pos) <= 64:
            self.player.damage(self.damage)