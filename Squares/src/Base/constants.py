'''
Created on 2013-09-22

@author: Davide
'''

size = (width, height) = (320, 240)
BLACK = (0, 0, 0)
WHITE = (255,255,255)

square_colors = {
    "magenta" : (158,14,64),
    "blue"    : (37,191,218),
    "green"   : (159,232,85),
    ##"red"     : (232,19,40),
    ##"orange"  : (242,217,51)
}

STATE_MENU = 0
STATE_PLAY = 1
STATE_EXIT = 2

# Gameplay modes
MODE_MOVE = 0
MODE_TIME = 1

MAX_TIME = 60
MAX_MOVES = 3

# Table and squares parameters
TAB_W = 6
TAB_H = 6

S_SIZE = 10
S_DETECT_SIZE = 22
S_DISTANCE = 30
