import pygame

class Camera:
    def __init__(self, player_pos):
        self.pos = (0,0)
        self.player_pos = player_pos
        self.display = pygame.display.get_surface()
        self.size = pygame.Vector2(self.display.get_size())
        self.all_sprites = pygame.sprite.Group()

    def render(self, *items):
        draw_order = []
        for item in items:
            self.all_sprites.add(item)

        for sprite in self.all_sprites:
            draw_order.append([sprite, sprite.zlayer])

        for sprite in draw_order.sort():
            new_pos = pygame.Vector2(sprite[0].pos.x - self.player_pos.x, -sprite[0].pos.y + self.player_pos.y) + self.size / 2
            sprite[0].rect = sprite[0].image.get_rect(center = new_pos)
            self.display.blit(sprite[0].image, sprite[0].rect)

    def update(self):
        self.pos = self.player_pos