import random
import math

class Battleship:
    def __init__(self, sea):
        self.health = 100
        self.xpos = random.randint(0, sea[0])
        self.ypos = random.randint(0,sea[1])
        self.angle = random.uniform(0, 2*math.pi)
        self.vel = 0
        self.perception = 400

class DNABattleship(Battleship):
    def __init__(self, sea):
        super().__init__(sea)
        self.DNA_grid_size = 10
        self.DNA = []
        """The DNA is a 3d array, where the first two dimensions correspond to the relative position of another ship, 
        and the last one is an array of this ships desired velocity in that case, as well as its desire to fire
        The blocks into which the other ships are categorized are 10x10 and the ships see ships 400 units away"""
        for x in range(2*self.perception//self.DNA_grid_size):
            col = []
            for y in range(2*self.perception//self.DNA_grid_size):
                gene = (random.uniform(-1, 1), random.uniform(-1, 1), random.randint(0, 1))
                col.append(gene)
            self.DNA.append(col)

    def move(self, ships):
        desired_state = [0, 0, 0]
        for ship in ships:
            if ship != self:
                x_diff = ship.xpos - self.xpos
                y_diff = ship.ypos - self.ypos
                if abs(x_diff) > self.perception or abs(y_diff) > self.perception:  # The ship is too far away to see
                    continue
                gene = self.DNA[(x_diff - self.perception)//10][(y_diff - self.perception)//10]
                for a in range(len(desired_state)):
                    desired_state[a] += gene[a]


class PlayerBattleship(Battleship):
    def __init__(self, sea):
        super().__init__(sea)