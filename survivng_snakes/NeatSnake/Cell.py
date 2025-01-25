class Cell:
    def __init__(self, x: int = None, y: int = None, position: tuple[int, int] = None):
        if position is not None:
            self.x, self.y = position
        elif x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            raise ValueError("Either provide (x, y) or a position tuple.")
        
    def __add__(self, other) -> tuple[int, int]:
        return Cell(x=self.x + other.x, y=self.y + other.y)
    
    def __eq__(self, other) -> bool:
        # Compare with another Cell object
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        # Compare with a tuple (x, y)
        elif isinstance(other, tuple) and len(other) == 2:
            return (self.x, self.y) == other
        else:
            return False
        