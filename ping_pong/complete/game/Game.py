import pygame 
import game.DATA as DATA 
from game.Ball import Ball 
from game.Paddles import LeftPaddle, RightPaddle

class Window:
    def __init__(self):
        self.screen_width = DATA.SCREEN_WIDTH
        self.screen_height = DATA.SCREEN_HEIGHT
        self.ball: Ball = Ball()
        self.left_paddle: LeftPaddle = LeftPaddle()
        self.right_paddle: RightPaddle = RightPaddle()
        
        self.left_counter: int = 0
        self.right_counter: int = 0
        self.press_to_start: bool = True
        
        pygame.init()
        pygame.display.set_caption('Ping Pong')
        self.screen: pygame.Surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS = 60
        
    def draw_court(self):
        center_y: int = self.screen_height // 2
        center_x: int = self.screen_width // 2
        
        pygame.draw.line(self.screen, DATA.COURT_COLOR, (center_x, 0), (center_x, self.screen_height), 1)
        
        pygame.draw.circle(self.screen, DATA.COURT_COLOR, (0, center_y), DATA.TEXT_SIZE, 1)
        pygame.draw.circle(self.screen, DATA.COURT_COLOR, (self.screen_width, center_y), DATA.TEXT_SIZE, 1)
        
        font: pygame.font.Font = pygame.font.Font(None, DATA.TEXT_SIZE)
        text: pygame.Surface = font.render(f"{self.left_counter} {self.right_counter}", True, DATA.COURT_COLOR)
        text_rect: pygame.Rect = text.get_rect(center=(self.screen_width/2, self.screen_height/2))
        self.screen.blit(text, text_rect)
            
    def start_game(self) -> bool:
        self.screen.fill(DATA.BACKGROUND_COLOR)
        self.draw_court()
            
        pygame.draw.circle(self.screen, DATA.BALL_COLOR, (self.ball.x, self.ball.y), self.ball.radius)
        pygame.draw.rect(self.screen, DATA.PADDLE_COLOR, self.left_paddle.rect)
        pygame.draw.rect(self.screen, DATA.PADDLE_COLOR, self.right_paddle.rect)
            
        pygame.display.flip()
            
        if not self.press_to_start:
            return True
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    return False
                if event.type == pygame.KEYDOWN:
                    self.run()
                    return True
                
    def update_objects(self):
        if self.ball.dx > 0:
            self.ball.update(self.right_paddle)
        else:
            self.ball.update(self.left_paddle)
            
        self.left_paddle.update()
        self.right_paddle.update()
            
    def check_exit(self) -> bool:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_game()
        return False 
    
    def on_goal(self):
        if self.ball.x < 0:
            self.right_counter += 1
        else:
            self.left_counter += 1
        
        self.ball.reset()
        self.start_game()
                    
    def run(self):
        self.start_game()
        running: bool = True
        while running:
            if self.ball.is_out_of_screen():
                self.on_goal()

            if self.check_exit():
                running = False
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.left_paddle.move_up()
            if keys[pygame.K_s]: 
                self.left_paddle.move_down()
            if keys[pygame.K_UP]:
                self.right_paddle.move_up()
            if keys[pygame.K_DOWN]:
                self.right_paddle.move_down()
                
            self.update_objects()
            
            self.screen.fill(DATA.BACKGROUND_COLOR)
            self.draw_court()
            
            pygame.draw.circle(self.screen, DATA.BALL_COLOR, (self.ball.x, self.ball.y), self.ball.radius)
            
            pygame.draw.rect(self.screen, DATA.PADDLE_COLOR, self.left_paddle.rect)
            pygame.draw.rect(self.screen, DATA.PADDLE_COLOR, self.right_paddle.rect)
                
            pygame.display.flip()
            self.clock.tick(self.FPS)  
            
if __name__ == "__main__":
    w: Window = Window()
    w.start_game()
            
            
        
        
        
        
        
        