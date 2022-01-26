# Imports
import pprint as pp # for output
from collections import Counter # for more efficient counting
from time import sleep # for adding delay

# SOLVER CLASS for modularity
class Solver():
  def __init__(self, board_in):
      self.map = board_in
  
  # solve function
  def solve(self, board_in):
      self.map = board_in
      # get list of all 0's in list
      idxList = []
      for y in range(len(self.map)):
          for x in range(len(self.map)):
              row = self.map[y]
              if row[x] == 0:
                  idxList.append([x,y])
      # start loop
      solved = False
      idx = 0
      while not solved:

          # get coords
          x,y = idxList[idx]
          
          # if number is too high
          if self.map[y][x]+1 > 9:
              # reset number, go backwards
              self.map[y][x] = 0
              idx -=1
              continue
          # increment number
          self.map[y][x] +=1
          number = self.map[y][x]
          # check constraints
          rowcheck = checkRow(self.map, self.map[y][x], y)
          colcheck = checkColumn(self.map, self.map[y][x], x)
          box = int(x/3) + int(y/3) # get box position
          boxcheck = checkBox(self.map, self.map[y][x], box)
          if rowcheck and colcheck and boxcheck:
              # if valid, move forward
              idx+= 1
              if idx > len(idxList)-1:
                  solved = True
          
          sleep(0)
      return self.map
                  

  def checkBoard(self):
        # get list of numbers in list
      idxList = []
      for y in range(len(self.map)):
          for x in range(len(self.map)):
              idxList.append([x,y])  
      idx = 0
      for i in range(81):
        x,y = idxList[idx]
        # check
        rowcheck = checkRow(self.map, self.map[y][x], y)
        colcheck = checkColumn(self.map, self.map[y][x], x)
        box = int(x/3) + int(y/3) # get box position
        boxcheck = checkBox(self.map, self.map[y][x], box)
        if rowcheck and colcheck and boxcheck:
            # if valid, move forward
            idx+= 1
        else: 
          return False
      return True

def checkRow(board_in, num, row_idx):
    # get row list
    row = board_in[row_idx]
    # get dictionary of counts of numbers
    count = Counter(row)
    # get count of num in row
    count = count[num]
    # if not valid,
    if count > 1:
        # return not valid
        return False
    else:
        # return valid
        return True

def checkColumn(board_in, num, col_idx):
    # get column list
    col = []
    for i in range(9):
        row = board_in[i]
        col.append(row[col_idx])
    # get dictionary of counts of numbers
    counter = Counter(col)
    # get count of num in row
    count = counter[num]
    # if not valid,
    if count > 1:
        # return not valid
        return False
    else:
        # return valid
        return True

def checkBox(board_in, num, box_idx):
    # get box coords
    box_x = (box_idx % 3)*3
    box_y = int(box_idx/3)*3
    # get box list
    box = []
    for y in range(3):
        for x in range(3):
            row = board_in[box_y + y]
            box.append(row[box_x+x])
    # get dictionary of counts of numbers
    count = Counter(box)
    # get count of num in box
    count = count[num]
    # if not valid,
    if count > 1:
        # return not valid
        return False
    else:
        # return valid
        return True

def countNum(board_in, num):
        # get dictionary of counts of numbers
    board_in = [item for sublist in board_in for item in sublist]
    counter = Counter(board_in)
    # get count of num in box
    count = counter[num]
    return count
