import pygame

class Entity:
    def __init__(self,app,sprite = "none"):
        self.children = {}
        self.visible = False
        self.sprite = sprite
        self.app = app
        self.pos = pygame.Vector3(0, 0, 0)
        self.offset = pygame.Vector2(0, 0) 

    def update(self):
        for child in self.children:
            child.update()

    def draw(self, surface: pygame.Surface):
        sprite = self.app.asset_loader.get(self.sprite)
        surface.blit(sprite, self.pos.xy + self.offset - pygame.Vector2(sprite.width // 2, sprite.height // 2))
        if self.visible:
            for child in self.children:
                child.draw(surface)
    
    def add_child(self, entity, key):
        self.children[key] = entity

    def remove_child(self, key):
        self.children.pop(key)