import random
from particle import Particle

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_height = y - random.randint(50, 80)  # Adjusted explosion height
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
        num_particles = 20
        spread = 1.5  # Spread variable to keep particles closer
        colour = random.randint(1, 0xFFFFFF)  # Random colour for firework explosion particles
        for _ in range(num_particles):
            vx, vy = (random.random() * 2 - 1) * spread, (random.random() * 2 - 1) * spread
            lifespan = 100 if random.random() < 0.5 else None  # Random decay
            self.particles.append(Particle(self.x, self.y, vx, vy, colour, lifespan))
