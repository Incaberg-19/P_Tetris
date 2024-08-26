import pygame
import sys
from backend import *
from frontend import *

class Main(GameInfo):  
    def __init__(self):  
        pygame.init()  
        self.screen = pygame.display.set_mode(GameInfo.gameResolution)  
        self.grid = [
            pygame.Rect (
                x * GameInfo.rectSize,
                y * GameInfo.rectSize,
                GameInfo.rectSize,
                GameInfo.rectSize
            )
            for x in range(GameInfo.rectWidth)
            for y in range(GameInfo.rectHeight)
        ]
        self.clock = pygame.time.Clock()
    
    def game_loop(self):  
        self.model=GameModel()
        self.control=GameController(self.model)
        while self.control.states["QUIT"]==0:  
            currentFigure=self.control.processInput(pygame.event.get())
            printObjects(self.screen,self.grid,currentFigure)
            self.clock.tick(GameInfo.FPS)
        pygame.quit()  
        sys.exit()  
  
if __name__ == '__main__':  
    Main().game_loop()