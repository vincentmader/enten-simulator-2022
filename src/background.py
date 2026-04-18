import pygame
import numpy as np

import config

COLOR_GRASS        = (88,  148,  54)
COLOR_GRASS_DARK   = (72,  124,  44)
COLOR_POND_SHALLOW = (82,  148, 212)   # near edge
COLOR_POND_DEEP    = (38,   88, 168)   # centre
COLOR_POND_BANK    = (72,  130,  60)   # muddy bank ring
COLOR_SHIMMER      = (155, 205, 242)
COLOR_PAD          = (52,  118,  52)
COLOR_PAD_DARK     = (36,   88,  36)
COLOR_FLOWER       = (245, 185, 200)

_surface = None


def _lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def _in_ellipse(x, y, cx, cy, rx, ry):
    dx, dy = (x - cx) / rx, (y - cy) / ry
    return dx*dx + dy*dy <= 1.0


def _build_surface():
    surf = pygame.Surface((int(config.WINDOW_WIDTH), int(config.WINDOW_HEIGHT)))
    cx   = int(config.POND_CENTER[0])
    cy   = int(config.POND_CENTER[1])
    rx   = config.POND_RADIUS_X
    ry   = config.POND_RADIUS_Y

    surf.fill(COLOR_GRASS)
    _draw_grass(surf)
    _draw_pond_gradient(surf, cx, cy, rx, ry)
    _draw_shimmer(surf, cx, cy, rx, ry)
    _draw_lily_pads(surf, cx, cy, rx, ry)

    return surf


def _draw_grass(surf):
    rng = np.random.default_rng(42)
    xs  = rng.integers(0, int(config.WINDOW_WIDTH),  1800)
    ys  = rng.integers(0, int(config.WINDOW_HEIGHT), 1800)
    for x, y in zip(xs, ys):
        pygame.draw.rect(surf, COLOR_GRASS_DARK, (x, y, 2, 4))


def _draw_pond_gradient(surf, cx, cy, rx, ry):
    # Muddy bank — slightly larger than pond
    pygame.draw.ellipse(surf, COLOR_POND_BANK,
                        (cx - rx - 14, cy - ry - 14, 2*(rx+14), 2*(ry+14)))

    # Gradient: draw filled ellipses from edge (shallow) inward (deep)
    N = 40
    for i in range(N, 0, -1):
        t    = i / N                          # 1.0 at edge → 0.0 at centre
        col  = _lerp(COLOR_POND_DEEP, COLOR_POND_SHALLOW, t ** 0.6)
        rx_i = max(1, int(rx * t))
        ry_i = max(1, int(ry * t))
        pygame.draw.ellipse(surf, col,
                            (cx - rx_i, cy - ry_i, 2*rx_i, 2*ry_i))


def _draw_shimmer(surf, cx, cy, rx, ry):
    rng = np.random.default_rng(7)
    for _ in range(160):
        for _ in range(30):
            px = int(rng.uniform(cx - rx, cx + rx))
            py = int(rng.uniform(cy - ry, cy + ry))
            if _in_ellipse(px, py, cx, cy, rx, ry):
                break
        else:
            continue

        length = int(rng.uniform(8, 28))
        angle  = rng.uniform(-0.25, 0.25)
        ex = px + int(length * np.cos(angle))
        ey = py + int(length * np.sin(angle))
        pygame.draw.line(surf, COLOR_SHIMMER, (px, py), (ex, ey), 1)


def _draw_lily_pads(surf, cx, cy, rx, ry):
    aspect    = ry / rx          # pond foreshortening ratio (~0.71)
    rng       = np.random.default_rng(13)

    for _ in range(10):
        for _ in range(60):
            angle = rng.uniform(0, 2 * np.pi)
            r     = rng.uniform(0.25, 0.78)
            px    = int(cx + rx * r * np.cos(angle))
            py    = int(cy + ry * r * np.sin(angle))
            if _in_ellipse(px, py, cx, cy, rx * 0.82, ry * 0.82):
                break
        else:
            continue

        pad_rx      = int(rng.uniform(18, 34))
        pad_ry      = max(1, int(pad_rx * aspect))
        notch_angle = rng.uniform(0, 2 * np.pi)

        # Main pad (ellipse matching pond perspective)
        pygame.draw.ellipse(surf, COLOR_PAD,
                            (px - pad_rx, py - pad_ry, 2*pad_rx, 2*pad_ry))

        # Notch cut-out — triangle from centre to ellipse rim
        notch = [
            (px, py),
            (px + int(pad_rx * np.cos(notch_angle - 0.35)),
             py + int(pad_ry * np.sin(notch_angle - 0.35))),
            (px + int(pad_rx * np.cos(notch_angle + 0.35)),
             py + int(pad_ry * np.sin(notch_angle + 0.35))),
        ]
        water_col = _lerp(COLOR_POND_DEEP, COLOR_POND_SHALLOW, r ** 0.6)
        pygame.draw.polygon(surf, water_col, notch)

        # Rim
        pygame.draw.ellipse(surf, COLOR_PAD_DARK,
                            (px - pad_rx, py - pad_ry, 2*pad_rx, 2*pad_ry), 2)

        # Optional small flower
        if rng.random() < 0.45:
            pygame.draw.circle(surf, COLOR_FLOWER, (px, py), 5)
            pygame.draw.circle(surf, (255, 225, 235), (px, py), 2)


def render(screen):
    global _surface
    if _surface is None:
        _surface = _build_surface()
    screen.blit(_surface, (0, 0))


def is_in_pond(position):
    dx = (position[0] - config.POND_CENTER[0]) / config.POND_RADIUS_X
    dy = (position[1] - config.POND_CENTER[1]) / config.POND_RADIUS_Y
    return dx*dx + dy*dy <= 1.0
