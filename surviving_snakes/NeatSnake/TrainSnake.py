import os
import random
import neat
import pickle
import DATA
from Apple import Apple
from NeatSnake import NeatSnake

# Spawn points (one per snake), each in its own quarter of the board.
SPAWNS: list[tuple[int, int, tuple[int, int]]] = [
    (DATA.CELLS_IN_WIDTH // 4, DATA.CELLS_IN_HEIGHT // 4, (1, 0)),
    (3 * DATA.CELLS_IN_WIDTH // 4, DATA.CELLS_IN_HEIGHT // 4, (0, 1)),
    (3 * DATA.CELLS_IN_WIDTH // 4, 3 * DATA.CELLS_IN_HEIGHT // 4, (-1, 0)),
    (DATA.CELLS_IN_WIDTH // 4, 3 * DATA.CELLS_IN_HEIGHT // 4, (0, -1)),
]

class TrainSnake:
    def __init__(self):
        self.snakes: list[NeatSnake] = []
        self.apples: list[Apple] = []
        self.score: int = 0

    def run(self, genomes, config):
        # NEAT fitness function. Every genome plays GAMES_PER_GENERATION boards,
        # each time with other random rivals. Fitness is the mean over the boards.
        for _, genome in genomes:
            genome.fitness = 0
        genomes = list(genomes)
        for _ in range(DATA.GAMES_PER_GENERATION):
            if DATA.SELF_PLAY:
                # The board holds copies of one genome. A crash into a rival
                # always costs the genome itself, so it learns to avoid it.
                for _, genome in genomes:
                    self.play_board([genome] * DATA.SNAKES_PER_BOARD, config)
            else:
                random.shuffle(genomes)
                for i in range(0, len(genomes), DATA.SNAKES_PER_BOARD):
                    self.play_board([genome for _, genome in genomes[i:i + DATA.SNAKES_PER_BOARD]], config)
        snakes_per_genome: int = DATA.SNAKES_PER_BOARD if DATA.SELF_PLAY else 1
        for _, genome in genomes:
            genome.fitness /= DATA.GAMES_PER_GENERATION * snakes_per_genome

    def play_board(self, genomes: list, config):
        self.snakes = []
        for (x, y, direction), genome, color in zip(SPAWNS, genomes, DATA.SNAKE_COLORS):
            self.snakes.append(NeatSnake(x, y, direction, genome, config, color))
        self.apples = []
        for _ in range(DATA.APPLES_ON_BOARD):
            self.apples.append(Apple(None, None, self.occupied()))
        self.score = 0
        self.training()

    def occupied(self) -> set:
        return {cell for snake in self.snakes for cell in snake.body}

    def calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return abs(x2 - x1) + abs(y2 - y1)

    def render(self):
        pass

    def training(self):
        move: int = 1
        while len(self.snakes) > 0 and move <= DATA.MAX_MOVES:
            # All snakes decide on the same board state, then all move.
            blocked: set = self.occupied()
            heads: list = [snake.head for snake in self.snakes]
            for snake in self.snakes:
                snake.change_direction(self.apples, blocked, [head for head in heads if head is not snake.head])
            for snake in self.snakes:
                apple: Apple = snake.nearest_apple(self.apples)
                distance_before = self.calculate_distance(
                    snake.head.x, snake.head.y, apple.x, apple.y
                )
                snake.move()
                distance_after = self.calculate_distance(
                    snake.head.x, snake.head.y, apple.x, apple.y
                )
                # Reward for moving closer to the apple, penalty for moving away
                if distance_after < distance_before:
                    snake.reward(DATA.CLOSER_REWARD)
                else:
                    snake.punish(DATA.AWAY_PUNISHMENT)

            # Collisions are checked after every snake has moved.
            dead: list[NeatSnake] = [snake for snake in self.snakes
                                     if snake.check_collision(self.snakes)
                                     or snake.hunger > DATA.HUNGER_LIMIT]
            for snake in dead:
                snake.punish(DATA.DEATH_PUNISHMENT)
            self.snakes = [snake for snake in self.snakes if snake not in dead]

            for snake in self.snakes:
                # Small reward for staying alive
                snake.reward(DATA.ALIVE_REWARD)
                # Reward for eating an apple
                for apple in self.apples:
                    if snake.check_eat(apple):
                        snake.eat()
                        snake.reward(DATA.APPLE_REWARD)
                        apple.randomize_position(self.occupied())
                        self.score += 1

            move += 1
            self.render()

def load_config() -> neat.config.Config:
    return neat.config.Config(neat.DefaultGenome,
                              neat.DefaultReproduction,
                              neat.DefaultSpeciesSet,
                              neat.DefaultStagnation,
                              DATA.FILE_PATH)

def get_winner() -> neat.genome.DefaultGenome:
    with open("winner.pkl", "rb") as f:
        return pickle.load(f)

def get_last_possible_population() -> neat.Population:
    checkpoints = [file for file in os.listdir() if file.startswith("neat-checkpoint-")]
    if len(checkpoints) == 0:
        print("[DEBUG] No checkpoints found.")
        return None
    last_checkpoint = max(checkpoints, key=lambda x: int(x.split("-")[2]))
    print(f"[DEBUG] Loaded checkpoint {last_checkpoint}.")
    return neat.Checkpointer.restore_checkpoint(last_checkpoint)

def train(object, generations: int = DATA.GENERATIONS, resume: bool = False):
    population: neat.Population = get_last_possible_population() if resume else None
    if not population:
        population = neat.Population(load_config())
    population.add_reporter(neat.StdOutReporter(True))
    stats: neat.StatisticsReporter = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(25))

    trainer = object
    winner = population.run(trainer.run, generations)

    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
    stats.save_genome_fitness(delimiter=",", filename="fitness_history.csv")

if __name__ == "__main__":
    import sys
    trainer = TrainSnake()
    train(trainer, resume="--resume" in sys.argv)
