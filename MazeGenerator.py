#!/usr/bin/env python3

class Cell:
    def __init__(self):
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False


class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def print_maze(self) -> None:
        for line in self.grid:
            for cell in line:
                print("#", end="")
            print()

    def remove_wall(current, neighbor):
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
                self.remove_wall(current, neighbor)
                neighbor.visited = True
                stack.append((nx, ny))
            else:
                stack.pop()    

def main() -> None:
    grid: MazeGenerator = MazeGenerator(10, 4)
    grid.print_maze()

if __name__ == "__main__":
    main()
