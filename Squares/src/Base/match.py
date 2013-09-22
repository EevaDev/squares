'''
Created on 2013-09-21

@author: Davide
'''
import utils
import pygame

size = (width, height) = (320, 240)
black = 0, 0, 0

class Match(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.speed = [5,5]
        self.ball, self.ballrect = utils.load_image("ball.gif")
        
    def handle_event(self, ev):
        pass
    
    def update(self):
        self.ballrect = self.ballrect.move(self.speed)
        if self.ballrect.left < 0 or self.ballrect.right > width:
            self.speed[0] = -self.speed[0]
        if self.ballrect.top < 0 or self.ballrect.bottom > height:
            self.speed[1] = -self.speed[1]
            
    def draw(self, screen):
        screen.fill(black)
        screen.blit(self.ball, self.ballrect)
        pygame.display.flip()