import pygame

from random import randint

def getRandomIndex(index=None):
    randomNumber=index
    while(randomNumber==index):
        randomNumber=randint(0,6)
    return randomNumber

def rotateFigure(currentFigure,gameField,*parameters):
    # currentFigure[0] - center coordinate, point of rotation
    checkValue=checkBorders(currentFigure,gameField,0,0,"ACTION",*parameters)
    
    if checkValue==True:
        for i in range(4):
            x = currentFigure[i].y - currentFigure[0].y
            y = currentFigure[i].x - currentFigure[0].x
            currentFigure[i].x = currentFigure[0].x - x
            currentFigure[i].y = currentFigure[0].y + y


def checkBorders(currentFigure,gameField,add_X,add_Y,state,*parameters):
    checkValue=True
    rectWidth,rectHeight,rectSize=parameters
    checkFigure=[]
    if state=="MOVING":
        checkFigure=[
            pygame.Rect(
                (currentFigure[i].x+add_X),
                (currentFigure[i].y+add_Y),
                rectSize-1,
                rectSize-1
            ) 
            for i in range(4)
        ]
    elif state=="ACTION":
        checkFigure=[
            pygame.Rect(
                (currentFigure[0].x - (currentFigure[i].y - currentFigure[0].y)),
                (currentFigure[0].y + (currentFigure[i].x - currentFigure[0].x)),
                rectSize-1,
                rectSize-1
            ) 
            for i in range(4)
        ]
        
    for i in range(4):
        if (checkFigure[i] in gameField):
            checkValue=False
        if (checkFigure[i].x) < 0 or (checkFigure[i].x) > rectWidth*rectSize-1:
            checkValue=False
        if (checkFigure[i].y) > rectHeight*rectSize-1:
            checkValue=False
            
    return checkValue

def moveFigure(currentFigure,gameField,add_X,add_Y,*parameters):
    checkValue=checkBorders(currentFigure,gameField,add_X,add_Y,"MOVING",*parameters)
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
            
def dropGameField(gameField,rectSize):
    
    countDeletedRows = 0
    saveY=[]
    counter=0
    lenGameField=len(gameField)
    
    for i in range(lenGameField):
        if gameField[i].y in saveY:
            continue
        
        counter=0
        for j in range(lenGameField):
            if gameField[i].y==gameField[j].y:
                counter+=1
                
        if counter==10:
            countDeletedRows+=1
            saveY.append(gameField[i].y)
            
    if countDeletedRows>0:
        saveY=sorted(saveY)
        for y in saveY:
            for i in range(lenGameField-1,-1,-1):
                if gameField[i].y==y:
                    gameField.pop(i)
                    
            for rect in gameField:
                if rect.y<y:
                    rect.y+=rectSize
                    
            lenGameField=len(gameField)

    return countDeletedRows

def countGameScore(gameField,rectSize,gameScore,gameLevel,gameSpeed):
    
    countDeletedRows=dropGameField(gameField,rectSize)
    if countDeletedRows==1:
        gameScore+=100
    elif countDeletedRows==2:
        gameScore+=300
    elif countDeletedRows==3:
        gameScore+=700
    elif countDeletedRows==4:
        gameScore+=1500
    
    gameLevel = 10 if gameScore>=6000 else (1+gameScore//600)
    gameSpeed=50-(gameLevel-1)*4
        
    return gameScore,gameLevel,gameSpeed