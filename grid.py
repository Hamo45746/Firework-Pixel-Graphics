class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [0] * (width * height)

    def clear(self):
        self.grid = [0] * (self.width * self.height)

    def set(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y * self.width + x] = color

    def swap(self, a, b):
        self.grid[a], self.grid[b] = self.grid[b], self.grid[a]

    def is_empty(self, index):
        return self.grid[index] == 0

    def update_pixel(self, i):
        below = i + self.width
        below_left = below - 1
        below_right = below + 1

        if below < len(self.grid) and self.is_empty(below):
            self.swap(i, below)
        elif below_left < len(self.grid) and self.is_empty(below_left):
            self.swap(i, below_left)
        elif below_right < len(self.grid) and self.is_empty(below_right):
            self.swap(i, below_right)

    def update(self):
        for i in range(len(self.grid) - self.width - 1, 0, -1):
            self.update_pixel(i)
