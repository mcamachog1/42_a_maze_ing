#!/usr/bin/env python3


from MazeGenerator import (
    MazeGenerator,
    print_maze_test_all1 as print_maze
)


def read_maze(filename: str) -> MazeGenerator:
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
    grid: MazeGenerator = MazeGenerator(width, height)

    bits: str = "0000"
    # Read the file to set the cells of the grid
    try:
        with open(filename) as file:
            for y, line in enumerate(file):
                line = line.strip()
                for x, num_hexa in enumerate(line):
                    bits = format(int(num_hexa, 16), '04b')
                    # print(f"bits: {bits} bits[0]: {bits[3]}")
                    grid.grid[y][x].north = (bits[3] == '1')
                    grid.grid[y][x].east = (bits[2] == '1')
                    grid.grid[y][x].south = (bits[1] == '1')
                    grid.grid[y][x].west = (bits[0] == '1')
    except Exception as e:
        print(f"{e}")

    return grid


def main() -> None:
    filename: str = "maze.txt"
    print_maze(read_maze(filename))


if __name__ == "__main__":
    main()
