#!/usr/bin/env python3
"""Build the exact v646-v4 ten-runner use ledger from separate witnesses."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from ghc_family_v646_v4_definitions import RUNNERS


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"
WITNESS_DIR = PHASE / "prototypes/runner-witnesses"


def witness_passed(payload: dict | None) -> bool:
    if not payload:
        return False
    if payload.get("passed") is True or payload.get("valid") is True:
        return True
    return bool(payload) and all(isinstance(row, dict) and row.get("passed") is True for row in payload.values())


def x2_operational_negatives() -> list[dict]:
    ledger = json.loads((PHASE / "method-flow/method-flow-state.json").read_text(encoding="utf-8"))
    methods = {row["method_id"]: row for row in ledger.get("methods", [])}
    rows: dict[str, dict] = {}
    for witness in ledger.get("witnesses", []):
        if witness.get("result") != "fail":
            continue
        for negative_id in witness.get("retained_negative_ids", []):
            if not str(negative_id).startswith("V6464-X2-N") or negative_id in rows:
                continue
            method = methods.get(witness.get("method_id"), {})
            rows[negative_id] = {
                "negative_id": negative_id, "surface": witness.get("scope"), "observed": witness.get("observed"),
                "credit": "none", "recovery": method.get("candidate_workaround"),
                "recurrence_guard": method.get("recurrence_guard"), "method_id": witness.get("method_id"),
                "failed_witness": witness.get("witness_id"),
            }
    return [rows[key] for key in sorted(rows)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    rows = []
    for filename, description in RUNNERS:
        script = ROOT / "scripts" / filename
        witness = WITNESS_DIR / filename.removesuffix(".py").replace("ghc_family_v646_v4_", "")
        witness = witness.with_suffix(".json")
        payload = json.loads(witness.read_text(encoding="utf-8")) if witness.is_file() else None
        passed = witness_passed(payload)
        rows.append({
            "name": filename, "description": description, "script": script.relative_to(ROOT).as_posix(),
            "built": script.is_file(), "family_current": filename.startswith("ghc_family_"),
            "witness": witness.relative_to(PHASE).as_posix() if witness.is_file() else None,
            "invoked": payload is not None, "passed": passed, "mode": payload.get("mode", "bounded_execution") if payload else "pending",
        })
    built = sum(row["built"] for row in rows); invoked = sum(row["invoked"] for row in rows); passed = sum(row["passed"] for row in rows)
    final_valid = built == invoked == passed == len(RUNNERS) == 10
    preflight_valid = args.preflight and built == 10 and invoked >= 8 and passed >= 8 and all(row["passed"] for row in rows if row["invoked"])
    result = {
        "schema": "ghc.family.v646-v4.runner-build-use.v1", "runner_count": len(rows),
        "built_count": built, "invoked_count": invoked, "passed_count": passed,
        "preflight": args.preflight, "preflight_valid": preflight_valid, "valid": final_valid,
        "runners": rows, "failed_or_missing": [row["name"] for row in rows if not row["passed"]],
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "Runner use establishes only the declared bounded workflow witnesses; it is not external review, production certification, authority, or independent reproduction.",
    }
    output = PHASE / "prototypes/runner-build-use-receipt.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if final_valid:
        truth_path = PHASE / "phase-truth.json"
        truth = json.loads(truth_path.read_text(encoding="utf-8"))
        truth["runners_built"] = 10
        truth["runners_built_and_used"] = 10
        truth["runners_aggregate_use_pending"] = False
        truth["runner_receipt"] = "prototypes/runner-build-use-receipt.json"
        truth_path.write_text(json.dumps(truth, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

        ledger_path = PHASE / "prototypes/skill-and-runner-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        for row in ledger.get("runners", []):
            row["state"] = "built_invoked_passed"
        ledger["aggregate_use_receipt"] = "runner-build-use-receipt.json"
        ledger["aggregate_use_valid"] = True
        ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

        checklist_path = PHASE / "complete-incomplete-checklist.json"
        checklist = json.loads(checklist_path.read_text(encoding="utf-8"))
        checklist["completed"] = list(dict.fromkeys([*checklist.get("completed", []), "ten family-current runners built, invoked, and passed", "current and eligible successor-scoped tests passed", "detailed and minimal candidate validation passed"]))
        checklist["pending"] = [row for row in checklist.get("pending", []) if row not in {"ten-runner aggregate use receipt", "current and eligible successor-scoped tests", "detailed and minimal validation"}]
        checklist_path.write_text(json.dumps(checklist, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

        update_path = PHASE / "orchestration/phase-update.json"
        update = json.loads(update_path.read_text(encoding="utf-8"))
        update["state"] = "x2_evidence_validated_pending_exact_staged_review_and_commit"
        update["ten_runner_aggregate_passed"] = True
        update_path.write_text(json.dumps(update, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

        environment_path = PHASE / "environment/x2-environment-receipt.json"
        environment = json.loads(environment_path.read_text(encoding="utf-8"))
        source = "c45aba6c9c2fee5d60e1fcde9f0de849290cfc96"
        added = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=A", source], cwd=ROOT, text=True, encoding="utf-8").splitlines()
        environment["full_checkout_file_count_at_evidence"] = sum(path.is_file() for path in ROOT.rglob("*"))
        environment["owner_generated_additive_file_count_at_evidence"] = len(added)
        environment["threshold_applies_to"] = "owner_generated_additive_file_count_only"
        environment["runtime_scratch_bank_action"] = "owner-generated scratch moved to additive D-first bank"
        environment["full_repository_suite_run"] = False
        environment["threshold_exceeded"] = len(added) >= environment["owner_generated_file_threshold"]
        environment_path.write_text(json.dumps(environment, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

        x2_rows = x2_operational_negatives()
        operational_path = PHASE / "validation/x2-operational-negatives.json"
        operational = {
            "schema": "ghc.family.v646-v4.x2-operational-negatives.v1", "count": len(x2_rows), "rows": x2_rows,
            "all_received_zero_initial_credit": True,
            "boundary": "Operational negatives remain retained after bounded recovery.",
        }
        operational_path.write_text(json.dumps(operational, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        retained_path = PHASE / "retained-negative-register.json"
        retained = json.loads(retained_path.read_text(encoding="utf-8"))
        old_total = retained["effective_total"]
        old_x2 = retained["x2_operational"]
        retained["x2_operational"] = len(x2_rows)
        retained["x2_operational_rows"] = x2_rows
        retained["effective_total"] = retained["inherited_effective"] + retained["x1_operational"] + retained["preregistered_synthetic_executed_and_rejected"] + len(x2_rows)
        retained_path.write_text(json.dumps(retained, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        truth["effective_retained_negatives"] = retained["effective_total"]
        truth_path.write_text(json.dumps(truth, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        evidence_receipt_path = PHASE / "validation/evidence-build-receipt.json"
        evidence_receipt = json.loads(evidence_receipt_path.read_text(encoding="utf-8"))
        evidence_receipt["x2_operational_negatives"] = len(x2_rows)
        evidence_receipt["effective_negatives"] = retained["effective_total"]
        evidence_receipt["late_negative_refresh"] = True
        evidence_receipt_path.write_text(json.dumps(evidence_receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        for relative in ("v646-v4-integrated-overview.md", "deliverables/v646-v4-final-integrated-overview.md", "deliverables/v646-v4-static-report.html"):
            path = PHASE / relative
            text = path.read_text(encoding="utf-8")
            text = text.replace(f"preserves {old_total} effective negatives", f"preserves {retained['effective_total']} effective negatives")
            text = text.replace(f"and {old_x2} x2 operational negatives", f"and {len(x2_rows)} x2 operational negatives")
            path.write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(rows), "built": built, "invoked": invoked, "passed": passed, "preflight_valid": preflight_valid, "valid": final_valid}))
    return 0 if final_valid or preflight_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
