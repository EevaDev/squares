'''
Created on 2013-09-20

@author: Davide
'''
import pygame, sys
import start_menu, match
import constants as const

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

 
size = (width, height) = (320, 240)
 
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("First Python Game")
    
    clock = pygame.time.Clock()
    cur_screen = start_menu.StartMenu(screen)
    state = const.STATE_MENU
    old_state = state
     
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            else:
                state = cur_screen.handle_event(event)
                
        if old_state != state:
            if state == const.STATE_MENU:
                cur_screen = start_menu.StartMenu(screen)
            elif state == const.STATE_PLAY:
                cur_screen = match.Match(screen)
            elif state == const.STATE_EXIT:
                pygame.quit()
                sys.exit(0)
        old_state = state
        
        cur_screen.update()
        
        cur_screen.draw()
    