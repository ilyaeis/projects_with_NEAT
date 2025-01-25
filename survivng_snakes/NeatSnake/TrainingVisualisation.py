import pygame
import neat
import DATA
from Apple import Apple
from TrainSnake import TrainSnake, get_last_possible_population, get_winner, train

class Visualization(TrainSnake):
    def __init__(self):
        super().__init__()
        
        pygame.init()
        self.font: pygame.font.Font = pygame.font.Font(None, DATA.TEXT_SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode((DATA.SCREEN_WIDTH, DATA.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
    def render(self):
        print(1)
        self.screen.fill((0, 0, 0))
        
        text = self.font.render(f"{self.score}", True, DATA.TEXT_COLOR)
        text_rect = text.get_rect(center=(DATA.SCREEN_WIDTH // 2, DATA.SCREEN_HEIGHT // 2))
        text.set_alpha(10)
        
        self.screen.blit(text, text_rect)
        for snake in self.snakes:
            for segment in snake.body:
                pygame.draw.rect(self.screen, DATA.SNAKE_COLOR, (segment.x * DATA.CELL_SIZE, segment.y * DATA.CELL_SIZE, DATA.CELL_SIZE, DATA.CELL_SIZE))
        pygame.draw.rect(self.screen, DATA.APPLE_COLOR, (self.apple.x * DATA.CELL_SIZE, self.apple.y * DATA.CELL_SIZE, DATA.CELL_SIZE, DATA.CELL_SIZE))
        
        pygame.display.flip()
    
def show_the_best():
    winner = get_winner()
    config: neat.config.Config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, 
                                DATA.FILE_PATH)
    snake = Visualization()
    snake.run([(0, winner)], config)
                
if __name__ == "__main__":
    vis = Visualization()
    train(vis)
        