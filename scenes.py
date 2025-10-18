from scene import Scene
from entity import Entity
import pygame
from player import Player
from enemy import Enemy
from enemy_manager import EnemyManager
from weapons import MeleeWeapon
from xp import Xp
from ui import * 
import random

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.player = Player(self.app)
        self.enemy_manager = EnemyManager(self.app, self.player)
        self.target_camera_pos = self.player.pos
        self.camera_pos = self.player.pos
        self.hud = HUD(self.app, self.player)
        self.hud.z_index = 1000000

        weapon = MeleeWeapon(self.app,"sheet_6_katana_slash", 1, 2, 20, 10, 3, 1)
        self.player.add_child(weapon)

        #btn1 = Button(app, self.spawn_enemy, sprite="spawn_enemy_button") 
        self.add_entity(self.enemy_manager)
        #self.add_entity(btn1)
        self.add_entity(self.player)
        self.add_entity(self.hud)

    def update(self):
        if self.app.paused:
            self.hud.update()
        else:
            super().update()
            self.camera_pos = self.target_camera_pos.smoothstep(self.camera_pos, 0.65)
            
    def spawn_enemy(self):
        enemy = Enemy(self.app, self.player)
        rnd_dir = random.randrange(0, 360)
        enemy.pos = self.player.pos + pygame.Vector2(1,0).rotate(rnd_dir) * 900
        xp = Xp(self.app, self.player)
        xp.pos = self.player.pos + pygame.Vector2(1,0).rotate(rnd_dir) * 900
        #self.add_entity(enemy)
        self.add_entity(xp)

    def draw(self, screen):
        grass = self.app.asset_loader.get("grass_background")
        offsets = [
            (0,0),
            (0,1),
            (0,-1),
            (1,0),
            (1,1),
            (1,-1),
            (-1,1),
            (-1,0),
            (-1,-1)
        ]
        for offset in offsets:
            screen.blit(grass, ((offset[0] + self.player.pos.x // self.app.width) * self.app.width - self.camera_pos.x, (offset[1] + self.player.pos.y // self.app.height) * self.app.height - self.camera_pos.y))
        return super().draw(screen)

class WeaponSelectScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.weapons = {
            "Dex Melee": MeleeWeapon(self.app,"sheet_6_katana_slash", 1, 1.5, 20, 10, 1, 3),
            "Qua Melee": MeleeWeapon(self.app,"sheet_6_katana_slash", 1.5, 2, 15, 15, 2, 2),
            "Str Melee": MeleeWeapon(self.app,"sheet_6_katana_slash", 2, 2.5, 10, 20, 1, 3),
            "Dex Ranged": MeleeWeapon(self.app,"sheet_6_katana_slash", 1, 2, 20, 10, 1, 3),
            "Qua Ranged": MeleeWeapon(self.app,"sheet_6_katana_slash", 1, 2, 20, 10, 2, 2),
            "Str Ranged": MeleeWeapon(self.app,"sheet_6_katana_slash", 1, 2, 20, 10, 1, 3),
        }

    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)

class MainMenu(Scene):
    def __init__(self, app):
        super().__init__(app)
        bg = Entity(self.app, "grass_background")
        bg.z_index = -1
        menu = Entity(self.app, "start_menu")
        self.add_entity(bg)
        self.add_entity(menu)

    def update(self):
        super().update()
    
    def draw(self, screen):
        super().draw(screen)
        self.draw_cursor(screen)
    
    def draw_cursor(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect = self.cursor_image.get_rect(topleft= mouse_pos)
        if not pygame.mouse.get_pressed()[0]:
            surface.blit(self.cursor_image, self.cursor_rect)
        else:
            surface.blit(self.down_cursor ,self.cursor_rect)