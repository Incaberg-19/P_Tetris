from .fsm import *
from sys import exit

class GameController(FiniteStateMachine):
    def __init__(self,model,view):
        self.model=model
        self.view=view
        super().__init__()
        self.clock = pygame.time.Clock()
    
    def gameLoop(self):
        while self.quit!=True: 
            self.handleEvents(pygame.event.get())
            self.view.callAllFront(self.currentFigure,self.gameScore,self.gameLevel,self.model.getCurrentFigure(self.nextIndex))
            self.clock.tick(self.model.FPS)
        pygame.quit()  
        exit()