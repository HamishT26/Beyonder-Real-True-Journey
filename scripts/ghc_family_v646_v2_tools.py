#!/usr/bin/env python3
"""Family-current runner implementations for Ilyra Fen v646-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

from ghc_family_v646_v2_runtime import evidence_dag_closure, run as run_core


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v2"
X1 = "df5dd03db76936d6ad6484eda36960a44c5e4b0b"
BOUNDARY = "Bounded same-owner structural evidence only; no empirical, authority, production, exhaustive-assurance, independent-reproduction, or Stage 20 credit."


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def source_status_drift_guard() -> dict[str, Any]:
    ledger = load("sources/source-ledger.json")
    rows = ledger.get("sources", [])
    allowed = {"current", "stable", "draft", "watch"}
    checks = [
        len(rows) == 18,
        all(row.get("status") in allowed for row in rows),
        all(str(row.get("url", "")).startswith("https://") or (row.get("url") is None and "local skill" in str(row.get("authority", "")).casefold()) for row in rows),
        bool(ledger.get("checked_on")),
        all(row.get("use") for row in rows),
        sum(ledger.get(key, 0) for key in ("real_data_rows_ingested", "likelihood_evaluations", "real_participants", "real_keys_or_proofs")) == 0,
    ]
    return {"runner": "source-status-drift-guard", "checks": len(checks), "passed": all(checks), "source_count": len(rows), "statuses": sorted({row.get("status") for row in rows}), "boundary": BOUNDARY}


def proposal_neighbor_quarantine() -> dict[str, Any]:
    audit = load("provenance/prior-proposal-collision-audit.json")
    index = load("provenance/frozen-chain-proposal-index.json")
    rows = audit.get("comparisons", [])
    checks = [
        audit.get("prior_frozen_proposal_count") == 400,
        audit.get("new_proposal_count") == 10,
        audit.get("exact_title_collision_count") == 0,
        len(rows) == 10,
        all(row.get("manual_result") == "distinct" for row in rows),
        index.get("frozen_chain_count_after_x1") == 410,
    ]
    return {"runner": "proposal-neighbor-quarantine", "checks": len(checks), "passed": all(checks), "comparisons": len(rows), "frozen_after_x1": index.get("frozen_chain_count_after_x1"), "boundary": BOUNDARY}


def logical_manifest_parity() -> dict[str, Any]:
    manifest = load("validation/x1-staged-manifest.json")
    mismatches = []
    for row in manifest.get("entries", []):
        result = subprocess.run(["git", "show", f"{X1}:{row['path']}"], cwd=ROOT, capture_output=True)
        if result.returncode:
            mismatches.append({"path": row["path"], "reason": "missing_from_x1"})
            continue
        observed = hashlib.sha256(result.stdout).hexdigest()
        if observed != row.get("sha256"):
            mismatches.append({"path": row["path"], "reason": "hash_mismatch"})
    checks = len(manifest.get("entries", [])) + 2
    return {"runner": "logical-manifest-parity", "checks": checks, "passed": manifest.get("entry_count") == len(manifest.get("entries", [])) and not mismatches, "entry_count": manifest.get("entry_count"), "mismatches": mismatches, "hash_domain": manifest.get("hash_domain"), "boundary": BOUNDARY}


def method_state_preflight() -> dict[str, Any]:
    ledger = load("method-flow/method-flow-state.json")
    methods = ledger.get("methods", [])
    witnesses = ledger.get("witnesses", [])
    ids = [row.get("method_id") for row in methods]
    witness_ids = [row.get("witness_id") for row in witnesses]
    failed = [row for row in witnesses if row.get("result") == "fail"]
    checks = [
        len(ids) == len(set(ids)),
        len(witness_ids) == len(set(witness_ids)),
        all(row.get("retained_negative_ids") for row in failed),
        all(row.get("recommendation_state") in {"preferred", "deprecated", "superseded"} for row in methods),
        all(row.get("independent_reproduction") is False for row in witnesses),
        len(failed) >= 1,
    ]
    return {"runner": "method-state-preflight", "checks": len(checks), "passed": all(checks), "method_count": len(methods), "witness_count": len(witnesses), "failed_witness_count": len(failed), "boundary": BOUNDARY}


def terminal_route_guard() -> dict[str, Any]:
    route = load("orchestration/terminal-route-plan.json")
    update = load("orchestration/phase-update.json")
    checks = [
        route.get("current_state") == "PREPARED_NOT_SENT",
        route.get("send_count") == 0,
        route.get("target_title") == "Sable Rook",
        route.get("target_phase") == "v646-v3",
        update.get("terminal_route") == "PREPARED_NOT_SENT",
        update.get("standby_contact_count") == 0,
        update.get("no_task_creation") is True,
        update.get("no_delegation") is True,
    ]
    return {"runner": "terminal-route-guard", "checks": len(checks), "passed": all(checks), "state": route.get("current_state"), "send_count": route.get("send_count"), "boundary": BOUNDARY}


def evidence_dag_runner() -> dict[str, Any]:
    return evidence_dag_closure()


def core_runner() -> dict[str, Any]:
    names = [
        "evidence-dag", "schwinger-keldysh", "microscope-zero-row", "seismic-handover",
        "haip-profile", "earthquake-authority", "sqlite-wal", "svg-chart", "hatano-sasa", "registered-report",
    ]
    rows = {name: run_core(name, Path("D:/GHC-Family-Scratch/v646-v2-runtime")) for name in names}
    return {"runner": "v646-v2-core-runner", "checks": sum(row.get("checks", 0) for row in rows.values()), "passed": all(row.get("passed") for row in rows.values()), "core_count": len(rows), "results": rows, "boundary": BOUNDARY}


def portfolio_runner() -> dict[str, Any]:
    safe = load("approval-packets/x2-safe-now-execution.json")
    candidates = load("prototypes/x2-candidate-execution.json")
    cleanup = load("maintenance/x2-clean-refine-ledger.json")
    checks = [
        len(safe.get("tasks", [])) == 30,
        all(row.get("state") == "completed" for row in safe.get("tasks", [])),
        len(candidates.get("tasks", [])) == 20,
        all(row.get("state") == "completed" for row in candidates.get("tasks", [])),
        len(cleanup.get("tasks", [])) == 30,
        all(row.get("state") == "completed" for row in cleanup.get("tasks", [])),
        safe.get("unsafe_reclassification_count") == 0,
        candidates.get("production_claims") == 0,
        cleanup.get("destructive_actions") == 0,
    ]
    return {"runner": "v646-v2-portfolio-runner", "checks": len(checks), "passed": all(checks), "safe": 30, "candidates": 20, "cleanup": 30, "boundary": BOUNDARY}


def skill_runner() -> dict[str, Any]:
    receipt = load("prototypes/skill-build-receipt.json")
    checks = [
        receipt.get("skill_count") == 20,
        receipt.get("validated_count") == 20,
        receipt.get("smoke_use_pass_count") == 20,
        receipt.get("newly_initialized_count") == 19,
        receipt.get("compatible_reused_count") == 1,
        receipt.get("valid") is True,
    ]
    return {"runner": "v646-v2-skill-runner", "checks": len(checks), "passed": all(checks), "skill_count": receipt.get("skill_count"), "validated": receipt.get("validated_count"), "smoke_used": receipt.get("smoke_use_pass_count"), "boundary": BOUNDARY}


def validation_runner() -> dict[str, Any]:
    from ghc_family_v646_v2_validator import validate
    return validate(mode="minimal", revision=None, require_clean=False)


TOOLS: dict[str, Callable[[], dict[str, Any]]] = {
    "source-status": source_status_drift_guard,
    "proposal-neighbor": proposal_neighbor_quarantine,
    "logical-manifest": logical_manifest_parity,
    "method-preflight": method_state_preflight,
    "terminal-route": terminal_route_guard,
    "evidence-dag": evidence_dag_runner,
    "core": core_runner,
    "portfolio": portfolio_runner,
    "skill": skill_runner,
    "validation": validation_runner,
}


def main_for(name: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = TOOLS[name]()
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if payload.get("passed") or payload.get("valid") else 1
