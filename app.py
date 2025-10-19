import pygame
import sys
import asset_loader
from scene import Scene
from entity import Entity

class App:
    def init(self, cfg):
        pygame.display.init()

        self.cfg = cfg
        self.config = cfg.config
        self.name = self.config["NAME"]
        self.width = self.config["SCREEN_WIDTH"]
        self.height = self.config["SCREEN_HEIGHT"]
        

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.asset_loader = asset_loader.AssetLoader(self.config["ASSET_DIR"])
        pygame.display.set_caption(self.name) 
        self.timer = 0
        self.running = True
        self.paused = False 

        self.scenes = {}
        self.current_scene = ""

        self.clock = pygame.Clock()

    def run(self):
        while self.running:
            self.check_events()
            self.update()            
            self.draw()
            if not self.paused:
                self.timer += 1

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

    def get_current_scene(self):
        return self.scenes[self.current_scene]

    def play_sound(self, key, vol):
        self.asset_loader.sounds[key].set_volume(vol)
        self.asset_loader.sounds[key].play()
