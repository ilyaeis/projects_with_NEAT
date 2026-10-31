import neat
import DATA
from Cell import Cell
from Apple import Apple

class NeatSnake:
    def __init__(self, x: int, y: int, direction: tuple, genome, config, color: tuple = DATA.SNAKE_COLORS[0]):
        self.direction: Cell = Cell(position=direction)
        # The body starts straight, behind the head.
        self.body: list[Cell] = [Cell(x=x - i * self.direction.x, y=y - i * self.direction.y)
                                 for i in range(DATA.START_LENGTH)]
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.color: tuple = color
        self.hunger: int = 0
        self.apples_eaten: int = 0

    def move(self):
        head: Cell = self.head
        new_head: Cell = head + self.direction
        self.body.insert(0, new_head)
        self.body.pop()
        self.hunger += 1

    def eat(self):
        tail: Cell = self.tail
        self.body.append(tail)
        self.hunger = 0
        self.apples_eaten += 1

    def check_collision(self, others: list["NeatSnake"]) -> bool:
        head: Cell = self.head
        if head in self.body[1:]:
            return True
        if head.x < 0 or head.x >= DATA.CELLS_IN_WIDTH or head.y < 0 or head.y >= DATA.CELLS_IN_HEIGHT:
            return True
        # Any cell of another snake kills, also its head (head-on: both die).
        for other in others:
            if other is not self and head in other.body:
                return True
        return False

    def check_eat(self, apple: Apple) -> bool:
        head: Cell = self.head
        return head == apple.position

    # Directions relative to the current heading (screen y points down).
    @property
    def left(self) -> Cell:
        return Cell(x=self.direction.y, y=-self.direction.x)
    @property
    def right(self) -> Cell:
        return Cell(x=-self.direction.y, y=self.direction.x)

    def danger(self, direction: Cell, blocked: set) -> float:
        # 1 if the next cell in this direction is a wall or a snake, else 0.
        # (A soft 1/distance ray was tried first: evolution mostly ignored it.)
        cell: Cell = self.head + direction
        if cell.x < 0 or cell.x >= DATA.CELLS_IN_WIDTH or cell.y < 0 or cell.y >= DATA.CELLS_IN_HEIGHT:
            return 1.0
        return 1.0 if cell in blocked else 0.0

    def head_danger(self, direction: Cell, other_heads: list[Cell]) -> float:
        # 1 if another snake's head can step into the same cell next move.
        cell: Cell = self.head + direction
        for head in other_heads:
            if abs(head.x - cell.x) + abs(head.y - cell.y) == 1:
                return 1.0
        return 0.0

    def nearest_apple(self, apples: list[Apple]) -> Apple:
        head: Cell = self.head
        return min(apples, key=lambda a: abs(a.x - head.x) + abs(a.y - head.y))

    def change_direction(self, apples: list[Apple], blocked: set, other_heads: list[Cell]):
        # All inputs are relative to the heading and scaled to about [-1, 1],
        # so one rule ("turn towards food") works in every direction.
        head: Cell = self.head
        apple: Apple = self.nearest_apple(apples)
        delta_x: int = apple.x - head.x
        delta_y: int = apple.y - head.y
        food_ahead: float = delta_x * self.direction.x + delta_y * self.direction.y
        food_right: float = delta_x * self.right.x + delta_y * self.right.y

        output = self.net.activate((
            self.danger(self.direction, blocked),
            self.danger(self.left, blocked),
            self.danger(self.right, blocked),
            max(-1.0, min(1.0, food_ahead / 5)),
            max(-1.0, min(1.0, food_right / 5)),
            self.head_danger(self.direction, other_heads),
            self.head_danger(self.left, other_heads),
            self.head_danger(self.right, other_heads),
        ))
        decision = output.index(max(output))
        # 0: keep going, 1: turn left, 2: turn right. A snake can never reverse.
        if decision == 1:
            self.direction = self.left
        elif decision == 2:
            self.direction = self.right

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
