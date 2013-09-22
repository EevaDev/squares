'''
Created on 2013-09-21

@author: Davide
'''
import pygame


black = 255,255,255

class MenuItem(object):
    def __init__(self, text, font):
        self.text = font.render(text, 1, (10, 10, 255))
        self.yCenter = 10
        self.xCenter = 10
    
    def setPos(self, posX, posY):
        self.yCenter = posY
        self.xCenter = posX
        
    def isClicked(self, pos):
        if 
        
    def draw(self, screen):
        self.position = self.text.get_rect(centery=self.yCenter, centerx=self.xCenter)
        screen.blit(self.text, self.position)

class StartMenu(object):
    '''
    classdocs
    '''
    def __init__(self, screen):
        '''
        Constructor
        '''
        self.screen = screen
        font = pygame.font.Font(None, 36)
        startItem = MenuItem("Start", font) 
        startItem.setPos(screen.get_width()/2, 30)
        exitItem = MenuItem("Exit", font)
        self.items = [startItem, exitItem]
        for i in range(len(self.items)):
            self.items[i].setPos(screen.get_width()/2, 30*(i+1))
        
        
    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            print "CLICK"
    
    def update(self):
        pass
            
    def draw(self):
        self.screen.fill(black)
        for item in self.items:
            item.draw(self.screen)
        pygame.display.flip()