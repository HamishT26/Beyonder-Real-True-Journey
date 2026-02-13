"""
qc_transmuter.py
----------------

Minimal Quantum-to-Classical Information Transmuter (QCIT) helper.

This module provides a lightweight, dependency-free bridge from a list of
quantum amplitudes to compact classical features suitable for orchestrator
pipelines and logs.
"""

from __future__ import annotations

import math
import random
from typing import Dict, Iterable, List


def _normalize_probabilities(amplitudes: Iterable[complex]) -> List[float]:
    probabilities = [abs(amplitude) ** 2 for amplitude in amplitudes]
    total = sum(probabilities)
    if total <= 0:
        return []
    return [value / total for value in probabilities]


def _sample_counts(probabilities: List[float], shots: int) -> List[int]:
    if shots <= 0 or not probabilities:
        return [0] * len(probabilities)
    indices = list(range(len(probabilities)))
    draws = random.choices(indices, weights=probabilities, k=shots)
    counts = [0] * len(probabilities)
    for index in draws:
        counts[index] += 1
    return counts


def _entropy_bits(distribution: List[float]) -> float:
    return -sum(p * math.log2(p) for p in distribution if p > 0.0)


def transmute_state(amplitudes: Iterable[complex], shots: int = 512) -> Dict[str, object]:
    """
    Convert quantum amplitudes into compact classical summary features.

    Args:
        amplitudes: Complex amplitudes describing a quantum state.
        shots: Number of sampling shots used for empirical frequencies.

    Returns:
        A dictionary of classical features that can be fed into downstream
        classical modules.
    """
    probabilities = _normalize_probabilities(amplitudes)
    if not probabilities:
        return {
            "num_states": 0,
            "shots": max(0, int(shots)),
            "dominant_state": None,
            "dominant_probability": 0.0,
            "entropy_bits": 0.0,
            "top_states": [],
            "empirical_top_states": [],
        }

    shots = max(0, int(shots))
    dominant_index = max(range(len(probabilities)), key=probabilities.__getitem__)
    entropy = _entropy_bits(probabilities)

    ranked = sorted(
        [{"state": i, "probability": float(p)} for i, p in enumerate(probabilities)],
        key=lambda row: row["probability"],
        reverse=True,
    )
    top_states = ranked[:3]

    counts = _sample_counts(probabilities, shots)
    empirical_ranked = sorted(
        [
            {
                "state": i,
                "count": count,
                "frequency": float(count / shots) if shots > 0 else 0.0,
            }
            for i, count in enumerate(counts)
        ],
        key=lambda row: row["frequency"],
        reverse=True,
    )

    return {
        "num_states": len(probabilities),
        "shots": shots,
        "dominant_state": dominant_index,
        "dominant_probability": float(probabilities[dominant_index]),
        "entropy_bits": float(entropy),
        "top_states": top_states,
        "empirical_top_states": empirical_ranked[:3],
    }
