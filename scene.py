import pygame

class Scene:
    def __init__(self, app):
        self.entities = [] 
        self.draw_queue = []
        self.app = app
        self.camera_pos = pygame.Vector2(app.screen.width//2,app.screen.height//2)

    def draw(self, screen: pygame.Surface):
        self.entities.sort(key = lambda x: x.z_index)
        for entity in self.entities:
            entity.draw(screen, self.camera_pos)

    def update(self):
        for entity in self.entities:
            entity.update() 

    def add_entity(self, entity):
        self.entities.append(entity)