import random
import DATA
from Cell import Cell
class Apple:
    def __init__(self, x: int, y: int):
        if x and y:
            self.position: Cell = Cell(x=x, y=y)
        else:
            self.randomize_position()
        
    def randomize_position(self):
        x: int = random.randint(0, DATA.CELLS_IN_WIDTH - 1)
        y: int = random.randint(0, DATA.CELLS_IN_HEIGHT - 1)
        self.position = Cell(x=x, y=y)
        
    @property
    def x(self) -> int:
        return self.position.x
    @property
    def y(self) -> int:
        return self.position.y