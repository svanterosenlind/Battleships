import numpy as np
from numpy.core.multiarray import ndarray
import math
FPS = 30

class Battleship:
    pos: ndarray
    vel: ndarray
    acc: ndarray

    def __init__(self):
        self.pos = np.array([400, 400])
        self.vel = np.array([0, 0])
        self.acc = np.array([0, 0])

        self.angle = 0
        self.angle_vel = 0
        self.angle_acc = 0

        self.reload_time = 2    # In seconds
        self.reload_status = 0

        self.size = (20, 12)  # length, width
        self.max_F = 30000
        self.m = 10000  # Weight in kilos
        self.J = 100000  # Moment of inertia

        self.fric = 100
        self.angle_fric = 1000000

        self.shot_deviation = 0.1
    def update(self):
        self.vel = self.vel + self.acc/FPS
        self.pos = self.pos + self.vel/FPS
        self.angle_vel += self.angle_acc/FPS
        self.angle += self.angle_vel/FPS

    def corners(self) -> ndarray:
        rotator = np.array([[math.cos(self.angle), math.sin(self.angle)], [-math.sin(self.angle), math.cos(self.angle)]])
        p1 = self.pos + np.dot(rotator, np.array([-self.size[0]/3, self.size[1]/2]))
        p2 = self.pos + np.dot(rotator, np.array([2 * self.size[0] / 3, self.size[1] / 2]))
        p3 = self.pos + np.dot(rotator, np.array([2 * self.size[0] / 3, - self.size[1] / 2]))
        p4 = self.pos + np.dot(rotator, np.array([-self.size[0]/3, - self.size[1]/2]))
        return np.array([p1, p2, p3, p4])

    def shoot_left(self):
        corn = self.corners()
        p1 = (3 * corn[3] + corn[2])/4
        p2 = (corn[3] + corn[2]) / 2
        p3 = (3 * corn[2] + corn[3]) / 4
        return [Cannonball(p1, self.angle + math.pi/2 + self.shot_deviation),
                Cannonball(p2, self.angle + math.pi/2),
                Cannonball(p3, self.angle + math.pi/2 - self.shot_deviation)]

    def shoot_right(self):
        corn = self.corners()
        p1 = (3 * corn[0] + corn[1]) / 4
        p2 = (corn[0] + corn[1]) / 2
        p3 = (3 * corn[1] + corn[0]) / 4
        return [Cannonball(p1, self.angle - math.pi/2 - self.shot_deviation),
                Cannonball(p2, self.angle - math.pi/2),
                Cannonball(p3, self.angle - math.pi/2 + self.shot_deviation)]


class PlayerBattleship(Battleship):
    def __init__(self):
        super().__init__()

    def calculate_FM(self, keys):
        [up, right, left] = keys
        F = np.array([0, 0])
        M = 0
        direction = np.array([math.cos(self.angle), -math.sin(self.angle)])
        ortho_direction = np.array([math.cos(self.angle + math.pi/2), -math.sin(self.angle + math.pi/2)])
        #   Calculate added force and moment from steering inputs
        if up:
            F = F + np.array([self.max_F]*2) * direction
        if left and right:
            pass
        elif left:
            M = (np.dot(self.vel, direction)+2) * 1000
            F = F + (np.array([M]*2) * ortho_direction) / 100
        elif right:
            M = -(np.dot(self.vel, direction)+2) * 1000
            F = F - (np.array([M] * 2) * ortho_direction) / 100
        #   Calculate friction and rotational friction
        F = F - np.linalg.norm(self.vel) * self.vel * self.fric
        M = M - (abs(self.angle_vel) ** 2) * self.angle_vel * self.angle_fric

        self.acc = F/self.m
        self.angle_acc = M/self.J

    def shoot(self, keys):
        a, d = keys
        self.reload_status -= 1
        if a and self.reload_status <= 0:
            self.reload_status = self.reload_time * FPS
            return self.shoot_left()
        elif d and self.reload_status <= 0:
            self.reload_status = self.reload_time * FPS
            return self.shoot_right()
        return []

class Cannonball:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.vel = 5
        self.distance_left = 60

    def update(self):
        self.pos = self.pos + np.array([self.vel]*2) * np.array([math.cos(self.angle), -math.sin(self.angle)])
        self.distance_left -= self.vel