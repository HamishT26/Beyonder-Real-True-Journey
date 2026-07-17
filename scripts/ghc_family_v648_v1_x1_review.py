#!/usr/bin/env python3
"""Validate the Tamar Vey v648-v1 x1-only packet."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v648_v1_definitions import (
    INHERITED_EFFECTIVE_NEGATIVES,
    OUTCOME_CLASSES,
    PHASE_SHORT,
    PRIOR_FROZEN_PROPOSALS,
    SLUG,
    X1_OPERATIONAL_NEGATIVES,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / SLUG / PHASE_SHORT
ALLOWED_STATUS = {"current", "stable", "draft", "watch"}
RAW_ID = re.compile(r"\b019[a-f0-9]{5}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", re.I)
PRIVATE_PATH = re.compile(r"(?:[A-Za-z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I)
SECRET_ASSIGNMENT = re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|private[_-]?key|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def review() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, observed: Any) -> None:
        checks.append({"name": name, "pass": bool(condition), "observed": observed})

    proposals = load(PHASE_DIR / "x1-proposals.json")
    collision = load(PHASE_DIR / "provenance" / "proposal-collision-audit.json")
    sources = load(PHASE_DIR / "sources" / "source-ledger.json")
    safe = load(PHASE_DIR / "approval-packets" / "x1-approval-portfolio.json")
    candidates = load(PHASE_DIR / "prototypes" / "x1-candidate-plan.json")
    skill_runner = load(PHASE_DIR / "prototypes" / "x1-skill-runner-plan.json")
    cleanup = load(PHASE_DIR / "maintenance" / "x1-clean-refine-plan.json")
    negatives = load(PHASE_DIR / "retained-negative-register.json")
    phase_truth = load(PHASE_DIR / "phase-truth.json")

    check("exactly_ten_proposals", len(proposals["proposals"]) == 10, len(proposals["proposals"]))
    check("prior_frozen_550", proposals["prior_frozen_proposal_count"] == PRIOR_FROZEN_PROPOSALS, proposals["prior_frozen_proposal_count"])
    check("frozen_after_560", proposals["frozen_chain_count_after_x1"] == 560, proposals["frozen_chain_count_after_x1"])
    check("x1_only", proposals["x2_execution_present"] is False and phase_truth["x1_only"] is True, phase_truth["x1_only"])
    check("no_exact_title_collision", collision["exact_collision_count"] == 0, collision["exact_collision_count"])
    dispositions = Counter(row["expected_disposition"] for row in proposals["proposals"])
    check("expected_6_2_1_1", dispositions == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}), dict(dispositions))
    check("outcome_vocabulary", set(dispositions) == set(OUTCOME_CLASSES), sorted(dispositions))
    check("source_status_vocabulary", set(sources["status_counts"]).issubset(ALLOWED_STATUS), sources["status_counts"])
    check("source_count_19", len(sources["sources"]) == 19, len(sources["sources"]))
    check("safe_floor_30", safe["count"] == 30 and len(safe["tasks"]) == 30, safe["count"])
    check("candidate_floor_20", candidates["count"] == 20 and len(candidates["tasks"]) == 20, candidates["count"])
    check("skill_floor_20", skill_runner["skill_count"] == 20 and len(skill_runner["skills"]) == 20, skill_runner["skill_count"])
    check("runner_floor_10", skill_runner["runner_count"] == 10 and len(skill_runner["runners"]) == 10, skill_runner["runner_count"])
    check("cleanup_floor_30", cleanup["count"] == 30 and len(cleanup["tasks"]) == 30, cleanup["count"])
    check("x1_negatives_retained", negatives["x1_operational"] == len(X1_OPERATIONAL_NEGATIVES), negatives["x1_operational"])
    check("effective_negative_count", negatives["effective_total_at_x1"] == INHERITED_EFFECTIVE_NEGATIVES + len(X1_OPERATIONAL_NEGATIVES), negatives["effective_total_at_x1"])
    check("terminal_not_ready", phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", phase_truth["terminal_verdict"])
    check("route_prepared_not_sent", phase_truth["route_state"] == "PREPARED_NOT_SENT", phase_truth["route_state"])

    json_files = sorted(PHASE_DIR.rglob("*.json"))
    parse_errors = []
    for path in json_files:
        try:
            load(path)
        except Exception as exc:  # pragma: no cover - receipt path
            parse_errors.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    check("all_json_parses", not parse_errors, len(json_files))

    privacy_hits = []
    word_cap_violations = []
    for path in sorted(PHASE_DIR.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        for name, pattern in (("raw_id", RAW_ID), ("private_path", PRIVATE_PATH), ("secret_assignment", SECRET_ASSIGNMENT)):
            if pattern.search(text):
                privacy_hits.append({"path": relative, "class": name})
        if path.suffix.lower() in {".md", ".html"}:
            words = len(re.findall(r"\b\w+\b", text, re.UNICODE))
            if words > 6000:
                word_cap_violations.append({"path": relative, "words": words})
    check("privacy_scan_zero", not privacy_hits, len(privacy_hits))
    check("document_word_caps", not word_cap_violations, word_cap_violations)

    forbidden_paths = [
        path.relative_to(PHASE_DIR).as_posix()
        for path in PHASE_DIR.rglob("*")
        if path.is_file()
        and (
            path.name.startswith("x2-")
            or path.name in {"evidence-receipt.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}
        )
    ]
    check("no_x2_or_closeout_artifacts", not forbidden_paths, forbidden_paths)

    valid = all(row["pass"] for row in checks)
    return {
        "schema": "ghc.family.v648-v1.x1-review.v1",
        "valid": valid,
        "checks_total": len(checks),
        "checks_passed": sum(row["pass"] for row in checks),
        "json_files_parsed": len(json_files),
        "privacy_hits": privacy_hits,
        "word_cap_violations": word_cap_violations,
        "checks": checks,
        "boundary": "X1 validation proves only preregistration structure and separation; it grants no x2, empirical, authority, production, accessibility-complete, or independent-reproduction credit.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=PHASE_DIR / "validation" / "x1-review.json")
    args = parser.parse_args()
    result = review()
    write(args.receipt, result)
    print(json.dumps({"valid": result["valid"], "checks": result["checks_total"], "json": result["json_files_parsed"]}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
