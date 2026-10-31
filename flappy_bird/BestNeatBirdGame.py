import sys
import pickle
import neat
from NeatGame import NeatWindow
from NeatSimulation import NeatSimulation


def load_config() -> neat.config.Config:
    config_path: str = "./config.txt"
    return neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )


RUNS_PER_GENERATION: int = 3


def evaluate(genomes, config):
    # One run can be lucky (easy gaps). Score each bird by its worst of several runs.
    sim: NeatSimulation = NeatSimulation()
    scores: dict = {genome_id: [] for genome_id, _ in genomes}
    for _ in range(RUNS_PER_GENERATION):
        sim.run(genomes, config)
        for genome_id, genome in genomes:
            scores[genome_id].append(genome.fitness)
    for genome_id, genome in genomes:
        genome.fitness = min(scores[genome_id])


def train(generations: int = 50):
    # Headless training: fast, no window. Saves winner.pkl and the fitness history.
    population: neat.Population = neat.Population(load_config())
    population.add_reporter(neat.StdOutReporter(True))
    stats: neat.StatisticsReporter = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(10))

    winner = population.run(evaluate, generations)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
    stats.save_genome_fitness(delimiter=",", filename="fitness_history.csv")


def replay():
    # Watch the saved winner fly. Close the window to stop.
    with open("winner.pkl", "rb") as f:
        winner = pickle.load(f)
    nw: NeatWindow = NeatWindow()
    nw.run([(1, winner)], load_config())


if __name__ == "__main__":
    if "--replay" not in sys.argv:
        train()
    replay()
