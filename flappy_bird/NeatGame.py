import neat
import pygame
import DATA
from Game import Window
from Bird import NeatBird
from Obstacle import Obstacle

class NeatWindow(Window):
    def __init__(self):
        Window.__init__(self)
        pygame.display.set_caption('Neat Flappy Bird')

    def create_objects(self, genomes, config):
        self.birds: list[NeatBird] = []
        for _, genome in genomes:
            self.birds.append(NeatBird(genome, config))   
        self.obstacles = [Obstacle(self.screen_width)]         
        
    def run(self, genomes, config):
        self.create_objects(genomes, config)
        running: bool = True
        obstacle_ind: int = 0
        counter: int = 0
        
        while running:
            if not self.obstacles:
                raise IndexError 
            if not self.birds:
                return
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False
            
            if self.obstacles[0].passed_x(0):
                obstacle_ind = 0
                self.obstacles.pop(0)
            if self.obstacles[0].passed_x(self.birds[0].x) and obstacle_ind == 0:
                counter += 1
                for bird in self.birds:
                    bird.reward(5)
                obstacle_ind = 1
                
            for bird in self.birds:
                if self.obstacles[obstacle_ind].check_bird_collision(bird) or bird.check_screen_collision():
                    bird.punish(5)
                    self.birds.remove(bird) 
            
            if self.obstacles[-1].passed_x(self.screen_width - DATA.GAP_BETWEEN_OBSTACLES):
                self.obstacles.append(Obstacle(self.screen_width))
            
            self.screen.fill(DATA.BACKGROUND_COLOR)
            
            font = pygame.font.Font(None, DATA.TEXT_FONT)
            text = font.render(f"{counter}", True, DATA.TEXT_COLOR)
            text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
            self.screen.blit(text, text_rect)
            
            for bird in self.birds:
                pygame.draw.circle(self.screen, DATA.BIRD_COLOR, (bird.x, bird.y), bird.radius)
                bird.update(self.obstacles[obstacle_ind].gap_start, self.obstacles[obstacle_ind].gap_end)
                bird.reward(0.01)
                
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, DATA.OBSTACLE_COLOR, obstacle.upper_block)
                pygame.draw.rect(self.screen, DATA.OBSTACLE_COLOR, obstacle.lower_block)
                obstacle.update()
                
            pygame.display.flip()
            
if __name__ == "__main__":
    config_path: str = "./config.txt"
    config: neat.config.Config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    #population: neat.Population = neat.Population(config)
    population: neat.Population = neat.Checkpointer.restore_checkpoint("neat-checkpoint-5")
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(1))

    w: NeatWindow = NeatWindow()
    winner = population.run(w.run, 50)  # 50 generations
    print(winner)