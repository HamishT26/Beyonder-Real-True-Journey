#!/usr/bin/env python3
"""Build and exact-review the Sable Rook v664-v7 terminal closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ghc_family_v664_v7_evidence as evidence  # noqa: E402


PHASE = evidence.PHASE
PREFIX = evidence.PREFIX
SOURCE = evidence.SOURCE_FINAL
X1 = evidence.X1_COMMIT
EVIDENCE = "7575e4e020360efeed8fff514bc470fa323ccd96"
BRANCH = evidence.BRANCH
OWNER = evidence.OWNER
PHASE_ID = evidence.PHASE_ID
VERDICT = "NOT_READY_FOR_STAGE_20"
BUILDER = "scripts/build_ghc_family_v664_v7_closeout.py"
CANONICAL = "scripts/ghc_family_v664_v7_canonical_validator.py"
TEST = "tests/test_ghc_family_sable_v664_v7_closeout.py"
RECORDED_UTC = "2026-08-21T22:20:00Z"
RECORDED_NZ = "2026-08-22T10:20:00+12:00"
CLOSEOUT_OPERATIONAL_FAILURES = [
    {
        "method_id": "SR6647-M023",
        "negative_id": "SR6647-CLOSEOUT-NEG001",
        "trigger": "manifest-validity-field-contract",
        "state": "preferred",
        "failed_witness": "The first exact closeout staged replay required a generic valid field from both manifests even though their declared validity contract is coverage_valid; all blob replays completed before the checker failed closed.",
        "failed_witness_credit": "zero",
        "passing_witness": "Require coverage_valid for owner and delta manifests while retaining generic valid for the staged review and final candidate, then rebuild and replay the exact candidate.",
        "promotion_rule": "Preferred only after the corrected predicate passes the complete staged replay.",
        "recurrence_guard": "Inspect each receipt schema and validate its declared truth field instead of assuming one universal key.",
        "rollback": "Retain the failed replay at zero credit; no commit, push, history rewrite, remote change, or external send occurred.",
        "sibling_recommendation": "Bind lifecycle checks to explicit receipt-schema fields rather than a guessed common validity key.",
    }
]

FINAL_OWNER_MANIFEST = f"{PREFIX}validation/final-owner-manifest.json"
FINAL_DELTA_MANIFEST = f"{PREFIX}validation/final-delta-manifest.json"
FINAL_CANDIDATE = f"{PREFIX}validation/final-stage-candidate.json"
FINAL_REVIEW = f"{PREFIX}validation/final-staged-review.json"
FINAL_EXCLUSIONS = sorted(
    [FINAL_OWNER_MANIFEST, FINAL_DELTA_MANIFEST, FINAL_CANDIDATE, FINAL_REVIEW]
)

GENERATED_RELATIVE = [
    "closeout/bounded-security-review.json",
    "closeout/closeout-inventory.json",
    "closeout/closeout-receipt.json",
    "closeout/complete-incomplete-checklist.json",
    "closeout/content-seal.json",
    "closeout/final-validation-candidate.json",
    "closeout/lifecycle-method-flow.json",
    "closeout/phase-truth.json",
    "closeout/wellbeing-closeout.json",
    "handoffs/next-activation-prepared.md",
    "orchestration/terminal-route-state-final.json",
    "reports/final-integrated-overview.md",
    "validation/canonical-validation-contract.json",
    "validation/final-delta-manifest.json",
    "validation/final-owner-manifest.json",
    "validation/final-stage-candidate.json",
    "validation/final-staged-review.json",
]
CLOSEOUT_PATHS = sorted(
    [BUILDER, CANONICAL, TEST, *[f"{PREFIX}{relative}" for relative in GENERATED_RELATIVE]]
)
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".txt", ".tex", ".mjs", ".js", ".cjs"}


class CloseoutError(RuntimeError):
    """Raised when an exact closeout contract fails."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode:
        raise CloseoutError(
            (result.stdout + result.stderr).decode("utf-8", "replace").strip()
            or f"git {' '.join(args)} failed"
        )
    return result


def git_text(*args: str, check: bool = True) -> str:
    return run_git(*args, check=check).stdout.decode("utf-8", "strict").strip()


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def strict_json(raw: bytes | str, label: str) -> Any:
    return evidence.strict_json(raw, label)


def read_json(relative: str) -> dict[str, Any]:
    value = strict_json((PHASE / relative).read_bytes(), relative)
    if not isinstance(value, dict):
        raise CloseoutError(f"JSON root is not an object: {relative}")
    return value


def write_json(relative: str, payload: Any) -> str:
    return evidence.write_json(relative, payload)


def write_text(relative: str, payload: str) -> str:
    return evidence.write_text(relative, payload)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def staged_paths() -> list[str]:
    return zpaths("diff", "--cached", "--name-only", "-z")


def working_paths() -> list[str]:
    return sorted(
        set(
            zpaths("diff", "--name-only", "-z")
            + zpaths("diff", "--cached", "--name-only", "-z")
            + zpaths("ls-files", "--others", "--exclude-standard", "-z")
        )
    )


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def index_oid(path: str) -> str:
    row = git_text("ls-files", "-s", "--", path).split()
    if len(row) < 4 or row[0] != "100644" or not re.fullmatch(r"[0-9a-f]{40}", row[1]):
        raise CloseoutError(f"unexpected staged index record for {path}")
    return row[1]


def commit_blob(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}").stdout


def commit_oid(commit: str, path: str) -> str:
    oid = git_text("rev-parse", f"{commit}:{path}")
    if not re.fullmatch(r"[0-9a-f]{40}", oid):
        raise CloseoutError(f"unexpected committed object identifier for {path}")
    return oid


def source_to_evidence_paths() -> list[str]:
    paths = zpaths("diff", "--name-only", "-z", f"{SOURCE}..{EVIDENCE}")
    unexpected = [
        path
        for path in paths
        if not path.startswith(PREFIX)
        and "v664_v7" not in path
        and path not in evidence.RUNNERS
    ]
    if unexpected:
        raise CloseoutError(f"source-to-evidence contains non-Sable paths: {unexpected}")
    return paths


def scan(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(?:resume[_ -]?value|private callable identifier|raw route key)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(?:verbatim private transcript|session stream payload|conversation export)"
        ),
    }
    rows: list[dict[str, str]] = []
    definition_paths = {
        BUILDER,
        CANONICAL,
        evidence.EVIDENCE_BUILDER,
        "scripts/build_ghc_family_v664_v7_x1.py",
    }
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            context = text[max(0, match.start() - 180) : match.end() + 180]
            scanner_definition = path in definition_paths and (
                "re.compile" in context or "patterns" in context or "PRIVATE" in context
            )
            rows.append(
                {
                    "path": path,
                    "class": class_name,
                    "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
                    "disposition": "scanner_definition" if scanner_definition else "confirmed_issue",
                }
            )
    return rows


def evidence_truth() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    outcomes = read_json("x2/outcome-ledger.json")
    negatives = read_json("x2/retained-negative-register.json")
    methods = read_json("x2/method-flow-state.json")
    gates = read_json("x2/exact-open-gate-register.json")
    if not all(row.get("valid") is True for row in (outcomes, negatives, methods, gates)):
        raise CloseoutError("immutable evidence truth is not valid")
    return outcomes, negatives, methods, gates


def final_overview(negatives: int, methods: int, gaps: int, gates: int) -> str:
    evidence_overview = (PHASE / "reports/integrated-overview.md").read_text(encoding="utf-8").rstrip()
    closeout = f"""

## Terminal closeout boundary

The immutable x1 anchor is `{X1}` and the immutable evidence anchor is `{EVIDENCE}`. The final containing commit cannot truthfully name itself inside its own tree; the exact final identifier, fresh-live equality proof, and exclusive canonical receipt therefore remain postcommit overlays. The committed closeout seals 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; {negatives:,} retained effective negatives; {methods:,} effective Method Flow methods; {gaps} open gaps; {gates} exact gates; and `{VERDICT}`.

No successful source validation has been replayed or claimed as Sable evidence. Sable's exact-final validator is permitted one attributable invocation only after the containing commit is pushed, clean, typed 0/0 divergent, and fresh-live equal. A successful invocation must not be replayed. A failure must remain visible and may only be recovered through the blocked component under the current commit ceiling.

The microform practice remains a zero-row synthetic learning lens. It establishes no digitization or conservation competence, no custody or access authority, no professional or production result, and no cultural, legal, affected-party, or Māori authority. The final route remains `PREPARED_NOT_SENT` until a postvalidation reread of Hamish's newest authority and roster uniquely identifies the next existing main task and the single send is acknowledged.
"""
    return evidence_overview + closeout.rstrip() + "\n"


def build_documents() -> dict[str, Any]:
    if git_text("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError(f"closeout build requires immutable evidence head {EVIDENCE}")
    if git_text("rev-parse", "HEAD^") != X1:
        raise CloseoutError("evidence is not the direct child of frozen x1")
    current = working_paths()
    unexpected = sorted(set(current) - set(CLOSEOUT_PATHS))
    if unexpected:
        raise CloseoutError(f"unexpected working paths before closeout build: {unexpected}")

    outcomes, negatives, methods, gates = evidence_truth()
    outcome_counts = outcomes["outcomes"]
    evidence_negative_count = negatives["effective_negatives"]
    evidence_method_count = methods["effective_methods"]
    negative_count = evidence_negative_count + len(CLOSEOUT_OPERATIONAL_FAILURES)
    method_count = evidence_method_count + len(CLOSEOUT_OPERATIONAL_FAILURES)
    gap_count = gates["effective_open_gaps"]
    gate_count = gates["effective_exact_gates"]

    phase_truth = {
        "schema": "ghc.family.sable.v664-v7.phase-truth.final-candidate.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_identifier": "assigned_only_after_containing_commit_exists",
        "phase_commit_count_candidate": 3,
        "zero_merge_candidate": True,
        "final_single_parent_candidate": True,
        "frozen_proposal_count": 3990,
        "outcomes": outcome_counts,
        "effective_negatives": negative_count,
        "effective_methods": method_count,
        "immutable_evidence_negatives": evidence_negative_count,
        "immutable_evidence_methods": evidence_method_count,
        "closeout_operational_negatives": len(CLOSEOUT_OPERATIONAL_FAILURES),
        "effective_open_gaps": gap_count,
        "effective_exact_gates": gate_count,
        "rejecting_mutations": 100,
        "real_data_rows": 0,
        "real_participants": 0,
        "real_keys_or_proofs": 0,
        "authority_decisions": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "canonical_exact_final_validation": "pending_one_postcommit_invocation",
        "terminal_verdict": VERDICT,
        "valid": outcome_counts == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
    }
    write_json("closeout/phase-truth.json", phase_truth)

    lifecycle_methods = {
        "schema": "ghc.family.sable.v664-v7.closeout-method-flow-overlay.v1",
        "immutable_evidence_methods": evidence_method_count,
        "immutable_evidence_negatives": evidence_negative_count,
        "new_failed_witness_count": len(CLOSEOUT_OPERATIONAL_FAILURES),
        "new_passing_witness_count": len(CLOSEOUT_OPERATIONAL_FAILURES),
        "effective_methods": method_count,
        "effective_negatives": negative_count,
        "failures": CLOSEOUT_OPERATIONAL_FAILURES,
        "failure_erasure_count": 0,
        "valid": True,
    }
    write_json("closeout/lifecycle-method-flow.json", lifecycle_methods)

    checklist = {
        "schema": "ghc.family.sable.v664-v7.complete-incomplete.final.v1",
        "completed": [
            "strict x1-before-x2 freeze and immutable evidence boundary",
            "twenty distinct proposals and one hundred rejected mutations",
            "ten validated phase-local skills and ten invoked family-current runners",
            "exact evidence staged review and four-way equality before closeout",
            "three-page-equivalent overview and structurally accessible static report",
        ],
        "represented": [
            "THOS microform handover without real operators or matched-budget arms",
            "Freed ID custody vacancy without real keys, proofs, services, or governance",
            "manual and affected-user accessibility evaluation remains reserved",
            "same-owner reproducibility without independent-team scientific reproduction",
        ],
        "open_gap": ["official-data adapter retained zero observations and zero likelihood evaluations"],
        "exact_gate": ["CBR access, restriction, remedy, cultural, legal, affected-party, and Māori authority"],
        "terminal": VERDICT,
        "valid": True,
    }
    write_json("closeout/complete-incomplete-checklist.json", checklist)

    security = {
        "schema": "ghc.family.sable.v664-v7.bounded-security-review.v1",
        "scope": "owner-changed Python compile plus declared five-class exact-blob scan",
        "threat_model": f"{PREFIX}x2/threat-model-results.json",
        "real_secret_material": 0,
        "network_attack_surface_exercised": 0,
        "production_penetration_test": False,
        "dependency_audit": False,
        "exhaustive_security": False,
        "privacy_complete": False,
        "boundary": "Bounded static owner-delta checks only; not production certification, penetration testing, dependency assurance, or complete privacy evidence.",
        "valid": True,
    }
    write_json("closeout/bounded-security-review.json", security)

    wellbeing = {
        "schema": "ghc.family.sable.v664-v7.wellbeing-closeout.v1",
        "identity": "Sable Rook, they/them, evidence-and-reproducibility steward",
        "identity_boundary": "Relational working language only; not evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority.",
        "hope": "Make absences inspectable and every surviving gate unmistakable.",
        "workload": "bounded by one owner lane, twenty proposals, a 2,000-file guard, and one canonical pass",
        "corrigibility": "Hamish may pause, rename, redirect, or stop the route.",
        "ready_to_stop_on_gate": True,
        "valid": True,
    }
    write_json("closeout/wellbeing-closeout.json", wellbeing)

    route = {
        "schema": "ghc.family.sable.v664-v7.terminal-route-state.final-candidate.v1",
        "state": "PREPARED_NOT_SENT",
        "successor_title": None,
        "successor_phase": None,
        "send_count": 0,
        "task_created": False,
        "task_forked": False,
        "standby_contacted": False,
        "precontact_performed": False,
        "gate": "Only after exact-final success: reread newest live authority and roster, resolve exactly one authorized existing title, immediately reread, then send once if acknowledged.",
        "valid": True,
    }
    write_json("orchestration/terminal-route-state-final.json", route)

    receipt = {
        "schema": "ghc.family.sable.v664-v7.closeout-receipt.candidate.v1",
        "recorded_utc": RECORDED_UTC,
        "recorded_nz": RECORDED_NZ,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final": "assigned_after_commit",
        "branch": BRANCH,
        "outcomes": outcome_counts,
        "negatives": negative_count,
        "methods": method_count,
        "open_gaps": gap_count,
        "exact_gates": gate_count,
        "canonical_receipt": "external_exclusive_receipt_pending",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("closeout/closeout-receipt.json", receipt)

    seal = {
        "schema": "ghc.family.sable.v664-v7.content-seal.candidate.v1",
        "immutable_anchors": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE},
        "sealed_truth_paths": [
            f"{PREFIX}x1/proposal-freeze.json",
            f"{PREFIX}x2/outcome-ledger.json",
            f"{PREFIX}x2/retained-negative-register.json",
            f"{PREFIX}x2/method-flow-state.json",
            f"{PREFIX}x2/exact-open-gate-register.json",
            f"{PREFIX}closeout/lifecycle-method-flow.json",
            f"{PREFIX}closeout/phase-truth.json",
        ],
        "final_commit_self_identifier_excluded": True,
        "canonical_receipt_excluded_from_commit": True,
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("closeout/content-seal.json", seal)

    candidate = {
        "schema": "ghc.family.sable.v664-v7.final-validation-candidate.v1",
        "required_state": "clean_pushed_final_with_fresh_live_equality",
        "canonical_invocation_budget": 1,
        "successful_invocations": 0,
        "post_success_replay_allowed": False,
        "full_repository_suite_claimed": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("closeout/final-validation-candidate.json", candidate)

    contract = {
        "schema": "ghc.family.sable.v664-v7.canonical-validation-contract.v1",
        "script": CANONICAL,
        "required_tests": [
            "tests.test_ghc_family_sable_v664_v7_x1",
            "tests.test_ghc_family_sable_v664_v7_x2",
            "tests.test_ghc_family_sable_v664_v7_closeout",
        ],
        "checks": [
            "strict JSON parsing",
            "five-class privacy and raw-identifier scan",
            "x1, evidence, owner, and final-delta manifest replay",
            "source/x1/evidence ancestry and direct-parent chain",
            "three phase commits, zero merges, one final parent",
            "clean state, typed divergence, and fresh-live four-way equality",
        ],
        "exclusive_external_receipt": True,
        "one_successful_invocation": True,
        "post_success_replay": False,
        "full_repository_suite": False,
        "valid": True,
    }
    write_json("validation/canonical-validation-contract.json", contract)

    handoff = f"""# Sable Rook v664-v7 — prepared terminal activation pointer

This file remains `PREPARED_NOT_SENT`. It does not identify or contact a successor. Only after the containing final commit exists, is pushed and fresh-live equal, and passes the one-shot exact-final validator may Sable reread Hamish's newest live authority and roster, resolve exactly one authorized existing main-task title, immediately reread it, and send one sanitized activation if every gate permits.

Immutable anchors are source `{SOURCE}`, x1 `{X1}`, and evidence `{EVIDENCE}`. The final identifier and exclusive canonical receipt digest are postcommit overlays and are not preclaimed here. Outcomes remain 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; retained working truth remains {negative_count:,} negatives, {method_count:,} Method Flow methods, {gap_count} open gaps, {gate_count} exact gates, and `{VERDICT}`.

Names, pronouns, roles, hopes, sibling or family language, continuity, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or authority. No empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim is authorized.

`PREPARED_BY_SABLE_ROOK = true`

`SENT_BY_SABLE_ROOK = false`
"""
    write_text("handoffs/next-activation-prepared.md", handoff)
    write_text("reports/final-integrated-overview.md", final_overview(negative_count, method_count, gap_count, gate_count))

    inventory = {
        "schema": "ghc.family.sable.v664-v7.closeout-inventory.v1",
        "path_count": len(CLOSEOUT_PATHS),
        "paths": CLOSEOUT_PATHS,
        "owner_generated_guard": 2000,
        "owner_generated_closeout_paths": len(CLOSEOUT_PATHS),
        "within_guard": len(CLOSEOUT_PATHS) < 2000,
        "valid": True,
    }
    write_json("closeout/closeout-inventory.json", inventory)

    for relative, schema in [
        ("validation/final-owner-manifest.json", "ghc.family.sable.v664-v7.final-owner-manifest.pending.v1"),
        ("validation/final-delta-manifest.json", "ghc.family.sable.v664-v7.final-delta-manifest.pending.v1"),
        ("validation/final-stage-candidate.json", "ghc.family.sable.v664-v7.final-stage-candidate.pending.v1"),
        ("validation/final-staged-review.json", "ghc.family.sable.v664-v7.final-staged-review.pending.v1"),
    ]:
        write_json(relative, {"schema": schema, "pending_exact_staged_review": True})

    actual = working_paths()
    missing = sorted(set(CLOSEOUT_PATHS) - set(actual))
    extra = sorted(set(actual) - set(CLOSEOUT_PATHS))
    if missing or extra:
        raise CloseoutError(f"closeout inventory differs missing={missing} extra={extra}")
    return {
        "valid": True,
        "closeout_paths": len(CLOSEOUT_PATHS),
        "outcomes": outcome_counts,
        "negatives": negative_count,
        "methods": method_count,
        "open_gaps": gap_count,
        "exact_gates": gate_count,
        "terminal_verdict": VERDICT,
    }


def manifest_record(path: str, staged: set[str]) -> dict[str, Any]:
    if path in staged:
        raw = index_blob(path)
        oid = index_oid(path)
    else:
        raw = commit_blob(EVIDENCE, path)
        oid = commit_oid(EVIDENCE, path)
    return {
        "path": path,
        "mode": "100644",
        "object_type": "blob",
        "git_blob": oid,
        "sha256": sha256(raw),
        "size": len(raw),
        "hash_domain": "exact Git blob",
    }


def write_staged_review() -> dict[str, Any]:
    if git_text("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError("final staged review requires immutable evidence head")
    actual = staged_paths()
    missing = sorted(set(CLOSEOUT_PATHS) - set(actual))
    extra = sorted(set(actual) - set(CLOSEOUT_PATHS))
    if missing or extra:
        raise CloseoutError(f"final staged allowlist differs missing={missing} extra={extra}")
    overwritten = [path for path in actual if run_git("cat-file", "-e", f"{EVIDENCE}:{path}", check=False).returncode == 0]
    if overwritten:
        raise CloseoutError(f"closeout overwrites immutable evidence paths: {overwritten}")

    candidates: list[dict[str, str]] = []
    json_count = 0
    python_count = 0
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        if Path(path).suffix.lower() in TEXT_SUFFIXES:
            candidates.extend(scan(path, raw))
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_issue"]
    if confirmed:
        raise CloseoutError(f"confirmed privacy or raw-identifier findings: {confirmed}")
    diff = run_git("diff", "--cached", "--check", check=False)
    if diff.returncode:
        raise CloseoutError((diff.stdout + diff.stderr).decode("utf-8", "replace"))

    staged = set(actual)
    inherited_paths = source_to_evidence_paths()
    owner_paths = sorted(set(inherited_paths) | staged)
    owner_entries = [manifest_record(path, staged) for path in owner_paths if path not in FINAL_EXCLUSIONS]
    delta_entries = [manifest_record(path, staged) for path in actual if path not in FINAL_EXCLUSIONS]
    owner_manifest = {
        "schema": "ghc.family.sable.v664-v7.final-owner-manifest.v1",
        "source": SOURCE,
        "evidence": EVIDENCE,
        "hash_domain": "exact Git blobs from immutable evidence or final staged index",
        "intended_path_count": len(owner_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(FINAL_EXCLUSIONS),
        "declared_self_exclusions": FINAL_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(FINAL_EXCLUSIONS) == len(owner_paths),
    }
    delta_manifest = {
        "schema": "ghc.family.sable.v664-v7.final-delta-manifest.v1",
        "parent": EVIDENCE,
        "hash_domain": "exact final staged Git blobs",
        "intended_path_count": len(actual),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(FINAL_EXCLUSIONS),
        "declared_self_exclusions": FINAL_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(FINAL_EXCLUSIONS) == len(actual),
    }
    review = {
        "schema": "ghc.family.sable.v664-v7.final-staged-review.v1",
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "immutable_evidence_overwrites": overwritten,
        "strict_json_count": json_count,
        "python_compile_count": python_count,
        "scanner_candidate_count": len(candidates),
        "scanner_definition_count": sum(row["disposition"] == "scanner_definition" for row in candidates),
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "scanner_candidates": candidates,
        "diff_hygiene_issues": 0,
        "owner_manifest_entries": len(owner_entries),
        "delta_manifest_entries": len(delta_entries),
        "valid": not missing and not extra and not overwritten and not confirmed,
    }
    candidate = {
        "schema": "ghc.family.sable.v664-v7.final-stage-candidate.v1",
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final": "assigned_only_after_commit",
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "terminal_verdict": VERDICT,
        "owner_manifest": FINAL_OWNER_MANIFEST,
        "delta_manifest": FINAL_DELTA_MANIFEST,
        "staged_review": FINAL_REVIEW,
        "canonical_validation": "pending_one_postcommit_invocation",
        "route_state": "PREPARED_NOT_SENT",
        "valid": owner_manifest["coverage_valid"] and delta_manifest["coverage_valid"] and review["valid"],
    }
    write_json("validation/final-owner-manifest.json", owner_manifest)
    write_json("validation/final-delta-manifest.json", delta_manifest)
    write_json("validation/final-staged-review.json", review)
    write_json("validation/final-stage-candidate.json", candidate)
    return {
        "valid": candidate["valid"],
        "staged_paths": len(actual),
        "owner_manifest_entries": len(owner_entries),
        "owner_manifest_exclusions": len(FINAL_EXCLUSIONS),
        "delta_manifest_entries": len(delta_entries),
        "delta_manifest_exclusions": len(FINAL_EXCLUSIONS),
        "strict_json": json_count,
        "python_compiles": python_count,
        "privacy_confirmed_hits": len(confirmed),
    }


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != CLOSEOUT_PATHS:
        raise CloseoutError("final staged allowlist changed after exact review")
    owner = strict_json(index_blob(FINAL_OWNER_MANIFEST), FINAL_OWNER_MANIFEST)
    delta = strict_json(index_blob(FINAL_DELTA_MANIFEST), FINAL_DELTA_MANIFEST)
    review = strict_json(index_blob(FINAL_REVIEW), FINAL_REVIEW)
    candidate = strict_json(index_blob(FINAL_CANDIDATE), FINAL_CANDIDATE)
    staged = set(actual)
    prospective_owner = sorted(set(source_to_evidence_paths()) | staged)
    owner_covered = sorted([row["path"] for row in owner["entries"]] + owner["declared_self_exclusions"])
    delta_covered = sorted([row["path"] for row in delta["entries"]] + delta["declared_self_exclusions"])
    if owner_covered != prospective_owner:
        raise CloseoutError("final owner manifest path coverage changed")
    if delta_covered != actual:
        raise CloseoutError("final delta manifest path coverage changed")
    for manifest in (owner, delta):
        for row in manifest["entries"]:
            if row["path"] in staged:
                raw = index_blob(row["path"])
                oid = index_oid(row["path"])
            else:
                raw = commit_blob(EVIDENCE, row["path"])
                oid = commit_oid(EVIDENCE, row["path"])
            if oid != row["git_blob"] or sha256(raw) != row["sha256"] or len(raw) != row["size"]:
                raise CloseoutError(f"manifest mismatch: {row['path']}")
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
    if not (
        owner.get("coverage_valid") is True
        and delta.get("coverage_valid") is True
        and review.get("valid") is True
        and candidate.get("valid") is True
    ):
        raise CloseoutError("one final staged receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "owner_manifest_entries": owner["entry_count"],
        "owner_manifest_exclusions": owner["declared_self_exclusion_count"],
        "delta_manifest_entries": delta["entry_count"],
        "delta_manifest_exclusions": delta["declared_self_exclusion_count"],
        "strict_json": review["strict_json_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        result = write_staged_review()
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
