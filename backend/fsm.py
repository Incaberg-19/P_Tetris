import pygame
from .auxToFsm import *
from enum import Enum
 
class State(Enum):
        START = 0
        SPAWN = 1 
        MOVING = 2
        SHIFTING = 3 
        ATTACHING = 4
        GAMEOVER = 5 
        
class FiniteStateMachine:

    def __init__(self):  
        self.indexState=0
        self.states=list(State)
        self.quit=False
        self.pause=False
        self.lenStatesList=len(self.states)
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
    
    def nextState(self) -> None:
        if (self.indexState+1)!=self.lenStatesList:
            self.indexState+=1
            self.state=self.states[self.indexState]
            
    def previouslyState(self) -> None:
        if (self.indexState-1)!=-1:
            self.indexState-=1
            self.state=self.states[self.indexState]
    
    def checkState(self,wantedState) -> bool:
        if self.state!=None:
            return True if self.states[self.indexState]==wantedState else False
    
    def resetStateMachine(self):
        self.indexState=0
        self.state=self.states[self.indexState]
        
    def handleEvents(self,events):
        for event in events:
            self.handleStop(event)
            if self.pause==False:
                self.handleStart(event)
                self.handleSpawn()
                self.handleMoving(event)
                self.handleShifting("INCYCLE")
                self.handleAction(event)
        if self.pause==False:
            self.handleShifting("OUTCYCLE")
            self.handleTimer()
            self.handleAttaching()
        
    def handleMoving(self,event):
        if self.checkState(State.MOVING):
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT,pygame.K_RIGHT):
                    self.restrictionForShifting=4
                elif event.key==pygame.K_DOWN:
                    self.restrictionForShifting=1
                self.holdTimer = 0
            elif event.type == pygame.KEYUP:
                self.holdTimer = 0
                
    def handleShifting(self,state):
        if self.checkState(State.MOVING):
            self.nextState()
        if self.checkState(State.SHIFTING):
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
            self.previouslyState()
    
    def ProcessMoveFigure(self,pressedKeys):
        if pressedKeys[pygame.K_DOWN]:
            self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45,*self.parameters)
        elif pressedKeys[pygame.K_RIGHT]:
            self.currentFigure=moveFigure(self.currentFigure,self.gameField,45,0,*self.parameters)
        elif pressedKeys[pygame.K_LEFT]:
            self.currentFigure=moveFigure(self.currentFigure,self.gameField,-45,0,*self.parameters)
    
    def handleAction(self,event):
        if self.checkState(State.MOVING) or self.checkState(State.SHIFTING):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rotateFigure(self.currentFigure,self.gameField,*self.parameters)
                
    def handleStop(self,event):
        if event.type == pygame.QUIT:
            self.quit=True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.quit=True
            elif event.key == pygame.K_SPACE:
                if self.checkState(State.MOVING) or self.checkState(State.ATTACHING):
                    self.pause=True if self.pause==False else False
                    
    def handleStart(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.state==None or self.checkState(State.GAMEOVER):
                    self.resetStateMachine()
                    self.handleRestart()
    
    def handleSpawn(self):
        if self.checkState(State.START):
            self.nextState()
        
        if self.checkState(State.SPAWN):
            self.nextState()
    
    def handleTimer(self):
        if self.checkState(State.MOVING):
            if checkBorders(self.currentFigure,self.gameField,0,45,"MOVING",*self.parameters)==False:
                self.nextState()
                self.nextState()
        
        if self.checkState(State.MOVING):
            self.timer+=1
            if self.timer>self.gameSpeed:
                self.timer=0
                self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45,*self.parameters) 
    
    def handleAttaching(self):
        if self.checkState(State.ATTACHING):
            self.gameField=saveFigure(self.currentFigure,self.gameField,self.rectSize)
            self.gameScore,self.gameLevel,self.gameSpeed=countGameScore(self.gameField,self.rectSize,self.gameScore,self.gameLevel,self.gameSpeed)

            self.index=self.nextIndex
            self.nextIndex=getRandomIndex(self.index)
            self.currentFigure=self.model.getCurrentFigure(self.index)
            if checkBorders(self.currentFigure,self.gameField,0,45,"MOVING",*self.parameters)==False:
                self.nextState()
            else:
                self.resetStateMachine()
                self.handleSpawn()
    
    def handleRestart(self):
        self.gameField.clear()
        self.gameScore=0
        self.gameLevel=1
        self.gameSpeed=50
        