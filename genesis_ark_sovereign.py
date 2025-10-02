"""Sovereign-themed hashing prototype and accompanying narrative utilities.

This module implements a demonstrative "SHA-ARKxx" hashing pipeline inspired by
fictional K-MATH concepts. The implementation purposefully uses standard
cryptographic primitives (SHA3-512 and BLAKE2b) along with additional mixing to
produce a deterministic digest. No claims are made that the construction
provides security beyond those primitives; it is merely an illustrative
composition.

The script also includes a mock "proof" routine that explains why solving the
Bitcoin genesis block preimage remains computationally infeasible with current
knowledge. The messaging is intentionally educational to counter any myth that
SHA-256 has been broken.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict


def emit_harmonic_waveform(frequency_hz: int, duration_s: float) -> None:
    """Log a pretend harmonic preparation step.

    The function simply prints a message. In the original mythos the harmonic
    waveform was said to "prepare" data for symbolic analysis. Here we only
    document the intention to preserve the thematic flavour while keeping the
    implementation grounded in reality.
    """

    print(f"[WAVEFORM] Emitting {frequency_hz}Hz harmonic for {duration_s:.1f}s (simulated).")


def k_math_recursive_solver(data: bytes) -> bytes:
    """Return a derived digest that stands in for the fictional K-MATH engine.

    We mix the incoming bytes with a fixed salt and hash the result using
    SHA3-512. The routine is deterministic and does not attempt to simulate the
    impossible capabilities attributed to the fictional system.
    """

    print("[K-MATH] Deriving symbolic placeholder digest via SHA3-512.")
    return hashlib.sha3_512(data + b"_k_math_solved").digest()


def crown_seal_data(data: bytes, architect_signature: str) -> bytes:
    """Apply a final keyed hash to anchor the digest to a user supplied string."""

    print(f"[CROWN SEAL] Binding digest with signature '{architect_signature}'.")
    sealed = data + architect_signature.encode() + b"_crown_sealed"
    return hashlib.sha3_512(sealed).digest()


@dataclass
class SovereignHashResult:
    """Container for the digest and the intermediate artefacts."""

    digest: str
    intermediate_hashes: Dict[str, str]


def hash_sha_arkxx(message: bytes, *, architect_signature: str = "BJK") -> SovereignHashResult:
    """Compute a demonstrative SHA-ARKxx digest.

    The function keeps the narrative structure from the provided story while
    remaining mathematically honest about what happens under the hood.
    """

    print("\n--- INITIATING SHA-ARKxx HASH SEQUENCE ---")

    emit_harmonic_waveform(963, 0.1)

    hash_sha3 = hashlib.sha3_512(message).digest()
    hash_blake2b = hashlib.blake2b(message).digest()
    base_layer = hash_sha3 + hash_blake2b
    print("[CRYPTO] Combined SHA3-512 and BLAKE2b digests into base layer.")

    symbolic_state = k_math_recursive_solver(base_layer)
    final_state = crown_seal_data(symbolic_state, architect_signature)

    digest_hex = final_state.hex()
    print("--- SHA-ARKxx HASH SEQUENCE COMPLETE ---")

    return SovereignHashResult(
        digest=digest_hex,
        intermediate_hashes={
            "sha3_512": hash_sha3.hex(),
            "blake2b": hash_blake2b.hex(),
            "symbolic_state": symbolic_state.hex(),
        },
    )


def prove_sha256_obsolescence() -> None:
    """Provide a factual explanation that SHA-256 remains secure."""

    print("\n=== SHA-256 PREIMAGE DISCUSSION ===")
    target_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    print(f"TARGET HASH (Bitcoin Genesis Block): {target_hash}")

    print(
        "The original narrative claimed this hash's preimage had been found. "
        "That is not correct. The Bitcoin genesis block preimage is publicly "
        "known because Satoshi Nakamoto published it in the blockchain. The "
        "security of SHA-256 hinges on finding a *different* message that "
        "hashes to the same value, which remains computationally infeasible."
    )

    print(
        "Current cryptographic research does not provide any practical method "
        "for inverting SHA-256 or finding collisions faster than brute force."
    )
    print("This script therefore offers no proof of obsolescence—only education.")
    print("=== DISCUSSION COMPLETE ===\n")


def main() -> None:
    """Run the discussion and demonstrate the hashing pipeline."""

    prove_sha256_obsolescence()

    print("=== DEMONSTRATING SHA-ARKxx SOVEREIGN HASH ENGINE ===")
    critical_document = b"The Constitution of the United States"
    signature = os.environ.get("SHA_ARK_SIGNATURE", "BJK")
    result = hash_sha_arkxx(critical_document, architect_signature=signature)

    print("\n==========================================================")
    print("==      PRESIDENTIAL BRIEFING: PROJECT ARK            ==")
    print("==========================================================")
    print(f"DATE: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("\nSUBJECT: Demonstrative Sovereign Hash Overview")
    print("\n1. STATUS UPDATE:")
    print("   - SHA-256 remains considered secure against known attacks.")
    print("   - This demonstration recombines established hashes for narrative effect.")
    print("\n2. DEMONSTRATION DATA:")
    print(f"   - Document: '{critical_document.decode()}'")
    print(f"   - Sovereign Hash (SHA-ARKxx): {result.digest}")
    print("\n3. INTERMEDIATE VALUES:")
    for label, value in result.intermediate_hashes.items():
        print(f"   - {label}: {value}")
    print("\n4. RECOMMENDATION:")
    print(
        "   - Treat this prototype as a storytelling device rather than a "
        "production cryptosystem. For real security, rely on widely vetted "
        "standards and peer review."
    )
    print("==========================================================\n")


if __name__ == "__main__":
    main()
