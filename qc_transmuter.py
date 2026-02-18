"""QCIT: Quantum-to-Classical Information Transmuter.
Prototype-only: accepts complex amplitudes (statevector proxy), samples outcomes,
emits classical summary metrics.
API: transmute_state(amplitudes, shots=4096, top_k=8, seed=None)
"""

from __future__ import annotations

import argparse, cmath, json, math, random
from typing import Any, Dict, List, Optional, Sequence, Tuple

def _as_complex(v: Any) -> complex:
    if isinstance(v, complex):
        return v
    if isinstance(v, (list, tuple)) and len(v) == 2:
        return complex(float(v[0]), float(v[1]))
    return complex(v)

def _to_complex_list(amplitudes: Any) -> List[complex]:
    if isinstance(amplitudes, dict):
        items = sorted(((int(k), v) for k, v in amplitudes.items()), key=lambda x: x[0])
        return [_as_complex(v) for _, v in items]
    if isinstance(amplitudes, (list, tuple)):
        return [_as_complex(v) for v in amplitudes]
    raise TypeError("amplitudes must be list/tuple or dict")


def _normalize_state(state: Sequence[complex]) -> List[complex]:
    if not state:
        raise ValueError("statevector must be non-empty")
    norm2 = sum(abs(a) ** 2 for a in state)
    if norm2 <= 0.0:
        raise ValueError("statevector has zero norm")
    inv = 1.0 / math.sqrt(norm2)
    return [a * inv for a in state]


def _probabilities(state: Sequence[complex]) -> List[float]:
    probs = [float(abs(a) ** 2) for a in state]
    s = sum(probs)
    if s <= 0.0:
        raise ValueError("probability sum is zero")
    return [p / s for p in probs]

def _entropy_nats(probs: Sequence[float], eps: float = 1e-15) -> float:
    ent = 0.0
    for p in probs:
        if p > eps:
            ent -= p * math.log(p)
    return float(ent)


def _circular_mean(phases: Sequence[float], weights: Sequence[float]) -> float:
    x = sum(w * math.cos(a) for a, w in zip(phases, weights))
    y = sum(w * math.sin(a) for a, w in zip(phases, weights))
    return 0.0 if (x == 0.0 and y == 0.0) else math.atan2(y, x)


def _coherence_metric(state: Sequence[complex]) -> float:
    s = sum(state)
    den = sum(abs(a) ** 2 for a in state)
    return 0.0 if den <= 0.0 else float((abs(s) ** 2) / den)

def _sample_counts(probs: Sequence[float], shots: int, rng: random.Random) -> Dict[int, int]:
    if shots <= 0:
        raise ValueError("shots must be > 0")
    idx = list(range(len(probs)))
    draws = rng.choices(idx, weights=probs, k=shots)
    counts: Dict[int, int] = {}
    for i in draws:
        counts[i] = counts.get(i, 0) + 1
    return counts


def transmute_state(amplitudes: Any, shots: int = 4096, top_k: int = 8, seed: Optional[int] = None) -> Dict[str, Any]:
    state = _normalize_state(_to_complex_list(amplitudes))
    probs = _probabilities(state)
    rng = random.Random(seed)
    counts = _sample_counts(probs, shots, rng)

    phases = [cmath.phase(a) for a in state]
    mean_phase = _circular_mean(phases, probs)
    ent_nats = _entropy_nats(probs)
    ent_bits = ent_nats / math.log(2.0)

    top = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:max(1, top_k)]
    top_out = [
        {"index": int(i), "count": int(c), "freq": float(c)/float(shots), "p": float(probs[i])}
        for i, c in top
    ]

    return {
        "inputs": {"num_states": len(state), "shots": int(shots), "seed": seed, "top_k": int(top_k)},
        "outputs": {
            "probabilities": probs,
            "counts": {str(i): int(c) for i, c in sorted(counts.items())},
            "entropy_nats": float(ent_nats),
            "entropy_bits": float(ent_bits),
            "mean_phase_rad": float(mean_phase),
            "coherence": float(_coherence_metric(state)),
            "top_outcomes": top_out,
        },
    }

def _cli() -> int:
    p = argparse.ArgumentParser(description="QCIT: transmute a statevector proxy into classical metrics")
    p.add_argument("--shots", type=int, default=4096)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--top-k", type=int, default=8)
    p.add_argument("--amplitudes-json", type=str, default=None,
                   help="JSON list/dict of amplitudes; list entries can be complex-like or [re,im].")
    args = p.parse_args()

    amps = [1/math.sqrt(2), 1/math.sqrt(2)] if args.amplitudes_json is None else json.loads(args.amplitudes_json)
    report = transmute_state(amps, shots=args.shots, top_k=args.top_k, seed=args.seed)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
