import glfw
from OpenGL.GL import *
from simulation import Simulation
from PIL import Image
from gl_utils import create_quad_vao, create_shader_program
import os
import imageio



def create_video(frames_folder, output_name, fps=60, delete_frames=True):
    # Get a list of PNG files in the frames folder
    png_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.png')])
    
    # Create a list to store the frames
    frames = []
    
    # Read the frames and append them to the list
    for f in png_files:
        frame = imageio.imread(os.path.join(frames_folder, f))
        frames.append(frame)
    
    # Write the frames to the video
    imageio.mimsave(f"{output_name}.mp4", frames, fps=fps)
    
    # Delete the PNG files if specified
    if delete_frames:
        for f in png_files:
            os.remove(os.path.join(frames_folder, f))

def main():
    if not glfw.init():
        return

    x_window, y_window = 800, 600  # Window dimensions
    scaling_factor = 4  # Each grid cell maps to `scaling_factor x scaling_factor` pixels
    grid_width = int(x_window / scaling_factor)
    grid_height = int(y_window / scaling_factor)
    
    frame_count = 0
    max_frames = 500
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)  # Needed on macOS

    window = glfw.create_window(x_window, y_window, "Firework Pixels", None, None)
    if not window:
        glfw.terminate()
        return
    #glfw.window_hint(glfw.DOUBLEBUFFER, True)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    sim = Simulation(grid_width, grid_height, scaling_factor)

    # Create a framebuffer object (FBO) for off-screen rendering
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    
    # Create a texture to store the rendered image
    frame_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, frame_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, x_window * 2, y_window * 2, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, frame_texture, 0)
    # Unbind
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    quad_vao = create_quad_vao()
    quad_shader_program = create_shader_program("Shaders/quad_vertex_shader.glsl", "Shaders/quad_fragment_shader.glsl")

    def on_mouse_button(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            # Convert window to grid coordinates
            grid_x, grid_y = int(x / scaling_factor), int(y / scaling_factor)
            sim.launch_firework(grid_x, grid_y)

    glfw.set_mouse_button_callback(window, on_mouse_button)
    
    def on_mouse_move(window, x, y):
        grid_x = int(x / sim.scaling_factor)
        if grid_x < 10:  # Scroll left
            sim.scroll_position = max(sim.scroll_position - 1, -(sim.background.background_width - sim.width))
        elif grid_x > sim.width - 10:  # Scroll right
            sim.scroll_position = min(sim.scroll_position + 1, sim.background.background_width - sim.width)
        sim.background.update_scroll_pos(sim.scroll_position)

    glfw.set_cursor_pos_callback(window, on_mouse_move)

    while not glfw.window_should_close(window):
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glViewport(0, 0, x_window * 2, y_window * 2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        sim.update()
        sim.render()
        
        #Capture the frame
        # if frame_count < max_frames:
        #     buffer = glReadPixels(0, 0, x_window * 2, y_window * 2, GL_RGB, GL_UNSIGNED_BYTE)
        #     image = Image.frombytes("RGB", (x_window * 2, y_window * 2), buffer)
        #     image = image.transpose(Image.FLIP_TOP_BOTTOM)
        #     image.save(f"Captures/frame_{frame_count:04d}.png")
        #     frame_count += 1
            
        # Render the framebuffer texture to the screen
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, x_window * 2, y_window * 2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(quad_shader_program)
        glBindVertexArray(quad_vao)
        glBindTexture(GL_TEXTURE_2D, frame_texture)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)
        glUseProgram(0)
        
        glfw.swap_buffers(window)
        glfw.poll_events()  # Poll for events

    # Create video of window on exit
    create_video("Captures", "Sim_2")
    glfw.terminate()

if __name__ == "__main__":
    main()
