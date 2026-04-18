import os

import numpy as np
import pygame
from random import randint

import background
import config
from config import SIZE_DUCK, DUCK_ACCELERATION, DUCK_GROWUP_TIME
from splash import Splash
import utils

class Duck:
    def __init__(self, position):
        self.age = 0
        self.is_leader = False
        self.position = position
        self.velocity = np.array([0., 0.])

        self.type_id = 0
        self.orientation_id = 0
        self.animation_phase_id = 0

        self.is_following_leader = False
        self.water_immersion = 1.0 if background.is_in_pond(position) else 0.0
        self._was_in_pond = background.is_in_pond(position)

    def forward(self, game):
        if not self.is_leader and game.frame_id % 60 == 0:
            self.velocity += 0.5*np.array([randint(-1, 1), randint(-1, 1)])
            self.velocity *= 0.8
        if self.is_following_leader and not self.is_leader:
            tmp = self.velocity
            v = sum([i**2 for i in tmp])**.5
            pos = game.player.position
            phi = np.arctan2(pos[1] - self.position[1], pos[0] - self.position[0])
            self.velocity = np.array([v * np.cos(phi), v * np.sin(phi)])
        self.position = self.position + self.velocity * config.DT

        # if self.position[0] < 0 or config.WINDOW_WIDTH < self.position[0]:
        #     self.velocity[0] *= -1
        # if self.position[1] < 0 or config.WINDOW_HEIGHT < self.position[1]:
        #     self.velocity[1] *= -1

        if self.position[0] < 0:
            self.position[0] += config.WINDOW_WIDTH
        elif self.position[0] > config.WINDOW_WIDTH:
            self.position[0] -= config.WINDOW_WIDTH
        if self.position[1] < 0:
            self.position[1] += config.WINDOW_HEIGHT
        elif self.position[1] > config.WINDOW_HEIGHT:
            self.position[1] -= config.WINDOW_HEIGHT

        in_pond = background.is_in_pond(self.position)
        target_immersion = 1.0 if in_pond else 0.0
        self.water_immersion += (target_immersion - self.water_immersion) * 0.08

        # Ripple on enter/exit; paired wake particles while moving in water
        wl = self._waterline_pos()
        if in_pond and not self._was_in_pond:
            game.splashes.append(Splash(wl, config.SPLASH_SIZE_LARGE, 'ripple'))
        elif not in_pond and self._was_in_pond:
            game.splashes.append(Splash(wl, config.SPLASH_SIZE_MEDIUM, 'ripple'))
        elif in_pond and game.frame_id % config.SPLASH_INTERVAL == 0:
            speed = np.linalg.norm(self.velocity)
            if speed > 0.5:
                vel_norm = self.velocity / speed
                behind   = wl - vel_norm * 18
                game.splashes.append(Splash(behind, config.SPLASH_SIZE_WAKE, 'wake'))
        self._was_in_pond = in_pond

        foo = randint(1, 5)
        self.age += foo
        # if self.age < DUCK_GROWUP_TIME and self.age + foo >= DUCK_GROWUP_TIME:
        #     self.quack()

    def _waterline_pos(self):
        img_h    = config.SIZE_DUCK[1] if self.is_leader else config.SIZE_MINIDUCK[1]
        clip_px  = self.water_immersion * 0.38 * img_h
        sink_px  = self.water_immersion * 28
        offset_y = img_h / 2 + sink_px - clip_px
        return self.position + np.array([0.0, offset_y])

    def move(self, direction):
        if direction == "right":
            self.velocity[0] = int(self.velocity[0] + DUCK_ACCELERATION)
        elif direction == "left":
            self.velocity[0] = int(self.velocity[0] - DUCK_ACCELERATION)
        elif direction == "up":
            self.velocity[1] = int(self.velocity[1] - DUCK_ACCELERATION)
        elif direction == "down":
            self.velocity[1] = int(self.velocity[1] + DUCK_ACCELERATION)
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
        if self.age < DUCK_GROWUP_TIME:
            path = os.path.join(config.PATH_TO_SPRITES, f"miniducks/{x}_{y}.png")
        else:
            path = os.path.join(config.PATH_TO_SPRITES, f"ducks/{x}_{y}.png")
        img = pygame.image.load(path)

        if self.is_leader:
            img_size = config.SIZE_DUCK
        else:
            img_size = config.SIZE_MINIDUCK
        img = pygame.transform.scale(img, img_size)

        # Clip bottom portion and sink duck into water as immersion increases
        clip_px  = int(self.water_immersion * 0.38 * img_size[1])
        sink_px  = int(self.water_immersion * 28)
        src_rect = pygame.Rect(0, 0, img_size[0], img_size[1] - clip_px)

        left = int(self.position[0] - img_size[0] / 2)
        top  = int(self.position[1] - img_size[1] / 2) + sink_px
        screen.blit(img, (left, top), src_rect)

    def quack(self, world):
        for duck in world.ducks:
            duck.is_following_leader = not duck.is_following_leader
        path = os.path.join(config.PATH_TO_SOUNDS, "quack.mp3")
        soundObj = pygame.mixer.Sound(path)
        soundObj.play()
