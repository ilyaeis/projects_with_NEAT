"""Plot best and mean fitness per generation from a fitness_history.csv.

The training scripts write fitness_history.csv (best,mean per generation).

Example (from the repo root):
    python tools/plot_fitness.py flappy_bird/fitness_history.csv docs/flappy_bird_fitness.png "Flappy Bird"
"""
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

SURFACE = "#fcfcfb"
TEXT = "#3d3d3a"
MUTED = "#8a897f"
BEST = "#2a78d6"
MEAN = "#eb6834"


def main(csv_path: str, out_path: str, title: str):
    with open(csv_path) as f:
        rows = [(float(best), float(mean)) for best, mean in csv.reader(f)]
    generations = range(len(rows))
    best = [r[0] for r in rows]
    mean = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=110)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    marker = "o" if len(rows) < 20 else None  # short runs: show each generation
    ax.plot(generations, best, color=BEST, linewidth=2, marker=marker, markersize=6, label="best genome")
    ax.plot(generations, mean, color=MEAN, linewidth=2, marker=marker, markersize=6, label="population mean")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_title(title, loc="left", color=TEXT, fontsize=12)
    ax.set_xlabel("generation", color=MUTED)
    ax.set_ylabel("fitness", color=MUTED)
    ax.grid(axis="y", color="#e4e3dd", linewidth=0.8)
    ax.axhline(0, color="#c9c8c0", linewidth=0.8)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c0")
    ax.tick_params(colors=MUTED, length=0)
    ax.legend(frameon=False, labelcolor=TEXT, loc="lower right", bbox_to_anchor=(1, 1.0), ncol=2)
    fig.tight_layout()
    fig.savefig(out_path, facecolor=SURFACE)
    print(out_path)


if __name__ == "__main__":
    main(*sys.argv[1:4])
