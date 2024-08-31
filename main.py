import pygame
import sys
from backend import *
from frontend import *

class Main:  
    def __init__(self):  
        self.model=GameModel()
        self.control=GameController(self.model)
        self.clock = pygame.time.Clock()
    
    def game_loop(self):
        while self.control.states["QUIT"]==0:  
            currentFigure,gameField=self.control.processInput(pygame.event.get())
            printObjects(self.model.screen,self.model.grid,currentFigure,gameField)
            self.clock.tick(self.model.FPS)
            # self.control.printStates()
        pygame.quit()  
        sys.exit()  
  
if __name__ == '__main__':  
    Main().game_loop()