import pygame

class Entity:
    def __init__(self,app,sprite = "none"):
        self.children = {}
        self.attributes = {"visible":True}
        self.sprite = sprite
        self.app = app
        self.pos = pygame.Vector3(0, 0, 0)
        self.offset = pygame.Vector2(0,0)

    def update(self):
        for child in self.children:
            child.update()

    def get_rect(self) -> pygame.Rect:
        rect = self.app.asset_loader.get(self.sprite).get_rect()
        rect.topleft = self.pos.xy + self.offset
        return rect

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        sprite = self.app.asset_loader.get(self.sprite)
        screen_size = surface.get_size()
        self.offset = pygame.Vector2(screen_size)//2 - camera_pos
        if self.attributes.get("visible", False):
            surface.blit(sprite, self.pos.xy + self.offset)
            for child in self.children:
                child.draw(surface)
    
    def add_child(self, entity, key):
        self.children[key] = entity

    def remove_child(self, key):
        self.children.pop(key)