import neat
from Paddles import LeftPaddle, RightPaddle

class NeatLPaddle(LeftPaddle):
    def __init__(self, genome, config):
        super().__init__()
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome
        
    def update(self, ball_x: int, ball_y: int):
        output = self.net.activate(
                (self.y, abs(self.width - ball_x), ball_y))
        decision = output.index(max(output))
        
        if decision == 0:
            self.move_up()
        else:
            self.move_down() 
            
        self.y += self.velocity
        
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
            self.punish(1)
        elif self.y >= self.screen_height - self.height:
            self.y = self.screen_height - self.height
            self.velocity = 0
            self.punish(1)
            
    def reward(self, num: float):
        self.genome.fitness += num 
    def punish(self, num: float):
        self.genome.fitness -= num 
        
class NeatRPaddle(RightPaddle):
    def __init__(self, genome, config, id: int):
        super().__init__()
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.genome = genome
        self.ball_catched: bool = False
        self.id: int = id
        
    def update(self, ball_x: int, ball_y: int):
        output = self.net.activate(
                (self.y, self.x - ball_x, ball_y))
        decision = output.index(max(output))
        
        if decision == 0:
            self.move_up()
        else:
            self.move_down()
            
        self.y += self.velocity
        
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
            self.punish(1)
        elif self.y >= self.screen_height - self.height:
            self.y = self.screen_height - self.height
            self.velocity = 0
            self.punish(1)
    
    def reward(self, num: float):
        self.genome.fitness += num 
    def punish(self, num: float):
        self.genome.fitness -= num 