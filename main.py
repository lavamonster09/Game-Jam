from app import *
from scene import *
from scenes import * 

game = App()

def main():
    config = {
        "NAME": "totally not vampire survivors",
        "SCREEN_WIDTH": 1600,
        "SCREEN_HEIGHT": 900,
        "ASSET_DIR": "./assets"
    } 
    scenes = {
        "test": ExampleScene(game),
        "death": ExampleScene(game),
    }
    game.init(config)
    game.scenes = scenes
    game.current_scene = "test"
    game.run()

if __name__ == "__main__":
    main()