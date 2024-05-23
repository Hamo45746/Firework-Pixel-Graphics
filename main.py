import glfw
from OpenGL.GL import *
import numpy as np
from grid import Grid
# import imageio

def main():
    if not glfw.init():
        print("Failed to initialise GLFW")
        return

    # Window dimensions
    x_window, y_window = 200, 150
    scaling_factor = 2
    # Logical grid dimensions
    grid_width = int(x_window / scaling_factor)
    grid_height = int(y_window / scaling_factor)

    window = glfw.create_window(x_window, y_window, "Fixel", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    grid = Grid(grid_width, grid_height)
    grid.clear()

    # Setup for rendering
    glClearColor(0, 0, 0, 1)
    glEnable(GL_POINT_SMOOTH)
    point_size = scaling_factor * 2
    glPointSize(point_size)

    is_dragging = False
    
    # writer = imageio.get_writer('Captures/sand.mp4', fps=60)

    def on_mouse_button(window, button, action, mods):
        nonlocal is_dragging
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                is_dragging = True
                create_particle_at_mouse_pos(window)
            elif action == glfw.RELEASE:
                is_dragging = False

    def on_mouse_move(window, xpos, ypos):
        if is_dragging:
            create_particle_at_mouse_pos(window)

    def create_particle_at_mouse_pos(window):
        # Scale mouse coords to grid coords
        x, y = glfw.get_cursor_pos(window)
        grid_x = int(x * grid_width / x_window)
        grid_y = int(y * grid_height / y_window)
        grid.set(grid_x, grid_y, np.random.randint(1, 0xFFFFFF)) # Colour

    glfw.set_mouse_button_callback(window, on_mouse_button)
    glfw.set_cursor_pos_callback(window, on_mouse_move)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        grid.update()

        # buffer = glReadPixels(0, 0, x_window * 2, y_window * 2, GL_RGB, GL_UNSIGNED_BYTE)
        # image = np.frombuffer(buffer, dtype=np.uint8).reshape(y_window * 2, x_window * 2, 3)
        # image = np.flip(image, axis=0)
        # writer.append_data(image)

        glClear(GL_COLOR_BUFFER_BIT) # Set prev frame black
        glBegin(GL_POINTS)
        # scale grid to window size
        for y in range(grid.height):
            for x in range(grid.width):
                colour = grid.grid[y * grid.width + x]
                if colour != 0:
                    # Extract RGB values from integer
                    r = ((colour >> 16) & 0xFF) / 255.0
                    g = ((colour >> 8) & 0xFF) / 255.0
                    b = (colour & 0xFF) / 255.0
                    # Set the current colour for drawing
                    glColor3f(r, g, b)
                    # Calculate NDC for vertex positions
                    ndc_x = x * 2 / grid.width - 1
                    ndc_y = 1 - y * 2 / grid.height
                    # Place vertex
                    glVertex2f(ndc_x, ndc_y)
        glEnd()

        glfw.swap_buffers(window)
    # writer.close()
    glfw.terminate()

if __name__ == "__main__":
    main()