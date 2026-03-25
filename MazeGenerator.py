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
        self.second_solution = False

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

    def format_output_hexa_file(self) -> str:
        output: str = ""
        for line in self.grid:
            for cell in line:
                output += cell.get_hexa()
            output += "\n"
        return output            

    def create_output_hexa_file(self, filename: str) -> None:
        try:
            with open(filename, "w") as file:
                file.write(self.format_output_hexa_file())
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

    def break_north_and_south(self, rows_to_break: List[int], columns_to_break: List[int]) -> None:
        for y in rows_to_break:
            for x in range(self.width):
                current = self.grid[y][x]
                # if y > 0 and self.grid[y-1][x].first_solution and current.north and current.first_solution and self.grid[y-1][x].south:
                #     self.remove_wall(current, self.grid[y-1][x])
                # if y < self.height - 1 and self.grid[y + 1][x].first_solution and current.south and current.first_solution and self.grid[y+1][x].north:
                #     self.remove_wall(current, self.grid[y + 1][x])
                print(f"x={x} y={y}")
                print(f"neig first_solution: {self.grid[y][x-1].first_solution}")
                print(f"current west: {current.west}")
                print(f"current first sol: {current.first_solution}")
                print(f"neig east: {self.grid[y][x - 1].east}")
                print()
                if x > 0 and self.grid[y][x-1].first_solution and current.west and current.first_solution and self.grid[y][x - 1].east:
                    current.west = False
                    self.grid[y][x-1].east = False
                # if x < self.width - 1 and self.grid[y][x+1].first_solution and current.east and current.first_solution and self.grid[y][x+1].west:
                #     current.east = False
                #     self.grid[y][x + 1].west = False
        # for x in columns_to_break:
        #     for y in range(self.height):
        #         current = self.grid[y][x]
        #         if y > 0 and self.grid[y-1][x].first_solution and current.north and current.first_solution and self.grid[y-1][x].south:
        #             current.north = False
        #             self.grid[y-1][x].south = False
        #         if y < self.height - 1 and self.grid[y + 1][x].first_solution and current.south and current.first_solution and self.grid[y+1][x].north:
        #             current.south = False
        #             self.grid[y + 1][x].north = False
                # if x > 0 and self.grid[y][x-1].first_solution and current.west and current.first_solution and self.grid[y][x - 1].east:
                #     self.remove_wall(current, self.grid[y][x - 1])
                # if x < self.width - 1 and self.grid[y][x+1].first_solution and current.east and current.first_solution and self.grid[y][x+1].west:
                #     self.remove_wall(current, self.grid[y][x + 1])


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

    def update_maze(self):
        # # select rows to open
        # row1: List[Tuple] = []
        # # row 1
        # row1 = self.grid[6]
        # count_south_closed: int = 0
        # for cell in row1:
        #     print(f"({cell.x},{cell.y})")
        #     if cell.south:
        #         count_south_closed += 1
        # south_percentage_closed = count_south_closed/self.width
        # print(f"% south closed: {south_percentage_closed}")
        column_to_break: List[int] = []
        count_east_closed: int = 0
        for x in range(self.width - 1):
            for y in range(self.height):
                if self.grid[y][x].east:
                    count_east_closed += 1
            east_percentage_closed = count_east_closed/self.height
            if east_percentage_closed >= 0.50:
                column_to_break.append(x)
            count_east_closed = 0

        row_to_break: List[int] = []
        count_south_closed: int = 0
        for y in range(self.height - 1):
            for x in range(self.width):
                if self.grid[y][x].south:
                    count_south_closed += 1
            south_percentage_closed = count_south_closed/self.width
            if south_percentage_closed >= 0.50:
                row_to_break.append(y)
            count_south_closed = 0
        print(f"column to break: {column_to_break} rows to break: {row_to_break}")
        self.break_north_and_south(row_to_break, column_to_break)

    def make_imperfect(self) -> None:
        for _ in range(5):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                
                neighbors = [
                    (nx, ny)
                    for nx, ny in [
                        (x, y-1),
                        (x, y+1),
                        (x-1, y),
                        (x+1, y),
                    ]
                    if 0 <= nx < self.width and 0 <= ny < self.height
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

    def new_path(self, solution_path):
        while True:
            if len(solution_path) < 3:
                return

            # escolhe dois pontos distantes no caminho
            (x1, y1) = random.choice(solution_path)
            (x2, y2) = random.choice(solution_path)

            # evitar escolher o mesmo ou vizinhos diretos

            current = self.grid[y1][x1]
            neighbor = self.grid[y2][x2]


            dx = x2 - x1
            dy = y2 - y1

            if dx == 1 and current.east:
                self.remove_wall(current, neighbor)
                return
            elif dx == -1 and current.west:
                self.remove_wall(current, neighbor)
                return
            elif dy == 1 and current.south:
                self.remove_wall(current, neighbor)
                return
            elif dy == -1 and current.north:
                self.remove_wall(current, neighbor)
                return           

            
