#!/usr/bin/env python3
"""Detailed bounded validator for Elowen Cairn v658-v1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v1_phase_data as d
import ghc_family_v658_v1_x2_config as c
from ghc_family_v658_v1_runtime import validate_contract


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(path for path in (ROOT / "scripts").glob("*v658_v1*.py") if path.is_file())
    for name in ["tests/test_ghc_family_v658_v1.py", "tests/test_ghc_family_v658_v1_x1.py"]:
        path = ROOT / name
        if path.is_file():
            paths.append(path)
    return sorted({path.resolve() for path in paths})


def validate() -> dict[str, Any]:
    checks = 0
    issues: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            issues.append(label)

    proposal_ledger = load("preregistration/proposal-ledger.json")
    x2_ledger = load("x2/proposal-ledger.json")
    check(proposal_ledger["proposal_count"] == c.EXPECTED_PROPOSALS, "proposal_count")
    check(x2_ledger["proposal_count"] == c.EXPECTED_PROPOSALS, "x2_proposal_count")
    check(x2_ledger["outcome_counts"] == c.EXPECTED_DISTRIBUTION, "outcome_distribution")
    check(set(x2_ledger["outcome_counts"]) == d.ALLOWED_OUTCOMES, "outcome_vocabulary")

    mutation_total = 0
    for proposal in d.PROPOSALS:
        base = f"surfaces/{proposal['slug']}"
        contract = load(f"{base}/contract.json")
        mutations = load(f"{base}/mutation-results.json")
        receipt = load(f"{base}/bounded-receipt.json")
        check(not validate_contract(contract), f"{proposal['proposal_id']}:valid_contract")
        check(contract["outcome"] == proposal["expected_disposition"], f"{proposal['proposal_id']}:outcome")
        check(mutations["mutation_count"] == c.MUTATIONS_PER_PROPOSAL, f"{proposal['proposal_id']}:mutation_count")
        check(mutations["rejected_count"] == c.MUTATIONS_PER_PROPOSAL and mutations["all_rejected"], f"{proposal['proposal_id']}:mutations_rejected")
        check(receipt["valid_fixture_passed"] and receipt["rejected_mutation_count"] == c.MUTATIONS_PER_PROPOSAL, f"{proposal['proposal_id']}:receipt")
        check(receipt["real_data_used"] is False and receipt["network_called"] is False, f"{proposal['proposal_id']}:no_real_data")
        check(receipt["authority_granted"] is False, f"{proposal['proposal_id']}:authority")
        mutation_total += mutations["mutation_count"]
    check(mutation_total == c.EXPECTED_MUTATIONS, "mutation_total")

    skill_receipts = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    runner_receipts = sorted((PHASE / "runners").glob("*-receipt.json"))
    check(len(skill_receipts) == 10, "skill_receipt_count")
    check(len(runner_receipts) == 10, "runner_receipt_count")
    for path in skill_receipts:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check(payload["valid"] is True, f"skill:{path.parent.name}:valid")
        check(payload["read_completely_before_use"] is True, f"skill:{path.parent.name}:read")
        check(payload["private_value_hit_count"] == 0, f"skill:{path.parent.name}:privacy")
    for path in runner_receipts:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check(payload["valid"] is True, f"runner:{path.name}:valid")
        check(payload["surface_count"] == 3, f"runner:{path.name}:surface_count")
        check(payload["valid_fixture_count"] == 3, f"runner:{path.name}:fixture_count")
        check(payload["rejected_mutation_count"] == 15, f"runner:{path.name}:mutation_count")

    tasks = load("x2/task-execution.json")
    check(tasks["counts"] == {"safe_now": 30, "candidate": 20, "clean": 30, "total": 80}, "task_counts")
    check(all(row["state"] == "completed" for row in tasks["safe_now"]), "safe_tasks")
    check(all(row["state"] == "completed" for row in tasks["candidate"]), "candidate_tasks")
    check(all(row["state"] == "completed" for row in tasks["clean"]), "clean_tasks")
    check(tasks["unsafe_work_manufactured"] is False, "unsafe_work")
    for row in tasks["candidate"]:
        receipt = load(row["evidence"])
        check(
            receipt["state"] == "completed"
            and receipt["reversible"] is True
            and receipt["external_side_effects"] is False
            and receipt["production_or_authority_credit"] is False,
            f"prototype:{row['task_id']}",
        )
    for row in tasks["clean"]:
        receipt = load(row["evidence"])
        check(
            receipt["state"] == "completed"
            and receipt["additive_only"] is True
            and receipt["user_material_deleted"] is False
            and receipt["history_rewritten"] is False
            and receipt["sibling_lane_mutated"] is False
            and receipt["gate_weakened"] is False,
            f"cleanup:{row['task_id']}",
        )

    negatives = load("truth/retained-negative-register-x2.json")
    check(negatives["source_effective_count"] == c.SOURCE_EFFECTIVE_NEGATIVES, "source_negatives")
    check(negatives["x1_operational_count"] == c.X1_OPERATIONAL_NEGATIVES, "x1_negatives")
    check(negatives["mutation_count"] == c.EXPECTED_MUTATIONS, "mutation_negatives")
    check(negatives["x2_operational_count"] == len(negatives["x2_operational_negatives"]), "x2_operational_negatives")
    check(negatives["effective_count"] == c.SOURCE_EFFECTIVE_NEGATIVES + c.X1_OPERATIONAL_NEGATIVES + c.EXPECTED_MUTATIONS + negatives["x2_operational_count"], "effective_negatives")
    check(negatives["all_retained"] is True, "negative_retention")

    gaps = load("truth/open-gap-register-x2.json")
    gates = load("truth/exact-gate-register-x2.json")
    check(gaps["effective_count"] == c.SOURCE_OPEN_GAPS + 1, "open_gaps")
    check(gates["effective_count"] == c.SOURCE_EXACT_GATES + 1, "exact_gates")

    flow = load("method-flow/method-flow-state-x2.json")
    expected_methods = c.EXPECTED_MUTATIONS + len(c.X2_OPERATIONAL_NEGATIVES)
    check(flow["counts"]["current_methods"] == expected_methods, "method_count")
    check(flow["counts"]["current_witness_results"] == {"fail": expected_methods, "pass": expected_methods}, "method_witness_counts")
    check(len(flow["current_witnesses"]) == expected_methods * 2, "method_witness_rows")
    check(flow["all_failed_witnesses_retained"] is True, "method_retention")

    frozen_paths = [
        line
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", c.X1_COMMIT).splitlines()
        if line
    ]
    index_changed = subprocess.run(
        ["git", "diff", "--cached", "--name-only", c.X1_COMMIT, "--", *frozen_paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    working_changed = subprocess.run(
        ["git", "diff", "--name-only", "--", *frozen_paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    changed = sorted(set(index_changed + working_changed))
    check(not changed, "x1_frozen_paths_changed")

    correction = load("truth/frozen-x1-stale-label-correction.json")
    hygiene = load("validation/stale-label-hygiene-x2.json")
    check(correction["x1_commit"] == c.X1_COMMIT, "stale_label_x1_anchor")
    check(correction["finding_count"] == 0 and correction["file_count"] == 0, "stale_label_frozen_count")
    check(correction["x1_bytes_preserved"] is True, "stale_label_x1_preserved")
    stale_compounds = [
        "Sable Rook" + " v658-v1",
        "Caelen Ash" + " v658-v1",
        "Orin Thale" + " v658-v1",
    ]
    frozen_set = set(frozen_paths)
    mutable_stale_hits = [
        path.relative_to(ROOT).as_posix()
        for path in owner_paths()
        if path.relative_to(ROOT).as_posix() not in frozen_set
        and any(token in path.read_text(encoding="utf-8") for token in stale_compounds)
    ]
    check(not mutable_stale_hits, "mutable_x2_stale_labels")
    check(
        hygiene["mutable_x2_undeclared_finding_count"] == 0
        and hygiene["valid_with_declared_frozen_correction"] is True,
        "stale_label_hygiene_receipt",
    )

    route = load("orchestration/route-state-x1.json")
    check(route["state"] == "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE", "route_state")
    check(route["message_sent"] is False, "route_message")
    check(route["next_exact_title"] == "Sylven Arc", "route_title")
    check(route["next_phase"] == "v658-v2", "route_phase")
    check(route["tavian_sol_state"] == "ON_STANDBY", "tavian_state")

    report = (PHASE / "deliverables/v658-v1-dry-stone-evidence-report.html").read_text(encoding="utf-8")
    check('<html lang="en">' in report, "report_language")
    check("<h1>" in report and "<h2" in report, "report_headings")
    check("<table>" in report and "<caption>" in report and 'scope="col"' in report, "report_table")
    check("<script" not in report.lower(), "report_no_active_script")
    check("affected-user" in report, "report_manual_reservation")

    json_paths = sorted(PHASE.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            json_issues.append(path.relative_to(ROOT).as_posix())
    check(not json_issues, "json_parse")

    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)\b(?:sk-[a-z0-9_-]{20,}|bearer\s+[a-z0-9._-]{20,}|password\s*[:=]\s*[^\s\"']{8,})"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "private_callable_value": re.compile(r"(?i)\bprivate_callable_(?:id|identifier)\s*[:=]\s*[a-z0-9_-]{8,}"),
    }
    privacy_hits = []
    paths = owner_paths()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                privacy_hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern": label, "count": count})
    check(not privacy_hits, "privacy")
    check(len(paths) < 2000, "owner_file_cap")

    docs = [
        path
        for path in PHASE.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}
    ]
    word_counts = {path.relative_to(PHASE).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in docs}
    check(max(word_counts.values()) <= 100000, "document_word_cap")

    truth = load("truth/phase-truth-x2.json")
    check(truth["outcome_counts"] == c.EXPECTED_DISTRIBUTION, "phase_truth_outcomes")
    check(truth["real_data_used"] is False, "phase_truth_real_data")
    check(truth["independent_reproduction"] is False, "phase_truth_reproduction")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "phase_truth_verdict")

    return {
        "schema": "ghc.family.v658-v1.detailed-validation.v1",
        "valid": not issues,
        "check_count": checks,
        "issues": issues,
        "proposal_count": len(d.PROPOSALS),
        "mutation_count": mutation_total,
        "skill_receipt_count": len(skill_receipts),
        "runner_receipt_count": len(runner_receipts),
        "json_parse_count": len(json_paths),
        "privacy_file_count": len(paths),
        "privacy_pattern_class_count": len(patterns),
        "privacy_confirmed_hits": privacy_hits,
        "maximum_document_words": max(word_counts.values()),
        "owner_file_count": len(paths),
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = validate()
    if args.output:
        path = ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
