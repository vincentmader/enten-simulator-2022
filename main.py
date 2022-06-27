import sys
import numpy as np
import pygame
import time

pygame.init()

width = 2*640
height = 2*480
size = width, height
velocity = np.array([0, 0])
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("duck-happy.gif")
ball = pygame.transform.scale(ball, (100, 100))
ballrect = ball.get_rect()

v = 1

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # X
            if event.key == pygame.K_LEFT:
                # ballrect = ballrect.move([-v, 0])
                velocity[0] = int(velocity[0] - 10)
            if event.key == pygame.K_RIGHT:
                # ballrect = ballrect.move([v, 0])
                velocity[0] = int(velocity[0] + 10)
            # Y
            if event.key == pygame.K_DOWN:
                # ballrect = ballrect.move([0, v])
                velocity[1] = int(velocity[1] + 10)
            if event.key == pygame.K_UP:
                # ballrect = ballrect.move([0, -v])
                velocity[1] = int(velocity[1] - 10)
            if event.key == pygame.K_SPACE:
                soundObj = pygame.mixer.Sound('quack.mp3')
                soundObj.play()
                # soundObj.stop()

    velocity = np.array([int(0.9999 * i) for i in velocity])

    speed = sum([i**2 for i in velocity])
    # if speed > 1:
    #     new_speed = [int(i * 0.7) for i in velocity]
    #     velocity = np.array([new_speed / speed * i for i in velocity])
    #     print(velocity)
    print(speed)

    ballrect = ballrect.move(velocity)

    x_min = ballrect.left
    x_max = ballrect.right
    y_min = ballrect.top
    y_max = ballrect.bottom

    if x_min < 0:
        ballrect.left += size[0]
    elif x_max > width:
        ballrect.right -= size[0]
    if y_max < 0:
        ballrect.top += size[1]
    elif y_min > height:
        ballrect.bottom -= size[1]

    screen.fill(white)
    screen.blit(ball, ballrect)
    pygame.display.flip()
