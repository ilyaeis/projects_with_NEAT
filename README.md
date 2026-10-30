# projects_with_NEAT

Three small pygame games where neural networks learn to play. The networks evolve with NEAT (NeuroEvolution of Augmenting Topologies) through the `neat-python` library.

| Project | Status | Docs |
|---|---|---|
| Flappy Bird | Done. The bird learns to pass the obstacles. | [flappy_bird/README.md](flappy_bird/README.md) |
| Ping Pong | Done. The trained `winner.neat` network is included. | [ping_pong/README.md](ping_pong/README.md), [ping_pong/complete/README.md](ping_pong/complete/README.md) |
| Surviving Snakes | Experiment. It did not converge. | [surviving_snakes/PROJECT_PLAN.md](surviving_snakes/PROJECT_PLAN.md) |

## Setup

```
pip install -r requirements.txt
```

## Run

Run each command from inside the project folder, because the code reads `config.txt` from the current directory.

- Flappy Bird: `cd flappy_bird && python BestNeatBirdGame.py`
- Ping Pong: `cd ping_pong/complete && python main.py`. This trains for 50 generations, then plays with the new winner. To only watch the saved `winner.neat`, call `NeatGame.neat_best_play()` from that folder.
- Surviving Snakes: see the plan and the `NeatSnake/` and `SnakeGame/` folders.

## License

MIT. See [LICENSE](LICENSE).
