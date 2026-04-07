Proof of the ADE Classification
================================

We prove that a connected simple graph has a finite root system under the
mutation game if and only if it is one of the Dynkin diagrams
:math:`A_n`, :math:`D_n`, :math:`E_6`, :math:`E_7`, or :math:`E_8`.

The spectral criterion
----------------------

Let :math:`G` be a connected simple graph on :math:`n` vertices with adjacency
matrix :math:`A` and Cartan matrix :math:`C = 2I - A`. As established in
:doc:`background`, the root system is finite if and only if :math:`C` is
positive definite.

Since the eigenvalues of :math:`C` are :math:`2 - \lambda_i` where
:math:`\lambda_i` are the eigenvalues of :math:`A`, positive definiteness of
:math:`C` is equivalent to:

.. math::

   \rho(A) < 2

where :math:`\rho(A)` denotes the spectral radius (largest eigenvalue) of
:math:`A`. We now classify all connected simple graphs satisfying this
condition.

Step 1: The graph must be a tree
---------------------------------

**Claim.** If :math:`G` contains a cycle, then :math:`\rho(A) \geq 2`.

*Proof.* The cycle graph :math:`C_m` on :math:`m` vertices has eigenvalues
:math:`2\cos(2\pi k/m)` for :math:`k = 0, 1, \ldots, m-1`. The largest
eigenvalue is :math:`2\cos(0) = 2`.

If :math:`G` contains :math:`C_m` as a subgraph, then by the interlacing
theorem for graph spectra, :math:`\rho(A_G) \geq \rho(A_{C_m}) = 2`.

Therefore :math:`G` must be acyclic. Since :math:`G` is connected, it is a
tree. :math:`\square`

Step 2: Maximum degree at most 3
----------------------------------

**Claim.** Every vertex of :math:`G` has degree at most 3.

*Proof.* The star graph :math:`K_{1,m}` (one center connected to :math:`m`
leaves) has adjacency eigenvalues :math:`\pm\sqrt{m}` and :math:`0` with
multiplicity :math:`m-1`. Thus :math:`\rho(K_{1,m}) = \sqrt{m}`.

For :math:`m \geq 4`, we have :math:`\sqrt{m} \geq 2`. If :math:`G` contains
a vertex of degree :math:`\geq 4`, then :math:`G` contains :math:`K_{1,4}` as
a subgraph, and by interlacing :math:`\rho(A_G) \geq 2`. :math:`\square`

Step 3: At most one branch point
----------------------------------

**Claim.** :math:`G` has at most one vertex of degree 3 (branch point).

*Proof.* Suppose :math:`G` has two vertices :math:`u, v` of degree 3. Since
:math:`G` is a tree, there is a unique path from :math:`u` to :math:`v`. Each
of :math:`u` and :math:`v` has two additional arms branching off this path.
This means :math:`G` contains the graph :math:`T` formed by two degree-3
vertices connected by a path with an extra leaf at each end:

.. math::

   \bullet - u - \cdots - v - \bullet

with at least one additional edge at both :math:`u` and :math:`v`. The
smallest such graph is:

.. math::

   \bullet - \bullet - \bullet - \bullet - \bullet - \bullet

(a path of length 5, i.e. :math:`D_4` with an extra arm). One can verify
directly (or by interlacing with the known :math:`\tilde{D}_4` extended Dynkin
diagram) that two branch points force :math:`\rho(A) \geq 2`. :math:`\square`

Step 4: No branch point gives A\ :sub:`n`
-------------------------------------------

If :math:`G` is a tree with no vertex of degree 3, then every vertex has
degree at most 2, so :math:`G` is a **path graph** :math:`A_n` on :math:`n`
vertices. Its eigenvalues are :math:`2\cos\!\bigl(\frac{k\pi}{n+1}\bigr)` for
:math:`k = 1, \ldots, n`, so:

.. math::

   \rho(A_{A_n}) = 2\cos\!\left(\frac{\pi}{n+1}\right) < 2

for all :math:`n \geq 1`. :math:`\checkmark`

Step 5: The Diophantine inequality
------------------------------------

Suppose :math:`G` is a tree with exactly one branch point, having three arms
of lengths :math:`p, q, r` edges (so :math:`p + q + r + 1` vertices total),
with :math:`1 \leq p \leq q \leq r`. We denote this tree :math:`T_{p,q,r}`.

**Theorem.** :math:`\rho(T_{p,q,r}) < 2` if and only if

.. math::
   :label: diophantine

   \frac{1}{p+1} + \frac{1}{q+1} + \frac{1}{r+1} > 1

*Proof sketch.* The characteristic polynomial of the adjacency matrix of
:math:`T_{p,q,r}` can be expressed in terms of Chebyshev polynomials. Setting
:math:`\lambda = 2` and analyzing the sign yields the condition above. The key
identity is that a path of length :math:`\ell` contributes a factor related to
:math:`U_\ell(\lambda/2)` (Chebyshev polynomial of the second kind), and the
condition :math:`\rho < 2` reduces to a positivity condition on the sum of
reciprocals of these Chebyshev values, which simplifies to
:eq:`diophantine`. For a complete proof, see [Wild2003]_ or standard references
on Coxeter groups. :math:`\square`

Step 6: Enumerating solutions
------------------------------

We now enumerate all integer solutions of :eq:`diophantine` with
:math:`1 \leq p \leq q \leq r`.

**Case** :math:`p = 1`:

.. math::

   \frac{1}{2} + \frac{1}{q+1} + \frac{1}{r+1} > 1
   \quad\Longleftrightarrow\quad
   \frac{1}{q+1} + \frac{1}{r+1} > \frac{1}{2}

- :math:`q = 1`: :math:`\frac{1}{2} + \frac{1}{r+1} > \frac{1}{2}` holds for
  all :math:`r \geq 1`. This gives :math:`T_{1,1,r} = D_{r+3}` for
  :math:`r \geq 1`, i.e. :math:`D_n` for :math:`n \geq 4`. :math:`\checkmark`

- :math:`q = 2`: :math:`\frac{1}{3} + \frac{1}{r+1} > \frac{1}{2}`, so
  :math:`r+1 < 6`, i.e. :math:`r \in \{2, 3, 4\}`:

  - :math:`T_{1,2,2}`: :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{3} = \frac{7}{6} > 1` → **E**\ :sub:`6` :math:`\checkmark`
  - :math:`T_{1,2,3}`: :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{4} = \frac{13}{12} > 1` → **E**\ :sub:`7` :math:`\checkmark`
  - :math:`T_{1,2,4}`: :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{5} = \frac{31}{30} > 1` → **E**\ :sub:`8` :math:`\checkmark`
  - :math:`T_{1,2,5}`: :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{6} = 1` → **fails** (affine :math:`\tilde{E}_8`)

- :math:`q \geq 3`: :math:`\frac{1}{q+1} + \frac{1}{r+1} \leq \frac{1}{4} + \frac{1}{4} = \frac{1}{2}`, which does not satisfy :math:`> \frac{1}{2}`. **No solutions.**

**Case** :math:`p = 2`:

.. math::

   \frac{1}{3} + \frac{1}{q+1} + \frac{1}{r+1} > 1
   \quad\Longleftrightarrow\quad
   \frac{1}{q+1} + \frac{1}{r+1} > \frac{2}{3}

Since :math:`q \geq p = 2`, we have :math:`\frac{1}{q+1} \leq \frac{1}{3}`,
so :math:`\frac{1}{r+1} > \frac{1}{3}`, requiring :math:`r < 2`. But
:math:`r \geq q \geq 2`, a contradiction. **No solutions.**

**Case** :math:`p \geq 3`: Then :math:`\frac{1}{p+1} + \frac{1}{q+1} + \frac{1}{r+1} \leq 3 \cdot \frac{1}{4} < 1`. **No solutions.**

The complete classification
----------------------------

Combining all steps, the connected simple graphs with :math:`\rho(A) < 2` are
exactly:

.. list-table::
   :header-rows: 1
   :widths: 15 25 30

   * - Diagram
     - Tree structure
     - Diophantine data
   * - :math:`A_n` (:math:`n \geq 1`)
     - Path on :math:`n` vertices
     - (no branch point)
   * - :math:`D_n` (:math:`n \geq 4`)
     - :math:`T_{1, 1, n-3}`
     - :math:`\frac{1}{2} + \frac{1}{2} + \frac{1}{n-2} > 1`
   * - :math:`E_6`
     - :math:`T_{1, 2, 2}`
     - :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{3} > 1`
   * - :math:`E_7`
     - :math:`T_{1, 2, 3}`
     - :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{4} > 1`
   * - :math:`E_8`
     - :math:`T_{1, 2, 4}`
     - :math:`\frac{1}{2} + \frac{1}{3} + \frac{1}{5} > 1`

No other connected simple graphs produce a finite root system under the
mutation game. :math:`\blacksquare`

Connections
-----------

The inequality :math:`\frac{1}{p+1} + \frac{1}{q+1} + \frac{1}{r+1} > 1` is
the same constraint that classifies:

- **Platonic solids** — via Euler's formula :math:`V - E + F = 2` applied to
  regular polyhedra with face valence :math:`p+1`, vertex valence :math:`q+1`
- **Finite subgroups of SO(3)** — cyclic, dihedral, tetrahedral (E₆),
  octahedral (E₇), icosahedral (E₈)
- **Finite subgroups of SU(2)** — the binary polyhedral groups (McKay
  correspondence)
- **Spherical triangle groups** — triangles with angles
  :math:`\frac{\pi}{p+1}, \frac{\pi}{q+1}, \frac{\pi}{r+1}` on the sphere
  (angle sum > π)
- **Simple singularities** — Arnold's classification of ADE singularities
  (the low-codimension cases are Thom's seven catastrophes)

This ubiquity was highlighted by V. I. Arnold [Arnold1976]_ and is one of the
most striking phenomena in mathematics.

References
^^^^^^^^^^

.. [Arnold1976] V. I. Arnold, "Problems in present day mathematics,"
   in *Mathematical Developments Arising from Hilbert Problems*,
   Proceedings of Symposia in Pure Mathematics, vol. 28, AMS, 1976.
