import os
import pygame
import tkinter as tk
from random import randrange
from tkinter import messagebox
from screeninfo import get_monitors

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
    window.fill(green)
    drawGrid(window, size, rows)

def listenToEvents():
    global direction

    aux = direction
    turns = []
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_LEFT]):
        if(aux != 'right'):
            turns.append('left')
        
    if(keys[pygame.K_RIGHT]):
        if(aux != 'left'):
            turns.append('right')
        
    if(keys[pygame.K_UP]):
        if(aux != 'down'):
            turns.append('up')
        
    if(keys[pygame.K_DOWN]):
        if(aux != 'up'):
            turns.append('down')
        
    if(keys[pygame.K_ESCAPE]):
        pygame.quit()
        exit()      
    
    if len(turns) > 0:
        for turn in turns:
            if turn != aux:
                print("CHANGING FROM: " + direction + " to " + turn)
                direction = turn

def redrawElement(window, size, rows, element, color):
    blockSize = size // rows

    for block in element:
        # (position) + 1 for a better positioning of the block
        positionX = block['positionX'] * blockSize + 1
        positionY = block['positionY'] * blockSize + 1

        pygame.draw.rect(window, color, (positionX, positionY, blockSize - 1, blockSize - 1))

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

    print('moving')
    aux = snake[0]

    snake[0] = getNextPosition()
    
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

def messageBox(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(title=subject, message=content)

def main():
    size = 400
    rows = 16

    setWindowPositionCentered(size, size)
    window = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Snake wants snack!")

    clock = pygame.time.Clock()

    changeFoodPosition(rows)
    
    state = True
    while state:

        pygame.time.delay(50)
        clock.tick(8)

        listenToEvents()

        if not willSnakeHitItsHead(rows):
            move()
        else:
            messageBox('Oh no!', 'You hit your head on the wall!')
            pygame.quit()
            exit()

        redrawWindow(window, size, rows)
        redrawElement(window, size, rows, [ food ], yellow)
        redrawElement(window, size, rows, snake, snakeColor)
        pygame.display.update()
        
        if didSnakeEat():
            increaseSnake()
            changeFoodPosition(rows)

main()