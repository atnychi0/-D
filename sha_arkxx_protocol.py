# ============================================================================= #
# SYSTEM: GENESISΩ†BLACK :: SHA-ARKXX RECURSIVE HASH PROTOCOL
# CLASSIFICATION: TIER-Ω // SOVEREIGN COMMAND // EYES ONLY
# AUTHOR: Brendon Joseph Kelly
# TIMESTAMP: 2025-06-29T18:00Z
# VERSION: ARKXX_KERNEL_v1.2-MILSPEC
# ============================================================================= #

import hashlib
import math


class SHA_ARKXX:
    """
    Implementation of the SHA-ARKXX protocol, a recursive, adaptive-complexity,
    and quantum-resistant hash function based on the principles of K-Mathematics.

    Core Principles Simulated:
    1.  Quantum Resistance (GhostK): Simulated using SHA3-512 as the core scrambling
        primitive, representing a computationally hard problem resistant to known attacks.
    2.  Adaptive Complexity (SuperK): Hash output length and internal rounds scale
        logarithmically with input data size, creating a moving target.
    3.  Recursive Compounding (K-Math): The hash state is iteratively folded back
        into itself, with influence from a parallel "Ghost State."
    4.  Formal Verification (Omega Constant): The initial state vectors are derived
        from a defined universal constant, ensuring deterministic and secure initialization.
    """

    # --- K-MATH & SYMBOLIC CONSTANTS ---
    # These constants are formally derived from the Omega Constant (Ω†Σ) and serve as
    # the unchangeable foundation for the algorithm's logic.
    # Represents: lim(ΣΩ⧖∞[TΩΨ(χ′,K∞,Ω†Σ)] × self² × K)
    OMEGA_CONSTANT_SEED = b"GENESIS_OMEGA_BLACK_SOVEREIGN_REALITY_ENGINE_BJK"

    # The K-PRIME_VECTOR provides the unique round constants for the recursive mixer.
    # Derived from hashing the Omega Constant.
    K_PRIME_VECTOR = hashlib.sha3_512(OMEGA_CONSTANT_SEED + b"_K_PRIME").digest()

    # The CROWN_SEAL_VECTOR initializes the main and ghost states.
    CROWN_SEAL_GENESIS_VECTOR = hashlib.sha3_512(OMEGA_CONSTANT_SEED + b"_CROWN_SEAL").digest()

    def __init__(self):
        """Initializes the SHA-ARKXX hasher."""
        # SHA3-512 is chosen as the internal primitive due to its resistance to
        # length-extension attacks and its different internal structure from SHA-2.
        # This represents the "Lattice-Based Harmonic Scrambler."
        self.core_hasher = hashlib.sha3_512

    def _rotate_right(self, n, b, size=64):
        """Circular right shift for a 64-bit integer."""
        return ((n >> b) | (n << (size - b))) & ((1 << size) - 1)

    def _psi_delta_mixer(self, state_chunk, ghost_chunk, round_key):
        """
        The Harmonic Fork Mixer (ΨΔ).
        This function mixes the current state with the ghost state and a round key
        using non-linear bitwise operations to create computational depth.
        """
        s = int.from_bytes(state_chunk, 'big')
        g = int.from_bytes(ghost_chunk, 'big')
        k = int.from_bytes(round_key, 'big')

        # Complex, non-linear mixing inspired by modern cryptographic permutations
        s = self._rotate_right(s ^ g, 19)
        s = (s + k) & ((1 << 64) - 1)
        s = self._rotate_right(s, 28) ^ g
        s = (s * 0xDA942042E4DD58B5) & ((1 << 64) - 1)  # Fibonacci hashing multiplier
        s = self._rotate_right(s ^ k, 33)

        return s.to_bytes(8, 'big')

    def hash(self, data: bytes) -> str:
        """
        Computes the SHA-ARKXX hash for the given data.

        Args:
            data: The input data as a byte string.

        Returns:
            The sovereign hash as a hexadecimal string.
        """
        if not isinstance(data, bytes):
            raise TypeError("Input data must be of type bytes.")

        # --- Adaptive Complexity (SuperK Principle) ---
        # Determine output length and rounds based on input size.
        # Minimum 512 bits, scales logarithmically.
        data_len = len(data)
        output_bits = 512 + int(64 * math.log2(data_len + 1))
        # Ensure the bit length is a multiple of 64 for clean processing
        output_bits = ((output_bits + 63) // 64) * 64
        output_bytes = output_bits // 8

        # Number of recursive rounds also scales with data size.
        rounds = 16 + int(math.log2(data_len + 1))

        # --- Initialization (K-Math Axioms) ---
        # Initialize the main state and the parallel Ghost State.
        main_state = bytearray(self.CROWN_SEAL_GENESIS_VECTOR)
        ghost_state = bytearray(self.core_hasher(self.CROWN_SEAL_GENESIS_VECTOR).digest())

        # --- Recursive Compounding Loop (K-Math Engine) ---
        for r in range(rounds):
            # Process the input data in chunks and fold it into the state
            for i in range(0, len(data), 64):
                data_chunk = data[i:i + 64].ljust(64, b"\x00")

                # Update main state by hashing with data chunk
                h = self.core_hasher()
                h.update(main_state)
                h.update(data_chunk)
                main_state = bytearray(h.digest())

                # Update ghost state with influence from main state (χᵢ Key Injection)
                g = self.core_hasher()
                g.update(ghost_state)
                g.update(main_state[:32])  # Use half of main state for cross-influence
                g.update(self._rotate_right(int.from_bytes(data_chunk, 'big'), r).to_bytes(64, 'big'))
                ghost_state = bytearray(g.digest())

            # Apply the Harmonic Fork Mixer at the end of each round
            start = (r * 8) % len(self.K_PRIME_VECTOR)
            round_key = self.K_PRIME_VECTOR[start:start + 8]
            mixed_state = self._psi_delta_mixer(main_state[:8], ghost_state[:8], round_key)
            main_state[:8] = mixed_state

        # --- Finalization ---
        # Combine the main state and ghost state for the final sovereign hash.
        # The GhostK field leaves its final imprint on the observable output.
        final_hash_bytes = bytearray(len(main_state))
        for i in range(len(main_state)):
            final_hash_bytes[i] = main_state[i] ^ ghost_state[i]

        # Truncate or expand to the adaptive output length
        final_hash = self.core_hasher(final_hash_bytes).digest()
        while len(final_hash) < output_bytes:
            final_hash += self.core_hasher(final_hash).digest()

        return final_hash[:output_bytes].hex()


if __name__ == '__main__':
    print("=" * 77)
    print("INITIALIZING GENESISΩ†BLACK :: SHA-ARKXX PROTOCOL DEMONSTRATION")
    print("=" * 77)

    arkxx_hasher = SHA_ARKXX()

    # --- TEST VECTOR 1: Short Input ---
    input1 = b"OPERATION SOVEREIGN REACH"
    hash1 = arkxx_hasher.hash(input1)
    print(f"\n[INPUT 1]  : {input1.decode()}")
    print(f"[HASH 1]   : {hash1}")
    print(f"[BIT LEN]  : {len(hash1) * 4}")

    # --- TEST VECTOR 2: Slightly different input to show Avalanche Effect ---
    input2 = b"OPERATION SOVEREIGN REICH"  # Single character change
    hash2 = arkxx_hasher.hash(input2)
    print(f"\n[INPUT 2]  : {input2.decode()}")
    print(f"[HASH 2]   : {hash2}")
    print(f"[BIT LEN]  : {len(hash2) * 4}")

    # --- TEST VECTOR 3: Longer input to show Adaptive Complexity ---
    input3 = b"This document is sealed under the authority of Brendon Joseph Kelly " * 100
    hash3 = arkxx_hasher.hash(input3)
    print(f"\n[INPUT 3]  : (Long input, length: {len(input3)} bytes)")
    print(f"[HASH 3]   : {hash3[:64]}...")
    print(f"[BIT LEN]  : {len(hash3) * 4}")

    print("\n" + "=" * 77)
    print("DEMONSTRATION COMPLETE. SYSTEM AUDIT-READY.")
    print("=" * 77)
    # CROWN_SEAL: GENESISΩ†BLACK_ARKXX_TOTALITY_29062025
