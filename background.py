import random
from OpenGL.GL import *
from PIL import Image
from gl_utils import *

class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background_width = int(2.5 * self.width)
        self.grid = self.create_background()
        self.texture_id = None
        self.additional_textures = []
        self.scroll_position = 0
        self.shader_program = create_shader_program("Shaders/background_vertex_shader.glsl", "Shaders/background_fragment_shader.glsl")
        #self.translation_location = glGetUniformLocation(self.shader_program, 'translation')
        #self.scale_location = glGetUniformLocation(self.shader_program, 'scale')

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
                row = [random.choice(ground_colours) for _ in range(self.background_width)]
            else:
                row = [(0, 0, 0)] * self.background_width
            grid.append(row)
        for _ in range(150):
            # Generate random coordinates for stars
            x = random.randint(0, self.background_width - 1)
            y = random.randint(0, self.height * 3 // 4 - 1)
            grid[y][x] = (1, 1, 1)  # Note reversal of x and y for indexing
        return grid
    
    def setup_background(self):
        # create far background 
        self.setup_texture()

        # Vertices for a full-screen quad with texture coordinates
        vertices = [
            -2.3, 1.0, 0.0, 1.0,  # Top-left
            2.3, 1.0, 1.0, 1.0,  # Top-right
            2.3, -1.0, 1.0, 0.0,  # Bottom-right
            -2.3, -1.0, 0.0, 0.0   # Bottom-left
        ]
        
        first_back_vertices = [
            -1, 1.0, 0.0, 1.0,  # Top-left
            1, 1.0, 1.0, 1.0,  # Top-right
            1, -1.0, 1.0, 0.0,  # Bottom-right
            -1, -1.0, 0.0, 0.0   # Bottom-left
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
        
        # Create VAO and VBO for far back grid background
        self.grid_back_vao = create_vao()
        self.grid_back_vbo = create_buffer(first_back_vertices)
        glBindVertexArray(self.grid_back_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.grid_back_vbo)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 4 * 4, ctypes.c_void_p(2 * 4))
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

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
        # self.additional_textures.append((self.texture_id, (0,0), 1)) # This doesn't work for a bunch of reasons

    def render(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glUseProgram(self.shader_program)
        
        # render first background texture self.texture_id to its properly scaled vao
        glBindVertexArray(self.grid_back_vao)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        
        glBindVertexArray(self.vao)

        for texture_info in self.additional_textures:
            texture_id, position, scale = texture_info

            tex_left = self.scroll_position / self.width
            tex_right = (self.scroll_position + self.width) / self.width

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glUniform1f(glGetUniformLocation(self.shader_program, "scroll_position"), self.scroll_position)
            glUniform1f(glGetUniformLocation(self.shader_program, "tex_left"), tex_left)
            glUniform1f(glGetUniformLocation(self.shader_program, "tex_right"), tex_right)
            glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
            glBindTexture(GL_TEXTURE_2D, 0)

        glBindVertexArray(0)
        glUseProgram(0)
        glDisable(GL_BLEND)

    def update_scroll_pos(self, new_scroll_pos):
        self.scroll_position = new_scroll_pos