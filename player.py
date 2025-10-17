import pygame
from entity import *

class Player(Entity):
    def __init__(self, app):
        super().__init__(app, "knight_placeholder")       
        
        self.pos = pygame.Vector2(800, 450)
        self.health = 100
        self.xp = 0

        self.damage_cooldown = 30
        self.damage_counter = 0

        self.roll_cooldown = 80 
        self.roll_length = 20 
        self.roll_counter = self.roll_cooldown 
        self.roll_strenth = 20 

        self.speed_modifier = 1.25 
        self.velocity = pygame.Vector2(0, 0)
        self.FRICTION_COEFF = 0.65
        self.ROLLNG_COEFF = 0.95
        self.friction_coeff = self.FRICTION_COEFF
        self.MAX_VEL = 2

        
        self.state = "idle"

        self.keybinds = self.app.cfg

        self.attributes["collidable"] = True
        self.attributes["damageable"] = True

    def get_input(self):
        key = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if self.state != "rolling":
            if key[self.keybinds.get_key_code("MOVE_UP")]:
                direction.y -= 1
                self.state = "moveing"
            if key[self.keybinds.get_key_code("MOVE_DOWN")]:
                direction.y += 1
                self.state = "moveing"
            if key[self.keybinds.get_key_code("MOVE_LEFT")]:
                direction.x -= 1
                self.state = "moveing"
            if key[self.keybinds.get_key_code("MOVE_RIGHT")]:
                direction.x += 1
                self.state = "moveing"

        self.velocity *= self.friction_coeff
        if direction.length() != 0 and self.velocity.length() < self.MAX_VEL:
            self.velocity += direction.normalize() * self.speed_modifier

        if key[self.keybinds.get_key_code("DODGE")] and self.roll_cooldown == self.roll_counter:
            self.state = "rolling"
            self.roll_counter = 0 
            self.velocity = direction.normalize() * self.roll_strenth
            self.friction_coeff= self.ROLLNG_COEFF
        if self.roll_counter <= self.roll_length:
            self.state = "rolling"
            self.attributes["collidable"] = False
            self.attributes["damageable"] = False
        else:
            self.state = "moveing"
            self.attributes["collidable"] = True
            self.attributes["damageable"] = True
            self.friction_coeff = self.FRICTION_COEFF


        self.pos += self.velocity

    def update(self):
        super().update()
        self.get_input()
        if self.damage_counter != self.damage_cooldown:
            self.damage_counter += 1 
        if self.roll_counter != self.roll_cooldown:
            self.roll_counter += 1 

    def damage(self, damage):
        if self.damage_counter == self.damage_cooldown:
            self.damage_counter = 0 
            self.health -= damage
            print(self.health)
            if self.health <= 0:
                self.app.current_scene = "death"