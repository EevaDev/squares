'''
Created on 2013-09-21

@author: Davide
'''
import utils
import pygame
import random
from constants import *

class Square(object):
    def __init__(self, row, col, not_color = None):
        color_selected = False
        while not color_selected:
            self.color = square_colors[random.choice(square_colors.keys())]
            if not_color is not None:
                if self.color != not_color:
                    color_selected = True
            else:
                color_selected = True
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
    
    def slide(self):
        self.y += S_DISTANCE
        self.rect = pygame.Rect(self.x,self.y,self.width,self.width)
        self.detect_rect = pygame.Rect(self.x-(S_DETECT_SIZE-S_SIZE)/2, 
                                       self.y-(S_DETECT_SIZE-S_SIZE)/2,
                                       S_DETECT_SIZE, S_DETECT_SIZE)

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
        self.chain_sorted = {}
        self.all_same_color = []
        self.before_square = None # To store the last place before a square was composed
    
    def _organize_chain(self):
        self.chain_sorted = {} # {col:[row,row,row,..]}
        for (row,col) in self.chain:
            if col in self.chain_sorted.keys():
                self.chain_sorted[col].append(row)
            else:
                self.chain_sorted[col] = [row]
        
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
            if len(self.chain) >= 2:
                ## Reorganize chain
                for (a,b) in self.all_same_color:
                    if (a,b) not in self.chain:
                        self.chain.append((a,b))
                self._organize_chain()
                for col in self.chain_sorted:
                    rows = sorted(self.chain_sorted[col])
                    for r in rows:
                        tmp = self.table[r][col]
                        for j in range(r, -1, -1):
                            if j == 0:
                                if self.before_square is not None:
                                    self.table[j][col] = Square(j,col, not_color = self.current_color)
                                else:
                                    self.table[j][col] = Square(j,col)
                            else:
                                self.table[j][col] = self.table[j-1][col]
                                self.table[j][col].slide()
                        del(tmp)
            
            elif len(self.chain) == 1:
                self.table[self.chain[0][0]][self.chain[0][1]].deselect()
            # Reset everything
            self.button_down = False
            self.current_color = (0,0,0)
            self.chain = []
            self.all_same_color = []
            self.before_square = None
    
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
                    if square.isOver(mouse_pos) and square.get_color()==self.current_color:
                        if len(self.chain) >= 2 and square.isSelected() and (new_row, new_col) != self.chain[-2]:
                            # If I go back and forward again there is a problem
                            # Select all squares of the same color
                            self.before_square = self.chain[-1]
                            self.chain.append((new_row,new_col))
                            self.all_same_color = []
                            for rx in range(TAB_H):
                                for cx in range(TAB_W):
                                    sx = self.table[rx][cx]
                                    if sx.get_color() == self.current_color:
                                        sx.select()
                                        self.all_same_color.append((rx, cx))
                        elif not square.isSelected():
                            square.select()
                            self.chain.append((new_row,new_col))
                    if len(self.chain) >= 2:
                        if square.isOver(mouse_pos) and new_row == self.chain[-2][0] and new_col == self.chain[-2][1]:
                            if self.before_square == (new_row, new_col):
                                for (r,c) in self.all_same_color:
                                    if (r,c) not in self.chain:
                                        self.table[r][c].deselect()
                                self.all_same_color = []
                            else:
                                self.table[cur_row][cur_col].deselect()
                                self.chain.pop(-1)
                                
    def draw(self):
        self.screen.fill(WHITE)
        for row in range(TAB_H):
            for square in self.table[row]:
                square.draw(self.screen)
        pygame.display.flip()