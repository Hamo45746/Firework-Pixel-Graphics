import random
from OpenGL.GL import *

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_background()
        self.texture_id = None
        self.setup_texture()

    def create_background(self):
        # Initialize an empty grid to represent the background scene
        grid = []

        # Define multiple shades of green for the grass
        ground_colours = [
            (0.0, 0.4, 0.0),  # Darker green
            (0.0, 0.5, 0.0),  # Mid-dark green
            (0.1, 0.6, 0.1),  # Mid-green
            (0.1, 0.7, 0.1),  # Mid-light green
            (0.2, 0.8, 0.2)   # Lighter green
        ]

        # Iterate over each row
        for y in range(self.height):
            row = []  # Initialize an empty row
            # Determine if the current row is in the ground or sky
            if y >= self.height * 3 // 4:
                # If in the ground portion, randomly select a shade of green for each pixel
                row = [random.choice(ground_colours) for _ in range(self.width)]
            else:
                # If in the sky portion, set the entire row to black
                row = [(0, 0, 0)] * self.width
            # Add the row to the grid
            grid.append(row)
        # Add stars to the sky portion of the grid
        for _ in range(100):
            # Generate random coordinates for the star within the sky portion
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height * 3 // 4 - 1)
            # Set the colour of the point to white to represent a star
            grid[y][x] = (1, 1, 1)  # Note the reversal of x and y for proper indexing
        return grid

    def setup_texture(self):
        # Flatten grid and convert to a format suitable for OpenGL texture
        data = []
        for row in self.grid:
            for colour in row:
                data.extend([int(c * 255) for c in colour])  # Convert to RGB values
        data = bytes(data)

        # Generate and bind the texture
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

    def render(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, 1)
        glTexCoord2f(1, 0); glVertex2f(1, 1)
        glTexCoord2f(1, 1); glVertex2f(1, -1)
        glTexCoord2f(0, 1); glVertex2f(-1, -1)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
