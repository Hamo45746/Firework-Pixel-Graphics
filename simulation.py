from OpenGL.GL import *
from grid import Grid
from firework import Firework
from background import Background
import random
from particle import FlameParticle, SmokeParticle


class Simulation:
    def __init__(self, width, height, scaling_factor):
        self.width = width
        self.height = height
        self.grid = Grid(width, height)
        self.fireworks = []
        self.flame_particles = []
        self.smoke_particles = []
        self.scaling_factor = scaling_factor  # Grid to window size ratio
        self.background = Background(width, height)

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

    def emit_flame_and_smoke(self):
        # Position where the fire is
        fire_x = random.uniform(114, 121)
        fire_y = random.uniform(113, 123)
        if random.random() < 0.1:  # Control the emission rate
            self.flame_particles.append(FlameParticle(fire_x, fire_y))
            self.smoke_particles.append(SmokeParticle(fire_x, fire_y))

    def render(self):
        # Clear the colour buffer with a black background
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Render the background first
        self.render_background()
        # Render fire and smoke particles
        self.render_particles()
        # Set point size for fireworks
        glPointSize(self.scaling_factor * 2)

        # Draw points
        glBegin(GL_POINTS)
        for fw in self.fireworks:
            if not fw.is_exploded:
                # Render active fireworks as white points
                glColor3f(1.0, 1.0, 1.0)
                glVertex2f(fw.x * 2 / self.grid.width - 1, 1 - fw.y * 2 / self.grid.height)
            for p in fw.particles:
                # Render particles with their colours
                glColor3f(((p.colour >> 16) & 0xFF) / 255.0, ((p.colour >> 8) & 0xFF) / 255.0, (p.colour & 0xFF) / 255.0)
                glVertex2f(p.x * 2 / self.grid.width - 1, 1 - p.y * 2 / self.grid.height)
        glEnd()
        
    def render_particles(self):
        # Render flame and smoke particles
        glBegin(GL_POINTS)
        for p in self.flame_particles + self.smoke_particles:
            glColor4f(*p.colour, 1 - p.lifespan / 100.0)
            glVertex2f(p.x * 2 / self.grid.width - 1, 1 - p.y * 2 / self.grid.height)
        glEnd()

    def render_background(self):
        # Use orthogonal projection for background rendering
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Disable depth testing and texturing
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)

        # Render the background
        self.background.render()
