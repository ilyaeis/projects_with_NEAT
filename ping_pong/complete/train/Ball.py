import random
import game.DATA as DATA
from train.Paddles import Paddle
from train.NeatPaddles import NeatRPaddle

class Ball:
    def __init__(self):
        self.screen_width: int = DATA.SCREEN_WIDTH
        self.screen_height: int = DATA.SCREEN_HEIGHT
        
        self.x: int = self.screen_width // 2
        self.y: int = self.screen_height // 2
        self.radius: int = DATA.BALL_RADIUS
        
        self.dx: int = random.choice([*range(-5, 0), *range(1, 6)])
        self.dy: int = random.choice([-1, 1])

        self.max_x_speed: int = self.screen_width // 10 # min(self.screen_height, self.screen_width) // 10
        self.max_y_speed: int = self.screen_height // 10 # min(self.screen_height, self.screen_width) // 10
        
    def update(self, paddles: Paddle) -> bool:
        steps: int = max(abs(self.dx), abs(self.dy))
        for _ in range(steps):
            self.x += self.dx / steps
            self.y += self.dy / steps
            
            ball_catched: bool = False
            self.check_screen_collision()
            for paddle in paddles:
                if paddle.check_ball_collision(self.x, self.y, self.radius):
                    if isinstance(paddle, NeatRPaddle):
                        print(f"[DEBUG] Ball caught by {paddle.id} ({paddle})")
                        paddle.ball_catched = True
                    ball_catched = True 
            if ball_catched:
                self.dx = max(-self.dx - 1, -self.max_x_speed) if self.dx > 0 else min(-self.dx + 1, self.max_x_speed)
                return ball_catched
        return False 
            
    def reset(self):
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        
        self.dx = random.randint(1, 5)
        self.dy = random.randint(1, 5)
        
    def check_screen_collision(self):
        if self.y <= 0:
            self.dy = min(-self.dy + 1, self.max_y_speed)
            self.y += self.dy
            
        elif self.y >= self.screen_height:
            self.dy = max(-self.dy - 1, -self.max_y_speed)
            self.y += self.dy
        
    def is_out_of_screen(self) -> bool:
        return self.x <= 0 or self.x >= self.screen_width
            