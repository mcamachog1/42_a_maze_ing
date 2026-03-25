import random
from typing import List, Dict, Any, Tuple,  Optional, Union


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

    def get_hexa(self) -> str:
        n: int = int(self.north)
        e: int = int(self.east)
        s: int = int(self.south) 
        w: int = int(self.west)
        number: int = w * 8 + s * 4 + e * 2 + n
        return format(number, "X")


class MazeGenerator:
    def __init__(self, config: Dict[str, Any]):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.grid = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]
        seed = config.get("SEED", None)
        if seed is not None:
            random.seed(seed)

    def print_maze_hexa(self) -> None:
        for line in self.grid:
            for cell in line:
                print(cell.get_hexa(), end="")
            print()

    def format_output_file(self) -> str:
        output: str = ""
        for line in self.grid:
            for cell in line:
                output += cell.get_hexa()
            output += "\n"
        return output            

    def create_output_file(self, filename: str) -> None:
        try:
            with open(filename, "w") as file:
                file.write(self.format_output_file())
        except Exception as error:
            print("Error:", error)

    @staticmethod
    def remove_wall(current: Cell, neighbor: Cell):
        dx = neighbor.x - current.x
        dy = neighbor.y - current.y

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

    def generate_maze(self, start_x=0, start_y=0):
        stack = []
        current = self.grid[start_y][start_x]
        current.visited = True

        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            current = self.grid[y][x]

            # encontra vizinhos não visitados
            neighbors = []
            if y > 0 and not self.grid[y-1][x].visited:
                neighbors.append((x, y-1))
            if y < self.height-1 and not self.grid[y+1][x].visited:
                neighbors.append((x, y+1))
            if x > 0 and not self.grid[y][x-1].visited:
                neighbors.append((x-1, y))
            if x < self.width-1 and not self.grid[y][x+1].visited:
                neighbors.append((x+1, y))

            if neighbors:
                nx, ny = random.choice(neighbors)
                neighbor = self.grid[ny][nx]
                MazeGenerator.remove_wall(current, neighbor)
                neighbor.visited = True
                stack.append((nx, ny))
            else:
                stack.pop() 

    def find_first_solution(self, start_x, start_y, exit_x, exit_y) -> List[Tuple]:
        stack = []
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

    def print_maze_ascii(self, stack: List[Tuple]):

        def in_stack(cell: Cell, stack: List[Tuple]) -> str:
            coord: Tuple = (cell.x, cell.y)
            if len(stack) == 0:
                return "   "
            coord_entry: Tuple = stack[0]
            coord_exit: Tuple = stack[len(stack) - 1]
            if coord == coord_entry:
                return " B "
            if coord == coord_exit:
                return " E " 
            if coord in stack:
                return " * "
            else:
                return "   "
        
        height = self.height
        width = self.width
        for y in range(height):
            line_n = "+"
            line_s = "+"
            line_e = ""
            for x in range(width):
                cell = self.grid[y][x]
                line_n += "---" if cell.north else in_stack(cell, stack)
                line_n += "+"
                if x == 0:
                    line_e += "|" + in_stack(cell, stack) if cell.west else in_stack(cell, stack)
                else:
                    line_e += in_stack(cell, stack)
                line_e += "|" if cell.east else " "                
                line_s += "---" if cell.south else "   "
                line_s += "+"
            if y == 0:
                print(line_n)           
            print(line_e)
            print(line_s)
