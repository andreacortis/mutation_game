import numpy as np

class MutationGame:
    def __init__(self, adj_matrix):
        """
        adj_matrix: A square matrix where 1 indicates a connection.
        populations: An array representing the Martians (positive) or 
                     Anti-Martians (negative) at each node.
        """
        self.adj = np.array(adj_matrix)
        self.num_nodes = len(adj_matrix)
        self.populations = np.zeros(self.num_nodes, dtype=int)
        self.name = None
        self._mutation_matrices = self._build_mutation_matrices()
        self._cartan = 2 * np.eye(self.num_nodes, dtype=int) - self.adj

    def _build_mutation_matrices(self):
        """
        Precompute the mutation matrix M_k for each node k.

        M_k is the identity matrix with row k replaced:
            M_k[k, k] = -1
            M_k[k, j] = adj[k, j]  for j != k

        Applying mutation at node k is then: v' = M_k @ v
        """
        matrices = []
        for k in range(self.num_nodes):
            M = np.eye(self.num_nodes, dtype=int)
            M[k] = self.adj[k]
            M[k, k] = -1
            matrices.append(M)
        return matrices

    def mutation_matrix(self, node_idx):
        """Return the mutation matrix for a given node index."""
        if not (0 <= node_idx < self.num_nodes):
            raise ValueError("Invalid node index.")
        return self._mutation_matrices[node_idx].copy()

    def cartan_matrix(self):
        """Return the Cartan matrix C = 2I - A."""
        return self._cartan.copy()

    def is_finite_type(self):
        """
        Check whether the root system is finite.

        The root system is finite if and only if the Cartan matrix C = 2I - A
        is positive definite (all eigenvalues > 0).
        """
        eigenvalues = np.linalg.eigvalsh(self._cartan)
        return bool(np.all(eigenvalues > 1e-10))

    def cartan_eigenvalues(self):
        """Return the eigenvalues of the Cartan matrix, sorted ascending."""
        return np.sort(np.linalg.eigvalsh(self._cartan))

    def cartan_eigenvectors(self):
        """
        Return the eigenvalues and eigenvectors of the Cartan matrix.

        Returns a tuple ``(eigenvalues, eigenvectors)`` where *eigenvalues* is
        a 1-D array sorted ascending and *eigenvectors* is a 2-D array whose
        column *i* is the eigenvector for ``eigenvalues[i]``.
        """
        vals, vecs = np.linalg.eigh(self._cartan)
        order = np.argsort(vals)
        return vals[order], vecs[:, order]

    @classmethod
    def from_dynkin(cls, name):
        """
        Create a MutationGame from a Dynkin diagram name.

        Supported types (simply-laced):
            A_n (n >= 1): path graph
            D_n (n >= 4): path with fork at one end
            E_6, E_7, E_8: exceptional diagrams

        Examples: "A3", "D5", "E6"
        """
        name = name.strip().upper()
        if len(name) < 2 or name[0] not in "ADE":
            raise ValueError(f"Unknown Dynkin type: {name}")

        family = name[0]
        try:
            n = int(name[1:])
        except ValueError:
            raise ValueError(f"Unknown Dynkin diagram: {name}")

        if family == "A":
            if n < 1:
                raise ValueError("A_n requires n >= 1")
            adj = np.zeros((n, n), dtype=int)
            for i in range(n - 1):
                adj[i, i + 1] = adj[i + 1, i] = 1

        elif family == "D":
            if n < 4:
                raise ValueError("D_n requires n >= 4")
            adj = np.zeros((n, n), dtype=int)
            # Main chain: 0-1-2-...-(n-3)
            for i in range(n - 3):
                adj[i, i + 1] = adj[i + 1, i] = 1
            # Fork: node (n-3) connects to both (n-2) and (n-1)
            adj[n - 3, n - 2] = adj[n - 2, n - 3] = 1
            adj[n - 3, n - 1] = adj[n - 1, n - 3] = 1

        elif family == "E":
            if n not in (6, 7, 8):
                raise ValueError("E_n is only defined for n = 6, 7, 8")
            adj = np.zeros((n, n), dtype=int)
            # Main chain: 0-1-2-3-...-(n-2)
            for i in range(n - 2):
                adj[i, i + 1] = adj[i + 1, i] = 1
            # Branch: node (n-1) connects to node 2
            adj[2, n - 1] = adj[n - 1, 2] = 1

        instance = cls(adj)
        instance.name = f"{family}{n}"
        return instance

    def set_starting_population(self, node_values):
        """Initializes the cities with specific populations."""
        self.populations = np.array(node_values)

    def mutate(self, node_idx):
        """
        Apply the mutation at node_idx as a matrix multiplication.

        The mutation matrix M_k is the identity with row k replaced so that:
            M_k[k, k] = -1,  M_k[k, j] = adj[k, j]  for j != k

        This gives: new_population = M_k @ old_population, which is equivalent
        to the mutation game rule: new[k] = -old[k] + sum(neighbors of k).
        """
        if not (0 <= node_idx < self.num_nodes):
            raise ValueError("Invalid node index.")
        self.populations = self._mutation_matrices[node_idx] @ self.populations
        return self.populations.copy()

    def _build_root_system(self):
        """
        BFS over all mutation sequences from the simple roots.

        Each mutation is applied as a matrix multiplication: v' = M_k @ v.
        The Cartan matrix must be positive definite (finite-type graph),
        otherwise the root system is infinite and cannot be fully computed.

        Returns:
            roots: set of tuples (each tuple is a root vector)
            edges: list of (src_tuple, dst_tuple, mutation_index)

        Raises:
            RuntimeError: if the graph is not finite type.
        """
        if not self.is_finite_type():
            raise RuntimeError(
                "The Cartan matrix is not positive definite — the root "
                "system is infinite and cannot be fully enumerated. "
                f"Smallest eigenvalue: {self.cartan_eigenvalues()[0]:.6f}"
            )

        roots = set()
        queue = []
        edges = []

        for i in range(self.num_nodes):
            e_i = np.zeros(self.num_nodes, dtype=int)
            e_i[i] = 1
            for v in (e_i, -e_i):
                roots.add(tuple(v))
                queue.append(v)

        head = 0
        while head < len(queue):
            vec = queue[head]
            head += 1
            for k, M in enumerate(self._mutation_matrices):
                new_vec = M @ vec
                key = tuple(new_vec)
                src = tuple(vec)
                if src != key:
                    edges.append((src, key, k))
                if key not in roots:
                    roots.add(key)
                    queue.append(new_vec)

        return roots, edges

    def calculate_roots(self):
        """
        Compute the root system by applying all possible mutation sequences
        starting from each simple root (standard basis vector e_i).

        Requires a finite-type graph (positive definite Cartan matrix).

        Returns:
            roots: list of numpy arrays representing the distinct roots
        """
        roots, _ = self._build_root_system()
        return [np.array(r) for r in sorted(roots)]

    def find_mutation_path(self, source, target):
        """
        Find a shortest sequence of mutations transforming source into target.

        Args:
            source: root vector (list or array)
            target: root vector (list or array)

        Returns:
            A list of (mutation_index, resulting_vector) pairs representing
            each step. Returns an empty list if source == target.

        Raises:
            ValueError: if source or target is not in the root system,
                        or no path exists between them.
        """
        from collections import deque

        roots, edges = self._build_root_system()
        src = tuple(int(x) for x in source)
        dst = tuple(int(x) for x in target)

        if src not in roots:
            raise ValueError(f"{list(source)} is not a root.")
        if dst not in roots:
            raise ValueError(f"{list(target)} is not a root.")
        if src == dst:
            return []

        # Build adjacency dict: node -> list of (neighbor, mutation_index)
        adj = {}
        for s, d, m in edges:
            if s != d:
                adj.setdefault(s, []).append((d, m))
                adj.setdefault(d, []).append((s, m))

        # BFS for shortest path
        visited = {src: None}  # node -> (parent, mutation_index)
        queue = deque([src])
        while queue:
            node = queue.popleft()
            for neighbor, mut in adj.get(node, []):
                if neighbor not in visited:
                    visited[neighbor] = (node, mut)
                    if neighbor == dst:
                        queue.clear()
                        break
                    queue.append(neighbor)

        if dst not in visited:
            raise ValueError("No path exists between the given roots.")

        # Reconstruct path
        path = []
        node = dst
        while visited[node] is not None:
            parent, mut = visited[node]
            path.append((mut, np.array(node)))
            node = parent
        path.reverse()
        return path

    def mutation_path_table(self, positive_only=True):
        """
        Build a table of shortest mutation paths between all pairs of roots.

        Args:
            positive_only: if True (default), only include positive roots

        Returns:
            A list of dicts with keys 'source', 'target', 'path', 'length'.
            'path' is a list of mutation indices.
        """
        from collections import deque

        roots, edges = self._build_root_system()

        if positive_only:
            roots = {r for r in roots if all(x >= 0 for x in r)}
            edges = [(s, d, m) for s, d, m in edges
                     if all(x >= 0 for x in s) and all(x >= 0 for x in d)]

        # Build adjacency dict
        adj = {}
        for s, d, m in edges:
            if s != d:
                adj.setdefault(s, []).append((d, m))
                adj.setdefault(d, []).append((s, m))

        sorted_roots = sorted(roots)

        def fmt(t):
            return "(" + ", ".join(str(int(x)) for x in t) + ")"

        # BFS from each root (all-pairs shortest paths)
        table = []
        for src in sorted_roots:
            visited = {src: None}
            queue = deque([src])
            while queue:
                node = queue.popleft()
                for neighbor, mut in adj.get(node, []):
                    if neighbor not in visited:
                        visited[neighbor] = (node, mut)
                        queue.append(neighbor)

            for dst in sorted_roots:
                if src >= dst:
                    continue
                if dst not in visited:
                    continue
                # Reconstruct
                mutations = []
                node = dst
                while visited[node] is not None:
                    parent, mut = visited[node]
                    mutations.append(mut)
                    node = parent
                mutations.reverse()
                table.append({
                    "source": fmt(src),
                    "target": fmt(dst),
                    "path": mutations,
                    "length": len(mutations),
                })

        return table

    def print_mutation_path_table(self, positive_only=True):
        """Print the mutation path table in a formatted layout."""
        table = self.mutation_path_table(positive_only)
        if not table:
            print("No pairs found.")
            return

        # Column widths
        sw = max(len(row["source"]) for row in table)
        tw = max(len(row["target"]) for row in table)
        pw = max(len(" -> ".join(str(m) for m in row["path"])) for row in table)

        header = f"{'Source':<{sw}}  {'Target':<{tw}}  {'Mutations':<{pw}}  Len"
        print(header)
        print("-" * len(header))
        for row in table:
            path_str = " -> ".join(str(m) for m in row["path"])
            print(f"{row['source']:<{sw}}  {row['target']:<{tw}}  {path_str:<{pw}}  {row['length']}")

    def plot_root_orbits(self, positive_only=True):
        """
        Build and display the mutation graph of the root system.

        Each node is a root vector; an edge connects two roots that differ by
        a single mutation, labeled with the mutation index.

        Args:
            positive_only: if True (default), show only positive roots with
                           simple roots aligned at the top

        Requires: pip install networkx matplotlib
        """
        import matplotlib
        import matplotlib.pyplot as plt
        import networkx as nx

        all_roots, all_edges = self._build_root_system()

        def label(t):
            return "(" + ", ".join(str(int(x)) for x in t) + ")"

        def is_positive(t):
            return all(x >= 0 for x in t)

        # One distinct color per node index, shared between Dynkin diagram
        # and the corresponding simple roots in the mutation graph
        cmap = matplotlib.colormaps["tab10"]
        node_colors_map = {i: cmap(i % 10) for i in range(self.num_nodes)}

        pos_simple = {}
        neg_simple = {}
        for i in range(self.num_nodes):
            e_i = tuple(int(j == i) for j in range(self.num_nodes))
            pos_simple[label(e_i)] = i
            neg_simple[label(tuple(-x for x in e_i))] = i

        if positive_only:
            roots = {r for r in all_roots if is_positive(r)}
            edges = [(s, d, m) for s, d, m in all_edges
                     if is_positive(s) and is_positive(d)]
        else:
            roots = all_roots
            edges = all_edges

        G = nx.Graph()
        roots_by_label = {}
        for r in roots:
            roots_by_label[label(r)] = r
            G.add_node(label(r))
        for src, dst, mut in edges:
            G.add_edge(label(src), label(dst), mutation=mut)

        if positive_only:
            # Hierarchical layout: simple roots at top, height by sum of coords
            max_height = max(sum(r) for r in roots)
            by_height = {}
            for r in roots:
                h = sum(r)
                by_height.setdefault(h, []).append(label(r))

            node_pos = {}
            for h, nodes in by_height.items():
                y = h / max(1, max_height)
                for idx, n in enumerate(sorted(nodes)):
                    x = (idx - (len(nodes) - 1) / 2) * 1.5
                    node_pos[n] = (x, -y)
        else:
            node_pos = nx.spring_layout(G, seed=42, k=2.0 / max(1, len(G)) ** 0.5)

        colors = []
        for n in G.nodes:
            if n in pos_simple:
                colors.append(node_colors_map[pos_simple[n]])
            elif n in neg_simple:
                colors.append(node_colors_map[neg_simple[n]])
            elif is_positive(roots_by_label[n]):
                colors.append("peachpuff")
            else:
                colors.append("lightgreen")

        fig, (ax_graph, ax_roots) = plt.subplots(1, 2, figsize=(16, 8),
                                                    gridspec_kw={"width_ratios": [1, 3]})

        # Left panel: original adjacency graph
        O = nx.from_numpy_array(self.adj)
        O = nx.relabel_nodes(O, {i: str(i) for i in range(self.num_nodes)})
        o_pos = nx.spring_layout(O, seed=42)
        o_colors = [node_colors_map[i] for i in range(self.num_nodes)]
        nx.draw(
            O, o_pos, ax=ax_graph,
            with_labels=True,
            node_size=700,
            font_size=10,
            node_color=o_colors,
            edge_color="gray",
            edgecolors="black",
        )
        graph_title = self.name if self.name else "Input graph"
        ax_graph.set_title(graph_title)

        # Right panel: mutation graph of roots
        nx.draw(
            G, node_pos, ax=ax_roots,
            with_labels=True,
            node_size=600,
            font_size=7,
            node_color=colors,
            edge_color="gray",
        )
        edge_labels = nx.get_edge_attributes(G, "mutation")
        nx.draw_networkx_edge_labels(
            G, node_pos, edge_labels=edge_labels, font_size=6, ax=ax_roots
        )
        n_label = "positive roots" if positive_only else "roots"
        prefix = f"{self.name} — " if self.name else ""
        ax_roots.set_title(f"{prefix}{len(roots)} {n_label}, {len(G.edges)} edges")

        return fig
