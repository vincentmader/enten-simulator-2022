import sys
import numpy as np
import pygame
import time

WINDOW_SCALE = 480
ASPECT_RATIO = 4/3
WINDOW_HEIGHT = WINDOW_SCALE
WINDOW_WIDTH = WINDOW_SCALE * ASPECT_RATIO
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

acceleration = 4

class Game:
    def __init__(self):
        self.entities = []

        pygame.init()
    def start(self):
        velocity = np.array([0, 0])
        black = 0, 0, 0
        white = 255, 255, 255
        
        screen = pygame.display.set_mode(WINDOW_SIZE)
        
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
                ballrect.left += WINDOW_SIZE[0]
            elif x_max > WINDOW_WIDTH:
                ballrect.right -= WINDOW_SIZE[0]
            if y_max < 0:
                ballrect.top += WINDOW_SIZE[1]
            elif y_max > WINDOW_HEIGHT:
                ballrect.bottom -= WINDOW_SIZE[1]
        
            screen.fill(white)
            screen.blit(ball, ballrect)
            pygame.display.flip()
        
            frame_id += 1
    def forward(self):
        for entity in self.entities:
            entitiy.forward()
    def render(self):
        for entity in self.entities:
            entitiy.render()

class Duck:
    def __init__(self, position):
        self.position = position

class Egg:
    def __init__(self, position):
        self.position = position

if __name__ == "__main__":
    game = Game()
    game.start()
    
