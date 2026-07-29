#!/usr/bin/env python3
"""Review Eiren's exact staged closeout without rerunning a successful suite."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v654_v6_2_remaster_manifest as manifest


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v654-v6-2-remaster"
EVIDENCE = "f878615e289d8d383bc54f75c0dca4c75b16b0e4"
ROUTE_STATE = "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
OUTPUT = ROOT / "validation/final-staged-review.json"
REQUIRED = {
    "docs/eiren-kestrel/v654-v6-2-remaster/handoffs/"
    "elaren-kestrel-v654-v7-activation.md",
    "docs/eiren-kestrel/v654-v6-2-remaster/truth/final-phase-truth.json",
    "docs/eiren-kestrel/v654-v6-2-remaster/validation/"
    "final-delta-manifest.json",
    "docs/eiren-kestrel/v654-v6-2-remaster/validation/"
    "final-owner-manifest.json",
    "docs/eiren-kestrel/v654-v6-2-remaster/validation/"
    "final-privacy-scan.json",
    "docs/eiren-kestrel/v654-v6-2-remaster/validation/"
    "final-json-parse.json",
    "scripts/ghc_family_v654_v6_2_remaster_final_validate.py",
    "tests/test_ghc_family_v654_v6_2_remaster_closeout.py",
}


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=check,
    )
    return result.stdout.strip()


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write(payload: Any) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any) -> None:
        checks.append(
            {"name": name, "passed": bool(passed), "observed": observed}
        )

    staged = sorted(
        path
        for path in git(
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            EVIDENCE,
        ).splitlines()
        if path
    )
    staged_set = set(staged)
    out_of_scope = [
        path for path in staged if not manifest.is_owner_path(path)
    ]
    sibling_docs = [
        path
        for path in staged
        if path.startswith("docs/")
        and not path.startswith(
            "docs/eiren-kestrel/v654-v6-2-remaster/"
        )
    ]
    whitespace = subprocess.run(
        ["git", "diff", "--cached", "--check", EVIDENCE],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    check("staged_nonempty", bool(staged), len(staged))
    check("exact_owner_scope", not out_of_scope, out_of_scope)
    check("no_sibling_docs", not sibling_docs, sibling_docs)
    check("required_paths", REQUIRED <= staged_set, sorted(REQUIRED - staged_set))
    check(
        "diff_whitespace",
        whitespace.returncode == 0,
        (whitespace.stdout + whitespace.stderr).splitlines(),
    )

    privacy = load("validation/final-privacy-scan.json")
    json_parse = load("validation/final-json-parse.json")
    delta_validation = load(
        "validation/final-delta-manifest-validation.json"
    )
    owner_validation = load(
        "validation/final-owner-manifest-validation.json"
    )
    metadata = load(
        "handoffs/elaren-kestrel-v654-v7-activation-metadata.json"
    )
    truth = load("truth/final-phase-truth.json")
    baton = (
        ROOT / "handoffs/elaren-kestrel-v654-v7-activation.md"
    ).read_text(encoding="utf-8")
    words = re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)

    check(
        "privacy",
        privacy["valid"] and privacy["confirmed_hit_count"] == 0,
        {
            "scanned": privacy["scanned_file_count"],
            "confirmed_hits": privacy["confirmed_hit_count"],
        },
    )
    check(
        "json_parse",
        json_parse["valid"] and json_parse["invalid_count"] == 0,
        {
            "json_count": json_parse["json_count"],
            "invalid": json_parse["invalid_count"],
        },
    )
    check(
        "manifest_replay",
        delta_validation["valid"] and owner_validation["valid"],
        {
            "delta_entries": delta_validation["entry_count"],
            "delta_issues": delta_validation["issue_count"],
            "owner_entries": owner_validation["entry_count"],
            "owner_issues": owner_validation["issue_count"],
        },
    )
    check(
        "route_prepared_not_sent",
        metadata["recipient"] == "Elaren Kestrel"
        and metadata["endpoint_kind"] == "main_task"
        and metadata["next_recipient"] == "Neris Solane"
        and metadata["delivery_state"] == ROUTE_STATE
        and metadata["contact_count"] == 0
        and metadata["send_cap"] == 1,
        metadata,
    )
    check(
        "baton_word_cap",
        10000 <= len(words) <= 100000
        and metadata["word_count"] == len(words),
        len(words),
    )
    check(
        "truth_counts",
        truth["effective_negative_count"] == 11871
        and truth["open_gap_count"] == 86
        and truth["exact_gate_count"] == 85
        and truth["method_count"] == 130
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        {
            "effective_negatives": truth["effective_negative_count"],
            "open_gaps": truth["open_gap_count"],
            "exact_gates": truth["exact_gate_count"],
            "methods": truth["method_count"],
            "verdict": truth["terminal_verdict"],
        },
    )

    valid = all(row["passed"] for row in checks)
    payload = {
        "schema": "ghc.family.v654-v6-2-remaster.final-staged-review.v1",
        "checks": checks,
        "passed": sum(row["passed"] for row in checks),
        "total": len(checks),
        "valid": valid,
        "staged_path_count": len(staged),
        "route_state": ROUTE_STATE,
        "full_repository_suite_run": False,
        "successful_suite_replayed": False,
        "canonical_postcommit_pass_required": True,
        "boundary": (
            "Exact precommit staged review only; not pushed-final equality, "
            "canonical repository success, delivery, independent validation, "
            "authority, or Stage 20 evidence."
        ),
    }
    write(payload)
    print(
        json.dumps(
            {
                "passed": payload["passed"],
                "total": payload["total"],
                "valid": valid,
                "staged_paths": len(staged),
            },
            sort_keys=True,
        )
    )
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
