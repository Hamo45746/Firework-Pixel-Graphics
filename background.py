import random
from OpenGL.GL import *
from PIL import Image

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_background()
        self.texture_id = None
        self.additional_textures = []
        self.setup_texture()
        self.load_additional_textures()

    def create_background(self):
        # Initialise empty grid to represent the background scene
        grid = []

        # Define shades of green for the grass
        ground_colours = [
            (0.0, 0.4, 0.0),  # Darker green
            (0.0, 0.5, 0.0),  # Mid-dark green
            (0.1, 0.6, 0.1),  # Mid-green
            (0.1, 0.7, 0.1),  # Mid-light green
            (0.2, 0.8, 0.2)   # Lighter green
        ]

        # Iterate over each row
        for y in range(self.height):
            row = []  # Initialise an empty row
            # Determine if row in ground or sky
            if y >= self.height * 3 // 4:
                # If in ground randomly select a shade of green for each pixel
                row = [random.choice(ground_colours) for _ in range(self.width)]
            else:
                # If in sky set row to black
                row = [(0, 0, 0)] * self.width
            # Add row to grid
            grid.append(row)
        # Add stars to the sky
        for _ in range(100):
            # Generate random coordinates for stars
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height * 3 // 4 - 1)
            # Set colour of the point to white for stars
            grid[y][x] = (1, 1, 1)  # Note reversal of x and y for proper indexing
        return grid

    def load_image_as_texture(self, image_path):
        # Load an image and convert it to a texture
        img = Image.open(image_path)
        img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture_id, img.width, img.height

    def load_additional_textures(self):
        # Load specific images as textures
        tree_texture = self.load_image_as_texture("PNGs/Pixel_Pine_1.png")
        #tent_texture = self.load_image_as_texture("path/to/tent.png")
        self.additional_textures.append((tree_texture, (0.85, -0.2), 0.7))
        self.additional_textures.append((tree_texture, (-0.9, -0.2), 0.7))
        self.additional_textures.append((tree_texture, (0.5, -0.2), 0.7))  # (texture_id, position, scale)
        self.additional_textures.append((tree_texture, (0.7, -0.35), 0.8))
        self.additional_textures.append((tree_texture, (0.9, -0.55), 0.7))
        #self.additional_textures.append((tent_texture, (0.3, 0.8), 0.1))
    
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
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, 1)
        glTexCoord2f(1, 0); glVertex2f(1, 1)
        glTexCoord2f(1, 1); glVertex2f(1, -1)
        glTexCoord2f(0, 1); glVertex2f(-1, -1)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glEnable(GL_TEXTURE_2D)
        for texture, position, scale in self.additional_textures:
            glBindTexture(GL_TEXTURE_2D, texture[0])
            glBegin(GL_QUADS)
            x, y = position
            w, h = texture[1] * scale / self.width, texture[2] * scale / self.height  # Adjust scale
            glTexCoord2f(0, 0); glVertex2f(x - w, y - h)
            glTexCoord2f(1, 0); glVertex2f(x + w, y - h)
            glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
            glTexCoord2f(0, 1); glVertex2f(x - w, y + h)
            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        
