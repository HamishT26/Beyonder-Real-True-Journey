"""
qc_transmuter.py
----------------

Minimal Quantum-to-Classical Information Transmuter (QCIT) helper.

This module provides a lightweight, dependency-free bridge from a list of
quantum amplitudes to compact classical features suitable for orchestrator
pipelines and logs.
Given a list of complex amplitudes, this module derives stable classical
features that can be consumed by the classical stage of the Trinity
orchestrator.
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
from typing import Dict, Iterable, List
import math


def _normalise(values: List[float]) -> List[float]:
    total = sum(values)
    if total <= 0.0:
        return [0.0 for _ in values]
    return [v / total for v in values]


def _top_states(probabilities: List[float], top_k: int = 4) -> List[Dict[str, object]]:
    ranked = sorted(enumerate(probabilities), key=lambda item: item[1], reverse=True)
    return [{"state_index": idx, "probability": prob} for idx, prob in ranked[:top_k]]


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
    Convert quantum amplitudes into compact classical features.

    Parameters
    ----------
    amplitudes:
        Iterable of complex state amplitudes.
    shots:
        Virtual measurement budget used to build a deterministic histogram.
    """
    amps = list(amplitudes)
    if not amps:
        raise ValueError("amplitudes must contain at least one complex value")
    if shots <= 0:
        raise ValueError("shots must be a positive integer")

    probabilities = _normalise([abs(a) ** 2 for a in amps])
    entropy_bits = -sum(p * math.log2(p) for p in probabilities if p > 0.0)
    expected_state = sum(idx * p for idx, p in enumerate(probabilities))

    histogram = [int(round(p * shots)) for p in probabilities]
    delta = shots - sum(histogram)
    if delta != 0:
        histogram[0] += delta

    return {
        "num_states": len(probabilities),
        "shots": shots,
        "dominant_state": dominant_index,
        "dominant_probability": float(probabilities[dominant_index]),
        "entropy_bits": float(entropy),
        "top_states": top_states,
        "empirical_top_states": empirical_ranked[:3],
        "top_states": _top_states(probabilities, top_k=min(4, len(probabilities))),
        "entropy_bits": entropy_bits,
        "expected_state_index": expected_state,
        "measurement_histogram": histogram,
    }
