"""Generate example images for the documentation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import matplotlib
matplotlib.use("Agg")

from mutation_game import MutationGame

diagrams = [
    # Getting started examples
    ("A3", True, "a3_positive.png"),
    ("A3", False, "a3_all.png"),
    # Type A explorations
    ("A2", True, "a2_positive.png"),
    ("A4", True, "a4_positive.png"),
    ("A5", True, "a5_positive.png"),
    # Type D explorations
    ("D4", True, "d4_positive.png"),
    ("D5", True, "d5_positive.png"),
    ("D6", True, "d6_positive.png"),
    # Type E explorations
    ("E6", True, "e6_positive.png"),
    ("E7", True, "e7_positive.png"),
    ("E8", True, "e8_positive.png"),
    # Type B explorations
    ("B2", True, "b2_positive.png"),
    ("B3", True, "b3_positive.png"),
    ("B4", True, "b4_positive.png"),
    # Type C explorations
    ("C3", True, "c3_positive.png"),
    ("C4", True, "c4_positive.png"),
    # Type F and G explorations
    ("G2", True, "g2_positive.png"),
    ("F4", True, "f4_positive.png"),
]

for name, positive_only, filename in diagrams:
    print(f"  {filename}...", end=" ", flush=True)
    game = MutationGame.from_dynkin(name)
    fig = game.plot_root_orbits(positive_only=positive_only)
    fig.savefig(f"_static/{filename}", bbox_inches="tight", dpi=150)
    matplotlib.pyplot.close(fig)
    print("done")

print(f"\n{len(diagrams)} images generated.")
