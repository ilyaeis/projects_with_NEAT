import DATA
from Apple import Apple

class Snake:
    def __init__(self, x: int, y: int, direction: tuple):
        self.body: list[tuple[int, int]] = [(x, y)]
        self.direction: tuple[int, int] = direction
        
    def move(self):
        head: tuple[int, int] = self.body[0]
        new_head: tuple[int, int] = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()
    
    def eat(self):
        tail: tuple[int, int] = self.body[-1]
        self.body.append(tail)
        
    def check_collision(self) -> bool:
        head: tuple[int, int] = self.body[0]
        if head in self.body[1:]:
            return True
        if head[0] < 0 or head[0] >= DATA.CELLS_IN_WIDTH or head[1] < 0 or head[1] >= DATA.CELLS_IN_HEIGHT:
            return True
        return False
    
    def check_eat(self, food: Apple) -> bool:
        head: tuple[int, int] = self.body[0]
        return head == food.position
    
    def change_direction(self, direction: str):
        if direction == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        if direction == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        if direction == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        if direction == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)
            
        