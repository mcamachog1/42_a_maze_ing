from MazeGenerator import (
    MazeGenerator
)


def read_maze_from_file(filename: str) -> MazeGenerator:
    height: int = 0
    # Read the file to get height and width
    try:
        with open(filename) as file:
            for line in file:
                line = line.strip()
                height += 1
            width: int = len(line)
    except Exception as e:
        print(f"{e}")
    base_config: Dict[str, Any] = {"WIDTH": width, "HEIGHT": height}
    maze: MazeGenerator = MazeGenerator(base_config)

    bits: str = "0000"
    # Read the file to set the cells of the grid
    try:
        with open(filename) as file:
            for y, line in enumerate(file):
                line = line.strip()
                for x, num_hexa in enumerate(line):
                    bits = format(int(num_hexa, 16), '04b')
                    # print(f"bits: {bits} bits[0]: {bits[3]}")
                    maze.grid[y][x].north = (bits[3] == '1')
                    maze.grid[y][x].east = (bits[2] == '1')
                    maze.grid[y][x].south = (bits[1] == '1')
                    maze.grid[y][x].west = (bits[0] == '1')
    except Exception as e:
        print(f"{e}")

    return maze
