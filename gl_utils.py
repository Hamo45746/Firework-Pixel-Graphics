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
    # Check for compilation errors
    # if not glGetShaderiv(shader, GL_COMPILE_STATUS):
    #     error = glGetShaderInfoLog(shader).decode('utf-8')
    #     print(f'Error compiling shader: {error}')
    #     glDeleteShader(shader)
    #     raise Exception(f"Shader compilation error: {error}")
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

    # Check linking errors
    # if not glGetProgramiv(program, GL_LINK_STATUS):
    #     error = glGetProgramInfoLog(program).decode('utf-8')
    #     print(f'Error linking program: {error}')
    #     glDeleteProgram(program)
    #     raise Exception(f"Program linking error: {error}")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program
