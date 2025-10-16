import pygame
from entity import *

class Player(Entity):
    def __init__(self, app):
        super().__init__(app)
        self.pos = pygame.Vector2(800, 450)
        self.sprite = "knight_placeholder"
        self.health = 100

    def get_input(self):
        key_down = pygame.key.get_pressed()

        if key_down[pygame.K_w]:
            self.pos.y -= 1
        if key_down[pygame.K_s]:
            self.pos.y += 1
        if key_down[pygame.K_a]:
            self.pos.x -= 1
        if key_down[pygame.K_d]:
            self.pos.x += 1

    def update(self):
        self.get_input()