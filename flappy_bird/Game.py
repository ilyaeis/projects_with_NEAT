import pygame 
import DATA 
from Bird import Bird 
from Obstacle import Obstacle

class Window:
    def __init__(self):
        self.screen_width = DATA.SCREEN_WIDTH
        self.screen_height = DATA.SCREEN_HEIGHT
        self.obstacles: list[Obstacle] = []
        
        pygame.init()
        pygame.display.set_caption('Flappy Bird')
        self.screen: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        
    def create_objects(self):
        self.bird = Bird() 
        self.obstacles.append(Obstacle(self.screen_width))
        
    def start_game(self) -> bool:
        self.screen.fill(DATA.BACKGROUND_COLOR)
            
        pygame.draw.circle(self.screen, DATA.BIRD_COLOR, (self.bird.x, self.bird.y), self.bird.radius)
        self.bird.update()
        
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, DATA.OBSTACLE_COLOR, obstacle.upper_block)
            pygame.draw.rect(self.screen, DATA.OBSTACLE_COLOR, obstacle.lower_block)
            obstacle.update()
            
        pygame.display.flip()
            
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        return True
    def run(self):
        self.create_objects()
        if not self.start_game():
            return
        
        running: bool = True
        obstacle_ind: int = 0
        counter: int = 0
        
        while running:
            if not self.obstacles:
                raise IndexError 
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        self.bird.jump()
            
            if self.obstacles[0].passed_x(0):
                obstacle_ind = 0
                self.obstacles.pop(0)
            if self.obstacles[obstacle_ind].passed_x(self.bird.x) and obstacle_ind == 0:
                obstacle_ind = 1
                counter += 1
                
            if self.obstacles[obstacle_ind].check_bird_collision(self.bird) or self.bird.check_screen_collision():
                running = False 
                
            
            if self.obstacles[-1].passed_x(self.screen_width - DATA.GAP_BETWEEN_OBSTACLES):
                self.obstacles.append(Obstacle(self.screen_width))
            
            self.screen.fill(DATA.BACKGROUND_COLOR)
            
            font = pygame.font.Font(None, DATA.TEXT_FONT)
            text = font.render(f"{counter}", True, DATA.TEXT_COLOR)
            text_rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
            self.screen.blit(text, text_rect)

            pygame.draw.circle(self.screen, DATA.BIRD_COLOR, (self.bird.x, self.bird.y), self.bird.radius)
            self.bird.update()
            
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, DATA.OBSTACLE_COLOR, obstacle.upper_block)
                pygame.draw.rect(self.screen, DATA.OBSTACLE_COLOR, obstacle.lower_block)
                obstacle.update()
                
            pygame.display.flip()
            self.clock.tick(60)  
            
if __name__ == "__main__":
    w: Window = Window()
    w.run()
            
            
        
        
        
        
        
        