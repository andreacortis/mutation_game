From Platonic Solids to Dynkin Diagrams
========================================

The same Diophantine inequality :math:`\frac{1}{p+1} + \frac{1}{q+1} + \frac{1}{r+1} > 1`
that classifies ADE Dynkin diagrams (see :doc:`classification_proof`) also
classifies the Platonic solids, finite rotation groups, and spherical triangle
groups. This section traces the chain of connections.

1. Euler's Formula and Regular Polyhedra
-----------------------------------------

A **regular polyhedron** (Platonic solid) is a convex polyhedron whose faces
are congruent regular polygons and whose vertices all have the same valence.
Let a regular polyhedron have:

- :math:`V` vertices, each of valence :math:`q` (edges meeting at each vertex)
- :math:`E` edges
- :math:`F` faces, each a regular :math:`p`-gon

**Euler's polyhedron formula** gives:

.. math::

   V - E + F = 2

Each edge borders 2 faces and connects 2 vertices, so:

.. math::

   pF = 2E, \qquad qV = 2E

Substituting into Euler's formula:

.. math::

   \frac{2E}{q} - E + \frac{2E}{p} = 2

Dividing by :math:`2E`:

.. math::

   \frac{1}{q} + \frac{1}{p} - \frac{1}{2} = \frac{1}{E}

Since :math:`E > 0`, we need:

.. math::
   :label: platonic-ineq

   \frac{1}{p} + \frac{1}{q} > \frac{1}{2}

with :math:`p \geq 3` (faces are at least triangles) and :math:`q \geq 3`
(at least 3 edges meet at each vertex).

2. Enumerating Solutions
-------------------------

We enumerate all integer solutions of :eq:`platonic-ineq` with
:math:`3 \leq p \leq q` (by duality, swapping :math:`p` and :math:`q` gives
the dual polyhedron):

**Case** :math:`p = 3` (triangular faces):

.. math::

   \frac{1}{3} + \frac{1}{q} > \frac{1}{2}
   \quad\Longleftrightarrow\quad
   q < 6

- :math:`q = 3`: :math:`E = 6` -- **Tetrahedron** (4 vertices, 4 faces)
- :math:`q = 4`: :math:`E = 12` -- **Octahedron** (6 vertices, 8 faces)
- :math:`q = 5`: :math:`E = 30` -- **Icosahedron** (12 vertices, 20 faces)

**Case** :math:`p = 4` (square faces):

- :math:`q = 3`: :math:`E = 12` -- **Cube** (8 vertices, 6 faces) -- dual of octahedron

**Case** :math:`p = 5` (pentagonal faces):

- :math:`q = 3`: :math:`E = 30` -- **Dodecahedron** (20 vertices, 12 faces) -- dual of icosahedron

**Case** :math:`p \geq 6`: :math:`\frac{1}{p} + \frac{1}{q} \leq \frac{1}{6} + \frac{1}{6} < \frac{1}{2}`. **No solutions.**

That gives exactly **5 Platonic solids** (3 + 2 duals). Each is labeled
below with its corresponding Dynkin type -- the tetrahedron corresponds to
:math:`E_6`, the cube/octahedron dual pair to :math:`E_7`, and the
dodecahedron/icosahedron dual pair to :math:`E_8`.

**Interactive 3D viewer** -- click and drag to rotate, scroll to zoom
(`open fullscreen <_static/platonic_viewer.html>`__):

.. raw:: html

   <iframe src="_static/platonic_viewer.html"
     style="width:100%; height:380px; border:1px solid #444; border-radius:6px; background:#1a1a2e;"
     loading="lazy" allowfullscreen></iframe>
   <noscript>

.. image:: _static/platonic_solids_3d.png
   :width: 100%
   :alt: The five Platonic solids in 3D (static fallback for non-JS environments)

.. raw:: html

   </noscript>

3. The Rotation Groups
------------------------

Each Platonic solid has a **rotation group** -- the group of orientation-preserving
symmetries. Up to conjugacy, these are exactly the finite subgroups of
:math:`SO(3)`:

.. list-table::
   :header-rows: 1

   * - Solid
     - :math:`(p, q)`
     - Rotation group
     - Order
     - Generators
   * - Tetrahedron
     - (3, 3)
     - :math:`A_4` (alternating)
     - 12
     - 3-fold and 2-fold rotations
   * - Cube / Octahedron
     - (4, 3) / (3, 4)
     - :math:`S_4` (symmetric)
     - 24
     - 4-fold, 3-fold, 2-fold rotations
   * - Dodecahedron / Icosahedron
     - (5, 3) / (3, 5)
     - :math:`A_5` (alternating)
     - 60
     - 5-fold, 3-fold, 2-fold rotations

Additionally, there are two infinite families of finite subgroups of
:math:`SO(3)`:

- **Cyclic groups** :math:`C_n` (rotation by :math:`2\pi/n` about an axis)
- **Dihedral groups** :math:`D_n` (rotations of a regular :math:`n`-gon, including flips)

**Theorem.** *The finite subgroups of* :math:`SO(3)` *are exactly: cyclic*
:math:`C_n`, *dihedral* :math:`D_n`, *and the three polyhedral groups*
:math:`A_4, S_4, A_5`.

4. The McKay Correspondence: From SO(3) to SU(2) to Dynkin
------------------------------------------------------------

The rotation group :math:`SO(3)` has a double cover :math:`SU(2)` (the group
of unit quaternions). Every finite subgroup :math:`G \subset SO(3)` lifts to a
**binary** subgroup :math:`\tilde{G} \subset SU(2)` of twice the order:

.. list-table::
   :header-rows: 1

   * - :math:`SO(3)` subgroup
     - :math:`SU(2)` lift
     - Order
     - Dynkin diagram
   * - :math:`C_n` (cyclic)
     - Binary cyclic :math:`\tilde{C}_n`
     - :math:`2n`
     - :math:`A_{n-1}`
   * - :math:`D_n` (dihedral)
     - Binary dihedral :math:`\tilde{D}_n`
     - :math:`4n`
     - :math:`D_{n+2}`
   * - :math:`A_4` (tetrahedral)
     - Binary tetrahedral :math:`\tilde{T}`
     - 24
     - :math:`E_6`
   * - :math:`S_4` (octahedral)
     - Binary octahedral :math:`\tilde{O}`
     - 48
     - :math:`E_7`
   * - :math:`A_5` (icosahedral)
     - Binary icosahedral :math:`\tilde{I}`
     - 120
     - :math:`E_8`

The **McKay correspondence** (John McKay, 1980) explains *how* the Dynkin
diagram emerges from the group. It works as follows:

**Step 1.** Let :math:`\tilde{G} \subset SU(2)` be a finite subgroup. The
natural 2-dimensional representation :math:`\rho` of :math:`\tilde{G}`
(inherited from :math:`SU(2)`) is called the **fundamental representation**.

**Step 2.** List all irreducible representations :math:`\rho_0, \rho_1, \ldots, \rho_r`
of :math:`\tilde{G}`, where :math:`\rho_0` is the trivial representation.

**Step 3.** For each :math:`\rho_i`, decompose the tensor product with the
fundamental representation:

.. math::

   \rho \otimes \rho_i = \bigoplus_j a_{ij} \rho_j

**Step 4.** Build a graph with one node per irreducible representation, and
:math:`a_{ij}` edges between nodes :math:`i` and :math:`j`.

**Result.** The graph obtained is the **extended** (affine) Dynkin diagram
:math:`\tilde{A}_{n-1}`, :math:`\tilde{D}_{n+2}`, :math:`\tilde{E}_6`,
:math:`\tilde{E}_7`, or :math:`\tilde{E}_8`. Removing the node corresponding
to the trivial representation :math:`\rho_0` gives the ordinary Dynkin
diagram.

5. Spherical Triangle Groups
------------------------------

A **spherical triangle** is a triangle on the unit sphere :math:`S^2` with
angles :math:`\pi/p`, :math:`\pi/q`, :math:`\pi/r`. The **triangle group**
:math:`\Delta(p, q, r)` is generated by reflections in the sides of this
triangle.

On a sphere, the angle sum of a triangle exceeds :math:`\pi`:

.. math::

   \frac{\pi}{p} + \frac{\pi}{q} + \frac{\pi}{r} > \pi

Dividing by :math:`\pi`:

.. math::

   \frac{1}{p} + \frac{1}{q} + \frac{1}{r} > 1

This is exactly the same inequality as in the ADE classification (see
:doc:`classification_proof`, equation :eq:`diophantine`), with the
identification :math:`p \to p+1`, :math:`q \to q+1`, :math:`r \to r+1` (the
triangle group uses the actual angles, while the Dynkin classification uses
arm lengths).

The spherical triangle groups are:

.. list-table::
   :header-rows: 1

   * - Triangle :math:`(p, q, r)`
     - Triangle group
     - Rotation subgroup
     - Dynkin diagram
   * - :math:`(2, 2, n)`
     - Dihedral
     - :math:`D_n`
     - :math:`A_{n-1}` / :math:`D_{n+2}`
   * - :math:`(2, 3, 3)`
     - Tetrahedral
     - :math:`A_4`
     - :math:`E_6`
   * - :math:`(2, 3, 4)`
     - Octahedral
     - :math:`S_4`
     - :math:`E_7`
   * - :math:`(2, 3, 5)`
     - Icosahedral
     - :math:`A_5`
     - :math:`E_8`

When :math:`\frac{1}{p} + \frac{1}{q} + \frac{1}{r} = 1`, the triangle is
**Euclidean** (flat) and tiles the plane -- these correspond to the affine
Dynkin diagrams. When the sum is :math:`< 1`, the triangle is **hyperbolic**.

6. The Unified Picture
-----------------------

All these classifications are manifestations of the same Diophantine
constraint. The connections can be summarized as:

.. math::

   \frac{1}{p} + \frac{1}{q} + \frac{1}{r} > 1

.. list-table::
   :header-rows: 1
   :widths: 10 20 20 20 20

   * - :math:`(p,q,r)`
     - Dynkin
     - Platonic solid
     - :math:`SO(3)` group
     - Singularity
   * - :math:`(2,2,n)`
     - :math:`D_{n+2}`
     - :math:`n`-gon prism
     - Dihedral :math:`D_n`
     - :math:`x^2 y + y^{n+1}`
   * - :math:`(2,3,3)`
     - :math:`E_6`
     - Tetrahedron
     - :math:`A_4`
     - :math:`x^3 + y^4`
   * - :math:`(2,3,4)`
     - :math:`E_7`
     - Cube / Octahedron
     - :math:`S_4`
     - :math:`x^3 + xy^3`
   * - :math:`(2,3,5)`
     - :math:`E_8`
     - Dodecahedron / Icosahedron
     - :math:`A_5`
     - :math:`x^3 + y^5`

The :math:`A_n` family (path graphs) corresponds to the cyclic groups and the
:math:`x^{n+1}` singularities. They don't correspond to Platonic solids
(which require :math:`p, q \geq 3`), but rather to the simpler geometry of a
regular polygon.

We can verify the Dynkin diagrams and root counts for all these types:

.. code-block:: pycon

   >>> from mutation_game import MutationGame

   >>> # the five exceptional connections
   >>> for name, solid in [("E6", "Tetrahedron"),
   ...                      ("E7", "Cube/Octahedron"),
   ...                      ("E8", "Dodecahedron/Icosahedron")]:
   ...     game = MutationGame.from_dynkin(name)
   ...     roots = game.calculate_roots()
   ...     pos = [r for r in roots if all(v >= 0 for v in r)]
   ...     print(f"  {name} ({solid}): {len(pos)} positive roots, {len(roots)} total")
     E6 (Tetrahedron): 36 positive roots, 72 total
     E7 (Cube/Octahedron): 63 positive roots, 126 total
     E8 (Dodecahedron/Icosahedron): 120 positive roots, 240 total

Root systems as 3D polytopes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The root system of :math:`A_3` consists of 12 vectors :math:`e_i - e_j`
(:math:`i \neq j`) in :math:`\mathbb{R}^4`, projected onto the hyperplane
:math:`\sum x_i = 0`. These 12 points form the vertices of a
**cuboctahedron** -- the Archimedean solid obtained by truncating a cube at
the midpoint of every edge.

**Interactive viewer** -- positive roots in red, negative in teal, simple
roots highlighted in gold
(`open fullscreen <_static/roots_viewer.html>`__):

.. raw:: html

   <iframe src="_static/roots_viewer.html"
     style="width:100%; height:420px; border:1px solid #444; border-radius:6px; background:#1a1a2e;"
     loading="lazy" allowfullscreen></iframe>

Edges connect roots whose difference is itself a root (i.e. they are adjacent
in the root system). The cuboctahedral geometry reflects the :math:`S_4`
symmetry of the Weyl group -- the same group as the rotation group of the
cube/octahedron.

.. note::

   The 240 roots of :math:`E_8` can be realized as vectors in
   :math:`\mathbb{R}^8`. Their convex hull is the **Gosset polytope**
   :math:`4_{21}`, a remarkable 8-dimensional object with 240 vertices,
   6720 edges, and deep connections to string theory and the octonions.

7. The du Val Singularities
-----------------------------

The circle closes with the **du Val singularities** (also called rational
double points or Kleinian singularities). Given a finite subgroup
:math:`\tilde{G} \subset SU(2)`, consider its action on :math:`\mathbb{C}^2`.
The quotient :math:`\mathbb{C}^2 / \tilde{G}` is a surface with an isolated
singularity at the origin, and this singularity is of ADE type:

.. list-table::
   :header-rows: 1

   * - Group :math:`\tilde{G}`
     - Quotient singularity
     - Equation in :math:`\mathbb{C}^3`
     - Type
   * - Binary cyclic :math:`\tilde{C}_n`
     - :math:`\mathbb{C}^2 / \tilde{C}_n`
     - :math:`x^2 + y^2 + z^n = 0`
     - :math:`A_{n-1}`
   * - Binary dihedral :math:`\tilde{D}_n`
     - :math:`\mathbb{C}^2 / \tilde{D}_n`
     - :math:`x^2 + y^2 z + z^{n-1} = 0`
     - :math:`D_{n+2}`
   * - Binary tetrahedral :math:`\tilde{T}`
     - :math:`\mathbb{C}^2 / \tilde{T}`
     - :math:`x^2 + y^3 + z^4 = 0`
     - :math:`E_6`
   * - Binary octahedral :math:`\tilde{O}`
     - :math:`\mathbb{C}^2 / \tilde{O}`
     - :math:`x^2 + y^3 + yz^3 = 0`
     - :math:`E_7`
   * - Binary icosahedral :math:`\tilde{I}`
     - :math:`\mathbb{C}^2 / \tilde{I}`
     - :math:`x^2 + y^3 + z^5 = 0`
     - :math:`E_8`

The equations in the right column are exactly the ADE singularities from
Arnold's classification (see :doc:`singularities`). The resolution of these
surface singularities produces a configuration of exceptional curves whose
intersection graph is the corresponding Dynkin diagram.

This completes the circle:

.. math::

   \boxed{\text{Platonic solid}}
   \to \boxed{\text{Rotation group}}
   \to \boxed{\text{Binary group } \tilde{G} \subset SU(2)}
   \to \boxed{\mathbb{C}^2 / \tilde{G}}
   \to \boxed{\text{ADE singularity}}
   \to \boxed{\text{Dynkin diagram}}

References
-----------

.. [McKay1980] J. McKay, "Graphs, singularities, and finite groups,"
   *Proceedings of Symposia in Pure Mathematics* 37 (1980), 183--186.

.. [Klein1884] F. Klein, *Vorlesungen uber das Ikosaeder und die Auflosung
   der Gleichungen vom funften Grade*, Teubner, 1884. English translation:
   *Lectures on the Icosahedron*, Dover, 2003.

.. [duVal1934] P. du Val, "On isolated singularities of surfaces which do not
   affect the conditions of adjunction," *Proceedings of the Cambridge
   Philosophical Society* 30 (1934), 453--459.
