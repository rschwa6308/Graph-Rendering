import pygame
from pygame.math import Vector2 as V2
from random import randint, choice, sample, uniform

from Graphs import Graph
from Physics import *



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TARGET_FPS = 120
TIMESTEP_PER_FRAME = 0.05
VIEWPORT_SHIFT_SPEED = 0.1
VIEWPORT_ZOOM_SPEED = 0.3

MIN_SCREEN_WIDTH = 160   # px
MIN_SCREEN_HEIGHT = 120  # px


class Viewport:
    def __init__(self, topleft, dims):
        self.topleft = V2(topleft)
        self.dims = dims
    
    def shift(self, disp):
        self.topleft += disp
    
    def zoom(self, dist):
        self.topleft += V2(1, 1) * dist
        self.dims -= V2(2, 2) * dist


# viewport aspect ratio should match dims aspect ratio
def render_system(system, viewport, dims):
    img = pygame.Surface(dims)
    img.fill(WHITE)

    pixels_per_meter = dims[0] / viewport.dims[0]
    def pos_to_render_pos(pos):
        render_vect = (pos - viewport.topleft) * pixels_per_meter
        return (round(render_vect.x), round(render_vect.y))

    for s in system.springs:
        start = pos_to_render_pos(s.endpoints[0].pos)
        end = pos_to_render_pos(s.endpoints[1].pos)
        pygame.draw.line(img, BLACK, start, end, round(s.k * pixels_per_meter / 20))
    
    for b in system.bodies:
        pygame.draw.circle(img, b.color, pos_to_render_pos(b.pos), round(b.radius * pixels_per_meter))

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
                if event.key == pygame.K_SPACE:
                    system.agitate()
            elif event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:   # zoom in
                    viewport.zoom(VIEWPORT_ZOOM_SPEED)
                elif event.button == 5: # zoom out
                    viewport.zoom(-VIEWPORT_ZOOM_SPEED)
            elif event.type == pygame.VIDEORESIZE:
                new_screen_width = max(event.w, MIN_SCREEN_WIDTH)
                new_screen_height = max(event.h, MIN_SCREEN_HEIGHT)
                screen_dims = (new_screen_width, new_screen_height)
                screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)
                # TODO: update viewport here

        if pygame.K_LEFT in keys_pressed:
            viewport_vel.x = -1
        elif pygame.K_RIGHT in keys_pressed:
            viewport_vel.x = 1
        else:
            viewport_vel.x = 0

        if pygame.K_UP in keys_pressed:
            viewport_vel.y = -1
        elif pygame.K_DOWN in keys_pressed:
            viewport_vel.y = 1
        else:
            viewport_vel.y = 0
        
        viewport.shift(viewport_vel * VIEWPORT_SHIFT_SPEED)
        
        img = render_system(system, viewport, screen_dims)
        screen.blit(img, (0, 0))

        actual_fps = clock.get_fps()
        text_img = text_font.render(f'FPS: {round(actual_fps)}', True, BLACK)
        screen.blit(text_img, (2, 2))

        pygame.display.update()
        system.step(TIMESTEP_PER_FRAME)


if __name__ == '__main__':
    # test_graph = Graph(
    #     [1, 2, 3, 4, 5],
    #     [(1, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1), (1, 4, 1)]
    # )
    # test_system = System.from_graph(test_graph)

    test_graph = Graph.complete_graph(11)
    test_system = System.from_graph(test_graph, max_spring_length=2)

    # a, b, c = Body((3, 3), 1), Body((5, 4), 3), Body((4, 1), 1)
    # test_system = System(
    #     [a, b, c],
    #     [Spring((a, b), 3, 1, 0.2), Spring((b, c), 1, 1, 0.1)]
    # )

    # test_system = System.random(10, 20)

    run_system(test_system)
