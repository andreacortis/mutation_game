# Mutation Game

[![PyPI](https://img.shields.io/pypi/v/mutation-game)](https://pypi.org/project/mutation-game/)
[![Documentation](https://readthedocs.org/projects/mutation-game/badge/?version=latest)](https://mutation-game.readthedocs.io/en/latest/)

A Python library for exploring root systems through the combinatorial mutation game on graphs.

Given a graph (or a Dynkin diagram name like `A3`, `D5`, `E8`), the library computes the full root system via iterated mutations and visualizes the mutation graph.

## Installation

```bash
pip install mutation-game
```

Or for development:

```bash
git clone git@github.com:andreacortis/mutation_game.git
cd mutation_game
uv sync
```

```python
from mutation_game import MutationGame

game = MutationGame.from_dynkin("A3")
roots = game.calculate_roots()
print(f"A3 has {len(roots)} roots")  # 12

fig = game.plot_root_orbits()
fig.savefig("a3_positive.png", bbox_inches="tight", dpi=150)
```

![A3 positive roots](docs/_static/a3_positive.png)

## Features

- **Dynkin diagram support** -- create games from `A_n`, `D_n`, `E_6`, `E_7`, `E_8` by name
- **Matrix-based mutations** -- each mutation is a precomputed matrix multiply (`v' = M_k @ v`)
- **Cartan matrix analysis** -- eigenvalues, eigenvectors, and automatic finite-type detection via positive definiteness
- **Root system computation** -- full BFS enumeration with verified root counts for all ADE types
- **Mutation path finding** -- shortest path between any two roots via BFS on the mutation graph
- **Path tables** -- all-pairs shortest mutation paths in a formatted table
- **Visualization** -- side-by-side Dynkin diagram and mutation graph with color-coded simple roots

## Finite-type detection

The library checks whether the Cartan matrix `C = 2I - A` is positive definite before attempting to enumerate roots. Infinite-type graphs are rejected early with a clear error:

```python
cycle = MutationGame([[0,1,1],[1,0,1],[1,1,0]])
cycle.is_finite_type()  # False
cycle.calculate_roots()  # RuntimeError: Cartan matrix is not positive definite
```

## Mutation path table

```python
game = MutationGame.from_dynkin("A3")
game.print_mutation_path_table()
```

```
Source     Target     Mutations         Len
-------------------------------------------
(0, 0, 1)  (0, 1, 0)  1 -> 2            2
(0, 0, 1)  (0, 1, 1)  1                 1
(0, 0, 1)  (1, 0, 0)  1 -> 2 -> 0 -> 1  4
(0, 0, 1)  (1, 1, 0)  1 -> 2 -> 0       3
(0, 0, 1)  (1, 1, 1)  1 -> 0            2
...
```

Each path is reversible: to go from B back to A, apply the same mutations in reverse order.

## Tests

```bash
uv run pytest test_mutation.py -v
```

43 tests covering Dynkin construction, mutation rule, root counts for all ADE types, Cartan matrix properties, mutation paths, and plotting.

## Documentation

Full documentation with mathematical background is available at
**[mutation-game.readthedocs.io](https://mutation-game.readthedocs.io/en/latest/)**

To build locally:

```bash
cd docs
uv run sphinx-build -b html . _build/html
```

## Dependencies

- `numpy` -- linear algebra and matrix operations
- `networkx` -- graph construction and layout
- `matplotlib` -- visualization

## License

See [LICENSE](LICENSE).
