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

        cutout_mask = pygame.mask.from_surface(self.health_image)
        self.cutout_image = cutout_mask.to_surface()
        self.cutout_image.set_colorkey('#FFFFFF')
        
        self.player = player
        self.previous_health = 0
        self.previous_xp = -1
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
        if self.previous_health != self.player.health:
            self.health_pos = self.get_missing_health()
            self.cutout_health()

        self.health_text = self.font.render(str(self.player.health), True, '#00A494')
        self.health_rect = self.health_text.get_rect(center= (self.pos + self.HEALTH_TEXT_OFFSET))

        surface.blit(self.new_health_image, self.pos + self.health_pos + self.HEALTH_BAR_OFFSET)
        surface.blit(self.health_text, self.health_rect)

        self.previous_health = self.player.health

    def draw_xp(self, surface: pygame.Surface):
        if self.previous_xp != self.player.xp:
            self.cutout_xp()

        surface.blit(self.new_xp_image, self.new_xp_image.get_rect(topleft = (self.pos + self.XP_OFFSET)))

        self.previous_xp = self.player.xp

    def draw_cursor(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect = self.cursor_image.get_rect(center= mouse_pos)
        surface.blit(self.cursor_image, self.cursor_rect)

    def cutout_health(self):
        size = self.health_image.size
        rect_size = (size[0], self.health_pos.y)
        rect_cutout = pygame.Surface(rect_size)
        rect_cutout.fill('#000000')
        self.new_health_image = self.health_image.copy()
        self.new_health_image.blit(self.cutout_image, self.cutout_image.get_rect(topleft= -self.health_pos))
        self.new_health_image.blit(rect_cutout, rect_cutout.get_rect(bottomright= size))
        self.new_health_image.set_colorkey('#000000')

    def cutout_xp(self):
        bar_size = self.xp_image.get_size()
        percent_missing_xp = 1 - self.player.xp / self.player.max_xp
        cutout_size = (bar_size[0] * percent_missing_xp, bar_size[1])
        print(cutout_size)
        cutout_surf = pygame.Surface(cutout_size)
        cutout_surf.fill('#000000')
        self.new_xp_image = self.xp_image.copy()
        self.new_xp_image.blit(cutout_surf, cutout_surf.get_rect(bottomright= bar_size))
        self.new_xp_image.set_colorkey('#000000')


    def get_missing_health(self) -> pygame.Vector2:
        percent_health_missing = 1 - self.player.health / 100
        img_height = self.health_image.get_height() - 64
        health_pos = pygame.Vector2(0, img_height * percent_health_missing)
        return health_pos

    def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
        self.pos = self.get_relative_pos(surface, camera_pos)
        self.draw_xp(surface)
        self.draw_health(surface)
        self.draw_cursor(surface)
        self.draw_fps(surface)
        surface.blit(self.hud_image, self.pos)