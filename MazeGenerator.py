#!/usr/bin/env python3
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

    def get_hexa(self) -> str:
        n: int = int(self.north)
        e: int = int(self.east)
        s: int = int(self.south) 
        w: int = int(self.west)
        number: int = w * 8 + s * 4 + e * 2 + n
        return format(number, "X")




class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def print_maze(self) -> None:
        for line in self.grid:
            for cell in line:
                print(cell.get_hexa(), end="")
            print()

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



def print_maze_test_NW(maze: MazeGenerator):
    height = maze.height
    width = maze.width

    # topo
    #print("+" + "---+" * width)

    for y in range(height):
        line_n = "+"
        line_w = ""
        for x in range(width):
            cell = maze.grid[y][x]

            # espaço da célula
            line_n += "---" if cell.north else "   "
            line_n += "+"
            line_w += "|" if cell.west else " "
            line_w += "   "
        print(line_n)
        print(line_w)       

def print_maze_test_SE(maze: MazeGenerator):
    height = maze.height
    width = maze.width

    # topo
    #print("+" + "---+" * width)

    for y in range(height):
        line_s = "+"
        line_e = " "
        for x in range(width):
            cell = maze.grid[y][x]

            # espaço da célula
            line_s += "---" if cell.south else "   "
            line_s += "+"
            line_e += "   "
            line_e += "|" if cell.east else " "
            
        print(line_e)
        print(line_s)

def print_maze_test_all(maze: MazeGenerator):
    height = maze.height
    width = maze.width

    # topo
    #print("+" + "---+" * width)

    for y in range(height):
        line_n = "+"
        line_w = ""
        line_s = "+"
        line_e = " "
        for x in range(width):
            cell = maze.grid[y][x]

            # espaço da célula
            line_n += "---" if cell.north else "   "
            line_n += "+"
            line_w += "|" if cell.west else " "
            line_w += "   "            
            line_s += "---" if cell.south else "   "
            line_s += "+"
            line_e += "   "
            line_e += "|" if cell.east else " "

        print(line_n)
        print(line_w)            
        print(line_e)
        print(line_s)

def print_maze_test_all1(maze: MazeGenerator):
    height = maze.height
    width = maze.width

    # topo
    #print("+" + "---+" * width)

    for y in range(height):
        line_n = "+"
        line_w = ""
        line_s = "+"
        line_e = ""
        for x in range(width):
            cell = maze.grid[y][x]

            # espaço da célula
            
            line_n += "---" if cell.north else "   "
            line_n += "+"
            if x == 0 and y != 0:
                line_w += "|" if cell.west else " "
                print(line_w, end="")           
            line_s += "---" if cell.south else "   "
            line_s += "+"
            line_e += "   "
            line_e += "|" if cell.east else " "
        if y == 0:
            print(line_n)           
        print(line_e)
        print(line_s)


def main() -> None:
    grid: MazeGenerator = MazeGenerator(5, 5)
    grid.generate_maze()
    grid.print_maze()
    

    print_maze_test_NW(grid)
    print()
    print("------------------------------------")
    print()
    print_maze_test_SE(grid)
    print()
    print("------------------------------------")
    print()
    print_maze_test_all1(grid)

if __name__ == "__main__":
    main()
