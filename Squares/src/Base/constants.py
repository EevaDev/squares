'''
Created on 2013-09-22

@author: Davide
'''

size = (width, height) = (320, 240)
TABLE_SIZE = (tab_w, tab_h) = (200, 200)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREY = (245,245,250)
TITLE_BLUE = (61,35,200)

square_colors = {
    "blue"    : (61,35,255),
    "orange"  : (255,206,35),
    "azzurro" : (35,211,255),
    "green"   : (35,255,82),
    "red"     : (255,35,35),
    "viola"  : (175,35,255)
}

STATE_MENU = 0
STATE_MOVES = 1
STATE_TIME = 2
STATE_EXIT = 3
STATE_RESULT = 4

# Gameplay modes
MODE_MOVE = 0
MODE_TIME = 1

MAX_TIME = 60
MAX_MOVES = 30

# Table and squares parameters
TAB_W = 6
TAB_H = 6

S_SIZE = 18
S_DETECT_SIZE = 24
S_DISTANCE = 30
OFF_X = 30
OFF_Y = 35
SLIDE_SPEED = 7

INFO_X = 260
SCORE_Y = 50
SCORE_VAL_Y = 70
COUNT_Y = 100
COUNT_VAL_Y = 120
