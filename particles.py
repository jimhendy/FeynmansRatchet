import numpy as np
import pandas as pd

from particle import Particle


class Particles:

    def __init__(self, num_particles=50, mass=1, rotor=None, radius=0.01, random_state=1):
        np.random.seed(random_state)
        self.num_particles = num_particles
        self.mass = mass
        self.radius = radius
        self.particles = self.create_particles()
        self.rotor = rotor

    def step(self, dt=0.01):
        for i, p in enumerate(self.particles):
            p.step(dt)
            if i < self.num_particles:
                for pp in self.particles[i+1:]:
                    if p.overlaps(pp):
                        p.collide(pp)
            if self.rotor and self.rotor.overlaps(p):
                self.rotor.collide(p)
            p.bounce_off_walls()
        self.rotor.step(dt)

    def create_particles(self):
        particles = []
        while len(particles) < self.num_particles:
            new_particle = Particle(
                *np.random.uniform(self.radius, 1-self.radius, size=2),
                *np.random.uniform(-1, 1, size=2),
                mass=self.mass, radius=self.radius
            )
            overlap = False
            for p in particles:
                if p.overlaps(new_particle):
                    overlap = True
                    break
            if overlap:
                continue
            particles.append(new_particle)
        return particles
