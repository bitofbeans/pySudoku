import pprint as pp
from collections import Counter
from time import sleep

unsolvedBoard = [
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
board = unsolvedBoard


def solve():
    idxList = []
    for y in range(len(board)):
        for x in range(len(board)):
            row = board[y]
            if row[x] == 0:
                idxList.append([x,y])
    solved = False
    idx = 0
    while not solved:

        # get coords
        x,y = idxList[idx]
        
        # increment number
        if board[y][x]+1 > 9:
            board[y][x] = 0
            idx -=1
            continue
        
        board[y][x] +=1
        number = board[y][x]
        # check constraints
        rowcheck = checkRow(board[y][x], y)
        colcheck = checkColumn(board[y][x], x)
        box = int(x/3) + int(y/3)
        boxcheck = checkBox(board[y][x], box)
        if rowcheck and colcheck and boxcheck:
            idx+= 1
            if idx > len(idxList)-1:
                solved = True

        sleep(0)
        if x == 8 and y == 3:
            
            pass
                
    pp.pprint(board)
            
        
            

def checkRow(num, row_idx):
    # get row list
    row = board[row_idx]
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

def checkColumn(num, col_idx):
    # get column list
    col = []
    for i in range(9):
        row = board[i]
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

def checkBox(num, box_idx):
    # get box coords
    box_x = (box_idx % 3)*3
    box_y = int(box_idx/3)*3
    # get box list
    box = []
    for y in range(3):
        for x in range(3):
            row = board[box_y + y]
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


pp.pprint(unsolvedBoard)
print()
solve()