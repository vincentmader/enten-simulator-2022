import os

import numpy as np
import pygame
from random import randint

import config
from config import SIZE_DUCK
import utils

acceleration = 1.5

class Duck:
    def __init__(self, position):
        self.is_leader = False
        self.position = position
        self.velocity = np.array([0., 0.])

        self.type_id = 0
        self.orientation_id = 0
        self.animation_phase_id = 0

    def forward(self, game):
        if not self.is_leader and game.frame_id % 60 == 0:
            self.velocity += np.array([randint(-1, 1), randint(-1, 1)])
            self.velocity *= 0.9
        self.position = self.position + self.velocity * config.DT

        if self.position[0] < 0 or config.WINDOW_WIDTH < self.position[0]:
            self.velocity[0] *= -1
        if self.position[1] < 0 or config.WINDOW_HEIGHT < self.position[1]:
            self.velocity[1] *= -1

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
        self.orientation_id = utils.get_orientation_id(self.velocity)

        speed = sum([i**2 for i in self.velocity])
        if speed < 0.01:
            self.animation_phase_id = 1
        else:
            if frame_id % 25 == 0:
                self.animation_phase_id += 1
                if self.animation_phase_id > 3:
                    self.animation_phase_id = 0

        x = (self.type_id % 4) * 3 + (self.animation_phase_id if self.animation_phase_id != 3 else 1)
        y = (self.type_id // 4) * 4 + self.orientation_id

        path = os.path.join(config.PATH_TO_SPRITES, f"ducks/{x}_{y}.png")
        img = pygame.image.load(path)

        if self.is_leader:
            img_size = config.SIZE_DUCK
        else:
            img_size = config.SIZE_MINIDUCK
        img = pygame.transform.scale(img, img_size)
        ballrect = img.get_rect()
        ballrect.left = int(self.position[0] - SIZE_DUCK[0]/2)
        ballrect.top = int(self.position[1] - SIZE_DUCK[0]/2)
        screen.blit(img, ballrect)

    def quack(self):
        path = os.path.join(config.PATH_TO_SOUNDS, "quack.mp3")
        soundObj = pygame.mixer.Sound(path)
        soundObj.play()

