from pygame.math import Vector2 as V2
import pygame.gfxdraw
from functools import lru_cache


def draw_aaline(surf, start, end, color, width=2):
    offset = V2(end) - V2(start)
    offset.scale_to_length(width // 2)
    offset = offset.rotate(90)
    points = [
        start + offset,
        start - offset,
        end - offset,
        end + offset
    ]
    pygame.gfxdraw.aapolygon(surf, points, color)
    pygame.gfxdraw.filled_polygon(surf, points, color)


# Binary search to find a font size s.t. the given text fills width_px pixels horizontally
@lru_cache(maxsize=20)  # for good measure
def get_sized_font(font_family, text, width_px, bold=False):
    pygame.font.init()

    size_lower_bound = 8
    size_upper_bound = 200

    font = None
    size = width_px  # initial guess
    while size_upper_bound - size_lower_bound > 1:
        font = pygame.font.SysFont(font_family, size, bold=bold)
        text_size_px = max(font.size(text))
        error = text_size_px - width_px
        # print(size, error, size_lower_bound, size_upper_bound)
        if error >= 0:
            size_upper_bound = size
        else:
            size_lower_bound = size
        size = (size_lower_bound + size_upper_bound) // 2

    return font