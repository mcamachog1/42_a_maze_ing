import random
from collections import deque
from typing import List, Dict, Any, Tuple, Optional, Deque
import sys


class Cell:

    """Represents a single element within the maze grid.

        This class keep of the information related to a cell such as:
            - walls status
            - coordinates
            - flags (visited, is_42, best_path)
            - metadata for visualization.

        Attributes:
            north (bool): north wall status. True: closed, False: open
            east (bool): east wall status. True: closed, False: open
            south (bool): south wall status. True: closed, False: open
            west (bool): west wall status. True: closed, False: open
            x (int): Horizontal coordinate of the cell in the grid.
            y (int): Vertical coordinate of the cell in the grid.
            visited (bool): Flag. True: visited, False: not visited
            best_path (bool): Flag. True: belongs to solution, False: doesn't
            is_42 (bool): Flag. True: belongs to 42 branding, False: doesn't
            cardinal (str): direction (N,S,E,W) if belongs to the solution
        """

    def __init__(self, x: int, y: int) -> None:

        """Initializes a new Cell

            Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """

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

        """Calculates the hexadecimal representation of the cell's walls.

            Use a 4-bit integer representation:
            +---------+-----------+---------------+
            |   Bit   | Direction | Decimal Value |
            +---------+-----------+---------------+
            | 0 (LSB) | North     |    1          |
            |    1    | East      |    2          |
            |    2    | South     |    4          |
            |    3    | West      |    8          |
            +---------+-----------+---------------+

            Returns:
                str: A single uppercase hexadecimal character (0-F)
                representing the walls present.

            Example:
                If only North and South walls exist:
                w s e n
                1 1 0 0
                (8 * 1) + (4 * 1) + (2 * 0) + (1 * 0) = 12 -> 'C'.

                If all walls exist:
                w s e n
                1 1 1 1
                (8 * 1) + (4 * 1) + (2 * 1) + (1 * 1) = 15 -> 'F'.
        """

        n: int = int(self.north)
        e: int = int(self.east)
        s: int = int(self.south)
        w: int = int(self.west)
        number: int = w * 8 + s * 4 + e * 2 + n
        return format(number, "X")


class MazeGenerator:

    """Generates and manages a maze represented as a 2D grid of cells.

    The grid is accessed using the format [y][x], where:
        - y represents the row index
        - x represents the column index

    Attributes:
        width (int): Width of the maze grid.
        height (int): Height of the maze grid.
        entry (Tuple[int, int]): Coordinates (x, y) of the maze entry point.
        exit (Tuple[int, int]): Coordinates (x, y) of the maze exit point.
        perfect (bool): Indicates whether the maze is perfect (no loops).
        new_colors (bool): Flag indicating if new colors are used.
        grid (List[List[Cell]]): 2D list representing the maze grid.
        seed (Optional[int]): Seed for random generation (if provided).
        IMPERFECTION_ATTEMPTS (int): Number of attempts to introduce
        imperfections.
    """

    IMPERFECTION_ATTEMPTS: int = 3

    def __init__(self, config: Dict[str, Any]):

        """Initializes the MazeGenerator with a configuration dictionary.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing:
                - WIDTH (int): Width of the maze.
                - HEIGHT (int): Height of the maze.
                - ENTRY (Tuple[int, int]): Entry coordinates (x, y).
                - EXIT (Tuple[int, int]): Exit coordinates (x, y).
                - PERFECT (bool): Whether the maze should be perfect.
                - SEED (Optional[int]): Random seed (optional).

        Raises:
            KeyError: If required configuration keys are missing.
        """

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

        """Formats the maze grid and metadata into a hexadecimal string output.

        Each cell in the grid is converted to its hexadecimal representation
        using the `get_hexa()` method. The output includes:
            - The grid representation (row by row)
            - A blank line
            - Entry coordinates
            - Exit coordinates

        Returns:
            str: A formatted string representing the maze in hexadecimal
            format.
        """

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

        """Creates a file containing the maze in hexadecimal
        format and appends a path.

        The method first writes the formatted maze output to the file, then
        appends a path representation using the `add_path_to_file` method.

        Args:
            path (List[Tuple[int, int]]): List of coordinates
            representing a path through the maze.
            filename (str): Name of the file to be created or modified.

        Raises:
            IOError: If the file cannot be written.
            Exception: For any other unexpected errors during file operations.
        """

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

        """Removes the wall between two adjacent cells in the maze.

        This method updates the wall attributes of both the current cell and
        its neighboring cell based on their relative positions. It assumes
        that both cells are adjacent either horizontally or vertically.

        Args:
            current (Cell): The current cell from which the wall
            will be removed.
            neighbor (Cell): The neighboring cell adjacent to the current cell.

        Raises:
            ValueError: If the provided cells are not adjacent.
        """

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

        """Generates a maze using a depth-first search (DFS)
        backtracking algorithm.

        This method builds the maze starting from the given
        coordinates. It uses a stack-based DFS approach to
        visit cells, removing walls between adjacent cells to create
        valid paths. All cells are initially reset before generation.

        The algorithm:
            1. Resets all cells (walls closed, visited flags cleared).
            2. Starts from the initial cell.
            3. Iteratively visits unvisited neighbors.
            4. Removes walls between the current cell and a chosen neighbor.
            5. Backtracks when no unvisited neighbors are available.

        Cells marked with `is_42` are treated as blocked and
        will not be visited.

        If the maze is configured as non-perfect, additional
        walls may be removed after generation to introduce loops.

        Args:
            start_x (int, optional): Starting column index. Defaults to 0.
            start_y (int, optional): Starting row index. Defaults to 0.

        Raises:
            IndexError: If the starting coordinates are outside
            he grid bounds.
        """

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

        """Closes all walls of a given cell and updates its
        neighboring cells accordingly.

        Args:
            cell (Cell): The cell whose walls will be closed.

        Raises:
            IndexError: If the cell is located on the grid boundary
        """

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

        """Creates a "42" pattern in the maze by blocking specific cells.

        This method modifies the maze grid by closing walls of selected cells
        to visually form the number "42" near the center of the maze. It uses
        the `close_cell_walls` method to mark these cells as blocked (`is_42`)
        and ensure their walls are fully closed.

        The pattern is constructed relative to the center of the grid:
            - The number "4" is drawn on the left side of the center.
            - The number "2" is drawn on the right side of the center.

        Raises:
            IndexError: If the maze dimensions are too small to fit the "42"
                pattern or if any of the computed coordinates fall outside
                the grid boundaries.
        """

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

        """Retrieves the coordinates of all cells marked
        as part of the "42" pattern.

        This method iterates through the entire grid and collects
        the coordinates of cells where the `is_42` attribute
        is set to True.

        Returns:
            List[Tuple[int, int]]: A list of (x, y) coordinates corresponding
            to cells that belong to the "42" pattern. Returns an empty list
            if no such cells are found.
        """

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

        """Introduces imperfections into the maze by removing additional
        walls.

        This method modifies a previously generated perfect maze by
        randomly removing walls between adjacent cells

        The process runs a fixed number of attempts (`IMPERFECTION_ATTEMPTS`).
        In each attempt:
            - A random cell is selected (optionally restricted to a
                given path).
            - A valid neighboring cell is chosen.
            - If a wall exists between them, it is removed.

        Cells marked as part of the "42" pattern (`is_42 = True`)
            are excluded from selection and modification.

        Args:
            path (Optional[List[Tuple[int, int]]], optional): A list of (x, y)
                coordinates restricting where imperfections can be introduced.
                If provided, only cells within this path are considered.
                Defaults to None.

        Raises:
            RuntimeError: If no valid wall can be removed after
                repeated attempts
                (potential infinite loop in degenerate cases).
        """

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

        """Finds the shortest path between two points in the maze using BFS.

        This method performs a Breadth-First Search (BFS) starting from the
        initial coordinates to find the shortest path to the end coordinates.
        It uses the `best_path` flag in cells to mark visited nodes and
        reconstructs the path once the destination is reached.

        The algorithm:
            1. Explores the maze level by level using a queue.
            2. Tracks predecessors in a dictionary to reconstruct the path.
            3. Stops when the end coordinates are reached.
            4. Backtracks to build the final path.
            5. Assigns directional arrows using `set_cell_arrow_direction`.

        Args:
            init_coords (Tuple[int, int]): Starting coordinates (x, y).
            end_coords (Tuple[int, int]): Target coordinates (x, y).

        Returns:
            List[Tuple[int, int]]: Ordered list of coordinates representing the
            shortest path from start to end, inclusive.

        Raises:
            KeyError: If no valid path exists between the given coordinates.
            IndexError: If coordinates are outside the grid boundaries.
        """

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
