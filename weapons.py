import pygame
import math
from entity import Entity

class MeleeWeapon(Entity):
    def __init__(self, app, sprite, range: int, damage: int, attack_time: int, knockback: float, str_scaling: int, dex_scaling: int):
        super().__init__(app)
        self.sprite = sprite
        self.range = range
        self.damage = damage
        self.attack_time = attack_time
        self.attack_counter = attack_time
        self.damage_rect = app.asset_loader.get(self.sprite)[0].get_rect()
        self.knockback = knockback
        self.attributes["visible"] = False
        self.attack_angle = 0
        self.rect = pygame.Rect()
        self.str_mul = 0
        self.dex_mul = 0

        self.DAMAGE_MUL = 0.5

        self.scaling = {
            "Strength": str_scaling,
            "Dexterity": dex_scaling,
        }

    def update(self):        
        super().update()
        if self.attack_time != self.attack_counter:
            self.attack_counter += 1
            if self.attack_counter == self.attack_time//2:
                self.player = self.get_parent()
                if self.player.levels["Strength"] != 0:
                    self.str_mul = math.log(self.player.levels["Strength"], 4) + 1
                if self.player.levels["Dexterity"] != 0:
                    self.dex_mul = math.log(self.player.levels["Dexterity"], 4) + 1
                str_dmg = self.scaling["Strength"] * self.str_mul * self.DAMAGE_MUL
                dex_dmg = self.scaling["Dexterity"] * self.dex_mul * self.DAMAGE_MUL
                damage_scaled = round(self.damage + str_dmg + dex_dmg, 2)
                for entity in self.app.get_current_scene().enemy_manager.children:
                    if self.rect.colliderect(entity.get_rect()) and entity.attributes.get("player_damageable", False): 
                        entity.hurt(damage_scaled, self.knockback)

        else:
            if pygame.mouse.get_just_pressed()[0]:
                self.attack()
                self.rect = self.get_rect()
                self.attack_angle = pygame.Vector2(0,1).angle_to(pygame.mouse.get_pos() - self.get_screen_pos())

    def attack(self):
        self.attack_counter = 0 

    def draw(self, surface, camera_pos):
        if self.attack_counter < self.attack_time:
            if self.attack_counter:
                i = self.attack_counter // (self.attack_time // (len(self.app.asset_loader.get(self.sprite))) + 1 )
                frame = self.app.asset_loader.get(self.sprite)[i]
                frame = pygame.transform.rotate(frame, self.attack_angle)
                frame = pygame.transform.flip(frame, False, True)
                surface.blit(frame, self.rect.topleft)
                self.damage_rect = frame.get_rect() 
            if self.attack_counter == self.attack_time // 2:
                pass
                #pygame.draw.rect(surface, (255,255,255), self.rect, 1)
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
