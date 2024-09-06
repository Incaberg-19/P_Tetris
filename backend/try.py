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