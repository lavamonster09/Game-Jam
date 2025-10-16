import pygame
import sys
import asset_loader
from scene import Scene
from entity import Entity

class App:
    def init(self, config: dict):
        self.name = config["NAME"]
        self.width = config["SCREEN_WIDTH"]
        self.height = config["SCREEN_HEIGHT"]
        
        self.asset_loader = asset_loader.AssetLoader(config["ASSET_DIR"])

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.name) 
        self.running = True

        self.scenes = {}
        self.current_scene = Scene()
        self.current_scene.add_entity(Entity(self), "test")
        self.current_scene.entities["test"]

    def run(self):
        while self.running:
            self.check_events()
            self.current_scene.update()
            self.draw()

    def check_events(self):       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
                self.running = False

    def draw(self):
        self.screen.fill((0,0,0))
        self.current_scene.draw(self.screen)
        pygame.display.flip()

    def update(self):
        self.current_scene.update() 