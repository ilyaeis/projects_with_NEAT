import sys
import DATA 
from Ball import Ball 
from NeatPaddles import NeatRPaddle
from Paddles import LeftPaddle

class Simulation:
    def __init__(self):
        self.screen_width = DATA.SCREEN_WIDTH
        self.screen_height = DATA.SCREEN_HEIGHT
        self.left_paddle: LeftPaddle = LeftPaddle()
        self.right_paddles: list[NeatRPaddle] = []
        self.ball: Ball = Ball()
        
        self.left_counter: int = 0
        self.right_counter: int = 0
        self.right_ball_reflected_times = 0
            
    def update_paddles(self, genomes, config):
        for id, genome in genomes:
            genome.fitness = 0
            self.right_paddles.append(NeatRPaddle(genome, config, id))
        
    def update_objects(self):
        self.left_paddle.y = self.ball.y - self.left_paddle.width // 2
        ball_reflected: bool = False
        if self.ball.dx > 0:
            value: bool = self.ball.update(self.right_paddles)
            if value:
                self.right_ball_reflected_times += 1
                ball_reflected = True
        else:
            self.ball.update([self.left_paddle])
          
        if self.ball.is_out_of_screen() or ball_reflected:
            print(f"[DEBUG] {len(self.right_paddles) =}")
            for i in range(len(self.right_paddles) - 1, -1, -1):
                right_paddle = self.right_paddles[i]
                if right_paddle.ball_catched:
                    right_paddle.reward(5)
                    right_paddle.update(self.ball.x, self.ball.y)
                    right_paddle.ball_catched = False
                else:
                    right_paddle.punish(1)
                    self.right_paddles.pop(i)
            print(f"[DEBUG] {len(self.right_paddles) =}")
                    
        for right_paddle in self.right_paddles:
            right_paddle.update(self.ball.x, self.ball.y)
            right_paddle.reward(0.0001)
            
    def on_goal(self):
        if self.ball.x < 0:
            self.right_counter += 1
        else:
            self.left_counter += 1
        
        self.ball.reset()
        
    def check_exit(self) -> bool:
        counter_sum: int = self.left_counter + self.right_counter
        
        # Check first condition
        if counter_sum >= 10 and self.right_ball_reflected_times <= 0:
            print("[DEBUG] Exit condition 1 met: Too many goals without reflection.")
            return True 
        
        # Check second condition
        if self.right_ball_reflected_times >= 25:
            print("[DEBUG] Exit condition 2 met: Ball reflected 25 times.")
            return True  
        
        # Check third condition
        if len(self.right_paddles) == 0:
            print("[DEBUG] Exit condition 3 met: No paddles left.")
            return True
        
        # If no condition is met
        print("[DEBUG] No exit conditions met.")
        return False
           
    def run(self):
        running: bool = True
        while running:
            if self.ball.is_out_of_screen():
                self.on_goal()

            if self.check_exit():
                running = False
                
            self.update_objects()
            
def train_neat_sim(genomes, config):
    sim: Simulation = Simulation()
    sim.update_paddles(genomes, config)
    sim.run()