import os
import sys
import time

import numpy as np
import pygame

import config
from duck import Duck
from egg import Egg

# PI = np.pi

black = 0, 0, 0
white = 255, 255, 255

class Game:
    def __init__(self):
        self.ducks = []
        self.eggs = []

        self.player = Duck(config.INITIAL_POSITION)
        self.player.is_leader = True
        self.player.age = 10000

        self.is_running = True
        self.frame_id = 0
        self.screen = pygame.display.set_mode(config.WINDOW_SIZE)

        pygame.init()

    def get_entities(self):
        res = ([self.player] + self.ducks + self.eggs)[::-1]
        return res

    def start(self):
        while self.is_running:
            self.forward()
            self.render()

    def forward(self): 
        for event in pygame.event.get():
            self.handle_event(event)

        for entity in self.get_entities():
            entity.forward(self)
    
        self.frame_id += 1

    def render(self):
        self.screen.fill(black)
        
        for entity in self.get_entities():
            entity.render(self.screen, self.frame_id)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # MOVEMENT
            if event.key in [pygame.K_LEFT, pygame.K_h]:
                self.player.move("left")
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                self.player.move("right")
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                self.player.move("down")
            elif event.key in [pygame.K_UP, pygame.K_k]:
                self.player.move("up")
            # QUACK
            elif event.key == pygame.K_q:
                self.player.quack(self)
            # EGG PRODUCTION
            elif event.key == pygame.K_e:
                egg_id = len(self.eggs)
                egg = Egg(egg_id, self.player.type_id, self.player.position)
                self.eggs.append(egg)
            # VARIANT CHANGE
            elif event.key == pygame.K_v:
                self.player.type_id += 1 
                if self.player.type_id > 7:
                    self.player.type_id = 0
            # QUIT GAME
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_h]:
                self.player.move("right")
            elif event.key in [pygame.K_RIGHT, pygame.K_l]:
                self.player.move("left")
            elif event.key in [pygame.K_DOWN, pygame.K_j]:
                self.player.move("up")
            elif event.key in [pygame.K_UP, pygame.K_k]:
                self.player.move("down")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.QUIT: 
            sys.exit()

