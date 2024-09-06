import pygame
from .auxToFsm import *
from enum import Enum
import sys

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
        self.direction=None
        self.state=None 
        self.timer=0
        self.shiftingTimer=0
        self.timerShiftingLeft=0
        self.timerShiftingRight=0
        self.timerShiftingDown=0
        self.holdDown=False
        self.holdDown2=0
        self.holdLeft=False
        self.holdRight=False
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
            self.handleMovement(event)
            self.handleAction(event)
        self.handleTimer()
        self.handleAttaching()
        
    
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

    def handleMovement(self,event):
        if self.state==States.MOVING:        
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT):
                        self.state = States.SHIFTING
        if self.state == States.SHIFTING:
            if event.key==pygame.K_DOWN:
                self.currentFigure=moveFigure(self.currentFigure,self.gameField,0,45,*self.parameters)
            elif event.key==pygame.K_LEFT:
                self.currentFigure=moveFigure(self.currentFigure,self.gameField,-45,0,*self.parameters)
            elif event.key==pygame.K_RIGHT:
                self.currentFigure=moveFigure(self.currentFigure,self.gameField,45,0,*self.parameters)
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
    
    def printState(self):
        print(self.state)
        