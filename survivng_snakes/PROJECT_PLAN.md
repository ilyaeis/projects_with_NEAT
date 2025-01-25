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
- [ ] Add more snakes to the environment.
- [ ] Implement interactions between snakes (e.g., biting, avoiding each other).
- [ ] Train multiple snakes simultaneously and observe their behavior.

---

## What went wrong
Despite effort and 100,000 generations of evolution, the snake AI was unable to learn to consistently eat the apple and survive. Below are the key challenges faced, potential reasons for the lack of progress, and suggestions for future improvements.

While the project did not achieve the desired outcome, it provided valuable insights into the challenges of training AI using evolutionary algorithms. Every obstacle is an opportunity to learn and grow, and I plan to return to this project when I have more knowledge and experience.

---

## 🛠️ Tools and Technologies
- List the tools, libraries, and technologies you’ll use:
  - Python
  - Pygame (for game visualization)
  - NEAT-Python (for AI training)
