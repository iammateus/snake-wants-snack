import os
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from screeninfo import get_monitors
from random import randrange

green = (119, 195, 43)
white = (255, 255, 255)
snakeColor = (94,57,31)
yellow = (204,204,0)

snake = [
    {
        "positionX": 0,
        "positionY": 0
    }
]

food = {}

direction = 'down'

def setWindowPositionCentered(width, height):
    monitors = get_monitors()
    primaryMonitor = monitors[0]
    positionX = primaryMonitor.width / 2 - width / 2
    positionY = primaryMonitor.height / 2 - height / 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (positionX,positionY)
    os.environ['SDL_VIDEO_CENTERED'] = '0'

def setWindowColor(window, rgb):
    window.fill(rgb)

def drawGrid(window, size, rows):
    blockSize = size // rows

    x = 0
    y = 0
    for count in range(rows):
        x += blockSize
        y += blockSize

        pygame.draw.line(window, white, (0, y), (size, y))
        pygame.draw.line(window, white, (x, 0), (x, size))

def redrawWindow(window, size, rows):
    window.fill((119, 195, 43))
    drawGrid(window, size, rows);

def eventListeners():
    global direction

    aux = direction
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        keys = pygame.key.get_pressed()

        if(keys[pygame.K_LEFT]):
            if(aux != 'right'):
                direction = 'left'
                # print('left')
            
        if(keys[pygame.K_RIGHT]):
            if(aux != 'left'):
                direction = 'right'
                # print('right')
            
        if(keys[pygame.K_UP]):
            if(aux != 'down'):
                direction = 'up'
                # print('up')
            
        if(keys[pygame.K_DOWN]):
            if(aux != 'up'):
                direction = 'down'
                # print('down')
            
        if(keys[pygame.K_ESCAPE]):
            pygame.quit()
            exit()      

def redrawSnake(window, size, rows):
    blockSize = size // rows

    for block in snake:
        xPosition = block['positionX'] * blockSize
        yPosition = block['positionY'] * blockSize

        pygame.draw.rect(window, snakeColor, (xPosition + 1, yPosition + 1, blockSize - 1, blockSize - 1))

def redrawFood(window, size, rows):
    blockSize = size // rows

    xPosition = food['positionX'] * blockSize
    yPosition = food['positionY'] * blockSize

    pygame.draw.rect(window, yellow, (xPosition + 1, yPosition + 1, blockSize - 1, blockSize - 1))

def getNextPosition():
    
    global direction
    global snake

    if(direction == "down"):
        x = 0
        y = 1
    elif direction == "up":
        x = 0
        y = -1
    elif direction == "left":
        x = -1
        y = 0
    elif direction == "right":
        x = 1
        y = 0
    
    return {
        "positionX": snake[0]['positionX'] + x,
        "positionY": snake[0]['positionY'] + y
    }

def move():

    aux = snake[0]

    snake[0] = getNextPosition();
    
    index = 0
    for block in snake:
        if index != 0:
            snake[index], aux = aux, snake[index]
        index += 1

def didSnakeEat():
    return snake[0] == food
    
def increaseSnake():
    snake.append({})

def willSnakeHitItsHead(rows):
    nextPosition = getNextPosition()

    for block in snake:
        if nextPosition == block:
            return True
    
    if nextPosition['positionX'] < 0:
        return True
    
    if nextPosition['positionX'] > rows - 1:
        return True
    
    if nextPosition['positionY'] < 0:
        return True
    
    if nextPosition['positionY'] > rows - 1:
        return True

    return False

def changeFoodPosition(rows):
    global food

    randomPosition = {
        "positionX": randrange(rows),
        "positionY": randrange(rows)
    }
    
    while randomPosition in snake:
        randomPosition = {
            "positionX": randrange(rows),
            "positionY": randrange(rows)
        }
    
    food = randomPosition

def main():
    size = 400
    rows = 16

    setWindowPositionCentered(size, size)
    window = pygame.display.set_mode((size, size))
    setWindowColor(window, green)

    clock = pygame.time.Clock()

    changeFoodPosition(rows)
    
    state = True

    while state:

        pygame.time.delay(50)
        clock.tick(8)

        eventListeners()

        if not willSnakeHitItsHead(rows):
            move()
            pass
        else:
            messagebox.showinfo(title='Oh no!', message='You hit your head on the wall')
            pygame.quit()
            exit()

        redrawWindow(window, size, rows)
        redrawFood(window, size, rows)
        redrawSnake(window, size, rows)
        pygame.display.update()
        
        if didSnakeEat():
            increaseSnake()
            changeFoodPosition(rows)

main()