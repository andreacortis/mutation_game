Mathematical Background
=======================

The mutation game is a combinatorial process on graphs that naturally produces
the root systems of Lie algebras. It was introduced by N. J. Wildberger
[Wild2003]_ and later published in a generalized form in [Wild2020]_.
This section describes the mathematical setting.

The mutation game
-----------------

The game is set on a network of cities on Mars, as described by Wildberger
[Wild2003]_. Consider a simple undirected graph *G* with *n* nodes, described
by its adjacency matrix *A* (where :math:`A_{ij} = 1` if nodes *i* and *j* are
connected, and 0 otherwise).

A **state** of the game is an integer vector :math:`v \in \mathbb{Z}^n`, where
each component :math:`v_i` represents the population at node *i*. Populations
can be positive ("Martians") or negative ("Anti-Martians") -- Wildberger's
original terminology.

A **mutation at node** *k* transforms the state according to the rule:

.. math::

   v_k' = -v_k + \sum_{j \sim k} v_j

where the sum runs over all neighbors *j* of *k*. All other components remain
unchanged: :math:`v_i' = v_i` for :math:`i \neq k`.

Equivalently, the mutation at node *k* is the linear map :math:`v \mapsto M_k v`
where :math:`M_k` is the identity matrix with row *k* replaced:

.. math::

   (M_k)_{ij} = \begin{cases}
     -1             & \text{if } i = k \text{ and } j = k \\
     A_{kj}         & \text{if } i = k \text{ and } j \neq k \\
     \delta_{ij}    & \text{if } i \neq k
   \end{cases}

Each mutation is an **involution**: :math:`M_k^2 = I`. Applying the same
mutation twice returns the state to its original value.

Root systems
------------

The **simple roots** are the standard basis vectors :math:`e_1, \ldots, e_n`.
Starting from these seeds, the **root system** :math:`\Phi` is the set of all
distinct vectors reachable by applying any sequence of mutations:

.. math::

   \Phi = \{ M_{k_m} \cdots M_{k_2} M_{k_1} \, e_i
           \mid i \in \{1, \ldots, n\},\;
           k_1, \ldots, k_m \in \{1, \ldots, n\},\;
           m \geq 0 \}

The root system decomposes into **positive roots** (all components
:math:`\geq 0`) and **negative roots** (all components :math:`\leq 0`). Every
root is either positive or negative, and :math:`v \in \Phi` implies
:math:`-v \in \Phi`.

Roots vs. bases
^^^^^^^^^^^^^^^

The simple roots :math:`e_1, \ldots, e_n` form a **basis** of
:math:`\mathbb{R}^n` -- they are linearly independent and span the space. The
root system, however, is much larger than a basis. For example, the A3 root
system lives in :math:`\mathbb{R}^3` (which needs only 3 basis vectors) but
contains 12 roots.

Every root can be written as an integer linear combination of simple roots:
positive roots have all non-negative coefficients, negative roots all
non-positive. But the roots are far from independent -- the root system is a
highly structured, symmetric set of vectors that the Weyl group permutes.

The Weyl group as a group of symmetries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The mutation matrices :math:`M_1, \ldots, M_n` generate a **group** under
matrix multiplication: the **Weyl group** :math:`W`. This group is finite for
ADE-type graphs and acts on the root system.

The group axioms are satisfied as follows:

- **Closure**: the product of any two mutation matrices (or compositions
  thereof) is another element of *W*. In particular, for any root
  :math:`v \in \Phi` and any mutation :math:`M_k`, the image
  :math:`M_k v` is again a root in :math:`\Phi`.
- **Identity**: the identity matrix *I* is the "do nothing" mutation (apply
  zero mutations).
- **Inverses**: each mutation is its own inverse (:math:`M_k^2 = I`), so
  every generator is an involution. Arbitrary products are inverted by
  reversing the order:
  :math:`(M_{k_1} M_{k_2} \cdots M_{k_m})^{-1} = M_{k_m} \cdots M_{k_2} M_{k_1}`.
- **Associativity**: inherited from matrix multiplication.

The root system :math:`\Phi` is then an **orbit** of the simple roots under
this group action: :math:`\Phi = W \cdot \{e_1, \ldots, e_n\}` (together with
their negatives). The root system itself is *not* a group (it is not closed
under addition), but it is the set on which the Weyl group acts faithfully.

Finite and infinite types
-------------------------

Whether the root system is finite depends on the graph:

- **Finite type** -- The graph is a simply-laced Dynkin diagram (types A, D, E).
  The mutation game terminates with a finite root system whose size is
  determined by the type:

  .. list-table::
     :header-rows: 1

     * - Type
       - Graph structure
       - Positive roots
       - Total roots
     * - :math:`A_n`
       - Path on *n* nodes
       - :math:`\frac{n(n+1)}{2}`
       - :math:`n(n+1)`
     * - :math:`D_n` (:math:`n \geq 4`)
       - Path with a fork at one end
       - :math:`n(n-1)`
       - :math:`2n(n-1)`
     * - :math:`E_6`
       - See below
       - 36
       - 72
     * - :math:`E_7`
       - See below
       - 63
       - 126
     * - :math:`E_8`
       - See below
       - 120
       - 240

- **Infinite type** -- For any other connected graph (e.g. a cycle, or a tree
  not of ADE type), the mutation process generates infinitely many distinct
  roots.

The Cartan matrix and finite-type classification
-------------------------------------------------

The **Cartan matrix** of the graph is:

.. math::

   C = 2I - A

The type of the root system is determined entirely by the spectrum of *C*:

- **Positive definite** (all eigenvalues :math:`> 0`): the root system is
  **finite**. This happens exactly for the ADE Dynkin diagrams.
- **Positive semi-definite** (smallest eigenvalue :math:`= 0`): the root system
  is **affine** (infinite, but with controlled growth). Example: a cycle graph.
- **Indefinite** (a negative eigenvalue): the root system is **infinite** with
  no finiteness structure.

The library uses this criterion directly: ``is_finite_type()`` checks whether
the Cartan matrix is positive definite. Methods that require the full root
system (``calculate_roots``, ``plot_root_orbits``, etc.) raise a
``RuntimeError`` early if the graph is not finite type, rather than running
an unbounded BFS.

.. code-block:: pycon

   >>> from mutation import MutationGame
   >>> game = MutationGame.from_dynkin("D4")
   >>> game.is_finite_type()
   True
   >>> print(game.cartan_eigenvalues())
   [0.58578644 2.         2.         3.41421356]

   >>> cycle = MutationGame([[0,1,1],[1,0,1],[1,1,0]])
   >>> cycle.is_finite_type()
   False
   >>> print(cycle.cartan_eigenvalues())
   [0. 3. 3.]

Eigenvectors of the Cartan matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since :math:`C = 2I - A`, the eigenvectors of *C* are exactly the eigenvectors
of the adjacency matrix *A* (only the eigenvalues shift: if
:math:`A v = \lambda v` then :math:`C v = (2 - \lambda) v`).

The bilinear form :math:`\langle v, w \rangle = v^T C \, w` is the natural
**inner product** on the root lattice. The Weyl group preserves this form --
every mutation matrix satisfies :math:`M_k^T C \, M_k = C`. For simple roots,
:math:`\langle e_i, e_j \rangle = C_{ij}`, so the Cartan matrix is literally
the **Gram matrix** of the simple roots under this inner product.

The **Perron--Frobenius eigenvector** (the eigenvector of *A* with the largest
eigenvalue, equivalently the eigenvector of *C* with the smallest eigenvalue)
has all positive entries and is closely related to the **highest root** -- the
positive root with the largest height in the system.

.. code-block:: pycon

   >>> game = MutationGame.from_dynkin("A3")
   >>> vals, vecs = game.cartan_eigenvectors()
   >>> print("Eigenvalues:", vals)
   Eigenvalues: [0.58578644 2.         3.41421356]
   >>> print("Perron-Frobenius eigenvector:", vecs[:, 0])
   Perron-Frobenius eigenvector: [ 0.5         0.70710678  0.5       ]

Connection to Lie theory
------------------------

The mutation game is a combinatorial realization of the **Weyl group** action
on a root system [Wild2003]_ [Wild2020]_. The mutation matrices :math:`M_k`
are the **simple reflections** :math:`s_k` of the Weyl group *W(G)*, and the
root system :math:`\Phi` produced by the game coincides with the root system of
the corresponding simply-laced Lie algebra. Wildberger showed that the graphs
for which the mutation game produces a finite root system are precisely the
Dynkin diagrams of finite-dimensional complex simple Lie algebras. A related
purely combinatorial construction of the Lie algebras themselves for
simply-laced diagrams is given in [Wild2003b]_.

The simple reflection at node *k* acts on the weight lattice as:

.. math::

   s_k(v) = v - (C v)_k \, e_k = v - (2 v_k - \sum_{j \sim k} v_j) \, e_k

which is precisely the mutation rule:
:math:`v_k \mapsto -v_k + \sum_{j \sim k} v_j`.

The mutation graph
------------------

The **mutation graph** has the roots as vertices and an edge between two roots
whenever one can be obtained from the other by a single mutation. Each edge is
labeled with the index of the mutated node.

For finite-type graphs, the mutation graph is a finite connected graph whose
structure encodes the combinatorics of the Weyl group. The shortest path
between two roots in this graph gives the minimal sequence of mutations (simple
reflections) needed to transform one into the other.

References
----------

.. [Wild2003] N. J. Wildberger, "The Mutation Game, Coxeter Graphs, and
   Partially Ordered Multisets," preprint, UNSW, 2003.
   https://web.maths.unsw.edu.au/~norman/papers/MutationGameCoxeterGraphs.pdf

.. [Wild2020] N. J. Wildberger, "The Mutation Game, Coxeter--Dynkin Graphs,
   and Generalized Root Systems," *Algebra Colloquium*, vol. 27, no. 1,
   pp. 55--78, 2020.

.. [Wild2003b] N. J. Wildberger, "A Combinatorial Construction for
   Simply-Laced Lie Algebras," *Advances in Applied Mathematics*, vol. 30,
   no. 1--2, pp. 385--396, 2003.
   doi:`10.1016/S0196-8858(02)00541-9 <https://doi.org/10.1016/S0196-8858(02)00541-9>`_
