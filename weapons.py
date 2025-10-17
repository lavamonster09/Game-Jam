import pygame
import math
from entity import Entity

class BaseWeapon(Entity):
    def __init__(self, app, range: int, damage: int):
        super().__init__(app)
        self.range = range
        self.damage = damage

    # def attack(self, surface: pygame.Surface, rel_mouse_pos: pygame.Vector2, player_pos: pygame.Vector2):
    #     angle_to_mouse = math.atan2(rel_mouse_pos.y, rel_mouse_pos.x)
    #     start_angle = angle_to_mouse + math.pi / 3
    #     stop_angle = angle_to_mouse - math.pi / 3
    #     pygame.draw.arc(surface, '#FFFFFF', pygame.Rect(player_pos, (self.range, self.range)), start_angle, stop_angle, self.range)

    # def draw(self, surface: pygame.Surface, camera_pos: pygame.Vector2):
    #     sprite = self.app.asset_loader.get(self.sprite)
    #     screen_size = surface.get_size()
    #     self.offset = pygame.Vector2(screen_size)//2 - camera_pos
    #     pygame.draw.arc(surface, '#FFFFFF', pygame.Rect(player_pos, (self.range, self.range)), start_angle, stop_angle, self.range)
    #     if self.visible:
    #         for child in self.children:
    #             child.draw(surface)