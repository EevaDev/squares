'''
Created on 2013-09-21

@author: Davide
'''
import pygame
import utils
from constants import *

class MenuItem(object):
    '''
    Any Item of the Menu. This class provides methods for positioning and display
    '''
    def __init__(self, text, font):
        '''
        Constructor
        '''
        self.text = font.render(text, 1, (10, 10, 255))
        self.yCenter = 10
        self.xCenter = 10
    
    def setPos(self, posX, posY):
        '''Set item position on the screen'''
        self.yCenter = posY
        self.xCenter = posX
        
    def isClicked(self, pos):
        '''Determine if the item has been clicked'''
        self.position = self.text.get_rect(centery=self.yCenter, centerx=self.xCenter)
        if self.position.collidepoint(pos):
            return True
        else:
            return False
        
    def draw(self, screen):
        '''Draw item'''
        self.position = self.text.get_rect(centery=self.yCenter, centerx=self.xCenter)
        screen.blit(self.text, self.position)

class StartMenu(object):
    '''
    Main Menu of the game
    '''
    def __init__(self, screen):
        '''
        Constructor
        Initialisation of all items and determine position 
        '''
        self.screen = screen
        font = utils.load_font("ka1.ttf", 20)
        startMovesItem = MenuItem("Moves Mode", font)
        startTimeItem = MenuItem("Time Mode", font)  
        exitItem = MenuItem("Exit", font)
        self.items = (startMovesItem, startTimeItem, exitItem)
        for i in range(len(self.items)):
            self.items[i].setPos(screen.get_width()/2, 30*(i+1))
        
        
    def handle_event(self, ev):
        '''
        Handle mouse clicks to determine if one of the menu items has been selected
        '''
        state = STATE_MENU
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.items[0].isClicked(pygame.mouse.get_pos()):
                state = STATE_MOVES
            elif self.items[1].isClicked(pygame.mouse.get_pos()):
                state = STATE_TIME
            elif self.items[2].isClicked(pygame.mouse.get_pos()):
                state = STATE_EXIT
        return state
    
    def update(self, state):
        return state
            
    def draw(self):
        '''
        Draw menu to screen
        '''
        self.screen.fill(WHITE)
        for item in self.items:
            item.draw(self.screen)
        pygame.display.flip()