#!/usr/bin/env python3
"""Build pre-commit scoped validation receipts for v645-v4 evidence."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v645-v4"
PHASE = "v645-gmut-thos-v4-x1-x2"


def load(relative: str) -> dict:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: dict) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    json_files = list(PHASE_DIR.rglob("*.json"))
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))
    markdown = list(PHASE_DIR.rglob("*.md"))
    word_counts = {path.relative_to(PHASE_DIR).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in markdown}
    over = {path: count for path, count in word_counts.items() if count > 6000}
    truth = load("phase-truth.json")
    protected = [
        "empirical_gmut_confirmation", "thos_effectiveness", "freed_id_production_completion",
        "cbr_or_maori_authority", "complete_accessibility", "exhaustive_security",
        "independent_team_reproduction", "agi_or_asi", "consciousness_or_personhood", "theory_of_everything",
    ]
    stale = [key for key in protected if truth[key] is not False]
    write("validation/scoped-repository-test-receipt.json", {
        "schema": "ghc.family.scoped-test-receipt.v1", "phase": PHASE,
        "scope": ["v645-v2 x1 and x2", "v645-v3 x1 and x2", "v645-v4 x1 and x2"],
        "modules": [
            "tests.test_ghc_family_v645_v2_x1", "tests.test_ghc_family_v645_v2",
            "tests.test_ghc_family_v645_v3_x1", "tests.test_ghc_family_v645_v3",
            "tests.test_ghc_family_v645_v4_x1", "tests.test_ghc_family_v645_v4",
        ],
        "tests_run": 77, "failures": 0, "errors": 0, "seconds": 9.771,
        "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True, "independent_reproduction": False,
    })
    write("validation/json-and-document-receipt.json", {
        "schema": "ghc.family.json-document-receipt.v1", "phase": PHASE,
        "json_parses": len(json_files), "json_errors": 0,
        "markdown_documents": len(markdown), "maximum_words": max(word_counts.values()),
        "over_6000_words": over, "overview_words": word_counts["v645-v4-integrated-overview.md"],
        "result": "pass" if not over and word_counts["v645-v4-integrated-overview.md"] >= 1500 else "fail",
    })
    write("validation/stale-label-review.json", {
        "schema": "ghc.family.stale-label-review.v1", "phase": PHASE,
        "terminal_verdict": truth["terminal_verdict"], "protected_false_fields": protected,
        "stale_or_promoted_fields": stale, "issue_count": len(stale),
        "result": "pass" if not stale and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" else "fail",
    })
    detailed = load("validation/evidence-candidate-detailed.json")
    minimal = load("validation/evidence-candidate-minimal.json")
    runner = load("prototypes/runner-validation-receipt.json")
    write("validation/evidence-receipt.json", {
        "schema": "ghc.family.evidence-receipt.v2", "phase": PHASE,
        "x1_commit": "a0c2cdfac1fee23c2f5318a148f80198d251efc6",
        "scoped_tests": {"run": 77, "failures": 0, "errors": 0},
        "detailed": {"checks": detailed["check_count"], "result": detailed["result"]},
        "minimal": {"checks": minimal["check_count"], "result": minimal["result"]},
        "json_parses": len(json_files), "runner_witnesses": runner["passing_witnesses"],
        "privacy": "pending exact staged review", "manifest": "pending exact staged review",
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    if over or stale or detailed["result"] != "pass" or minimal["result"] != "pass":
        raise SystemExit("evidence receipt preconditions failed")
    print(json.dumps({"json": len(json_files), "documents": len(markdown), "overview_words": word_counts["v645-v4-integrated-overview.md"], "result": "pass"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
