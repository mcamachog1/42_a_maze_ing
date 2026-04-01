import random
from enum import Enum
from collections import deque
from typing import List, Dict, Any, Tuple,  Optional, Union, Deque


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
        self.first_solution = False
        self.second_solution = False
        self.best_path = False
        self.is_42 = False

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
    WALL_COLORS = random.choice(list(CellColor)).value
    BG_COLORS: str
    def __init__(self, config: Dict[str, Any]):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.grid = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]
        seed = config.get("SEED", None)
        #if seed is not None:
        random.seed(seed)

    def print_maze_hexa(self) -> None:
        for line in self.grid:
            for cell in line:
                print(cell.get_hexa(), end="")
            print()

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

    def create_output_hexa_file(self, filename: str) -> None:
        try:
            with open(filename, "w") as file:
                file.write(self.format_output_hexa_file())
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
        self.WALL_COLORS = random.choice(list(CellColor)).value
        bg_colors = [c for c in CellColor if c.name.startswith("BG_")]
        self.BG_COLORS = random.choice(bg_colors).value
        stack: List[Tuple] = []
        # If exist a maze, close all walls and reset visited
        for line in self.grid:
            for cell in line:
                cell.north = True
                cell.east = True
                cell.south = True
                cell.west = True
                cell.visited = False
                cell.first_solution = False
                cell.second_solution = False
                cell.best_path = False
        
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


    def find_first_solution(self) -> List[Tuple]:
        stack = []
        start_x, start_y = self.entry
        exit_x, exit_y = self.exit
        current = self.grid[start_y][start_x]
        current.first_solution = True

        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            current = self.grid[y][x]
            self.grid[y][x].first_solution = True
            if x == exit_x and y == exit_y:
                break

            # find neighbors without visit and without wall
            neighbors = []
            if not current.north and not self.grid[y-1][x].first_solution:
                neighbors.append((x, y - 1))
            if not current.south and not self.grid[y+1][x].first_solution:
                neighbors.append((x, y + 1))                
            if not current.east and not self.grid[y][x+1].first_solution:
                neighbors.append((x + 1, y))
            if not current.west and not self.grid[y][x-1].first_solution:
                neighbors.append((x - 1, y))                

            if neighbors:
                nx, ny = random.choice(neighbors)
                neighbor = self.grid[ny][nx]
                neighbor.first_solution = True
                stack.append((nx, ny))
            else:
                stack.pop()
        return stack

    def find_second_solution(self, start_x, start_y, exit_x, exit_y) -> List[Tuple]:
        stack = []
        current = self.grid[start_y][start_x]
        current.second_solution = True

        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            current = self.grid[y][x]
            self.grid[y][x].second_solution = True
            if x == exit_x and y == exit_y:
                break

            # find neighbors without visit and without wall
            neighbors = []
            if not current.north and not self.grid[y-1][x].second_solution:
                neighbors.append((x, y - 1))
            if not current.south and not self.grid[y+1][x].second_solution:
                neighbors.append((x, y + 1))                
            if not current.east and not self.grid[y][x+1].second_solution:
                neighbors.append((x + 1, y))
            if not current.west and not self.grid[y][x-1].second_solution:
                neighbors.append((x - 1, y))                

            if neighbors:
                nx, ny = random.choice(neighbors)
                neighbor = self.grid[ny][nx]
                neighbor.second_solution = True
                stack.append((nx, ny))
            else:
                stack.pop()
        return stack

    def print_maze_ascii(self, stack: Optional[List[Tuple]] = None):

        print("\033[H\033[J", end="")  # limpa terminal
        def in_stack(cell: Cell, stack: List[Tuple]) -> str:
            coord: Tuple = (cell.x, cell.y)
            if stack is None:
                return self.BG_COLORS + "   " + self.END_COLOR                
            if len(stack) == 0:
                return self.BG_COLORS + "   " + self.END_COLOR
            coord_entry: Tuple = self.entry # stack[0]
            coord_exit: Tuple = self.exit # stack[len(stack) - 1]
            if coord == coord_entry:
                return '\033[44m' + " B " + self.END_COLOR
            if coord == coord_exit:
                return '\033[44m' + " E " + self.END_COLOR
            if coord in stack:
                return self.BG_COLORS + " * " + self.END_COLOR
            else:
                return self.BG_COLORS + "   " + self.END_COLOR
        
        steps: int = 0
        height = self.height
        width = self.width
        for y in range(height):
            line_n = self.EXTERNAL_WALL_COLOR + "+" + self.END_COLOR
            line_s = self.EXTERNAL_WALL_COLOR + "+" + self.END_COLOR
            line_e = ""
            for x in range(width):
                cell = self.grid[y][x]
                line_n += self.EXTERNAL_WALL_COLOR + "---" + self.END_COLOR if cell.north else in_stack(cell, stack)
                line_n += self.EXTERNAL_WALL_COLOR + "+" + self.END_COLOR
                if x == 0:
                    line_e += self.EXTERNAL_WALL_COLOR + "|" + self.END_COLOR + in_stack(cell, stack) if cell.west else in_stack(cell, stack)
                else:
                    if cell.x == self.entry[0] and cell.y == self.entry[1]:
                        line_e += self.WALL_COLORS + '\033[1m' + " B " + self.END_COLOR
                    elif cell.x == self.exit[0] and cell.y == self.exit[1]:
                        line_e += self.WALL_COLORS + " E " + self.END_COLOR                    
                    elif cell.is_42:
                        line_e += self.EXTERNAL_WALL_COLOR + " # " + self.END_COLOR
                    else:    
                        line_e += in_stack(cell, stack)
                if x < width - 1:
                    line_e += self.WALL_COLORS + "|" + self.END_COLOR if cell.east else self.BG_COLORS + " " + self.END_COLOR               
                else:
                    line_e += self.EXTERNAL_WALL_COLOR + "|" + self.END_COLOR if cell.east else self.BG_COLORS + " " + self.END_COLOR
                if y < height - 1:
                    line_s += self.WALL_COLORS + "---" + self.END_COLOR if cell.south else self.BG_COLORS + "   " + self.END_COLOR
                else:
                    line_s += self.EXTERNAL_WALL_COLOR + "---" + self.END_COLOR if cell.south else self.BG_COLORS + "   " + self.END_COLOR
                if x < width - 1 and y < height - 1:
                    line_s += self.WALL_COLORS + "+" + self.END_COLOR
                else:
                    line_s += self.EXTERNAL_WALL_COLOR + "+" + self.END_COLOR
            if y == 0:
                print(line_n)           
            print(line_e)
            print(line_s)
        if stack is not None:
            steps = len(stack)
        print(f"Total steps: {steps}")

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
            print(f"x={x}, y={y}, nx={nx}, ny={ny}")


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
        
        path: List[Tuples[int, int]] = []
        path.append(current_coords)
        while current_coords != init_coords:
            current_coords = paths[current_coords]
            path.append(current_coords)
        path.reverse()
        return path
            
    def add_path_to_file(self, path: list, filename: str) -> list:
        coord_path = "\n"
        for coord1, coord2 in zip(path[:-1], path[1:]):
            x_1, y_1 = coord1
            x_2, y_2 = coord2
            dx = x_2 - x_1
            dy = y_2 - y_1
            coord_path += self.get_coord(tuple([dx, dy]))
        try:
            with open(filename, "a") as file:
                file.write(coord_path)
        except Exception as e:
            print(f"{e}")

    def get_coord(self, coord: tuple) -> str:
        if coord == (0, -1):
            return "N"
        if coord == (0, 1):
            return "S"
        if coord == (1, 0):
            return "E"
        if coord == (-1, 0):
            return "W"