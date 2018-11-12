import numpy as np
from numpy.core.multiarray import ndarray
import math
import random
FPS = 10

class Battleship:
    def __init__(self, sea):
        self.sea = sea

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

        #   looparound in the x direction
        if self.pos[0] < 0:
            self.pos[0] = self.sea[0]
        elif self.pos[0] > self.sea[0]:
            self.pos[0] = 0
        #   looparound in the y direction
        if self.pos[1] < 0:
            self.pos[1] = self.sea[1]
        elif self.pos[1] > self.sea[1]:
            self.pos[1] = 0

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
        return [Cannonball(p1, self.angle + math.pi/2 + self.shot_deviation, self),
                Cannonball(p2, self.angle + math.pi/2, self),
                Cannonball(p3, self.angle + math.pi/2 - self.shot_deviation, self)]

    def shoot_right(self):
        corn = self.corners()
        p1 = (3 * corn[0] + corn[1]) / 4
        p2 = (corn[0] + corn[1]) / 2
        p3 = (3 * corn[1] + corn[0]) / 4
        return [Cannonball(p1, self.angle - math.pi/2 - self.shot_deviation, self),
                Cannonball(p2, self.angle - math.pi/2, self),
                Cannonball(p3, self.angle - math.pi/2 + self.shot_deviation, self)]


class DNABattleship(Battleship):
    def __init__(self, sea):
        super().__init__(sea)
        self.DNA = [[0]*4]*4
        for x in range(4):
            for y in range(4):
                gene = np.array([random.uniform(-1, 1)] * 2 + [random.random()] * 2)    # acc, angle, shootleft, right
                self.DNA[x][y] = gene
        self.pos = np.array([random.randint(0, sea[0]), random.randint(0, sea[1])])

    def calculate(self, boats):
        total_gene = np.array([0]*4)
        for boat in boats:
            if boat is self:
                continue
            if np.dot(boat.pos - self.pos, boat.pos - self.pos) > 10000:
                continue
            rel_pos = boat.pos - self.pos
            rotator = np.array(
                [[math.cos(self.angle), math.sin(self.angle)], [-math.sin(self.angle), math.cos(self.angle)]])
            rel_pos_rotated = np.dot(rel_pos, rotator)
            gene_index = ((rel_pos_rotated - np.array([100]*2)) // 50).tolist()
            gene = self.DNA[int(gene_index[0])][int(gene_index[1])]   # BUG in pycharm
            total_gene = total_gene + gene
        [up, left, right, a, d] = [False] * 5
        if 0.5 < total_gene[2] > total_gene[3]:
            a = True
        elif 0.5 < total_gene[3] > total_gene[2]:
            d = True
        if total_gene[0] > 0.7:
            up = True
        if total_gene[1] > 0.3:
            left = True
        elif total_gene[1] < -0.3:
            right = True
        super().calculate_FM([up, right, left])
        return super().shoot([a, d])


class PlayerBattleship(Battleship):
    def __init__(self, sea):
        super().__init__(sea)

    def calculate(self, keys):
        [up, right, left, a, d] = keys
        super().calculate_FM([up, right, left])
        return super().shoot([a, d])

class Cannonball:
    def __init__(self, pos, angle, boat):
        self.pos = pos
        self.angle = angle
        self.vel = 5
        self.distance_left = 60
        self.boat = boat

    def update(self):
        self.pos = self.pos + np.array([self.vel]*2) * np.array([math.cos(self.angle), -math.sin(self.angle)])
        self.distance_left -= self.vel

    def check_collision(self, b):
        if b is not self.boat:
            rel_pos = b.pos - self.pos
            rotator = np.array(
                [[math.cos(b.angle), math.sin(b.angle)], [-math.sin(b.angle), math.cos(b.angle)]])
            rel_pos_rotated = np.dot(rel_pos, rotator)
            if -b.size[0]/3 < rel_pos_rotated[0] < 2*b.size[0]/3 and -b.size[1]/2 < rel_pos_rotated[1] < b.size[1]/2:
                return True
        else:
            return False

