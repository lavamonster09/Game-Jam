import os 
import pygame

class AssetLoader:
    def __init__(self, asset_dir):
        pygame.font.init()
        self.asset_dir = os.walk(asset_dir)
        self.assets = {}
        self.fonts = {}
        self.load()

    def load(self):
        for dir in self.asset_dir:
            for file in dir[2]:
                if file.split(".")[-1] in ["png","jpg","jpeg"]:
                    self.assets[file.split(".")[0]] = pygame.transform.scale2x(pygame.image.load(dir[0] + "/" + file))
                elif file.split(".")[-1] == "ttf":
                    self.fonts[file.split(".")[0]] = pygame.font.Font(dir[0] + "/" + file)
                  
    def get(self, key):
        null = pygame.Surface((2,2))
        pygame.draw.rect(null,(255, 0, 255),(0,0,1,1))
        pygame.draw.rect(null,(255, 0, 255),(1,1,1,1))
        null = pygame.transform.scale(null, (64, 64))
        return self.assets.get(key, null) 