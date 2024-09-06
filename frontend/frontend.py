import pygame

class GameView:
    def __init__(self,*args):
        self.screen,self.grid,self.gameField=args
        self.font = pygame.font.SysFont('bahnschrift', 30)
    
    def callAllFront(self,currentFigure,gameScore,gameLevel,nextFigure):
        self.printObjects(currentFigure,nextFigure)
        gameNextFigure="NEXT FIGURE"
        gameScoreString=f"GAME SCORE: {gameScore}"
        gameLevelString=f"GAME LEVEL: {gameLevel}"
        scoreArea=self.font.render(gameScoreString, True, (255, 255, 255))
        levelArea=self.font.render(gameLevelString, True, (255, 255, 255))
        NextFigureArea=self.font.render(gameNextFigure, True, (255, 255, 255))
        self.screen.blit(scoreArea, (500, 20)) 
        self.screen.blit(levelArea, (500, 70)) 
        self.screen.blit(NextFigureArea, (580, 120)) 
        pygame.display.flip() 
        
    
    def printObjects(self,currentFigure,nextFigure):
        self.screen.fill((0, 0, 0))
        [pygame.draw.rect(self.screen,(40,40,40),ptrOnRect,1) for ptrOnRect in self.grid] 
        for square in currentFigure: 
            pygame.draw.rect(self.screen,pygame.Color('White'),square) 
        for square in self.gameField:
            pygame.draw.rect(self.screen,pygame.Color('White'),square) 
        for square in nextFigure:
            pygame.draw.rect(self.screen, pygame.Color('White'), (square[0]+440, square[1]+170, square[2], square[3]))