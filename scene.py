import pygame

class Scene:
    def __init__(self, app):
        self.entities = {}
        self.draw_queue = []
        self.app = app
        self.camera_pos = pygame.Vector2(0,0)

    def draw(self, screen: pygame.Surface):
        for entity in self.entities:
            self.entities[entity].draw(screen, self.camera_pos)

    def update(self):
        for entity in self.entities:
            self.entities[entity].update() 

    def add_entity(self, entity, name):
        self.entities[name] = entity