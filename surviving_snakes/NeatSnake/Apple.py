import random
import DATA
from Cell import Cell
class Apple:
    def __init__(self, x: int, y: int, occupied: set = None):
        if x is not None and y is not None:
            self.position: Cell = Cell(x=x, y=y)
        else:
            self.randomize_position(occupied)
        
    def randomize_position(self, occupied: set = None):
        # Never put the apple on a snake.
        while True:
            x: int = random.randint(0, DATA.CELLS_IN_WIDTH - 1)
            y: int = random.randint(0, DATA.CELLS_IN_HEIGHT - 1)
            self.position = Cell(x=x, y=y)
            if not occupied or self.position not in occupied:
                return
        
    @property
    def x(self) -> int:
        return self.position.x
    @property
    def y(self) -> int:
        return self.position.y
