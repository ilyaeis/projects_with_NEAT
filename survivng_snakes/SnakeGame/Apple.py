import random
import DATA

class Apple:
    def __init__(self, x: int, y: int):
        self.position: tuple[int, int] = (x, y)
        
    def randomize_position(self):
        self.position = (random.randint(0, DATA.CELLS_IN_WIDTH - 1), random.randint(0, DATA.CELLS_IN_HEIGHT - 1))