# Generates sudoku puzzles for main.py
import json,numpy
import main_solver as s
from dokusan import generators
import copy
from typing import Union

DATA_FILE= 'generated_puzzles.json'
# Load data from .json
def loadData(input): 
    # Load file
    with open(DATA_FILE, "r") as read_file:
        data = json.load(read_file)
    if input != '':
        return data[input]
    else: return data
# Save data to .json
def saveData(input, key):
    # open file
    with open(DATA_FILE, "r") as read_file:
        data = json.load(read_file)
    # change world data in file
    data[key] = input
    # output
    json.dump(data, open(DATA_FILE, "w"), cls=CompactJSONEncoder)
# generate boards
def genBoard(diff):
    # generate board value in array
    gen = numpy.array(list(str(generators.random_sudoku(avg_rank=diff))))
    gen = gen.reshape(9,9)
    gen = gen.tolist()

    # convert to int
    board = []
    for row in gen:
      new_row = []
      for item in row:
        item = int(item)
        new_row.append(item)
      board.append(new_row)
    return board

# REMEMBER, THIS IS NOT IMPORTANT
# JUST FOR BETTER VISUALS
# json formatting thanks to jannismain
# https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92
class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small containers on single lines."""

    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""

    MAX_WIDTH = 70
    """Maximum width of a container that might be put on a single line."""

    MAX_ITEMS = 30
    """Maximum number of items in container that might be put on single line."""

    INDENTATION_CHAR = " "

    def __init__(self, *args, **kwargs):
        # using this class without indentation is pointless
        if kwargs.get("indent") is None:
            kwargs.update({"indent": 4})
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            if self._put_on_single_line(o):
                return "[" + ", ".join(self.encode(el) for el in o) + "]"
            else:
                self.indentation_level += 1
                output = [self.indent_str + self.encode(el) for el in o]
                self.indentation_level -= 1
                return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"
        elif isinstance(o, dict):
            if o:
                if self._put_on_single_line(o):
                    return "{ " + ", ".join(f"{self.encode(k)}: {self.encode(el)}" for k, el in o.items()) + " }"
                else:
                    self.indentation_level += 1
                    output = [self.indent_str + f"{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()]
                    self.indentation_level -= 1
                    return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"
            else:
                return "{}"
        elif isinstance(o, float):  # Use scientific notation for floats, where appropiate
            return format(o, "g")
        elif isinstance(o, str):  # escape newlines
            o = o.replace("\n", "\\n")
            return f'"{o}"'
        else:
            return json.dumps(o)

    def iterencode(self, o, **kwargs):
        """Required to also work with `json.dump`."""
        return self.encode(o)

    def _put_on_single_line(self, o):
        return self._primitives_only(o) and len(o) <= self.MAX_ITEMS and len(str(o)) - 2 <= self.MAX_WIDTH

    def _primitives_only(self, o: Union[list, tuple, dict]):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
        elif isinstance(o, dict):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o.values())

    @property
    def indent_str(self) -> str:
        return self.INDENTATION_CHAR*(self.indentation_level*self.indent)

# create solver
solver = s.Solver([])
# get count of puzzles
count = int(len(loadData(''))/2)

run = True
while run:
    count = int(len(loadData(''))/2)
    answer = input(f"Go? Create board {count}?: " )
    if answer == 'n' or answer == 'N':
        run = False
        break
    # generate a board
    board = genBoard(75)
    saveData(board,f"puzzle{count}")
    solvedBoard = copy.deepcopy(board)
    solvedBoard = solver.solve(board)
    saveData(board,f"solution{count}")
    
