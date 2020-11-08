import numpy as np


class Particle:

    num_particles = 1

    def __init__(self, x, y, v_x, v_y, mass=1, radius=0.01):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.mass = mass
        self.radius = radius
        self.particle_number = Particle.num_particles
        Particle.num_particles += 1

    def __repr__(self):
        return f'Particle {self.particle_number}: ({self.x:.2f}, {self.y:.2f}), ({self.v_x:.2f}, {self.v_y:.2f})'

    def collide(self, other):
        self._collide_direction('x', other)
        self._collide_direction('y', other)

    def _collide_direction(self, direction, other):
        m_a = self.mass
        m_b = other.mass
        speed = f'v_{direction}'
        v_a_i = getattr(self, speed)
        v_b_i = getattr(other, speed)
        v_a_f = Particle.collision_speed(m_a, m_b, v_a_i, v_b_i)
        v_b_f = Particle.collision_speed(m_b, m_a, v_b_i, v_a_i)
        setattr(self, speed, v_a_f)
        setattr(other, speed, v_b_f)

    @staticmethod
    def collision_speed(m_a, m_b, v_a_i, v_b_i):
        return (m_a-m_b)/(m_a+m_b) * v_a_i + (2*m_b)/(m_a+m_b) * v_b_i

    def overlaps(self, other):
        inside_radius = np.hypot(
            self.x - other.x,
            self.y - other.y
        ) <= (self.radius + other.radius)
        if not inside_radius: 
            return False
        incoming = self.next_step_closer(other)
        return incoming

    def next_step_closer(self, other):
        next_distance = np.hypot(
            (self.x + self.v_x) - (other.x + other.v_x),
            (self.y + self.v_y) - (other.y + other.v_y)
        )
        reversed_distance = np.hypot(
            (self.x - self.v_x) - (other.x - other.v_x),
            (self.y - self.v_y) - (other.y - other.v_y)
        )
        return next_distance < reversed_distance

    def step(self, dt):
        self.x += self.v_x * dt
        self.y += self.v_y * dt

    def bounce_off_walls(self):
        self._wall_bounce_direction('x')
        self._wall_bounce_direction('y')

    def _wall_bounce_direction(self, direction):
        position = getattr(self, direction)
        speed = f'v_{direction}'
        if position < 0:
            setattr(self, direction, -position / 2)
            setattr(self, speed, -getattr(self, speed))
        elif position > 1:
            setattr(self, direction, 2-position)
            setattr(self, speed, -getattr(self, speed))
