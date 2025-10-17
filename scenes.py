from scene import Scene
from entity import Entity
import pygame
from player import Player
from enemy import Enemy
from weapons import MeleWeapon
from ui import * 
import random

class ExampleScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.test = Entity(self.app)
        self.test.pos = pygame.Vector2(0, 0)
        test2 = Entity(self.app, "grass_background")
        test2.pos = pygame.Vector2(64,64)
        self.player = Player(self.app)
        self.target_camera_pos = self.player.pos
        self.camera_pos = self.player.pos
        self.hud = HUD(self.app, self.player)
        self.player.add_child(MeleWeapon(self.app, 100, 1))

        btn1 = Button(app, self.spawn_enemy, sprite="spawn_enemy_button") 
        self.add_entity(btn1)
        self.add_entity(self.test,)
        #self.add_entity(test2)
        self.add_entity(self.player)
        self.add_entity(self.hud)

    def update(self):
        super().update()
        self.camera_pos = self.target_camera_pos.slerp(self.camera_pos, 0.65)
        
        self.test.pos.x += 1  

    def spawn_enemy(self):
        enemy = Enemy(self.app, self.player)
        rnd_dir = random.randrange(0, 360)
        enemy.pos = self.player.pos + pygame.Vector2(1,0).rotate(rnd_dir) * 900


        self.add_entity(enemy)
    