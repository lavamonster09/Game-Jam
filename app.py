import pygame
import sys

class App:
    def init(self, config: dict):
        self.name = config["NAME"]
        self.width = config["SCREEN_WIDTH"]
        self.height = config["SCREEN_HEIGHT"]

        self.screen = pygame.display.set_mode((self.width, self.height)) 
        self.running = True

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()

    def check_events(self):       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
                self.running = False

    def draw():
        pass

    def update():
        pass