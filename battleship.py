import random
import math


class Battleship:
    def __init__(self, sea):
        self.health = 100
        self.xpos = random.randint(0, sea[0])
        self.ypos = random.randint(0, sea[1])
        self.angle = random.uniform(0, 2*math.pi)
        self.vel = 0
        self.perception = 400
        self.max_vel = 2
        self.max_acc = 1
        self.max_angular_vel = 0.5
        self.reload_time = 5
        self.reload_status = 0      # 0 means ready to shoot
        self.width = 2
        self.length = 5

    def corners(self):
        x = self.xpos
        y = self.ypos
        a = self.angle
        """             length
                        [3] ----------------------- [2]                       <-
                   width  |                           |      --> Forward       |  angle
                       xpos, ypos [0] --------------- [1]                      |
                   """
        return [(x, y),
                (x + self.length * math.cos(a), y + self.length * math.sin(a)),
                (x + self.length * math.cos(a) - self.width * math.sin(a),
                 y + self.length * math.sin(a) + self.width * math.cos(a)),
                (x - self.width * math.sin(a), y + self.width * math.cos(a))]


class DNABattleship(Battleship):
    def __init__(self, sea):
        super().__init__(sea)
        self.DNA_grid_size = 10
        self.DNA = []
        """The DNA is a 3d array, where the first two dimensions correspond to the relative position of another ship, 
        and the last one is an array of this ships desired velocity in that case, as well as its desire to fire in both 
        directions.
        The blocks into which the other ships are categorized are 10x10 and the ships see ships 400 units away"""
        for x in range(2*self.perception//self.DNA_grid_size):
            col = []
            for y in range(2*self.perception//self.DNA_grid_size): # TODO: fix so that the vector fields are rotated
                gene = (random.uniform(-1, 1), random.uniform(-1, 1), random.randint(0, 1), random.randint(0, 1))
                col.append(gene)
            self.DNA.append(col)

    def update(self, ships):
        # Calculate desires
        desired_state = [0, 0, 0, 0]   # xvel, yvel, fire left, fire right
        for ship in ships:
            if ship.xpos != self.xpos or ship.ypos != self.ypos:
                x_diff = ship.xpos - self.xpos
                y_diff = ship.ypos - self.ypos
                if abs(x_diff) > self.perception or abs(y_diff) > self.perception:  # The ship is too far away to see
                    continue
                gene = self.DNA[int((x_diff - self.perception)//10)][int((y_diff - self.perception)//10)]

                for j in [0, 1]:
                    desired_state[j] += gene[j] / (len(ships) - 1)  # Genes relating to movement
                
                for j in [2, 3]:
                    desired_state[j] += gene[j]     # Genes related to shooting
        #   Ship movement
        desired_angle = math.atan2(desired_state[1], desired_state[0])
        if abs((self.angle - desired_angle) % 2*math.pi) < self.max_angular_vel * self.vel:
            self.angle = desired_angle
        if self.angle - desired_angle < 0:
            right_error = self.angle - desired_angle + 2*math.pi
            left_error = desired_angle - self.angle
        else:
            right_error = self.angle - desired_angle
            left_error = desired_angle - self.angle + 2*math.pi

        if right_error < left_error:    # The ship wants to turn right
            self.angle -= self.max_angular_vel * self.vel
        else:       # The ship wants to turn left
            self.angle += self.max_angular_vel * self.vel

        self.angle %= 2*math.pi
        self.xpos += math.sin(self.angle) * self.vel
        self.ypos += math.cos(self.angle) * self.vel
        #   Fire cannons
        corners = self.corners()
        if desired_state[2] >= 1 and self.reload_status == 0:
            self.reload_status = self.reload_time
            p1 = corners[3]
            p2 = corners[2]
            return [Cannonball((p1[0] + 3 * p2[0]) / 4, (p1[1] + 3 * p2[1]) / 4, self.angle + math.pi / 2),
                    Cannonball((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, self.angle + math.pi / 2),
                    Cannonball((3 * p1[0] + p2[0]) / 4, (3 * p1[1] + p2[1]) / 4, self.angle + math.pi / 2)]
        if desired_state[3] >= 1 and self.reload_status == 0:
            self.reload_status = self.reload_time
            p1 = corners[0]
            p2 = corners[1]
            return [Cannonball((p1[0] + 3 * p2[0]) / 4, (p1[1] + 3 * p2[1]) / 4, self.angle - math.pi / 2),
                    Cannonball((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, self.angle - math.pi / 2),
                    Cannonball((3 * p1[0] + p2[0]) / 4, (3 * p1[1] + p2[1]) / 4, self.angle - math.pi / 2)]
        self.reload_status -= 1
        if self.reload_status < 0:
            self.reload_status = 0


class PlayerBattleship(Battleship):
    def __init__(self, sea):
        super().__init__(sea)

    def update(self, left, right, up, a, d):
        #   Ship movement
        if right:
            self.angle -= self.max_angular_vel * self.vel
        if left:
            self.angle += self.max_angular_vel * self.vel

        if up:
            self.vel += self.max_acc
            if self.vel > self.max_vel:
                self.vel = self.max_vel

        self.xpos += math.cos(self.angle) * self.vel
        self.ypos += math.sin(self.angle) * self.vel

        #   Fire cannonballs
        corners = self.corners()
        if a and self.reload_status == 0:
            self.reload_status = self.reload_time
            p1 = corners[3]
            p2 = corners[2]
            return [Cannonball((p1[0] + 3 * p2[0])/4,   (p1[1] + 3 * p2[1])/4,    self.angle + math.pi/2),
                    Cannonball((p1[0] + p2[0])/2,       (p1[1] + p2[1])/2,        self.angle + math.pi/2),
                    Cannonball((3*p1[0] + p2[0])/4,     (3*p1[1] + p2[1])/4,      self.angle + math.pi/2)]
        if d and self.reload_status == 0:
            self.reload_status = self.reload_time
            p1 = corners[0]
            p2 = corners[1]
            return [Cannonball((p1[0] + 3 * p2[0]) / 4, (p1[1] + 3 * p2[1]) / 4, self.angle - math.pi / 2),
                    Cannonball((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, self.angle - math.pi / 2),
                    Cannonball((3 * p1[0] + p2[0]) / 4, (3 * p1[1] + p2[1]) / 4, self.angle - math.pi / 2)]
        self.reload_status -= 1
        if self.reload_status < 0:
            self.reload_status = 0



class Cannonball:
    def __init__(self, xpos, ypos, angle):
        self.xpos = xpos
        self.ypos = ypos
        self.vel = 4
        self.angle = angle
        self.distance_left = 40

    def update(self):
        self.xpos += math.sin(self.angle) * self.vel
        self.ypos += math.cos(self.angle) * self.vel
        self.distance_left -= self.vel