import pygame
from entity import *
import random
class Player(Entity):
    def __init__(self, app):
        super().__init__(app, "sheet_2_knight_placeholder") 
        self.pos = pygame.Vector2(0, 0)
        self.health = 100
        self.max_health = 100
        self.xp = 0
        self.max_xp = 100
        self.max_health = 100
        self.total_kills = 0
        self.dead = False

        self.damage_cooldown = 30
        self.damage_counter = 0

        self.roll_cooldown = 80 
        self.roll_length = 20 
        self.roll_counter = self.roll_cooldown 
        self.roll_strength = 20 

        self.speed_modifier = 1.25 
        self.velocity = pygame.Vector2(0, 0)
        self.FRICTION_COEFF = 0.65
        self.ROLLNG_COEFF = 0.95
        self.friction_coeff = self.FRICTION_COEFF
        self.MAX_VEL = 4
        
        self.state = "idle"

        self.keybinds = self.app.cfg

        self.total_level = 0

        self.levels = {
            "Strength": 0,
            "Dexterity": 0,
            "Vigor": 0,
            "Endurance": 0,
        }
        
        self.attributes["collidable"] = True
        self.attributes["damageable"] = True

    def get_input(self):
        key = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if self.state != "rolling":
            if key[self.keybinds.get_key_code("MOVE_UP")]:
                direction.y -= 1
                self.state = "moveing"
            if key[self.keybinds.get_key_code("MOVE_DOWN")]:
                direction.y += 1
                self.state = "moveing"
            if key[self.keybinds.get_key_code("MOVE_LEFT")]:
                direction.x -= 1
                self.state = "moveing"
            if key[self.keybinds.get_key_code("MOVE_RIGHT")]:
                direction.x += 1
                self.state = "moveing"

        self.velocity *= self.friction_coeff
        if direction.length() != 0 and self.velocity.length() < self.MAX_VEL:
            self.velocity += direction.normalize() * self.speed_modifier

        if key[self.keybinds.get_key_code("DODGE")] and self.roll_cooldown == self.roll_counter and direction.length() != 0:
            self.state = "rolling"
            self.roll_counter = 0 
            self.velocity = direction.normalize() * self.roll_strength
            self.friction_coeff= self.ROLLNG_COEFF
        if self.roll_counter <= self.roll_length:
            self.state = "rolling"
            self.attributes["collidable"] = False
            self.attributes["damageable"] = False
        else:
            self.state = "moveing"
            self.attributes["collidable"] = True
            self.attributes["damageable"] = True
            self.friction_coeff = self.FRICTION_COEFF


        self.pos += self.velocity

    def level_up(self, stat):
        self.total_level += 1
        self.levels[stat] += 1

        if stat == "Vigor":
            self.max_health += 10
            self.health += 10
        if stat == "Endurance":
            self.speed_modifier += 0.15

        if self.health + 20 <= self.max_health:
            self.health += 20
        self.max_xp += 20
        self.xp = 0

    def update(self):
        super().update()
        self.get_input()
        if self.damage_counter != self.damage_cooldown:
            self.damage_counter += 1 
        if self.roll_counter != self.roll_cooldown:
            self.roll_counter += 1 

    def damage(self, damage):
        if self.damage_counter == self.damage_cooldown:
            self.damage_counter = 0 
            self.health -= damage
            self.app.play_sound(random.choice(["Hurt (1)","Hurt (2)","Hurt (3)"]), 0.03)
            if self.health <= 0:
                self.app.paused = True
                self.dead = True

    def draw(self, surface, camera_pos):
        if self.state == "rolling":
            sheet_index = 1
        else:
            sheet_index = 0
        super().draw(surface, camera_pos, sheet_index)
        # sprite = self.app.asset_loader.get(self.sprite)
        # screen_size = surface.get_size()
        #self.offset = pygame.Vector2(screen_size)//2 - camera_pos
        # if self.attributes.get("visible", False):
        #     surface.blit(self.sprite, self.pos.xy + self.offset)
        #     for child in self.children:
        #         child.draw(surface, camera_pos)