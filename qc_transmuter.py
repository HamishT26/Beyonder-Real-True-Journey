"""
qc_transmuter.py
----------------

Minimal Quantum-to-Classical Information Transmuter (QCIT) helper.
Converts complex amplitudes into deterministic classical features.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List


def _normalize_probabilities(amplitudes: Iterable[complex]) -> List[float]:
    probabilities = [abs(amplitude) ** 2 for amplitude in amplitudes]
    total = sum(probabilities)
    if total <= 0.0:
        return []
    return [value / total for value in probabilities]


def _entropy_bits(distribution: List[float]) -> float:
    return -sum(p * math.log2(p) for p in distribution if p > 0.0)


def _deterministic_histogram(probabilities: List[float], shots: int) -> List[int]:
    histogram = [int(round(p * shots)) for p in probabilities]
    delta = shots - sum(histogram)
    if histogram and delta != 0:
        histogram[0] += delta
    return histogram


def transmute_state(amplitudes: Iterable[complex], shots: int = 512) -> Dict[str, object]:
    """
    Convert quantum amplitudes into compact classical summary features.
    """
    probabilities = _normalize_probabilities(amplitudes)
    shots = max(1, int(shots))

    if not probabilities:
        return {
            "num_states": 0,
            "shots": shots,
            "dominant_state": None,
            "dominant_probability": 0.0,
            "entropy_bits": 0.0,
            "top_states": [],
            "empirical_top_states": [],
            "expected_state_index": 0.0,
            "measurement_histogram": [],
        }

    dominant_index = max(range(len(probabilities)), key=probabilities.__getitem__)
    entropy = _entropy_bits(probabilities)
    expected_state = sum(idx * p for idx, p in enumerate(probabilities))

    ranked = sorted(
        [{"state": i, "probability": float(p)} for i, p in enumerate(probabilities)],
        key=lambda row: row["probability"],
        reverse=True,
    )
    top_states = ranked[: min(4, len(ranked))]

    histogram = _deterministic_histogram(probabilities, shots)
    empirical_ranked = sorted(
        [
            {
                "state": i,
                "count": count,
                "frequency": float(count / shots),
            }
            for i, count in enumerate(histogram)
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
        "empirical_top_states": empirical_ranked[: min(4, len(empirical_ranked))],
        "expected_state_index": float(expected_state),
        "measurement_histogram": histogram,
    }
