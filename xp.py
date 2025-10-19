import pygame 
from entity import Entity
import math
import random
class Xp(Entity):
    def __init__(self, app, player):
        super().__init__(app, "xp")
        self.player = player
        self.counter = 0
        self.z_index = -1

    def update(self):
        self.counter += 0.1
        if self.pos.distance_to(self.player.pos) <= 32:
            self.attributes["visible"] = False
            self.player.xp += 10
            sound = random.choice(["pickupCoin","pickupCoin(1)","pickupCoin(2)"])
            self.app.play_sound(sound, 0.03)
            if self.player.xp > self.player.max_xp:
                self.player.xp = self.player.max_xp
            self.app.get_current_scene().entities.remove(self)
        elif self.pos.distance_to(self.player.pos) <= 128:
            self.pos = self.pos.move_towards(self.player.pos, 5)

        self.pos.y += math.sin(self.counter) 
        super().update() 

