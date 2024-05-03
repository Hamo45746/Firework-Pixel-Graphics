import random

class Particle:
    def __init__(self, x, y, vx, vy, colour, lifespan=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colour = colour
        self.lifespan = lifespan

    def update(self):
        self.x += self.vx
        self.vy += 0.025  # Gravity effect of vertical velocity
        self.y += self.vy
        if self.lifespan is not None:
            self.lifespan -= 1
            return self.lifespan > 0
        return True

class FlameParticle(Particle):
    def __init__(self, x, y):
        vx = random.uniform(-0.05, 0.05)
        vy = random.uniform(-0.2, -0.1)
        
        initial_color = (1, random.uniform(0.3, 0.6), 0)  # Fiery colour
        super().__init__(x, y, vx, vy, initial_color, 100)

    def update(self):
        self.x += self.vx
        self.vy += 0.001  # Gravity effect of vertical velocity
        self.y += self.vy
        # Fade to transparency
        if self.lifespan:
            self.lifespan -= 1
            fade = self.lifespan / 100.0
            self.colour = (1 * fade, (self.colour[1] / 1.2) * fade, 0)
        return self.lifespan > 0

class SmokeParticle(Particle):
    def __init__(self, x, y):
        vx = random.uniform(-0.05, 0.05)
        vy = random.uniform(-0.2, -0.1)
        lifespan = 100 if random.random() < 0.5 else None  # Random decay
        initial_color = (0.6, 0.6, 0.6)  # Smoky color
        super().__init__(x, y, vx, vy, initial_color, 150)

    def update(self):
        self.x += self.vx
        self.vy += 0.001  # Gravity effect of vertical velocity
        self.y += self.vy
        # Fade to transparency
        if self.lifespan:
            self.lifespan -= 1
            fade = self.lifespan / 150
            self.colour = (1 * fade, (self.colour[1] / 1.2) * fade, 0)
        return self.lifespan > 0
