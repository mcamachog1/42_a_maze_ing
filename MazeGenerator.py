import random
from enum import Enum
from collections import deque
from typing import List, Dict, Any, Tuple,  Optional, Union, Deque
import sys


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
    
class CellColor(Enum):
# Reset
    # Texto (foreground)
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    # Fundo (background)
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    # Cores brilhantes (texto)
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    # Cores brilhantes (fundo)
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.x = x
        self.y = y
        self.visited = False
        self.best_path = False
        self.is_42 = False
        self.cardinal= ""

    def get_hexa(self) -> str:
        n: int = int(self.north)
        e: int = int(self.east)
        s: int = int(self.south) 
        w: int = int(self.west)
        number: int = w * 8 + s * 4 + e * 2 + n
        return format(number, "X")


class MazeGenerator:
    IMPERFECTION_ATTEMPTS: int = 3
    EXTERNAL_WALL_COLOR = CellColor.BG_BRIGHT_YELLOW.value
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


    def __init__(self, config: Dict[str, Any]):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.new_colors = False
        self.grid = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]
        self.seed = config.get("SEED", None)
    
    @classmethod
    def change_color(cls):
        cls.WALL_COLORS = random.choice(list(WallColor)).value

    def format_output_hexa_file(self) -> str:
        output: str = ""
        for line in self.grid:
            for cell in line:
                output += cell.get_hexa()
            output += "\n"
        output += "\n"
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        output += str(entry_x) + "," + str(entry_y)
        output += "\n"
        output += str(exit_x) + "," + str(exit_y)
        return output

    def create_output_hexa_file(self, path: List[Tuple[int, int]],filename: str) -> None:
        try:
            with open(filename, "w") as file:
                file.write(self.format_output_hexa_file())
        except IOError as error:
            print(f"Error: IOError. Can not write file '{filename}' {error}", file=sys.stderr)
        except Exception as error:
            print(f"Error: {error}", file=sys.stderr)
        try:
            with open(filename, "a") as file:
                file.write(self.add_path_to_file(path, filename))
        except IOError as error:
            print(f"Error: IOError. Can not write file '{filename}' {error}", file=sys.stderr)
        except Exception as error:
            print(f"Error: {error}", file=sys.stderr)

    @staticmethod
    def remove_wall(current: Cell, neighbor: Cell):
        dx: int = neighbor.x - current.x
        dy: int  = neighbor.y - current.y

        if dx == 1:  # vizinho à direita
            current.east = False
            neighbor.west = False
        elif dx == -1:  # vizinho à esquerda
            current.west = False
            neighbor.east = False
        elif dy == 1:  # vizinho em baixo
            current.south = False
            neighbor.north = False
        elif dy == -1:  # vizinho em cima
            current.north = False
            neighbor.south = False

    def generate_maze(self, start_x: int =0, start_y: int =0):
        if self.seed is not None:
            random.seed(self.seed)
        stack: List[Tuple[int, int]] = []
        # If exist a maze, close all walls and reset visited
        for line in self.grid:
            for cell in line:
                cell.north = True
                cell.east = True
                cell.south = True
                cell.west = True
                cell.visited = False
                cell.best_path = False
                cell.cardinal = ""
        
        current: Cell = self.grid[start_y][start_x]
        current.visited = True

        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            current = self.grid[y][x]

            # encontra vizinhos não visitados
            neighbors = []
            if y > 0 and not self.grid[y-1][x].visited and not self.grid[y-1][x].is_42:
                neighbors.append((x, y-1))
            if y < self.height-1 and not self.grid[y+1][x].visited and not self.grid[y+1][x].is_42:
                neighbors.append((x, y+1))
            if x > 0 and not self.grid[y][x-1].visited and not self.grid[y][x-1].is_42:
                neighbors.append((x-1, y))
            if x < self.width-1 and not self.grid[y][x+1].visited and not self.grid[y][x+1].is_42:
                neighbors.append((x+1, y))

            if neighbors:
                nx, ny = random.choice(neighbors)
                neighbor = self.grid[ny][nx]
                MazeGenerator.remove_wall(current, neighbor)
                neighbor.visited = True
                stack.append((nx, ny))
            else:
                stack.pop()
        if not self.perfect:
            self.make_imperfect()

    def close_cell_walls(self, cell: Cell) -> None:
        x = cell.x
        y = cell.y
        cell.north = True
        cell.south = True
        cell.east = True
        cell.west = True
        cell.is_42 = True
        self.grid[y][x - 1].east = True
        self.grid[y][x + 1].west = True
        self.grid[y + 1][x].north = True
        self.grid[y - 1][x].south = True

    def make_42(self):
        cx = self.width // 2
        cy = self.height // 2
        # Number 4 (column 1)
        for i in range(3):
            self.close_cell_walls(self.grid[cy - i][cx - 3])
        # Number 4 (column 2)
        self.close_cell_walls(self.grid[cy][cx - 2])
        # Number 4 (column 3)        
        for i in range(-2, 3):
            self.close_cell_walls(self.grid[cy + i][cx - 1])
        # Number 2 (column 1)
        self.close_cell_walls(self.grid[cy - 2][cx + 1])        
        for i in range(3):
            self.close_cell_walls(self.grid[cy + i][cx + 1])
        # Number 2 (column 2)
        self.close_cell_walls(self.grid[cy - 2][cx + 2])
        self.close_cell_walls(self.grid[cy][cx + 2])        
        self.close_cell_walls(self.grid[cy + 2][cx + 2])
        # Number 2 (column 3)
        self.close_cell_walls(self.grid[cy + 2][cx + 3])        
        for i in range(3):
            self.close_cell_walls(self.grid[cy - i][cx + 3])

    def print_maze_ascii(self, stack: Optional[List[Tuple]] = None):
        def in_stack(cell: Cell, stack: Optional[List[Tuple]] = None) -> str:
            coord: Tuple = (cell.x, cell.y)
            coord_entry: Tuple = self.entry # stack[0]
            coord_exit: Tuple = self.exit # stack[len(stack) - 1]
            if coord == coord_entry:
                return self.ENTRY_COLOR + self.BOLD + self.BEGIN + self.END_COLOR
            if coord == coord_exit:
                return self.EXIT_COLOR + self.BOLD + self.END + self.END_COLOR
            if stack is None:
                return self.BG_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR                
            if len(stack) == 0:
                return self.BG_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR

            if coord in stack:
                return self.BG_COLORS + " " + self.BOLD + self.select_arrow(cell, stack) + " " + self.END_COLOR
            else:
                return self.BG_COLORS + self.WALL_SOUTH_NORTH  + self.BOLD + self.END_COLOR
        
        steps: int = 0
        height = self.height
        width = self.width
        for y in range(height):
            line_n = self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR
            line_s = self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR
            line_e = ""
            for x in range(width):
                cell = self.grid[y][x]
                line_n += self.WALL_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR if cell.north else in_stack(cell, stack)
                line_n += self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR
                if x == 0:
                    if cell.west:
                        line_e += self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR
                    else:
                        line_e += self.BG_COLORS + self.WALL_EAST_WEST + self.END_COLOR
                    line_e += in_stack(cell, stack)
                else:
                    if cell.x == self.entry[0] and cell.y == self.entry[1]:
                        line_e += self.ENTRY_COLOR + self.BOLD + " B " + self.END_COLOR
                    elif cell.x == self.exit[0] and cell.y == self.exit[1]:
                        line_e += self.EXIT_COLOR + self.BOLD + " E " + self.END_COLOR                    
                    elif cell.is_42:
                        line_e += self.FORTY_TWO + self.WALL_SOUTH_NORTH + self.END_COLOR
                    else:    
                        line_e += in_stack(cell, stack)
                if x < width - 1:
                    line_e += self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR if cell.east else self.BG_COLORS + self.WALL_EAST_WEST + self.END_COLOR               
                else:
                    line_e += self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR if cell.east else self.BG_COLORS + self.WALL_EAST_WEST + self.END_COLOR
                if y < height - 1:
                    line_s += self.WALL_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR if cell.south else self.BG_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR
                else:
                    line_s += self.WALL_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR if cell.south else self.BG_COLORS + self.WALL_SOUTH_NORTH + self.END_COLOR
                if x < width - 1 and y < height - 1:
                    line_s += self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR
                else:
                    line_s += self.WALL_COLORS + self.WALL_EAST_WEST + self.END_COLOR
            if y == 0:
                print(line_n)           
            print(line_e)
            print(line_s)
        if stack is not None:
            steps = len(stack)


    def make_imperfect(self, path: Optional[List[Tuple]] = None) -> None:
        for _ in range(self.IMPERFECTION_ATTEMPTS):
            while True:
                if path is not None:
                    x, y = random.choice(path)                
                else:
                    x = random.randint(0, self.width - 1)
                    y = random.randint(0, self.height - 1)                
                if self.grid[y][x].is_42:
                    continue
                neighbors = [
                    (nx, ny)
                    for nx, ny in [
                        (x, y-1),
                        (x, y+1),
                        (x-1, y),
                        (x+1, y),
                    ]
                    if 0 <= nx < self.width and 0 <= ny < self.height and not self.grid[ny][nx].is_42
                ]

                if not neighbors:
                    continue

                nx, ny = random.choice(neighbors)
                current = self.grid[y][x]
                neighbor = self.grid[ny][nx]

                dx = nx - x
                dy = ny - y

                if dx == 1 and current.east:
                    self.remove_wall(current, neighbor)
                    break
                elif dx == -1 and current.west:
                    self.remove_wall(current, neighbor)
                    break
                elif dy == 1 and current.south:
                    self.remove_wall(current, neighbor)
                    break
                elif dy == -1 and current.north:
                    self.remove_wall(current, neighbor)
                    break

    def find_best_path(
            self,
            init_coords: Tuple[int, int],
            end_coords: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        
        paths: Dict[Tuple[int, int], Tuple[int, int]] = {}
        cells_coords: Deque[Tuple[int, int]] = deque()
        cells_coords.append(init_coords)

        while cells_coords:
            current_coords = cells_coords.popleft()
            if current_coords == end_coords:
                break
            x, y = current_coords       
            current_cell: Cell = self.grid[y][x]
            current_cell.best_path = True
            neighbors = []
            if not current_cell.north and not self.grid[y-1][x].best_path:
                neighbors.append((x, y - 1))
            if not current_cell.south and not self.grid[y+1][x].best_path:
                neighbors.append((x, y + 1))                
            if not current_cell.east and not self.grid[y][x+1].best_path:
                neighbors.append((x + 1, y))
            if not current_cell.west and not self.grid[y][x-1].best_path:
                neighbors.append((x - 1, y))   
            for n in neighbors:
                nx, ny = n
                self.grid[ny][nx].best_path = True
                paths[n] = current_coords
                cells_coords.append(n)
        
        path: List[Tuple[int, int]] = []
        path.append(current_coords)
        while current_coords != init_coords:
            current_coords = paths[current_coords]
            path.append(current_coords)
        path.reverse()
        self.set_cell_arrow_direction(path)
        return path
            
    def add_path_to_file(self, path: list, filename: str) -> str:
        coord_path = "\n"
        for coord1, coord2 in zip(path[:-1], path[1:]):
            x_1, y_1 = coord1
            x_2, y_2 = coord2
            dx = x_2 - x_1
            dy = y_2 - y_1
            coord_path += self.get_cardinal(tuple([dx, dy]))
        return coord_path
        # try:
        #     with open(filename, "a") as file:
        #         file.write(coord_path)
        # except Exception as e:
        #     print(f"{e}")

    def get_cardinal(self, coord: tuple) -> str:
        if coord == (0, -1):
            return "N"
        if coord == (0, 1):
            return "S"
        if coord == (1, 0):
            return "E"
        if coord == (-1, 0):
            return "W"

    def set_cell_arrow_direction(self, path: list) -> None:
        for coord1, coord2 in zip(path[1:-1], path[2:]):
            x_1, y_1 = coord1
            x_2, y_2 = coord2
            dx = x_2 - x_1
            dy = y_2 - y_1
            self.grid[y_1][x_1].cardinal = self.get_cardinal(tuple([dx, dy]))
           
    
    def select_arrow(self, cell: Cell, stack: List[Tuple[int, int]]) -> str:
        current = tuple([cell.x, cell.y])
        prev_position = stack.index(current) - 1
        next_position = stack.index(current) + 1
        previous_coord = stack[prev_position]
        next_coord = stack[next_position]
        px, py = previous_coord
        nx, ny = next_coord
        dx = nx - px
        dy = ny - py
        difference = tuple([dx, dy])
        if difference == tuple([1, 1]):
            if cell.cardinal == "E":
                return "\u2BA1"
            if cell.cardinal == "S":
                return "\u2BA7"            
        if difference == tuple([1, -1]):
            if cell.cardinal == "N":
                return "\u2BA5"
            if cell.cardinal == "E":
                return "\u2BA3"  
        if difference == tuple([-1, -1]):
            if cell.cardinal == "W":
                return "\u2BA2"
            if cell.cardinal == "N":
                return "\u2BA4"  
        if difference == tuple([-1, 1]):
            if cell.cardinal == "S":
                return "\u2BA6"
            if cell.cardinal == "W":
                return "\u2BA0"            
        if difference == tuple([0, 2]): # v
            return "\u2B63" 
        if difference == tuple([0, -2]):# ^
            return "\u2B61" 
        if difference == tuple([2, 0]):# >
            return "\u2B62" 
        if difference == tuple([-2, 0]):# <
            return "\u2B60"
        else:
            return "*"