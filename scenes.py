from scene import Scene
from entity import Entity
import pygame
from camera import Camera

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        test = Entity(self.app)
        test.pos = pygame.Vector2(0, 0)
        test2 = Entity(self.app)
        test2.pos = pygame.Vector2(64,64)
        self.camera_pos = test.pos

        self.add_entity(test, "test")
        self.add_entity(test2, "test2")
