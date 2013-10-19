'''
Created on 2013-09-20

@author: Davide
'''
import pygame, sys
import start_menu, match
from constants import *

# Check if pygame' modules are initialized
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Size of the screen
size = (width, height) = (320, 240)
 
# If main.py is the main file called, run the game
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Squares")
    
    clock = pygame.time.Clock()
    cur_screen = start_menu.StartMenu(screen)
    state = STATE_MENU
    old_state = state
     
    while True:
        clock.tick(30)
        ## HANDLE EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            else:
                state = cur_screen.handle_event(event)
        
        ## UPDATE GAME
        state = cur_screen.update(state)
        
        # Change state/screen if necessary
        if old_state != state:
            if state == STATE_MENU:
                cur_screen = start_menu.StartMenu(screen)
            elif state == STATE_MOVES:
                cur_screen = match.Match(screen, MODE_MOVE)
            elif state == STATE_TIME:
                cur_screen = match.Match(screen, MODE_TIME)
            elif state == STATE_RESULT:
                score = cur_screen.get_score()
                cur_screen = start_menu.EndMenu(screen, score)
            elif state == STATE_EXIT:
                pygame.quit()
                sys.exit(0)
        old_state = state
        
        ## DRAW SCREEN
        cur_screen.draw()
    