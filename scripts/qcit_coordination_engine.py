#!/usr/bin/env python3
"""QCIT Coordination Engine.

Translates uncoordinated domain vectors (energy/information/material/consciousness)
into a coordinated state and validation digest for downstream orchestration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class QcitVectors:
    energy: float
    information: float
    material: float
    consciousness: float


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def coordinate(v: QcitVectors) -> dict[str, float]:
    e = clamp01(v.energy)
    i = clamp01(v.information)
    m = clamp01(v.material)
    c = clamp01(v.consciousness)

    balanced_mean = (e + i + m + c) / 4
    dispersion = ((e - balanced_mean) ** 2 + (i - balanced_mean) ** 2 + (m - balanced_mean) ** 2 + (c - balanced_mean) ** 2) / 4
    coordination_score = round(max(0.0, balanced_mean - dispersion), 6)

    return {
        "balanced_mean": round(balanced_mean, 6),
        "dispersion": round(dispersion, 6),
        "coordination_score": coordination_score,
        "integrated_energy": round(coordination_score * (1 + e) / 2, 6),
        "integrated_information": round(coordination_score * (1 + i) / 2, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run QCIT coordination engine")
    parser.add_argument("--energy", type=float, default=0.82)
    parser.add_argument("--information", type=float, default=0.84)
    parser.add_argument("--material", type=float, default=0.79)
    parser.add_argument("--consciousness", type=float, default=0.87)
    parser.add_argument("--out", default="docs/qcit-coordination-report.json")
    args = parser.parse_args()

    vectors = QcitVectors(
        energy=args.energy,
        information=args.information,
        material=args.material,
        consciousness=args.consciousness,
    )

    outputs = coordinate(vectors)
    digest_seed = json.dumps({"vectors": asdict(vectors), "outputs": outputs}, sort_keys=True).encode("utf-8")
    validation_digest = hashlib.sha256(digest_seed).hexdigest()

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "engine": "qcit-coordination-engine",
        "vectors": asdict(vectors),
        "outputs": outputs,
        "validation_digest_sha256": validation_digest,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
