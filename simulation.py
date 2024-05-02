import glfw
from OpenGL.GL import *
from grid import Grid
from firework import Firework

class Simulation:
    def __init__(self, width, height, scaling_factor):
        self.grid = Grid(width, height)
        self.fireworks = []
        self.scaling_factor = scaling_factor  # Grid to window size ratio

    def launch_firework(self, x, y):
        self.fireworks.append(Firework(x, y))

    def update(self):
        for fw in self.fireworks[:]:
            fw.update()
            if fw.is_exploded and not fw.particles:
                self.fireworks.remove(fw)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glPointSize(self.scaling_factor * 2)
        glBegin(GL_POINTS)
        for fw in self.fireworks:
            if not fw.is_exploded:
                glColor3f(1.0, 1.0, 1.0)  # White for active firework
                glVertex2f(fw.x * 2 / self.grid.width - 1, 1 - fw.y * 2 / self.grid.height)
            for p in fw.particles:
                glColor3f(((p.colour >> 16) & 0xFF) / 255.0, ((p.colour >> 8) & 0xFF) / 255.0, (p.colour & 0xFF) / 255.0)
                glVertex2f(p.x * 2 / self.grid.width - 1, 1 - p.y * 2 / self.grid.height)
        glEnd()
