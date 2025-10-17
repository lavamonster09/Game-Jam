from entity import Entity
from enemy import Enemy
import pygame

class Button(Entity):
    def __init__(self, app, on_click , sprite="none"):
        super().__init__(app, sprite)
        self.on_click = on_click
        
    def update(self):
        super().update()
        if self.get_rect().collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_just_pressed()[0]:
                self.on_click()

class HUD(Entity):
    def __init__(self, app, player):
        super().__init__(app, sprite="")
        self.player = player
        self.pos = self.player.pos
        self.font = self.app.asset_loader.fonts.get("JetBrainsMonoNL-Medium")
        self.hud_image = self.app.asset_loader.get("assets_hud")
        self.HEALTH_OFFSET = pygame.Vector2(64, 300)

    def get_relative_pos(self, surface: pygame.Surface, camera_pos: pygame.Vector2) -> pygame.Vector2:
        relative_pos = self.player.pos - camera_pos
        return relative_pos

    def draw_health(self, surface: pygame.Surface):
        self.health_text = self.font.render(str(self.player.health), True, color= '#00A494')
        self.health_rect = self.health_text.get_rect(center= (self.pos + self.HEALTH_OFFSET))
        surface.blit(self.health_text, self.health_rect)

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        self.pos = self.get_relative_pos(surface, camera_pos)
        self.draw_health(surface)
        surface.blit(self.hud_image, self.pos)