from app import *

game = App()

def main():
    config = {
        "NAME": "totally not vampire survivors",
        "SCREEN_WIDTH": 1600,
        "SCREEN_HEIGHT": 900
    }
    game.init(config)
    game.run()

if __name__ == "__main__":
    main()