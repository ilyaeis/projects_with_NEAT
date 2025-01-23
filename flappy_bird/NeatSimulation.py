import DATA
from Bird import NeatBird
from Obstacle import Obstacle

class NeatSimulation:
    def __init__(self):
        self.screen_width = DATA.SCREEN_WIDTH
        self.screen_height = DATA.SCREEN_HEIGHT
        self.obstacles: list[Obstacle] = []
    
    def create_objects(self, genomes, config):
        self.birds: list[NeatBird] = []
        for _, genome in genomes:
            self.birds.append(NeatBird(genome, config))   
        self.obstacles = [Obstacle(self.screen_width)] 
        
    def run(self, genomes, config):
        self.create_objects(genomes, config)
        running: bool = True
        obstacle_ind: int = 0
        
        while running:
            if not self.obstacles:
                raise IndexError 
            if not self.birds:
                return
            
            if self.obstacles[0].passed_x(0):
                obstacle_ind = 0
                self.obstacles.pop(0)
            if self.obstacles[0].passed_x(self.birds[0].x) and obstacle_ind == 0:
                for bird in self.birds:
                    bird.reward(10)
                obstacle_ind = 1
                
            for bird in self.birds:
                if self.obstacles[obstacle_ind].check_bird_collision(bird) or bird.check_screen_collision():
                    bird.punish(5)
                    self.birds.remove(bird) 
            
            if self.obstacles[-1].passed_x(self.screen_width - DATA.GAP_BETWEEN_OBSTACLES):
                self.obstacles.append(Obstacle(self.screen_width))
            
            for bird in self.birds:
                bird.update(self.obstacles[obstacle_ind].gap_start, self.obstacles[obstacle_ind].gap_end)
                bird.reward(0.01)
                
            for obstacle in self.obstacles:
                obstacle.update()