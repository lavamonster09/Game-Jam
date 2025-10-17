import pygame 
from entity import Entity

class Xp(Entity):
    def __init__(self, app, player):
        super().__init__(app, "xp")
        self.player = player

    def update(self):
        if self.pos.distance_to(self.player.pos) <= 32:
            self.attributes["visible"] = False
            self.player.xp += 10
            if self.player.xp > self.player.max_xp:
                self.player.xp = self.player.max_xp
            self.app.get_current_scene().entities.remove(self)
        elif self.pos.distance_to(self.player.pos) <= 128:
            self.pos = self.pos.move_towards(self.player.pos, 5)
        super().update() 

