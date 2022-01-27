# IMPORTS--------------------------- #
 # import pygame for gui
import pygame
 # import sudoku solver/checker (by me)
import source.main_solver as s
 # to copy lists without linking them AND keeping nested lists
import copy
 # for storing puzzles
import json
 # for random numbers
import random
 # for paths
import os

# INITIALIZE -------------- -------- #
 # Begin Pygame
pygame.init()

# Open window
SIZE = 50
SCREEN_WIDTH = 450 + 9*2
SCREEN_HEIGHT = 450 + SIZE + 9*2
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Sudoku')

# Set clock
clock = pygame.time.Clock()
fps = 60

# Set fonts
fontPath = os.path.abspath("source/segoe_light.ttf")
font = pygame.font.Font(fontPath, 35)
fontSmall = pygame.font.Font(fontPath, 20)
fontPath = os.path.abspath("source/segoe_bold.ttf")
fontThick = pygame.font.Font(fontPath, 35)
fontSmallThick = pygame.font.Font(fontPath, 25)

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LGREY = (200,200,200)
DGREY = (100,100,100)
FONT =  (60,80,105)
FONT_ALT = (90,160,90)

# Data file for puzzle inputs
DATA_FILE= 'source/generated_puzzles.json'

# FUNCTIONS ------------------------- #
def drawText(text, font, color, x, y, align='c'):
    # render text to a surface
    img = font.render(text, True, color)
    # position text to center
    rect = img.get_rect()
    if align == 'c':
      rect.center = x-2, y-2
    elif align == 'lc': 
      rect.x = x
      rect.centery = y
    # draw
    screen.blit(img, rect)
    
def loadData(input): 
    # Load file
    with open(DATA_FILE, "r") as read_file:
        data = json.load(read_file)
    return data[input]
    
# SUDOKU SPRITE---------------------- #
class Sudoku():
  def __init__(self, board_in, solved =None):
    # get boards for play
     # make board to modify
    self.board = copy.deepcopy(board_in)
     # make unsolved board
    self.unsolvedBoard = copy.deepcopy(board_in)
     # make solved board
    self.solvedBoard = copy.deepcopy(solved)
     # make ghost board
    self.ghostBoard = copy.deepcopy(board_in)

    # lists for square data
    self.squares = []
    self.squareCoords = []
    # variables
     # if won
    self.win = 0
     # selected square
    self.selected = 0
     # key that is pressed
    self.pressed = 0
    self.tabpressed = False
     # number of strikes
    self.strikes = 0
     # ghost board and bool for ghost enabled
    self.ghost_selected = []
    self.ghostmode = False
    
  def renderBoard(self):
    # RENDER SQUARES AND LINES
    # empty lists
    self.squares = []
    self.squareCoords = []
    
    # render grid
    for y in range(9):
      for x in range(9):
        # get position
        posx = x*SIZE + x*2
        posy = y*SIZE + y*2
        
        # make list of all squares in order
        square = pygame.rect.Rect(posx, posy, SIZE, SIZE)
        self.squares.append(square)
        self.squareCoords.append((x,y))
        
        # draw squares
        pygame.draw.rect(screen,WHITE,square,border_radius=2)
        
        if x == 3 or x == 6:
          # vertical lines 
          pygame.draw.line(screen,DGREY,(posx-1,0),(posx-1,468),3)
        
        if not self.board[y][x] == 0:
          # draw text if not a 0
          drawText(str(self.board[y][x]), font, FONT, posx+25, posy+25)
        elif not self.ghostBoard[y][x] == 0:
          # draw ghost text if exists
          drawText(str(self.ghostBoard[y][x]), fontThick, FONT, posx+25, posy+25)
          
      if y == 3 or y == 6:
        # horizontal lines
        pygame.draw.line(screen,DGREY,(0,posy-1),(SCREEN_WIDTH,posy-1),3)
        
    # draw bottom part
    bottom = pygame.rect.Rect(0,468,SCREEN_WIDTH,SIZE)
    pygame.draw.rect(screen,WHITE,bottom)
    pygame.draw.line(screen,DGREY,(0,468),(SCREEN_WIDTH,468),3)
    # bottom text
    drawText(f"Ghost Mode (Tab): {self.ghostmode}",fontSmall, FONT, SCREEN_WIDTH/2, 493, align='lc')
    drawText("X "*self.strikes, fontSmallThick, (194,0,42), 50, 494, align='c')
    
    # draw overlay for win condition
    if self.win != 0:
      fill = pygame.Surface((1000,750))  
      fill.set_alpha(200)                
      fill.fill(WHITE)           
      screen.blit(fill, (0,0))
      if self.win == 1:
        drawText("You Won!", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
        drawText("Press Space to continue...", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50)
      elif self.win == -1:
        drawText("You Lost!", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
        drawText("Press Space to restart...", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50)

  def boardLogic(self):
    # get square rect of selected
    square = self.squares[self.selected]
    # get coord of selected square
    coord = self.squareCoords[self.selected]
    x,y = coord
    
    # render cursor
    if self.win == 0:
      if self.board[y][x] == 0:
        # yellow thing
        pygame.draw.rect(screen,(200,160,5),square,width = 5, border_radius=10)
        pygame.draw.rect(screen,(249,215,28),square,width = 3, border_radius=10) 
      else:
        # green thing
        pygame.draw.rect(screen,(0,150,0),square,width = 5, border_radius=10)
        pygame.draw.rect(screen,(0,200,0),square,width = 3, border_radius=10) 
      
    # get selected from mouse position
    mouse = pygame.mouse.get_pos()
    i = 0
    for square in self.squares:
      if square.collidepoint(mouse):
        self.selected = i
        if pygame.mouse.get_pressed()[0] == True:
          pass
      i += 1

    # keys pressed
    keys = pygame.key.get_pressed()
    
    # get coords from selected
    coord = self.squareCoords[self.selected]
    x,y = coord
    
    # see if key works
    def tryKey(key):
      coord = self.squareCoords[self.selected]
      x,y = coord
      if self.win != 0 or self.board[y][x] != 0:
        # if already won or lost / if item is already taken
        return
      if self.solvedBoard[y][x] == key:
          self.board[y][x] = key
      else:
        square = self.squares[self.selected]
        pygame.draw.rect(screen,(100,0,0),square,width = 0, border_radius=10)
        pygame.draw.rect(screen,(200,0,0),square,width = 5, border_radius=10) 
        self.ghostBoard[y][x] = 0
        
        self.strikes += 1
        if self.strikes > 3:
          self.strikes = 3
    
    # add key to ghost
    def addKey(key_in):
      if self.pressed == key_in: return
      self.pressed = key_in
      self.ghostBoard[y][x] = key_in
      # remove any duplicates
      i = 0
      for elem in self.ghost_selected:
        if elem[1] == self.selected:
          self.ghost_selected.pop(i)
        i +=1
      self.ghost_selected.append((key_in,self.selected))
    # inputs
    
    if keys[pygame.K_TAB] and self.tabpressed == False:
      self.tabpressed = True
      if self.ghostmode is True:
        self.ghostmode = False
        self.ghostBoard = copy.deepcopy(board)
        self.ghost_selected = []
      else: self.ghostmode = True
    elif not keys[pygame.K_TAB]: self.tabpressed = False
    
    if keys[pygame.K_1]:
      addKey(1)
    elif keys[pygame.K_2]:
      addKey(2)
    elif keys[pygame.K_3]:
      addKey(3)
    elif keys[pygame.K_4]:
      addKey(4)
    elif keys[pygame.K_5]:
      addKey(5)
    elif keys[pygame.K_6]:
      addKey(6)
    elif keys[pygame.K_7]:
      addKey(7)
    elif keys[pygame.K_8]:
      addKey(8)
    elif keys[pygame.K_9]:
      addKey(9)
    elif not keys[pygame.K_RETURN]:
      self.pressed = 0
    if keys[pygame.K_0]:
      # Delete item
      self.ghostBoard[y][x] = 0
      i = 0
      for key in self.ghost_selected:
        if key[1] == self.selected:
          self.ghost_selected.pop(i)
        i +=1
    
    elif keys[pygame.K_p]:
      self.board = copy.deepcopy(self.solvedBoard) # instant solve
    
    # If input board has changed
    if self.board != self.ghostBoard:
      if (self.ghostmode and keys[pygame.K_RETURN] and self.pressed != 'return') or (self.ghostmode is not True):
          if keys[pygame.K_RETURN]:
            self.pressed = 'return'
          # update board
          temp = self.selected
          for elem in self.ghost_selected:
            self.selected = elem[1]
            tryKey(elem[0])
          self.selected = temp
          self.ghost_selected = []
      elif not keys[pygame.K_RETURN]:
        self.pressed = 0 
    i
    # if won or lost
    if self.board == self.solvedBoard:
      # if won
      self.win = 1 
    if self.strikes >= 3:
      # if lost
      self.win = -1
    if self.win == 1:
      if keys[pygame.K_SPACE]:
        # restart on space
        self.win = 0
        self.board = copy.deepcopy(self.unsolvedBoard)
        self.strikes = 0
        return True
    if self.win == -1:
      if keys[pygame.K_SPACE]:
        # restart on space
        self.win = 0
        self.board = copy.deepcopy(self.unsolvedBoard)
        self.strikes = 0
        return True
    return False

# ---------------------------------- #
# pick random puzzle
randomInt = random.randint(0,100)
# load random puzzle
board = loadData(f"puzzle{randomInt}")
solution = loadData(f"solution{randomInt}")

# instance of sudoku sprite with inputs
sudoku = Sudoku(board, solved=solution)

# game loop -------------- #
run = True
while run:
    # tick clock --------- #
    clock.tick(fps)
    # escape condition --- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # fill screen -------- #
    screen.fill(LGREY)
    # sudoku logic ------- #
    sudoku.renderBoard()
    if sudoku.boardLogic(): # if reset
      # delete sudoku board
      del sudoku
      # recreate sudoku
      randomInt = random.randint(0,100)
      board = loadData(f"puzzle{randomInt}")
      solution = loadData(f"solution{randomInt}")
      sudoku = Sudoku(board, solved=solution)
    # update screen ------ #
    pygame.display.update()
# end --- #
pygame.quit()
