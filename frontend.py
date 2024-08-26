import pygame

def printObjects(screen,grid,currentFigure):
    screen.fill((0, 0, 0))
    [pygame.draw.rect(screen,(40,40,40),ptrOnRect,1) for ptrOnRect in grid] 
    for square in currentFigure: 
        pygame.draw.rect(screen,pygame.Color('White'),square) 
    pygame.display.flip() 