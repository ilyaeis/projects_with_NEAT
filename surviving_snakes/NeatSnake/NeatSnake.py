import neat 
import DATA
from Cell import Cell
from Apple import Apple

class NeatSnake:
    def __init__(self, x: int, y: int, direction: tuple, genome, config):
        self.body: list[Cell] = [Cell(x=x, y=y)]
        self.direction: Cell = Cell(position=direction)
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome.fitness = 0
        
    def move(self):
        head: Cell = self.head
        new_head: Cell = head + self.direction
        self.body.insert(0, new_head)
        self.body.pop()
    
    def eat(self):
        tail: Cell = self.tail
        self.body.append(tail)
        
    def check_collision(self) -> bool:
        head: Cell = self.head
        if head in self.body[1:]:
            return True
        if head.x < 0 or head.x >= DATA.CELLS_IN_WIDTH or head.y < 0 or head.y >= DATA.CELLS_IN_HEIGHT:
            return True
        return False
    
    def check_eat(self, apple: Apple) -> bool:
        head: Cell = self.head
        return head == apple.position
    
    def change_direction(self, apple: Apple):
        head: Cell = self.head
        
        delta_x: int = apple.x - head.x
        delta_y: int = apple.y - head.y
        
        wall_dist_up: int = head.y
        wall_dist_down: int = DATA.CELLS_IN_HEIGHT - head.y
        wall_dist_left: int = head.x
        wall_dist_right: int = DATA.CELLS_IN_WIDTH - head.x
        
        body_dist_up: int = 0
        body_dist_down: int = 0
        body_dist_left: int = 0
        body_dist_right: int = 0
        for cell in self.body:
            if cell.x == head.x and cell.y < head.y:
                body_dist_up = max(body_dist_up, head.y - cell.y)
            if cell.x == head.x and cell.y > head.y:
                body_dist_down = max(body_dist_down, cell.y - head.y)
            if cell.y == head.y and cell.x < head.x:
                body_dist_left = max(body_dist_left, head.x - cell.x)
            if cell.y == head.y and cell.x > head.x:
                body_dist_right = max(body_dist_right, cell.x - head.x)
                
        output = self.net.activate((
            delta_x, delta_y,
            wall_dist_up, wall_dist_down, wall_dist_left, wall_dist_right,
            body_dist_up, body_dist_down, body_dist_left, body_dist_right
        ))
        decision = output.index(max(output))
        if decision == 0 and self.direction != (0, 1):
            self.direction = Cell(x=0, y=-1)
        if decision == 1 and self.direction != (0, -1):
            self.direction = Cell(x=0, y=1)
        if decision == 2 and self.direction != (1, 0):
            self.direction = Cell(x=-1, y=0)
        if decision == 3 and self.direction != (-1, 0):
            self.direction = Cell(x=1, y=0)
    
    def reward(self, reward: float):
        self.genome.fitness += reward
        
    def punish(self, punishment: float):
        self.genome.fitness -= punishment        
        
    @property
    def head(self) -> Cell:
        return self.body[0]
    @property
    def tail(self) -> Cell:
        return self.body[-1]
    