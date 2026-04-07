from MazeGenerator import MazeGenerator, Cell
from typing import Optional, List, Tuple
from enum import Enum
import random


class FortyTwoColor(Enum):
    #BG_VIVID_RED     = '\033[48;2;220;0;0m\033[97m'   # vermelho vivo, texto branco
    BG_VIVID_ORANGE  = '\033[48;2;255;140;0m\033[30m' # laranja vivo, texto preto
    #BG_VIVID_MAGENTA = '\033[48;2;220;0;220m\033[97m' # magenta, texto branco


class WallColor(Enum):
    BG_DEEP_BLACK   = '\033[48;2;10;10;10m'   # preto quase total
    BG_DEEP_RED     = '\033[48;2;80;0;0m'     # vermelho muito escuro
    BG_DEEP_BLUE    = '\033[48;2;0;0;80m'     # azul profundo
    #BG_DEEP_GREEN   = '\033[48;2;0;80;0m'     # verde profundo
    BG_DEEP_PURPLE  = '\033[48;2;50;0;50m'    # roxo escuro
    #BG_DEEP_BROWN   = '\033[48;2;80;40;0m'    # marrom escuro

class BackgroundColor(Enum):
    BG_SOFT_BEIGE      = '\033[48;2;245;245;220m' + '\033[30m'  # path: texto preto sobre fundo bege suave
    #BG_SOFT_YELLOW     = '\033[103m' + '\033[30m'                # path: texto preto sobre fundo amarelo suave
    BG_SOFT_CYAN       = '\033[106m' + '\033[30m'                # path: texto preto sobre fundo ciano suave

END_COLOR = '\033[0m'
BG_COLORS: str = random.choice(list(BackgroundColor)).value
WALL_COLORS: str = random.choice(list(WallColor)).value
FORTY_TWO: str = random.choice(list(FortyTwoColor)).value
ENTRY_COLOR = '\033[30m' + '\033[105m'
EXIT_COLOR = '\033[30m' + '\033[102m'
BOLD = '\033[1m'
# UP_ARROW = '\u2934'
# DOWN_ARROW = '\u2935'
# LEFT_ARROW = '\u21E6'
# RIGHT_ARROW = '\u21E8'
WALL_EAST_WEST = "  "
WALL_SOUTH_NORTH = "   "
BEGIN = " B "
END = " E "

def change_color():
    WALL_COLORS = random.choice(list(WallColor)).value
    return WALL_COLORS

def get_color():
    return WALL_COLORS

def print_maze_ascii(maze: MazeGenerator, stack: Optional[List[Tuple]] = None):
    def in_stack(cell: Cell, stack: Optional[List[Tuple]] = None) -> str:
        coord: Tuple = (cell.x, cell.y)
        coord_entry: Tuple = maze.entry # stack[0]
        coord_exit: Tuple = maze.exit # stack[len(stack) - 1]
        if coord == coord_entry:
            return ENTRY_COLOR + BOLD + BEGIN + END_COLOR
        if coord == coord_exit:
            return EXIT_COLOR + BOLD + END + END_COLOR
        if stack is None:
            return BG_COLORS + WALL_SOUTH_NORTH + END_COLOR                
        if len(stack) == 0:
            return BG_COLORS + WALL_SOUTH_NORTH + END_COLOR

        if coord in stack:
            return BG_COLORS + " " + BOLD + maze.select_arrow(cell, stack) + " " + END_COLOR
        else:
            return BG_COLORS + WALL_SOUTH_NORTH  + BOLD + END_COLOR
    
    steps: int = 0
    height = maze.height
    width = maze.width
    for y in range(height):
        line_n = WALL_COLORS + WALL_EAST_WEST + END_COLOR
        line_s = WALL_COLORS + WALL_EAST_WEST + END_COLOR
        line_e = ""
        for x in range(width):
            cell = maze.grid[y][x]
            line_n += WALL_COLORS + WALL_SOUTH_NORTH + END_COLOR if cell.north else in_stack(cell, stack)
            line_n += WALL_COLORS + WALL_EAST_WEST + END_COLOR
            if x == 0:
                if cell.west:
                    line_e += WALL_COLORS + WALL_EAST_WEST + END_COLOR
                else:
                    line_e += BG_COLORS + WALL_EAST_WEST + END_COLOR
                line_e += in_stack(cell, stack)
            else:
                if cell.x == maze.entry[0] and cell.y == maze.entry[1]:
                    line_e += ENTRY_COLOR + BOLD + " B " + END_COLOR
                elif cell.x == maze.exit[0] and cell.y == maze.exit[1]:
                    line_e += EXIT_COLOR + BOLD + " E " + END_COLOR                    
                elif cell.is_42:
                    line_e += FORTY_TWO + WALL_SOUTH_NORTH + END_COLOR
                else:    
                    line_e += in_stack(cell, stack)
            if x < width - 1:
                line_e += WALL_COLORS + WALL_EAST_WEST + END_COLOR if cell.east else BG_COLORS + WALL_EAST_WEST + END_COLOR               
            else:
                line_e += WALL_COLORS + WALL_EAST_WEST + END_COLOR if cell.east else BG_COLORS + WALL_EAST_WEST + END_COLOR
            if y < height - 1:
                line_s += WALL_COLORS + WALL_SOUTH_NORTH + END_COLOR if cell.south else BG_COLORS + WALL_SOUTH_NORTH + END_COLOR
            else:
                line_s += WALL_COLORS + WALL_SOUTH_NORTH + END_COLOR if cell.south else BG_COLORS + WALL_SOUTH_NORTH + END_COLOR
            if x < width - 1 and y < height - 1:
                line_s += WALL_COLORS + WALL_EAST_WEST + END_COLOR
            else:
                line_s += WALL_COLORS + WALL_EAST_WEST + END_COLOR
        if y == 0:
            print(line_n)           
        print(line_e)
        print(line_s)