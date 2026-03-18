#!/usr/bin/env python3
"""Validate the v17 external-establishment criteria board against runtime truth."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_REQUIREMENT_STATES = {"PASS", "HOLD", "OPEN"}


def _repo_path(path_str: str) -> Path:
    resolved = (ROOT / path_str).resolve()
    resolved.relative_to(ROOT)
    return resolved


def _load_json(path_str: str, failures: list[str], label: str) -> dict[str, Any]:
    try:
        payload = json.loads(_repo_path(path_str).read_text(encoding="utf-8"))
    except FileNotFoundError:
        failures.append(f"{label} missing: {path_str}")
        return {}
    except json.JSONDecodeError as exc:
        failures.append(f"{label} invalid json: {path_str} ({exc})")
        return {}
    if not isinstance(payload, dict):
        failures.append(f"{label} must decode to an object: {path_str}")
        return {}
    return payload


def _status(failures: list[str], warnings: list[str]) -> str:
    if failures:
        return "FAIL"
    if warnings:
        return "WARN"
    return "PASS"


def _check(name: str, ok: bool, success_detail: str, failure_detail: str, failures: list[str]) -> dict[str, str]:
    if ok:
        return {"name": name, "status": "PASS", "detail": success_detail}
    failures.append(failure_detail)
    return {"name": name, "status": "FAIL", "detail": failure_detail}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the v17 external-establishment criteria board.")
    parser.add_argument("--criteria-board", default="docs/v17-external-establishment-criteria-board-v1.json")
    parser.add_argument("--runtime-validation", default="docs/v17-runtime-session-validation-latest.json")
    parser.add_argument("--session-log", default="docs/v17-runtime-session-log-latest.json")
    parser.add_argument("--latest-json", default="docs/v17-external-establishment-validation-latest.json")
    parser.add_argument("--fail-on-warn", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, str]] = []

    board = _load_json(args.criteria_board, failures, "criteria board")
    runtime_validation = _load_json(args.runtime_validation, failures, "runtime validation")
    session_log = _load_json(args.session_log, failures, "session log")

    label_definitions = board.get("truth_label_definitions", {})
    truth_label_summary = board.get("truth_label_summary", {})
    criteria = board.get("criteria", [])
    pillars = board.get("pillars", {})
    protected_claims = board.get("not_externally_established_claims", [])
    claim_language_rules = board.get("claim_language_rules", [])
    allowed_labels = set(label_definitions.keys()) if isinstance(label_definitions, dict) else set()
    runtime_metrics = runtime_validation.get("metrics", {})
    runtime_truth_complete = bool(runtime_metrics.get("runtime_truth_complete"))
    runtime_validation_ok = bool(runtime_validation.get("effective_success"))
    establishment_gate_state = str(board.get("establishment_gate_state") or "")

    checks.append(
        _check(
            "runtime_dependency_status",
            runtime_validation_ok,
            f"runtime_truth_complete={runtime_truth_complete}",
            "runtime validation must pass before external-establishment claims are promoted",
            failures,
        )
    )

    schema_ok = (
        isinstance(label_definitions, dict)
        and {"repo_proven_strength", "comparative_promise", "open_gap"} <= allowed_labels
        and isinstance(criteria, list)
        and isinstance(truth_label_summary, dict)
    )
    checks.append(
        _check(
            "criteria_board_shape",
            schema_ok,
            f"criteria_count={len(criteria) if isinstance(criteria, list) else 0}",
            "criteria board must define truth labels, summary counts, and a criteria list",
            failures,
        )
    )

    protected_claims_ok = (
        isinstance(protected_claims, list)
        and any("GMUT" in str(item) for item in protected_claims)
        and any("Trinity Hybrid OS" in str(item) for item in protected_claims)
        and any("Freed ID" in str(item) for item in protected_claims)
        and isinstance(claim_language_rules, list)
        and bool(claim_language_rules)
    )
    checks.append(
        _check(
            "protected_claim_boundaries",
            protected_claims_ok,
            f"protected_claim_count={len(protected_claims) if isinstance(protected_claims, list) else 0}",
            "criteria board must preserve protected non-establishment claims and claim-language rules",
            failures,
        )
    )

    counts: dict[str, int] = {label: 0 for label in allowed_labels}
    board_errors: list[str] = []
    runtime_gate_errors: list[str] = []
    live_claim_found = False

    for index, row in enumerate(criteria if isinstance(criteria, list) else []):
        label = f"criteria[{index}]"
        if not isinstance(row, dict):
            board_errors.append(f"{label} must be an object")
            continue
        required_fields = (
            "criterion_id",
            "title",
            "claim_boundary",
            "truth_label",
            "requirement_state",
            "requires_complete_runtime_truth",
            "evidence_paths",
            "notes",
        )
        missing = [field for field in required_fields if field not in row]
        if missing:
            board_errors.append(f"{label} missing fields {missing}")
            continue

        truth_label = str(row.get("truth_label") or "")
        requirement_state = str(row.get("requirement_state") or "")
        evidence_paths = row.get("evidence_paths", [])
        criterion_id = str(row.get("criterion_id") or "")

        if truth_label not in allowed_labels:
            board_errors.append(f"{criterion_id or label} invalid truth_label {truth_label}")
        else:
            counts[truth_label] = counts.get(truth_label, 0) + 1
        if requirement_state not in ALLOWED_REQUIREMENT_STATES:
            board_errors.append(f"{criterion_id or label} invalid requirement_state {requirement_state}")
        if not isinstance(row.get("requires_complete_runtime_truth"), bool):
            board_errors.append(f"{criterion_id or label} requires_complete_runtime_truth must be boolean")
        if not isinstance(evidence_paths, list) or not evidence_paths:
            board_errors.append(f"{criterion_id or label} evidence_paths must be a non-empty list")
        else:
            for evidence_path in evidence_paths:
                text = str(evidence_path).strip()
                if not text:
                    board_errors.append(f"{criterion_id or label} evidence_paths contain an empty entry")
                    continue
                try:
                    evidence = _repo_path(text)
                except Exception:
                    board_errors.append(f"{criterion_id or label} invalid evidence path {text}")
                    continue
                if not evidence.exists():
                    board_errors.append(f"{criterion_id or label} missing evidence path {text}")

        if truth_label == "repo_proven_strength" and requirement_state != "PASS":
            board_errors.append(f"{criterion_id or label} repo_proven_strength rows must be PASS")

        if bool(row.get("requires_complete_runtime_truth")):
            live_claim_found = True
            if not runtime_truth_complete and truth_label != "open_gap":
                runtime_gate_errors.append(f"{criterion_id or label} must stay open_gap until runtime truth is complete")
            if not runtime_truth_complete and requirement_state not in {"OPEN", "HOLD"}:
                runtime_gate_errors.append(f"{criterion_id or label} must stay OPEN or HOLD until runtime truth is complete")

    checks.append(
        _check(
            "criteria_rows",
            not board_errors,
            f"truth_label_counts={counts}",
            "; ".join(board_errors) or "criteria rows must match the board schema",
            failures,
        )
    )

    summary_ok = all(int(truth_label_summary.get(label, -1) or 0) == counts.get(label, 0) for label in ("repo_proven_strength", "comparative_promise", "open_gap"))
    checks.append(
        _check(
            "truth_label_summary",
            summary_ok,
            f"summary={truth_label_summary}",
            "truth_label_summary must match the actual criteria counts",
            failures,
        )
    )

    gate_state_ok = establishment_gate_state == ("ready_for_live_establishment" if runtime_truth_complete else "repo_first_hold")
    checks.append(
        _check(
            "establishment_gate_state",
            gate_state_ok,
            f"establishment_gate_state={establishment_gate_state}",
            "establishment_gate_state must remain repo_first_hold until runtime truth is complete",
            failures,
        )
    )

    checks.append(
        _check(
            "live_establishment_guard",
            live_claim_found and not runtime_gate_errors,
            f"runtime_truth_complete={runtime_truth_complete}, overlay_state={session_log.get('overlay_state')}",
            "; ".join(runtime_gate_errors) or "criteria board must include a live-establishment guard row",
            failures,
        )
    )

    pillar_errors: list[str] = []
    if pillars and not isinstance(pillars, dict):
        pillar_errors.append("pillars must be an object when present")
    elif isinstance(pillars, dict):
        for pillar_name in ("mind", "body", "heart", "trinity_mandala"):
            row = pillars.get(pillar_name)
            if not isinstance(row, dict):
                pillar_errors.append(f"pillars.{pillar_name} must be an object")
                continue
            truth_label = str(row.get("current_truth_label") or "")
            if truth_label not in allowed_labels:
                pillar_errors.append(f"pillars.{pillar_name}.current_truth_label must use a declared truth label")
        if not runtime_truth_complete:
            trinity_label = str((pillars.get("trinity_mandala") or {}).get("current_truth_label") or "")
            if trinity_label and trinity_label != "open_gap":
                pillar_errors.append("pillars.trinity_mandala.current_truth_label must stay open_gap until runtime truth is complete")

    checks.append(
        _check(
            "pillar_truth_alignment",
            not pillar_errors,
            f"pillar_keys={sorted(pillars.keys()) if isinstance(pillars, dict) else []}",
            "; ".join(pillar_errors) or "pillar truth labels must align with the declared evidence boundary",
            failures,
        )
    )

    payload = {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "system_id": "v17_external_establishment_validation",
        "pillar": "trinity",
        "overall_status": _status(failures, warnings),
        "checks": checks,
        "metrics": {
            "runtime_truth_complete": runtime_truth_complete,
            "establishment_gate_state": establishment_gate_state,
            "truth_label_counts": counts,
            "criteria_count": len(criteria) if isinstance(criteria, list) else 0,
        },
        "source_artifacts_checked": [
            args.criteria_board,
            args.runtime_validation,
            args.session_log,
        ],
        "failures": failures,
        "warnings": warnings,
        "next_action": "Keep live external-establishment claims at open_gap until runtime truth is complete, and promote only repo_proven_strength or comparative_promise rows backed by repo evidence.",
        "effective_success": not failures and (not warnings or not args.fail_on_warn),
    }

    latest_json = _repo_path(args.latest_json)
    latest_json.parent.mkdir(parents=True, exist_ok=True)
    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"overall_status={payload['overall_status']}")
    print(f"runtime_truth_complete={runtime_truth_complete}")
    print(f"latest_json={latest_json.relative_to(ROOT)}")
    return 0 if payload["effective_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
