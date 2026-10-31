import os

FILE_PATH: str = os.path.dirname(os.path.realpath(__file__)) + "/config.txt"

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

CELL_SIZE = 20
CELLS_IN_WIDTH = SCREEN_WIDTH // CELL_SIZE
CELLS_IN_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# One board: several snakes share it and compete for a few apples.
SNAKES_PER_BOARD = 4
APPLES_ON_BOARD = 2
START_LENGTH = 3
HUNGER_LIMIT = 150       # moves without food before a snake starves
MAX_MOVES = 1000         # a board ends after this many moves
GAMES_PER_GENERATION = 2 # each genome plays this many boards
SELF_PLAY = True         # True: a board holds copies of one genome; False: random rivals

# Fitness
APPLE_REWARD = 10
CLOSER_REWARD = 0.1
AWAY_PUNISHMENT = 0.15
ALIVE_REWARD = 0.01
DEATH_PUNISHMENT = 10

GENERATIONS = 150
FPS = 15

SNAKE_COLORS = [(0, 220, 0), (0, 160, 255), (255, 200, 0), (220, 80, 255)]
APPLE_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
TEXT_SIZE = SCREEN_WIDTH // 2
