#!/usr/bin/env python3

import sys
import numpy as np
import pygame
import time

PI = np.pi
WINDOW_SCALE = 480*2
ASPECT_RATIO = 4/3
WINDOW_HEIGHT = WINDOW_SCALE
WINDOW_WIDTH = WINDOW_SCALE * ASPECT_RATIO
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
INITIAL_POSITION = np.array([0, 0])
DT = 1
SIZE_DUCK = (200, 200)
SIZE_EGG = (20, 20)

acceleration = 4
black = 0, 0, 0
white = 255, 255, 255

def initialize_entitites():
    entities = []

    player = Duck(INITIAL_POSITION)
    entities.append(player)

    return entities

class Game:
    def __init__(self):
        self.entities = initialize_entitites()
        self.is_running = True
        self.frame_id = 0
        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        pygame.init()

    def start(self):
        while self.is_running:
            self.forward()
            self.render()

    def forward(self): 
        player = self.entities[0]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # X Movement
                if event.key in [pygame.K_LEFT, pygame.K_h]:
                    player.move("left")
                if event.key in [pygame.K_RIGHT, pygame.K_l]:
                    player.move("right")
                # Y Movement
                if event.key in [pygame.K_DOWN, pygame.K_j]:
                    player.move("down")
                if event.key in [pygame.K_UP, pygame.K_k]:
                    player.move("up")
                #  quack
                if event.key == pygame.K_SPACE:
                    player.quack()
                if event.key == pygame.K_e:
                    egg = Egg(player.position)
                    self.entities.append(egg)
            if event.type == pygame.QUIT: 
                sys.exit()

        for entity in self.entities:
            entity.forward()
    
        self.frame_id += 1

    def render(self):
        self.screen.fill(black)
        
        for entity in self.entities[::-1]:
            entity.render(self.screen, self.frame_id)

        # ballrect = ballrect.move(velocity)
    
        # x_min = ballrect.left
        # x_max = ballrect.right
        # y_min = ballrect.top
        # y_max = ballrect.bottom
    
        # if x_max < 0:
        #     ballrect.left += WINDOW_SIZE[0]
        # elif x_max > WINDOW_WIDTH:
        #     ballrect.right -= WINDOW_SIZE[0]
        # if y_max < 0:
        #     ballrect.top += WINDOW_SIZE[1]
        # elif y_max > WINDOW_HEIGHT:
        #     ballrect.bottom -= WINDOW_SIZE[1]

        pygame.display.flip()

class Duck:
    def __init__(self, position):
        self.position = position
        self.velocity = np.array([0., 0.])
        self.type_id = 0
        self.animation_phase_id = 0

    def forward(self):
        self.position = self.position + self.velocity * DT
        self.velocity *= 0.95

        speed = sum([i**2 for i in self.velocity])
        if speed < 0.01:
            self.animation_phase_id = 1
        else:
            self.animation_phase_id += 1
            if self.animation_phase_id > 3:
                self.animation_phase_id = 0

    def move(self, direction):
        if direction == "right":
            self.velocity[0] = int(self.velocity[0] + acceleration)
        elif direction == "left":
            self.velocity[0] = int(self.velocity[0] - acceleration)
        elif direction == "up":
            self.velocity[1] = int(self.velocity[1] - acceleration)
        elif direction == "down":
            self.velocity[1] = int(self.velocity[1] + acceleration)
        else:
            raise Exception("")

    def render(self, screen, frame_id):
        orientation_id = get_orientation_id(self.velocity)
        # animation_phase_id = 50*int(frame_id/50) % 4

        x = self.type_id * 3 + (self.animation_phase_id if self.animation_phase_id != 3 else 1)
        y = self.type_id * 4 + orientation_id
        
        img_id = [x, y]
        img = pygame.image.load(f"sprites/ducks/{img_id[0]}_{img_id[1]}.png")

        img = pygame.transform.scale(img, SIZE_DUCK)
        ballrect = img.get_rect()
        ballrect.left = int(self.position[0] - SIZE_DUCK[0]/2)
        ballrect.top = int(self.position[1] - SIZE_DUCK[0]/2)
        screen.blit(img, ballrect)

    def quack(self):
        soundObj = pygame.mixer.Sound('quack.mp3')
        soundObj.play()

class Egg:
    def __init__(self, position):
        self.position = position

    def forward(self):
        pass

    def render(self, screen, frame_id):
        img = pygame.image.load('sprites/egg.png')
        img = pygame.transform.scale(img, SIZE_EGG)
        screen.blit(img, self.position)

def get_orientation_id(velocity):
    theta = np.arctan2(velocity[1], velocity[0])
    # right
    if -PI/4 < theta <= PI/4:
        orientation_id = 2 
    # top
    elif PI/4 < theta <= 3*PI/4:
        orientation_id = 0 
    # down
    elif -PI/4 >= theta > -3*PI/4:
        orientation_id = 3 
    # left
    elif theta < -3*PI/4 or theta > 3*PI/4:
        orientation_id = 1 
    else:
        raise Exception(f"angle: {theta/PI}")
    return orientation_id

if __name__ == "__main__":
    game = Game()
    game.start()
