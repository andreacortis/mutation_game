import numpy as np
import numpy.testing as npt
import pytest
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for tests

from mutation_game import MutationGame


# --- from_dynkin construction ---

class TestFromDynkin:
    def test_a1(self):
        g = MutationGame.from_dynkin("A1")
        npt.assert_array_equal(g.adj, [[0]])

    def test_a3(self):
        g = MutationGame.from_dynkin("A3")
        expected = [[0, 1, 0],
                    [1, 0, 1],
                    [0, 1, 0]]
        npt.assert_array_equal(g.adj, expected)

    def test_d4(self):
        g = MutationGame.from_dynkin("D4")
        # chain 0-1, fork at 1: 1-2 and 1-3
        assert g.num_nodes == 4
        assert g.adj[0, 1] == 1
        assert g.adj[1, 0] == 1
        assert g.adj[1, 2] == 1
        assert g.adj[1, 3] == 1
        assert g.adj[2, 3] == 0  # fork arms not connected

    def test_d5(self):
        g = MutationGame.from_dynkin("D5")
        assert g.num_nodes == 5
        # chain 0-1-2, fork at 2: 2-3 and 2-4
        assert g.adj[0, 1] == 1
        assert g.adj[1, 2] == 1
        assert g.adj[2, 3] == 1
        assert g.adj[2, 4] == 1
        assert g.adj[3, 4] == 0

    def test_e6(self):
        g = MutationGame.from_dynkin("E6")
        assert g.num_nodes == 6
        # chain 0-1-2-3-4, branch: 2-5
        assert g.adj[2, 5] == 1
        assert g.adj[5, 2] == 1
        row_sums = g.adj.sum(axis=1)
        assert row_sums[2] == 3  # node 2 is the branch point

    def test_e8(self):
        g = MutationGame.from_dynkin("E8")
        assert g.num_nodes == 8
        assert g.adj[2, 7] == 1

    def test_invalid_type(self):
        with pytest.raises(ValueError):
            MutationGame.from_dynkin("B3")

    def test_invalid_rank(self):
        with pytest.raises(ValueError):
            MutationGame.from_dynkin("D3")
        with pytest.raises(ValueError):
            MutationGame.from_dynkin("E5")
        with pytest.raises(ValueError):
            MutationGame.from_dynkin("A0")

    def test_case_insensitive(self):
        g = MutationGame.from_dynkin("a3")
        assert g.num_nodes == 3


# --- Cartan matrix and finite type ---

class TestCartan:
    def test_cartan_matrix_a3(self):
        g = MutationGame.from_dynkin("A3")
        expected = [[ 2, -1,  0],
                    [-1,  2, -1],
                    [ 0, -1,  2]]
        npt.assert_array_equal(g.cartan_matrix(), expected)

    def test_finite_type_ade(self):
        for name in ["A1", "A5", "D4", "D6", "E6", "E7", "E8"]:
            g = MutationGame.from_dynkin(name)
            assert g.is_finite_type(), f"{name} should be finite type"

    def test_infinite_type_cycle(self):
        # A cycle (affine A_2) is not finite type
        adj = [[0, 1, 1],
               [1, 0, 1],
               [1, 1, 0]]
        g = MutationGame(adj)
        assert not g.is_finite_type()

    def test_infinite_type_raises_on_root_calculation(self):
        adj = [[0, 1, 1],
               [1, 0, 1],
               [1, 1, 0]]
        g = MutationGame(adj)
        with pytest.raises(RuntimeError, match="not positive definite"):
            g.calculate_roots()

    def test_cartan_eigenvalues_positive_for_ade(self):
        g = MutationGame.from_dynkin("D5")
        vals = g.cartan_eigenvalues()
        assert all(v > 0 for v in vals)

    def test_cartan_eigenvectors_shape(self):
        g = MutationGame.from_dynkin("A3")
        vals, vecs = g.cartan_eigenvectors()
        assert vals.shape == (3,)
        assert vecs.shape == (3, 3)

    def test_cartan_eigenvectors_are_correct(self):
        g = MutationGame.from_dynkin("A3")
        vals, vecs = g.cartan_eigenvectors()
        C = g.cartan_matrix()
        for i in range(3):
            npt.assert_allclose(C @ vecs[:, i], vals[i] * vecs[:, i], atol=1e-10)


# --- Mutation rule ---

class TestMutate:
    def test_basic_mutation(self):
        # A2: 0-1
        g = MutationGame.from_dynkin("A2")
        g.set_starting_population([1, 0])
        result = g.mutate(0)
        # new[0] = -1 + 0 = -1
        npt.assert_array_equal(result, [-1, 0])

    def test_mutation_with_neighbor(self):
        g = MutationGame.from_dynkin("A2")
        g.set_starting_population([1, 2])
        result = g.mutate(0)
        # new[0] = -1 + 2 = 1
        npt.assert_array_equal(result, [1, 2])

    def test_mutation_middle_node(self):
        g = MutationGame.from_dynkin("A3")
        g.set_starting_population([3, 1, 2])
        result = g.mutate(1)
        # new[1] = -1 + 3 + 2 = 4
        npt.assert_array_equal(result, [3, 4, 2])

    def test_invalid_node(self):
        g = MutationGame.from_dynkin("A2")
        g.set_starting_population([1, 0])
        with pytest.raises(ValueError):
            g.mutate(5)

    def test_mutation_is_involution(self):
        """Mutating the same node twice restores the original vector."""
        g = MutationGame.from_dynkin("A3")
        g.set_starting_population([2, -1, 3])
        original = g.populations.copy()
        g.mutate(1)
        g.mutate(1)
        npt.assert_array_equal(g.populations, original)


# --- Root system counts ---
# Known: |Phi+(A_n)| = n(n+1)/2, |Phi+(D_n)| = n(n-1), |Phi+(E_n)| = 36,63,120

class TestRootCounts:
    @pytest.mark.parametrize("n,expected_positive", [
        (1, 1), (2, 3), (3, 6), (4, 10), (5, 15),
    ])
    def test_a_n_positive_roots(self, n, expected_positive):
        g = MutationGame.from_dynkin(f"A{n}")
        roots = g.calculate_roots()
        assert len(roots) == 2 * expected_positive

    @pytest.mark.parametrize("n,expected_positive", [
        (4, 12), (5, 20), (6, 30),
    ])
    def test_d_n_positive_roots(self, n, expected_positive):
        g = MutationGame.from_dynkin(f"D{n}")
        roots = g.calculate_roots()
        assert len(roots) == 2 * expected_positive

    def test_e6_roots(self):
        g = MutationGame.from_dynkin("E6")
        roots = g.calculate_roots()
        assert len(roots) == 72

    def test_e7_roots(self):
        g = MutationGame.from_dynkin("E7")
        roots = g.calculate_roots()
        assert len(roots) == 126

    def test_e8_roots(self):
        g = MutationGame.from_dynkin("E8")
        roots = g.calculate_roots()
        assert len(roots) == 240

    def test_roots_symmetric(self):
        """Every root has its negative also in the set."""
        g = MutationGame.from_dynkin("D4")
        roots = g.calculate_roots()
        root_set = {tuple(r) for r in roots}
        for r in roots:
            assert tuple(-r) in root_set

    def test_all_positive_roots_have_nonneg_coords(self):
        g = MutationGame.from_dynkin("A4")
        roots = g.calculate_roots()
        for r in roots:
            is_pos = all(x >= 0 for x in r)
            is_neg = all(x <= 0 for x in r)
            assert is_pos or is_neg, f"Root {r} is neither positive nor negative"


# --- Mutation paths ---

class TestMutationPath:
    def test_same_root_returns_empty(self):
        g = MutationGame.from_dynkin("A3")
        path = g.find_mutation_path([1, 0, 0], [1, 0, 0])
        assert path == []

    def test_simple_path(self):
        g = MutationGame.from_dynkin("A2")
        # (1,0) -> mutate(0) -> (-1+0, 0) = (-1,0), or mutate(1) -> (1, -0+1) = (1,1)
        path = g.find_mutation_path([1, 0], [1, 1])
        assert len(path) == 1
        mut_idx, result = path[0]
        npt.assert_array_equal(result, [1, 1])

    def test_path_is_valid(self):
        """Walk the path and verify each mutation produces the next root."""
        g = MutationGame.from_dynkin("A3")
        source = [1, 0, 0]
        target = [0, 0, 1]
        path = g.find_mutation_path(source, target)
        assert len(path) > 0
        vec = np.array(source)
        for mut_idx, expected in path:
            neighbors = np.where(g.adj[mut_idx] == 1)[0]
            new_vec = vec.copy()
            new_vec[mut_idx] = -vec[mut_idx] + vec[neighbors].sum()
            npt.assert_array_equal(new_vec, expected)
            vec = new_vec
        npt.assert_array_equal(vec, target)

    def test_invalid_source(self):
        g = MutationGame.from_dynkin("A2")
        with pytest.raises(ValueError, match="not a root"):
            g.find_mutation_path([5, 5], [1, 0])

    def test_invalid_target(self):
        g = MutationGame.from_dynkin("A2")
        with pytest.raises(ValueError, match="not a root"):
            g.find_mutation_path([1, 0], [9, 9])

    def test_path_between_positive_and_negative(self):
        g = MutationGame.from_dynkin("A2")
        path = g.find_mutation_path([1, 0], [-1, 0])
        assert len(path) > 0
        # Verify final step lands on target
        npt.assert_array_equal(path[-1][1], [-1, 0])


# --- Plotting ---

class TestPlot:
    def test_plot_positive_only_returns_figure(self):
        g = MutationGame.from_dynkin("A3")
        fig = g.plot_root_orbits(positive_only=True)
        assert fig is not None
        assert len(fig.axes) == 2

    def test_plot_all_roots_returns_figure(self):
        g = MutationGame.from_dynkin("A2")
        fig = g.plot_root_orbits(positive_only=False)
        assert fig is not None

    def test_plot_d4(self):
        g = MutationGame.from_dynkin("D4")
        fig = g.plot_root_orbits()
        assert fig is not None
