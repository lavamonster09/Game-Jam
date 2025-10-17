import pygame
from entity import *

class Player(Entity):
    def __init__(self, app):
        super().__init__(app, "knight_placeholder" )       
        
        self.pos = pygame.Vector2(800, 450)
        self.health = 100
        self.xp = 0
        self.damage_cooldown = 30
        self.damage_counter = 0

        self.speed_modifier = 1.25 
        self.velocity = pygame.Vector2(0, 0)
        self.FRICTION_COEFF = 0.65
        self.MAX_VEL = 2

        self.keybinds = self.app.cfg

        self.attributes["collidable"] = True

    def get_input(self):
        key = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if key[self.keybinds.get_key_code("MOVE_UP")]:
            direction.y -= 1
        if key[self.keybinds.get_key_code("MOVE_DOWN")]:
            direction.y += 1
        if key[self.keybinds.get_key_code("MOVE_LEFT")]:
            direction.x -= 1
        if key[self.keybinds.get_key_code("MOVE_RIGHT")]:
            direction.x += 1

        self.velocity *= self.FRICTION_COEFF
        if direction.length() != 0 and self.velocity.length() < self.MAX_VEL:
            self.velocity += direction.normalize() * self.speed_modifier

        self.pos += self.velocity

    def update(self):
        super().update()
        self.get_input()
        if self.damage_counter != self.damage_cooldown:
            self.damage_counter += 1 

    def damage(self, damage):
        if self.damage_counter == self.damage_cooldown:
            self.damage_counter = 0 
            self.health -= damage
            print(self.health)
            if self.health <= 0:
                self.app.current_scene = "death"