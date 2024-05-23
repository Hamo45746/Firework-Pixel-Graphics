from OpenGL.GL import *
import numpy as np

def create_buffer(data, data_type=GL_ARRAY_BUFFER, usage=GL_DYNAMIC_DRAW):
    """ Create a buffer (VBO or EBO) and upload data to it. """
    buffer_id = glGenBuffers(1)
    glBindBuffer(data_type, buffer_id)
    array_type = GLfloat if data_type == GL_ARRAY_BUFFER else GLuint
    glBufferData(data_type, np.array(data, dtype=array_type), usage)
    glBindBuffer(data_type, 0)
    return buffer_id

def create_vao():
    """ Create a Vertex Array Object (VAO). """
    vao_id = glGenVertexArrays(1)
    glBindVertexArray(vao_id)
    return vao_id

def load_shader(source, shader_type):
    """Compiles a shader from provided source code."""
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def create_shader_program(vertex_source_path, fragment_source_path):
    """Creates a shader program from vertex and fragment shader sources."""
    with open(vertex_source_path, 'r') as f:
        vertex_source = f.read()
    with open(fragment_source_path, 'r') as f:
        fragment_source = f.read()

    vertex_shader = load_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = load_shader(fragment_source, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program

def create_quad_vao():
    quad_vertices = np.array([
        # positions     # texture coords
        -1.0,  1.0,      0.0, 1.0,
        -1.0, -1.0,      0.0, 0.0,
         1.0, -1.0,      1.0, 0.0,
         1.0,  1.0,      1.0, 1.0,
    ], dtype=np.float32)

    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    vao = create_vao()
    vbo = create_buffer(quad_vertices, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
    ebo = create_buffer(indices, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao