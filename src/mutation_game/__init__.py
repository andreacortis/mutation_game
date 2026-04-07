"""Mutation Game -- root system explorer via the combinatorial mutation game on graphs."""

from mutation_game.mutation import MutationGame
from mutation_game.singularity import (
    milnor_number,
    corank,
    classify,
    splitting_lemma,
    jet_reduce,
    homotopy_equivalence,
)

__all__ = [
    "MutationGame",
    "milnor_number",
    "corank",
    "classify",
    "splitting_lemma",
    "jet_reduce",
    "homotopy_equivalence",
]
__version__ = "0.1.2"
