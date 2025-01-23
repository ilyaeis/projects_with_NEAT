import DATA

class Paddle:
    def __init__(self):
        self.screen_width: int = DATA.SCREEN_WIDTH
        self.screen_height: int = DATA.SCREEN_HEIGHT
        
        self.width = DATA.PADDLE_WIDTH
        self.height = DATA.PADDLE_HEIGHT
        
        self.y: int = (self.screen_height - self.height) // 2
        self.velocity: int = 0
        
    def update(self):
        self.y += self.velocity
        
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
        elif self.y >= self.screen_height - self.height:
            self.y = self.screen_height - self.height
            self.velocity = 0
        
    def move_up(self):
        self.velocity -= 1
    def move_down(self):
        self.velocity += 1
         
class LeftPaddle(Paddle):
    def __init__(self):
        Paddle.__init__(self)
        self.x: int = 0
        
    def check_ball_collision(self, bx: int, by: int, bradius: int) -> bool:
        if self.x <= bx - bradius <= self.x + self.width:  
            if self.y <= by <= self.y + self.height:  
                return True
        return False

            
    @property
    def rect(self):
        return [0, self.y, self.width, self.height]
    
class RightPaddle(Paddle):
    def __init__(self):
        Paddle.__init__(self)
        self.x: int = self.screen_width - self.width
        
    def check_ball_collision(self, bx: int, by: int, bradius: int) -> bool:
        if self.x <= bx + bradius <= self.x + self.width:  # Check horizontal collision
            if self.y <= by <= self.y + self.height:  # Check vertical collision
                return True
        return False

            
    @property
    def rect(self):
        return [self.x, self.y, self.width, self.height]