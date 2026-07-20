#!/usr/bin/env python3
"""Build the additive Vesper v650-v1 terminal-validator correction."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v650-v1"
EVIDENCE = "95918f8f6d66a6bc9458cf2a7fffb4e2b9a6d85f"
CLOSEOUT = "30b55426db0f1ed646d9474a9ffde10a63c00811"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
FINAL_SELF_EXCLUSIONS = {
    "docs/vesper-arlen/v650-v1/validation/final-owner-manifest.json",
    "docs/vesper-arlen/v650-v1/validation/final-staged-manifest.json",
    "docs/vesper-arlen/v650-v1/validation/final-staged-privacy.json",
    "docs/vesper-arlen/v650-v1/validation/final-staged-review.json",
}


def run(*args: str, check: bool = True, timeout: int = 240) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, check=check, capture_output=True, timeout=timeout,
        text=True, encoding="utf-8", errors="replace",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def status_paths() -> list[str]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    paths: list[str] = []
    for record in (row for row in raw.split("\0") if row):
        value = record[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value.strip('"').replace("\\", "/"))
    return sorted(set(paths))


def append_lifecycle_method() -> dict[str, Any]:
    ledger = PHASE / "method-flow" / "method-flow-ledger-final.json"
    if not ledger.exists():
        shutil.copy2(PHASE / "method-flow" / "method-flow-ledger-x2.json", ledger)
    method_id = "V6501-M23"
    negative_id = "NEG-V6501-LIFECYCLE-001"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = (
            "A static terminal preflight found that the evidence validator would prefix already repository-relative "
            "script and test manifest paths with the phase-doc directory, guaranteeing false mismatches."
        )
        recovery = (
            "Keep the evidence validator byte-frozen, add a corrected final validator, and treat every manifest "
            "repository_path as already repository-relative across owner and evidence manifest domains."
        )
        record = {
            "method_id": method_id, "title": "Retain and correct repository-relative final manifest paths",
            "failure_signature": failure,
            "trigger_preconditions": ["A final manifest entry already contains a repository-relative script or test path."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the defective validator zero pass credit and retain the clean closeout head until an additive corrected validator exists.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["manifest_domain", "evidence_immutability", "single_pass_budget", "failure_retention"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner static preflight and additive recovery only; no canonical-pass, independent-reproduction, or authority credit.",
        }
        record_path = write_json("method-flow/v6501-m23-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "The additive final validator preserved repository-relative manifest paths and the evidence validator remained unchanged."),
        ):
            witness = {
                "witness_id": f"{method_id}-W{suffix}", "method_id": method_id,
                "procedure": procedure, "scope": f"bounded lifecycle {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable manifest-domain evidence without consuming the canonical pass.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Static preflight or additive code witness only; not the canonical pass or independent review.",
            }
            witness_path = write_json(f"method-flow/v6501-m23-w{suffix.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted for the exact manifest-domain defect after retaining one failed and one passing static witness.",
        )
    method_id = "V6501-M24"
    negative_id = "NEG-V6501-LIFECYCLE-002"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = (
            "A combined file-presence, Git-status, and expectation inspection exceeded its bounded wrapper timeout "
            "before returning attributable state."
        )
        recovery = (
            "Split file-presence inspection from Git status and expectation scans; retain the timed-out wrapper, "
            "then accept only the independently completed bounded probes."
        )
        record = {
            "method_id": method_id, "title": "Split overloaded terminal inspections into bounded attributable probes",
            "failure_signature": failure,
            "trigger_preconditions": ["A combined inspection wrapper mixes filesystem, Git, and content scans near a timeout boundary."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the timed-out wrapper zero state or validation credit and leave the closeout head untouched.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["attributable_state", "timeout_retention", "single_pass_budget", "failure_retention"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner inspection recovery only; no canonical-pass, production, or independent-reproduction credit.",
        }
        record_path = write_json("method-flow/v6501-m24-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "The isolated file probe and isolated Git-status probe both completed and returned attributable state."),
        ):
            witness = {
                "witness_id": f"{method_id}-W{suffix}", "method_id": method_id,
                "procedure": procedure, "scope": f"bounded lifecycle {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable terminal-inspection evidence without consuming the canonical pass.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Inspection witness only; not the canonical pass or independent review.",
            }
            witness_path = write_json(f"method-flow/v6501-m24-w{suffix.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted after retaining the combined timeout and witnessing both split bounded probes.",
        )
    method_id = "V6501-M25"
    negative_id = "NEG-V6501-LIFECYCLE-003"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = "The first correction-builder invocation stopped because its closeout constant contained a stale full object identifier."
        recovery = "Resolve the exact closeout object through Git, verify its parent and source-to-head history, then update only the additive builder constant."
        record = {
            "method_id": method_id, "title": "Resolve lifecycle anchors from exact Git objects before additive generation",
            "failure_signature": failure,
            "trigger_preconditions": ["A copied full commit identifier does not equal the canonical lane HEAD."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Stop before generation, give the invocation zero credit, and leave canonical history untouched.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["exact_head", "ancestry", "commit_cap", "failure_retention"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Exact Git-object recovery only; no canonical-pass, validation, or independent-reproduction credit.",
        }
        record_path = write_json("method-flow/v6501-m25-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "Git resolved the exact closeout head, its evidence parent, three source-to-head commits, and zero merges."),
        ):
            witness = {
                "witness_id": f"{method_id}-W{suffix}", "method_id": method_id,
                "procedure": procedure, "scope": f"bounded lifecycle {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Use an attributable exact Git object without consuming the canonical pass.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Anchor-resolution witness only; not the canonical pass or independent review.",
            }
            witness_path = write_json(f"method-flow/v6501-m25-w{suffix.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted after retaining the stale-anchor stop and witnessing exact Git resolution.",
        )
    method_id = "V6501-M26"
    negative_id = "NEG-V6501-LIFECYCLE-004"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = "A repository-wide exact-hash search exceeded its bounded timeout before returning an attributable result."
        recovery = "Search only the named correction builder and phase-local lifecycle surface when the target constant is already known."
        record = {
            "method_id": method_id, "title": "Scope exact-anchor searches to the known lifecycle surface",
            "failure_signature": failure,
            "trigger_preconditions": ["A known constant is searched across the inherited repository rather than its owning file."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the timed-out search zero result credit and avoid repeating repository-wide enumeration.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["bounded_search", "attributable_state", "timeout_retention", "failure_retention"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Phase-local search recovery only; no canonical-pass, validation, or independent-reproduction credit.",
        }
        record_path = write_json("method-flow/v6501-m26-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "The scoped literal search completed and located the stale constant on one exact builder line."),
        ):
            witness = {
                "witness_id": f"{method_id}-W{suffix}", "method_id": method_id,
                "procedure": procedure, "scope": f"bounded lifecycle {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return one attributable phase-local search result without consuming the canonical pass.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Search witness only; not the canonical pass or independent review.",
            }
            witness_path = write_json(f"method-flow/v6501-m26-w{suffix.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted after retaining the broad-search timeout and witnessing the scoped literal search.",
        )
    method_id = "V6501-M27"
    negative_id = "NEG-V6501-LIFECYCLE-005"
    current = json.loads(ledger.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in current["methods"]}:
        failure = (
            "A final static assertion review found that the closeout test admitted only two or three phase commits "
            "even though the sealed protocol and terminal validator allow the fourth correction commit."
        )
        recovery = (
            "Preserve the flawed pushed head, create one additive owner recovery lane from the clean closeout anchor, "
            "and include two, three, or four commits in the closeout cadence assertion before rebuilding the sole fourth commit."
        )
        record = {
            "method_id": method_id, "title": "Align closeout cadence assertions with the sealed four-commit cap",
            "failure_signature": failure,
            "trigger_preconditions": ["A pre-terminal test assertion is stricter than the phase's sealed commit-cap protocol."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Do not consume the canonical pass or rewrite the pushed head; return to the clean closeout anchor in an additive owner lane.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["commit_cap", "no_rewrite", "single_pass_budget", "failure_retention"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Additive same-owner lifecycle recovery only; no canonical-pass or independent-reproduction credit.",
        }
        record_path = write_json("method-flow/v6501-m27-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in (
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "The additive recovery lane remained at the clean closeout anchor and the corrected assertion admitted the sealed fourth commit."),
        ):
            witness = {
                "witness_id": f"{method_id}-W{suffix}", "method_id": method_id,
                "procedure": procedure, "scope": f"bounded lifecycle {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Align the assertion with the sealed cap without rewriting history or consuming the canonical pass.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Static cadence and additive-lane witness only; not the canonical pass or independent review.",
            }
            witness_path = write_json(f"method-flow/v6501-m27-w{suffix.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted after preserving the flawed head and witnessing the additive cadence correction.",
        )
    validation = PHASE / "method-flow" / "method-flow-validation-final.json"
    summary_json = PHASE / "method-flow" / "method-flow-summary-final.json"
    summary_md = PHASE / "method-flow" / "method-flow-summary-final.md"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(validation))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(summary_json), "--markdown-output", str(summary_md))
    return json.loads(summary_json.read_text(encoding="utf-8"))


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def owner_paths() -> list[str]:
    paths = {path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()}
    paths.update(git("ls-files", "scripts/*v650_v1*.py", "tests/test_ghc_family_v650_v1*.py").splitlines())
    for path in status_paths():
        if re.fullmatch(r"scripts/(?:build_)?ghc_family_v650_v1_.*\.py", path):
            paths.add(path)
        if re.fullmatch(r"tests/test_ghc_family_v650_v1.*\.py", path):
            paths.add(path)
    return sorted(path for path in paths if path and (ROOT / path).is_file())


def build_owner_manifest() -> None:
    entries = []
    for relative in owner_paths():
        if relative in FINAL_SELF_EXCLUSIONS:
            continue
        path = ROOT / relative
        entries.append({
            "path": relative, "repository_path": relative,
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "working_bytes": path.stat().st_size,
        })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc.family.v650-v1.final-owner-manifest.v2",
        "hash_domain": "git_path_filtered_blob", "entry_count": len(entries), "entries": entries,
        "self_exclusions": sorted(FINAL_SELF_EXCLUSIONS), "declared_exclusion_count": len(FINAL_SELF_EXCLUSIONS),
        "owner_path_count": len(entries) + len(FINAL_SELF_EXCLUSIONS),
        "boundary": "All public Vesper v650-v1 owner paths except four declared lifecycle self-exclusions; exact committed parity is checked at the final head.",
    })


def build_staged_review() -> dict[str, Any]:
    exclusions = {
        "docs/vesper-arlen/v650-v1/validation/final-staged-manifest.json",
        "docs/vesper-arlen/v650-v1/validation/final-staged-privacy.json",
        "docs/vesper-arlen/v650-v1/validation/final-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    allowed = [
        path for path in paths
        if path.startswith("docs/vesper-arlen/v650-v1/")
        or re.fullmatch(r"scripts/(?:build_)?ghc_family_v650_v1_.*\.py", path)
        or re.fullmatch(r"tests/test_ghc_family_v650_v1.*\.py", path)
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    frozen = set(git("ls-tree", "-r", "--name-only", EVIDENCE).splitlines())
    frozen_changes = sorted(set(paths) & frozen)
    definitions = {
        "scripts/build_ghc_family_v650_v1_correction.py",
        "scripts/ghc_family_v650_v1_final_validate.py",
        "docs/vesper-arlen/v650-v1/validation/final-staged-privacy.json",
    }
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": relative, "bytes": len(data),
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "checkout_sha256": hashlib.sha256(data).hexdigest(),
        })
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/final-staged-privacy.json", {
        "schema": "ghc.family.v650-v1.final-staged-privacy.v2", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
    })
    write_json("validation/final-staged-manifest.json", {
        "schema": "ghc.family.v650-v1.final-staged-manifest.v2", "hash_domain": "git_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    payload = {
        "schema": "ghc.family.v650-v1.final-staged-review.v2",
        "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries),
        "self_exclusion_count": len(exclusions), "out_of_scope_paths": out_of_scope,
        "evidence_frozen_changes": frozen_changes, "privacy_confirmed_hits": len(confirmed),
        "passed": not out_of_scope and not frozen_changes and not confirmed,
    }
    write_json("validation/final-staged-review.json", payload)
    return payload


def update_documents(summary: dict[str, Any]) -> int:
    write_json("lifecycle/retained-negative-register-final.json", {
        "schema": "ghc.family.v650-v1.retained-negatives.final.v1",
        "evidence_effective": 5573, "lifecycle_operational": 5, "effective_final": 5578,
        "negative_erased": False,
        "lifecycle_rows": [
            {
                "negative_id": "NEG-V6501-LIFECYCLE-001",
                "title": "Repository-relative manifest paths would have been prefixed incorrectly by the evidence validator.",
                "state": "retained_recovered", "method_id": "V6501-M23",
            },
            {
                "negative_id": "NEG-V6501-LIFECYCLE-002",
                "title": "A combined terminal inspection wrapper timed out before returning attributable state.",
                "state": "retained_recovered", "method_id": "V6501-M24",
            },
            {
                "negative_id": "NEG-V6501-LIFECYCLE-003",
                "title": "The first correction-builder invocation stopped on a stale closeout object identifier.",
                "state": "retained_recovered", "method_id": "V6501-M25",
            },
            {
                "negative_id": "NEG-V6501-LIFECYCLE-004",
                "title": "A repository-wide exact-hash search timed out before returning attributable state.",
                "state": "retained_recovered", "method_id": "V6501-M26",
            },
            {
                "negative_id": "NEG-V6501-LIFECYCLE-005",
                "title": "A closeout cadence assertion excluded the permitted fourth phase commit.",
                "state": "retained_recovered", "method_id": "V6501-M27",
            },
        ],
    })
    for relative in ("closeout-receipt.json", "phase-truth-closeout-candidate.json"):
        payload = load(relative)
        payload["effective_negatives"] = 5578
        payload["post_evidence_operational_negatives"] = 5
        if relative == "closeout-receipt.json":
            payload["method_fail_witnesses"] = summary["counts"]["witness_results"]["fail"]
            payload["method_pass_witnesses"] = summary["counts"]["witness_results"]["pass"]
        write_json(relative, payload)
    baton_path = PHASE / "handoffs" / "ilyra-fen-v650-v2-activation.md"
    baton = baton_path.read_text(encoding="utf-8")
    for previous in ("5,573", "5,574", "5,575", "5,576", "5,577"):
        baton = baton.replace(previous, "5,578")
    baton = baton.replace(
        "codex/GHC-Family/vesper-arlen-v650-v1-full-tools",
        "codex/GHC-Family/vesper-arlen-v650-v1-terminal-recovery",
    )
    marker = "## Validation and closeout protocol for Ilyra v650-v2"
    correction = (
        "## Final lifecycle correction retained\n\n"
        "A static preflight found that the evidence validator would have prefixed already repository-relative "
        "script and test manifest paths with the phase-doc directory. That defect received zero canonical-pass "
        "credit and remains `NEG-V6501-LIFECYCLE-001`. The evidence validator stayed byte-frozen; an additive "
        "`ghc_family_v650_v1_final_validate.py` corrects only the manifest-path domain. Method Flow now preserves "
        "27 failed witnesses, 27 bounded passing witnesses, and 27 preferred methods. The successor baseline is "
        "5,578 effective negatives. The separate combined-inspection timeout is retained as "
        "`NEG-V6501-LIFECYCLE-002`; its split file and Git probes passed without erasing the failed wrapper. "
        "The stale-anchor stop and broad-search timeout remain retained as `NEG-V6501-LIFECYCLE-003` and "
        "`NEG-V6501-LIFECYCLE-004`; exact Git resolution and the scoped literal search passed without erasure. "
        "The stale closeout cadence assertion remains `NEG-V6501-LIFECYCLE-005`; the flawed pushed head was "
        "preserved and one additive owner recovery lane rebuilt the permitted fourth commit without rewriting it. "
        "These recoveries are not a canonical pass, independent reproduction, "
        "external audit, or authority.\n\n"
    )
    if correction not in baton:
        baton = baton.replace(marker, correction + marker)
    baton_path.write_text(baton, encoding="utf-8", newline="\n")
    baton_words = len(baton.split())
    index = load("tooling/ghc-family-index-final.json")
    index["methods"] = 27
    index["baton_words"] = baton_words
    write_json("tooling/ghc-family-index-final.json", index)
    protocol = load("validation/final-validation-protocol.json")
    protocol["validator"] = "scripts/ghc_family_v650_v1_final_validate.py"
    protocol["preflight_corrections_retained"] = [
        "NEG-V6501-LIFECYCLE-001", "NEG-V6501-LIFECYCLE-002",
        "NEG-V6501-LIFECYCLE-003", "NEG-V6501-LIFECYCLE-004",
        "NEG-V6501-LIFECYCLE-005",
    ]
    write_json("validation/final-validation-protocol.json", protocol)
    seal = load("seal-receipt.json")
    seal["additive_final_validator"] = True
    seal["evidence_validator_modified"] = False
    write_json("seal-receipt.json", seal)
    memory = load("orchestration/applicable-memory-record-final.json")
    memory["portable_guards"].append(
        "Treat final-owner-manifest repository_path values as already repository-relative; never prepend the phase directory."
    )
    write_json("orchestration/applicable-memory-record-final.json", memory)
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_20000": words <= 20000})
    write_json("validation/final-document-cap-receipt.json", {
        "schema": "ghc.family.v650-v1.final-document-cap.v2", "document_count": len(documents),
        "maximum_words": max(row["words"] for row in documents),
        "all_under_20000": all(row["under_20000"] for row in documents),
        "baton_words": baton_words, "baton_within_8000_20000": 8000 <= baton_words <= 20000,
        "documents": documents,
    })
    return baton_words


def main() -> int:
    if git("rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError(f"correction requires exact closeout head {CLOSEOUT}")
    summary = append_lifecycle_method()
    baton_words = update_documents(summary)
    if not 8000 <= baton_words <= 20000:
        raise RuntimeError(f"corrected baton outside 8000..20000 words: {baton_words}")
    build_owner_manifest()
    review = build_staged_review()
    if not review["passed"]:
        raise RuntimeError(f"correction staged review failed: {review}")
    print(json.dumps({
        "correction": "prepared", "head": CLOSEOUT, "baton_words": baton_words,
        "effective_negatives": 5578, "methods": summary["counts"]["methods"],
        "review_paths": review["intended_path_count"], "route": "PREPARED_NOT_SENT",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
