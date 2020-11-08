import numpy as np
import logging

logger = logging.getLogger(__name__)

"""
ALL angles(theta) are defined from y axis moving to positive x direction
"""


class Rotor:

    def __init__(self, length=0.25, mass=100):
        self.length = length
        self.fixed_point = (0.5, 0.5)
        self.mass = mass
        self.theta = 0
        self.theta_history = [self.theta]
        self.v_theta = 0
        self.v_theta_history = [self.v_theta]
        self.free_point = self.get_free_point()
        self.moment_of_inertia = 1/3 * self.mass * self.length**2

    def get_free_point(self):
        return (
            self.fixed_point[0] + self.length * np.sin(self.theta),
            self.fixed_point[1] + self.length * np.cos(self.theta)
        )

    def step(self, dt):
        self.theta = (self.theta + self.v_theta * dt) % (2*np.pi)
        self.free_point = self.get_free_point()
        self.theta_history.append(self.theta if self.theta < np.pi else self.theta - 2 * np.pi)
        self.v_theta_history.append(self.v_theta)

    def overlaps(self, particle):
        self.add_particle_angular_properties(particle)
        inside_rotar_span = (particle.r <= self.length) and (
            particle.r_free_point <= self.length)
        if not inside_rotar_span:
            return False
        # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        distance = abs(
            (self.free_point[1]-self.fixed_point[1]) * particle.x
            - (self.free_point[0]-self.fixed_point[0]) * particle.y
            + self.free_point[0] * self.fixed_point[1]
            - self.free_point[1] * self.fixed_point[0]
        ) / self.length
        within_a_radius = distance <= particle.radius
        if not within_a_radius:
            return False
        d_theta = particle.theta - self.theta
        is_clockwise = (d_theta > 0 and d_theta < np.pi) or d_theta < -np.pi
        incoming = (is_clockwise and particle.v_theta < 0) or (
            not is_clockwise and particle.v_theta > 0)
        return incoming

    @staticmethod
    def get_particle_r(particle, point):
        dx = particle.x - point[0]
        dy = particle.y - point[1]
        return np.hypot(dx, dy)

    def add_particle_angular_properties(self, particle):
        dx = particle.x - self.fixed_point[0]
        dy = particle.y - self.fixed_point[1]
        particle.r = np.hypot(dx, dy)
        particle.r_free_point = Rotor.get_particle_r(particle, self.free_point)
        particle.theta = np.arctan2(dx, dy) % (2*np.pi)
        particle.v_r = (dx * particle.v_x + dy * particle.v_y) / particle.r
        particle.v_theta = (
            dy * particle.v_x - dx * particle.v_y) / particle.r**2
        pass

    def collide(self, particle):
        I_r = self.moment_of_inertia
        I_p = particle.mass * particle.r**2
        w_r_i = self.v_theta
        w_p_i = particle.v_theta
        w_r_f = Rotor.collison_speed(I_r, I_p, w_r_i, w_p_i)
        w_p_f = Rotor.collison_speed(I_p, I_r, w_p_i, w_r_i)
        self.v_theta = w_r_f
        Rotor.set_particle_final_speed(particle, w_p_f)
        pass

    def __repr__(self):
        return f'ROTOR ({self.free_point[0]:.2f}, {self.free_point[1]:.2f}), ({self.theta:.2f}, {self.v_theta:.2f})'

    @staticmethod
    def set_particle_final_speed(particle, v_theta):
        sin_theta = np.sin(particle.theta)
        cos_theta = np.cos(particle.theta)
        particle.v_x = particle.v_r * sin_theta + particle.r * v_theta * cos_theta
        particle.v_y = particle.v_r * cos_theta - particle.r * v_theta * sin_theta

    @staticmethod
    def collison_speed(I_a, I_b, w_a_i, w_b_i):
        return (I_a-I_b)/(I_a+I_b) * w_a_i + (2*I_b)/(I_a+I_b) * w_b_i
