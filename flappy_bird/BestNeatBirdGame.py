import neat
from NeatGame import NeatWindow
from NeatSimulation import NeatSimulation
            
if __name__ == "__main__":
    config_path: str = "./config.txt"
    config: neat.config.Config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    population: neat.Population = neat.Checkpointer.restore_checkpoint("neat-checkpoint-5")
    population.add_reporter(neat.Checkpointer(1))
    
    sim: NeatSimulation = NeatSimulation()
    winner = population.run(sim.run, 50)  # 50 generations
    genomes = [(1, winner)]
    
    nw: NeatWindow = NeatWindow()
    nw.run(genomes, config)
    