import sys
import numpy as np
import pygame
import time

class Game:
    def __init__(self):
        self.ducks = []
        self.eggs = []
    def forward(self):
        pass
    def render(self):
        for duck in ducks:
            duck.render()
        for egg in eggs:
            egg.render()

class Duck:
    def __init__(self, position):
        self.position = position

class Egg:
    def __init__(self, position):
        self.position = position
        

pygame.init()

width = 640
height = 480
scale = 1
size = scale*width, scale*height
velocity = np.array([0, 0])
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("duck-happy.gif")
ball = pygame.transform.scale(ball, (100, 100))
ballrect = ball.get_rect()

v = 1

frame_id = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # X Movement
            if event.key in [pygame.K_LEFT, pygame.K_h]:
                velocity[0] = int(velocity[0] - acceleration)
            if event.key in [pygame.K_RIGHT, pygame.K_l]:
                velocity[0] = int(velocity[0] + acceleration)
            # Y Movement
            if event.key in [pygame.K_DOWN, pygame.K_j]:
                velocity[1] = int(velocity[1] + acceleration)
            if event.key in [pygame.K_UP, pygame.K_k]:
                velocity[1] = int(velocity[1] - acceleration)
            #  quack
            if event.key == pygame.K_SPACE:
                soundObj = pygame.mixer.Sound('quack.mp3')
                soundObj.play()
            if event.key == pygame.K_e:
                egg = Egg()
                eggs.append(egg)

    if frame_id % 10 == 0:
        velocity = np.array([int(0.9999 * i) for i in velocity])
        # velocity = np.array([i-1 if i>10 else i for i in velocity])

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

    if x_max < 0:
        ballrect.left += size[0]
    elif x_max > width:
        ballrect.right -= size[0]
    if y_max < 0:
        ballrect.top += size[1]
    elif y_max > height:
        ballrect.bottom -= size[1]

    screen.fill(white)
    screen.blit(ball, ballrect)
    pygame.display.flip()

    frame_id += 1
