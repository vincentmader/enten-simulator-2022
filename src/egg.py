import os
import random

import numpy as np
import pygame

import config
from config import SIZE_EGG
from duck import Duck

class Egg:
    def __init__(self, egg_id, type_id, position):
        self.position = position
        self.progress = 0
        self.id = egg_id
        self.type_id = type_id

    def forward(self, game):
        self.progress += random.randint(0, 10)
        if self.progress > 1000:
            duck = Duck(self.position)
            duck.type_id = self.type_id
            for egg in game.eggs:
                if egg.id > self.id:
                    egg.id -= 1
            del game.eggs[self.id]
            game.ducks.append(duck)

    def render(self, screen, frame_id):
        path = os.path.join(config.PATH_TO_SPRITES, f"egg.png")

        img = pygame.image.load(path)
        img = pygame.transform.scale(img, SIZE_EGG)
        ballrect = img.get_rect()
        ballrect.left = int(self.position[0] - SIZE_EGG[0]/2)
        ballrect.top = int(self.position[1] - SIZE_EGG[0]/2)
        screen.blit(img, ballrect)
