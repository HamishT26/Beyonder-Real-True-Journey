#!/usr/bin/env python3
"""Build the bounded v649-v6 validation-correction commit after one failed aggregate."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v649-v6"
X1 = "d82382737868160e1b16c9302ca8a008b6f3153e"
EVIDENCE = "4e5f250f8dbe4f77fadce2dfdccfb7869f06ab30"
TAMAR_EVIDENCE = "63f679b002e3f17df465a11c30632e769215ff7c"
TAMAR_FINAL = "295aa503d3c336273f541504a83b88783563ad90"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env).stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def changed_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def restore_evidence_ledger() -> Path:
    relative = "docs/sylven-arc/v649-v6/method-flow/method-flow-ledger.json"
    path = ROOT / relative
    path.write_text(git("show", f"{EVIDENCE}:{relative}") + "\n", encoding="utf-8", newline="\n")
    return path


def add_recovery_methods() -> dict[str, int]:
    ledger = restore_evidence_ledger()
    specs = [
        {
            "method_id": "V6496-M23",
            "negative_ids": ["V6496-X2-N05"],
            "title": "Decompose remote-anchor probes into bounded scalar commands",
            "failures": ["A combined read-only evidence-anchor probe exceeded its sixty-second wrapper before returning and received zero credit."],
            "recovery": "Run cleanliness, parent, commit-count, merge-count, upstream, and live-remote checks as bounded scalar commands.",
            "passing": "The decomposed checks proved the evidence head, direct x1 parent, two phase commits, zero merges, clean state, and four-way equality.",
            "guard": "Do not aggregate slow Git metadata checks under one narrow wrapper when each scalar result is independently attributable.",
        },
        {
            "method_id": "V6496-M24",
            "negative_ids": ["V6496-X2-N06"],
            "title": "Quote PowerShell upstream shorthand before invoking Git",
            "failures": ["PowerShell parsed unquoted @{upstream} as an incomplete hash literal before any Git child command ran."],
            "recovery": "Quote the upstream shorthand as '@{upstream}' in PowerShell commands.",
            "passing": "The quoted command resolved the exact upstream branch and the evidence equality proof passed.",
            "guard": "Always quote Git revision shorthand containing braces in PowerShell.",
        },
        {
            "method_id": "V6496-M25",
            "negative_ids": ["V6496-X2-N07", "V6496-X2-N08", "V6496-X2-N10"],
            "title": "Project historical lifecycle assertions to their immutable evidence commits",
            "failures": [
                "The first canonical aggregate failed the inherited v649-v5 evidence-manifest assertion because it compared Tamar's evidence manifest to successor HEAD.",
                "The same aggregate failed the inherited v649-v5 Method Flow assertion because it read Tamar's later closeout ledger instead of the v649-v5 evidence ledger.",
                "Pre-retry review found the v649-v6 evidence-manifest test would likewise compare the immutable evidence manifest to a later correction index.",
            ],
            "recovery": "Run every historical JSON and manifest assertion against its exact evidence commit while preserving every selected test and current-phase correction assertion.",
            "passing": "Tamar v649-v5 loads from its exact evidence commit, HEAD:path manifest reads project to that commit, and Sylven's evidence manifest binds the exact Sylven evidence commit.",
            "guard": "Successor validation must not reinterpret phase-local evidence assertions against a later closeout or successor head.",
        },
        {
            "method_id": "V6496-M26",
            "negative_ids": ["V6496-X2-N09"],
            "title": "Decompose diagnostic reads before parallel orchestration",
            "failures": ["An overbroad parallel diagnostic read returned exit 1 without delivering the successful sibling outputs, so it received zero evidence credit."],
            "recovery": "Resolve candidate paths first, then read each required source contract with explicit existence handling.",
            "passing": "The decomposed reads recovered Tamar's validator, canonical receipt, validation plan, correction receipt, and exact failing test definitions.",
            "guard": "Do not let one optional diagnostic path suppress independently successful read-only results.",
        },
    ]
    for spec in specs:
        method_id = spec["method_id"]
        record = {
            "method_id": method_id,
            "title": spec["title"],
            "failure_signature": " ".join(spec["failures"]),
            "trigger_preconditions": ["A bounded post-evidence validation or remote-proof step fails before credit is assigned."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": spec["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": spec["guard"],
            "rollback": "Give every failed probe or aggregate zero credit, retain its exact signature, and change only the demonstrated lifecycle or wrapper fault.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "single_successful_pass", "immutable_phase_evidence", "remote_equality", "evidence_credit"],
            "retained_negative_ids": spec["negative_ids"],
            "scope_boundary": "Bounded same-owner recovery only; no independent reproduction, production, scientific, professional, legal, cultural, privacy-complete, security-complete, or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for index, (negative_id, failure) in enumerate(zip(spec["negative_ids"], spec["failures"]), 1):
            suffix = "WFAIL" if len(spec["negative_ids"]) == 1 else f"WFAIL-{index}"
            witness = {
                "witness_id": f"{method_id}-{suffix}",
                "method_id": method_id,
                "procedure": failure,
                "scope": "bounded v649-v6 post-evidence failure",
                "expected": "No failed probe or aggregate receives evidence credit.",
                "observed": failure,
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "Failed witness retained with zero pass credit.",
            }
            witness_path = write_json(f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        pass_witness = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": spec["recovery"],
            "scope": "bounded v649-v6 post-evidence recovery",
            "expected": "Produce attributable bounded evidence without weakening any lifecycle gate.",
            "observed": spec["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": spec["negative_ids"],
            "boundary": "Bounded recovery witness only; no broader evidence credit.",
        }
        pass_path = write_json(f"method-flow/{pass_witness['witness_id'].casefold()}-witness.json", pass_witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path))
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Preferred only after the bounded passing recovery witness while every failed witness remains retained.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/correction-method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/correction-method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/correction-method-flow-summary.md"))
    payload = json.loads(ledger.read_text(encoding="utf-8"))
    counts = {
        "methods": len(payload["methods"]),
        "witnesses": len(payload["witnesses"]),
        "failed": sum(row["result"] == "fail" for row in payload["witnesses"]),
        "passed": sum(row["result"] == "pass" for row in payload["witnesses"]),
        "preferred": sum(row["recommendation_state"] == "preferred" for row in payload["methods"]),
    }
    if counts != {"methods": 26, "witnesses": 44, "failed": 18, "passed": 26, "preferred": 26}:
        raise RuntimeError(f"unexpected correction Method Flow counts: {counts}")
    return counts


def privacy(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v649_v6_correction.py",
        "scripts/build_ghc_family_v649_v6_closeout.py",
        "scripts/ghc_family_v649_v6_validate.py",
        "docs/sylven-arc/v649-v6/validation/correction-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    scanned = 0
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v649-v6.correction-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Correction-commit paths only; zero confirmed hits is not complete privacy assurance.",
    }


def update_overviews() -> None:
    addition = (
        "\n\n## Validation correction before the credited pass\n\n"
        "The first canonical aggregate received zero credit after 156 of 158 selected tests passed. Two inherited v649-v5 lifecycle assertions read successor HEAD and Tamar's later closeout Method Flow state instead of Tamar's exact evidence commit. No test was removed or excluded. The correction projects Tamar's historical JSON and manifest assertions to the exact v649-v5 evidence commit and binds Sylven's evidence manifest to the exact Sylven evidence commit. A combined anchor-probe timeout, an unquoted PowerShell upstream shorthand, and an overbroad parallel diagnostic read also remain retained. The correction boundary preserves 5,197 effective negatives: 5,109 inherited, eight x1 operational, seventy synthetic, and ten x2 operational. Exactly one credited successful canonical pass remains available; no post-success replay is permitted.\n"
    )
    for relative in ["integrated-overview.md", "handoffs/eiren-kestrel-v649-v7-activation.md"]:
        path = PHASE / relative
        text = path.read_text(encoding="utf-8")
        if "## Validation correction before the credited pass" not in text:
            text = text.rstrip() + addition
        path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("correction must begin at the exact pushed evidence commit")
    if git("rev-parse", f"{EVIDENCE}^") != X1:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("correction builder requires an empty index")

    method_counts = add_recovery_methods()
    prior = load("validation/x2-operational-negatives.json")
    new_negatives = [
        {"negative_id": "V6496-X2-N05", "category": "combined_anchor_probe_timeout", "failed": "A combined read-only evidence-anchor probe exceeded its wrapper before returning.", "recovery": "Decompose into bounded scalar checks.", "passing": "Scalar checks proved parent, commit count, zero merges, cleanliness, and four-way equality.", "canonical_attempt_consumed": False},
        {"negative_id": "V6496-X2-N06", "category": "powershell_upstream_shorthand_parse", "failed": "PowerShell parsed unquoted @{upstream} before Git ran.", "recovery": "Quote '@{upstream}'.", "passing": "The quoted upstream command and equality proof passed.", "canonical_attempt_consumed": False},
        {"negative_id": "V6496-X2-N07", "category": "inherited_manifest_head_projection", "failed": "The failed canonical aggregate compared Tamar's evidence manifest to successor HEAD.", "recovery": "Project HEAD:path reads to Tamar's exact evidence commit.", "passing": "The source-local manifest remains bound to the exact evidence commit.", "canonical_attempt_consumed": True},
        {"negative_id": "V6496-X2-N08", "category": "inherited_method_flow_lifecycle_projection", "failed": "The failed canonical aggregate read Tamar's later closeout Method Flow ledger for an evidence-phase assertion.", "recovery": "Load Tamar phase JSON from its exact evidence commit.", "passing": "The source-local Method Flow assertion sees its exact evidence state.", "canonical_attempt_consumed": True},
        {"negative_id": "V6496-X2-N09", "category": "parallel_diagnostic_output_suppression", "failed": "An overbroad parallel diagnostic read returned exit 1 without delivering successful sibling outputs.", "recovery": "Resolve paths first and read contracts separately.", "passing": "The exact validator, plan, receipt, correction, and test definitions were recovered.", "canonical_attempt_consumed": False},
        {"negative_id": "V6496-X2-N10", "category": "current_evidence_manifest_lifecycle_projection", "failed": "Pre-retry review found the current evidence-manifest test would compare the evidence manifest to a later correction index.", "recovery": "Bind it to the exact Sylven evidence commit.", "passing": "The test now replays the immutable evidence commit objects.", "canonical_attempt_consumed": False},
    ]
    write_json("validation/x2-operational-negatives.json", {**prior, "count": 10, "negatives": prior["negatives"] + new_negatives, "all_retained": True})
    write_json("x2/retained-negative-register.json", {
        **load("x2/retained-negative-register.json"),
        "schema": "ghc.family.v649-v6.retained-negatives.correction.v1",
        "x2_operational": 10,
        "effective_at_evidence": 5197,
        "negative_erased": False,
    })
    write_json("retained-negative-register-final.json", {"schema": "ghc.family.v649-v6.retained-negatives.correction-candidate.v1", "inherited_effective": 5109, "x1_operational": 8, "synthetic_executed_rejected": 70, "x2_operational": 10, "effective_at_evidence": 5197, "negative_erased": False})
    write_json("validation/failed-canonical-attempt-01.json", {
        "schema": "ghc.family.v649-v6.failed-canonical-attempt.v1",
        "attempt": 1,
        "head": EVIDENCE,
        "tests_selected": 158,
        "tests_run": 158,
        "tests_passed": 156,
        "failures": [
            "tests.test_ghc_family_v649_v5.TestV649V5Evidence.test_evidence_manifest_matches_head",
            "tests.test_ghc_family_v649_v5.TestV649V5Evidence.test_method_flow_parity",
        ],
        "errors": 0,
        "credited_success": False,
        "result_receipt_written": False,
        "privacy_scan_reached": False,
        "post_success_replay": False,
    })
    write_json("validation/source-local-lifecycle-projection.json", {
        "schema": "ghc.family.v649-v6.source-lifecycle-projection.v1",
        "source_phase": "v649-v5",
        "source_evidence_commit": TAMAR_EVIDENCE,
        "source_final_commit": TAMAR_FINAL,
        "projections": [
            "v649-v5 phase JSON reads bind to the exact v649-v5 evidence commit",
            "v649-v5 HEAD:path evidence-manifest reads bind to the exact v649-v5 evidence commit",
        ],
        "tests_removed": 0,
        "tests_excluded": 0,
        "assertions_weakened": 0,
        "boundary": "Lifecycle projection only; it creates no new source-phase evidence and does not hide the failed aggregate.",
    })
    plan = load("validation/final-validation-plan.json")
    write_json("validation/final-validation-plan.json", {**plan, "selected_test_count": 158, "failed_canonical_attempts_before_success": 1, "successful_passes_used": 0, "post_success_replay": False, "source_local_lifecycle_projection": "validation/source-local-lifecycle-projection.json"})
    write_json("x2/validation-correction-ledger.json", {"schema": "ghc.family.v649-v6.validation-correction.v1", "parent_evidence": EVIDENCE, "failed_aggregate_count": 1, "failed_tests": 2, "tests_removed": 0, "tests_excluded": 0, "method_flow": method_counts, "effective_negatives": 5197, "successful_passes_used": 0, "post_success_replay": False})
    write_json("phase-truth.json", {**load("phase-truth.json"), "schema": "ghc.family.v649-v6.phase-truth.correction.v1", "stage": "x2_validation_correction_candidate", "evidence_commit": EVIDENCE, "failed_canonical_attempts": 1, "single_pass_used": False, "effective_negatives": 5197, "method_flow_methods": 26, "method_flow_failed_witnesses": 18, "method_flow_passing_witnesses": 26, "terminal_route": "PREPARED_NOT_SENT"})
    write_json("orchestration/final-phase-state.json", {**load("orchestration/final-phase-state.json"), "schema": "ghc.family.v649-v6.orchestration.correction.v1", "stage": "validation_correction_candidate", "failed_canonical_attempts": 1, "successful_passes": 0, "terminal_route": "PREPARED_NOT_SENT"})
    write_json("closeout/closeout-candidate.json", {**load("closeout/closeout-candidate.json"), "schema": "ghc.family.v649-v6.closeout-candidate.correction.v1", "failed_canonical_attempts": 1, "canonical_successful_pass_used": False, "ready_for_closeout_runner": False, "terminal_route": "PREPARED_NOT_SENT"})
    update_overviews()

    exclusions = [
        "docs/sylven-arc/v649-v6/validation/correction-staged-manifest.json",
        "docs/sylven-arc/v649-v6/validation/correction-staged-privacy.json",
        "docs/sylven-arc/v649-v6/validation/correction-staged-review.json",
    ]
    paths = [path for path in changed_paths() if path not in exclusions]
    entries = [{"path": path, "git_blob": git("hash-object", f"--path={path}", path), "bytes": (ROOT / path).stat().st_size} for path in paths if (ROOT / path).is_file()]
    scan = privacy(paths + exclusions)
    write_json("validation/correction-staged-privacy.json", scan)
    write_json("validation/correction-staged-manifest.json", {"schema": "ghc.family.v649-v6.correction-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": exclusions, "coverage_boundary": "All validation-correction changes except three self-referential receipts."})
    write_json("validation/correction-staged-review.json", {"schema": "ghc.family.v649-v6.correction-staged-review.v1", "intended_path_count": len(entries) + 3, "manifest_entry_count": len(entries), "self_exclusion_count": 3, "out_of_scope_paths": [], "privacy_confirmed_hits": scan["confirmed_hit_count"], "failed_canonical_attempts_retained": 1, "tests_removed": 0, "tests_excluded": 0, "successful_passes_used": 0, "terminal_route": "PREPARED_NOT_SENT"})
    if scan["confirmed_hit_count"]:
        raise RuntimeError("correction privacy review found confirmed hits")
    print(json.dumps({"paths": len(entries) + 3, "method_flow": method_counts, "effective_negatives": 5197, "privacy_confirmed_hits": 0, "passed": True}, sort_keys=True))


if __name__ == "__main__":
    main()
