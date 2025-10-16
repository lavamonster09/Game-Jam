from scene import Scene
from entity import Entity
import pygame
from camera import Camera
from player import Player

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.test = Entity(self.app)
        self.test.pos = pygame.Vector2(0, 0)
        test2 = Entity(self.app)
        test2.pos = pygame.Vector2(64,64)
        self.player = Player(self.app)
        self.camera_pos = self.player.pos

        self.add_entity(self.test, "test")
        self.add_entity(test2, "test2")
        self.add_entity(self.player, "player")

    def update(self):
        super().update()
        self.test.pos.x += 1  