#!/usr/bin/env python3
"""Standard-library-only second oracle for committed GHC boundary evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify(phase_dir: Path, output: Path | None = None) -> dict[str, Any]:
    failures: list[str] = []

    def require(condition: bool, label: str) -> None:
        if not condition:
            failures.append(label)

    x1 = read(phase_dir / "x1-proposals.json")
    sources = read(phase_dir / "sources/source-ledger.json")
    x2 = read(phase_dir / "x2-proposal-ledger.json")
    negatives = read(phase_dir / "retained-negative-register.json")
    gates = read(phase_dir / "exact-open-gate-register.json")
    truth = read(phase_dir / "phase-truth.json")
    terminal = read(phase_dir / "stage20/terminal-verdict.json")
    manifest = read(phase_dir / "reproduction/manifest.json")

    require(len(x1["proposals"]) == x1["proposal_count"] == 10, "proposal count")
    require(len({row["proposal_id"] for row in x1["proposals"]}) == 10, "proposal id uniqueness")
    source_ids = {row["source_id"] for row in sources["sources"]}
    referenced = {ref for row in x1["proposals"] for ref in row["authoritative_source_needs"]}
    require(not (referenced - source_ids), "source reference resolution")
    require(len(sources["sources"]) == sources["source_count"] == 34, "source count")

    disposition_counts = dict(Counter(row["observed_disposition"] for row in x2["proposals"]))
    require(disposition_counts == x2["disposition_counts"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, "disposition counts")
    require(x2["x1_commit"] == "4785eae506ec19152b282297e496ff7f0209fa2e", "x1 commit")
    require(x2["source_revision"] == "62f35540964e964760fdf10c7acf580f320dcd29", "source revision")

    require((negatives["inherited_count"], negatives["new_count"], negatives["negative_count"]) == (32, 14, 46), "negative counts")
    require(negatives["all_retained"] and all(row["retained"] for row in negatives["negatives"]), "negative retention")
    gate_counts = Counter(row["gate_class"] for row in gates["gates"])
    require(gates["open_gap_count"] == gate_counts["open_gap"] == 5, "open gap count")
    require(gates["exact_gate_count"] == gate_counts["exact_gate"] == 6, "exact gate count")
    require(gates["silently_closed"] == 0, "silent gate closure")
    require(not any(truth["protected_claims"].values()), "protected claims")
    require(terminal["terminal_verdict"] == truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "terminal verdict")
    require(not terminal["stage20_complete"], "stage20 completion")

    actual = {rel: digest(phase_dir / rel) for rel in manifest["normalized_hashes"]}
    require(actual == manifest["normalized_hashes"], "manifest hashes")
    aggregate = hashlib.sha256("".join(f"{key}:{actual[key]}\n" for key in sorted(actual)).encode("utf-8")).hexdigest()
    require(aggregate == manifest["aggregate_sha256"], "manifest aggregate")
    require(not manifest["independent_team_reproduction"], "independent reproduction boundary")

    summary = {
        "proposal_count": x2["proposal_count"],
        "disposition_counts": x2["disposition_counts"],
        "negative_count": negatives["negative_count"],
        "open_gap_count": gates["open_gap_count"],
        "exact_gate_count": gates["exact_gate_count"],
        "terminal_verdict": terminal["terminal_verdict"],
    }
    result = {
        "schema": "ghc.family.evidence-boundary-minimal-verifier.v1",
        "runtime": "python_standard_library_only",
        "network_required": False,
        "private_route_required": False,
        "absolute_machine_path_required": False,
        "valid": not failures,
        "check_count": 17,
        "failure_count": len(failures),
        "failures": failures,
        "summary": summary,
    }
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.phase_dir.resolve(), args.output.resolve() if args.output else None)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
