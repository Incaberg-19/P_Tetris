#BACKEND
import pygame
from random import randint

def getRandomIndex(index=None):
    randomNumber=index
    while(randomNumber==index):
        randomNumber=randint(0,6)
    return randomNumber

class GameInfo:
    def __init__(self):
        self.rectWidth = 10  
        self.rectHeight = 17
        self.rectSize = 45
        self.FPS=60 
        self.gameResolution = self.rectWidth*self.rectSize,self.rectHeight*self.rectSize 
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
    
    def printFiguresModels(self):
        print(self.FigureModels[0])

class GameModel(GameInfo, FigureModels):
    def __init__(self):
        GameInfo.__init__(self)
        FigureModels.__init__(self, self.rectWidth, self.rectSize)
        pygame.init()  
        self.screen = pygame.display.set_mode(self.gameResolution)  
        
        
    
class FiniteStateMachine:
    
    def __init__(self):  
        self.states = {  
            "START": 1,  
            "SPAWN": 0,  
            "MOVING": 0,
            "SHIFTING": 0,  
            "ATTACHING": 0,
            "GAMEOVER": 0,  
            "QUIT": 0,
            "PAUSE": 0,  
            "ACTION": 0,
        }  
        self.timer=0
        self.currentFigure=0
        self.index=getRandomIndex()
        self.firstStart=0
    
    def giveCurrentFigure(self,currentFigure):
        self.currentFigure=currentFigure
    
    def giveGameField(self,gameField):
        self.gameField=gameField
        
    def handleEvents(self,events):
        for event in events:
            self.handleStop(event)
            self.handleStart(event)
            self.handleMovement(event)
            self.handleAction(event)
        self.handleTimer()
        self.handleAttaching(events)
        return self.currentFigure,self.gameField
    
    def handleAction(self,event):
        if self.states["MOVING"]==1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.states["ACTION"]=1
        
        if self.states["ACTION"]==1:
            rotateFigure(self.currentFigure,self.gameField,self.model.rectSize)
            self.states["ACTION"]=0
                
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
                        self.firstStart=1
            
            if self.states["SPAWN"] == 1:
                self.states["SPAWN"] = 0
                if (self.firstStart!=1):
                    self.index=getRandomIndex(self.index)
                    self.currentFigure=self.model.getCurrentFigure(self.index)
                else:
                    self.firstStart=0
                self.states["MOVING"] = 1
                
    def handleMovement(self,event):
        if self.states["MOVING"] == 1:         
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT):
                            self.states["SHIFTING"] = 1
        if self.states["SHIFTING"] == 1:
                if event.key==pygame.K_DOWN:
                    self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45)
                elif event.key==pygame.K_LEFT:
                    self.currentFigure=moveFigure(self.currentFigure,self.gameField,-45,0)
                elif event.key==pygame.K_RIGHT:
                    self.currentFigure=moveFigure(self.currentFigure,self.gameField,45,0)
                self.states["SHIFTING"] = 0                
    
    def handleTimer(self):
        if self.states["MOVING"] == 1:  
            self.timer+=1
            if checkBorders(self.currentFigure,self.gameField,0,45,"MOVING")==False:
                self.states["ATTACHING"]=1
                self.timer=0
            elif(self.timer>50):
                self.timer=0
                self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45) 
    
    def handleAttaching(self,event):
        if self.states["ATTACHING"]==1:
            self.states["ATTACHING"]=0
            self.states["SPAWN"]=1
            self.gameField=saveFigure(self.currentFigure,self.gameField,self.model.rectSize)
            self.handleStart(event)
            
    
    def printStates(self):  
        print(self.states)  

def rotateFigure(currentFigure,gameField,rectSize):
    # currentFigure[0] - center coordinate, point of rotation
    checkValue=checkBorders(currentFigure,gameField,0,0,"ACTION")
    
    if checkValue==True:
        for i in range(4):
            x = currentFigure[i].y - currentFigure[0].y
            y = currentFigure[i].x - currentFigure[0].x
            currentFigure[i].x = currentFigure[0].x - (x)
            currentFigure[i].y = currentFigure[0].y + (y)


def checkBorders(currentFigure,gameField,add_X,add_Y,state):
    checkValue=True
    info=GameInfo()
    checkFigure=[]
    if state=="MOVING":
        checkFigure=[
            pygame.Rect(
                (currentFigure[i].x+add_X),
                (currentFigure[i].y+add_Y),
                info.rectSize-1,
                info.rectSize-1
            ) 
            for i in range(4)
        ]
    elif state=="ACTION":
        checkFigure=[
            pygame.Rect(
                (currentFigure[0].x - (currentFigure[i].y - currentFigure[0].y)),
                (currentFigure[0].y + (currentFigure[i].x - currentFigure[0].x)),
                info.rectSize-1,
                info.rectSize-1
            ) 
            for i in range(4)
        ]
        
    for i in range(4):
        if (checkFigure[i] in gameField):
            checkValue=False
        if (checkFigure[i].x) < 0 or (checkFigure[i].x) > info.rectWidth*info.rectSize-1:
            checkValue=False
        if (checkFigure[i].y) > info.rectHeight*info.rectSize-1:
            checkValue=False
            
    return checkValue

def moveFigure(currentFigure,gameField,add_X,add_Y):
    checkValue=checkBorders(currentFigure,gameField,add_X,add_Y,"MOVING")
    if checkValue==True:
        for i in range(4):
            currentFigure[i].x+=add_X
            currentFigure[i].y+=add_Y
    return currentFigure

def saveFigure(currentFigure,listToSave,rectSize):
    for i in range(4):
        listToSave.append(
            pygame.Rect(
                currentFigure[i].x,
                currentFigure[i].y,
                rectSize-1,
                rectSize-1
            ) 
        )
    return listToSave

class GameController(FiniteStateMachine):
    def __init__(self,model):
        super().__init__()
        self.model = model
        self.giveCurrentFigure(self.model.getCurrentFigure(getRandomIndex()))
        self.giveGameField(self.model.gameField)
        
    def processInput(self,events):
        return self.handleEvents(events)