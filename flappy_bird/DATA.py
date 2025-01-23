SCREEN_WIDTH: int = 500 # px
SCREEN_HEIGHT: int = 500 # px 

START_VELOCITY: int = 0
GRAVITY: float = 0.5
JUMP_STRENGTH: float = -8.0

BIRD_RADIUS: int = 10 # px
BIRD_START_X: int = SCREEN_WIDTH // 10 # px 
BIRD_START_Y: int = SCREEN_HEIGHT // 2 # px

OBSTACLE_WIDTH: int = 40 # px
OBSTACLE_PADDING: int = SCREEN_HEIGHT // 10 # px
OBSTACLE_GAP_HEIGHT: int = 100 # px

GAP_BETWEEN_OBSTACLES: int = 100 # px

BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)
OBSTACLE_COLOR: tuple[int, int, int] = (100, 100, 100)
TEXT_COLOR: tuple[int, int, int] = (150, 150, 150)
BIRD_COLOR: tuple[int, int, int] = (200, 200, 200, 200)

TEXT_FONT: int = 250


