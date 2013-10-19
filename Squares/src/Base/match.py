'''
Created on 2013-09-21

@author: Davide
'''
import pygame
import random
from constants import *
import utils
import time

class TextItem(object):
    '''
    Any Text Item. This class provides methods for positioning and display
    '''
    def __init__(self, text, font, posX, posY):
        '''
        Constructor
        '''
        self.font = font
        self.text = font.render(text, 1, TITLE_BLUE)
        self.xCenter = posX
        self.yCenter = posY
    
    def setPos(self, posX, posY):
        '''Set item position on the screen'''
        self.yCenter = posY
        self.xCenter = posX
        
    def setText(self, text):
        '''Change the text to be rendered'''
        self.text = self.font.render(text, 1, square_colors['blue'])
        
    def draw(self, screen):
        '''Draw item'''
        self.position = self.text.get_rect(centery=self.yCenter, centerx=self.xCenter)
        screen.blit(self.text, self.position)

class Square(object):
    '''
    Square item. All elements of the table used to play a game are instances of this class.
    It can be selected, deselected, moved, and it has a color
    '''
    
    
    def __init__(self, row, col, not_color = None):
        '''
        Constructor
        '''
        # Select a color among those of the square_colors dictionary, different from not_color
        color_selected = False
        while not color_selected:
            self.color = square_colors[random.choice(square_colors.keys())]
            if not_color is not None:
                if self.color != not_color:
                    color_selected = True
            else:
                color_selected = True
        # Set position and create the Rects which identify the square 
        self.x = OFF_X + (col)*S_DISTANCE
        self.y = OFF_Y + (row)*S_DISTANCE
        self.width = S_SIZE
        self.rect = pygame.Rect(self.x,self.y,self.width,self.width)
        self.detect_rect = pygame.Rect(self.x-(S_DETECT_SIZE-S_SIZE)/2, 
                                       self.y-(S_DETECT_SIZE-S_SIZE)/2,
                                       S_DETECT_SIZE, S_DETECT_SIZE)
        self.selected = False # Is the square selected?
        self.destination = self.y # For the sliding
        self.sliding = False
    
    def get_color(self):
        '''Just return the color of the square'''
        return self.color
    
    def slide(self):
        '''Move the square down one position'''
        if self.sliding:
            self.destination += S_DISTANCE
        else:
            self.destination = self.y + S_DISTANCE
            self.y += SLIDE_SPEED
            self.sliding = True
        self.rect = pygame.Rect(self.x,self.y,self.width,self.width)
        self.detect_rect = pygame.Rect(self.x-(S_DETECT_SIZE-S_SIZE)/2, 
                                       self.y-(S_DETECT_SIZE-S_SIZE)/2,
                                       S_DETECT_SIZE, S_DETECT_SIZE)
        
    def update(self):
        # If destination is not reached, move it
        if self.sliding:
            if self.y < self.destination:
                self.y += SLIDE_SPEED
                if self.y > self.destination:
                    self.y = self.destination
                    self.sliding = False
                self.rect = pygame.Rect(self.x,self.y,self.width,self.width)
                self.detect_rect = pygame.Rect(self.x-(S_DETECT_SIZE-S_SIZE)/2, 
                                               self.y-(S_DETECT_SIZE-S_SIZE)/2,
                                               S_DETECT_SIZE, S_DETECT_SIZE)
            else:
                self.sliding = False
                self.y = self.destination

    def isSelected(self):
        '''Return True if the square has been previously selected'''
        return self.selected
    
    def select(self):
        '''Select square'''
        self.selected = True
    
    def deselect(self):
        '''De-Select square'''
        self.selected = False
            
    def isOver(self, pos):
        '''Return True if the mouse in pos is over the square'''
        return self.detect_rect.collidepoint(pos)
    
    def draw(self, screen):
        '''Draw square'''
        pygame.draw.rect(screen, self.color, self.rect)
        if self.selected:
            pygame.draw.rect(screen, self.color, self.detect_rect)
#         else:
#             pygame.draw.rect(screen, self.color, self.detect_rect, 1)

class Match(object):
    '''
    Main class for the game, it handles event, update the state and draw everythin
    '''


    def __init__(self, screen, mode):
        '''
        Constructor
        
        Create table to play match a and all necessary variables
        '''
        # Texts
        font = utils.load_font("monof55.ttf", 18)
        font_big = utils.load_font("monof55.ttf", 22)
        score = TextItem("Score", font_big, INFO_X, SCORE_Y)
        score_val = TextItem("0", font, INFO_X, SCORE_VAL_Y)
        self.texts = [score, score_val]
        if mode == MODE_MOVE:
            self.texts.append(TextItem("Moves", font_big, INFO_X, COUNT_Y))
            self.texts.append(TextItem(str(MAX_MOVES), font, INFO_X, COUNT_VAL_Y))
        elif mode == MODE_TIME:
            self.texts.append(TextItem("Time", font_big, INFO_X, COUNT_Y))
            self.texts.append(TextItem(str(MAX_TIME), font, INFO_X, COUNT_VAL_Y))
            
        
        self.table = [] # Table of squares
        for r in range(TAB_H):
            self.table.append([])
            for c in range(TAB_W):
                self.table[r].append(Square(r,c))
        self.screen = screen
        self.mode = mode
        self.score = 0
        self.moves = 0
        self.start_time = time.time()
        
        # Variables to handle the gameplay
        self.button_down = False # Is the mouse left button clicked?
        self.current_color = (0,0,0) # Color being selected after a mouse click
        self.chain = [] # Chain of selected squares
        self.chain_sorted = {} # Useful dictionary to be used when deleting squares
        self.all_same_color = [] # All squares not in chain to be deleted because of a BigSquare
        self.before_square = None # To store the last place before a square was composed
        self.count_after_square = 0
    
    def _organize_chain(self):
        '''
        Create the chain_sorted dictionary to be used to update table
        Its structure is {col:[row1,row2,row3,..]} which identifies all squares (by their row)
        to be deleted for each column 
        '''
        self.chain_sorted = {} 
        for (row,col) in self.chain:
            if col in self.chain_sorted.keys():
                if not row in self.chain_sorted[col]:
                    self.chain_sorted[col].append(row)
            else:
                self.chain_sorted[col] = [row]
                
    def _check_combinations(self):
        '''
        Check if there is at least one possible combination
        Return False when there is none
        '''
        potential_move = False
        to_check = []
        for r in range(0,TAB_H):
            for c in range(0,TAB_W):
                square = self.table[r][c]
                if c != 0:
                    to_check.append(self.table[r][c-1])
                if c != TAB_W-1:
                    to_check.append(self.table[r][c+1])
                if r != 0:
                    to_check.append(self.table[r-1][c])
                if r != TAB_H-1:
                    to_check.append(self.table[r+1][c])
                for s in to_check:
                    if square.get_color() == s.get_color():
                        potential_move = True
                if potential_move:
                    return True
                else: 
                    to_check = []
        return False
    
    def _delete_line(self, line):
        for c in range(TAB_W):
            # Delete square in line, and slide all those above down
            tmp = self.table[line][c]
            for j in range(line, 0, -1):
                self.table[j][c] = self.table[j-1][c]
                self.table[j][c].slide()    
            del(tmp)
            # Create new square in line 0
            self.table[0][c] = Square(0,c)
        
    def handle_event(self, ev):
        '''
        Check when mouse buttons are clicked and released
        '''
        # Left Mouse button clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            self.button_down = True
            # Determine which square has been clicked and its color, select it, and start chain
            for row in range(TAB_H):
                for col in range(TAB_W):
                    square = self.table[row][col]
                    if square.isOver(pygame.mouse.get_pos()):
                        self.current_color = square.get_color() 
                        square.select()
                        self.chain.append((row,col))
        # Left Mouse button released
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            # If there is a chain to be removed from table
            if len(self.chain) >= 2:
                # If there is a big square, all_same_color isn't empty, append it to chain
                for (a,b) in self.all_same_color:
                    if (a,b) not in self.chain: # This shouldn't be necessary when elements in chain are removed from all_same_color
                        self.chain.append((a,b))
                # Sort chain in the right order to be processed later
                self._organize_chain()
                # Process it: for each square to be removed, slide all squares above it down
                for col in self.chain_sorted:
                    rows = sorted(self.chain_sorted[col])
                    for r in rows:
                        tmp = self.table[r][col]
                        for j in range(r, -1, -1):
                            if j == 0:
                                # Add new squares in row 0 when necessary
                                if self.before_square is not None:
                                    # When a big square is composed, new squares cannot have its color
                                    self.table[j][col] = Square(j,col, not_color = self.current_color)
                                else:
                                    self.table[j][col] = Square(j,col)
                            else:
                                # Slide down and then delete the removed square
                                self.table[j][col] = self.table[j-1][col]
                                self.table[j][col].slide()
                        del(tmp)
                        # Increment score
                        self.score += 1
                # Increment used moves
                self.moves += 1
            # No interesting chain, then deselect the inly square and do nothing else
            elif len(self.chain) == 1:
                self.table[self.chain[0][0]][self.chain[0][1]].deselect()
            # Reset everything
            self.button_down = False
            self.current_color = (0,0,0)
            self.chain = []
            self.all_same_color = []
            self.before_square = None
            self.count_after_square = 0
            
            # Check if there are possible moves
            while not self._check_combinations():
                self._delete_line(TAB_H-2)
            
            self.texts[1].setText(str(self.score))
            if self.mode == MODE_MOVE:
                self.texts[3].setText(str(MAX_MOVES-self.moves))
    
    def update(self, state):
        '''
        While the button is down keep selecting squares of the same color and identify big squares
        '''
        # If chain is started move only horizontally or vertically by one place
        if self.button_down and len(self.chain) > 0:
            mouse_pos = pygame.mouse.get_pos()
            cur_row = self.chain[-1][0]
            cur_col = self.chain[-1][1]
            for (new_row,new_col) in [(cur_row-1,cur_col),(cur_row+1,cur_col),(cur_row,cur_col-1),(cur_row,cur_col+1)]:
                if new_row >= 0 and new_row < TAB_H and new_col >= 0 and new_col < TAB_W: # Remain inside the table
                    square = self.table[new_row][new_col]
                    # If mouse is over a square of the color that is currently selected 
                    if square.isOver(mouse_pos) and square.get_color()==self.current_color:
                        # If mouse is over a square which is already selected (and it has not moved back) it means we have a big square
                        if len(self.chain) > 3 and square.isSelected() and (new_row, new_col) != self.chain[-2] and self.count_after_square == 0:
                            self.before_square = self.chain[-1]
                            self.chain.append((new_row,new_col))
                            self.all_same_color = []
                            # Select all squares of the same color
                            # TODO: We should select only those which aren't already in the chain
                            for rx in range(TAB_H):
                                for cx in range(TAB_W):
                                    sx = self.table[rx][cx]
                                    if sx.get_color() == self.current_color:
                                        sx.select()
                                        self.all_same_color.append((rx, cx))
                            self.count_after_square = 1
                        # If mouse is over a square of the right color, which is not selected, select it and add it to the chain
                        elif len(self.chain) >= 2:
                            if (new_row, new_col) != self.chain[-2]:
                                square.select()
                                self.chain.append((new_row,new_col))
                            if self.before_square is not None:
                                self.count_after_square += 1
                        elif not square.isSelected():
                            square.select()
                            self.chain.append((new_row,new_col))
                    
                    if len(self.chain) >= 2:
                        # Check if a big square has been un-done
                        if square.isOver(mouse_pos) and new_row == self.chain[-2][0] and new_col == self.chain[-2][1]:
                            if self.before_square == (new_row, new_col):
                                for (r,c) in self.all_same_color:
                                    if (r,c) not in self.chain: # This shouldn't be necessary if squares in all_same color aren't in chain
                                        self.table[r][c].deselect()
                                self.before_square = None
                                self.count_after_square = 0
                                self.all_same_color = []
                                self.chain.pop(-1)
                            elif self.count_after_square > 0:
                                self.chain.pop(-1)
                            # Check if mouse moved back and square must be deselected and removed from chain
                            else:
                                self.table[cur_row][cur_col].deselect()
                                self.chain.pop(-1)
                                
        # Move all sliding squares
        for r in range(0,TAB_H):
            for c in range(0,TAB_W):
                self.table[r][c].update()
        
        
        if self.mode == MODE_TIME:
            self.texts[3].setText(str(int(MAX_TIME + 1 - (time.time()-self.start_time))))
        
        if self.mode == MODE_MOVE and self.moves >= MAX_MOVES: 
            match_over = True 
        elif self.mode == MODE_TIME and time.time()-self.start_time >= MAX_TIME:
            match_over = True
        else:
            match_over = False
            
        if match_over:        
            return STATE_RESULT
        else:
            return state
        
    def get_score(self):
        return self.score
    
    def draw(self):
        '''
        Draw the entire table 
        '''
        self.screen.fill(GREY)
        for row in range(TAB_H):
            for square in self.table[row]:
                square.draw(self.screen)
        for t in self.texts:
            t.draw(self.screen)
        pygame.display.flip()