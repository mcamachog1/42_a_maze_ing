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

    def format_maze(self) -> str:
        output: str = ""
        for line in self.grid:
            for cell in line:
                output += cell.get_hexa()
            output += "\n"
        return output            

    def create_maze_file(self, filename: str) -> None:
        try:
            with open(filename, "w") as file:
                file.write(self.format_maze())
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


    def print_maze_ascii(self):
        height = self.height
        width = self.width
        for y in range(height):
            line_n = "+"
            line_s = "+"
            line_e = ""
            for x in range(width):
                cell = self.grid[y][x]
                line_n += "---" if cell.north else "   "
                line_n += "+"
                if x == 0:
                    line_e += "|   " if cell.west else "   "
                else:
                    line_e += "   "
                line_e += "|" if cell.east else " "                
                line_s += "---" if cell.south else "   "
                line_s += "+"
            if y == 0:
                print(line_n)           
            print(line_e)
            print(line_s)


def main() -> None:
    grid: MazeGenerator = MazeGenerator(5, 5)
    grid.generate_maze()
    grid.print_maze()
    

    grid.print_maze_ascii()

if __name__ == "__main__":
    main()
