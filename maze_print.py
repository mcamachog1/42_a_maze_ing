import mazegen
from typing import Optional, List, Tuple
from enum import Enum
import random


class FortyTwoColor(Enum):

    """Enumeration of ANSI escape codes for the '42' branding pattern.

        This class defines the specific visual identity for the cells that
        form the '42' logo within the maze.

        Attributes:
            BG_VIVID_ORANGE (str): A bright, high-saturation orange background
                using RGB (255, 140, 0) paired with a standard black
                foreground (\033[30m) for maximum legibility.
        """

    BG_VIVID_ORANGE = '\033[48;2;255;140;0m\033[30m'


class WallColor(Enum):

    """Enumeration of ANSI escape codes for maze wall backgrounds.

        This class defines various background colors used to render the walls
        or boundaries of the maze. It includes a mix of high-precision
        TrueColor (24-bit RGB) for deep tones and standard ANSI high-intensity
        codes for vibrant colors.

        Attributes:
            BG_DEEP_RED (str): A dark, somber red defined via RGB (80, 0, 0).
            BG_BRIGHT_BLUE (str): High-intensity blue background (\033[104m).
            BG_GREEN (str): Standard green background (\033[42m).
            BG_BLUE (str): Standard blue background (\033[44m).
            BG_MAGENTA (str): Standard magenta background (\033[45m).
            BG_CYAN (str): Standard cyan background (\033[46m).
        """

    # BG_DEEP_BLACK = '\033[48;2;10;10;10m'
    BG_DEEP_RED = '\033[48;2;80;0;0m'
    # BG_DEEP_BLUE = '\033[48;2;0;0;80m'
    # BG_DEEP_PURPLE = '\033[48;2;50;0;50m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'


class BackgroundColor(Enum):

    """Enumeration of ANSI escape codes for terminal background colors.

        This class provides curated color combinations, pairing background
        colors with high-contrast foreground (text) colors. It uses a mix of
        standard ANSI, 256-color palette, and TrueColor (24-bit) formats.

        Attributes:
            BG_SOFT_BEIGE (str): A soft beige background using TrueColor (RGB)
                paired with an absolute black foreground (\033[38;5;16m).
            BG_BLACK (str): A standard dark background (\033[40m) paired with
                a bright white foreground (\033[97m).
        """

    # Light background colors with dark text for better contrast
    # BG_SOFT_CYAN = '\033[106m' + '\033[30m' + '\033[38;5;16m'
    # BG_SOFT_YELLOW = '\033[103m' + '\033[38;5;16m'
    # BG_SOFT_GRAY = '\033[47m' + '\033[38;5;16m'
    BG_SOFT_BEIGE = '\033[48;2;245;245;220m' + '\033[38;5;16m'

    # Dark background colors with light text for better contrast
    BG_BLACK = '\033[40m' + '\033[97m'


"""Global configuration for maze visual elements and ANSI styling.

This section initializes the aesthetic parameters of the maze, including
randomly selected color themes and the string representations for walls
and special markers.

Attributes:
    END_COLOR (str): ANSI reset code to clear all formatting.
    BG_COLORS (str): Randomly selected background theme from BackgroundColor.
    WALL_COLORS (str): Randomly selected color for maze walls from WallColor.
    FORTY_TWO (str): Randomly selected color for the '42' pattern.
    ENTRY_COLOR (str): Bright Magenta background for the entry point.
    EXIT_COLOR (str): Bright Green background for the exit point.
    BOLD (str): ANSI code for bold/bright text.
    WALL_EAST_WEST (str): Visual representation of vertical walls (columns).
    WALL_SOUTH_NORTH (str): Visual representation of horizontal walls (rows).
    BEGIN (str): The label displayed at the maze's entry point.
    END (str): The label displayed at the maze's exit point.
"""


END_COLOR = '\033[0m'
BG_COLORS: str = random.choice(list(BackgroundColor)).value
WALL_COLORS: str = random.choice(list(WallColor)).value
FORTY_TWO: str = random.choice(list(FortyTwoColor)).value
ENTRY_COLOR = '\033[105m'
EXIT_COLOR = '\033[102m'
BOLD = '\033[1m'
WALL_EAST_WEST = "  "
WALL_SOUTH_NORTH = "   "
BEGIN = " B "
END = " E "


def change_color() -> str:

    """Randomly updates the global color scheme for the maze.

        This function selects a new random color for both the walls and the
        background by picking values from the WallColor and BackgroundColor
        enums. It modifies the global variables so the changes persist
        across re-renders.

        Returns:
            str: The newly selected ANSI escape code for the wall color.

        Global Abstractions:
            WALL_COLORS: Updated with a new random value from WallColor.
            BG_COLORS: Updated with a new random value from BackgroundColor.
        """

    global WALL_COLORS
    global BG_COLORS
    WALL_COLORS = random.choice(list(WallColor)).value
    BG_COLORS = random.choice(list(BackgroundColor)).value
    return WALL_COLORS


def get_color() -> str:

    """Retrieves the current global wall color.

        It is use for checking the new color against the current
        color to ensure that the color changes when requested.

        Returns:
            str: The ANSI escape code currently stored in the global
                variable WALL_COLORS.
        """

    return WALL_COLORS


def print_maze_ascii(
            maze: mazegen.MazeGenerator,
            stack: Optional[List[Tuple[int, int]]] = None
        ) -> None:

    """Renders the maze in the terminal using ASCII characters and ANSI colors.

        This function iterates through the maze grid and constructs a
        multi-line string representation for each row, accounting for
        walls, open paths, entry/exit points, and the solution path
        (if provided).

        Args:
            maze (mazegen.MazeGenerator): The maze instance containing the
                grid, dimensions, and metadata.
            stack (Optional[List[Tuple[int, int]]]): A list of coordinates
                representing the path to be highlighted (e.g., the solution).
                If provided, pathfinding arrows will be rendered.

        Returns:
            None: The maze is printed directly to the standard output.
        """

    def in_stack(
                cell: mazegen.Cell,
                stack: Optional[List[Tuple[int, int]]] = None
            ) -> str:

        """Determines the visual representation of a cell's interior.

                Checks if a cell is an entry point, exit point, part of the
                solution path, or a '42' branding cell, and returns the
                appropriate ANSI-colored string.

                Args:
                    cell (mazegen.Cell): The specific cell to evaluate.
                    stack (Optional[List[Tuple[int, int]]]): The current path
                    stack.

                Returns:
                    str: An ANSI escape-coded string ready for terminal output.
                """

        coord: Tuple[int, int] = (cell.x, cell.y)
        coord_entry: Tuple[int, int] = maze.entry
        coord_exit: Tuple[int, int] = maze.exit
        if coord == coord_entry:
            return ENTRY_COLOR + BOLD + BEGIN + END_COLOR
        if coord == coord_exit:
            return EXIT_COLOR + BOLD + END + END_COLOR
        if stack is None:
            return BG_COLORS + WALL_SOUTH_NORTH + END_COLOR
        if len(stack) == 0:
            return BG_COLORS + WALL_SOUTH_NORTH + END_COLOR

        if coord in stack:
            return (
                BG_COLORS + " " + BOLD +
                maze.select_arrow(cell, stack) + " " + END_COLOR
            )
        else:
            return BG_COLORS + WALL_SOUTH_NORTH + BOLD + END_COLOR

    height = maze.height
    width = maze.width
    for y in range(height):
        line_n = WALL_COLORS + WALL_EAST_WEST + END_COLOR
        line_s = WALL_COLORS + WALL_EAST_WEST + END_COLOR
        line_e = ""
        for x in range(width):
            cell = maze.grid[y][x]
            line_n += (
                WALL_COLORS + WALL_SOUTH_NORTH + END_COLOR if cell.north
                else BG_COLORS + WALL_SOUTH_NORTH + END_COLOR
            )
            line_n += WALL_COLORS + WALL_EAST_WEST + END_COLOR
            if x == 0:
                if cell.west:
                    line_e += WALL_COLORS + WALL_EAST_WEST + END_COLOR
                else:
                    line_e += BG_COLORS + WALL_EAST_WEST + END_COLOR
                line_e += in_stack(cell, stack)
            else:
                if cell.x == maze.entry[0] and cell.y == maze.entry[1]:
                    line_e += ENTRY_COLOR + BOLD + BEGIN + END_COLOR
                elif cell.x == maze.exit[0] and cell.y == maze.exit[1]:
                    line_e += EXIT_COLOR + BOLD + END + END_COLOR
                elif cell.is_42:
                    line_e += FORTY_TWO + WALL_SOUTH_NORTH + END_COLOR
                else:
                    line_e += in_stack(cell, stack)
            if x < width - 1:
                line_e += (
                    WALL_COLORS + WALL_EAST_WEST + END_COLOR
                    if cell.east else BG_COLORS + WALL_EAST_WEST + END_COLOR
                )
            else:
                line_e += (
                    WALL_COLORS + WALL_EAST_WEST + END_COLOR
                    if cell.east else BG_COLORS + WALL_EAST_WEST + END_COLOR
                )
            if y < height - 1:
                line_s += (
                    WALL_COLORS + WALL_SOUTH_NORTH + END_COLOR
                    if cell.south else BG_COLORS + WALL_SOUTH_NORTH + END_COLOR
                    )
            else:
                line_s += (
                    WALL_COLORS + WALL_SOUTH_NORTH + END_COLOR
                    if cell.south else BG_COLORS + WALL_SOUTH_NORTH + END_COLOR
                )
            if x < width - 1 and y < height - 1:
                line_s += WALL_COLORS + WALL_EAST_WEST + END_COLOR
            else:
                line_s += WALL_COLORS + WALL_EAST_WEST + END_COLOR
        if y == 0:
            print(line_n)
        print(line_e)
        print(line_s)
