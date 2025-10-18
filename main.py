from app import *
from scene import *
from scenes import *
from config import *

game = App()
cfg = Config()

def main():
    cfg.init()
    game.init(cfg)

    scenes = {
        "test": ExampleScene(game),
        "death": ExampleScene(game),
        "main_menu": MainMenu(game)
    }

    game.scenes = scenes
    game.current_scene = "main_menu"
    game.run()

if __name__ == "__main__":
    main()