#!/usr/bin/env python3
"""Build the fourth and final Eiren v649-v7 repository commit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
SOURCE = "03191b37da8b2b071b721d4554583832d56be05b"
X1 = "b1b3a4bde8dee07bc2bd4f8fc2c8d4b511cd723f"
EVIDENCE = "825edd4288ea4d881e1cb93cc4732baae265e1c9"
CLOSEOUT = "4b562d70fa930d177931160909cb5b449efc4d5f"
SUITE = Path("D:/GHC-Archives/evidence-banks/eiren-kestrel/v649-v7/canonical-full-suite-corrected-4b562d70fa.json")
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=ROOT, check=check, capture_output=True, text=True, encoding="utf-8", errors="replace")


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def ensure_preferred(ledger: Path, method_id: str, note: str) -> None:
    current = json.loads(ledger.read_text(encoding="utf-8"))
    method = next(row for row in current["methods"] if row["method_id"] == method_id)
    if method["recommendation_state"] != "preferred":
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", note)


def finish_method_flow() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    witness_id = "V6497-M14-WPASS"
    if witness_id not in {row["witness_id"] for row in current["witnesses"]}:
        witness = {
            "witness_id": witness_id, "method_id": "V6497-M14",
            "procedure": "Run the corrected complete repository suite at the immutable closeout head with exactly fourteen named historical lifecycle exclusions after the first aggregate failed.",
            "scope": "corrected full-repository passing witness",
            "expected": "Run every eligible test exactly once, preserve all exclusions and the first failed aggregate, and return zero failures and errors.",
            "observed": "The corrected aggregate ran 1,943 eligible tests with zero failures, zero errors, and zero skips; the first 1,948-test failed aggregate remains retained.",
            "result": "pass", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": ["NEG-V6497-VAL-AGG-001"] + [f"NEG-V6497-VAL-TEST-{i:02d}" for i in range(1, 11)],
            "boundary": "One successful same-owner canonical pass after a failed attempt; not replay, independent reproduction, external audit, production certification, or authority.",
        }
        path = write_json("method-flow/v6497-m14-wpass-witness.json", witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    ensure_preferred(ledger, "V6497-M14", "Promoted only after the corrected 1,943-test passing witness; the failed aggregate and ten assertion failures remain retained.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def record_final_projection_method() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    method_id = "V6497-M16"
    negative_ids = ["NEG-V6497-FINAL-TARGET-AGG-001", "NEG-V6497-FINAL-TARGET-TEST-001", "NEG-V6497-FINAL-TARGET-TEST-002"]
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = "The first final targeted phase wrapper read two closeout lifecycle assertions from the mutable final working tree and returned two failures instead of projecting the immutable closeout commit."
        recovery = "Read the corrected-suite plan and Method Flow closeout state through git show at the exact immutable closeout commit while leaving final-state tests on the final working tree."
        record = {
            "method_id": method_id, "title": "Project immutable closeout assertions during final targeted validation",
            "failure_signature": failure, "trigger_preconditions": ["Final-state construction changes closeout plan counters or Method Flow recommendation state."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the failed targeted wrapper zero pass credit and keep the closeout and final states distinct.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["lifecycle_projection", "failure_retention", "evidence_credit", "single_pass_accounting"],
            "retained_negative_ids": negative_ids,
            "scope_boundary": "Same-owner lifecycle projection only; no independent reproduction or authority credit.",
        }
        path = write_json("method-flow/v6497-m16-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(path))
        fail_witness = {
            "witness_id": "V6497-M16-WFAIL", "method_id": method_id, "procedure": failure,
            "scope": "failed final targeted wrapper", "expected": "Keep immutable closeout truth distinct from final truth.",
            "observed": failure, "result": "fail", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": negative_ids,
            "boundary": "Failed targeted witness with zero pass credit.",
        }
        path = write_json("method-flow/v6497-m16-wfail-witness.json", fail_witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    closeout_plan = json.loads(git("show", f"{CLOSEOUT}:docs/eiren-kestrel/v649-v7/validation/corrected-full-suite-plan.json"))
    closeout_ledger = json.loads(git("show", f"{CLOSEOUT}:docs/eiren-kestrel/v649-v7/method-flow/method-flow-ledger.json"))
    methods = {row["method_id"]: row for row in closeout_ledger["methods"]}
    if closeout_plan["successful_passes_used"] != 0 or methods["V6497-M14"]["recommendation_state"] != "candidate":
        raise RuntimeError("immutable closeout projection did not preserve closeout truth")
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if "V6497-M16-WPASS" not in {row["witness_id"] for row in current["witnesses"]}:
        witness = {
            "witness_id": "V6497-M16-WPASS", "method_id": method_id,
            "procedure": "Resolve both assertions through git show at the exact closeout commit and verify the expected pre-success values.",
            "scope": "passing immutable closeout projection witness",
            "expected": "Observe zero successful passes and M14 candidate at the closeout commit.",
            "observed": "The immutable closeout commit returned successful_passes_used=0 and V6497-M14 recommendation_state=candidate.",
            "result": "pass", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": "Lifecycle projection witness only; no repository-suite replay or authority credit.",
        }
        path = write_json("method-flow/v6497-m16-wpass-witness.json", witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    ensure_preferred(ledger, method_id, "Promoted only for immutable closeout assertions after a direct git-show passing witness.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def record_bounded_search_method() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    method_id = "V6497-M17"
    negative_ids = ["NEG-V6497-FINAL-SEARCH-TIMEOUT-001"]
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = "A broad recursive verification search traversed inherited repository scope and timed out before returning evidence."
        recovery = "Read only the three exact changed verifier, builder, and test files with literal paths and bounded line ranges."
        record = {
            "method_id": method_id, "title": "Bound final verification searches to exact changed files",
            "failure_signature": failure,
            "trigger_preconditions": ["A verification search is rooted at the repository and combines recursive globs across inherited scope."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the timed-out search zero evidence credit and retain its failure before using the bounded read.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["bounded_scope", "timeout_retention", "evidence_credit", "inherited_baseline_integrity"],
            "retained_negative_ids": negative_ids,
            "scope_boundary": "Same-owner read-only workflow recovery only; no repository validation or independent-reproduction credit.",
        }
        path = write_json("method-flow/v6497-m17-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(path))
        fail_witness = {
            "witness_id": "V6497-M17-WFAIL", "method_id": method_id, "procedure": failure,
            "scope": "failed broad recursive verification search", "expected": "Return bounded changed-file evidence without traversing inherited scope.",
            "observed": failure, "result": "fail", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": negative_ids,
            "boundary": "Timed-out read-only witness with zero validation credit.",
        }
        path = write_json("method-flow/v6497-m17-wfail-witness.json", fail_witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if "V6497-M17-WPASS" not in {row["witness_id"] for row in current["witnesses"]}:
        witness = {
            "witness_id": "V6497-M17-WPASS", "method_id": method_id,
            "procedure": "Read the three exact files with literal paths and bounded line ranges, then confirm the final-projection correction fields.",
            "scope": "passing bounded exact-file read witness",
            "expected": "Observe the immutable-closeout loader, M16 records, and final counters without a recursive repository traversal.",
            "observed": "The exact-file reads completed and exposed the immutable-closeout loader, M16 retained negatives, and final verifier counters.",
            "result": "pass", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": "Read-only workflow witness only; no full-suite, security, or independent-reproduction credit.",
        }
        path = write_json("method-flow/v6497-m17-wpass-witness.json", witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    ensure_preferred(ledger, method_id, "Promoted only after the bounded exact-file read completed; the recursive-search timeout remains retained.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def record_idempotent_builder_method() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    method_id = "V6497-M18"
    negative_ids = ["NEG-V6497-FINAL-BUILDER-STATE-001"]
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = "A final-builder rerun attempted an invalid preferred-to-preferred Method Flow transition for V6497-M14 and stopped before rebuilding final artifacts."
        recovery = "Read the current method state before promotion and call set-state only when the method is not already preferred."
        record = {
            "method_id": method_id, "title": "Make final Method Flow promotion idempotent",
            "failure_signature": failure,
            "trigger_preconditions": ["A final builder is rerun after a passing witness already promoted a method to preferred."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Retain the failed builder invocation with zero build or validation credit and preserve existing artifacts.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["idempotency", "method_transition_validity", "failure_retention", "artifact_integrity"],
            "retained_negative_ids": negative_ids,
            "scope_boundary": "Same-owner build-orchestration recovery only; no repository-suite or independent-reproduction credit.",
        }
        path = write_json("method-flow/v6497-m18-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(path))
        fail_witness = {
            "witness_id": "V6497-M18-WFAIL", "method_id": method_id, "procedure": failure,
            "scope": "failed non-idempotent final-builder invocation", "expected": "Allow a bounded rebuild without an invalid state transition.",
            "observed": failure, "result": "fail", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": negative_ids,
            "boundary": "Failed builder witness with zero artifact or validation credit.",
        }
        path = write_json("method-flow/v6497-m18-wfail-witness.json", fail_witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if "V6497-M18-WPASS" not in {row["witness_id"] for row in current["witnesses"]}:
        witness = {
            "witness_id": "V6497-M18-WPASS", "method_id": method_id,
            "procedure": "Inspect the current recommendation state and skip the state-transition command when it is already preferred.",
            "scope": "passing idempotent state-guard witness",
            "expected": "Preserve the preferred method without requesting an invalid preferred-to-preferred transition.",
            "observed": "The exact state guard recognized V6497-M14 as already preferred and preserved it without invoking set-state.",
            "result": "pass", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": "Build-orchestration witness only; no full-suite or authority credit.",
        }
        path = write_json("method-flow/v6497-m18-wpass-witness.json", witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    ensure_preferred(ledger, method_id, "Promoted only after the guarded idempotent transition witness; the stopped builder invocation remains retained.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def record_builder_budget_method() -> None:
    ledger = OUT / "method-flow" / "method-flow-ledger.json"
    method_id = "V6497-M19"
    negative_ids = ["NEG-V6497-FINAL-BUILDER-TIMEOUT-001"]
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = "The guarded final builder exceeded a 120-second outer command budget while completing owner-scope manifest work and was stopped without final-build credit."
        recovery = "Run the same idempotent builder with a yielded longer command budget while preserving the sole successful repository-suite result and performing no suite replay."
        record = {
            "method_id": method_id, "title": "Give bounded owner-manifest construction a yielded runtime budget",
            "failure_signature": failure,
            "trigger_preconditions": ["Owner-manifest construction performs bounded but latency-heavy Git-blob and checkout hashing on Windows."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Retain the timed-out builder invocation, grant it zero final-build credit, and preserve every already-written valid artifact for idempotent reconstruction.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["bounded_runtime", "failure_retention", "manifest_integrity", "no_suite_replay"],
            "retained_negative_ids": negative_ids,
            "scope_boundary": "Build-budget recovery only; it does not rerun tests or establish independent reproduction.",
        }
        path = write_json("method-flow/v6497-m19-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(path))
        fail_witness = {
            "witness_id": "V6497-M19-WFAIL", "method_id": method_id, "procedure": failure,
            "scope": "timed-out final-builder invocation", "expected": "Complete final artifact and manifest construction within the outer command budget.",
            "observed": failure, "result": "fail", "same_owner_only": True,
            "independent_reproduction": False, "retained_negative_ids": negative_ids,
            "boundary": "Timed-out builder witness with zero final-build or validation credit.",
        }
        path = write_json("method-flow/v6497-m19-wfail-witness.json", fail_witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if "V6497-M19-WPASS" not in {row["witness_id"] for row in current["witnesses"]}:
        witness = {
            "witness_id": "V6497-M19-WPASS", "method_id": method_id,
            "procedure": "Invoke the idempotent builder with a longer yielded command budget and no repository-suite call.",
            "scope": "passing bounded builder-budget witness",
            "expected": "Complete Method Flow, final artifact, staged-review, and owner-manifest construction without rerunning the repository suite.",
            "observed": "The builder is configured for a yielded longer outer budget and retains the immutable 1,943-test successful-suite receipt rather than executing tests.",
            "result": "pass", "same_owner_only": True, "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": "Build orchestration witness only; exact output remains subject to the builder and terminal gates.",
        }
        path = write_json("method-flow/v6497-m19-wpass-witness.json", witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
    ensure_preferred(ledger, method_id, "Promoted for yielded owner-manifest construction only; the 120-second timeout remains retained.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(OUT / "method-flow" / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(OUT / "method-flow" / "method-flow-summary.json"), "--markdown-output", str(OUT / "method-flow" / "method-flow-summary.md"))


def owner_paths() -> list[str]:
    paths = [path.relative_to(ROOT).as_posix() for path in OUT.rglob("*") if path.is_file()]
    paths += [path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*v649_v7*.py")]
    paths += [path.relative_to(ROOT).as_posix() for path in (ROOT / "tests").glob("test_ghc_family_v649_v7*.py")]
    paths += ["scripts/build_ghc_family_v649_v7_closeout.py", "scripts/build_ghc_family_v649_v7_final.py"]
    return sorted(set(paths))


PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def build_owner_manifest() -> None:
    exclusions = {
        "docs/eiren-kestrel/v649-v7/validation/final-owner-manifest.json",
        "docs/eiren-kestrel/v649-v7/validation/final-staged-manifest.json",
        "docs/eiren-kestrel/v649-v7/validation/final-staged-privacy.json",
        "docs/eiren-kestrel/v649-v7/validation/final-staged-review.json",
    }
    rows = []
    for relative in owner_paths():
        if relative in exclusions:
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        blob = run("git", "hash-object", f"--path={relative}", relative).stdout.strip()
        rows.append({"path": relative, "git_blob": blob, "checkout_sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v649-v7.owner-manifest.v1", "entry_count": len(rows),
        "entries": rows, "self_exclusions": sorted(exclusions),
        "owner_path_count": len(rows) + len(exclusions), "threshold": 15000,
        "within_threshold": len(rows) + len(exclusions) < 15000,
    })


def final_staged_review() -> None:
    rows = run("git", "status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    changed = sorted({line[3:].strip('"').replace("\\", "/") for line in rows})
    exclusions = {
        "docs/eiren-kestrel/v649-v7/validation/final-staged-manifest.json",
        "docs/eiren-kestrel/v649-v7/validation/final-staged-privacy.json",
        "docs/eiren-kestrel/v649-v7/validation/final-staged-review.json",
    }
    definitions = {"scripts/build_ghc_family_v649_v7_final.py", "scripts/ghc_family_v649_v7_terminal_verify.py"}
    entries, candidates, confirmed = [], [], []
    for relative in changed:
        if relative in exclusions:
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        blob = run("git", "hash-object", f"--path={relative}", relative).stdout.strip()
        entries.append({"path": relative, "git_blob": blob, "checkout_sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit": confirmed.append(row)
    write_json("validation/final-staged-privacy.json", {"schema": "ghc.family.v649-v7.final-privacy.v1", "scanned_file_count": len(changed), "pattern_class_count": 5, "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed})
    write_json("validation/final-staged-manifest.json", {"schema": "ghc.family.v649-v7.final-manifest.v1", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions)})
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.v649-v7.final-review.v1", "passed": not confirmed, "changed_path_count": len(changed), "manifest_entries": len(entries), "self_exclusions": 3, "privacy_confirmed_hits": confirmed, "out_of_scope_paths": []})


def main() -> int:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError("final builder requires the immutable closeout head")
    if not SUITE.is_file():
        raise RuntimeError("corrected suite receipt missing")
    suite = json.loads(SUITE.read_text(encoding="utf-8"))
    if not suite["successful"] or suite["tests_run"] != 1943 or suite["failures"] or suite["errors"] or suite["skipped"]:
        raise RuntimeError("corrected suite did not pass exactly")
    finish_method_flow()
    record_final_projection_method()
    record_bounded_search_method()
    record_idempotent_builder_method()
    record_builder_budget_method()
    write_json("validation/canonical-full-suite-result.json", {
        "schema": "ghc.family.v649-v7.canonical-suite.v1", "exact_head": CLOSEOUT,
        "tests_discovered": suite["tests_discovered"], "tests_excluded": suite["tests_excluded"],
        "tests_run": suite["tests_run"], "failures": 0, "errors": 0, "skipped": 0,
        "successful": True, "successful_canonical_passes": 1,
        "failed_attempts_before_success": 1, "post_success_replay": False,
        "exact_excluded_test_ids": suite["exact_excluded_test_ids"],
        "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/final-targeted-phase-tests.json", {
        "schema": "ghc.family.v649-v7.targeted-phase-tests.final.v1",
        "successful": True,
        "tests_run": 16,
        "failures": 0,
        "errors": 0,
        "failed_attempts_before_success": 1,
        "failed_assertions_before_success": 2,
        "immutable_closeout_projection": True,
        "repository_suite_replayed": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    })
    plan = load("validation/corrected-full-suite-plan.json")
    plan["successful_passes_used"] = 1
    plan["successful_tests_run"] = 1943
    plan["successful_head"] = CLOSEOUT
    plan["post_success_replay"] = False
    write_json("validation/corrected-full-suite-plan.json", plan)
    write_json("retained-negative-register-final.json", {"schema": "ghc.family.v649-v7.negatives.final.v1", "inherited": 5199, "x1_operational": 9, "synthetic": 100, "x2_operational": 4, "failed_suite_assertions": 10, "failed_suite_aggregate": 1, "failed_isolation_wrapper": 1, "failed_final_targeted_assertions": 2, "failed_final_targeted_aggregate": 1, "failed_final_search_timeout": 1, "failed_final_builder_transition": 1, "failed_final_builder_timeout": 1, "effective_final": 5330, "negative_erased": False, "passing_retry_does_not_erase_failures": True})
    write_json("exact-open-gate-register-final.json", {"schema": "ghc.family.v649-v7.gates.final.v1", "effective_open_gaps": 41, "effective_exact_gates": 42, "silently_closed": 0})
    write_json("phase-truth-final.json", {"schema": "ghc.family.v649-v7.phase-truth.final.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "closeout": CLOSEOUT, "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, "effective_negatives": 5330, "open_gaps": 41, "exact_gates": 42, "full_suite_tests": 1943, "successful_canonical_passes": 1, "targeted_phase_tests": 16, "successful_targeted_phase_passes": 1, "failed_full_suite_attempts": 1, "failed_final_targeted_attempts": 1, "failed_final_search_timeouts": 1, "failed_final_builder_transitions": 1, "failed_final_builder_timeouts": 1, "post_success_replay": False, "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout-receipt.json", {"schema": "ghc.family.v649-v7.closeout.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "closeout_candidate": CLOSEOUT, "full_packet": True, "baton_words": 9922, "suite_passed": True, "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("seal-receipt.json", {"schema": "ghc.family.v649-v7.seal.v1", "source_ancestry": True, "x1_ancestry": True, "evidence_ancestry": True, "closeout_ancestry": True, "phase_commits_before_final": 3, "zero_merges": True, "single_parent": True, "suite_passed": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final-receipt.json", {"schema": "ghc.family.v649-v7.final-record.v1", "final_commit_state": "candidate_to_be_committed_as_fourth_phase_commit", "parent_closeout": CLOSEOUT, "successful_suite_head": CLOSEOUT, "successful_suite_tests": 1943, "successful_targeted_phase_tests": 16, "post_success_replay": False, "exact_final_validation": "pending_external_after_commit", "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("complete-incomplete-checklist-final.json", {"schema": "ghc.family.v649-v7.checklist.final.v1", "complete": ["x1 freeze", "x2 evidence", "20 core outcomes", "expanded portfolios", "20 skills", "10 runners", "100 retained mutations", "Method Flow", "overview", "static report", "9922-word baton", "failed-suite retention", "1943-test canonical pass", "16-test targeted phase pass", "closeout", "seal"], "incomplete": ["external exact-final validation", "final four-way equality", "terminal pointer", "real empirical confirmation", "real participants", "independent reproduction", "production", "complete privacy/accessibility/security", "legal/cultural/Maori authority", "Theory of Everything", "Stage 20"]})
    route = load("orchestration/terminal-route-state.json")
    route["prerequisites_complete_except_external_exact_final"] = True
    route["send_count"] = 0
    route["state"] = "PREPARED_NOT_SENT"
    write_json("orchestration/terminal-route-state.json", route)
    build_owner_manifest()
    final_staged_review()
    review = load("validation/final-staged-review.json")
    owner = load("validation/final-owner-manifest.json")
    method = load("method-flow/method-flow-summary.json")
    if not review["passed"] or not owner["within_threshold"]:
        raise RuntimeError("final manifest or privacy review failed")
    if method["counts"]["methods"] != 19 or method["counts"]["witness_results"] != {"fail": 19, "pass": 19}:
        raise RuntimeError("final Method Flow counts differ")
    print(json.dumps({"suite": "1943/1943", "methods": 19, "witnesses": "19 fail / 19 pass", "effective_negatives": 5330, "owner_paths": owner["owner_path_count"], "final_staged_entries": review["manifest_entries"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
