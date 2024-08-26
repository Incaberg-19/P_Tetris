#BACKEND
import pygame

class GameInfo:
    rectWidth = 10  
    rectHeight = 17
    rectSize = 45
    FPS=60 
    gameResolution = rectWidth*rectSize,rectHeight*rectSize 

class FigureModels(GameInfo):
    def __init__(self):
        FigureModelCoordinates=[
            [(-1, 0), (-2, 0), (0, 0), (1, 0)],
            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, 0)]
        ]
        self.FigureModels=[[pygame.Rect(x+GameInfo.rectWidth//2,y+1,1,1) for x,y in figCoords] for figCoords in FigureModelCoordinates]

    def getModelCurrentFigure(self,index):
        currentFigure=[
            pygame.Rect(
                self.FigureModels[index][i].x * GameInfo.rectSize,
                self.FigureModels[index][i].y * GameInfo.rectSize,
                GameInfo.rectSize-1,
                GameInfo.rectSize-1
            ) 
            for i in range(4)
        ]
        return currentFigure

class GameModel(FigureModels):
    def __init__(self):
        super().__init__()
        
        
    
class FiniteStateMachine:
    
    def __init__(self):  
        self.states = {  
            "START": 1,  
            "SPAWN": 0,  
            "MOVING": 0,
            "SHIFTING": 0,  
            "GAMEOVER": 0,  
            "QUIT": 0,
            "PAUSE": 0,  
        }  
        self.timer=0
        self.numberFigure=0
        self.currentFigure=0
    
    def getCurrentFigure(self,currentFigure):
        self.currentFigure=currentFigure
        
    def handleEvents(self,events):
        for event in events:
            self.handleStop(event)
            self.handleStart(event)
            self.handleMovement(event)
        self.handleTimer()
        return self.currentFigure
            
    def handleStop(self,event):
        if event.type == pygame.QUIT:
            self.states["QUIT"] = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.states["QUIT"] = 1
            elif event.key == pygame.K_SPACE:  
                if self.states["PAUSE"]==1:
                    self.states["PAUSE"]=0
                    if self.states["START"]==0:
                        self.states["MOVING"]=1
                else:
                    self.states["PAUSE"]=1
                    self.states["MOVING"]=0
                    self.states["SHIFTING"]=0
                    
    def handleStart(self,event):
        if self.states["PAUSE"]==0 and self.states["QUIT"]==0:
            
            if self.states["START"]==1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.states["START"] = 0
                        self.states["SPAWN"] = 1
            
            if self.states["SPAWN"] == 1:
                self.states["SPAWN"] = 0
                self.states["MOVING"] = 1
                
    def handleMovement(self,event):
        if self.states["MOVING"] == 1:         
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT):
                            self.states["SHIFTING"] = 1
        if self.states["SHIFTING"] == 1:
                if event.key==pygame.K_DOWN:
                    self.currentFigure=moveFigureModel(self.currentFigure,0,45)
                elif event.key==pygame.K_LEFT:
                    self.currentFigure=moveFigureModel(self.currentFigure,-45,0)
                elif event.key==pygame.K_RIGHT:
                    self.currentFigure=moveFigureModel(self.currentFigure,45,0)
                self.states["SHIFTING"] = 0
                
    def handleTimer(self):
        if self.states["MOVING"] == 1:  
            self.timer+=1
            if self.timer>50:
                self.timer=0
                if checkBorders(self.currentFigure,0,45)==False:
                    self.states["SPAWN"]=1
                else:
                    self.currentFigure=moveFigureModel(self.currentFigure,0,45) 
    
    def printStates(self):  
        print(self.states)  

def checkBorders(currentFigure,add_X,add_Y):
    checkValue=True
    info=GameInfo()
    for i in range(4):
        if (currentFigure[i].x + add_X) < 0 or (currentFigure[i].x + add_X) > info.rectWidth*info.rectSize-1:
            checkValue=False
        if (currentFigure[i].y + add_Y) > info.rectHeight*info.rectSize-1:
            checkValue=False
    return checkValue

def moveFigureModel(currentFigure,add_X,add_Y):
    checkValue=checkBorders(currentFigure,add_X,add_Y)
    if checkValue==True:
        for i in range(4):
            currentFigure[i].x+=add_X
            currentFigure[i].y+=add_Y
    return currentFigure


class GameController(FiniteStateMachine):
    def __init__(self,model):
        super().__init__()
        self.model = model
        self.getCurrentFigure(self.model.getModelCurrentFigure(0))
        
    def processInput(self,events):
        return self.handleEvents(events)