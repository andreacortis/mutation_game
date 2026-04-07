"""Generate example images for the documentation."""
import sys
sys.path.insert(0, "..")
import matplotlib
matplotlib.use("Agg")

from mutation import MutationGame

# A3 positive roots
game = MutationGame.from_dynkin("A3")
fig = game.plot_root_orbits(positive_only=True)
fig.savefig("_static/a3_positive.png", bbox_inches="tight", dpi=150)

# A3 all roots
fig = game.plot_root_orbits(positive_only=False)
fig.savefig("_static/a3_all.png", bbox_inches="tight", dpi=150)

# D4 positive roots
game = MutationGame.from_dynkin("D4")
fig = game.plot_root_orbits(positive_only=True)
fig.savefig("_static/d4_positive.png", bbox_inches="tight", dpi=150)

# E6 positive roots
game = MutationGame.from_dynkin("E6")
fig = game.plot_root_orbits(positive_only=True)
fig.savefig("_static/e6_positive.png", bbox_inches="tight", dpi=150)

print("Images generated.")
