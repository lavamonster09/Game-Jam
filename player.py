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

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.pos.y -= 1
        if key[pygame.K_s]:
            self.pos.y += 1
        if key[pygame.K_a]:
            self.pos.x -= 1
        if key[pygame.K_d]:
            self.pos.x += 1

    def update(self):
        self.get_input()
        if self.damage_counter != self.damage_cooldown:
            self.damage_counter += 1 

    def damage(self, damage):
        if self.damage_counter == self.damage_cooldown:
            self.damage_counter = 0 
            self.health -= damage

            print(self.health)
        super().update()
        self.get_input()
