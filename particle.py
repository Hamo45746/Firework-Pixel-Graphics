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
