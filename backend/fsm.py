import pygame
from .auxToFsm import *
from enum import Enum

class States(Enum):
        START = 0
        SPAWN=1 
        MOVING = 2
        SHIFTING = 3 
        ATTACHING = 4
        GAMEOVER = 5 
        QUIT = 6
        PAUSE = 7  
        ACTION = 8
        
class FiniteStateMachine:

    def __init__(self):  
        self.state=None 
        self.timer=0
        self.holdTimer=0
        self.holdShiftingTimer=0
        self.restrictionForShifting=4
        
        self.index=getRandomIndex()
        self.nextIndex=getRandomIndex(self.index)
        
        self.gameField=self.model.gameField
        self.rectSize=self.model.rectSize
        self.rectWidth=self.model.rectWidth
        self.rectHeight=self.model.rectHeight
        self.currentFigure=self.model.getCurrentFigure(self.index)
        self.gameScore=self.model.gameScore
        self.gameLevel=self.model.gameLevel
        self.gameSpeed=self.model.gameSpeed
        self.parameters=(self.rectWidth,self.rectHeight,self.rectSize)
        
    def handleEvents(self,events):
        for event in events:
            self.handleStop(event)
            self.handleStart(event)
            self.handleSpawn()
            self.handleMoving(event)
            self.handleShifting("INCYCLE")
            self.handleAction(event)
        self.handleShifting("OUTCYCLE")
        self.handleTimer()
        self.handleAttaching()
        
    def handleMoving(self,event):
        if self.state==States.MOVING:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT,pygame.K_RIGHT):
                    self.restrictionForShifting=4
                elif event.key==pygame.K_DOWN:
                    self.restrictionForShifting=1
                self.holdTimer = 0
            elif event.type == pygame.KEYUP:
                self.holdTimer = 0
                
    def handleShifting(self,state):
        if self.state==States.MOVING:
            self.state = States.SHIFTING

        if self.state==States.SHIFTING:
            pressedKeys=pygame.key.get_pressed()

            if state=="OUTCYCLE":
                self.holdTimer += 1
            
                if self.holdTimer > 12:
                    if self.holdShiftingTimer>self.restrictionForShifting:
                        self.ProcessMoveFigure(pressedKeys)
                        self.holdShiftingTimer=0
                    else:
                        self.holdShiftingTimer+=1
                            
            elif state=="INCYCLE":
                self.ProcessMoveFigure(pressedKeys)
                
            self.state=States.MOVING
    
    def ProcessMoveFigure(self,pressedKeys):
        if pressedKeys[pygame.K_DOWN]:
            self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45,*self.parameters)
        elif pressedKeys[pygame.K_RIGHT]:
            self.currentFigure=moveFigure(self.currentFigure,self.gameField,45,0,*self.parameters)
        elif pressedKeys[pygame.K_LEFT]:
            self.currentFigure=moveFigure(self.currentFigure,self.gameField,-45,0,*self.parameters)
    
    def handleAction(self,event):
        if self.state==States.MOVING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state=States.ACTION
        if self.state==States.ACTION:
            rotateFigure(self.currentFigure,self.gameField,*self.parameters)
            self.state=States.MOVING
                
    def handleStop(self,event):
        if event.type == pygame.QUIT:
            self.state=States.QUIT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.state=States.QUIT
            elif event.key == pygame.K_SPACE:
                if self.state==States.MOVING:
                    self.state=States.PAUSE
                elif self.state==States.PAUSE:
                    self.state=States.MOVING
                    
    def handleStart(self,event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state==None or self.state==States.GAMEOVER:
                        self.state=States.START
                        self.handleRestart()
            
            if self.state==States.START:
                self.state=States.SPAWN
    
    def handleSpawn(self):
        if self.state==States.SPAWN:
            self.state=States.MOVING
    
    def handleTimer(self):
        if self.state==States.MOVING: 
            if checkBorders(self.currentFigure,self.gameField,0,45,"MOVING",*self.parameters)==False:
                self.state=States.ATTACHING
        
        if self.state==States.MOVING: 
            self.timer+=1
            if self.timer>self.gameSpeed:
                self.timer=0
                self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45,*self.parameters) 
    
    def handleAttaching(self):
        if self.state==States.ATTACHING:
            self.gameField=saveFigure(self.currentFigure,self.gameField,self.rectSize)
            self.gameScore,self.gameLevel,self.gameSpeed=countGameScore(self.gameField,self.rectSize,self.gameScore,self.gameLevel,self.gameSpeed)

            self.index=self.nextIndex
            self.nextIndex=getRandomIndex(self.index)
            self.currentFigure=self.model.getCurrentFigure(self.index)
            if checkBorders(self.currentFigure,self.gameField,0,45,"MOVING",*self.parameters)==False:
                self.state=States.GAMEOVER
            else:
                self.state=States.SPAWN
                self.handleSpawn()
    
    def handleRestart(self):
        self.gameField.clear()
        self.gameScore=0
        self.gameLevel=1
        self.gameSpeed=50
        