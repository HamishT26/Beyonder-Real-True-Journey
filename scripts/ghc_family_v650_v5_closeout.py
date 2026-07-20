#!/usr/bin/env python3
"""Build the combined closeout and seal packet for Tamar v650-v5."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v650_v5_phase_data as d

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE = d.SOURCE_HEAD
X1_INITIAL = "7c15d7e0f96e1ce5a1b7fd6049ef3c3285debc30"
X1_FINAL = "56ff8d5ab41d4b477184c854037122c81e2cc6a3"
EVIDENCE = "f485c4b053272eb384594d989ceeb6d85160111a"
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def method_run(*args: str) -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONUTF8"] = "1"
    subprocess.run(
        [sys.executable, str(METHOD_RUNNER), *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def record_closeout_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-state.json"
    state = read_json("method-flow/method-flow-state.json")
    existing_methods = {row["method_id"] for row in state["methods"]}
    existing_witnesses = {row["witness_id"] for row in state["witnesses"]}
    offset = len(d.X1_OPERATIONAL_NEGATIVES) + len(d.X2_OPERATIONAL_NEGATIVES)
    for index, negative in enumerate(d.CLOSEOUT_OPERATIONAL_NEGATIVES, start=1):
        method_id = f"V6505-M{offset + index:02d}"
        record = {
            "method_id": method_id,
            "title": f"Recover {negative['category']} without erasing its failed witness",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [f"A bounded v650-v5 closeout exposes {negative['category']}."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": "Give the failed assertion no closeout credit, retain it, and rely only on the corrected bounded witness.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["evidence_credit", "failure_retention", "claim_boundaries", "caller_compatibility"],
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": "Bounded same-owner closeout recovery only; no independent reproduction or authority credit.",
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": negative["failed"],
            "scope": f"bounded {negative['category']} failed witness",
            "expected": "The closeout assertion matches the frozen boundary.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Retained failure only; no closeout or authority credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": negative["recovery"],
            "scope": f"bounded {negative['category']} recovery witness",
            "expected": "The corrected assertion passes without changing the frozen boundary.",
            "observed": negative["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Bounded same-owner recovery only; no independent reproduction or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        fail_path = write_json(f"method-flow/{fail['witness_id'].casefold()}-witness.json", fail)
        pass_path = write_json(f"method-flow/{passed['witness_id'].casefold()}-witness.json", passed)
        if method_id not in existing_methods:
            method_run("record", "--ledger", str(ledger), "--record-file", str(record_path))
        for witness, path in ((fail, fail_path), (passed, pass_path)):
            if witness["witness_id"] not in existing_witnesses:
                method_run("witness", "--ledger", str(ledger), "--witness-file", str(path))
        state = read_json("method-flow/method-flow-state.json")
        method_state = next(row["recommendation_state"] for row in state["methods"] if row["method_id"] == method_id)
        if method_state == "validated":
            method_run("set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only after the failed assertion was retained and the exact frozen clause passed.")
        elif method_state != "preferred":
            raise RuntimeError(f"method {method_id} did not reach validated or preferred state")
    method_run("validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    method_run("summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


def main() -> int:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("closeout must start at the exact evidence head")
    status_lines = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    unexpected = [
        line for line in status_lines
        if not (
            line[3:].replace("\\", "/").startswith("docs/tamar-vey/v650-v5/")
            or line[3:].replace("\\", "/").startswith("scripts/ghc_family_v650_v5_")
            or line[3:].replace("\\", "/").startswith("tests/test_ghc_family_v650_v5_")
        )
    ]
    if unexpected:
        raise RuntimeError(f"unexpected precloseout paths: {unexpected}")
    for ancestor in (SOURCE, X1_INITIAL, X1_FINAL):
        subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, EVIDENCE], cwd=REPO, check=True)

    truth = read_json("phase-truth.json")
    negatives = read_json("retained-negative-register.json")
    gates = read_json("exact-open-gate-register.json")
    expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    present_closeout_ids = {
        row["negative_id"]
        for row in negatives["entries"]
        if row["negative_id"].startswith("V6505-CLOSE-")
    }
    if (
        truth["distribution"] != expected
        or negatives["effective_total"] != 6051 + len(present_closeout_ids)
    ):
        raise RuntimeError("evidence truth changed before closeout")

    record_closeout_method_flow()
    negative_entries = {
        row["negative_id"]: row
        for row in [*negatives["entries"], *d.CLOSEOUT_OPERATIONAL_NEGATIVES]
    }
    negatives = {
        **negatives,
        "schema": "ghc.family.v650-v5.retained-negatives.combined-seal.v1",
        "closeout_operational": len(d.CLOSEOUT_OPERATIONAL_NEGATIVES),
        "effective_total": 6051 + len(d.CLOSEOUT_OPERATIONAL_NEGATIVES),
        "entries": list(negative_entries.values()),
    }
    write_json("retained-negative-register.json", negatives)
    method = read_json("method-flow/method-flow-state.json")

    write_json(
        "closeout/source-ancestry.json",
        {
            "schema": "ghc.family.v650-v5.source-ancestry.closeout.v1",
            "source": SOURCE,
            "x1_initial": X1_INITIAL,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "expected_final_parent": EVIDENCE,
            "expected_phase_commit_count": 4,
            "expected_merge_count": 0,
            "expected_final_parent_count": 1,
            "all_anchors_ancestral_before_final": True,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v650-v5.closeout-receipt.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "source": SOURCE,
            "x1_commits": [X1_INITIAL, X1_FINAL],
            "evidence_commit": EVIDENCE,
            "combined_closeout_and_seal_commit": "this_commit",
            "distribution": expected,
            "effective_negatives": negatives["effective_total"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "method_flow": method["counts"],
            "evidence_tests": {"passed": 20, "run": 20},
            "inherited_precloseout_tests": {"passed": 32, "run": 32, "canonical_credit": False},
            "final_canonical_validation": "PENDING_EXTERNAL_EXACT_HEAD_PASS",
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        "closeout/seal-receipt.json",
        {
            "schema": "ghc.family.v650-v5.combined-seal-receipt.v1",
            "seal_state": "COMMITTED_PACKET_PENDING_EXTERNAL_CANONICAL_PASS",
            "source": SOURCE,
            "x1_final": X1_FINAL,
            "evidence": EVIDENCE,
            "final": "self",
            "commit_cap": 4,
            "phase_commits_before_final": 3,
            "zero_merges_before_final": True,
            "one_successful_pass_rule": True,
            "post_success_replay_allowed": False,
            "full_repository_suite_owner": "Eiren Kestrel",
            "full_repository_suite_run": False,
            "sandbox_or_hyperv_used": False,
            "desktop_updated": False,
            "host_security_changed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/final-record.json",
        {
            "schema": "ghc.family.v650-v5.final-record.contract.v1",
            "state": "PENDING_EXTERNAL_CANONICAL_PASS",
            "exact_final_head": "resolved_after_this_commit",
            "expected_parent": EVIDENCE,
            "expected_phase_commits": 4,
            "expected_merges": 0,
            "expected_parent_count": 1,
            "expected_tests": 62,
            "expected_test_modules": [
                "tests.test_ghc_family_v650_v4_x1",
                "tests.test_ghc_family_v650_v4_x2",
                "tests.test_ghc_family_v650_v4_closeout",
                "tests.test_ghc_family_v650_v5_x1",
                "tests.test_ghc_family_v650_v5_x2",
                "tests.test_ghc_family_v650_v5_closeout",
            ],
            "no_replay_after_success": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/final-canonical-validation-contract.json",
        {
            "schema": "ghc.family.v650-v5.final-canonical-validation-contract.v1",
            "runner": "scripts/ghc_family_v650_v5_final_validate.py",
            "external_output_required": True,
            "d_drive_output": True,
            "full_repository_suite": False,
            "one_successful_pass": True,
            "post_success_replay": False,
            "test_count": 62,
            "minimal_check_count": 25,
            "required_checks": [
                "exact head and clean before and after",
                "local upstream tracking and fresh live remote equality",
                "source x1 evidence ancestry",
                "four phase commits zero merges one final parent",
                "all phase JSON parses",
                "five-class public-owner privacy scan",
                "x1 initial x1 repair evidence and final manifest parity",
                "stale-label and document-cap review",
                "terminal verdict and reserved gates",
            ],
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    stale = read_json("validation/x1-stale-label-review.json")
    write_json(
        "validation/stale-label-review.json",
        {
            "schema": "ghc.family.v650-v5.stale-label-review.closeout.v1",
            "historical_candidate_count": stale["candidate_count"],
            "historical_candidates": stale["candidates"],
            "confirmed_current_stale_claim_count": stale["confirmed_current_stale_claim_count"],
            "passed": stale["passed"],
            "boundary": "Append-only historical placeholders retain zero current credit; correction witnesses remain authoritative.",
        },
    )
    documents = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.casefold() in {".md", ".html"}]
    word_counts = {path.relative_to(ROOT).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in documents}
    write_json(
        "validation/final-document-cap-receipt.json",
        {
            "schema": "ghc.family.v650-v5.document-cap.final.v1",
            "document_count": len(word_counts),
            "word_cap": 20000,
            "maximum_words": max(word_counts.values(), default=0),
            "violations": [path for path, count in word_counts.items() if count > 20000],
            "passed": all(count <= 20000 for count in word_counts.values()),
        },
    )
    owner_files = sum(1 for path in ROOT.rglob("*") if path.is_file())
    write_json(
        "validation/final-owner-file-threshold.json",
        {
            "schema": "ghc.family.v650-v5.owner-threshold.final.v1",
            "owner_files_before_final_manifests": owner_files,
            "threshold": 15000,
            "exceeded": owner_files >= 15000,
            "inherited_baseline_counted": False,
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v650-v5.phase-truth.combined-seal.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "SEALED_PENDING_EXTERNAL_CANONICAL_PASS",
            "source": SOURCE,
            "x1_commit": X1_FINAL,
            "x1_commits": [X1_INITIAL, X1_FINAL],
            "evidence_commit": EVIDENCE,
            "final_commit": "self",
            "proposal_count": 20,
            "distribution": expected,
            "effective_negatives": 6055,
            "effective_open_gaps": 47,
            "effective_exact_gates": 48,
            "same_owner_repeatability": True,
            "independent_team_reproduction": False,
            "canonical_validation": "pending_external_exact_head_pass",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        "ghc-family-index.json",
        {
            "schema": "ghc.family.v650-v5.phase-index.combined-seal.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_head": SOURCE,
            "x1_head": X1_FINAL,
            "evidence_head": EVIDENCE,
            "final_head": "self",
            "state": "sealed_pending_external_canonical_pass",
            "reviewed_current": True,
            "proposal_count": 20,
            "distribution": expected,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v650-v5.checklist.combined-seal.v1",
            "complete": [
                "source verified and fast-forward inherited",
                "x1 frozen in two dedicated commits before x2",
                "x2 evidence committed and remote-equal",
                "twenty proposals executed in frozen evidence classes",
                "four x2 operational failures and all x1 failures retained",
                "four closeout and lifecycle failures retained",
                "one hundred synthetic mutations retained",
                "expanded portfolios completed within bounded gates",
                "combined closeout and seal packet prepared within four-commit cap",
            ],
            "incomplete": [
                "sole successful exact-final canonical scoped pass",
                "final local upstream tracking and live-remote equality proof",
                "exact-title Sylven Arc resolution and one acknowledged baton",
                "all forty-seven open gaps and forty-eight exact gates",
                "independent-team scientific reproduction",
            ],
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v650-v5.terminal-route.combined-seal.v1",
            "target_title": "Sylven Arc",
            "target_phase": "v650-v6",
            "state": "PREPARED_NOT_SENT",
            "messages_sent": 0,
            "cross_platform_send": False,
            "send_gate": "exact final canonical validation plus four-way equality",
        },
    )
    write_text(
        "handoffs/sylven-arc-v650-v6-prepared.md",
        """# Sylven Arc v650-v6 prepared activation

This sanitized baton is prepared, not sent. The exact final head and validation counts must be supplied from verified live state at send time.

Tamar v650-v5 preserves fourteen completed, four represented, one open gap, and one exact gate; 6,055 effective negatives; 47 open gaps; 48 exact gates; same-owner evidence only; and `NOT_READY_FOR_STAGE_20`.

The successor must verify the exact branch, final head, source, x1, evidence, clean state, four-commit single-parent history, zero merges, manifests, privacy result, and remote equality before mutation. No full repository suite, replay after success, Sandbox or Hyper-V use, cross-platform send, authority promotion, empirical promotion, production identity claim, or independent-reproduction claim is authorized.
""",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
