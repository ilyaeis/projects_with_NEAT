import sys
import DATA 
from Ball import Ball 
from NeatPaddles import NeatLPaddle, NeatRPaddle

class Simulation:
    def __init__(self):
        self.screen_width = DATA.SCREEN_WIDTH
        self.screen_height = DATA.SCREEN_HEIGHT
        self.ball: Ball = Ball()
        
        self.left_counter: int = 0
        self.right_counter: int = 0
        self.left_ball_reflected_times = 0
        self.right_ball_reflected_times = 0
            
    def update_paddles(self, left_genome, right_genome, config):
        self.left_paddle: NeatLPaddle = NeatLPaddle(left_genome, config)
        self.right_paddle: NeatRPaddle = NeatRPaddle(right_genome, config)
    
    def update_objects(self):
        self.right_paddle.reward(0.001)
        self.left_paddle.reward(0.001)
        
        if self.ball.dx > 0:
            if self.ball.update(self.right_paddle):
                self.right_paddle.reward(1)
                self.right_ball_reflected_times += 1
        else:
            if self.ball.update(self.left_paddle):
                self.left_paddle.reward(1)
                self.left_ball_reflected_times += 1
            
        self.left_paddle.update(self.ball.x, self.ball.y)
        self.right_paddle.update(self.ball.x, self.ball.y)
        
    def on_goal(self):
        if self.ball.x < 0:
            self.left_paddle.punish(2)
            self.right_counter += 1
            
        else:
            self.right_paddle.punish(2)
            self.left_counter += 1
        
        self.ball.reset()
        
    def pie(self):
        self.left_paddle.reward(self.left_ball_reflected_times)
        self.right_paddle.reward(self.right_ball_reflected_times)
        
    def check_exit(self) -> bool:
        reflected_times_sum: int = self.left_ball_reflected_times + self.right_ball_reflected_times
        counter_sum: int = self.left_counter + self.right_counter
        if counter_sum >= 10 and \
         (reflected_times_sum <= reflected_times_sum // 2 or self.left_ball_reflected_times == 0 or self.right_ball_reflected_times == 0):
            self.pie()
            return True 
        if reflected_times_sum >= 50:
            self.pie()
            return True  
        if counter_sum >= 50:
            self.pie()
            return True 
        return False 
           
    def run(self):
        running: bool = True
        while running:
            if self.ball.is_out_of_screen():
                self.on_goal()

            if self.check_exit():
                running = False
                
            self.update_objects()
            
def train_neat(genomes, config):
    print("Model is learning:")
    for i, (_, genome1) in enumerate(genomes):
        percent: int = round(int(i / len(genomes) * 100))
        
        string: str = "█" * round(percent / 2) # 50 symbols max
        if string == "":
            string += "▢" 
        string += f" {percent}%"
        
        sys.stdout.write('\r' + string)
        
        genome1.fitness = 0
        for _, genome2 in genomes:
            genome2.fitness = 0
            sim: Simulation = Simulation()
            sim.update_paddles(genome1, genome2, config)
            sim.run()
            
    string: str = "█" * 50 + " 100%\n"
    sys.stdout.write('\r' + string)
    