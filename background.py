import random
from OpenGL.GL import *
from PIL import Image
from gl_utils import *

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_background()
        self.texture_id = None
        self.additional_textures = []
        self.shader_program = create_shader_program("background_vertex_shader.glsl", "background_fragment_shader.glsl")
        self.translation_location = glGetUniformLocation(self.shader_program, 'translation')
        self.scale_location = glGetUniformLocation(self.shader_program, 'scale')

        self.setup_texture()
        self.load_additional_textures()
        self.setup_background()

    def create_background(self):
        # Initialise empty grid to represent the background scene
        grid = []

        ground_colours = [
            (0.0, 0.4, 0.0),  # Darker green
            (0.0, 0.5, 0.0),  # Mid-dark green
            (0.1, 0.6, 0.1),  # Mid-green
            (0.1, 0.7, 0.1),  # Mid-light green
            (0.2, 0.8, 0.2)   # Lighter green
        ]

        for y in range(self.height):
            row = [] 
            # Determine if row in ground or sky
            if y >= self.height * 3 // 4:
                row = [random.choice(ground_colours) for _ in range(self.width)]
            else:
                row = [(0, 0, 0)] * self.width
            grid.append(row)
        for _ in range(100):
            # Generate random coordinates for stars
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height * 3 // 4 - 1)
            grid[y][x] = (1, 1, 1)  # Note reversal of x and y for indexing
        return grid
    
    def setup_background(self):
        # Vertices for a full-screen quad with texture coordinates
        vertices = [
            -1.0, 1.0, 0.0, 1.0,  # Top-left
             1.0, 1.0, 1.0, 1.0,  # Top-right
             1.0,-1.0, 1.0, 0.0,  # Bottom-right
            -1.0,-1.0, 0.0, 0.0   # Bottom-left
        ]
        # Create VAO and VBO
        self.vao = create_vao()
        self.vbo = create_buffer(vertices)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(2 * 4))
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        self.texture_id = self.load_image_as_texture("PNGs/Background.png")

    def load_image_as_texture(self, image_path):
        img = Image.open(image_path)
        img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        # Set the texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture_id


    def load_additional_textures(self):
        # Load images as textures
        background_texture = self.load_image_as_texture("PNGs/Background.png")
        self.additional_textures.append((background_texture, (0, 0), 1)) # (texture_id, position, scale)
    
    def setup_texture(self):
        # Flatten grid + convert to format suitable for OpenGL texture
        data = []
        for row in self.grid:
            for colour in row:
                data.extend([int(c * 255) for c in colour])  # Convert to RGB
        data = bytes(data)

        # Generate and bind texture
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

    def render(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao)

        for texture_info in self.additional_textures:
            texture_id, position, scale = texture_info

            # Activate the texture unit first
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Apply the translation and scale uniforms
            glUniform2f(self.translation_location, *position)  # Unpack position tuple directly
            glUniform2f(self.scale_location, scale, scale)  # Apply scale uniformly

            # Draw the textured quad
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

            # Unbind the texture
            glBindTexture(GL_TEXTURE_2D, 0)

        glBindVertexArray(0)
        glUseProgram(0)
        glDisable(GL_BLEND)

