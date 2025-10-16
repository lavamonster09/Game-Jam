import pygame

class Entity:
    def __init__(self,app,sprite = "none"):
        self.children = {}
        self.visible = False
        self.sprite = sprite
        self.app = app
        self.pos = pygame.Vector3(0, 0, 0)

    def update(self):
        for child in self.children:
            child.update()

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        sprite = self.app.asset_loader.get(self.sprite)
        screen_size = surface.get_size()
        surface.blit(sprite, self.pos.xy + pygame.Vector2(screen_size)//2 - camera_pos)
        if self.visible:
            for child in self.children:
                child.draw(surface)
    
    def add_child(self, entity, key):
        self.children[key] = entity

    def remove_child(self, key):
        self.children.pop(key)