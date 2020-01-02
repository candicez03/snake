#########################################
# File Name: Snake_candiceZ.py
# Description: This program is an implementation of snake using pygame.
# Author: Candice Zhang
# Date: 02/11/2018
#########################################
from random import randint
import pygame,time
pygame.init()
WIDTH  = 800
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

TOP = 0
BOTTOM = HEIGHT
LEFT = 0
RIGHT = WIDTH
MIDDLE = int(WIDTH/2.0)

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
outline = 0
font = pygame.font.SysFont("Courier New Bold",24)

#---------------------------------------#
# functions                             #
#---------------------------------------#
def redrawGameWindow():
    gameWindow.blit(bgPic,(0,0)) 
    # draw the information about the game
    graphics1 = font.render('SNAKE feat. Tim Cook',1,BLACK)
    gameWindow.blit(graphics1,(50,50))
    graphics2 = font.render('made by Candice Zhang',1,BLACK)
    gameWindow.blit(graphics2,(50,100))
    # draw the snake
    for i in range(len(segX)):
        if i == 0:
            blitPic = snakeHeadPic
        else:
            blitPic = snakeSegPic
        gameWindow.blit(blitPic,(segX[i],segY[i]))
    # draw the apple
    for i in range(len(appleX)):
        gameWindow.blit(applePic,(appleX[i],appleY[i]))
    # draw the remaining time, score and current difficulty
    if gameStatus == 1:
        graphics3 = font.render(('time:'+str(maxTime - int(time.time()-startTime))),1,BLACK)
        gameWindow.blit(graphics3,(50,150))
    else:
        graphics3 = font.render('press SPACE to restart, press ESC to quit',1,BLACK)
        gameWindow.blit(graphics3,(50,150))
    graphics4 = font.render(('score:'+str(score)),1,BLACK)
    gameWindow.blit(graphics4,(50,200))
    graphics5 = font.render(('difficulty level:'+str(score/5+1)),1,BLACK)
    gameWindow.blit(graphics5,(50,250))
    # draw tips
    graphics5 = font.render('collect 2 apples in 3 seconds for extra time!',1,BLACK)
    gameWindow.blit(graphics5,(50,300))
    pygame.display.update()

def generateApple():
    appleNum = 0
    while appleNum < 1:
        tempX, tempY = randint(LEFT,RIGHT), randint(TOP,BOTTOM)
        flag = 1
        for i in range(len(segX)):
            if tempX == segX[i] and tempY == segY[i]:
                flag = 0
        for i in range(len(appleX)):
            if tempX == appleX[i] and tempY == appleY[i]:
                flag = 0
        if flag == 1:
            appleX.append(tempX)
            appleY.append(tempY)
            appleNum += 1
    return
#---------------------------------------#
# main program                          #
#---------------------------------------#

# maximum time in seconds for the game
maxTime = 20

# snake's properties
SEGMENT_R = 15
HSTEP = SEGMENT_R *2
VSTEP = SEGMENT_R *2
stepX = 0
stepY = -VSTEP
segX = []
segY = []
for i in range(4):
    segX.append(MIDDLE)
    segY.append(BOTTOM + i*VSTEP)
score = 0

# apple's properties
APPLE_R  = 15
appleX = []
appleY = []

#load pictures
bgPic = pygame.transform.scale(pygame.image.load('assets/background.jpg'),(WIDTH,HEIGHT))
applePic = pygame.transform.scale(pygame.image.load('assets/apple.png'),(APPLE_R*2,APPLE_R*2))
snakeHeadPic = pygame.transform.scale(pygame.image.load('assets/head.png'),(SEGMENT_R*2,SEGMENT_R*2))
snakeSegPic = pygame.transform.scale(pygame.image.load('assets/body.png'),(SEGMENT_R*2,SEGMENT_R*2))

#--------------------------------#
inPlay = True
clock = pygame.time.Clock()
gameStatus = 1    # 1:playing 2:waiting for restart
startTime  = time.time()
tickSpeed  = 15
counter  = -1 # record the last time that an apple is added
counter2 = -1 # record the last time that an apple is eaten
while inPlay:
    redrawGameWindow()
    clock.tick(tickSpeed+(score/5)*5)
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if gameStatus == 1:
        if keys[pygame.K_LEFT]:
            if not(stepX == HSTEP and stepY == 0):
                stepX = -HSTEP
                stepY = 0
        if keys[pygame.K_RIGHT]:
            if not(stepX == -HSTEP and stepY == 0):
                stepX = HSTEP
                stepY = 0
        if keys[pygame.K_UP]:
            if not(stepX == 0 and stepY == VSTEP):
                stepX = 0
                stepY = -VSTEP
        if keys[pygame.K_DOWN]:
            if not(stepX == 0 and stepY == -VSTEP):
                stepX = 0
                stepY = VSTEP
        
# move the segments
        lastIndex = len(segX)-1
        for i in range(lastIndex,0,-1):     # starting from the tail, and going backwards:
            segX[i]=segX[i-1]               # every segment takes the coordinates
            segY[i]=segY[i-1]               # of the previous one

# move the head
        segX[0] = segX[0] + stepX
        segY[0] = segY[0] + stepY
        for i in range(lastIndex,0,-1):     # starting from the tail, and going backwards:
            if segX[i] == segX[0] and segY[i] == segY[0]: # if the head and the body overlaps
                    redrawGameWindow()
                    gameStatus = 0
        if segX[0]< LEFT or segX[0]> RIGHT or segY[0] < TOP or segY[0] > BOTTOM:
            gameStatus = 0
# detect when the snake eats the apple
        for i in range(len(appleX)):
            if abs(segX[0]-appleX[i])<=SEGMENT_R and abs(segY[0]-appleY[i])<=SEGMENT_R:
                # remove the apple
                appleX.pop(i)
                appleY.pop(i)
                # add 2 segments to the snake
                for i in range(2):
                    segX.append(segX[-1])
                    segY.append(segY[-1])
                score+=1
                # if two apples are eaten within 3 secs, boost up 5 secs
                if time.time()-counter2 <= 3:
                    maxTime += 5
                counter2 = time.time()
                generateApple()
                break
# generate an apple every other 5 seconds
        passedSeconds = int(time.time() - startTime)
        if passedSeconds %5 == 0 and passedSeconds != counter:
            generateApple()
            counter = passedSeconds
# if run out of time then end the game
        if int(time.time()-startTime) > maxTime:
            gameStatus = 0
# press space to restart the game
    elif gameStatus == 0:
        if keys[pygame.K_SPACE]:
            segX = []
            segY = []
            for i in range(4):
                segX.append(MIDDLE)
                segY.append(BOTTOM + i*VSTEP)
            stepX = 0
            stepY = -VSTEP
            APPLE_R  = 10
            appleX = []
            appleY = []
            score = 0
            counter  = -1
            counter2 = -1
            maxTime = 20
            startTime  = time.time()
            gameStatus = 1
#---------------------------------------#    
pygame.quit()
