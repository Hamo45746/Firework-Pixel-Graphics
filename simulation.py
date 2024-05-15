from OpenGL.GL import *
import random
from grid import Grid
from firework import Firework
from background import Background
from particle import FlameParticle, SmokeParticle
from gl_utils import *


class Simulation:
    def __init__(self, width, height, scaling_factor):
        self.width = width
        self.height = height
        self.scaling_factor = scaling_factor  # Grid to window size ratio
        self.grid = Grid(width, height)
        self.background = Background(width, height)
        
        self.particle_shader_program = create_shader_program("particle_vertex_shader.glsl", "particle_fragment_shader.glsl")
        
        self.fireworks = []
        self.flame_particles = []
        self.smoke_particles = []
        
        self.firework_vao = create_vao()
        self.firework_vbo = create_buffer(np.zeros(1, dtype=np.float32))
        glBindVertexArray(self.firework_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.firework_vbo)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        self.particle_vao = create_vao()
        self.particle_vbo = create_buffer(np.zeros(1, dtype=np.float32))
        glBindVertexArray(self.particle_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.particle_vbo)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def launch_firework(self, x, y):
        self.fireworks.append(Firework(x, y))

    def update(self):
        for fw in self.fireworks[:]:
            fw.update()
            if fw.is_exploded and not fw.particles:
                self.fireworks.remove(fw)
                
        self.flame_particles = [p for p in self.flame_particles if p.update()]
        self.smoke_particles = [p for p in self.smoke_particles if p.update()]

        self.emit_flame_and_smoke()
        self.update_firework_buffers()
        self.update_particle_buffers()

    def emit_flame_and_smoke(self):
        # Position where the fire is
        fire_x = random.uniform(114, 121)
        fire_y = random.uniform(113, 123)
        if random.random() < 0.1:  # Control the emission rate
            self.flame_particles.append(FlameParticle(fire_x, fire_y))
            self.smoke_particles.append(SmokeParticle(fire_x, fire_y))

    def update_particle_buffers(self):
        particle_data = []
        for p in self.flame_particles + self.smoke_particles:
            normalized_x = p.x * 2 / self.width - 1
            normalized_y = 1 - p.y * 2 / self.height
            r, g, b = p.colour
            a = 1 - p.lifespan / 100.0
            particle_data.extend([normalized_x, normalized_y, r, g, b, a])

        # Update VBO data
        glBindBuffer(GL_ARRAY_BUFFER, self.particle_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(particle_data, dtype=np.float32), GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
    def update_firework_buffers(self):
        firework_data = []
        for fw in self.fireworks:
            if not fw.is_exploded:
                x = fw.x
                y = fw.y
                normalized_x = x * 2 / self.width - 1
                normalized_y = 1 - y * 2 / self.height
                r, g, b = fw.colour
                firework_data.extend([normalized_x, normalized_y, r, g, b, 1.0])
            for p in fw.particles:
                x = p.x
                y = p.y
                normalized_x = x * 2 / self.width - 1
                normalized_y = 1 - y * 2 / self.height
                r, g, b = p.colour
                firework_data.extend([normalized_x, normalized_y, r, g, b, 1.0])

        # Update VBO for fireworks
        glBindBuffer(GL_ARRAY_BUFFER, self.firework_vbo)
        glBufferData(GL_ARRAY_BUFFER, np.array(firework_data, dtype=np.float32), GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


    def render_fireworks(self):
        glUseProgram(self.particle_shader_program)
        glPointSize(self.scaling_factor * 2)
        glBindVertexArray(self.firework_vao)
        num_particles = 0
        for fw in self.fireworks:
            if fw.is_exploded:
                num_particles += len(fw.particles)
            else:
                num_particles += 1
        glDrawArrays(GL_POINTS, 0, num_particles)
        glBindVertexArray(0)
        glUseProgram(0)

    def render_particles(self):
        glUseProgram(self.particle_shader_program)
        glPointSize(self.scaling_factor * 2)
        glBindVertexArray(self.particle_vao)
        glDrawArrays(GL_POINTS, 0, len(self.flame_particles) + len(self.smoke_particles))
        glBindVertexArray(0)
        glUseProgram(0)

    def render(self):
        # Clear the color buffer with a black background
        # Clear the color and depth buffers
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render the background
        self.background.render()

        if len(self.fireworks) != 0:
        # Render firework particles
            self.render_fireworks()
        
        if (len(self.flame_particles) + len(self.smoke_particles)) != 0:
        # Render flame and smoke particles
            self.render_particles()
            