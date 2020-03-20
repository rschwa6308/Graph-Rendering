import pygame

from Colors import *
from Images import *
from UIHelpers import *


class UIElement:
    children = []

    def render_onto(self, surf):
        raise NotImplementedError

    def intersects_point(self, pos):
        return self.rect.collidepoint(pos)
    
    def handle_mouse_down(self, pos):
        for child in self.children:
            if child.intersects_point(pos):
                child.handle_mouse_down(pos)
                child.pressed = True
            else:
                child.pressed = False

    def handle_mouse_up(self, pos):
        for child in self.children:
            if child.intersects_point(pos) or child.pressed:
                child.handle_mouse_up(pos)


class Text(UIElement):
    pygame.font.init()
    default_font = pygame.font.SysFont('Arial', 28, bold=False)

    def __init__(self, pos, text, font=default_font, color=BLACK):
        self.pos = pos
        self.font = font
        self.color = color
        self.set_text(text)
    
    def render_onto(self, surf):
        surf.blit(self.img, self.pos)
    
    def set_text(self, text):
        self.text = text
        self.img = self.font.render(text, True, self.color)
        self.rect = pygame.Rect(self.pos, self.img.get_size())


class Button(UIElement):
    border_color = BLACK
    border_width = 1
    press_opacity = 0.5

    def __init__(self, pos, dims, src_img, on_press):
        self.pos = pos
        self.rect = pygame.Rect(pos, dims)

        self.img = pygame.Surface(dims, pygame.SRCALPHA)
        scaled_src_img = pygame.transform.smoothscale(src_img, dims)
        self.img.blit(scaled_src_img, (0, 0))
        # print(self.rect)
        draw_aarectangle(self.img, pygame.Rect((0, 0), self.rect.size), self.border_color, self.border_width)
        self.opacity_filter = pygame.Surface(dims, pygame.SRCALPHA)
        self.opacity_filter.fill((0, 0, 0, round(self.press_opacity * 255)))

        self.on_press = on_press
        self.pressed = False

    def render_onto(self, surf):
        surf.blit(self.img, self.pos)
        if self.pressed:
            surf.blit(self.opacity_filter, self.pos)

    def handle_mouse_down(self, pos):
        self.pressed = True
    
    def handle_mouse_up(self, pos):
        self.pressed = False
        self.on_press()


class ValueEditor(UIElement):
    label_color = BLACK
    label_format = '{0}: {1:.2f}'
    button_dims = (30, 15)
    padding = 2

    def __init__(self, pos, label, initial_value, on_value_changed, factor=1.1):
        self.pos = pos
        self.current_value = initial_value
        self.on_value_changed = on_value_changed
        self.factor = factor

        def modify_value(increase):
            self.current_value *= factor ** (1 if increase else -1)
            self.text.set_text(self.label_format.format(label, self.current_value))
            self.on_value_changed(self.current_value)
        
        up_button_pos = pos
        down_button_pos = (pos[0], pos[1] + self.button_dims[1] + self.padding)
        text_pos = (pos[0] + self.button_dims[0] + self.padding, pos[1])

        self.up_button = Button(up_button_pos, self.button_dims, up_arrow_icon, lambda: modify_value(True))
        self.down_button = Button(down_button_pos, self.button_dims, down_arrow_icon, lambda: modify_value(False))
        self.text = Text(text_pos, self.label_format.format(label, initial_value), color=self.label_color)
        self.children = [self.up_button, self.down_button, self.text]

        self.rect = bounding_box([child.rect for child in self.children])

    def render_onto(self, surf):
        for child in self.children:
            child.render_onto(surf)
