import os 
import pygame

class AssetLoader:
    def __init__(self, asset_dir):
        pygame.font.init()
        self.asset_dir = os.walk(asset_dir)
        self.assets = {}
        self.fonts = {}
        self.load()
        self.null = pygame.Surface((2,2))
        pygame.draw.rect(self.null,(255, 0, 255),(0,0,1,1))
        pygame.draw.rect(self.null,(255, 0, 255),(1,1,1,1))
        self.null = pygame.transform.scale(self.null, (64, 64))

    def load(self):
        for dir in self.asset_dir:
            for file in dir[2]:
                if file.split(".")[-1] in ["png","jpg","jpeg"]:
                    if file.split("_")[0] == "sheet":
                        image = pygame.image.load(dir[0] + "/" + file).convert_alpha()
                        images = []
                        for i in range(int(file.split("_")[1])):
                            surf = pygame.Surface((image.width / int(file.split("_")[1]), image.height))
                            surf.blit(image, (0,0), (surf.width * i, 0, surf.width, surf.height))
                            surf = pygame.transform.scale(surf, (surf.width * 2, surf.height * 2))
                            surf.set_colorkey((0,0,0))
                            images.append(surf)
                        self.assets[file.split(".")[-2]] = images
                        print(self.assets)
                    else:
                        image = pygame.image.load(dir[0] + "/" + file)
                        self.assets[file.split(".")[0]] = pygame.transform.scale(image, (image.width * 2, image.height * 2)).convert_alpha()
                elif file.split(".")[-1] == "ttf":
                    self.fonts[file.split(".")[0]] = pygame.font.Font(dir[0] + "/" + file)
                  
    def get(self, key):
        return self.assets.get(key, self.null)

    def get_frame(self, key, frame):
        asset = self.assets.get(key, self.null)
        if asset != self.null:
            asset = asset[frame]
        return asset