from scene import Scene
from entity import Entity
import pygame
from camera import Camera
from player import Player
from enemy import Enemy

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.test = Entity(self.app)
        self.test.pos = pygame.Vector2(0, 0)
        test2 = Entity(self.app)
        test2.pos = pygame.Vector2(64,64)
        self.player = Player(self.app)
        self.target_camera_pos = self.player.pos
        self.camera_pos = self.player.pos
        enemy = Enemy(app, self.player)
        self.add_entity(enemy, "enemy")
        self.add_entity(self.test, "test")
        self.add_entity(test2, "test2")
        self.add_entity(self.player, "player")

    def update(self):
        super().update()
        self.camera_pos = self.target_camera_pos.slerp(self.camera_pos, 0.2)
        self.test.pos.x += 1  