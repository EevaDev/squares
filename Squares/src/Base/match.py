'''
Created on 2013-09-21

@author: Davide
'''
import utils
import constants as const
import pygame

class Match(object):
    '''
    classdocs
    '''


    def __init__(self, screen):
        '''
        Constructor
        '''
        self.speed = [5,5]
        self.ball, self.ballrect = utils.load_image("ball.gif")
        self.screen = screen
        
    def handle_event(self, ev):
        pass
    
    def update(self):
        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > const.width:
            self.speed[0] = -self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > const.height:
            self.speed[1] = -self.speed[1]
            
    def draw(self):
        self.screen.fill(const.WHITE)
        self.screen.blit(self.ball, self.ballrect)
        pygame.display.flip()