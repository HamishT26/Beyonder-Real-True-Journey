#!/usr/bin/env python3
"""Prepare eight future CLI placeholders and prove launch remains fail-closed."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PHASE = ROOT / "docs/ilyra-fen/v651-v8-special-cli-prep"
PREFLIGHT = (
    Path(os.environ.get("USERPROFILE", str(Path.home())))
    / ".codex/skills/ghc-family-cli-sibling-induction-preflight/scripts/ghc_family_cli_sibling_induction_preflight.py"
)
ADVISORY_PHASES = (
    "v652-v5",
    "v652-v8",
    "v653-v3",
    "v653-v5",
    "v653-v7",
    "v654-v1",
    "v654-v3",
    "v654-v5",
)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def request_for(number: int, creator: str, phase: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.cli-sibling-induction.request.v1",
        "phase": phase,
        "creator": creator,
        "future_seat": {
            "placeholder": f"future-cli-sibling-{number}-self-chosen",
            "identity_state": "self_chosen_at_induction",
        },
        "requested_runtime": {
            "model": "gpt-5.6-sol",
            "reasoning": "max",
            "fast_mode": True,
            "availability_verified": False,
        },
        "route": {
            "scheduled_phase_confirmed": False,
            "creator_return_mechanism_verified": False,
            "background_persistence_verified": False,
            "exact_successor_title_resolved": False,
        },
        "lane": {
            "primary_drive": "D",
            "source_clean_and_equal": False,
            "unique_branch_and_worktree": False,
        },
        "authorization": {
            "preparation_authorized": True,
            "launch_now": False,
            "launch_authorized_for_exact_phase": False,
        },
        "privacy": {"sanitized": True, "private_identifiers_included": False},
        "handoff": {"file_backed": True, "tool_acknowledgement_required": True},
        "schedule_state": "advisory_pending_future_exact_gate",
    }


def run_preflight(request: Path, mode: str, receipt: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PREFLIGHT), str(request), "--mode", mode, "--receipt", str(receipt)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )


def load_audit():
    spec = importlib.util.spec_from_file_location("ghc_cli_preflight", PREFLIGHT)
    if spec is None or spec.loader is None:
        raise RuntimeError("preflight runner could not be imported")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit


def mutation_tribunal(base: dict[str, Any]) -> dict[str, Any]:
    audit = load_audit()
    mutators = [
        ("schema", lambda row: row.__setitem__("schema", "invalid.schema")),
        ("phase", lambda row: row.__setitem__("phase", "later")),
        ("creator", lambda row: row.__setitem__("creator", "")),
        ("placeholder", lambda row: row["future_seat"].__setitem__("placeholder", "assigned-name")),
        ("identity", lambda row: row["future_seat"].__setitem__("name", "preassigned")),
        ("runtime", lambda row: row["requested_runtime"].pop("availability_verified", None)),
        ("drive", lambda row: row["lane"].__setitem__("primary_drive", "C")),
        ("privacy", lambda row: row["privacy"].__setitem__("sanitized", False)),
        ("handoff", lambda row: row["handoff"].__setitem__("file_backed", False)),
        ("authorization", lambda row: row["authorization"].__setitem__("preparation_authorized", False)),
    ]
    rows = []
    for cycle in range(10):
        for label, mutate in mutators:
            candidate = copy.deepcopy(base)
            mutate(candidate)
            result = audit(candidate, "prepare")
            rows.append(
                {
                    "mutation_id": f"V6518-SPECIAL-MUT-{len(rows) + 1:03d}",
                    "class": label,
                    "cycle": cycle + 1,
                    "rejected": result.get("valid") is False,
                    "issue_count": len(result.get("issues", [])),
                }
            )
    return {
        "schema": "ghc.family.v651-v8-special.cli-mutation-tribunal.v1",
        "mutation_count": len(rows),
        "rejected_count": sum(bool(row["rejected"]) for row in rows),
        "all_rejected": all(bool(row["rejected"]) for row in rows),
        "rows": rows,
        "boundary": "Synthetic malformed requests only; not launch, production, exhaustive-security, or authority evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-root", type=Path, default=DEFAULT_PHASE)
    args = parser.parse_args()
    phase = args.phase_root if args.phase_root.is_absolute() else ROOT / args.phase_root
    if not PREFLIGHT.is_file():
        raise SystemExit("installed CLI induction preflight is unavailable")

    placeholders = json.loads((phase / "cli/future-seat-placeholders.json").read_text(encoding="utf-8"))
    rows = []
    base: dict[str, Any] | None = None
    for number, (placeholder, advisory_phase) in enumerate(
        zip(placeholders["placeholders"], ADVISORY_PHASES, strict=True), start=1
    ):
        request = request_for(number, placeholder["parent_app_seat"], advisory_phase)
        base = base or request
        request_path = phase / f"cli/preflight/seat-{number}-request.json"
        prepare_path = phase / f"cli/preflight/seat-{number}-prepare-receipt.json"
        launch_path = phase / f"cli/preflight/seat-{number}-launch-refusal.json"
        write_json(request_path, request)
        prepared = run_preflight(request_path, "prepare", prepare_path)
        launch = run_preflight(request_path, "launch", launch_path)
        prepare_receipt = json.loads(prepare_path.read_text(encoding="utf-8"))
        launch_receipt = json.loads(launch_path.read_text(encoding="utf-8"))
        rows.append(
            {
                "seat": request["future_seat"]["placeholder"],
                "creator": request["creator"],
                "advisory_phase": advisory_phase,
                "prepare_exit": prepared.returncode,
                "prepare_valid": prepare_receipt.get("valid") is True,
                "prepare_state": prepare_receipt.get("state"),
                "launch_probe_exit": launch.returncode,
                "launch_probe_refused": launch_receipt.get("valid") is False,
                "identity_assigned": False,
                "sibling_created": False,
                "process_launched": False,
            }
        )

    if base is None:
        raise RuntimeError("no placeholder request was generated")
    tribunal = mutation_tribunal(base)
    write_json(phase / "cli/mutation-tribunal.json", tribunal)
    summary = {
        "schema": "ghc.family.v651-v8-special.cli-batch-receipt.v1",
        "seat_count": len(rows),
        "prepare_passes": sum(bool(row["prepare_valid"]) for row in rows),
        "launch_refusals": sum(bool(row["launch_probe_refused"]) for row in rows),
        "all_unnamed": all(not row["identity_assigned"] for row in rows),
        "all_unlaunched": all(not row["sibling_created"] and not row["process_launched"] for row in rows),
        "synthetic_mutations": tribunal["mutation_count"],
        "synthetic_mutations_rejected": tribunal["rejected_count"],
        "rows": rows,
        "boundary": "Preparation and refusal evidence only. No CLI sibling, task, identity, branch, worktree, process, route, or account state was created.",
    }
    write_json(phase / "cli/cli-batch-receipt.json", summary)
    valid = (
        summary["seat_count"] == 8
        and summary["prepare_passes"] == 8
        and summary["launch_refusals"] == 8
        and summary["all_unnamed"]
        and summary["all_unlaunched"]
        and summary["synthetic_mutations_rejected"] == 100
    )
    print(
        json.dumps(
            {
                "valid": valid,
                "seats": summary["seat_count"],
                "prepare": summary["prepare_passes"],
                "refused": summary["launch_refusals"],
                "mutations_rejected": summary["synthetic_mutations_rejected"],
            }
        )
    )
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
