import pygame
import sys
import asset_loader
from scene import Scene
from entity import Entity

class App:
    def init(self, cfg):
        self.cfg = cfg
        self.config = cfg.config
        self.name = self.config["NAME"]
        self.width = self.config["SCREEN_WIDTH"]
        self.height = self.config["SCREEN_HEIGHT"]
        
        self.asset_loader = asset_loader.AssetLoader(self.config["ASSET_DIR"])

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name) 
        self.running = True

        self.scenes = {}
        self.current_scene = ""

        self.clock = pygame.Clock()

    def run(self):
        while self.running:
            self.check_events()
            self.scenes[self.current_scene].update()
            self.draw()

    def check_events(self):       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
                self.running = False

    def draw(self):
        self.screen.fill((0,0,0))
        self.scenes[self.current_scene].draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def update(self):
        self.scenes[self.current_scene].update() 