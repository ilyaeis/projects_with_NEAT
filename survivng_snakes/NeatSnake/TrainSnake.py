import os
import neat
import pickle
import DATA
from Apple import Apple
from NeatSnake import NeatSnake

class TrainSnake:
    def __init__(self):
        self.snakes: list[NeatSnake] = []
        self.score: int = 0

    def run(self, genomes, config):
        self.snakes = []
        self.apple: Apple = Apple(None, None)
        
        snake_start_x: int = DATA.CELLS_IN_WIDTH // 4
        snake_start_y: int = DATA.CELLS_IN_HEIGHT // 4
        snake_end_x: int = 3 * DATA.CELLS_IN_WIDTH // 4
        snake_end_y: int = 3 * DATA.CELLS_IN_HEIGHT // 4
        
        delta_x: int = snake_end_x - snake_start_x
        delta_y: int = snake_end_y - snake_start_y
        snake_count: int = len(genomes)
        
        spawn_snake_every_block: int = delta_x * delta_y // snake_count
        x: int = snake_start_x
        y: int = snake_start_y
        counter: int = spawn_snake_every_block
        
        for _, genome in genomes:
            while counter != spawn_snake_every_block:
                x += 1
                if x == snake_end_x:
                    x = snake_start_x
                    y += 1
                counter += 1
            counter = 0
            snake = NeatSnake(x, y, (1, 0), genome, config)
            self.snakes.append(snake)
        self.training()
        
    def calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return abs(x2 - x1) + abs(y2 - y1)
    
    def render(self):
        pass 
    
    def training(self):
        move: int = 1
        while len(self.snakes) > 0:
            this_move_apple: Apple = Apple(self.apple.x, self.apple.y)
            apple_ate: bool = False
            for snake in self.snakes:
                distance_before = self.calculate_distance(
                    snake.head.x, snake.head.y, self.apple.x, self.apple.y
                )
                snake.change_direction(self.apple)
                snake.move()
                
                distance_after = self.calculate_distance(
                    snake.head.x, snake.head.y, self.apple.x, self.apple.y
                )
                
                # Reward for moving closer to the apple
                if distance_after < distance_before:
                    snake.reward((distance_before - distance_after) * 0.1)
                # Penalty for moving away from the apple
                else:
                    snake.punish(0.1)

                # Reward for eating the apple
                if snake.check_eat(this_move_apple):
                    snake.eat()
                    snake.reward(len(snake.body) * 10)
                    apple_ate = True
                    
                # Penalty for collisions
                if snake.check_collision():
                    snake.punish(100)  # Fixed penalty
                    self.snakes.remove(snake)
                    continue

                # Small reward for staying alive
                snake.reward(0.01)

                # Reward for growing longer
                if move > 100 and len(snake.body) > 1:
                    snake.reward(len(snake.body))
                # Penalty for not growing after 100 moves
                elif move > 100 and len(snake.body) == 1:
                    snake.punish(10)
                    self.snakes.remove(snake)
            
            if apple_ate:
                self.apple.randomize_position()
                self.score += 1
                
            move += 1
            self.render()
    
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
    return neat.Checkpointer.restore_checkpoint("neat-checkpoint-46748")
    
def train(object):
    config: neat.config.Config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                DATA.FILE_PATH)
    population: neat.Population = get_last_possible_population() 
    if not population:
        population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(10_000))
    
    trainer = object
    winner = population.run(trainer.run, 100_000_000)
    
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        
if __name__ == "__main__":
    trainer = TrainSnake()
    train(trainer)
    