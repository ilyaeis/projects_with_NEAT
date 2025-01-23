# NEAT Ping Pong AI

This is my second project using NEAT, where I trained an AI to play Ping Pong. The goal was to create an autonomous Ping Pong player using the NeuroEvolution of Augmenting Topologies (NEAT) algorithm. This project builds on my first experience with NEAT (Flappy Bird) and dives deeper into training strategies and optimization.

---

## 🎯 Features

- NEAT Algorithm: Evolves neural networks to control the right paddle.
- Autonomous Gameplay: The AI learns to reflect the ball and compete against a simple bot on the left side.
- Training Strategy: Initially, I tried training one model against all others, but it was too time-consuming. Instead, I trained all models simultaneously, similar to my Flappy Bird project.
- Visualization: Watch the AI improve over generations with Pygame rendering.

---

## 🧠 How It Works

### NEAT Algorithm
- Inputs to Neural Network:
  - Paddle's current `y` position.
  - Distance to the ball (`x` and `y` coordinates).
  - Ball's velocity (`dx` and `dy`).
- Output: Decision to move up or down.

### Fitness Function
- Rewards:
  - `+5` for successfully reflecting the ball.
  - `+0.0001` per frame survived.
- Punishments:
  - `-1` for missing the ball or hitting the screen boundaries.

### Training Strategy
- All right paddles are trained simultaneously, competing against a simple bot on the left side.
- The bot on the left always reflects the ball, providing a consistent challenge for the AI.

---
## 📁 Project Structure

| Folder/File               | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `game/`                 | Contains all files for game visualization (both for 2 players or 2 bots).   |
| `train/`                | Contains all files for NEAT training.                                       |
| `main.py`               | Main entry point for training and playing the best model.                   |
| `NeatGame.py`           | Visualizes the best-performing model playing Ping Pong.                     |
| `NeatTrain.py`        | Handles the NEAT training process and checkpoints.                          |
| `config.txt`            | NEAT hyperparameters (mutation rates, population size, activation functions).|
| `winner.neat`           | Saved file containing the best-performing genome after training.            |

---

## 📦 Dependencies
- Python 3.9+
- `pygame` (for visualization)
- `neat-python` (for NEAT implementation)

---

## 📚 Learning Notes

### Key takeaways from this project:

1. Planning the Training Method:
   - Choosing the right training method is crucial. Initially, I tried training two NEAT models against each other, but this approach was time-consuming and inefficient. Good models often faced weak opponents, leading to poor learning outcomes. In the end - switching to a single NEAT model competing against a consistent bot (on the left side) proved to be more effective. This ensured that the AI faced a consistent challenge, allowing it to learn and improve steadily.

2. Importance of Model Functions:
   - The design of the fitness function and reward/punishment system significantly impacts the training process. Balancing rewards for reflecting the ball and punishments for missing it was key to guiding the AI toward better performance.

3. Debugging in Large Projects:
   - Debugging in a large project can be challenging without a proper setup. Initially, I struggled to identify issues because I didn’t have a debugging framework in place.
   - Adding debugging statements (e.g., logging fitness scores, collision events, and exit conditions) early in the project made it much easier to track down issues and optimize the training process.

4. Efficiency in Training:
   - Training all models simultaneously (as opposed to one model at a time) was more efficient and scalable. This approach allowed the AI to learn faster and adapt to different scenarios.
   - Using checkpoints to save progress during training ensured that I could resume training from a specific point if needed, saving time and computational resources.

5. Visualization Matters:
   - Visualizing the training process helped me understand how the AI was learning and identify areas for improvement. Seeing the paddles in action made it easier to spot issues like poor collision detection and other error (like ball not moving, because of endless loop).

### Lessons Learned
- Plan your training method carefully: A well-thought-out approach saves time and leads to better results.
- Debugging is easier with a framework: Set up debugging tools early to avoid headaches later.