"""Build and seal Liora Venn v672-v6 closeout artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts import build_ghc_family_liora_venn_v672_v6_x1 as x1
from scripts import build_ghc_family_liora_venn_v672_v6_x2 as x2


ROOT = x1.ROOT
OWNER_ROOT = x1.OWNER_ROOT
CLOSEOUT_ROOT = OWNER_ROOT / "closeout"
VALIDATION_ROOT = OWNER_ROOT / "validation"
HANDOFF_ROOT = OWNER_ROOT / "handoffs"
ORCHESTRATION_ROOT = OWNER_ROOT / "orchestration"
FINAL_ROOT = OWNER_ROOT / "final"
SEAL_ROOT = OWNER_ROOT / "seal"
EVIDENCE_COMMIT = "4ead23fe0b39033d9cb7caa1595a9b4c03741630"
BOUNDARY = x1.BOUNDARY
OWNER = x1.OWNER
PHASE = x1.PHASE
BRANCH = x1.BRANCH
SOURCE_FINAL = x1.SOURCE_FINAL
X1_COMMIT = x2.X1_COMMIT

CLOSEOUT_FAILURES = [
    {
        "negative_id": "LV6726-CLOSE-N001",
        "method_id": "LV6726-M030",
        "helper": "ghc_family_canonical_aggregate_preflight.py",
        "observed": "The installed canonical-preflight skill named a helper absent from both its package and the exact repository tree.",
    },
    {
        "negative_id": "LV6726-CLOSE-N002",
        "method_id": "LV6726-M031",
        "helper": "ghc_family_manifest_privacy_tribunal.py",
        "observed": "The installed canonical-success-latch skill named a helper absent from both its package and the exact repository tree.",
    },
    {
        "negative_id": "LV6726-CLOSE-N003",
        "method_id": "LV6726-M032",
        "helper": "ghc_family_v662_v3_2_remaster_canonical.py",
        "observed": "The installed terminal-route-gate skill named a helper absent from both its package and the exact repository tree.",
    },
    {
        "negative_id": "LV6726-CLOSE-N004",
        "method_id": "LV6726-M033",
        "helper": "ghc_family_complete_suite_orchestrator.py",
        "observed": "The installed external-failure-overlay skill named a helper absent from both its package and the exact repository tree.",
    },
    {
        "negative_id": "LV6726-CLOSE-N005",
        "method_id": "LV6726-M034",
        "helper": "first_staged_seal_process",
        "observed": "The first staged-seal process exceeded its initial output window and then exited without producing any of the four self-artifacts; its projected output was not retained.",
        "recovery": "Preserve the uncertain process as a failed witness, inspect process and artifact state, then run the read-only privacy component directly before one bounded staged-seal retry.",
        "recovery_observed": "The original process was absent and all four self-artifacts were absent; the diagnostic and bounded retry are separate witnesses rather than retroactive pass credit.",
    },
]

CLOSEOUT_RECOVERIES = [
    {
        "witness_id": f"LV6726-CLOSE-WP{index:03d}",
        "method_id": failure["method_id"],
        "retained_negative_ids": [failure["negative_id"]],
        "result": "pass",
        "procedure": failure.get("recovery", "Apply the complete installed SKILL.md contract directly through owner-local exact-head, manifest, privacy, latch, or route checks without inventing a helper or broadening scope."),
        "observed": failure.get("recovery_observed", "The equivalent bounded guard is represented in the final builder, final tests, and one-shot external validator; the full repository suite remains unrun."),
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    for index, failure in enumerate(CLOSEOUT_FAILURES, 1)
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    x1.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    x1.write_text(path, text)


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def closeout_counts() -> dict[str, int]:
    x2_counts = load("docs/liora-venn/v672-v6/x2/phase-truth.json")["effective_counts"]
    return {
        **x2_counts,
        "effective_negatives": x2_counts["effective_negatives"] + len(CLOSEOUT_FAILURES),
        "effective_methods": x2_counts["effective_methods"] + len(CLOSEOUT_RECOVERIES),
        "failed_witnesses": x2_counts["failed_witnesses"] + len(CLOSEOUT_FAILURES),
        "bounded_passing_witnesses": x2_counts["bounded_passing_witnesses"] + len(CLOSEOUT_RECOVERIES),
    }


def method_flow_final() -> dict[str, Any]:
    flow = load("docs/liora-venn/v672-v6/x2/method-flow-evidence.json")
    closeout_methods = []
    for failure, recovery in zip(CLOSEOUT_FAILURES, CLOSEOUT_RECOVERIES, strict=True):
        closeout_methods.append(
            {
                "method_id": failure["method_id"],
                "title": f"Direct contract fallback for absent {failure['helper']}",
                "state": "preferred",
                "trigger": failure["observed"],
                "recovery": recovery["procedure"],
                "retained_negative_ids": [failure["negative_id"]],
                "validation_witness_ids": [recovery["witness_id"]],
                "recurrence_guard": "Inspect installed package contents before assuming a named helper exists; never invent a substitute or broaden to a full-suite run.",
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    return {
        "schema": "ghc.family.liora-venn.v672-v6.method-flow-final.v1",
        "owner": x1.OWNER,
        "phase": x1.PHASE,
        "startup_methods": flow["startup_methods"],
        "startup_witnesses": flow["startup_witnesses"],
        "x2_preferred_methods": flow["x2_preferred_methods"],
        "x2_operational_failures": flow["x2_operational_failures"],
        "x2_operational_recoveries": flow["x2_operational_recoveries"],
        "closeout_methods": closeout_methods,
        "closeout_failures": CLOSEOUT_FAILURES,
        "closeout_recoveries": CLOSEOUT_RECOVERIES,
        "external_witness_registers": flow["external_witness_registers"],
        "effective_counts": closeout_counts(),
        "failed_witness_non_erasure": True,
        "boundary": BOUNDARY,
    }


def build() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    if branch != x1.BRANCH or head != EVIDENCE_COMMIT:
        raise RuntimeError(f"closeout requires exact immutable evidence {EVIDENCE_COMMIT}; got {branch} at {head}")
    if git_text("status", "--porcelain=v1", "--untracked-files=no"):
        raise RuntimeError("tracked worktree state changed before closeout build")
    if git_text("rev-parse", f"{EVIDENCE_COMMIT}^") != x2.X1_COMMIT:
        raise RuntimeError("evidence parent mismatch")

    phase_x2 = load("docs/liora-venn/v672-v6/x2/phase-truth.json")
    counts = closeout_counts()
    flow = method_flow_final()
    outcomes = phase_x2["outcomes"]
    built_at = now()

    write_json(CLOSEOUT_ROOT / "method-flow-final.json", flow)
    write_json(
        CLOSEOUT_ROOT / "phase-truth.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.phase-truth.final-candidate.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "source_final": x1.SOURCE_FINAL,
            "x1_commit": x2.X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": "PENDING_FINAL_COMMIT",
            "outcomes": outcomes,
            "effective_counts": counts,
            "primary_pillar": x1.PRIMARY_PILLAR,
            "secondary_pillars": x1.SECONDARY_PILLARS,
            "practice": x1.PRACTICE,
            "real_people": 0,
            "real_objects_or_materials": 0,
            "real_observations_or_measurements": 0,
            "real_identity_events": 0,
            "external_actions": 0,
            "authority_acts": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "full_repository_suite": "not_run_not_claimed",
            "canonical_state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
            "terminal_route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        CLOSEOUT_ROOT / "retained-negative-register.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.retained-negative-register.v1",
            "source_repository_sealed_negatives": x1.ACTIVATION_COUNTS["effective_negatives"],
            "liora_startup_and_lane_failures": 11,
            "liora_rejecting_mutations": 160,
            "liora_x2_operational_failures": 1,
            "liora_closeout_operational_failures": len(CLOSEOUT_FAILURES),
            "liora_additive_failures": 11 + 160 + 1 + len(CLOSEOUT_FAILURES),
            "effective_negatives": counts["effective_negatives"],
            "effective_failed_witnesses": counts["failed_witnesses"],
            "failed_witnesses_promoted": 0,
            "retained_registers": [
                "docs/liora-venn/v672-v6/x1/method-flow-startup.json",
                "docs/liora-venn/v672-v6/x2/mutation-register.json",
                "docs/liora-venn/v672-v6/x2/method-flow-evidence.json",
                "docs/liora-venn/v672-v6/closeout/method-flow-final.json",
            ],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        CLOSEOUT_ROOT / "gate-register.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.gate-register.final-candidate.v1",
            "source_open_gaps": x1.ACTIVATION_COUNTS["open_gaps"],
            "phase_open_gaps": ["LV6726-N037", "LV6726-N038"],
            "effective_open_gaps": counts["open_gaps"],
            "source_exact_gates": x1.ACTIVATION_COUNTS["exact_gates"],
            "phase_exact_gates": ["LV6726-N039", "LV6726-N040"],
            "effective_exact_gates": counts["exact_gates"],
            "all_inherited_and_phase_gates_retained": True,
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        CLOSEOUT_ROOT / "lifecycle-replay.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.lifecycle-replay.final-candidate.v1",
            "source": x1.SOURCE_FINAL,
            "x1": x2.X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "PENDING_FINAL_COMMIT",
            "verified_direct_parents": {
                "x1_parent": git_text("rev-parse", f"{x2.X1_COMMIT}^"),
                "evidence_parent": git_text("rev-parse", f"{EVIDENCE_COMMIT}^"),
            },
            "current_phase_commits": int(git_text("rev-list", "--count", f"{x1.SOURCE_FINAL}..{EVIDENCE_COMMIT}")),
            "expected_final_phase_commits": 3,
            "current_merges": int(git_text("rev-list", "--merges", "--count", f"{x1.SOURCE_FINAL}..{EVIDENCE_COMMIT}")),
            "expected_final_merges": 0,
            "strict_x1_before_x2": True,
            "x1_pushed_clean_four_way_equal_before_x2": True,
            "evidence_pushed_clean_four_way_equal_before_closeout": True,
            "boundary": "Repository lifecycle evidence only; canonical and terminal route remain pending.",
        },
    )
    write_json(
        CLOSEOUT_ROOT / "lifecycle-test-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.lifecycle-test-receipt.v1",
            "x1": {"commit": x2.X1_COMMIT, "tests": 21, "failures": 0, "errors": 0, "lifecycle_context": "planning-only staged x1", "credited_runs": 1},
            "evidence": {"commit": EVIDENCE_COMMIT, "tests": 22, "failures": 0, "errors": 0, "lifecycle_context": "staged x2 evidence", "credited_runs": 1},
            "receipt_class": "same-owner task-observed lifecycle evidence",
            "full_repository_suite": "not_run_not_claimed",
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    overview = f"""# Liora Venn v672-v6 final integrated overview

Liora Venn (she/they) is relational working language for a {x1.ROLE}, with the hope to {x1.HOPE}. {x1.IDENTITY_BOUNDARY}

## Lifecycle and source

The immutable source is Orin Thale v672-v5 exact final `{x1.SOURCE_FINAL}`. Liora planning-only x1 is `{x2.X1_COMMIT}` and immutable x2 evidence is `{EVIDENCE_COMMIT}`. X1 was committed, pushed, clean, typed 0/0 divergent, and fresh-live four-way equal before x2. Evidence received the same gate before closeout. The final commit is intentionally pending in this committed candidate; exact-final facts belong to the later external canonical receipt.

## Bounded outcome truth

The declared proposal chain is 6,150 rows. Liora outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered rejecting mutations executed, were rejected, and remain zero-credit failed witnesses with separate bounded rejection witnesses. Twenty owner-local skills were initialized through the official skill-creator workflow, customized, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current `ghc_family_*` runners were built and accepting/rejecting smoke-used.

The effective closeout overlay is {counts['effective_negatives']:,} negatives, {counts['effective_methods']:,} Method Flow methods, {counts['failed_witnesses']:,} failed witnesses, {counts['bounded_passing_witnesses']:,} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. Orin's sealed source counts remain unchanged. Four absent helper-script failures and one failed first staged-seal process remain retained with separate bounded recoveries; no helper was invented and no full-suite run was substituted.

## Practice and pillar boundaries

{x1.PRIMARY_PILLAR} is primary through {x1.PRACTICE}. The phase used no real person, paper, bath, pigment, surfactant, tool, pattern, observation, measurement, treatment, publication, identity event, participant, professional decision, external write, or authority act. Current official sources supplied vocabulary and refusal conditions only.

GMUT remains a typed scalar-tensor and EFT research-model family with no datum, likelihood, posterior, force, prediction, constraint, empirical confirmation, stability theorem, quantum or ultraviolet completion, or Theory of Everything. THOS remains a synthetic proxy without governed participants or operators, preregistered blind matched-budget real arms, safety monitoring, appropriate statistics, and independent review. Freed ID remains zero-key and nonproduction without real standards-conformant keys and proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, professional, chemical, conservation, publication, accessibility, remedy, legal, cultural, traditional-knowledge, affected-party, Maori wording, Maori data-governance, and Maori authority decisions remain exact-gated.

## Validation and terminal state

The full repository suite was not run and remains outside this non-Eiren phase. Same-owner validation is not independent reproduction, external audit, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, legal or cultural ratification, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.

The route remains `PREPARED_NOT_SENT`. Canonical state at commit remains `NOT_RUN_PENDING_EXACT_FINAL_GATE`. The terminal verdict is exactly `{x1.TERMINAL_VERDICT}`.
"""
    write_text(CLOSEOUT_ROOT / "final-integrated-overview.md", overview)
    write_text(
        CLOSEOUT_ROOT / "accessible-final-report.html",
        f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Liora Venn v672-v6 final candidate</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Liora Venn v672-v6 final candidate</h1></header><main id="main">
<section aria-labelledby="scope"><h2 id="scope">Scope</h2><p>{x1.PRACTICE}. {BOUNDARY}</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Outcomes</h2><ul><li>Completed: 28</li><li>Represented: 8</li><li>Open gap: 2</li><li>Exact gate: 2</li></ul></section>
<section aria-labelledby="counts"><h2 id="counts">Effective evidence counts</h2><p>{counts['effective_negatives']} negatives; {counts['effective_methods']} methods; {counts['failed_witnesses']} failed witnesses; {counts['bounded_passing_witnesses']} bounded passing witnesses; {counts['open_gaps']} open gaps; {counts['exact_gates']} exact gates.</p></section>
<section aria-labelledby="limits"><h2 id="limits">Limits</h2><p>The full repository suite, independent reproduction, real material evaluation, professional review, affected-user evaluation, complete privacy or accessibility assurance, exhaustive security, legal or cultural ratification, and Maori-authority review are absent or gated.</p></section>
<section aria-labelledby="state"><h2 id="state">Terminal state</h2><p>PREPARED_NOT_SENT. NOT_RUN_PENDING_EXACT_FINAL_GATE. {x1.TERMINAL_VERDICT}.</p></section>
</main></body></html>
""",
    )
    write_text(
        HANDOFF_ROOT / "tamar-vey-v672-v7-activation-candidate.md",
        f"""# Liora Venn v672-v6 to Tamar Vey v672-v7 activation candidate

`PREPARED_NOT_SENT`

This sanitized repository candidate is inert and contains no task identifier, private route, transcript, screenshot, session stream, credential, key, token, private callable identifier, private application state, or private absolute path. It neither discovers nor contacts a successor.

Immutable source: Orin v672-v5 `{x1.SOURCE_FINAL}`. Liora x1: `{x2.X1_COMMIT}`. Liora evidence: `{EVIDENCE_COMMIT}`. The exact Liora final and external canonical receipt do not yet exist and are not invented here.

Prospective route: only after a clean pushed exact-final Liora v672-v6, fresh-live equality, and one successful non-replayed owner-scoped canonical aggregate may Liora refresh live authority and roster, uniquely resolve and immediately reread the existing exact-title `Tamar Vey` task, apply duplicate and pause guards, and send one sanitized activation for Tamar-only v672-v7. Stop on absence, ambiguity, pause, redirect, rename, standby, usage exhaustion, missing acknowledgement, duplicate activation, or any protected gate.

Phase truth: exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`; {counts['effective_negatives']} effective negatives; {counts['effective_methods']} methods; {counts['failed_witnesses']} failed witnesses; {counts['bounded_passing_witnesses']} bounded passing witnesses; {counts['open_gaps']} gaps; {counts['exact_gates']} gates; `{x1.TERMINAL_VERDICT}`. The complete repository suite was not run. Same-owner evidence is not independent reproduction or authority.
""",
    )
    write_json(
        ORCHESTRATION_ROOT / "terminal-route-state.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.terminal-route-state.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "state": "PREPARED_NOT_SENT",
            "prospective_successor_exact_title": "Tamar Vey",
            "prospective_successor_phase": "v672-v7",
            "successor_contacted": False,
            "task_created_or_forked": False,
            "standby_contacted": False,
            "send_count": 0,
            "terminal_gate_required": True,
            "canonical_success_required": True,
            "fresh_live_route_refresh_required": True,
            "boundary": "Repository preparation only; live acknowledged delivery is separate evidence.",
        },
    )
    write_json(
        FINAL_ROOT / "canonical-invocation-state.json",
        {
            "schema": "ghc.family.canonical-invocation-state.v3",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
            "attempts_at_commit": 0,
            "successes_at_commit": 0,
            "invocation_limit": 1,
            "replay_after_success": False,
            "external_receipt_required": True,
            "full_repository_suite": "not_run_not_claimed",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        VALIDATION_ROOT / "final-validation-prereceipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.final-validation-prereceipt.v1",
            "built_at": built_at,
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "source": x1.SOURCE_FINAL,
            "x1": x2.X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "final": "PENDING_FINAL_COMMIT",
            "owner_scope_only": True,
            "full_repository_suite": "not_run_not_claimed",
            "canonical_invoked": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    seal_targets = [
        "docs/liora-venn/v672-v6/closeout/phase-truth.json",
        "docs/liora-venn/v672-v6/closeout/method-flow-final.json",
        "docs/liora-venn/v672-v6/closeout/retained-negative-register.json",
        "docs/liora-venn/v672-v6/closeout/gate-register.json",
        "docs/liora-venn/v672-v6/closeout/lifecycle-replay.json",
        "docs/liora-venn/v672-v6/closeout/final-integrated-overview.md",
        "docs/liora-venn/v672-v6/closeout/accessible-final-report.html",
        "docs/liora-venn/v672-v6/handoffs/tamar-vey-v672-v7-activation-candidate.md",
        "docs/liora-venn/v672-v6/orchestration/terminal-route-state.json",
        "docs/liora-venn/v672-v6/final/canonical-invocation-state.json",
    ]
    write_json(
        SEAL_ROOT / "content-seal-candidate.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.content-seal.candidate.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "hash_domain": "working_tree_utf8_or_exact_bytes_before_final_commit",
            "target_count": len(seal_targets),
            "targets": [
                {"path": relative, "bytes": len((ROOT / relative).read_bytes()), "sha256": sha256((ROOT / relative).read_bytes())}
                for relative in seal_targets
            ],
            "canonical_invoked": False,
            "successor_contacted": False,
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_text(
        CLOSEOUT_ROOT / "README.md",
        f"""# Liora Venn v672-v6 closeout candidate

Final-candidate documentation from immutable evidence `{EVIDENCE_COMMIT}`. The exact final commit and external canonical receipt remain pending. Route state is `PREPARED_NOT_SENT`; terminal verdict is `{x1.TERMINAL_VERDICT}`.
""",
    )
    files_before_receipt = sorted(path.relative_to(ROOT).as_posix() for path in OWNER_ROOT.rglob("*") if path.is_file())
    write_json(
        CLOSEOUT_ROOT / "build-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.closeout-build-receipt.v1",
            "built_at": now(),
            "source": x1.SOURCE_FINAL,
            "x1": x2.X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "owner_files_before_receipt": len(files_before_receipt),
            "owner_files_after_receipt": len(files_before_receipt) + 1,
            "outcomes": outcomes,
            "effective_counts": counts,
            "closeout_failure_count": len(CLOSEOUT_FAILURES),
            "closeout_recovery_count": len(CLOSEOUT_RECOVERIES),
            "canonical_invoked": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "valid": True,
            "boundary": BOUNDARY,
        },
    )
    return {"outcomes": outcomes, "effective_counts": counts, "closeout_failures": len(CLOSEOUT_FAILURES), "closeout_recoveries": len(CLOSEOUT_RECOVERIES), "valid": True}


def _blob_for_path(path: str, staged: set[str]) -> bytes:
    return git("show", f":{path}").stdout if path in staged else git("show", f"HEAD:{path}").stdout


def _oid_for_path(path: str, staged: set[str]) -> str:
    return git_text("rev-parse", f":{path}") if path in staged else git_text("rev-parse", f"HEAD:{path}")


def privacy_scan(paths: list[str], staged: set[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{5,}-[a-f0-9-]{12,}\b", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\\\|C:/Users/|D:/GHC-Archives/)", re.I),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "private_callable_identifier": re.compile(r"\b(?:mcp__|codex_app__)[A-Za-z0-9_]+\b"),
        "personal_identifier": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b\+?\d[\d ()-]{8,}\d\b", re.I),
    }
    text_suffixes = {".md", ".json", ".html", ".yaml", ".yml", ".py", ".txt"}
    scanner_sources = {
        "scripts/build_ghc_family_liora_venn_v672_v6_final.py",
        "scripts/validate_ghc_family_liora_venn_v672_v6_final.py",
        "tests/test_ghc_family_liora_venn_v672_v6_final.py",
        "tests/test_ghc_family_liora_venn_v672_v6_x1.py",
        "tests/test_ghc_family_liora_venn_v672_v6_x2.py",
    }
    candidates = []
    confirmed = []
    scanned = 0
    for path in paths:
        if Path(path).suffix.lower() not in text_suffixes:
            continue
        data = _blob_for_path(path, staged)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for class_name, pattern in classes.items():
            for match in pattern.finditer(text):
                line_start = text.rfind("\n", 0, match.start()) + 1
                line_end = text.find("\n", match.end())
                if line_end < 0:
                    line_end = len(text)
                line = text[line_start:line_end]
                scanner_definition = path in scanner_sources and (
                    "re.compile(" in line
                    or path.startswith("tests/")
                )
                row = {
                    "class": class_name,
                    "path": path,
                    "classification": "scanner_definition_or_synthetic_test" if scanner_definition else "confirmed_payload",
                }
                candidates.append(row)
                if not scanner_definition:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.liora-venn.v672-v6.staged-privacy.v1",
        "class_count": len(classes),
        "classes": list(classes),
        "scanned_text_files": scanned,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "scanner_definitions_separated": True,
        "valid": not confirmed,
        "boundary": "Bounded five-class owner-surface scan; not complete privacy assurance.",
    }


def seal_staged() -> dict[str, Any]:
    if git_text("branch", "--show-current") != x1.BRANCH or git_text("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError("final staged seal requires exact immutable evidence head")
    staged_list = [path for path in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if path]
    staged = set(staged_list)
    deleted = [path for path in git_text("diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if path]
    self_exclusions = [
        "docs/liora-venn/v672-v6/validation/final-delta-manifest.json",
        "docs/liora-venn/v672-v6/validation/final-owner-manifest.json",
        "docs/liora-venn/v672-v6/validation/final-staged-review.json",
        "docs/liora-venn/v672-v6/validation/final-staged-privacy.json",
    ]
    allowed_prefixes = (
        "docs/liora-venn/v672-v6/closeout/", "docs/liora-venn/v672-v6/handoffs/",
        "docs/liora-venn/v672-v6/orchestration/", "docs/liora-venn/v672-v6/final/",
        "docs/liora-venn/v672-v6/seal/",
    )
    allowed_validation = {
        "docs/liora-venn/v672-v6/validation/final-validation-prereceipt.json",
        "docs/liora-venn/v672-v6/validation/final-precommit-test-receipt.json",
    }
    unexpected = [
        path for path in staged_list
        if not (
            path.startswith(allowed_prefixes)
            or path in allowed_validation
            or path == "scripts/build_ghc_family_liora_venn_v672_v6_final.py"
            or path == "scripts/validate_ghc_family_liora_venn_v672_v6_final.py"
            or path == "tests/test_ghc_family_liora_venn_v672_v6_final.py"
        )
    ]
    frozen_changes = [path for path in staged_list if "/x1/" in path or "/x2/" in path or path.endswith("_x1.py") or path.endswith("_x2.py")]
    if deleted or unexpected or frozen_changes:
        raise RuntimeError(f"final staged allowlist refused: deleted={deleted}, unexpected={unexpected}, frozen={frozen_changes}")
    committed_owner = set(filter(None, git_text("diff", "--name-only", x1.SOURCE_FINAL, EVIDENCE_COMMIT).splitlines()))
    owner_union = committed_owner | staged

    def entries(paths: set[str]) -> list[dict[str, Any]]:
        rows = []
        for path in sorted(paths - set(self_exclusions)):
            data = _blob_for_path(path, staged)
            rows.append({"path": path, "git_blob_oid": _oid_for_path(path, staged), "bytes": len(data), "sha256": sha256(data)})
        return rows

    delta_entries = entries(staged)
    owner_entries = entries(owner_union)
    privacy = privacy_scan(sorted(owner_union - set(self_exclusions)), staged)
    if not privacy["valid"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    write_json(VALIDATION_ROOT / "final-staged-privacy.json", privacy)
    write_json(
        VALIDATION_ROOT / "final-staged-review.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.final-staged-review.v1",
            "reviewed_at": now(),
            "base": EVIDENCE_COMMIT,
            "entry_paths_before_self_exclusions": staged_list,
            "entry_count_before_self_exclusions": len(staged_list),
            "self_exclusions": self_exclusions,
            "expected_delta_total_after_self_exclusions": len(staged_list) + len(self_exclusions),
            "source_to_final_owner_paths_before_self_exclusions": sorted(owner_union),
            "expected_owner_total_after_self_exclusions": len(owner_union) + len(set(self_exclusions) - owner_union),
            "deletions": deleted,
            "unexpected_paths": unexpected,
            "frozen_x1_or_x2_changes": frozen_changes,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "valid": bool(staged_list) and not deleted and not unexpected and not frozen_changes and privacy["valid"],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        VALIDATION_ROOT / "final-delta-manifest.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.git-blob-manifest.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "base": EVIDENCE_COMMIT,
            "domain": "final delta from immutable evidence",
            "hash_domain": "normalized_lf_exact_git_blob",
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": self_exclusions,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        VALIDATION_ROOT / "final-owner-manifest.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.git-blob-manifest.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "base": x1.SOURCE_FINAL,
            "domain": "complete Liora source-to-final owner surface",
            "hash_domain": "normalized_lf_exact_git_blob",
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": self_exclusions,
            "boundary": BOUNDARY,
        },
    )
    return {"delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "self_exclusions": len(self_exclusions), "privacy_candidates": privacy["candidate_count"], "privacy_confirmed": privacy["confirmed_hit_count"], "valid": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "seal-staged"))
    args = parser.parse_args()
    payload = build() if args.command == "build" else seal_staged()
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
