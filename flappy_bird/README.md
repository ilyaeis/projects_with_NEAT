# Flappy Bird AI with NEAT

An AI-powered Flappy Bird game where the bird learns to navigate through obstacles autonomously using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. This project demonstrates how genetic algorithms can train neural networks to solve dynamic challenges in a simple game environment.

---

## 🎯 Features
- NEAT Algorithm: Evolves neural networks to control the bird's jumps.
- Autonomous Gameplay: The AI learns to avoid obstacles and survive as long as possible.
- Collision Detection: Real-time collision checks between the bird and obstacles/screen boundaries.
- Configurable Parameters: Adjust fitness functions, network structures, and game physics via `config.txt` and `DATA.py`.
- Visualization: Watch the AI improve over generations with Pygame rendering.

---

## 🧠 How It Works

### NEAT Algorithm
- Inputs to Neural Network:
  - Bird's current `y` position
  - Distance to the top and bottom of the upcoming obstacle gap
  - Bird's vertical velocity
- Output: Decision to jump (if output ≥ `0.5`)

### Fitness Function
- Rewards:
  - `+10` for passing an obstacle
  - `+0.01` per frame survived
- Punishments:
  - `-5` for collisions with obstacles or screen boundaries
- Each genome flies 3 runs per generation and keeps its worst score, so one lucky run with easy gaps does not count.
- A run stops at 100 passed obstacles (`MAX_SCORE` in `DATA.py`), so a perfect bird cannot run forever.

### Run
- `python BestNeatBirdGame.py`: train headless for up to 50 generations, save `winner.pkl` and `fitness_history.csv`, then watch the winner.
- `python BestNeatBirdGame.py --replay`: only watch the saved `winner.pkl`.
- `python NeatGame.py`: watch the training live (slower).
- `python Game.py`: play yourself (press `J` to jump).

### Obstacle Mechanics
- Obstacles spawn continuously with randomized gaps
- Speed: Moves left at 2 pixels per frame

---

## 📁 Project Structure

| File Name             | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `BestNeatBirdGame.py` | Main entry point: headless training, then replay of the saved winner.      |
| `Bird.py`             | Defines the bird's behavior, including physics and NEAT-controlled logic.   |
| `config.txt`          | Configuration file for NEAT hyperparameters and network settings.           |
| `DATA.py`             | Centralized configuration for game physics, colors, and dimensions.         |
| `winner.pkl`          | The saved best genome.                                                      |
| `Game.py`             | Implements the manual Flappy Bird game with Pygame visualization.           |
| `NeatGame.py`         | Visualizes the NEAT training process with Pygame.                           |
| `NeatSimulation.py`   | Runs the NEAT training loop without visualization for faster evolution.     |
| `Obstacle.py`         | Handles obstacle generation, movement, and collision detection.             |

---

## 📦 Dependencies
- Python 3.9+
- `pygame` (for visualization)
- `neat-python` (for NEAT implementation)

---

## 📚 Learning Notes
Key takeaways from this project:
- NEAT simplifies neuroevolution by dynamically adjusting network complexity
- Fitness functions must balance short-term rewards and long-term survival. (I mean if bird keeps crashing, it's not my — it's the bird's fault. Right?)
