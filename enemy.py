from entity import Entity
from player import Player
import pygame

class Enemy(Entity):
    def __init__(self,app, player):
        super().__init__(app, sprite= "enemy_placeholder")
        self.player = player
        self.pos = pygame.Vector2(0,0)
        self.speed = 2
        self.MAX_VEL = 300 
        self.damage = 10
        self.velocity = pygame.Vector2(0,0)
        self.attributes["collidable"] = True
        self.attributes["player_damageable"] = True
        self.health = 5
        self.alive = True
        self.boss = False
        self.held_xp = 1

    def update(self):
        super().update()
        self.velocity *= 0.65
        self.velocity += (self.pos.move_towards(self.player.pos, self.speed) - self.pos).normalize()
        for entity in self.app.get_current_scene().enemy_manager.children:
            if self.pos.distance_to(entity.pos.xy) <= 64 and entity.attributes.get("collidable",False) and entity != self and(self.pos.move_towards(entity.pos, self.speed) - self.pos).magnitude() != 0:
                self.velocity -= 2 *(self.pos.move_towards(entity.pos, self.speed) - self.pos).normalize() 
        self.velocity = self.velocity.clamp_magnitude(self.MAX_VEL)
        self.pos += self.velocity
        if self.pos.distance_to(self.player.pos) <= 64 and self.player.attributes.get("damageable", False):
            self.player.damage(self.damage)

    def hurt(self, dmg:float, knockback: float):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.player.total_kills += 1
            self.attributes["visible"] = False
        self.velocity = -self.velocity * knockback