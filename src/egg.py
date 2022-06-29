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
        if self.progress > config.EGG_HATCH_TIME:
            duck = Duck(self.position)
            duck.type_id = self.type_id
            for egg in game.eggs:
                if egg.id > self.id:
                    egg.id -= 1
            del game.eggs[self.id]
            game.ducks.append(duck)

    def render(self, screen, frame_id):
        if self.progress / config.EGG_HATCH_TIME < 1/4:
            egg_id = 0
        elif self.progress / config.EGG_HATCH_TIME < 1/2:
            egg_id = 1
        elif self.progress / config.EGG_HATCH_TIME < 3/4:
            egg_id = 2
        else:
            egg_id = 3
        path = os.path.join(config.PATH_TO_SPRITES, f"eggs/egg_{egg_id}.png")

        img = pygame.image.load(path)
        img = pygame.transform.scale(img, SIZE_EGG)
        ballrect = img.get_rect()
        ballrect.left = int(self.position[0] - SIZE_EGG[0]/2)
        ballrect.top = int(self.position[1] - SIZE_EGG[0]/2)
        screen.blit(img, ballrect)
