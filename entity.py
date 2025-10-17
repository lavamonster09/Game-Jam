import pygame

class Entity:
    def __init__(self,app,sprite = "none"):
        self.children = [] 
        self.attributes = {"visible":True}
        self.sprite = sprite
        self.app = app
        self.pos = pygame.Vector2(0, 0)
        self.offset = pygame.Vector2(0,0)
        self.z_index = 0

    def update(self):
        for child in self.children:
            child.pos = pygame.Vector2(self.get_rect().center)
            child.update()

    def get_rect(self) -> pygame.Rect:
        if type(self.app.asset_loader.get(self.sprite)) == list:
            rect = self.app.asset_loader.get(self.sprite)[0].get_rect()
            rect.topleft = self.pos.xy + self.offset
        else:
            rect = self.app.asset_loader.get(self.sprite).get_rect()
            rect.topleft = self.pos.xy + self.offset
        return rect
    
    def get_screen_pos(self) -> pygame.Vector2:
        return self.pos 

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        sprite = self.app.asset_loader.get(self.sprite)
        if type(sprite) == list:
            sprite = sprite[0]
        screen_size = surface.get_size()
        self.offset = pygame.Vector2(screen_size)//2 - camera_pos
        if self.attributes.get("visible", False):
            surface.blit(sprite, self.pos.xy + self.offset)
            for child in self.children:
                child.draw(surface, camera_pos)
    
    def add_child(self, entity):
        self.children.append(entity)

    def remove_child(self, key):
        self.children.remove(key)