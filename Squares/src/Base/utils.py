'''
Created on 2013-09-21

@author: Davide
'''
import pygame, os

CUR_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(CUR_DIR, '../../data/images/')
SOUND_DIR = os.path.join(CUR_DIR, '../../data/sounds/')
FONT_DIR = os.path.join(CUR_DIR, '../../data/fonts/')

def load_image(name, colorkey=None):
    fullname = IMG_DIR + name
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = SOUND_DIR + name
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound

def load_font(name, size):
    try:
        font = pygame.font.Font(FONT_DIR + name, size)
    except pygame.error, message:
        print 'Cannot load font: ', name
        raise SystemExit, message
    return font