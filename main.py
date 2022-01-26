# import pygame for gui
import pygame as pg
# import sudoku solver/checker (by me)
import solver as s
# import pprint for cleaner printing
import pprint as pp
# to copy lists without linking them AND keeping nested lists
import copy

# ---------------------------------- #
unsolved = [
    [4,2,0,  9,8,0,  5,1,0],
    [5,0,7,  4,0,3,  0,8,9],
    [8,0,0,  0,0,6,  4,0,7],
    
    [0,3,5,  8,7,0,  6,0,0],
    [6,0,4,  0,0,0,  0,7,0],
    [7,0,0,  1,0,4,  0,0,0],
   
    [3,0,0,  5,9,0,  1,0,0],
    [0,0,0,  0,4,1,  3,2,0],
    [2,4,1,  0,3,0,  7,9,0]
]
# add board
board = copy.deepcopy(unsolved)
# program will use 'board' variable
solvedBoard = copy.deepcopy(unsolved)
# create solver sprite
solver = s.Solver([])
# solve alt board
solvedBoard = solver.solve(solvedBoard)

# ---------------------------------- #

# begin pygame
pg.init()

# open window
SIZE = 50
SCREEN_WIDTH = 450 + 9*2
SCREEN_HEIGHT = 450 + SIZE + 9*2
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption('Sudoku')

# set tps
clock = pg.time.Clock()
fps = 60

# set font
font = pg.font.SysFont("segoeuisemilight", 35)
fontSmall = pg.font.SysFont("segoeuisemilight", 25)
fontSmallThick = pg.font.SysFont("segoeuisemibold", 25)

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LGREY = (200,200,200)
DGREY = (100,100,100)
FONT =  (60,80,105)

# functions ------------------------ #

# draw text
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
# ---------------------------------- #

def renderBoard():
    # RENDER SQUARES AND LINES
    
    # use global lists
    global squares
    global squareCoords
    squares = []
    squareCoords = []
    
    # render grid
    for y in range(9):
      for x in range(9):
        # get position
        posx = x*SIZE + x*2
        posy = y*SIZE + y*2
        
        # make list of all squares in order
        square = pg.rect.Rect(posx, posy, SIZE, SIZE)
        squares.append(square)
        squareCoords.append((x,y))
        
        # draw squares
        pg.draw.rect(screen,WHITE,square,border_radius=2)
        
        if x == 3 or x == 6:
          # vertical lines 
          pg.draw.line(screen,DGREY,(posx-1,0),(posx-1,468),3)
        
        if not board[y][x] == 0:
          # draw text if not a 0
          drawText(str(board[y][x]), font, FONT, posx+25, posy+25)
      
      if y == 3 or y == 6:
        # horizontal lines
        pg.draw.line(screen,DGREY,(0,posy-1),(SCREEN_WIDTH,posy-1),3)
        
    # draw bottom part
    bottom = pg.rect.Rect(0,468,SCREEN_WIDTH,SIZE)
    pg.draw.rect(screen,WHITE,bottom)
    pg.draw.line(screen,DGREY,(0,468),(SCREEN_WIDTH,468),3)
    drawText(f"Remaining Spots: {s.countNum(board,0)}",fontSmall, FONT, SCREEN_WIDTH/2, 493, align='lc')
    drawText("X "*strikes, fontSmallThick, (194,0,42), 50, 494, align='c')
    if win != 0:
      fill = pg.Surface((1000,750))  
      fill.set_alpha(200)                
      fill.fill(WHITE)           
      screen.blit(fill, (0,0))
      if win == 1:
        drawText("You Won!", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
        drawText("Press Space to continue...", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50)
      elif win == -1:
        drawText("You Lost!", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-50)
        drawText("Press Space to restart...", font, FONT, SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50)
      
    
# ---------------------------------- #

def boardLogic(board, solvedBoard):
  # use global selected variable
  global selected
  global win
  global pressed
  global strikes
  
  # get square rect of selected
  square = squares[selected]
  
  # render cursor
   # get coord of selected square
  coord = squareCoords[selected]
  x,y = coord
  
  if win == 0:
    if board[y][x] == 0:
      # yellow thing
      pg.draw.rect(screen,(200,160,5),square,width = 5, border_radius=10)
      pg.draw.rect(screen,(249,215,28),square,width = 3, border_radius=10) 
    else:
      # green thing
      pg.draw.rect(screen,(0,150,0),square,width = 5, border_radius=10)
      pg.draw.rect(screen,(0,200,0),square,width = 3, border_radius=10) 
    
  # get selected from click
  mouse = pg.mouse.get_pos()
  i = 0
  for square in squares:
    if square.collidepoint(mouse):
      selected = i
      if pg.mouse.get_pressed()[0] == True:
        pass
    i += 1

  # keys pressed
  keys = pg.key.get_pressed()
  
  # get coords from selected
  coord = squareCoords[selected]
  x,y = coord
  
  # see if key works
  def tryKey(key):
    if board[y][x] != 0:
      return
    if solvedBoard[y][x] == key:
      board[y][x] = key   
    else:
      square = squares[selected]
      pg.draw.rect(screen,(100,0,0),square,width = 0, border_radius=10)
      pg.draw.rect(screen,(200,0,0),square,width = 5, border_radius=10) 
      global pressed
      global strikes
      if pressed != key:
        pressed = key
        strikes += 1
  
  # inputs
  if keys[pg.K_1]:
    tryKey(1)
  elif keys[pg.K_2]:
    tryKey(2)
  elif keys[pg.K_3]:
    tryKey(3)
  elif keys[pg.K_4]:
    tryKey(4)
  elif keys[pg.K_5]:
    tryKey(5)
  elif keys[pg.K_6]:
    tryKey(6)
  elif keys[pg.K_7]:
    tryKey(7)
  elif keys[pg.K_8]:
    tryKey(8)
  elif keys[pg.K_9]:
    tryKey(9)
  elif keys[pg.K_p]:
    # auto solve
    board = copy.deepcopy(solvedBoard)
  else:
    pressed = 0
  
  if win == 1:
    if keys[pg.K_SPACE]:
      # restart on space
      win = 0
      board = copy.deepcopy(unsolved)
      strikes = 0
  if win == -1:
    if keys[pg.K_SPACE]:
      # restart on space
      win = 0
      board = copy.deepcopy(unsolved)
      strikes = 0
  
  if board == solvedBoard:
    # if won
    win = 1 
  if strikes >= 3:
    # if lost
    win = -1
  
  # return board changes
  return board, solvedBoard

# ---------------------------------- #

# globals for my sanity
## i know globals can be bad practice, 
## but feeding all of these values to 
## each function is just stupid,
## and classes would be be clunky
## forgive me :)
global selected
selected = 0
global win
win = 0 
global strikes
strikes = 0
global pressed
pressed = 0

# ---------------------------------- #

# game loop

run = True

while run:
    # tick clock
    clock.tick(fps)
    # escape condition
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # LOGIC
    
    #render
    screen.fill(LGREY)
    
    renderBoard()
    
    board, solvedBoard = boardLogic(board, solvedBoard)
    
    # update screen
    pg.display.update()


pg.quit()