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
        self.font = self.app.asset_loader.fonts.get("JetBrainsMonoNL-Medium")
        self.hud_image = self.app.asset_loader.get("assets_hud")
        self.health_image = self.app.asset_loader.get("full_health")
        self.xp_image = self.app.asset_loader.get("full_XP")
        self.cursor_image = self.app.asset_loader.get("null")
        
        self.player = player
        self.pos = self.player.pos

        self.clock = self.app.clock

        self.HEALTH_TEXT_OFFSET = pygame.Vector2(64, 300)
        self.HEALTH_BAR_OFFSET = pygame.Vector2(33, 33)
        self.XP_OFFSET = pygame.Vector2(544, 32)

    def get_relative_pos(self, surface: pygame.Surface, camera_pos: pygame.Vector2) -> pygame.Vector2:
        relative_pos = self.player.pos - camera_pos
        return relative_pos
    
    def draw_fps(self, surface: pygame.Surface):
        self.fps_text = self.font.render(str(round(self.clock.get_fps())), True, '#00A494')
        self.fps_rect = self.fps_text.get_rect(topright = (1600, 0))
        surface.blit(self.fps_text, self.fps_rect)

    def draw_health(self, surface: pygame.Surface):
        self.health_text = self.font.render(str(self.player.health), True, '#00A494')
        self.health_rect = self.health_text.get_rect(center= (self.pos + self.HEALTH_TEXT_OFFSET))
        #self.health_image.fill((0, 0, 0, 0), (10, 10, 100, 100))
        surface.blit(self.health_image, self.get_health_pos())
        surface.blit(self.health_text, self.health_rect)

    def draw_xp(self, surface: pygame.Surface):
        percent_xp = self.player.xp / 100
        self.xp_rect = self.xp_image.get_rect(topleft = (self.pos + self.XP_OFFSET))
        surface.blit(self.xp_image, self.xp_rect)

    def draw_cursor(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect = self.cursor_image.get_rect(center= mouse_pos)
        surface.blit(self.cursor_image, self.cursor_rect)

    def get_health_pos(self) -> pygame.Vector2:
        percent_health_missing = 1 - self.player.health / 100
        img_height = self.health_image.get_height() - 64
        health_pos = self.pos + (0, img_height * percent_health_missing) + self.HEALTH_BAR_OFFSET
        return health_pos

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        self.pos = self.get_relative_pos(surface, camera_pos)
        self.draw_xp(surface)
        self.draw_health(surface)
        self.draw_cursor(surface)
        self.draw_fps(surface)
        surface.blit(self.hud_image, self.pos)