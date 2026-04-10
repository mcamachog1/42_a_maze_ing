import random
from collections import deque
from typing import List, Dict, Any, Tuple, Optional, Deque
import sys


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
        self.cardinal = ""

    def get_hexa(self) -> str:
        n: int = int(self.north)
        e: int = int(self.east)
        s: int = int(self.south)
        w: int = int(self.west)
        number: int = w * 8 + s * 4 + e * 2 + n
        return format(number, "X")


class MazeGenerator:
    IMPERFECTION_ATTEMPTS: int = 3

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
        self.seed = config.get("SEED", None) or None

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

    def create_output_hexa_file(
        self,
        path: List[Tuple[int, int]],
        filename: str
    ) -> None:
        try:
            with open(filename, "w") as file:
                file.write(self.format_output_hexa_file())
        except IOError as error:
            print(
                "Error: IOError. Can not write file "
                f"'{filename}' {error}",
                file=sys.stderr
            )
        except Exception as error:
            print(f"Error: {error}", file=sys.stderr)
        try:
            with open(filename, "a") as file:
                file.write(self.add_path_to_file(path, filename))
        except IOError as error:
            print(
                f"Error: IOError. Can not write file '{filename}' {error}",
                file=sys.stderr
            )
        except Exception as error:
            print(f"Error: {error}", file=sys.stderr)

    @staticmethod
    def remove_wall(current: Cell, neighbor: Cell) -> None:
        dx: int = neighbor.x - current.x
        dy: int = neighbor.y - current.y

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

    def generate_maze(self, start_x: int = 0, start_y: int = 0) -> None:
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
            neighbors = []
            if (
                y > 0 and not self.grid[y-1][x].visited
                and not self.grid[y-1][x].is_42
            ):
                neighbors.append((x, y-1))
            if (
                y < self.height-1 and not self.grid[y+1][x].visited
                and not self.grid[y+1][x].is_42
            ):
                neighbors.append((x, y+1))
            if (
                x > 0 and not self.grid[y][x-1].visited
                and not self.grid[y][x-1].is_42
            ):
                neighbors.append((x-1, y))
            if (
                x < self.width-1 and not self.grid[y][x+1].visited
                and not self.grid[y][x+1].is_42
            ):
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

    def make_42(self) -> None:
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

    def get_42_cells(self) -> List[Tuple[int, int]]:
        cells_42: List[Tuple[int, int]] = []
        for line in self.grid:
            for cell in line:
                if cell.is_42:
                    cells_42.append((cell.x, cell.y))
        return cells_42

    def make_imperfect(
        self,
        path: Optional[List[Tuple[int, int]]] = None
    ) -> None:
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
                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and not self.grid[ny][nx].is_42
                    )
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

    def add_path_to_file(
        self,
        path: list[Tuple[int, int]],
        filename: str
    ) -> str:
        coord_path = "\n"
        for coord1, coord2 in zip(path[:-1], path[1:]):
            x_1, y_1 = coord1
            x_2, y_2 = coord2
            dx = x_2 - x_1
            dy = y_2 - y_1
            coord_path += self.get_cardinal((dx, dy))
        return coord_path

    def get_cardinal(self, coord: Tuple[int, int]) -> str:
        if coord == (0, -1):
            return "N"
        if coord == (0, 1):
            return "S"
        if coord == (1, 0):
            return "E"
        if coord == (-1, 0):
            return "W"
        else:
            return ""

    def set_cell_arrow_direction(self, path: list[Tuple[int, int]]) -> None:
        for coord1, coord2 in zip(path[1:-1], path[2:]):
            x_1, y_1 = coord1
            x_2, y_2 = coord2
            dx = x_2 - x_1
            dy = y_2 - y_1
            self.grid[y_1][x_1].cardinal = self.get_cardinal((dx, dy))

    def select_arrow(self, cell: Cell, stack: List[Tuple[int, int]]) -> str:
        current: Tuple[int, int] = (cell.x, cell.y)
        prev_position = stack.index(current) - 1
        next_position = stack.index(current) + 1
        previous_coord = stack[prev_position]
        next_coord = stack[next_position]
        px, py = previous_coord
        nx, ny = next_coord
        dx = nx - px
        dy = ny - py
        difference: tuple[int, int] = (dx, dy)
        if difference == (1, 1):
            if cell.cardinal == "E":
                return "\u2BA1"
            if cell.cardinal == "S":
                return "\u2BA7"
        if difference == (1, -1):
            if cell.cardinal == "N":
                return "\u2BA5"
            if cell.cardinal == "E":
                return "\u2BA3"
        if difference == (-1, -1):
            if cell.cardinal == "W":
                return "\u2BA2"
            if cell.cardinal == "N":
                return "\u2BA4"
        if difference == (-1, 1):
            if cell.cardinal == "S":
                return "\u2BA6"
            if cell.cardinal == "W":
                return "\u2BA0"
        if difference == (0, 2):
            return "\u2B63"
        if difference == (0, -2):
            return "\u2B61"
        if difference == (2, 0):
            return "\u2B62"
        if difference == (-2, 0):
            return "\u2B60"
        else:
            return "*"
