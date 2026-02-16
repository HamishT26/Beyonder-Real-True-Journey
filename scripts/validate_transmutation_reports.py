#!/usr/bin/env python3
"""Validate QCIT and quantum transmutation report artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_QCIT_OUTPUTS = {
    "balanced_mean",
    "dispersion",
    "coordination_score",
    "integrated_energy",
    "integrated_information",
}

REQUIRED_QUANTUM_OUTPUTS = {
    "coordination_index",
    "translation_yield",
    "recovered_entropy",
    "net_usable_energy",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json: {path}: {exc}") from exc


def validate_required_keys(obj: dict, required: set[str], label: str) -> None:
    missing = sorted(k for k in required if k not in obj)
    if missing:
        raise SystemExit(f"{label} missing keys: {', '.join(missing)}")


def ensure_non_negative(obj: dict, keys: set[str], label: str) -> None:
    bad: list[str] = []
    for k in keys:
        v = obj.get(k)
        if not isinstance(v, (int, float)) or v < 0:
            bad.append(k)
    if bad:
        raise SystemExit(f"{label} has invalid negative/non-numeric values for: {', '.join(sorted(bad))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate QCIT and quantum transmutation reports")
    parser.add_argument("--qcit", default="docs/qcit-coordination-report.json")
    parser.add_argument("--quantum", default="docs/quantum-energy-transmutation-report.json")
    args = parser.parse_args()

    qcit = load_json(Path(args.qcit))
    quantum = load_json(Path(args.quantum))

    qcit_outputs = qcit.get("outputs")
    quantum_outputs = quantum.get("outputs")
    if not isinstance(qcit_outputs, dict):
        raise SystemExit("qcit report missing outputs object")
    if not isinstance(quantum_outputs, dict):
        raise SystemExit("quantum report missing outputs object")

    validate_required_keys(qcit_outputs, REQUIRED_QCIT_OUTPUTS, "qcit outputs")
    validate_required_keys(quantum_outputs, REQUIRED_QUANTUM_OUTPUTS, "quantum outputs")

    ensure_non_negative(qcit_outputs, REQUIRED_QCIT_OUTPUTS, "qcit outputs")
    ensure_non_negative(quantum_outputs, REQUIRED_QUANTUM_OUTPUTS, "quantum outputs")

    if qcit_outputs["coordination_score"] > 1.0:
        raise SystemExit("qcit coordination_score must be <= 1.0")
    if quantum_outputs["coordination_index"] > 1.0:
        raise SystemExit("quantum coordination_index must be <= 1.0")

    print("validated qcit and quantum transmutation reports")


if __name__ == "__main__":
    main()
