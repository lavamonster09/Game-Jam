import pygame
import json

class Config:
    def init(self):
        with open("config.json") as data:
            cfg = json.load(data)
            self.keybinds = cfg["keybinds"]
            self.config = cfg["settings"] 
            data.close()

    def get_key_code(self, key: str) -> int:
        return pygame.key.key_code(self.keybinds[key])