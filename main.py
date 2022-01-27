# IMPORTS--------------------------- #
 # import pygame for gui
import pygame
 # import sudoku solver/checker (by me)
import main_solver as s
 # to copy lists without linking them AND keeping nested lists
import copy
 # for storing puzzles
import json
 # for random numbers
import random

# INITIALIZE -------------- -------- #
 # begin pygame
pygame.init()

# open window
SIZE = 50
SCREEN_WIDTH = 450 + 9*2
SCREEN_HEIGHT = 450 + SIZE + 9*2
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Sudoku')

# set tps
clock = pygame.time.Clock()
fps = 60

# set font
font = pygame.font.SysFont("segoeuisemilight", 35)
fontSmall = pygame.font.SysFont("segoeuisemilight", 25)
fontSmallThick = pygame.font.SysFont("segoeuisemibold", 25)

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LGREY = (200,200,200)
DGREY = (100,100,100)
FONT =  (60,80,105)

# data file
DATA_FILE= 'generated_puzzles.json'

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
    if input != '':
        return data[input]
    
# SUDOKU SPRITE---------------------- #
class Sudoku():
  def __init__(self, board_in, solved =None):
    # get boards for play
     # board to modify
    self.board = copy.deepcopy(board_in)
     # default unsolved board
    self.unsolvedBoard = copy.deepcopy(board_in)
     # default solved board
    self.solvedBoard = copy.deepcopy(solved)

    # get solver
    solver = s.Solver([])
    # solve alt board
    self.solvedBoard = solver.solve(board_in)
    # lists
    self.squares = []
    self.squareCoords = []
    # variables
     # if won
    self.win = 0
     # selected square
    self.selected = 0
     # key that is pressed
    self.pressed = 0
     # number of strikes
    self.strikes = 0

  def renderBoard(self):
    # RENDER SQUARES AND LINES
    # use global lists
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
      
      if y == 3 or y == 6:
        # horizontal lines
        pygame.draw.line(screen,DGREY,(0,posy-1),(SCREEN_WIDTH,posy-1),3)
        
    # draw bottom part
    bottom = pygame.rect.Rect(0,468,SCREEN_WIDTH,SIZE)
    pygame.draw.rect(screen,WHITE,bottom)
    pygame.draw.line(screen,DGREY,(0,468),(SCREEN_WIDTH,468),3)
    drawText(f"Remaining Spots: {s.countNum(self.board,0)}",fontSmall, FONT, SCREEN_WIDTH/2, 493, align='lc')
    drawText("X "*self.strikes, fontSmallThick, (194,0,42), 50, 494, align='c')
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
    # use global selected variable

    # get square rect of selected
    square = self.squares[self.selected]
    
    # render cursor
    # get coord of selected square
    coord = self.squareCoords[self.selected]
    x,y = coord
    
    if self.win == 0:
      if self.board[y][x] == 0:
        # yellow thing
        pygame.draw.rect(screen,(200,160,5),square,width = 5, border_radius=10)
        pygame.draw.rect(screen,(249,215,28),square,width = 3, border_radius=10) 
      else:
        # green thing
        pygame.draw.rect(screen,(0,150,0),square,width = 5, border_radius=10)
        pygame.draw.rect(screen,(0,200,0),square,width = 3, border_radius=10) 
      
    # get selected from click
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
      if self.win != 0:
        return
      if self.board[y][x] != 0:
        return
      if self.solvedBoard[y][x] == key:
        self.board[y][x] = key   
      else:
        square = self.squares[self.selected]
        pygame.draw.rect(screen,(100,0,0),square,width = 0, border_radius=10)
        pygame.draw.rect(screen,(200,0,0),square,width = 5, border_radius=10) 

        if self.pressed != key:
          self.pressed = key
          self.strikes += 1
    
    # inputs
    if keys[pygame.K_1]:
      tryKey(1)
    elif keys[pygame.K_2]:
      tryKey(2)
    elif keys[pygame.K_3]:
      tryKey(3)
    elif keys[pygame.K_4]:
      tryKey(4)
    elif keys[pygame.K_5]:
      tryKey(5)
    elif keys[pygame.K_6]:
      tryKey(6)
    elif keys[pygame.K_7]:
      tryKey(7)
    elif keys[pygame.K_8]:
      tryKey(8)
    elif keys[pygame.K_9]:
      tryKey(9)
    elif keys[pygame.K_p]:
      # auto solve
      self.board = copy.deepcopy(self.solvedBoard)
    else:
      self.pressed = 0
    
    if self.win == 1:
      if keys[pygame.K_SPACE]:
        # restart on space
        self.win = 0
        self.board = copy.deepcopy(self.unsolvedBoard)
        self.strikes = 0
    if self.win == -1:
      if keys[pygame.K_SPACE]:
        # restart on space
        self.win = 0
        self.board = copy.deepcopy(self.unsolvedBoard)
        self.strikes = 0
    
    if self.board == self.solvedBoard:
      # if won
      self.win = 1 
    if self.strikes >= 3:
      # if lost
      self.win = -1

# ---------------------------------- #
randomInt = random.randint(0,100)

board = loadData(f"puzzle{randomInt}")
solution = loadData(f"solution{randomInt}")

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
    sudoku.boardLogic()
    # update screen ------ #
    pygame.display.update()
# end --- #
pygame.quit()
