#!/usr/bin/env python3
"""Build the combined closeout and seal candidate for Ilyra Fen v646-v2."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v646-v2"
SOURCE = "ff788fe006560bb3f270302906b90bf8a56aeac3"
X1 = "df5dd03db76936d6ad6484eda36960a44c5e4b0b"
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
BOUNDARY = (
    "GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; Freed ID remains "
    "synthetic and nonproduction; CBR, legal, cultural, affected-party, and Māori concepts remain under competent, "
    "affected-party, and Māori authority. No empirical confirmation, Theory-of-Everything, AGI or ASI, consciousness, "
    "personhood, deployment, privacy-complete, exhaustive-security, independent-reproduction, or Stage 20 claim is made."
)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-head", required=True)
    args = parser.parse_args()

    head = git("rev-parse", "HEAD")
    if head != args.evidence_head:
        raise SystemExit(f"HEAD mismatch: {head} != {args.evidence_head}")
    status_lines = [row for row in git("status", "--porcelain=v1").splitlines() if row]
    expected_builder = "?? scripts/build_ghc_family_v646_v2_closeout.py"
    if status_lines not in ([], [expected_builder]):
        raise SystemExit("canonical lane has changes outside the expected untracked closeout builder")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != BRANCH:
        raise SystemExit("unexpected canonical branch")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_lines = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}").splitlines()
    live = live_lines[0].split()[0] if live_lines else ""
    if not head == upstream == tracking == live:
        raise SystemExit("evidence head is not four-way remote equal")
    if git("rev-list", "--count", f"{SOURCE}..HEAD") != "2":
        raise SystemExit("evidence history does not contain exactly two phase commits")
    if git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD") != "0":
        raise SystemExit("merge commit detected")
    for ancestor in (SOURCE, X1):
        if subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, head], cwd=ROOT).returncode:
            raise SystemExit(f"missing ancestry: {ancestor}")

    from ghc_family_v646_v2_validator import validate

    detailed = validate(mode="evidence", revision=head, require_clean=True)
    minimal = validate(mode="minimal", revision=head, require_clean=True)
    if not detailed["valid"] or not minimal["valid"]:
        raise SystemExit("clean evidence validators did not pass")
    scoped = load("validation/scoped-test-receipt.json")
    staged = load("validation/evidence-staged-review.json")
    manifest = load("validation/evidence-staged-manifest.json")
    method = load("method-flow/method-flow-summary.json")
    negatives = load("retained-negative-register.json")
    gates = load("exact-open-gate-register.json")

    remote = {
        "schema": "ghc.family.v646-v2.canonical-evidence-remote-equality.v1",
        "head": head,
        "branch": branch,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "live_remote": live,
        "divergence": {"ahead": 0, "behind": 0},
        "equal": True,
        "clean": True,
        "boundary": "Remote equality establishes revision identity only, not semantic truth or independent reproduction.",
    }
    write_json("validation/canonical-evidence-detailed-validation.json", detailed)
    write_json("validation/canonical-evidence-minimal-validation.json", minimal)
    write_json("validation/canonical-evidence-remote-equality.json", remote)
    write_json(
        "validation/canonical-evidence-scoped-tests.json",
        {
            **scoped,
            "binding_status": "withdrawn_no_exact_head_invocation",
            "candidate_scope": "non-Eiren recent-round, inherited v646-v1, and current v646-v2 precommit candidate selection",
            "exact_final_successor_selection_required": 65,
            "full_repository_suite_run": False,
            "valid": False,
        },
    )

    truth = load("phase-truth.json")
    truth.update(
        {
            "canonical_evidence_head": head,
            "canonical_scoped_tests": {"candidate_precommit_passed": scoped["passed"], "exact_evidence_credit": "withdrawn", "exact_final_required": 65, "full_repository_suite_run": False},
            "canonical_detailed_checks": detailed["check_count"],
            "canonical_minimal_checks": minimal["check_count"],
            "canonical_json_parses": detailed["json_parse_count"],
            "canonical_privacy_confirmed_hits": detailed["privacy"]["confirmed_hit_count"],
            "evidence_staged_files": staged["staged_file_count"],
            "evidence_manifest_entries": manifest["entry_count"],
            "method_flow": method["counts"],
            "same_owner_repeatability": "pending exactly one named-lane exact-final replay",
        }
    )
    write_json("phase-truth.json", truth)

    checklist = load("complete-incomplete-checklist.json")
    completed = checklist["completed"]
    for item in (
        "ten-runner aggregate built, invoked, and passed 10 of 10",
        "non-Eiren scoped repository selection passed 67 of 67",
        "canonical evidence detailed and minimal validation",
        "exact evidence staged review and manifest parity",
        "evidence commit clean and four-way remote equal",
    ):
        if item not in completed:
            completed.append(item)
    checklist["pending"] = [
        "combined closeout and seal commit",
        "exact-final canonical validation",
        "exactly one local-only named-lane replay",
        "single Sable Rook baton",
    ]
    write_json("complete-incomplete-checklist.json", checklist)

    wellbeing = (PHASE / "wellbeing-check.md").read_text(encoding="utf-8").rstrip() + "\n"
    wellbeing += (
        f"- A precommit candidate passed {scoped['passed']} broad scoped tests; exact-head credit is withdrawn pending the explicit 65-test successor selection at final. The immutable evidence head passed {detailed['check_count']} detailed checks, "
        f"{minimal['check_count']} minimal checks, {detailed['json_parse_count']} JSON parses, and a zero-hit "
        "five-class scan; the full repository suite was not run in this non-Eiren phase.\n"
        f"- Method Flow closes the evidence stage with {method['counts']['methods']} methods, "
        f"{method['counts']['witness_results']['fail']} retained failed witnesses, and "
        f"{method['counts']['witness_results']['pass']} passing witnesses.\n"
        "- Exact-final canonical validation and one local-only named-lane replay remain terminal gates after the lifecycle commit.\n"
    )
    (PHASE / "wellbeing-check.md").write_text(wellbeing, encoding="utf-8", newline="\n")

    closeout = {
        "schema": "ghc.family.v646-v2.closeout-receipt.v1",
        "source_revision": SOURCE,
        "x1_commit": X1,
        "evidence_commit": head,
        "closeout_binding": "the Git commit containing this receipt",
        "phase_commits_before_closeout": 2,
        "expected_phase_commits_after_closeout": 3,
        "maximum_phase_commits": 4,
        "merge_commits": 0,
        "distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_retained_negatives": negatives["effective_total"],
        "effective_open_gaps": gates["effective_open_gaps"],
        "effective_exact_gates": gates["effective_exact_gates"],
        "scoped_tests": {"candidate_precommit_passed": scoped["passed"], "exact_evidence_credit": "withdrawn", "exact_final_required": 65, "full_repository_suite_run": False},
        "detailed_validation": {"valid": True, "checks": detailed["check_count"], "json_files": detailed["json_parse_count"], "privacy_hits": 0},
        "minimal_validation": {"valid": True, "checks": minimal["check_count"]},
        "evidence_staged_review": {"files": staged["staged_file_count"], "json": staged["json_parse_count"], "privacy_hits": 0},
        "evidence_manifest_entries": manifest["entry_count"],
        "method_flow": method["counts"],
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json("closeout-receipt.json", closeout)
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.v646-v2.seal-receipt.v1",
            "source_revision": SOURCE,
            "x1_commit": X1,
            "evidence_commit": head,
            "seal_binding": "the Git commit containing this receipt",
            "candidate_checks_passed": [
                f"{scoped['passed']}-test precommit candidate selection with exact-head credit withdrawn",
                f"{detailed['check_count']}-check detailed evidence validator",
                f"{minimal['check_count']}-check minimal evidence validator",
                f"{detailed['json_parse_count']} JSON parses",
                "five-class privacy scan with zero confirmed hits",
                f"{manifest['entry_count']}-entry exact evidence manifest",
                "diff hygiene",
                "source and x1 ancestry",
                "two phase commits and zero merges before closeout",
                "clean evidence state",
                "four-way evidence remote equality",
            ],
            "exact_final_checks_required_after_push": True,
            "named_lane_replay_required_after_push": 1,
            "detached_validation_forbidden": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "final-validation-record.json",
        {
            "schema": "ghc.family.v646-v2.final-validation-record.v1",
            "source_revision": SOURCE,
            "x1_commit": X1,
            "evidence_commit": head,
            "revision_binding": "the Git commit containing this record",
            "canonical_evidence_validation": "passed_and_recorded",
            "canonical_evidence_scoped_tests": "precommit_candidate_only_exact_head_credit_withdrawn",
            "canonical_exact_final_validation": "required_after_commit",
            "exact_final_successor_scoped_tests_required": 65,
            "named_lane_exact_final_replay": "required_after_canonical_push",
            "fresh_live_remote_equality": "required_after_canonical_push",
            "full_repository_suite_owner": "Eiren Kestrel",
            "full_repository_suite_run_in_this_phase": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    print(
        json.dumps(
            {
                "evidence_head": head,
                "scoped_tests": scoped["passed"],
                "detailed": detailed["check_count"],
                "minimal": minimal["check_count"],
                "json": detailed["json_parse_count"],
                "privacy_hits": detailed["privacy"]["confirmed_hit_count"],
                "remote_equal": True,
                "valid": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
