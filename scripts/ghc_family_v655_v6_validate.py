#!/usr/bin/env python3
"""Detailed and minimal validators for Caelen Ash v655-v6 lifecycle packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v655_v6_phase_data as d
import ghc_family_v655_v6_core as core


REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/caelen-ash/v655-v6"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_OUTCOMES = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
SCANNER_FILES = {
    "scripts/build_ghc_family_v655_v6_x1.py",
    "scripts/ghc_family_v655_v6_x1_staged_review.py",
    "scripts/ghc_family_v655_v6_validate.py",
    "scripts/ghc_family_v655_v6_evidence_staged_review.py",
    "scripts/ghc_family_v655_v6_final_validate.py",
    "scripts/ghc_family_v655_v6_final_staged_review.py",
}


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def add(checks: list[dict[str, Any]], name: str, condition: bool, detail: Any) -> None:
    checks.append({"name": name, "passed": bool(condition), "detail": detail})


def parse_jsons() -> tuple[int, list[dict[str, str]]]:
    count = 0
    errors = []
    for path in sorted(PHASE.rglob("*.json")):
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(
                {
                    "path": path.relative_to(PHASE).as_posix(),
                    "error": type(exc).__name__,
                }
            )
    return count, errors


def verify_manifest(relative: str, committed: bool) -> tuple[int, list[dict[str, str]]]:
    manifest = load(relative)
    mismatches = []
    for row in manifest["entries"]:
        path = row["path"]
        if committed:
            try:
                actual = git("rev-parse", f"HEAD:{path}")
            except subprocess.CalledProcessError:
                actual = "missing"
        else:
            actual = git("hash-object", f"--path={path}", path)
        if actual != row["git_blob"]:
            mismatches.append(
                {"path": path, "expected": row["git_blob"], "actual": actual}
            )
    return len(manifest["entries"]), mismatches


def privacy_scan(paths: list[str]) -> tuple[int, list[dict[str, str]], int]:
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "private_route_value": re.compile(
            r"(?:source_thread_id|resume[_ -]?token|private_callable_identifier)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
        "session_stream_payload": re.compile(
            r"(?:conversation[_ -]?transcript|session[_ -]?stream)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
    }
    candidates = []
    file_count = 0
    for relative in paths:
        path = REPO / relative
        if (
            not path.is_file()
            or path.suffix.lower()
            not in {".py", ".json", ".md", ".txt", ".html", ".yaml", ".yml"}
        ):
            continue
        file_count += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": relative, "class": label})
    confirmed = [row for row in candidates if row["path"] not in SCANNER_FILES]
    return file_count, confirmed, len(candidates) - len(confirmed)


def validate(lifecycle: str, mode: str, manifest_relative: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    proposals = load("preregistration/proposals.json")
    x2 = load("x2/proposal-ledger.json")
    phase_truth = load("truth/phase-truth-evidence.json")
    negatives = load("truth/retained-negative-register-x2.json")
    gaps = load("truth/open-gap-register-x2.json")
    gates = load("truth/exact-gate-register-x2.json")
    portfolio = load("portfolios/execution-results.json")
    index = load("tooling/ghc-family-index-x2-addendum.json")
    methods = load("method-flow/method-flow-ledger-x2.json")
    threat = load("threat-model.json")
    manifest = load(manifest_relative)
    json_count, json_errors = parse_jsons()
    manifest_count, manifest_mismatches = verify_manifest(
        manifest_relative, committed=lifecycle == "final"
    )
    scan_count, privacy_hits, definition_only = privacy_scan(
        [row["path"] for row in manifest["entries"]]
    )

    add(checks, "proposal_count", proposals["proposal_count"] == 30, proposals["proposal_count"])
    add(
        checks,
        "outcome_distribution",
        x2["outcome_counts"] == EXPECTED_OUTCOMES,
        x2["outcome_counts"],
    )
    add(
        checks,
        "outcome_domain",
        {row["observed_outcome"] for row in x2["proposals"]} <= ALLOWED_OUTCOMES,
        sorted({row["observed_outcome"] for row in x2["proposals"]}),
    )
    add(
        checks,
        "valid_fixtures",
        all(row["valid_fixture_passed"] for row in x2["proposals"]),
        sum(row["valid_fixture_passed"] for row in x2["proposals"]),
    )
    add(
        checks,
        "mutation_rejections",
        sum(row["rejected_mutation_count"] for row in x2["proposals"]) == 150
        and sum(row["accepted_mutation_count"] for row in x2["proposals"]) == 0,
        {
            "rejected": sum(row["rejected_mutation_count"] for row in x2["proposals"]),
            "accepted": sum(row["accepted_mutation_count"] for row in x2["proposals"]),
        },
    )
    for row in x2["proposals"]:
        add(
            checks,
            f"surface:{row['proposal_id']}:receipt",
            (PHASE / f"surfaces/{next(p['slug'] for p in proposals['proposals'] if p['proposal_id'] == row['proposal_id'])}/bounded-receipt.json").is_file(),
            row["proposal_id"],
        )
        add(
            checks,
            f"surface:{row['proposal_id']}:mutation_count",
            row["rejected_mutation_count"] == 5
            and row["accepted_mutation_count"] == 0,
            {
                "rejected": row["rejected_mutation_count"],
                "accepted": row["accepted_mutation_count"],
            },
        )
    add(
        checks,
        "skills_and_runners",
        len(index["skills"]) == 10
        and len(index["runners"]) == 10
        and all(row["valid"] for row in index["runner_rows"]),
        {"skills": len(index["skills"]), "runners": len(index["runners"])},
    )
    add(
        checks,
        "portfolio_resolved",
        portfolio["safe_now"]["pending"] == 0
        and portfolio["candidate"]["pending"] == 0
        and portfolio["clean_fix_refine"]["pending"] == 0
        and portfolio["skills"]["used"] == 10
        and portfolio["runners"]["used"] == 10,
        portfolio,
    )
    add(
        checks,
        "retained_negatives",
        negatives["no_failure_erased"]
        and negatives["synthetic_mutation_negative_count"] == 150
        and negatives["effective_at_evidence"]
        == negatives["x1_effective"]
        + negatives["synthetic_mutation_negative_count"]
        + negatives["x2_operational_count"],
        negatives["effective_at_evidence"],
    )
    add(
        checks,
        "open_gaps",
        gaps["effective_count"] == d.SOURCE_OPEN_GAPS + 1
        and gaps["closed_count"] == 0,
        gaps["effective_count"],
    )
    add(
        checks,
        "exact_gates",
        gates["effective_count"] == d.SOURCE_EXACT_GATES + 1
        and gates["closed_count"] == 0,
        gates["effective_count"],
    )
    add(
        checks,
        "method_flow_parity",
        methods["counts"]["witness_results"]["fail"]
        == methods["counts"]["witness_results"]["pass"]
        == methods["counts"]["methods"]
        == d.SOURCE_METHODS
        + negatives["x1_operational_count"]
        + negatives["x2_operational_count"],
        methods["counts"],
    )
    zero_truth = [
        "real_keys_or_proofs",
        "real_identity_resolutions",
        "real_status_or_revocation_events",
    ] + list(core.ZERO_EXTERNAL_COUNTS)
    add(
        checks,
        "external_actions_zero",
        all(phase_truth[field] == 0 for field in zero_truth),
        {field: phase_truth[field] for field in zero_truth},
    )
    false_truth = [
        "independent_reproduction_claimed",
        "privacy_complete_claimed",
        "accessibility_complete_claimed",
        "exhaustive_security_claimed",
        "professional_validation_claimed",
        "theory_of_everything_claimed",
        "agi_or_asi_claimed",
        "consciousness_or_personhood_claimed",
    ]
    add(
        checks,
        "promotion_claims_false",
        all(phase_truth[field] is False for field in false_truth),
        {field: phase_truth[field] for field in false_truth},
    )
    add(
        checks,
        "terminal_verdict",
        phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        phase_truth["terminal_verdict"],
    )
    add(
        checks,
        "route_unsent",
        phase_truth["route_state"]
        == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        phase_truth["route_state"],
    )
    add(
        checks,
        "overview_three_page_equivalent",
        len(
            (PHASE / "deliverables/v655-v6-integrated-overview.md")
            .read_text(encoding="utf-8")
            .split()
        )
        >= 1800,
        len(
            (PHASE / "deliverables/v655-v6-integrated-overview.md")
            .read_text(encoding="utf-8")
            .split()
        ),
    )
    report = (
        PHASE / "deliverables/v655-v6-boundary-evidence-report.html"
    ).read_text(encoding="utf-8")
    add(
        checks,
        "static_accessible_report_structure",
        all(
            token in report
            for token in [
                'lang="en"',
                'href="#main"',
                'id="main"',
                "<caption>",
                'scope="col"',
            ]
        )
        and "<script" not in report.casefold(),
        "manual and affected-user evaluation reserved",
    )
    add(
        checks,
        "threat_model_residuals",
        len(threat["threats"]) >= 8 and len(threat["residuals"]) >= 6,
        {"threats": len(threat["threats"]), "residuals": len(threat["residuals"])},
    )
    add(checks, "json_parsing", not json_errors, {"count": json_count, "errors": json_errors})
    add(
        checks,
        "privacy_scan",
        not privacy_hits,
        {
            "files": scan_count,
            "confirmed_hits": privacy_hits,
            "definition_only": definition_only,
        },
    )
    add(
        checks,
        "manifest_parity",
        not manifest_mismatches,
        {"count": manifest_count, "mismatches": manifest_mismatches},
    )
    add(
        checks,
        "owner_file_cap",
        sum(1 for path in PHASE.rglob("*") if path.is_file()) < 2000,
        sum(1 for path in PHASE.rglob("*") if path.is_file()),
    )

    if mode == "minimal":
        names = {
            "proposal_count",
            "outcome_distribution",
            "mutation_rejections",
            "skills_and_runners",
            "retained_negatives",
            "open_gaps",
            "exact_gates",
            "method_flow_parity",
            "external_actions_zero",
            "promotion_claims_false",
            "terminal_verdict",
            "route_unsent",
            "json_parsing",
            "privacy_scan",
            "manifest_parity",
        }
        checks = [row for row in checks if row["name"] in names]
    failed = [row for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v655-v6.validation.v1",
        "lifecycle": lifecycle,
        "mode": mode,
        "check_count": len(checks),
        "passed_count": len(checks) - len(failed),
        "failed_count": len(failed),
        "checks": checks,
        "json_parse_count": json_count,
        "privacy_file_count": scan_count,
        "privacy_confirmed_hits": privacy_hits,
        "privacy_definition_only_count": definition_only,
        "manifest_entry_count": manifest_count,
        "manifest_mismatches": manifest_mismatches,
        "valid": not failed,
        "boundary": (
            "Bounded same-owner validation only; not independent reproduction, "
            "external audit, production certification, exhaustive security, "
            "privacy or accessibility completeness, professional validation, "
            "legal or cultural ratification, Māori authority, empirical GMUT "
            "confirmation, Theory-of-Everything proof, AGI/ASI, personhood, or Stage 20."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lifecycle", choices=["evidence", "final"], required=True)
    parser.add_argument("--mode", choices=["detailed", "minimal"], required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = validate(args.lifecycle, args.mode, args.manifest)
    output = args.output if args.output.is_absolute() else PHASE / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": payload["valid"],
                "checks": payload["check_count"],
                "json": payload["json_parse_count"],
                "privacy_files": payload["privacy_file_count"],
                "privacy_hits": len(payload["privacy_confirmed_hits"]),
                "manifest": payload["manifest_entry_count"],
            },
            sort_keys=True,
        )
    )
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
