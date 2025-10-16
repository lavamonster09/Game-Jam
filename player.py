import pygame
from entity import *

class Player(Entity):
    def __init__(self, app):
        super().__init__(app)
        self.pos = pygame.Vector2(800, 450)
        self.sprite = "knight_placeholder"
        
        self.health = 100
        self.damage_cooldown = 30
        self.damage_counter = 0

        self.speed_modifier = 3
        self.velocity = pygame.Vector2(0, 0)
        self.FRICTION_COEFF = 0.65
        self.MAX_VEL = 10

    def get_input(self):
        key = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if key[pygame.K_w]:
            direction.y -= 1
        if key[pygame.K_s]:
            direction.y += 1
        if key[pygame.K_a]:
            direction.x -= 1
        if key[pygame.K_d]:
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