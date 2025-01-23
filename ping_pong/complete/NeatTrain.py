import pygame
import pickle
import neat
import game.DATA as DATA
from train.Game import Window
from train.NeatSimulation import Simulation, train_neat_sim

class NeatGame(Window, Simulation):
    def __init__(self):
        Window.__init__(self)
        pygame.display.set_caption("Neat Ping-Pong")
        self.FPS = 300
        Simulation.__init__(self)
        
    def update_paddles(self, genomes, config):
        Simulation.update_paddles(self, genomes, config)
        
    def update_objects(self):
        Simulation.update_objects(self)
        
    def on_goal(self):
        Simulation.on_goal(self)
        
    def check_exit(self) -> bool:
        counter_sum: int = self.left_counter + self.right_counter
        if counter_sum >= 10 and self.right_ball_reflected_times <= 0:
            print("[DEBUG] Exit condition 1 met: Too many goals without reflection.")
            return True 
        if self.right_ball_reflected_times >= 25:
            print("[DEBUG] Exit condition 2 met: Ball reflected 25 times.")
            return True  
        if len(self.right_paddles) == 0:
            print("[DEBUG] Exit condition 3 met: No paddles left.")
            return True
        return False
        
    def run(self):
        while True:
            if self.ball.is_out_of_screen():
                self.on_goal()
            exit: bool = self.check_exit()
            if exit:
                return
            self.update_objects()
            self.screen.fill(DATA.BACKGROUND_COLOR)
            self.draw_court()

            pygame.draw.circle(self.screen, DATA.BALL_COLOR, (self.ball.x, self.ball.y), self.ball.radius)
            
            pygame.draw.rect(self.screen, DATA.PADDLE_COLOR, self.left_paddle.rect)
            for right_paddle in self.right_paddles:
                pygame.draw.rect(self.screen, DATA.PADDLE_COLOR, right_paddle.rect)
                
            pygame.display.flip()
            self.clock.tick(self.FPS)  

def train_neat_game(genomes, config):
    print("Model is learning")
    sim: NeatGame = NeatGame()
    sim.update_paddles(genomes, config)
    sim.run()
    print("Done")
    
def neat_train(func: callable, epochs = 50, checkpoint_num: int = 0):
    file_path: str = "config.txt"

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         file_path)
    if not checkpoint_num:
        population: neat.Population = neat.Population(config)
    else:
        population = get_population_from_checkpoint(checkpoint_num)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(1))
    
    winner = population.run(func, epochs)
    with open("winner.neat", "wb") as f:
        pickle.dump(winner, f)

def get_population_from_checkpoint(checkpoint_num: int):
    file_name: str = f"neat-checkpoint-{checkpoint_num}"
    population: neat.Population = neat.Checkpointer.restore_checkpoint(file_name)
    return population

if __name__ == "__main__":
    # neat_train(train_neat_game) # to see the process of learning
    neat_train(train_neat_sim, 50)
        