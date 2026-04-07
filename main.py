def main():
    from mutation import MutationGame
    # --- Example: Playing on the A3 Graph (0-1-2) ---
    # Diagram: (Node 0) --- (Node 1) --- (Node 2)
    a3_graph = [
        [0, 1, 0], # Node 0 connects to 1
        [1, 0, 1], # Node 1 connects to 0 and 2
        [0, 1, 0]  # Node 2 connects to 1
    ]

    game = MutationGame.from_dynkin("D5")

    # Start with one Martian at City 0, others empty
    game.set_starting_population([1, 0, 0, 0, 0])
    print(f"Initial State: {game.populations}")

    # Perform a sequence of mutations
    print(f"Mutate 0: {game.mutate(0)}")
    print(f"Mutate 1: {game.mutate(1)}")
    print(f"Mutate 2: {game.mutate(2)}")

    fig = game.plot_root_orbits()
    fig.savefig("roots.png", bbox_inches="tight", dpi=150)

if __name__ == "__main__":
    main()
