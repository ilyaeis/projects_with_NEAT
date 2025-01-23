import random 
import DATA
from Bird import Bird 

class Obstacle:
    def __init__(self, x: int):
        self.gap_height: int = DATA.OBSTACLE_GAP_HEIGHT
        self.width: int = DATA.OBSTACLE_WIDTH

        self.screen_width: int = DATA.SCREEN_WIDTH
        self.screen_height: int = DATA.SCREEN_HEIGHT
        self.padding: int = DATA.OBSTACLE_PADDING
        
        self.x = x
        self.gap_start: int = random.randint(self.padding, self.screen_height - self.padding - self.gap_height)
        self.gap_end: int = self.gap_start + self.gap_height
        
    def update(self):
        self.x -= 2
        
    @property
    def upper_block(self):
        return [
            self.x, 0,                   # start coord 
            self.width, self.gap_start   # distance from start coord
            ]
        
    @property
    def lower_block(self):
        distance_to_bottom = self.screen_height - self.gap_end
        return [
            self.x, self.gap_end,           # start coord 
            self.width, distance_to_bottom  # distance from start coord
            ]
        
    def check_bird_collision(self, bird: Bird) -> bool:
        if (bird.x < self.upper_block[0]):
            return False 

        if (bird.y < self.upper_block[3]) \
            or (bird.y > self.lower_block[1]):
            return True
        
        return False
    
    def passed_x(self, x: int) -> bool:
        return self.upper_block[0] + self.upper_block[2] < x