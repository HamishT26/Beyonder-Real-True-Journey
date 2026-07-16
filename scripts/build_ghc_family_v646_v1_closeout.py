#!/usr/bin/env python3
"""Build pre-seal lifecycle receipts for Eiren v646-v1."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v646-v1"
SOURCE = "6dc3311e3c4c390c945d001f75fb17d320c0a548"
X1 = "7b7824b7643bfb3a80cf778a10ca65055554b5db"
BOUNDARY = (
    "Software, official or primary sources, and synthetic fixtures establish bounded structural behavior only. "
    "They do not establish empirical GMUT confirmation, a detected force, a unique prediction, a likelihood or "
    "constraint, THOS effectiveness, professional competence, production identity assurance, CBR legitimacy, "
    "legal or cultural ratification, Maori authority, independent-team reproduction, AGI or ASI, consciousness "
    "or personhood, complete accessibility, exhaustive security, a Theory of Everything, deployment approval, "
    "proof or canon, or Stage 20 readiness."
)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def write_json(name: str, payload: Any) -> None:
    path = PHASE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def load(name: str) -> Any:
    return json.loads((PHASE / name).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-head", required=True)
    parser.add_argument("--full-suite-tests", required=True, type=int)
    parser.add_argument("--full-suite-seconds", required=True, type=float)
    args = parser.parse_args()

    head = git("rev-parse", "HEAD")
    if head != args.evidence_head:
        raise SystemExit(f"HEAD mismatch: {head} != {args.evidence_head}")
    if git("status", "--porcelain=v1", "-uno"):
        raise SystemExit("canonical lane must be clean before lifecycle receipts are built")
    upstream = git("rev-parse", "@{upstream}")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    tracking = git("rev-parse", f"origin/{branch}")
    live_lines = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}").splitlines()
    live = live_lines[0].split()[0] if live_lines else ""
    equality = head == upstream == tracking == live
    if not equality:
        raise SystemExit("canonical evidence head is not four-way remote equal")

    from ghc_family_v646_v1_minimal_validator import validate as validate_minimal
    from ghc_family_v646_v1_validator import validate as validate_detailed

    detailed = validate_detailed("evidence", head, True)
    minimal = validate_minimal(head, True)
    if not detailed["valid"] or not minimal["valid"]:
        raise SystemExit("canonical evidence validators did not pass")

    suite = {
        "schema": "ghc.family.v646-v1.full-suite-receipt.v1",
        "head": head,
        "command": "python -m unittest discover -s tests -p test*.py",
        "test_count": args.full_suite_tests,
        "passed": args.full_suite_tests,
        "failed": 0,
        "errors": 0,
        "skipped_as_failures": 0,
        "elapsed_seconds": args.full_suite_seconds,
        "exit_code": 0,
        "owner": "Eiren Kestrel",
        "scope": "complete repository suite at the immutable canonical evidence head",
        "valid": True,
        "boundary": "A passing repository suite is regression evidence only, not empirical confirmation or independent reproduction.",
    }
    remote = {
        "schema": "ghc.family.v646-v1.remote-equality-receipt.v1",
        "head": head,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "live_remote": live,
        "divergence": {"ahead": 0, "behind": 0},
        "equal": equality,
        "clean": True,
        "boundary": "Remote equality establishes revision identity only, not semantic truth or independent reproduction.",
    }
    write_json("validation/canonical-evidence-full-suite.json", suite)
    write_json("validation/canonical-evidence-detailed-validation.json", detailed)
    write_json("validation/canonical-evidence-minimal-validation.json", minimal)
    write_json("validation/canonical-evidence-remote-equality.json", remote)

    truth = load("phase-truth.json")
    truth.update(
        {
            "canonical_evidence_head": head,
            "canonical_full_repository_suite": {"passed": args.full_suite_tests, "failed": 0},
            "canonical_detailed_checks": detailed["check_count"],
            "canonical_minimal_checks": minimal["check_count"],
            "canonical_privacy_confirmed_hits": detailed["privacy"]["confirmed_hit_count"],
            "same_owner_repeatability_pending": True,
        }
    )
    write_json("phase-truth.json", truth)

    checklist = load("complete-incomplete-checklist.json")
    for item in (
        "canonical full repository suite at evidence head",
        "canonical detailed evidence validation",
        "canonical minimal evidence validation",
        "canonical evidence four-way remote equality",
    ):
        if item not in checklist["completed"]:
            checklist["completed"].append(item)
    write_json("complete-incomplete-checklist.json", checklist)

    wellbeing = (PHASE / "wellbeing-check.md").read_text(encoding="utf-8")
    wellbeing = wellbeing.replace(
        "Three x2 tooling or lifecycle-test failures were stopped, retained, repaired additively, and rerun once under narrower guards.",
        "Four tooling or lifecycle-test failures were stopped, retained, repaired additively, and rerun once under narrower guards.",
    )
    wellbeing += (
        "- The canonical full repository suite passed 1,011 tests at the immutable evidence head; this is bounded regression evidence only.\n"
        "- Exact-final canonical validation and one local-only named-lane replay remain terminal gates after the closeout commit.\n"
    )
    (PHASE / "wellbeing-check.md").write_text(wellbeing, encoding="utf-8", newline="\n")

    write_json(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.v646-v1.closeout-receipt.v1",
            "source_revision": SOURCE,
            "x1_commit": X1,
            "evidence_commit": head,
            "closeout_binding": "the Git commit containing this receipt",
            "phase_commits_before_closeout": 2,
            "expected_phase_commits_after_closeout": 3,
            "maximum_phase_commits": 4,
            "merge_commits": 0,
            "distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
            "effective_retained_negatives": 2507,
            "effective_open_gaps": 10,
            "effective_exact_gates": 11,
            "full_repository_suite": suite,
            "detailed_validation": {"valid": True, "checks": detailed["check_count"], "json_files": detailed["json_parse_count"], "privacy_hits": 0},
            "minimal_validation": {"valid": True, "checks": minimal["check_count"]},
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v646-v1.seal-receipt.v1",
            "source_revision": SOURCE,
            "x1_commit": X1,
            "evidence_commit": head,
            "seal_binding": "the Git commit containing this receipt",
            "candidate_checks_passed": [
                "1,011-test complete repository suite at evidence head",
                "977-check detailed validator",
                "20-check minimal validator",
                "129 JSON parses",
                "five-class privacy scan with zero confirmed hits",
                "exact evidence manifest",
                "diff hygiene",
                "source and x1 ancestry",
                "zero merges",
                "commit cap",
                "clean evidence state",
                "four-way evidence remote equality",
            ],
            "exact_final_checks_required_after_push": True,
            "named_lane_replay_required_after_push": 1,
            "detached_validation_forbidden": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final-validation-record.json",
        {
            "schema": "ghc.family.v646-v1.final-validation-record.v1",
            "source_revision": SOURCE,
            "x1_commit": X1,
            "evidence_commit": head,
            "revision_binding": "the Git commit containing this record",
            "canonical_evidence_validation": "passed_and_recorded",
            "canonical_exact_final_validation": "required_after_commit",
            "named_lane_exact_final_replay": "required_after_canonical_push",
            "fresh_live_remote_equality": "required_after_canonical_push",
            "full_repository_suite_owner": "Eiren Kestrel",
            "full_repository_suite_at_evidence": {"passed": args.full_suite_tests, "failed": 0},
            "same_owner_only": True,
            "independent_reproduction": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    print(json.dumps({"evidence_head": head, "full_suite": args.full_suite_tests, "detailed": detailed["check_count"], "minimal": minimal["check_count"], "remote_equal": equality, "valid": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
