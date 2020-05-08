import pygame
import pygame.gfxdraw
from pygame.math import Vector2 as V2
from random import randint, choice, sample, uniform
from functools import lru_cache

from Physics import *
from UIHelpers import *
from UIElements import *
from Colors import *
from Images import *

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


# Renders the given system onto img
# viewport aspect ratio should match dims aspect ratio
def render_system(system, viewport, img):
    dims = img.get_size()
    pixels_per_meter = dims[0] / viewport.dims[0]

    def pos_to_render_pos(pos):
        render_vect = (pos - viewport.topleft) * pixels_per_meter
        return (round(render_vect.x), round(render_vect.y))
    
    def body_in_viewport(body):
        x, y, r = *body.pos, body.radius
        vx, vy, w, h = *viewport.topleft, *viewport.dims
        return vx - r <= x <= vx + w + r and vy - r <= y <= vy + h + r      # TODO: bottom-edge clipping
    
    tl, w, h = viewport.topleft, *viewport.dims
    viewport_points = [tl, tl + (w, 0), tl + (w, h), tl + (0, h)]
    viewport_sides = [(viewport_points[i], viewport_points[i + 1]) for i in range(-1, 3)]
    def spring_in_viewport(spring):
        spring_segment = (spring.endpoints[0].pos, spring.endpoints[1].pos)
        return any(body_in_viewport(b) for b in spring.endpoints) or \
               any(line_segment_intersect(spring_segment, side) for side in viewport_sides)

    # springs
    for s in system.springs:
        if not spring_in_viewport(s): continue
        start = pos_to_render_pos(s.endpoints[0].pos)
        end = pos_to_render_pos(s.endpoints[1].pos)
        draw_width = max(2, round(s.k * pixels_per_meter / 60))
        draw_aaline(img, start, end, BLACK, width=draw_width)
    
    # bodies
    label_padding = 8
    lock_indicator_width = 3
    for b in system.bodies:
        if not body_in_viewport(b): continue
        center = pos_to_render_pos(b.pos)
        radius = round(b.radius * pixels_per_meter)
        if b.locked: draw_aacircle(img, center, radius + lock_indicator_width, BLACK)
        draw_aacircle(img, center, radius, b.color)
        if b.label and radius >= label_padding * 2:
            text = b.label if len(b.label) >= 5 else f' {b.label} '
            label_font = get_sized_font('Arial', text, radius * 2 - label_padding * 2)
            label_img = label_font.render(b.label, True, WHITE) # TODO: change color of text programatically
            topleft = (
                center[0] - label_img.get_width() // 2,
                center[1] - label_img.get_height() // 2
            )
            img.blit(label_img, topleft)

    return img


def run_system(system):
    viewport = Viewport((0, 0), (8, 6))
    viewport_vel = V2(0, 0)

    screen_dims = (1000, 800)
    screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)
    screen.fill(WHITE)

    def update_repulsion(new_value):
        system.repulsion_coefficient = new_value
    
    def update_friction(new_value):
        system.friction_coefficient = new_value
    
    def toggle_animation():
        system.animation_playing = not system.animation_playing
    
    def rewind_animation():
        system.animation_clock = 0

    # Initialize elements
    fps_indicator = Text((2, 2), '')
    repulsion_editor = ValueEditor((2, 50), 'Repulsion', system.repulsion_coefficient, update_repulsion)
    friction_editor = ValueEditor((2, repulsion_editor.rect.bottom + 10), 'Friction', system.friction_coefficient, update_friction)
    play_button = ToggleButton((2, 200), (40, 40), play_icon, pause_icon, toggle_animation, border=False, opacity=False)
    rewind_button = Button((2, 250), (40, 40), rewind_icon, rewind_animation, border=False, opacity=True)
    elements = [
        fps_indicator,
        repulsion_editor,
        friction_editor,
        play_button,
        rewind_button
    ]
    element_selected = None

    keys_pressed = set()
    body_selected = None

    def pixel_to_meter(pos_px):
        meters_per_pixel = viewport.dims[0] / screen_dims[0]
        return viewport.topleft + meters_per_pixel * V2(pos_px)

    def get_element_at_px(pos_px):
        elems_hit = [e for e in elements if e.intersects_point(pos_px)]
        return elems_hit[0] if elems_hit else None

    def get_body_at_px(pos_px):
        pos = pixel_to_meter(pos_px)
        bodies = system.get_bodies_at(pos)
        return bodies[0] if bodies else None    # return the first one arbitrarily

    alive = True
    clock = pygame.time.Clock()
    while alive:
        clock.tick(TARGET_FPS)

        # handle user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # quit gracefully
                alive = False
                continue

            elif event.type == pygame.KEYDOWN:
                keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:       # select body or press button
                    body_selected = get_body_at_px(event.pos)
                    element_selected = get_element_at_px(event.pos)
                    if element_selected:
                        element_selected.handle_mouse_down(event.pos)

                elif event.button == 3:     # lock body
                    body = get_body_at_px(event.pos)
                    if body: body.toggle_lock()
                elif event.button == 4:     # zoom in
                    viewport.zoom(1 / VIEWPORT_ZOOM_FACTOR)
                elif event.button == 5:     # zoom out
                    viewport.zoom(VIEWPORT_ZOOM_FACTOR)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    body_selected = None
                    if element_selected:
                        element_selected.handle_mouse_up(event.pos)
                        element_selected = None

            elif event.type == pygame.VIDEORESIZE:
                new_screen_width = max(event.w, MIN_SCREEN_WIDTH)
                new_screen_height = max(event.h, MIN_SCREEN_HEIGHT)
                old_screen_dims = tuple(screen_dims)
                screen_dims = (new_screen_width, new_screen_height)
                screen = pygame.display.set_mode(screen_dims, pygame.RESIZABLE)
                viewport.refit_to_screen(old_screen_dims, screen_dims)

        # handle viewport state changes
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
        
        viewport.shift(viewport_vel * VIEWPORT_SHIFT_SPEED)

        # handle system state changes
        if pygame.K_SPACE in keys_pressed:
            system.agitate()
        
        # if pygame.K_UP in keys_pressed:
        #     system.repulsion_coefficient *= CONSTANT_SCALE_FACTOR
        # elif pygame.K_DOWN in keys_pressed:
        #     system.repulsion_coefficient /= CONSTANT_SCALE_FACTOR
        
        if body_selected:
            pos_px = pygame.mouse.get_pos()
            body_selected.pos = V2(pixel_to_meter(pos_px))
        
        # handle UI element state changes
        actual_fps = clock.get_fps()
        fps_indicator.set_text(f'FPS: {actual_fps:.0f}')
        
        # render current frame
        screen.fill(WHITE)
        render_system(system, viewport, screen)

        for elem in elements:
            elem.render_onto(screen)
        
        # test_rect = pygame.Rect(500, 500, 150, 100)
        # draw_aarectangle(screen, test_rect, BLACK, 10)
        # pygame.draw.rect(screen, (255, 0, 0), test_rect, 1)

        pygame.display.update()

        # step system
        system.step(TIMESTEP_PER_FRAME)


if __name__ == '__main__':
    # a, b, c = Body((3, 3), 1), Body((5, 4), 3), Body((4, 1), 1)
    # test_system = System(
    #     [a, b, c],
    #     [Spring((a, b), 3, 1, 0.2), Spring((b, c), 1, 1, 0.1)]
    # )

    test_system = System.random(100, 120)

    run_system(test_system)
