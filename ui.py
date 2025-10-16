from entity import Entity
from enemy import Enemy
import pygame

class Button(Entity):
    def __init__(self, app, on_click , sprite="none"):
        super().__init__(app, sprite)
        self.on_click = on_click
        
    def update(self):
        super().update()
        if self.get_rect().collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_just_pressed()[0]:
                self.on_click()