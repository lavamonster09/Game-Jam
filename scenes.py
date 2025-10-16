from scene import Scene
from entity import Entity
import pygame

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        test = Entity(self.app)
        test.pos = pygame.Vector2(800,450)
        self.add_entity(test, "test")
