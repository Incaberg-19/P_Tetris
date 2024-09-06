import pygame

class GameInfo:
    def __init__(self):
        self.rectWidth = 10  
        self.rectHeight = 17
        self.rectSize = 45
        self.FPS=60
        self.gameResolution = (self.rectWidth*self.rectSize*2),(self.rectHeight*self.rectSize)
        self.grid = [
            pygame.Rect (
                x * self.rectSize,
                y * self.rectSize,
                self.rectSize,
                self.rectSize
            )
            for x in range(self.rectWidth)
            for y in range(self.rectHeight)
        ]   
        self.gameField=[]
        self.gameScore=0
        self.gameLevel=1
        self.gameSpeed=50

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
        self.screen = pygame.display.set_mode(self.gameResolution)  