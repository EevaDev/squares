'''
Created on 2013-09-21

@author: Davide
'''
import utils
import pygame
import random
from constants import *

class Square(object):
    def __init__(self, row, col):
        self.color = square_colors[random.choice(square_colors.keys())]
        self.x = (col+1)*S_DISTANCE
        self.y = (row+1)*S_DISTANCE
        self.width = S_SIZE
        self.rect = pygame.Rect(self.x,self.y,self.width,self.width)
        self.detect_rect = pygame.Rect(self.x-(S_DETECT_SIZE-S_SIZE)/2, 
                                       self.y-(S_DETECT_SIZE-S_SIZE)/2,
                                       S_DETECT_SIZE, S_DETECT_SIZE)
        self.selected = False
    
    def get_color(self):
        return self.color

    def isSelected(self):
        return self.selected
    
    def select(self):
        self.selected = True
    
    def deselect(self):
        self.selected = False
            
    def isOver(self, pos):
        return self.detect_rect.collidepoint(pos)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.selected:
            pygame.draw.rect(screen, self.color, self.detect_rect)
        else:
            pygame.draw.rect(screen, self.color, self.detect_rect, 1)

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
        self.table = []
        for r in range(TAB_H):
            self.table.append([])
            for c in range(TAB_W):
                self.table[r].append(Square(r,c))
        self.screen = screen
        self.button_down = False
        self.current_color = (0,0,0)
        self.chain = []
        
    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            self.button_down = True
            for row in range(TAB_H):
                for col in range(TAB_W):
                    square = self.table[row][col]
                    if square.isOver(pygame.mouse.get_pos()):
                        # Start a new chain
                        self.current_color = square.get_color() 
                        square.select()
                        self.chain.append((row,col))
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self.button_down = False
            self.current_color = (0,0,0)
            if len(self.chain):
                print self.chain
            if len(self.chain) >= 2:
                for (row, col) in self.chain:
                    del(self.table[row][col])
            ## TODO: Shift everything over the deleted ones in their places
            
            elif len(self.chain) == 1:
                self.table[self.chain[0][0]][self.chain[0][1]].deselect()
            self.chain = []
    
    def update(self):
        if self.button_down and len(self.chain) > 0:
            # The next square must be or in the same row or in the same col, 
            # next to the last square of the chain
            mouse_pos = pygame.mouse.get_pos()
            cur_row = self.chain[-1][0]
            cur_col = self.chain[-1][1]
            for (new_row,new_col) in [(cur_row-1,cur_col),(cur_row+1,cur_col),(cur_row,cur_col-1),(cur_row,cur_col+1)]:
                if new_row >= 0 and new_row < TAB_H and new_col >= 0 and new_col < TAB_W:
                    square = self.table[new_row][new_col]
                    if square.isOver(mouse_pos) and not square.isSelected() and square.get_color()==self.current_color:
                        square.select()
                        self.chain.append((new_row,new_col))
                    if len(self.chain) >= 2:
                        if square.isOver(mouse_pos) and new_row == self.chain[-2][0] and new_col == self.chain[-2][1]:
                            self.table[cur_row][cur_col].deselect()
                            self.chain.pop(-1)
            
    def draw(self):
        self.screen.fill(WHITE)
        for row in range(TAB_H):
            for square in self.table[row]:
                square.draw(self.screen)
        pygame.display.flip()