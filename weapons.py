import pygame
import math
from entity import Entity

class MeleWeapon(Entity):
    def __init__(self, app, range: int, damage: int):
        super().__init__(app)
        self.range = range
        self.damage = damage
        self.attack_time = 30
        self.attack_counter = 30
        self. damage_rect = None
    def update(self):        
        super().update()
        if self.attack_time != self.attack_counter:
            self.attack_counter += 1
        else:
            if pygame.mouse.get_just_pressed()[0]:
                self.attack()

    def attack(self):
        print("attack")
        self.attack_counter = 0 
        for entity in self.app.get_current_scene().entities :
            self.rect = self.get_rect()
            if self.get_rect().colliderect(entity.get_rect()) and entity.attributes.get("damageable", False): 
                entity.damage(1)

    def draw(self, surface, camera_pos):
        if self.attack_counter < self.attack_time:
            pygame.draw.rect(surface, (255,255,255), self.rect)
        return super().draw(surface, camera_pos)

    def get_rect(self):
        rect = super().get_rect()
        dir = pygame.Vector2(pygame.mouse.get_pos()[0] / self.app.width * 2 - 1, pygame.mouse.get_pos()[1] / self.app.height * 2 - 1)
        print(dir) 
        rect.center = self.pos + dir * 100
        return rect