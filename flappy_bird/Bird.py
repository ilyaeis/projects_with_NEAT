import neat
import DATA 

class Bird:
    def __init__(self):
        self.x: int = DATA.BIRD_START_X
        self.y: int = DATA.BIRD_START_Y
        self.radius: int = DATA.BIRD_RADIUS

        self.screen_height: int = DATA.SCREEN_HEIGHT

        self.velocity: float = DATA.START_VELOCITY
        self.gravity: float = DATA.GRAVITY
        self.jump_strength: float = DATA.JUMP_STRENGTH

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_strength
        
    def check_screen_collision(self):
        return self.y < 0 or self.y > self.screen_height
    
class NeatBird(Bird):
    def __init__(self, genome, config):
        Bird.__init__(self)
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        self.genome = genome
        
    def update(self, gap_start: int, gap_end: int):
        output = self.net.activate((self.y, abs(self.y - gap_start), abs(self.y - gap_end), self.velocity))
        if output[0] >= 0.5:
            self.jump()
        self.velocity += self.gravity
        self.y += self.velocity
            
    def reward(self, reward: float):
        self.genome.fitness += reward
        
    def punish(self, punishment: float):
        self.genome.fitness -+ punishment