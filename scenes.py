from scene import Scene
from entity import Entity
import pygame
from camera import Camera

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.test = Entity(self.app)
        self.test.pos = pygame.Vector2(0, 0)
        test2 = Entity(self.app)
        test2.pos = pygame.Vector2(64,64)
        self.camera_pos = self.test.pos

        self.add_entity(self.test, "test")
        self.add_entity(test2, "test2")

    def update(self):
        super().update()
        self.test.pos.x += 1  