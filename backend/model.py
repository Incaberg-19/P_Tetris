import pygame
from dataclasses import dataclass, field

@dataclass
class GameInfo:
        FPS: int = 60
        rectWidth: int = 10  
        rectHeight: int = 17
        rectSize: int = 45
        gameField: list = field(default_factory=list)
        gameScore: int = 0
        gameLevel: int = 1
        gameSpeed: int = 50
        gameResolution: tuple = field(init=False)
        
        def __post_init__(self):
            self.gameResolution: tuple = (self.rectWidth*self.rectSize*2),(self.rectHeight*self.rectSize)
            self.screen = pygame.display.set_mode(self.gameResolution)  
            self.grid: list = [
                pygame.Rect (
                    x * self.rectSize,
                    y * self.rectSize,
                    self.rectSize,
                    self.rectSize
                )
                for x in range(self.rectWidth)
                for y in range(self.rectHeight)
            ]   

class FigureModels:
    def __init__(self,rectWidth,rectSize):
        self.rectSize=rectSize
        self.rectWidth=rectWidth
        FigureModelCoordinates=[
            [(-1, 0), (-2, 0), (0, 0), (1, 0)],
            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, 0)]
        ]
        self.FigureModels=[[pygame.Rect(x+self.rectWidth//2,y+1,1,1) for x,y in figCoords] for figCoords in FigureModelCoordinates]

    def getCurrentFigure(self,index):
        currentFigure=[
            pygame.Rect(
                self.FigureModels[index][i].x * self.rectSize,
                self.FigureModels[index][i].y * self.rectSize,
                self.rectSize-1,
                self.rectSize-1
            ) 
            for i in range(4)
        ]
        return currentFigure

class GameModel(GameInfo, FigureModels):
    def __init__(self):
        GameInfo.__init__(self)
        FigureModels.__init__(self, self.rectWidth, self.rectSize)
        pygame.init()  