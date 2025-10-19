from scene import Scene
from entity import Entity
import pygame
from player import Player
from enemy import Enemy
from enemy_manager import EnemyManager
from weapons import *
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


        #btn1 = Button(app, self.spawn_enemy, sprite="spawn_enemy_button") 
        self.add_entity(self.enemy_manager)
        #self.add_entity(btn1)
        self.add_entity(self.player)
        self.add_entity(self.hud)
        self.app.paused = False
        self.app.timer = 0

    def update(self):
        if self.app.paused:
            self.hud.update()
        else:
            if pygame.key.get_just_pressed()[self.app.cfg.get_key_code("PAUSE")]:
                self.app.paused = True
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
            "Dex Melee": MeleeWeapon(self.app,"sheet_10_dex_slash", 5, 1.5, 10, 1, 1, 3),
            "Qua Melee": MeleeWeapon(self.app,"sheet_6_katana_slash", 7, 2, 20, 15, 2, 2),
            "Str Melee": MeleeWeapon(self.app,"sheet_10_heavy_slash", 10, 2.5, 45, 20, 3, 1),
            "Dex Ranged": RangedWeapon(self.app,"arrow_dex", 1, 2, 20, 10, 1, 3),
            "Qua Ranged": RangedWeapon(self.app,"sheet_6_katana_slash", 1, 2, 40, 10, 2, 2),
            "Str Ranged": RangedWeapon(self.app,"sheet_6_katana_slash", 1, 2, 60, 10, 1, 3),
        }
        self.selected_weapon = None

        bg = Entity(self.app, "grass_background")
        bg.z_index = -1
        self.add_entity(bg)

        menu = Entity(self.app, "weapon_select_menu")
        self.add_entity(menu)

        dex_melee_btn = Button(self.app, self.weapon_on_click, "sheet_2_select_button", [self.weapons["Dex Melee"]], toggleable=True)
        dex_melee_btn.pos = pygame.Vector2(11 * 16 * 2, 11 * 16 * 2)
        dex_melee_btn.z_index = 1
        self.add_entity(dex_melee_btn)
        
        qua_melee_btn = Button(self.app, self.weapon_on_click, "sheet_2_select_button", [self.weapons["Qua Melee"]], toggleable=True)
        qua_melee_btn.pos = pygame.Vector2(22 * 16 * 2, 11 * 16 * 2)
        qua_melee_btn.z_index = 1
        self.add_entity(qua_melee_btn)

        str_melee_btn = Button(self.app, self.weapon_on_click, "sheet_2_select_button", [self.weapons["Str Melee"]], toggleable=True)
        str_melee_btn.pos = pygame.Vector2(33 * 16 * 2, 11 * 16 * 2)
        str_melee_btn.z_index = 1 
        self.add_entity(str_melee_btn)

        dex_ranged_btn = Button(self.app, self.weapon_on_click, "sheet_2_select_button", [self.weapons["Dex Ranged"]], toggleable=True)
        dex_ranged_btn.pos = pygame.Vector2(11 * 16 * 2, 22 * 16 * 2)
        dex_ranged_btn.z_index = 1
        self.add_entity(dex_ranged_btn)

        qua_ranged_btn = Button(self.app, self.weapon_on_click, "sheet_2_select_button", [self.weapons["Qua Ranged"]], toggleable=True)
        qua_ranged_btn.pos = pygame.Vector2(22 * 16 * 2, 22 * 16 * 2)
        qua_ranged_btn.z_index = 1
        self.add_entity(qua_ranged_btn)

        str_ranged_btn = Button(self.app, self.weapon_on_click, "sheet_2_select_button", [self.weapons["Str Ranged"]], toggleable=True)
        str_ranged_btn.pos = pygame.Vector2(33 * 16 * 2, 22 * 16 * 2)
        str_ranged_btn.z_index = 1
        self.add_entity(str_ranged_btn)

        start_run_btn = Button(self.app, self.start_run_on_click, "sheet_2_startt_button", [])
        start_run_btn.pos = pygame.Vector2(22 * 16 * 2, 25 * 16 * 2)
        start_run_btn.z_index = 1
        self.add_entity(start_run_btn)

        back_btn = Button(self.app, self.back_on_click, "sheet_2_back_button", [])
        back_btn.pos = pygame.Vector2(32,32)
        back_btn.z_index = 1 
        self.add_entity(back_btn)

        self.weapon_buttons = [qua_melee_btn, qua_ranged_btn, str_melee_btn, str_ranged_btn, dex_melee_btn, dex_ranged_btn]

    def update(self):
        self.app.paused = True
        super().update()

    def back_on_click(self):
        self.app.current_scene = "main_menu"

    def weapon_on_click(self, weapon):
        for button in self.weapon_buttons:
            button.active = False
        self.selected_weapon = weapon

    def start_run_on_click(self):
        if self.selected_weapon != None:
            self.app.scenes["game"] = ExampleScene(self.app)
            self.app.scenes["game"].player.add_child(self.selected_weapon)
            self.app.current_scene = "game"


    def draw(self, screen):
        super().draw(screen)

class MainMenu(Scene):
    def __init__(self, app):
        super().__init__(app)
        bg = Entity(self.app, "grass_background")
        bg.z_index = -1
        menu = Entity(self.app, "start_menu")
        new_run_button = Button(self.app, self.btn_new_run, "sheet_2_startrun_button")
        new_run_button.pos = pygame.Vector2(272 * 2,160 * 2)
        new_run_button.z_index = 100000
        exit_button = Button(self.app, self.btn_exit, "sheet_2_exit_button")
        exit_button.pos = pygame.Vector2(272 * 2, 16 * 16 * 2)
        exit_button.z_index = 100000
        self.add_entity(exit_button)
        self.add_entity(new_run_button)
        self.add_entity(bg)
        self.add_entity(menu)

    def update(self):
        self.app.paused = True
        super().update()
    
    def draw(self, screen):
        super().draw(screen)
        self.draw_cursor(screen)

    def btn_new_run(self):
        self.app.current_scene = "weapon_select"

    def btn_exit(self):
        self.app.running = False
    
    def draw_cursor(self, surface: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_rect = self.cursor_image.get_rect(topleft= mouse_pos)
        if not pygame.mouse.get_pressed()[0]:
            surface.blit(self.cursor_image, self.cursor_rect)
        else:
            surface.blit(self.down_cursor ,self.cursor_rect)