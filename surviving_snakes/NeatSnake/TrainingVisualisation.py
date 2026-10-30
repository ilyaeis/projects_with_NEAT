import sys
import pygame
import DATA
from TrainSnake import TrainSnake, get_winner, load_config, train

class Visualization(TrainSnake):
    def __init__(self):
        super().__init__()

        pygame.init()
        self.font: pygame.font.Font = pygame.font.Font(None, DATA.TEXT_SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode((DATA.SCREEN_WIDTH, DATA.SCREEN_HEIGHT))
        pygame.display.set_caption("Surviving Snakes")

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.screen.fill((0, 0, 0))

        text = self.font.render(f"{self.score}", True, DATA.TEXT_COLOR)
        text_rect = text.get_rect(center=(DATA.SCREEN_WIDTH // 2, DATA.SCREEN_HEIGHT // 2))
        text.set_alpha(10)

        self.screen.blit(text, text_rect)
        for snake in self.snakes:
            for segment in snake.body:
                pygame.draw.rect(self.screen, snake.color, (segment.x * DATA.CELL_SIZE, segment.y * DATA.CELL_SIZE, DATA.CELL_SIZE - 1, DATA.CELL_SIZE - 1))
        for apple in self.apples:
            pygame.draw.rect(self.screen, DATA.APPLE_COLOR, (apple.x * DATA.CELL_SIZE, apple.y * DATA.CELL_SIZE, DATA.CELL_SIZE - 1, DATA.CELL_SIZE - 1))

        pygame.display.flip()
        self.clock.tick(DATA.FPS)

def show_the_best():
    # Copies of the saved winner share one board. A new board starts when all
    # snakes are dead or after MAX_MOVES. Close the window to stop.
    winner = get_winner()
    config = load_config()
    snake = Visualization()
    while True:
        winner.fitness = 0
        snake.play_board([winner] * DATA.SNAKES_PER_BOARD, config)

if __name__ == "__main__":
    if "--train" in sys.argv:
        # Watch the training live (slow: every board is drawn).
        train(Visualization())
    else:
        show_the_best()
