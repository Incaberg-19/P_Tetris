from backend import *
from frontend import *

def main():
    model=GameModel()
    view=GameView(model.screen,model.grid,model.gameField)
    controller = GameController(model, view)
    controller.gameLoop()

if __name__ == "__main__":  
    main()