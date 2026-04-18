import os

import numpy as np
import pygame

import config

_caches = {}


def _get_frames(kind):
    if kind not in _caches:
        if kind == 'ripple':
            names = [f"ripple_{i}.png" for i in range(config.SPLASH_FRAME_COUNT)]
        else:
            names = [f"wake_{i}.png"   for i in range(config.WAKE_FRAME_COUNT)]
        _caches[kind] = [
            pygame.image.load(
                os.path.join(config.PATH_TO_SPRITES, "splashes", name)
            ).convert_alpha()
            for name in names
        ]
    return _caches[kind]


class Splash:
    def __init__(self, position, size, kind='ripple'):
        self.position = np.array(position, dtype=float)
        self.size     = size
        self.kind     = kind
        self.frame    = 0
        self._tick    = 0
        self.done     = False

    def forward(self):
        self._tick += 1
        speed = config.SPLASH_FRAME_SPEED if self.kind == 'ripple' else config.WAKE_FRAME_SPEED
        if self._tick % speed == 0:
            self.frame += 1
            limit = config.SPLASH_FRAME_COUNT if self.kind == 'ripple' else config.WAKE_FRAME_COUNT
            if self.frame >= limit:
                self.done = True

    def render(self, screen):
        if self.done:
            return
        img  = pygame.transform.scale(_get_frames(self.kind)[self.frame], self.size)
        rect = img.get_rect()
        rect.center = (int(self.position[0]), int(self.position[1]))
        screen.blit(img, rect)
