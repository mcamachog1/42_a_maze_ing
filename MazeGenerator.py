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
