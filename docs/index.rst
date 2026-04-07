Mutation Game
=============

A Python library for exploring root systems through the combinatorial mutation
game on graphs and directed multigraphs. Given a Dynkin diagram name (``A3``,
``D5``, ``E8``, ``B4``, ``C3``, ``F4``, ``G2``, ...) or an arbitrary
adjacency matrix, the library computes the full root system via iterated
mutations and visualizes the mutation graph.

.. toctree::
   :maxdepth: 2

   background
   getting_started
   api

.. toctree::
   :maxdepth: 2
   :caption: Simply-Laced (Simple Graphs)

   type_a
   type_d
   type_e

.. toctree::
   :maxdepth: 2
   :caption: Non-Simply-Laced (Directed Multigraphs)

   type_b
   type_c
   type_fg
