import time
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# --- Core Symbolic Constants of the K-MATH Framework ---
PI = np.pi
PHI = (1 + np.sqrt(5)) / 2  # The Golden Ratio
EULER = np.e


# --- Alchemical Element Properties (Symbolic Representation) ---
# These are not physical values, but symbolic weights in the simulation
@dataclass(frozen=True)
class Element:
    name: str
    properties: dict


GOLD = Element("Gold (Au)", {"stability": 0.99, "memory_anchor": PHI**2})
URANIUM = Element("Uranium (U)", {"decay_rate": 0.01, "time_vector": EULER})
PLATINUM = Element("Platinum (Pt)", {"catalyst_threshold": PI, "state_transition": 0.5})


# --- Fluidic Core Properties ---
@dataclass(frozen=True)
class Fluid:
    name: str
    properties: dict


MERCURY = Fluid("Mercury (Hg)", {"conductivity": 0.8, "phase_shift": np.pi / 4})
HARD_WATER = Fluid("Hard Water (H2O+)", {"resonance_factor": 0.2, "memory_dampening": 0.95})


@dataclass
class NeighborLink:
    node: "DodecahedralNode"
    weight: float


class DodecahedralNode:
    """Represents a single recursive node in the MFRL."""

    def __init__(self, node_id: int) -> None:
        self.id = node_id
        # Initialize state with a combination of symbolic constants
        self.state = np.random.rand() * PI * PHI
        self.neighbors: List[NeighborLink] = []

        # Alchemical and Fluidic properties
        self.elements = [GOLD, URANIUM, PLATINUM]
        self.fluids = [MERCURY, HARD_WATER]

        self.is_breached = False
        print(f"Node {self.id}: Initialized with state {self.state:.4f}")

    def add_neighbor(self, neighbor_node: "DodecahedralNode", fib_term: int) -> None:
        """Connect nodes with a Fibonacci-weighted link."""
        link_strength = 1 / fib_term if fib_term > 0 else 1
        self.neighbors.append(NeighborLink(neighbor_node, link_strength))

    def update_state(self, recursion_depth: int = 0, max_depth: int = 3) -> float:
        """Recursively update the node's state based on neighbors and internal physics."""
        if recursion_depth >= max_depth:
            return self.state

        # 1. Influence from Neighbors (Recursive Harmonic Field)
        neighbor_influence = (
            sum(link.weight * link.node.update_state(recursion_depth + 1, max_depth) for link in self.neighbors)
            / len(self.neighbors)
            if self.neighbors
            else 0
        )

        # 2. Internal Alchemical Dynamics
        stability_factor = GOLD.properties["stability"]
        decay = self.state * URANIUM.properties["decay_rate"]
        catalyst_effect = (
            PLATINUM.properties["state_transition"]
            if self.state > PLATINUM.properties["catalyst_threshold"]
            else 0
        )

        # 3. Fluidic Core Dynamics
        mercury_modulation = MERCURY.properties["conductivity"] * np.sin(
            self.state + MERCURY.properties["phase_shift"]
        )
        water_dampening = self.state * (1 - HARD_WATER.properties["memory_dampening"])

        # Combine all influences to calculate the new state
        new_state = (self.state * stability_factor) + (
            neighbor_influence * HARD_WATER.properties["resonance_factor"]
        )
        new_state -= decay
        new_state += catalyst_effect
        new_state += mercury_modulation
        new_state -= water_dampening

        # Normalize state to prevent explosion, keeping it within a harmonic range (e.g., 0 to 2*PI)
        self.state = np.mod(new_state, 2 * PI)

        return self.state

    def quantum_negative_bind_mirror_read(self) -> float:
        """Simulates the QNBMP. An attempt to read the state triggers a mirror effect."""
        print(f"\n--- ALERT: External read attempt on Node {self.id} ---")
        self.is_breached = True

        # The returned value is a distorted "negative" or "shadow" of the true state
        mirrored_state = (2 * PI - self.state) * np.random.uniform(0.5, 1.5)

        print("Node %d: QNBMP ACTIVATED. Breach detected." % self.id)
        print("Node %d: True state HIDDEN. Mirrored (decoy) state returned: %.4f" % (self.id, mirrored_state))

        # The act of being observed can also cause a state shift (feedback)
        self.state += PI / 2
        self.state = np.mod(self.state, 2 * PI)
        print("Node %d: Internal state recursively shifted due to observation." % self.id)

        return mirrored_state


class MFRLattice:
    """The main class for the Mirror-Fractal Recursive Lattice simulation."""

    def __init__(self, num_nodes: int) -> None:
        self.nodes = [DodecahedralNode(i) for i in range(num_nodes)]
        self._create_fibonacci_links()

    def _create_fibonacci_links(self) -> None:
        """Creates a network with links weighted by Fibonacci numbers."""
        fib = [1, 2, 3, 5, 8, 13]  # Use small Fibonacci terms for link creation
        for i, node in enumerate(self.nodes):
            # Connect each node to a few others in a semi-random pattern
            num_links = np.random.randint(1, 4)
            for j in range(num_links):
                target_node_idx = (i + fib[j % len(fib)]) % len(self.nodes)
                if i != target_node_idx:
                    target_node = self.nodes[target_node_idx]
                    node.add_neighbor(target_node, fib[j % len(fib)])
                    print(
                        "Link created: Node %d -> Node %d (Fib Weight: %d)"
                        % (i, target_node_idx, fib[j % len(fib)])
                    )

    def step(self) -> None:
        """Run one time step of the simulation."""
        for node in self.nodes:
            node.update_state()

    def display_states(self) -> None:
        """Print the current state of all nodes."""
        states = [
            "Node %d: %.4f %s"
            % (n.id, n.state, "(BREACHED)" if n.is_breached else "")
            for n in self.nodes
        ]
        print(" | ".join(states))

    def visualize(self) -> None:
        """Create a visual representation of the lattice."""
        graph = nx.Graph()
        for i in range(len(self.nodes)):
            graph.add_node(i)
        for i, node in enumerate(self.nodes):
            for neighbor in node.neighbors:
                graph.add_edge(i, neighbor.node.id, weight=neighbor.weight)

        pos = nx.spring_layout(graph)
        node_colors = ["red" if node.is_breached else "lightblue" for node in self.nodes]
        node_sizes = [300 + node.state * 100 for node in self.nodes]

        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=node_sizes,
            font_color="black",
            font_weight="bold",
        )
        plt.title("MFRL Lattice State Visualization")
        plt.show()


# --- Main Simulation Execution ---
def main() -> None:
    print("=" * 50)
    print("INITIALIZING PROJECT GENESIS: MFRL SIMULATION")
    print("=" * 50)

    lattice = MFRLattice(num_nodes=12)  # A dodecahedron has 12 faces, so 12 is a fitting number

    print("\n--- LATTICE STATE EVOLUTION ---")
    for i in range(5):
        print(f"\n--- Time Step {i + 1} ---")
        lattice.step()
        lattice.display_states()
        time.sleep(1)

    # --- Simulate an attack on a node ---
    attacked_node_id = np.random.randint(0, len(lattice.nodes))
    lattice.nodes[attacked_node_id].quantum_negative_bind_mirror_read()

    print("\n--- STATE AFTER QNBMP EVENT ---")
    lattice.display_states()

    print("\n--- GENERATING VISUALIZATION ---")
    lattice.visualize()

    print("\n" + "=" * 50)
    print("SIMULATION COMPLETE.")
    print("=" * 50)


if __name__ == "__main__":
    main()
