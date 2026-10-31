import pygame
import DATA
from Snake import Snake
from Apple import Apple

class Game:
    def __init__(self):
        self.snake: Snake = Snake(DATA.CELLS_IN_WIDTH // 2, DATA.CELLS_IN_HEIGHT // 2, (1, 0))
        self.apple: Apple = Apple(0, 0)
        self.apple.randomize_position()
        self.score: int = 0
        
        pygame.init()
        self.font: pygame.font.Font = pygame.font.Font(None, DATA.TEXT_SIZE)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.screen: pygame.Surface = pygame.display.set_mode((DATA.SCREEN_WIDTH, DATA.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                if event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                if event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")
                    
    def update(self):
        self.snake.move()
        if self.snake.check_collision():
            self.running = False
        if self.snake.check_eat(self.apple):
            self.snake.eat()
            self.apple.randomize_position()
            self.score += 1
            
    def render(self):
        self.screen.fill((0, 0, 0))
        
        text = self.font.render(f"{self.score}", True, DATA.TEXT_COLOR)
        text_rect = text.get_rect(center=(DATA.SCREEN_WIDTH // 2, DATA.SCREEN_HEIGHT // 2))
        text.set_alpha(10)
        
        self.screen.blit(text, text_rect)
        
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, DATA.SNAKE_COLOR, (segment[0] * DATA.CELL_SIZE, segment[1] * DATA.CELL_SIZE, DATA.CELL_SIZE, DATA.CELL_SIZE))
        pygame.draw.rect(self.screen, DATA.APPLE_COLOR, (self.apple.position[0] * DATA.CELL_SIZE, self.apple.position[1] * DATA.CELL_SIZE, DATA.CELL_SIZE, DATA.CELL_SIZE))
        
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.clock.tick(10)
            self.handle_events()
            self.update()
            self.render()
            
        pygame.quit()
        
if __name__ == "__main__":  
    game = Game()
    game.run()