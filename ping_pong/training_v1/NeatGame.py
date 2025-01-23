import pygame
import pickle
import neat
from Game import Window
from NeatSimulation import Simulation, train_neat

class NeatGame(Window, Simulation):
    def __init__(self):
        Window.__init__(self)
        pygame.display.set_caption("Neat Ping-Pong")
        self.FPS = 60
        self.left_ball_reflected_times = 0
        self.right_ball_reflected_times = 0
        
    def update_paddles(self, left_genome, right_genome, config):
        Simulation.update_paddles(self, left_genome, right_genome, config)
        
    def update_objects(self):
        Simulation.update_objects(self)
        
    def on_goal(self):
        Simulation.on_goal(self)
        
    def check_exit(self) -> bool:
        Game.check_exit(self)
        
    def run(self):
        Window.run(self)

def neat_train():
    file_path: str = "config.txt"

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         file_path)
    
    population: neat.Population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(1))
    
    winner = population.run(train_neat, 50)
    with open("winner.neat", "wb") as f:
        pickle.dump(winner, f)
      

def get_winner_from_checkpoint(checkpoint_num: int):
    file_name: str = f"neat-checkpoint-{checkpoint_num}"
    population: neat.Population = neat.Checkpointer.restore_checkpoint(file_name)
    winner = population.run(train_neat, 1)
    with open("winner.neat", "wb") as f:
        pickle.dump(winner, f)
          
def neat_best_play():
    file_path: str = "config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         file_path)
    with open("winner.neat", "rb") as f:
        winner = pickle.load(f)
    ng: NeatGame = NeatGame()
    ng.update_paddles(winner, winner, config)
    ng.run()
    
if __name__ == "__main__":
    neat_best_play()
        