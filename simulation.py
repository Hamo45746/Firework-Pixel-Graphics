import glfw
from OpenGL.GL import *
import numpy as np
from grid import Grid

def main():
    if not glfw.init():
        print("Failed to initialise GLFW")
        return

    # Window dimensions
    x_window, y_window = 200, 150
    scaling_factor = 2
    # Logical grid dimensions (smaller than the window)
    grid_width = int(x_window / scaling_factor)
    grid_height = int(y_window / scaling_factor)

    window = glfw.create_window(x_window, y_window, "Fixel", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
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
        # Scale mouse coordinates to grid coordinates
        x, y = glfw.get_cursor_pos(window)
        grid_x, grid_y = int(x * grid_width / x_window), int(y * grid_height / y_window)
        grid.set(grid_x, grid_y, np.random.randint(1, 0xFFFFFF))

    glfw.set_mouse_button_callback(window, on_mouse_button)
    glfw.set_cursor_pos_callback(window, on_mouse_move)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        grid.update()

        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_POINTS)
        # Adjust rendering to scale grid to window size
        for y in range(grid.height):
            for x in range(grid.width):
                colour = grid.grid[y * grid.width + x]
                if colour != 0:
                    glColor3f(((colour >> 16) & 0xFF) / 255.0, ((colour >> 8) & 0xFF) / 255.0, (colour & 0xFF) / 255.0)
                    glVertex2f(x * 2 / grid_width - 1, 1 - y * 2 / grid_height)
        glEnd()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
