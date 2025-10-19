from entity import Entity
from player import Player
from weapons import Projectile
import pygame
import random

class Enemy(Entity):
    def __init__(self, app, player):
        super().__init__(app, sprite= "enemy_placeholder")
        self.player = player
        self.pos = pygame.Vector2(0,0)
        self.speed = 2
        self.MAX_VEL = 300 
        self.damage = 10
        self.velocity = pygame.Vector2(0,0)
        self.attributes["collidable"] = True
        self.attributes["player_damageable"] = True
        self.attributes["ranged"] = False
        self.health = 5
        self.alive = True
        self.boss = False
        self.held_xp = 1
        self.ranged_timer = 0
        self.RANGED_TIMER_LIMIT = 60

    def check_children(self):
        kill_list = []
        for child in self.children:
            child.update()
            if not child.alive:
                kill_list.append(child)

        for child in kill_list:
            self.children.remove(child)

    def update(self):
        self.check_children()
        if self.attributes["ranged"]:
            if self.pos.distance_to(self.player.pos) > 400:
                self.velocity *= 0.65
                self.velocity += (self.pos.move_towards(self.player.pos, self.speed) - self.pos).normalize()
                for entity in self.app.get_current_scene().enemy_manager.children:
                    if self.pos.distance_to(entity.pos.xy) <= 64 and entity.attributes.get("collidable", False) and entity != self and(self.pos.move_towards(entity.pos, self.speed) - self.pos).magnitude() != 0:
                        self.velocity -= 2 *(self.pos.move_towards(entity.pos, self.speed) - self.pos).normalize() 
                self.velocity = self.velocity.clamp_magnitude(self.MAX_VEL)
                self.pos += self.velocity
            else:
                if self.ranged_timer >= self.RANGED_TIMER_LIMIT:
                    target_pos = self.player.pos - self.pos
                    new_proj = Projectile(self.app, "arrow_dex", self.pos, target_pos, 10, 5, 10, False)
                    for entity in self.app.get_current_scene().enemy_manager.children:
                        if self.pos.distance_to(entity.pos.xy) <= 64 and entity.attributes.get("collidable", False) and entity != self and(self.pos.move_towards(entity.pos, self.speed) - self.pos).magnitude() != 0:
                            self.velocity -= 2 *(self.pos.move_towards(entity.pos, self.speed) - self.pos).normalize() 
                    self.add_child(new_proj)
                    self.ranged_timer = 0
                else:
                    self.ranged_timer += 1
        else:
            self.velocity *= 0.65
            self.velocity += (self.pos.move_towards(self.player.pos, self.speed) - self.pos).normalize()
            for entity in self.app.get_current_scene().enemy_manager.children:
                if self.pos.distance_to(entity.pos.xy) <= 64 and entity.attributes.get("collidable", False) and entity != self and(self.pos.move_towards(entity.pos, self.speed) - self.pos).magnitude() != 0:
                    self.velocity -= 2 *(self.pos.move_towards(entity.pos, self.speed) - self.pos).normalize() 
            self.velocity = self.velocity.clamp_magnitude(self.MAX_VEL)
            self.pos += self.velocity
            if self.pos.distance_to(self.player.pos) <= 32 and self.player.attributes.get("damageable", False):
                self.player.damage(self.damage)

    def hurt(self, dmg:float, knockback: float):
        sound = random.choice(["hitHurt","hitHurt(1)","hitHurt(2)"])
        self.app.play_sound(sound,0.015)

        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            self.player.total_kills += 1
            self.attributes["visible"] = False
        self.velocity = -self.velocity * knockback