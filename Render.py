import pygame
import pygame.gfxdraw
from pygame.math import Vector2 as V2
from random import randint, choice, sample, uniform

from Physics import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TARGET_FPS = 60
TIMESTEP_PER_FRAME = 0.05
VIEWPORT_SHIFT_SPEED = 0.01     # viewport widths
VIEWPORT_ZOOM_FACTOR = 1.1
CONSTANT_SCALE_FACTOR = 1.1

MIN_SCREEN_WIDTH = 160          # px
MIN_SCREEN_HEIGHT = 120         # px


class Viewport:
    def __init__(self, topleft, dims):
        self.topleft = V2(topleft)
        self.dims = dims
    
    def shift(self, disp):
        max_dim = max(self.dims)
        self.topleft += (disp[0] * max_dim, disp[1] * max_dim)
    
    def zoom(self, factor):
        self.topleft -= (self.dims[0] * (factor - 1) / 2, self.dims[1] * (factor - 1) / 2)
        self.dims = (self.dims[0] * factor, self.dims[1] * factor)
    
    def refit_to_screen(self, old_screen_dims, new_screen_dims):
        width_scale = new_screen_dims[0] / old_screen_dims[0]
        height_scale = new_screen_dims[1] / old_screen_dims[1]
        self.topleft -= (self.dims[0] * (width_scale - 1) / 2, self.dims[1] * (height_scale - 1) / 2)
        self.dims = (self.dims[0] * width_scale, self.dims[1] * height_scale)


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


# Renders the given system onto img
# viewport aspect ratio should match dims aspect ratio
def render_system(system, viewport, img):
    dims = img.get_size()
    pixels_per_meter = dims[0] / viewport.dims[0]

    def pos_to_render_pos(pos):
        render_vect = (pos - viewport.topleft) * pixels_per_meter
        return (round(render_vect.x), round(render_vect.y))

    for s in system.springs:
        start = pos_to_render_pos(s.endpoints[0].pos)
        end = pos_to_render_pos(s.endpoints[1].pos)
        draw_width = max(2, round(s.k * pixels_per_meter / 60))
        draw_aaline(img, start, end, BLACK, width=draw_width)
    
    for b in system.bodies:
        center = pos_to_render_pos(b.pos)
        radius = round(b.radius * pixels_per_meter)
        pygame.gfxdraw.filled_circle(img, *center, radius, b.color)
        pygame.gfxdraw.aacircle(img, *center, radius, b.color)

    return img


def run_system(system):
    viewport = Viewport((0, 0), (8, 6))
    viewport_vel = V2(0, 0)

    screen_dims = (1000, 800)
    screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)
    screen.fill(WHITE)

    pygame.font.init()
    text_font = pygame.font.SysFont('Arial', 20, bold=True)

    keys_pressed = set()

    alive = True
    clock = pygame.time.Clock()
    while alive:
        clock.tick(TARGET_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.KEYDOWN:
                keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:   # zoom in
                    viewport.zoom(1 / VIEWPORT_ZOOM_FACTOR)
                elif event.button == 5: # zoom out
                    viewport.zoom(VIEWPORT_ZOOM_FACTOR)
            elif event.type == pygame.VIDEORESIZE:
                new_screen_width = max(event.w, MIN_SCREEN_WIDTH)
                new_screen_height = max(event.h, MIN_SCREEN_HEIGHT)
                old_screen_dims = tuple(screen_dims)
                screen_dims = (new_screen_width, new_screen_height)
                screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)
                viewport.refit_to_screen(old_screen_dims, screen_dims)

        if pygame.K_a in keys_pressed:
            viewport_vel.x = -1
        elif pygame.K_d in keys_pressed:
            viewport_vel.x = 1
        else:
            viewport_vel.x = 0

        if pygame.K_w in keys_pressed:
            viewport_vel.y = -1
        elif pygame.K_s in keys_pressed:
            viewport_vel.y = 1
        else:
            viewport_vel.y = 0
        
        if pygame.K_SPACE in keys_pressed:
            system.agitate()
        
        if pygame.K_UP in keys_pressed:
            system.repulsion_coefficient *= CONSTANT_SCALE_FACTOR
        elif pygame.K_DOWN in keys_pressed:
            system.repulsion_coefficient /= CONSTANT_SCALE_FACTOR

        
        viewport.shift(viewport_vel * VIEWPORT_SHIFT_SPEED)
        
        screen.fill(WHITE)
        render_system(system, viewport, screen)

        actual_fps = clock.get_fps()
        text_img = text_font.render(f'FPS: {round(actual_fps)}', True, BLACK)
        screen.blit(text_img, (2, 2))

        pygame.display.update()
        system.step(TIMESTEP_PER_FRAME)


if __name__ == '__main__':
    # a, b, c = Body((3, 3), 1), Body((5, 4), 3), Body((4, 1), 1)
    # test_system = System(
    #     [a, b, c],
    #     [Spring((a, b), 3, 1, 0.2), Spring((b, c), 1, 1, 0.1)]
    # )

    test_system = System.random(100, 120)

    run_system(test_system)
