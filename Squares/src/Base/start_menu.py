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
        self.text = font.render(text, 1, (50, 50, 200))
        self.yCenter = 10
        self.xCenter = 10
        self.isOver = False
    
    def setPos(self, posX, posY):
        '''Set item position on the screen'''
        self.yCenter = posY
        self.xCenter = posX
        
    def setOver(self, value):
        self.isOver = value
        
    def isClicked(self, pos):
        '''Determine if the item has been clicked'''
        self.position = self.text.get_rect(centery=self.yCenter, centerx=self.xCenter)
        if self.position.collidepoint(pos):
            return True
        else:
            return False
        
    def draw(self, screen):
        '''Draw item'''
        if self.isOver:
            pygame.draw.rect(screen, (200,200,200), self.position)
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
        font_title = utils.load_font("ka1.ttf", 25)
        font = utils.load_font("technoid.ttf", 20)
        font.set_bold(True)
        title = MenuItem("SQUARES", font_title)
        startMovesItem = MenuItem("Moves Mode", font)
        startTimeItem = MenuItem("Time Mode", font)  
        exitItem = MenuItem("Exit", font)
        self.items = (title, startMovesItem, startTimeItem, exitItem)
        for i in range(len(self.items)):
            if i == 0:
                self.items[i].setPos(screen.get_width()/2, 50)
            else:
                self.items[i].setPos(screen.get_width()/2, 20*(i+4))
                
        self.over_option = None
        
        
    def handle_event(self, ev):
        '''
        Handle mouse clicks to determine if one of the menu items has been selected
        '''
        state = STATE_MENU
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.items[1].isClicked(pygame.mouse.get_pos()):
                state = STATE_MOVES
            elif self.items[2].isClicked(pygame.mouse.get_pos()):
                state = STATE_TIME
            elif self.items[3].isClicked(pygame.mouse.get_pos()):
                state = STATE_EXIT
        return state
    
    def update(self, state):
        currently_over = None
        for i in range(1,4):
            if self.items[i].isClicked(pygame.mouse.get_pos()):
                currently_over = i
                break
        if self.over_option != currently_over:
            if self.over_option is not None:
                self.items[self.over_option].setOver(False)
            if currently_over is not None:
                self.items[currently_over].setOver(True)
            self.over_option = currently_over
        return state
            
    def draw(self):
        '''
        Draw menu to screen
        '''
        self.screen.fill(WHITE)
        for item in self.items:
            item.draw(self.screen)
        pygame.display.flip()
    

class EndMenu(object):
    '''
    Main Menu of the game
    '''
    def __init__(self, screen, score):
        '''
        Constructor
        Initialisation of all items and determine position 
        '''
        self.screen = screen
        font = utils.load_font("ka1.ttf", 20)
        scoreItem = MenuItem(str(score), font)
        backItem = MenuItem("Back", font)
        self.items = (scoreItem, backItem)
        for i in range(len(self.items)):
            self.items[i].setPos(screen.get_width()/2, 30*(i+1))
        
        
    def handle_event(self, ev):
        '''
        Handle mouse clicks to determine if one of the menu items has been selected
        '''
        state = STATE_RESULT
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.items[1].isClicked(pygame.mouse.get_pos()):
                state = STATE_MENU
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
        