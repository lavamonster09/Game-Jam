import pygame

class Camera:
    def __init__(self):
        self.centre = pygame.Vector2(0,0)

    def get_offset(self, pos: pygame.Vector2):
        return self.centre - pos
