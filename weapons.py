import pygame
import math
from entity import Entity

class MeleeWeapon(Entity):
    def __init__(self, app, sprite, range: float, damage: float, attack_time: float, knockback: float, str_scaling: float, dex_scaling: float):
        super().__init__(app)
        self.sprite = sprite
        self.range = range
        self.damage = damage
        self.attack_time = attack_time
        self.attack_counter = attack_time
        self.damage_rect = app.asset_loader.get(self.sprite)[0].get_rect()
        self.knockback = knockback
        self.attributes["visible"] = False
        self.attributes["is_ranged"] = False
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
        self.player = self.app.get_current_scene().player
        if self.attack_time != self.attack_counter:
            self.attack_counter += 1
            if self.attack_counter == self.attack_time//2:
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
                self.attack_counter = 0 
                self.rect = self.get_rect()
                self.attack_angle = pygame.Vector2(0,1).angle_to(pygame.mouse.get_pos() - self.get_screen_pos())

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
        super().draw(surface, camera_pos)

    def get_rect(self):
        dir = pygame.mouse.get_pos() - self.get_screen_pos()
        if dir.length() == 0:
            dir = pygame.Vector2(0, 1)
        dir = dir.normalize()
        if self.damage_rect:
            rect = self.damage_rect
        else:
            rect = pygame.Rect(0,0,0,0)
        rect.center = self.pos + dir * self.range * 10
        return rect

class RangedWeapon(Entity):
    def __init__(self, app, sprite, range: float, damage: float, attack_time: float, knockback: float, str_scaling: float, dex_scaling: float):
        super().__init__(app)
        self.sprite = sprite
        self.range = range
        self.damage = damage
        self.attack_time = attack_time
        self.attack_counter = attack_time
        self.damage_rect = app.asset_loader.get(self.sprite)[0].get_rect()
        self.knockback = knockback
        self.attributes["visible"] = False
        self.attributes["is_ranged"] = True
        self.attack_angle = 0
        self.str_mul = 0
        self.dex_mul = 0
        self.draw_speed = 20 / attack_time
        self.draw_timer = 10

        self.DAMAGE_MUL = 0.5
        self.MAX_DRAW = 30
        self.MAX_PROJ_SPEED = 10

        self.scaling = {
            "Strength": str_scaling,
            "Dexterity": dex_scaling,
        }

    def update(self):        
        kill_list = []
        if self.attack_time != self.attack_counter:
            self.attack_counter += 1
        else:
            if pygame.mouse.get_pressed()[0] and self.draw_timer < self.MAX_DRAW:
                self.draw_timer += self.draw_speed
                if self.draw_timer > self.MAX_DRAW:
                    self.draw_timer = self.MAX_DRAW
            if pygame.mouse.get_just_released()[0]:
                self.attack_counter = 0
                self.make_projectile()
        for child in self.children:
            child.update()
            if not child.alive:
                kill_list.append(child)
        for child in kill_list:
            self.children.remove(child)

    def draw(self, surface, camera_pos):
        super().draw(surface, camera_pos)

    def make_projectile(self):
        self.player = self.get_parent()
        if self.player.levels["Strength"] != 0:
            self.str_mul = math.log(self.player.levels["Strength"], 4) + 1
        if self.player.levels["Dexterity"] != 0:
            self.dex_mul = math.log(self.player.levels["Dexterity"], 4) + 1
        str_dmg = self.scaling["Strength"] * self.str_mul * self.DAMAGE_MUL
        dex_dmg = self.scaling["Dexterity"] * self.dex_mul * self.DAMAGE_MUL
        damage_scaled = round(self.damage + str_dmg + dex_dmg, 2) * self.draw_timer / self.MAX_DRAW
        target_pos = pygame.mouse.get_pos() - self.get_screen_pos()
        proj_speed = self.MAX_PROJ_SPEED * self.draw_timer / self.MAX_DRAW
        knockback = self.knockback * self.draw_timer / self.MAX_DRAW
        proj = Projectile(self.app, self.player.pos, target_pos, knockback, damage_scaled, proj_speed, True)
        self.add_child(proj)
        self.draw_timer = 10
    
class Projectile(Entity):
    def __init__(self, app, pos: pygame.Vector2, target_pos: pygame.Vector2, knockback: float, damage: float, speed: float, friendly: bool):
        super().__init__(app, sprite= "")
        self.attributes["friendly"] = friendly
        self.target_pos = pygame.Vector2(target_pos)
        self.pos = pygame.Vector2(pos)
        self.damage = damage
        self.knockback = knockback
        self.player = self.app.get_current_scene().player
        self.speed = speed
        self.alive = True
        self.alive_timer = 0
        self.targets_pierced = []

        self.MAX_PIERCE = 5
        self.SLOW_DOWN_POINT = speed * 12

    def get_dir(self) -> pygame.Vector2:
        dir = self.target_pos
        if dir.length() == 0:
            dir = pygame.Vector2(0, 1)
        dir = dir.normalize()
        return dir

    def move_to_target(self):
        self.dir = self.get_dir()
        self.pos += self.dir * self.speed

    def check_collisions(self):
        if self.attributes["friendly"]:
            for entity in self.app.get_current_scene().enemy_manager.children:
                if self.get_rect().colliderect(entity.get_rect()) and entity.attributes.get("player_damageable", False) and not entity in self.targets_pierced: 
                    entity.hurt(self.damage, self.knockback)
                    self.targets_pierced.append(entity)
                    if len(self.targets_pierced) >= self.MAX_PIERCE:
                        self.alive = False
        else:
            if self.get_rect().colliderect(self.player.get_rect()) and self.player.attributes.get("damageable", True): 
                self.player.damage(self.damage)
                self.alive = False
            
    def update_speed(self):
        self.alive_timer += 1
        if self.alive_timer >= self.SLOW_DOWN_POINT:
            self.speed *= 0.95
        if self.speed <= 1:
            self.alive = False

    def update(self):
        self.update_speed()
        self.check_collisions()
        self.move_to_target()