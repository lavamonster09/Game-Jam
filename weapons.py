import pygame
import math
from entity import Entity

class MeleeWeapon(Entity):
    def __init__(self, app, range: int, damage: int, attack_time: int, knockback: float):
        super().__init__(app)
        self.range = range
        self.damage = damage
        self.attack_time = attack_time
        self.attack_counter = attack_time
        self.damage_rect = None
        self.knockback = knockback
        self.attributes["visible"] = False
    def update(self):        
        super().update()
        if self.attack_time != self.attack_counter:
            self.attack_counter += 1
        else:
            if pygame.mouse.get_just_pressed()[0]:
                self.attack()

    def attack(self):
        self.attack_counter = 0 
        for entity in self.app.get_current_scene().entities :
            self.rect = self.get_rect()
            if self.rect.colliderect(entity.get_rect()) and entity.attributes.get("damageable", False): 
                entity.hurt(self.damage, self.knockback)

    def draw(self, surface, camera_pos):
        if self.attack_counter < self.attack_time:
            pygame.draw.rect(surface, (255,255,255), self.rect)
        return super().draw(surface, camera_pos)

    def get_rect(self):
        dir = pygame.mouse.get_pos() - self.get_screen_pos()
        dir = dir.normalize()
        if self.damage_rect:
            rect = self.damage_rect
        else:
            rect = pygame.Rect(0,0,0,0)
        rect.center = self.pos + dir * 100
        return rect


