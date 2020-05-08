import os
import pygame.image

ASSETS_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'assets'
)

def load_image(filename):
    path = os.path.join(ASSETS_PATH, filename)
    return pygame.image.load(path)


up_arrow_icon = load_image('chevron-up-512.png')
down_arrow_icon = load_image('chevron-down-512.png')

play_icon = load_image('play-96.png')
pause_icon = load_image('pause-96.png')
rewind_icon = load_image('rewind-96.png')