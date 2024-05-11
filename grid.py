class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        # Init 2D array
        for _ in range(width):
            row = [0] * height
            self.cells.append(row)

    def set_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[x][y] = value

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x][y]
        return None

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.cells[x][y] = 0
