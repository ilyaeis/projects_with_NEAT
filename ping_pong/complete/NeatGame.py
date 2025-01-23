import pygame
import pickle
import neat
from game.Game import Window
from game.Paddles import LeftPaddle, RightPaddle
from game.NeatPaddles import NeatLPaddle, NeatRPaddle

class NeatGame(Window):
    def __init__(self):
        Window.__init__(self)
        pygame.display.set_caption("Neat Ping-Pong")
        self.press_to_start: bool = False
        self.FPS = 60
        self.left_ball_reflected_times = 0
        self.right_ball_reflected_times = 0
        
    def update_paddles(self, left_genome, right_genome, config):
        if left_genome is None:
            self.left_paddle: LeftPaddle = LeftPaddle()
        else:
            self.left_paddle: NeatLPaddle = NeatLPaddle(left_genome, config)
        if right_genome is None:
            self.right_paddle: RightPaddle = RightPaddle()
        else:
            self.right_paddle: NeatRPaddle = NeatRPaddle(right_genome, config)
        
    def update_objects(self):
        if self.ball.dx > 0:
            self.ball.update(self.right_paddle)
        else:
            self.ball.update(self.left_paddle)
            
        if isinstance(self.left_paddle, NeatLPaddle):
            self.left_paddle.update(self.ball.x, self.ball.y, self.ball.dx, self.ball.dy)
        else:
            self.left_paddle.update()
        if isinstance(self.right_paddle, NeatRPaddle):
            self.right_paddle.update(self.ball.x, self.ball.y, self.ball.dx, self.ball.dy)
        else:
            self.right_paddle.update()
        
    def on_goal(self):
        Window.on_goal(self)
        
    def check_exit(self) -> bool:
        Window.check_exit(self)
        
    def run(self):
        Window.run(self)

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
        