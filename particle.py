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
        self.vy += 0.02  # Gravity effect
        self.y += self.vy
        if self.lifespan is not None:
            self.lifespan -= 1
            return self.lifespan > 0
        return True

class FlameParticle(Particle):
    def __init__(self, x, y):
        vx = random.uniform(-0.03, 0.03)
        vy = random.uniform(-0.1, -0.05)
        red = 1
        green = random.uniform(0.3, 0.8)
        blue = 0
        initial_color = (red, green, blue)  # Fiery colour
        super().__init__(x, y, vx, vy, initial_color, 200)

    def update(self):
        self.x += self.vx
        self.vy += 0.0003  # Gravity effect
        self.y += self.vy
        
        if self.lifespan:
            self.lifespan -= 1
            fade = self.lifespan / 200.0
            self.colour = (0.8 * fade, self.colour[1] * fade, self.colour[2] * fade)
        return self.lifespan > 0

class SmokeParticle(Particle):
    def __init__(self, x, y):
        vx = random.uniform(-0.03, 0.03)
        vy = random.uniform(-0.1, -0.05)
        initial_color = (0.6, 0.6, 0.6)  # Smoky color
        super().__init__(x, y, vx, vy, initial_color, 300)

    def update(self):
        self.x += self.vx
        self.vy += 0.00015  # Gravity effect
        self.y += self.vy

        if self.lifespan:
            self.lifespan -= 1
            fade = self.lifespan / 300
            self.colour = (1 * fade, (self.colour[1] / 1.2) * fade, self.colour[2] * fade)
        return self.lifespan > 0
