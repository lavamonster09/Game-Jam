import pygame

class Scene:
    def __init__(self, app):
        self.entities = [] 
        self.draw_queue = []
        self.app = app
        self.camera_pos = pygame.Vector2(app.screen.width // 2, app.screen.height // 2)
        self.cursor_image = self.app.asset_loader.get("CURSOR2")
        self.down_cursor = self.app.asset_loader.get("CURSOR2_down") 

    def draw_cursor(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect = self.cursor_image.get_rect(topleft= mouse_pos)
        if not pygame.mouse.get_pressed()[0]:
            surface.blit(self.cursor_image, self.cursor_rect)
        else:
            surface.blit(self.down_cursor ,self.cursor_rect)

    def draw(self, screen: pygame.Surface):
        self.entities.sort(key = lambda x: x.z_index)
        for entity in self.entities:
            entity.draw(screen, self.camera_pos)
        self.draw_cursor(screen)

    def update(self):
        for entity in self.entities:
            entity.update() 

    def add_entity(self, entity):
        self.entities.append(entity)