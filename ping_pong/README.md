# NEAT Ping Pong AI

This is my second project using NEAT, where I trained an AI to play Ping Pong. The goal was to create an autonomous Ping Pong player using the NeuroEvolution of Augmenting Topologies (NEAT) algorithm. This project builds on my first experience with NEAT (Flappy Bird) and dives deeper into training strategies and optimization.

---

## 📁 Project Structure

| Folder               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `complete/`          | Contains the complete project with both training and gameplay. Combines the best aspects of `training_v1` and `training_v2` to support both AI training and player gameplay. |
| `training_v1/`       | Contains the first version of the project, where each model is trained against other models. This approach was inefficient, as good models often faced weak opponents, leading to poor learning outcomes. |
| `training_v2/`       | Uses the "all models against an undefeatable boss" approach. This version focuses on training all models simultaneously against a consistent challenge but does not support player gameplay. The `complete/` folder was created to combine the strengths of both versions. |

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