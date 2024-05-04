import random
import math
from particle import Particle

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_height = y - random.randint(50, 100)
        self.is_exploded = False
        self.colour = 0xFFFFFF  # Fireworks are white
        self.particles = []

    def update(self):
        if not self.is_exploded:
            self.y -= 1  # Move up
            if self.y <= self.target_height:
                self.is_exploded = True
                self.explode()
        else:
            self.particles = [p for p in self.particles if p.update()]

    def explode(self):
        num_particles = 60
        spread = 0.7
        colour = random.randint(1, 0xFFFFFF)  # Random colour
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)  # Angle between 0 and 360 degrees
            magnitude = random.uniform(0, spread)   # Magnitude from 0 to spread
            # Horizontal velocity
            vx = magnitude * math.cos(angle)
            # Vertical velocity
            vy = magnitude * math.sin(angle) - 0.75
            lifespan = 150
            self.particles.append(Particle(self.x, self.y, vx, vy, colour, lifespan))
