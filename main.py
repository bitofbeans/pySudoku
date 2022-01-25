# import pygame for gui
import pygame as pg
# import sudoku solver/checker (by me)
import solver as s
# import pprint for cleaner printing
import pprint as pp

# ---------------------------------- #

# add board
board = [
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
# program will use 'board' variable
solvedBoard = [
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
font = pg.font.SysFont('freesansbold', 40)

# functions ------------------------ #

# draw text
def drawText(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
# ---------------------------------- #

def renderBoard():
    # RENDER SQUARES AND LINES
    global squares
    global squareCoords
    squares = []
    squareCoords = []
    for y in range(9):
      for x in range(9):
        posx = x*SIZE + x*2
        posy = y*SIZE + y*2
        square = pg.rect.Rect(posx, posy, SIZE, SIZE)
        squares.append(square)
        squareCoords.append((x,y))
        # draw squares
        pg.draw.rect(screen,(200,200,200),square,border_radius=4)
        if x == 3 or x == 6:
          # vertical lines
          pg.draw.line(screen,(0,0,0),(posx-1,0),(posx-1,468),4)
        if not board[y][x] == 0:
          drawText(str(board[y][x]), font, (50,50,50),posx+5,posy+5)
      if y == 3 or y == 6:
        # horizontal lines
        pg.draw.line(screen,(0,0,0),(0,posy-1),(SCREEN_WIDTH,posy-1),4)
    # draw bottom part
    bottom = pg.rect.Rect(0,460,SCREEN_WIDTH,SIZE)
    pg.draw.rect(screen,(255,255,255),bottom)
    pg.draw.line(screen,(100,100,100),(0,460),(SCREEN_WIDTH,460),4)
    return squares, squareCoords
    
# ---------------------------------- #

def boardLogic(board, solvedBoard):
  global selected
  square = squares[selected]
  pg.draw.rect(screen,(255,0,0),square,width = 3, border_radius=4) 
  
  # get selected from click
  mouse = pg.mouse.get_pos()
  i = 0
  for square in squares:
    if square.collidepoint(mouse):
      if pg.mouse.get_pressed()[0] == True:
        selected = i
    i += 1

  # change from player in
  keys = pg.key.get_pressed()
  coord = squareCoords[selected]
  x,y = coord
  def tryKey(key):
    if solvedBoard[y][x] == key:
      board[y][x] = key   
    else:
      square = squares[selected]
      pg.draw.rect(screen,(255,0,0),square, border_radius=4) 
  # inputs
  if keys[pg.K_1]:
    tryKey(1)
  if keys[pg.K_2]:
    tryKey(2)
  if keys[pg.K_3]:
    tryKey(3)
  if keys[pg.K_4]:
    tryKey(4)
  if keys[pg.K_5]:
    tryKey(5)
  if keys[pg.K_6]:
    tryKey(6)
  if keys[pg.K_7]:
    tryKey(7)
  if keys[pg.K_8]:
    tryKey(8)
  if keys[pg.K_9]:
    tryKey(9)
  
  # return board changes
  return board, solvedBoard

# ---------------------------------- #

# global which selected square
global selected
selected = 0

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
    screen.fill((255,255,255))
    renderBoard()
    # board logic
    board, solvedBoard = boardLogic(board, solvedBoard)

    # update screen
    pg.display.update()


pg.quit()