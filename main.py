import glfw
from OpenGL.GL import *
from simulation import Simulation

def main():
    if not glfw.init():
        return

    x_window, y_window = 400, 300  # Window dimensions
    scaling_factor = 2  # Each grid cell maps to `scaling_factor x scaling_factor` pixels
    grid_width = x_window // scaling_factor
    grid_height = y_window // scaling_factor
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)  # Needed on macOS

    window = glfw.create_window(x_window, y_window, "Firework Pixels", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.window_hint(glfw.DOUBLEBUFFER, True)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    sim = Simulation(grid_width, grid_height, scaling_factor)

    def on_mouse_button(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            # Convert window to grid coordinates
            grid_x, grid_y = int(x / scaling_factor), int(y / scaling_factor)
            sim.launch_firework(grid_x, grid_y)

    glfw.set_mouse_button_callback(window, on_mouse_button)

    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set the clear colour to black
        glClear(GL_COLOR_BUFFER_BIT)  # Clear the colour buffer
        glEnable(GL_BLEND)  # Enable blending for alpha values
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blending function

        sim.update()
        sim.render()
        
        glfw.swap_buffers(window)
        glfw.poll_events()  # Poll for events

    glfw.terminate()

if __name__ == "__main__":
    main()
