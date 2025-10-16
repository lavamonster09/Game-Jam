import pygame

class Scene:
    def __init__(self):
        self.entities = {}
        self.draw_queue = []

    def draw(self, screen: pygame.Surface):
        for entity in self.entities:
            self.entities[entity].draw(screen)

    def update(self):
        for entity in self.entities:
            self.entities[entity].update() 

    def add_entity(self, entity, name):
        self.entities[name] = entity