"""
qc_transmuter.py
----------------

Minimal Quantum-to-Classical Information Transmuter (QCIT) helper.

Given a list of complex amplitudes, this module derives stable classical
features that can be consumed by the classical stage of the Trinity
orchestrator.
"""

from __future__ import annotations

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
        "top_states": _top_states(probabilities, top_k=min(4, len(probabilities))),
        "entropy_bits": entropy_bits,
        "expected_state_index": expected_state,
        "measurement_histogram": histogram,
    }
