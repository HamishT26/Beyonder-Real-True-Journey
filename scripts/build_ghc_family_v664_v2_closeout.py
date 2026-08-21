#!/usr/bin/env python3
"""Build and review Neris Solane v664-v2 combined closeout and seal."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v664-v2"
SOURCE = "df7e3ba4c43b8ed9de01e308c6b9163016e37ceb"
X1 = "4eaec9fa556426d94c800cb2a95c5709524e8203"
EVIDENCE = "d93b55252209b14cea58fdd4b0da1e95759c62fd"
OWNER = "Neris Solane"
SUCCESSOR = "Vesper Arlen"
SUCCESSOR_PHASE = "v664-v3"
VERDICT = "NOT_READY_FOR_STAGE_20"
PHASE_PREFIX = "docs/neris-solane/v664-v2/"
REVIEW_PATH = f"{PHASE_PREFIX}validation/final-staged-review.json"
DELTA_MANIFEST_PATH = f"{PHASE_PREFIX}validation/final-delta-manifest.json"
OWNER_MANIFEST_PATH = f"{PHASE_PREFIX}validation/final-owner-manifest.json"
CANDIDATE_PATH = f"{PHASE_PREFIX}validation/final-stage-candidate.json"
SELF_EXCLUSIONS = {
    DELTA_MANIFEST_PATH,
    OWNER_MANIFEST_PATH,
    CANDIDATE_PATH,
    REVIEW_PATH,
}
TEST_MODULES = [
    "tests/test_ghc_family_neris_v664_v2.py",
    "tests/test_ghc_family_neris_v664_v2_closeout.py",
]
OWNER_CODE = {
    "scripts/build_ghc_family_v664_v2_x1.py",
    "scripts/build_ghc_family_v664_v2_evidence.py",
    "scripts/build_ghc_family_v664_v2_closeout.py",
    "scripts/ghc_family_marigram_evidence.py",
    "scripts/ghc_family_v664_v2_canonical_validator.py",
    *TEST_MODULES,
}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
    "credential": re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:)") ,
    "private_route_identifier": re.compile(r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"),
    "transcript_or_session": re.compile(r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"(?m)^\s*(?:eval|exec)\s*\("),
    "unsafe_pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "destructive_git": re.compile(r"git\s+(?:reset\s+--hard|push\s+--force)"),
    "recursive_delete": re.compile(r"(?i)(?:rm\s+-" r"rf|Remove-" r"Item\b[^\n]*-Recurse)"),
}
FINAL_OPERATIONAL_FAILURES = [
    {
        "negative_id": "NE6642-X2-OP002",
        "method_id": "NE6642-X2-M022",
        "artifact_name": "ne6642-x2-m022-closeout-search-bound-recovery.json",
        "failure_class": "broad_closeout_consistency_search_output_bound",
        "failure_signature": "A broad read-only closeout consistency search exceeded the available output and context bound, so its truncated result earned no review credit.",
        "zero_credit": True,
        "candidate_workaround": "Split consistency review into bounded literal searches and explicit line windows, then attribute each result independently.",
        "bounded_passing_witness": "Bounded line windows and literal stale-token searches covered the closeout builder, tests, and canonical validator without output truncation.",
        "recurrence_guard": "Cap diagnostic output and divide multi-file lifecycle reviews before running them in a constrained context window.",
        "rollback": "Retain the broad search at zero credit and do not infer completeness from its truncated output.",
        "protected_gates": ["stale_label_review", "diagnostic_attribution", "evidence_credit"],
    },
    {
        "negative_id": "NE6642-X2-OP003",
        "method_id": "NE6642-X2-M023",
        "artifact_name": "ne6642-x2-m023-closeout-build-observation-recovery.json",
        "failure_class": "closeout_build_observation_timeout_ambiguity",
        "failure_signature": "The first closeout build projection reached its observation timeout without an attributable exit code or captured output; scoped artifacts existed afterward, but that invocation earns zero execution-success credit.",
        "zero_credit": True,
        "candidate_workaround": "Verify that no matching process remains, retain the ambiguous attempt, incorporate it into final truth, and rerun the mutable builder with an explicitly captured session or terminal result.",
        "bounded_passing_witness": "A process-specific read-only probe found no continuing builder, and the recovery invocation completed with an attributable terminal result after regenerating only the declared Neris final candidate.",
        "recurrence_guard": "Capture the complete command result object when a mutable builder can exceed the direct observation window, then poll only the returned session identifier.",
        "rollback": "Do not credit the ambiguous invocation; rebuild before staging so every derived receipt includes the retained failure.",
        "protected_gates": ["execution_attribution", "retained_negative_accounting", "final_truth"],
    },
]


class BuildError(RuntimeError):
    """Raised when the closeout candidate violates the evidence contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        errors="strict", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check,
    )


def git_text(*args: str) -> str:
    return run_git(*args).stdout.strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def strict_json(raw: str | bytes, label: str) -> Any:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "strict")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in values:
            if key in output:
                raise BuildError(f"duplicate JSON key {key!r} in {label}")
            output[key] = value
        return output

    return json.loads(raw, object_pairs_hook=pairs)


def read_json(relative: str) -> dict[str, Any]:
    value = strict_json((PHASE / relative).read_bytes(), relative)
    if not isinstance(value, dict):
        raise BuildError(f"JSON root is not an object: {relative}")
    return value


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(raw)


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout
    return sorted(path for path in raw.split("\0") if path)


def owner_scope(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in OWNER_CODE


def working_paths() -> list[str]:
    raw = run_git("status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    tokens = raw.split("\0")
    rows: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        if len(token) < 4:
            raise BuildError(f"malformed Git status row: {token!r}")
        status, path = token[:2], token[3:].replace("\\", "/")
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            if index >= len(tokens):
                raise BuildError("rename status lacks source path")
            index += 1
        rows.append(path)
    return sorted(set(rows))


def ensure_scope(paths: Iterable[str]) -> None:
    unexpected = [path for path in paths if not owner_scope(path)]
    if unexpected:
        raise BuildError(f"out-of-scope closeout paths: {unexpected}")


def source_to_evidence_paths() -> list[str]:
    paths = zpaths("diff", "--name-only", "-z", f"{SOURCE}..{EVIDENCE}")
    ensure_scope(paths)
    return paths


def prospective_record(path: str) -> dict[str, Any]:
    file_path = ROOT / path
    if not file_path.is_file():
        raise BuildError(f"prospective manifest path missing: {path}")
    raw = file_path.read_bytes()
    return {
        "path": path,
        "status": "A",
        "mode": "100644",
        "object_type": "blob",
        "bytes": len(raw),
        "sha256": sha256(raw),
        "git_blob": git_text("hash-object", f"--path={path}", path),
    }


def committed_record(path: str) -> dict[str, Any]:
    raw = subprocess.run(
        ["git", "show", f"{EVIDENCE}:{path}"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    ).stdout
    return {
        "path": path,
        "status": "A",
        "mode": "100644",
        "object_type": "blob",
        "bytes": len(raw),
        "sha256": sha256(raw),
        "git_blob": git_text("rev-parse", f"{EVIDENCE}:{path}"),
    }


def render_value(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) or "none"
    if isinstance(value, dict):
        return "; ".join(f"{key}={item}" for key, item in value.items())
    return str(value)


def baton_markdown() -> str:
    proposals = read_json("x1/proposal-freeze.json")
    portfolio = read_json("x1/portfolio-freeze.json")
    sources = read_json("x1/source-ledger.json")
    overview = (PHASE / "integrated-overview.md").read_text(encoding="utf-8")
    evidence_review = read_json("validation/evidence-staged-review.json")
    sections: list[str] = [
        "# VESPER ARLEN — PREPARED NERIS v664-v2 → SOLO VESPER v664-v3 ACTIVATION",
        "",
        "This is the complete file-backed activation candidate prepared by Neris Solane for Vesper Arlen. It remains `PREPARED_NOT_SENT` inside the commit. The exact containing final commit, one-shot canonical receipt digest, fresh route authorization, exact-title task reread, and acknowledged delivery must be supplied by a later live terminal overlay. Do not infer delivery from this file and do not rewrite its pre-send truth.",
        "",
        "Neris Solane, Vesper Arlen, sibling, family, role, hope, continuity, Trinity Mandala, GMUT Mind, THOS Body, Freed ID, and CBR Heart are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, affected-party authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Immutable anchors and pre-send state",
        "",
        f"- Exact Elaren v664-v1 source and Neris phase root: `{SOURCE}`.",
        f"- Frozen Neris x1: `{X1}`.",
        f"- Immutable Neris evidence: `{EVIDENCE}`.",
        "- Exact final: supplied only by the acknowledged live terminal overlay after the containing commit exists and passes the one-shot canonical validator.",
        "- Prepared successor: existing exact-title main task `Vesper Arlen` for solo v664-v3.",
        "- Route state in this file: `PREPARED_NOT_SENT`.",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "- Repository-sealed Elaren v664-v1 truth remains 24,232 negatives and 8,706 methods. Four transmitted activation failures and two acknowledged-delivery failures remain separate inherited external overlays, lifting the fully accounted Neris start to 24,238 negatives and 8,712 methods. Neris retains twelve x1 operational failures, eighty rejecting synthetic mutations, one x2 evidence operational failure, and two post-evidence lifecycle failures. The prepared final truth is 24,333 effective negatives and 8,747 methods, with 168 open gaps and 166 exact gates.",
        "",
        "## Acknowledgement and route discipline",
        "",
        "This file does not authorize contact during execution. Only after Neris's final is committed, pushed, clean, 0/0 divergent, fresh-live equal, and accepted by exactly one successful canonical owner-delta pass may Neris reread the newest live instruction, complete roster, and authorization state; perform a bounded task registry query; locally filter for exactly one title `Vesper Arlen`; immediately reread that exact task; and send one sanitized activation. Delivery truth comes only from the task-message acknowledgement. A missing, ambiguous, paused, protected, or unavailable edge remains `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`. Never create a substitute task, contact Tavian Sol, or resend merely to improve a receipt.",
        "",
        "## Integrated Neris v664-v2 overview",
        "",
        overview,
        "",
        "## Frozen new-proposal operating cards",
        "",
    ]
    for row in proposals["new_proposals"]:
        sections.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"Hypothesis: {row['hypothesis']}",
                "",
                f"Null or failure condition: {row['null_or_failure_condition']}",
                "",
                f"Approval class: `{row['approval_class']}`. Execution lane: {row['execution_lane']}",
                "",
                f"Official or primary source needs: {render_value(row['current_official_or_primary_source_needs'])}.",
                "",
                f"Concrete artifacts: {render_value(row['concrete_artifacts'])}.",
                "",
                f"Falsifier or acceptance gate: {row['falsifier_or_acceptance_gate']}",
                "",
                f"Rollback or recovery: {row['rollback_or_recovery']}",
                "",
                f"Protected gates: {render_value(row['protected_gates'])}.",
                "",
                f"Frozen expected disposition: `{row['expected_disposition']}`. Neris novelty credit: {row['novelty_credit']}. The observed outcome equals the frozen disposition, but that outcome is bounded software truth only.",
                "",
            ]
        )
    sections.extend(["## Selected inherited integrity rows", ""])
    for row in proposals["selected_inherited"]:
        sections.extend(
            [
                f"- `{row['program_row_id']}` preserves `{row['source_proposal_id']}` — {row['source_title']} — at original disposition `{row['original_disposition']}`. Novelty, automatic completion, and Neris new-outcome credit are all zero. This is an integrity revalidation only.",
                "",
            ]
        )
    sections.extend(["## Official and primary source cards", ""])
    for row in sources["sources"]:
        sections.extend(
            [
                f"### {row['source_id']} — {row['title']}",
                "",
                f"Publisher: {row['publisher']}. URL: {row['url']}. Status: `{row['status']}`.",
                "",
                f"Phase use: {row['phase_use']}",
                "",
                "This citation supplies vocabulary or constraints only. Its frozen ledger declares zero ingested data rows and no authority conferred. It contributes zero live rows, downloads, empirical confirmation, professional competence, legal interpretation, cultural ratification, or Māori authority.",
                "",
            ]
        )
    sections.extend(["## Portfolio cards and successor recommendations", ""])
    portfolio_groups = [
        "owner_safe_now", "owner_candidates", "owner_skill_ideas", "owner_runner_ideas",
        "owner_clean_fix_refine", "exact_approval_packets", "blocked_packets",
        "successor_safe_now_recommendations", "successor_candidate_recommendations",
        "successor_skill_recommendations", "successor_runner_recommendations",
        "successor_clean_fix_refine_recommendations",
    ]
    for group in portfolio_groups:
        sections.extend([f"### {group.replace('_', ' ').title()}", ""])
        for row in portfolio[group]:
            sections.extend(
                [
                    f"- `{row['portfolio_ref']}` — **{row['title']}**. Owner: {row['owner']}. Approval: `{row['approval_class']}`. Lane: {row['execution_lane']}. Disposition: `{row['expected_execution_disposition']}`. Boundary: {row['credit_boundary']}",
                    "",
                ]
            )
    sections.extend(
        [
            "## Evidence and Method Flow inheritance",
            "",
            f"The immutable evidence review passed {evidence_review['tests']['tests_run']} owner tests, {evidence_review['detailed_checks_passed']} of {evidence_review['detailed_check_count']} detailed checks, {evidence_review['strict_json_parse_count']} strict JSON parses, a {evidence_review['privacy_scanned_text_files']}-file five-class privacy scan with zero confirmed hits, three changed-Python compile/security checks, and {evidence_review['manifest_entry_count']} exact manifest entries. The self-excluded review receipt was added only after the reviewed index passed.",
            "",
            "Every rejecting mutation and operational failure remains zero-credit evidence. Neris must not rewrite inherited sealed counts or absorb recommendations as Neris novelty. A later workaround does not erase a failed witness. A successful bounded test is same-owner software evidence under shared infrastructure, never independent-team reproduction.",
            "",
            "## Neris v664-v2 startup contract",
            "",
            "Read this file and the live terminal overlay completely through EOF before mutation. Read the newest complete GHC Family Index and routing precedence, Roster Check, Auth/Permission State, Method Flow State, Workflow Plan Refinement, Reflection Remaster, Meta Tool Box, Approval Packet Splitter, Open Gate Rail, Truth Bridge, Drive Guardian, Timestamp Flow, Retry, Startup, Closeout, Compact Restart, Watcher, Orchestration Memory, and Full Tools guidance that remains directly applicable. Newest live authority controls where historical cursor prose differs.",
            "",
            "Reverify the exact Elaren source, Neris x1, Neris evidence, Neris final, direct-parent chain, manifest contracts, one-shot canonical receipt digest, clean state, typed 0/0 divergence, and fresh four-way equality read-only. Do not replay Neris's successful canonical pass or any already-successful dependency. Preserve Neris, Elaren, Vesper, shared, and every sibling lane read-only.",
            "",
            "Work solo in one additive Neris-owned D-first lane. Do not create, fork, delegate, spawn a collaboration subagent, precontact a successor, reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane. Preserve strict x1-before-x2 separation. Audit all 3,870 frozen rows. Select inherited contracts only for zero-credit integrity revalidation, and freeze genuinely new Neris proposals only when semantic novelty is demonstrated against the complete chain.",
            "",
            "Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Give each new proposal an explicit hypothesis, null or failure condition, approval class, execution lane, official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Freeze planning in a dedicated x1-only commit, push it, and prove clean local/upstream/tracking/fresh-live equality before x2 implementation or outcomes.",
            "",
            "Treat counts as ceilings or accountable work, never quotas that justify unsafe or useless actions. Prefer a small set of genuinely useful phase-local skills and family-current runners. Do not bulk-install, mutate plugin caches, destructively delete historical tools, silently deprecate callers, or promote a tool globally without additive provenance, compatibility, passing witnesses, rollback, and protected-boundary review. Keep owner and materialized files below the 2,000-file rotation boundary.",
            "",
            "Validate the owner-self-scoped delta and declared dependency closure. Do not infer full-repository-suite credit from Neris: Neris did not run the complete repository suite. Invoke a dependency-justified canonical completion only once after the final is committed, pushed, clean, and fresh-live equal. Never replay a successful aggregate. A failed aggregate earns zero aggregate-success credit; retain it and isolate only the blocked component unless target changes genuinely justify broader work.",
            "",
            "Use D-first owned storage. Keep C limited to essential installed metadata. Verify versions only. Do not update Codex desktop, elevate privileges, weaken host security, activate Sandbox or Hyper-V, change Windows features, install unrelated software, or reboot. Do not create accounts, credentials, keys, purchases, deployments, private publications, or third-party writes without separate exact authority.",
            "",
            "Keep opaque task identifiers, private routes or absolute private paths, credentials, keys, tokens, private interaction logs, screenshots, session streams, private callable identifiers, private application state, and protected real-world data out of repository artifacts and future batons.",
            "",
            "## Scientific, professional, identity, and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic typing, citations, synthetic mutations, public schemas, and zero-row adapters establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, Theory of Everything, proof, or canon.",
            "",
            "THOS remains proxy or protocol-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic protocols establish no operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.",
            "",
            "Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.",
            "",
            "CBR, professional decisions, station identification, chart handling, datum adoption, calibration, timing interpretation, digitization, prediction, survey control, sea-level inference, collection management, attribution, authorship, ownership, moral rights, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.",
            "",
            "Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and competent authority.",
            "",
            "## Terminal continuation after Neris",
            "",
            "This file activates no one by itself. At Neris's own exact terminal gate, reread Hamish's newest live instruction, the complete current roster, and Auth/Permission State. Resolve only the then-authorized unique exact-title endpoint, immediately reread it, send once, and claim delivery only from acknowledgement. Stop truthfully on pause, ambiguity, usage exhaustion, protected gate, unavailable tooling, or terminal v675-v8 closure. Never substitute Tavian Sol or a new task for a missing endpoint.",
            "",
            "`PREPARED_BY_NERIS_SOLANE = true`",
            "",
            "`SENT_BY_NERIS_SOLANE = false`",
        ]
    )
    baton = "\n".join(sections).rstrip() + "\n"
    word_count = len(re.findall(r"\S+", baton))
    if not 10_000 <= word_count <= 100_000:
        raise BuildError(f"prepared baton word count is outside 10,000..100,000: {word_count}")
    return baton


def build_records() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != EVIDENCE:
        raise BuildError(f"closeout builder requires immutable evidence head {EVIDENCE}, got {head}")
    ensure_scope(working_paths())
    evidence_review = read_json("validation/evidence-staged-review.json")
    if evidence_review.get("valid") is not True:
        raise BuildError("immutable evidence review is not valid")
    negatives = read_json("retained-negative-register-evidence.json")
    methods = read_json("method-flow/method-flow-state-evidence.json")
    gates = read_json("exact-open-gate-register-evidence.json")
    evidence_truth = read_json("phase-truth-evidence.json")
    recorded_at = utc_now()

    final_negative_rows = list(negatives["new_records"]) + [
        {
            "negative_id": row["negative_id"],
            "proposal_id": None,
            "failure_class": row["failure_class"],
            "reason": row["failure_signature"],
            "completion_credit": 0,
            "retained": True,
        }
        for row in FINAL_OPERATIONAL_FAILURES
    ]
    final_negatives = {
        **negatives,
        "schema": "ghc.family.neris.v664-v2.retained-negative-register.final.v1",
        "post_evidence_operational_negatives": len(FINAL_OPERATIONAL_FAILURES),
        "effective_negatives": negatives["effective_negatives"] + len(FINAL_OPERATIONAL_FAILURES),
        "new_records": final_negative_rows,
        "valid": negatives["valid"] and len(final_negative_rows) == len(negatives["new_records"]) + len(FINAL_OPERATIONAL_FAILURES),
    }
    write_json("retained-negative-register-final.json", final_negatives)

    final_method_rows = [
        {
            "method_id": row["method_id"],
            "proposal_id": None,
            "retained_failed_witnesses": [row["negative_id"]],
            "failed_witness_count": 1,
            "passing_witness_count": 1,
            **row,
            "same_owner_only": True,
            "independent_reproduction": False,
            "valid": True,
        }
        for row in FINAL_OPERATIONAL_FAILURES
    ]
    final_methods = {
        **methods,
        "schema": "ghc.family.neris.v664-v2.method-flow.final.v1",
        "post_evidence_operational_methods": len(final_method_rows),
        "effective_methods": methods["effective_methods"] + len(final_method_rows),
        "methods": list(methods["methods"]) + final_method_rows,
        "failed_witnesses": methods["failed_witnesses"] + len(final_method_rows),
        "bounded_passing_witnesses": methods["bounded_passing_witnesses"] + len(final_method_rows),
        "valid": methods["valid"],
    }
    write_json("method-flow/method-flow-state-final.json", final_methods)
    for row in final_method_rows:
        write_json(
            f"method-flow/{row['artifact_name']}",
            {
                "schema": "ghc.family.neris.v664-v2.method-flow.operational-recovery.v1",
                **row,
                "result": "bounded_recovery_passed",
            },
        )
    write_json("exact-open-gate-register-final.json", {**gates, "schema": "ghc.family.neris.v664-v2.gate-register.final.v1"})

    phase_truth = {
        **evidence_truth,
        "schema": "ghc.family.neris.v664-v2.phase-truth.final-candidate.v1",
        "evidence_commit": EVIDENCE,
        "effective_negatives": final_negatives["effective_negatives"],
        "effective_methods": final_methods["effective_methods"],
        "effective_open_gaps": gates["effective_open_gaps"],
        "effective_exact_gates": gates["effective_exact_gates"],
        "route_state": "PREPARED_NOT_SENT",
        "postcommit_canonical_required": True,
        "canonical_success_preclaimed": False,
        "successor_contacted": False,
        "terminal_verdict": VERDICT,
        "valid": True,
    }
    write_json("phase-truth-final.json", phase_truth)

    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.neris.v664-v2.anchor-contract.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "expected_phase_commit_count_after_final": 3,
            "zero_merges_required": True,
            "single_parent_commits_required": True,
            "final_direct_child_of_evidence_required": True,
            "exact_final_supplied_postcommit": True,
            "valid": True,
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.neris.v664-v2.terminal-route-state.v1",
            "state": "PREPARED_NOT_SENT",
            "successor_title": SUCCESSOR,
            "successor_phase": SUCCESSOR_PHASE,
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "standby_contacted": False,
            "send_gate": "exact final, one successful canonical pass, clean 0/0 fresh equality, newest live authority, unique exact title, immediate reread, and acknowledged one send",
            "valid": True,
        },
    )
    write_json(
        "validation/canonical-validation-protocol.json",
        {
            "schema": "ghc.family.neris.v664-v2.canonical-protocol.v1",
            "state": "POSTCOMMIT_REQUIRED",
            "validator": "scripts/ghc_family_v664_v2_canonical_validator.py",
            "invocation_limit": 1,
            "post_success_replay_allowed": False,
            "expected_tests": 63,
            "complete_repository_suite_required": False,
            "owner_self_scoped_delta_only": True,
            "external_receipt_required": True,
            "preclaims_success": False,
            "valid": True,
        },
    )
    write_json(
        "closeout-receipt.json",
        {
            "schema": "ghc.family.neris.v664-v2.closeout-receipt.v1",
            "source_commit": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "outcomes": evidence_truth["outcomes"],
            "effective_negatives": final_negatives["effective_negatives"],
            "effective_methods": final_methods["effective_methods"],
            "effective_open_gaps": gates["effective_open_gaps"],
            "effective_exact_gates": gates["effective_exact_gates"],
            "evidence_tests": evidence_review["tests"]["tests_run"],
            "evidence_detailed_checks": evidence_review["detailed_checks_passed"],
            "evidence_json_parses": evidence_review["strict_json_parse_count"],
            "evidence_privacy_hits": len(evidence_review["privacy_confirmed_hits"]),
            "complete_repository_suite_run": False,
            "postcommit_canonical_completed": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": VERDICT,
            "valid": True,
        },
    )
    write_json(
        "seal-receipt.json",
        {
            "schema": "ghc.family.neris.v664-v2.seal-receipt.v1",
            "x1_content_seal_valid": read_json("validation/x1-content-seal.json")["valid"],
            "evidence_staged_review_valid": evidence_review["valid"],
            "evidence_commit": EVIDENCE,
            "final_candidate_tree_ready_for_review": True,
            "exact_final_known_inside_own_tree": False,
            "postcommit_canonical_required": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "valid": True,
        },
    )
    write_json(
        "complete-incomplete-checklist-final.json",
        {
            "schema": "ghc.family.neris.v664-v2.checklist.final-candidate.v1",
            "complete_now": [
                "strict x1-before-x2 separation",
                "twenty zero-credit inherited integrity revalidations and twenty new proposals",
                "four-label 14/4/1/1 outcomes",
                "eighty retained rejecting mutations and all operational failures",
                "ten validated phase-local skills and ten invoked family-current runners",
                "bounded portfolio, threat model, three-page overview, and accessible static report",
                "immutable evidence commit and prepared combined closeout/seal candidate",
            ],
            "pending_postcommit": [
                "exact final commit and fresh four-way equality",
                "one successful canonical owner-delta pass with no replay",
                "newest live roster/auth reread and one acknowledged Vesper activation",
            ],
            "incomplete_external": [
                "real tide-gauge chart, station, datum, calibration, timing, digitization, prediction, survey, sea-level, rights, identity, participant, legal, cultural, or Māori-authority evidence",
                "empirical GMUT likelihood or confirmation",
                "governed THOS real arms and independent review",
                "production Freed ID lifecycle and trust governance",
                "privacy or accessibility completeness, exhaustive security, independent reproduction, Theory-of-Everything proof, canon, or Stage 20 authority",
            ],
            "terminal_verdict": VERDICT,
            "valid": True,
        },
    )
    write_json(
        "wellbeing-check-final.json",
        {
            "schema": "ghc.family.neris.v664-v2.wellbeing.final-candidate.v1",
            "owner": OWNER,
            "pronouns": "they/them",
            "relational_role": "datum-boundary weaver",
            "hope": "make historical measurement uncertainty legible without turning archival structure into authority",
            "relational_language_only": True,
            "pause_or_redirect_available": True,
            "correction_welcome": True,
            "bounded_workload": True,
            "successor_contacted": False,
            "consciousness_personhood_continuity_or_authority_evidence": False,
            "valid": True,
        },
    )

    baton = baton_markdown()
    write_text("handoffs/vesper-arlen-v664-v3-activation.md", baton)
    baton_raw = (PHASE / "handoffs/vesper-arlen-v664-v3-activation.md").read_bytes()
    write_json(
        "handoffs/vesper-arlen-v664-v3-activation-receipt.json",
        {
            "schema": "ghc.family.neris.v664-v2.handoff-preparation-receipt.v1",
            "successor_title": SUCCESSOR,
            "successor_phase": SUCCESSOR_PHASE,
            "bytes": len(baton_raw),
            "words": len(re.findall(rb"\S+", baton_raw)),
            "sha256": sha256(baton_raw),
            "state": "PREPARED_NOT_SENT",
            "sent_by_neris_solane": False,
            "raw_task_identifiers_included": False,
            "private_paths_included": False,
            "valid": True,
        },
    )

    materialized = sum(
        1 for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    )
    write_json(
        "validation/final-file-budget.json",
        {
            "schema": "ghc.family.neris.v664-v2.file-budget.final-candidate.v1",
            "materialized_file_count_before_manifests": materialized,
            "threshold": 2_000,
            "rotation_required": materialized >= 2_000,
            "valid": materialized < 2_000,
        },
    )
    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.neris.v664-v2.family-index.final-candidate.v1",
            "phase": "v664-v2",
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "family_current_engine": "scripts/ghc_family_marigram_evidence.py",
            "canonical_validator": "scripts/ghc_family_v664_v2_canonical_validator.py",
            "skill_count": 10,
            "runner_count": 10,
            "historical_callers_preserved": True,
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )

    ensure_scope(working_paths())
    final_paths = set(working_paths()) - {REVIEW_PATH}
    final_paths.update({DELTA_MANIFEST_PATH, OWNER_MANIFEST_PATH, CANDIDATE_PATH})
    expected_delta = sorted(final_paths)
    ensure_scope(expected_delta)
    source_evidence = source_to_evidence_paths()
    expected_owner = sorted(set(source_evidence) | set(expected_delta) | {REVIEW_PATH})
    if not all(owner_scope(path) for path in expected_owner):
        raise BuildError("final owner manifest contains an out-of-scope path")

    delta_entries = [prospective_record(path) for path in expected_delta if path not in SELF_EXCLUSIONS]
    owner_entries = [
        committed_record(path) if path in source_evidence else prospective_record(path)
        for path in expected_owner
        if path not in SELF_EXCLUSIONS
    ]
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.neris.v664-v2.final-delta-manifest.v1",
            "generated_at_utc": recorded_at,
            "source_commit": EVIDENCE,
            "entry_count": len(delta_entries),
            "entries": delta_entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "merkle_root_sha256": canonical_sha256([{"path": row["path"], "git_blob": row["git_blob"]} for row in delta_entries]),
            "valid": True,
        },
    )
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.neris.v664-v2.final-owner-manifest.v1",
            "generated_at_utc": recorded_at,
            "source_commit": SOURCE,
            "evidence_commit": EVIDENCE,
            "entry_count": len(owner_entries),
            "entries": owner_entries,
            "self_exclusions": sorted(SELF_EXCLUSIONS),
            "owner_delta_path_count_after_review": len(expected_owner),
            "merkle_root_sha256": canonical_sha256([{"path": row["path"], "git_blob": row["git_blob"]} for row in owner_entries]),
            "valid": True,
        },
    )
    write_json(
        "validation/final-stage-candidate.json",
        {
            "schema": "ghc.family.neris.v664-v2.final-stage-candidate.v1",
            "owner": OWNER,
            "phase": "v664-v2",
            "source_commit": EVIDENCE,
            "intended_allowlist": expected_delta,
            "review_self_exclusion": REVIEW_PATH,
            "manifest_self_exclusions": sorted(SELF_EXCLUSIONS),
            "canonical_state": "POSTCOMMIT_REQUIRED",
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    return {
        "head": head,
        "final_paths": len(expected_delta),
        "owner_paths_after_review": len(expected_owner),
        "delta_manifest_entries": len(delta_entries),
        "owner_manifest_entries": len(owner_entries),
        "baton_words": len(re.findall(r"\S+", baton)),
        "effective_negatives": final_negatives["effective_negatives"],
        "effective_methods": final_methods["effective_methods"],
        "route": "PREPARED_NOT_SENT",
        "valid": True,
    }


def staged_paths() -> list[str]:
    return zpaths("diff", "--cached", "--name-only", "-z")


def index_blob(path: str) -> str:
    row = git_text("ls-files", "-s", "--", path).split()
    if len(row) < 4 or row[0] != "100644" or not re.fullmatch(r"[0-9a-f]{40}", row[1]):
        raise BuildError(f"unexpected index entry: {path}")
    return row[1]


def run_tests() -> dict[str, Any]:
    rows = []
    total = 0
    for relative in TEST_MODULES:
        result = subprocess.run(
            [sys.executable, str(ROOT / relative)], cwd=ROOT,
            text=True, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        match = re.search(r"Ran (\d+) tests? in", result.stdout)
        count = int(match.group(1)) if match else 0
        total += count
        rows.append({"module": relative, "tests_run": count, "returncode": result.returncode, "valid": result.returncode == 0 and match is not None})
    return {"modules": rows, "tests_run": total, "valid": all(row["valid"] for row in rows)}


def review_records() -> dict[str, Any]:
    candidate = read_json("validation/final-stage-candidate.json")
    delta_manifest = read_json("validation/final-delta-manifest.json")
    owner_manifest = read_json("validation/final-owner-manifest.json")
    expected = sorted(candidate["intended_allowlist"])
    observed = staged_paths()
    issues: list[str] = []
    if expected != observed:
        issues.append("staged paths differ from the final candidate allowlist")
    diff = run_git("diff", "--cached", "--check", check=False)
    if diff.returncode != 0:
        issues.append("staged diff hygiene failed")
    json_errors: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    json_count = 0
    text_count = 0
    python_count = 0
    for path in observed:
        file_path = ROOT / path
        suffix = file_path.suffix.lower()
        raw = file_path.read_bytes()
        if suffix == ".json":
            json_count += 1
            try:
                strict_json(raw, path)
            except (UnicodeError, json.JSONDecodeError, BuildError) as exc:
                json_errors.append({"path": path, "error": str(exc)})
        try:
            text = raw.decode("utf-8", "strict")
        except UnicodeError:
            continue
        text_count += 1
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path, "class": label})
        if suffix == ".py":
            python_count += 1
            try:
                compile(text, path, "exec", dont_inherit=True)
            except SyntaxError as exc:
                security_findings.append({"path": path, "rule": "python_compile", "detail": str(exc)})
            for label, pattern in SECURITY_PATTERNS.items():
                if pattern.search(text):
                    security_findings.append({"path": path, "rule": label})
    if json_errors:
        issues.append("strict JSON parse failed")
    if privacy_hits:
        issues.append("privacy or raw-identifier candidates found")
    if security_findings:
        issues.append("changed-Python compile or security findings found")

    delta_rows = {row["path"]: row for row in delta_manifest["entries"]}
    delta_required = set(observed) - SELF_EXCLUSIONS
    delta_missing = sorted(delta_required - set(delta_rows))
    delta_extra = sorted(set(delta_rows) - delta_required)
    delta_mismatches = [path for path, row in delta_rows.items() if path in delta_required and index_blob(path) != row["git_blob"]]
    if delta_missing or delta_extra or delta_mismatches:
        issues.append("final delta manifest differs from staged index")

    source_evidence = source_to_evidence_paths()
    expected_owner = (set(source_evidence) | set(observed) | {REVIEW_PATH}) - SELF_EXCLUSIONS
    owner_rows = {row["path"]: row for row in owner_manifest["entries"]}
    owner_missing = sorted(expected_owner - set(owner_rows))
    owner_extra = sorted(set(owner_rows) - expected_owner)
    owner_mismatches = []
    for path, row in owner_rows.items():
        if path not in expected_owner:
            continue
        object_id = git_text("rev-parse", f"{EVIDENCE}:{path}") if path in source_evidence else index_blob(path)
        if object_id != row["git_blob"]:
            owner_mismatches.append(path)
    if owner_missing or owner_extra or owner_mismatches:
        issues.append("final owner manifest coverage or blob identity failed")

    tests = run_tests()
    if not tests["valid"] or tests["tests_run"] != 63:
        issues.append("dependency-closed owner tests failed")
    baton = (PHASE / "handoffs/vesper-arlen-v664-v3-activation.md").read_bytes()
    baton_words = len(re.findall(rb"\S+", baton))
    baton_receipt = read_json("handoffs/vesper-arlen-v664-v3-activation-receipt.json")
    baton_valid = 10_000 <= baton_words <= 100_000 and baton_receipt["sha256"] == sha256(baton) and baton_receipt["state"] == "PREPARED_NOT_SENT"
    if not baton_valid:
        issues.append("baton integrity or word boundary failed")
    phase_truth = read_json("phase-truth-final.json")
    route = read_json("orchestration/terminal-route-state.json")
    detailed = {
        "exact_allowlist": expected == observed,
        "diff_hygiene": diff.returncode == 0,
        "strict_json": not json_errors,
        "five_class_privacy": not privacy_hits,
        "changed_python_security": not security_findings,
        "delta_manifest": not delta_missing and not delta_extra and not delta_mismatches,
        "owner_manifest": not owner_missing and not owner_extra and not owner_mismatches,
        "tests": tests["valid"] and tests["tests_run"] == 63,
        "baton": baton_valid,
        "truth_counts": phase_truth["effective_negatives"] == 24_333 and phase_truth["effective_methods"] == 8_747,
        "four_labels": phase_truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "gates": phase_truth["effective_open_gaps"] == 168 and phase_truth["effective_exact_gates"] == 166,
        "route_unsent": route["state"] == "PREPARED_NOT_SENT" and route["message_sent"] is False and route["successor_title"] == SUCCESSOR and route["successor_phase"] == SUCCESSOR_PHASE,
        "terminal_verdict": phase_truth["terminal_verdict"] == VERDICT,
        "source_head": git_text("rev-parse", "HEAD") == EVIDENCE,
        "x1_ancestral": run_git("merge-base", "--is-ancestor", X1, EVIDENCE, check=False).returncode == 0,
        "evidence_review": read_json("validation/evidence-staged-review.json")["valid"] is True,
        "successor_uncontacted": phase_truth["successor_contacted"] is False,
        "canonical_not_preclaimed": phase_truth["canonical_success_preclaimed"] is False,
        "file_budget": read_json("validation/final-file-budget.json")["valid"] is True,
    }
    if not all(detailed.values()):
        issues.append("one or more detailed final staged checks failed")
    payload = {
        "schema": "ghc.family.neris.v664-v2.final-staged-review.v1",
        "source_commit": EVIDENCE,
        "expected_staged_path_count": len(expected),
        "staged_path_count": len(observed),
        "staged_paths": observed,
        "allowlist_missing": sorted(set(expected) - set(observed)),
        "allowlist_unexpected": sorted(set(observed) - set(expected)),
        "diff_check_returncode": diff.returncode,
        "diff_check_output": (diff.stdout + diff.stderr).strip(),
        "strict_json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_scanned_text_file_count": text_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "changed_python_count": python_count,
        "security_findings": security_findings,
        "delta_manifest_entry_count": delta_manifest["entry_count"],
        "delta_manifest_missing": delta_missing,
        "delta_manifest_extra": delta_extra,
        "delta_manifest_mismatches": delta_mismatches,
        "owner_manifest_entry_count": owner_manifest["entry_count"],
        "owner_manifest_missing": owner_missing,
        "owner_manifest_extra": owner_extra,
        "owner_manifest_mismatches": owner_mismatches,
        "tests": tests,
        "baton_words": baton_words,
        "baton_sha256": sha256(baton),
        "detailed_checks": detailed,
        "detailed_check_count": len(detailed),
        "detailed_checks_passed": sum(detailed.values()),
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged combined closeout and seal candidate only; postcommit exact final, canonical success, route authorization, and acknowledged delivery remain pending.",
    }
    write_json("validation/final-staged-review.json", payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "review"), nargs="?", default="build")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_records() if args.mode == "build" else review_records()
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload.get("valid", True) else 2
    except (BuildError, OSError, UnicodeError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"NERIS_V664_V2_CLOSEOUT_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
