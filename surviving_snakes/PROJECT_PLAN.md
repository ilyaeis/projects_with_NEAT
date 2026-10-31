# Project Plan: Surviving Snakes

## 🎯 Goal
- Create an environment with AI-powered snakes using the NEAT algorithm, where snakes compete against each other for survival.

---

## 💡 Idea
- Create a field with multiple snakes and food. Train snake models to survive the longest by eating food and avoiding dangers. Add features like biting each other to increase complexity.

---

## 🛠️ Approach
- Steps:
  1. Prototype: Build a basic snake game with manual controls.
  2. Training: Implement NEAT to train the AI.
  3. Optimization: Improve the AI's performance and add features.
  4. Testing: Test the game with different scenarios and refine the code.
  5. Multiplying: Add more snakes and observe their behavior.

---

## 📅 Tasks
- [x] Create a simple snake game with manual controls.
- [x] Implement basic movement (up, down, left, right).
- [x] Add food generation and collision detection for food.
- [x] Add a NEAT model to control the snake.
- [x] Train the snake model using NEAT and save the best genome.
- [x] Improve the snake's decision-making, if possible, by tweaking the fitness function.
- [x] Test the trained snake in different scenarios (e.g., varying food locations, obstacles).
- [x] Add more snakes to the environment.
- [x] Implement interactions between snakes (e.g., biting, avoiding each other).
- [x] Train multiple snakes simultaneously and observe their behavior.

---

## What went wrong (first attempt, January 2025)
Despite effort and 100,000 generations of evolution, the snake AI was unable to learn to consistently eat the apple and survive. Below are the key challenges faced, potential reasons for the lack of progress, and suggestions for future improvements.

While the project did not achieve the desired outcome, it provided valuable insights into the challenges of training AI using evolutionary algorithms. Every obstacle is an opportunity to learn and grow, and I plan to return to this project when I have more knowledge and experience.

---

## How it was finished (October 2026)
The first attempt had bugs that hid the learning problem:
- A snake that had grown never had to eat again, so a board could run forever.
- Snakes were removed from the list while the loop went over it, so the next snake skipped its turn.
- `Apple(0, y)` placed the apple at random, because `if x and y` treats 0 as "no value".
- The inputs were raw board coordinates and distances (up to 50), and the "body distance" took the farthest body cell, not the nearest one. The snakes could not see each other.
- All 100 genomes shared one board and one apple, so a genome's score depended mostly on luck.
- The checkpoint name `neat-checkpoint-46748` was hard-coded.

What changed:
- **Board**: 30 x 20 cells, 4 snakes, 2 apples. A snake dies when it hits a wall, itself or another snake (head-on: both die), or when it does not eat for 150 moves. A board ends after 1000 moves.
- **Inputs (8)**, all relative to the snake's heading: is the cell ahead / left / right blocked (wall or any snake); where the nearest apple is (ahead/behind, left/right, clipped to [-1, 1]); can another snake's head step into the cell ahead / left / right next move.
- **Outputs (3)**: go straight, turn left, turn right. A snake cannot reverse into itself.
- **Fitness** (per move): +0.1 closer to the apple, -0.15 away, +0.01 alive, +10 per apple, -10 on death.
- **Self-play**: each genome plays on a board with 3 copies of itself, 2 boards per generation. Random rivals (4 different genomes per board) were tried too. Self-play was kept because it trains the same setting that the replay shows (copies of one network), and in the tests it gave fewer head-on crashes.
- **Two settings mattered most** (found by running each variant several times):
  1. A binary "next cell is blocked" input instead of a soft 1/distance ray. With the ray, most runs ignored all danger inputs and only chased food.
  2. Wider initial weights (`weight_init_stdev = 3`), bigger weight mutations (`weight_mutate_power = 1`) and a weight cap of +-8. Without the cap, the food weights grew to about 20, and no danger weight could catch up. With these settings, 7 of 7 runs learned to avoid obstacles, against about 4 of 11 runs without them.

### Results
150 generations, population 150, about 3.5 to 10 minutes on one CPU core. Test: 50 new boards with 4 copies of the saved winner (200 snakes), and 50 boards with 1 snake. The test seed differs from the seed used to pick the best of 4 runs.

| | 4 snakes per board | 1 snake alone |
|---|---|---|
| Apples per snake, mean (median) | 11.1 (7) | 26.0 (25) |
| Most apples by one snake | 49 | 48 |
| Moves alive, mean | 212 | 362 |

For comparison, a food-only policy (the typical result before the two changes) reaches 5 apples per snake (median 2) with 4 snakes, and 15 alone.

### What the snakes learned, and where they still fail
- They learned to head for the nearest apple, and to turn away when the next cell is blocked.
- Head-on crashes are rare (4% of deaths).
- They still die, mostly in traps: they cannot see further than one cell, so a long snake curls into its own body (46% of deaths) or into a dead end made by other snakes (33%). Some run into the wall when the food pull is stronger than the danger signal (16%).
- They do not plan, block rivals or share the board on purpose. Every snake plays the same reflex policy.

### Run
From `surviving_snakes/NeatSnake/`:
- `python TrainSnake.py`: train headless (150 generations). Saves `winner.pkl` and `fitness_history.csv`. Add `--resume` to continue from the last checkpoint.
- `python TrainingVisualisation.py`: watch 4 copies of the saved winner. Add `--train` to watch the training live (slow).
- The manual game: `cd ../SnakeGame && python Game.py` (arrow keys).

---

## 🛠️ Tools and Technologies
- List the tools, libraries, and technologies you’ll use:
  - Python
  - Pygame (for game visualization)
  - NEAT-Python (for AI training)
