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
        self.text = font.render(text, 1, (10, 10, 255))
        self.yCenter = 10
        self.xCenter = 10
    
    def setPos(self, posX, posY):
        self.yCenter = posY
        self.xCenter = posX
        
    def isClicked(self, pos):
        self.position = self.text.get_rect(centery=self.yCenter, centerx=self.xCenter)
        if self.position.collidepoint(pos):
            return True
        else:
            return False
        
    def draw(self, screen):
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
        startItem = MenuItem("Start", font) 
        exitItem = MenuItem("Exit", font)
        self.items = (startItem, exitItem)
        for i in range(len(self.items)):
            self.items[i].setPos(screen.get_width()/2, 30*(i+1))
        
        
    def handle_event(self, ev):
        state = STATE_MENU
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.items[0].isClicked(pygame.mouse.get_pos()):
                state = STATE_PLAY
            elif self.items[1].isClicked(pygame.mouse.get_pos()):
                state = STATE_EXIT
        return state
    
    def update(self):
        pass
            
    def draw(self):
        self.screen.fill(WHITE)
        for item in self.items:
            item.draw(self.screen)
        pygame.display.flip()