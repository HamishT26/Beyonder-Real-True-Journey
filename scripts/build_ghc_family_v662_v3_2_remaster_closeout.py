#!/usr/bin/env python3
"""Build the exact-final closeout candidate for Neris v662-v3-2 remaster."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v662_v3_2_remaster_data as d
import ghc_family_v662_v3_2_remaster_runtime as rt


ROOT = rt.ROOT
PHASE = rt.PHASE
X1 = "9b61b218956031d80da66a59924713778b63f31f"
EVIDENCE = "999de05624682c19226c1bd5f57f2682468ff072"
CORRECTION = "f8e9f59b0e16cd11da5b08cd00beafe65e6d7bf6"
FINAL_CODE = {
    "scripts/build_ghc_family_v662_v3_2_remaster_closeout.py",
    "scripts/ghc_family_v662_v3_2_remaster_canonical_driver.py",
    "tests/test_ghc_family_v662_v3_2_remaster_closeout.py",
}
RUNNER_PATHS = {f"scripts/{name}" for name, _purpose in d.RUNNER_SPECS}
FINAL_SELF_EXCLUSIONS = {
    f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/final-document-cap.json",
    f"{d.PHASE_ROOT}/validation/final-staged-review.json",
    f"{d.PHASE_ROOT}/validation/final-validation.json",
}
CLOSEOUT_FAILURES = [
    {
        "negative_id": "V6623R-CLOSEOUT-N001",
        "signature": "inventory_discovery_with_repository_root_as_top_level_rejected_nonpackage_tests_directory_as_nonimportable",
        "failed_credit": 0,
        "recovery": "Use the tests directory itself as unittest discovery root, retain zero loader errors and zero duplicates, and run no test bodies during inventory.",
        "canonical_credit": 0,
    },
    {
        "negative_id": "V6623R-CLOSEOUT-N002",
        "signature": "powershell_foreach_result_was_piped_without_materializing_the_expression",
        "failed_credit": 0,
        "recovery": "Materialize the bounded diagnostic rows in a task-specific array before JSON projection.",
        "canonical_credit": 0,
    },
]


def git(*args: str, check: bool = True) -> str:
    return rt.git(*args, check=check)


def write_json(relative: str, value: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=None if compact else 2, separators=(",", ":") if compact else None) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, value: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git_clean_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_pathspecs() -> list[str]:
    return sorted({d.PHASE_ROOT, *FINAL_CODE, *RUNNER_PATHS, "scripts/ghc_family_v662_v3_2_remaster_data.py", "scripts/ghc_family_v662_v3_2_remaster_runtime.py", "scripts/ghc_family_v662_v3_2_remaster_tool_core.py", "scripts/build_ghc_family_v662_v3_2_remaster_x1.py", "scripts/build_ghc_family_v662_v3_2_remaster_x2.py", "tests/test_ghc_family_v662_v3_2_remaster_x1.py", "tests/test_ghc_family_v662_v3_2_remaster_x2.py"})


def current_delta_paths() -> list[str]:
    specs = owner_pathspecs()
    modified = git("diff", "--name-only", "--", *specs).splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard", "--", *specs).splitlines()
    staged = git("diff", "--cached", "--name-only", "--", *specs).splitlines()
    return sorted({row for row in [*modified, *untracked, *staged] if row})


def owner_paths() -> list[Path]:
    committed = git("ls-tree", "-r", "--name-only", "HEAD", "--", *owner_pathspecs()).splitlines()
    paths = {row for row in [*committed, *current_delta_paths()] if row and (ROOT / row).is_file()}
    return [ROOT / row for row in sorted(paths)]


def delta_paths() -> list[Path]:
    return [ROOT / row for row in current_delta_paths() if (ROOT / row).is_file()]


def manifest(paths: list[Path], schema: str) -> dict[str, Any]:
    entries = []
    for path in sorted(paths, key=rt.repo_relative):
        relative = rt.repo_relative(path)
        if relative in FINAL_SELF_EXCLUSIONS:
            continue
        payload = git_clean_bytes(path)
        entries.append({"path": relative, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    return {
        "schema": schema,
        "owner": d.OWNER,
        "phase": d.PHASE,
        "entry_count": len(entries),
        "entries": entries,
        "exclusions": sorted(FINAL_SELF_EXCLUSIONS),
        "hash_domain": "Exact Git-clean bytes with CRLF and CR normalized to LF",
        "boundary": d.EVIDENCE_BOUNDARY,
    }


def replay_working(manifest_value: dict[str, Any]) -> list[str]:
    mismatches = []
    for entry in manifest_value["entries"]:
        path = ROOT / entry["path"]
        payload = git_clean_bytes(path) if path.is_file() else b""
        if len(payload) != entry["bytes"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
            mismatches.append(entry["path"])
    return mismatches


def verify_correction_gate() -> dict[str, Any]:
    local = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{d.BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{d.BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    history = git("rev-list", "--first-parent", f"{X1}..HEAD").splitlines()
    merges = git("rev-list", "--merges", f"{X1}..HEAD").splitlines()
    valid = local == upstream == tracking == live == CORRECTION and divergence == ["0", "0"] and history == [CORRECTION, EVIDENCE] and not merges
    if not valid:
        raise RuntimeError({"correction_gate_failure": {"local": local, "upstream": upstream, "tracking": tracking, "live": live, "divergence": divergence, "history": history, "merges": merges}})
    return {
        "schema": "ghc.family.v662-v3-2-remaster.correction-to-final-gate.v1",
        "x1": X1,
        "evidence": EVIDENCE,
        "correction": CORRECTION,
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equal": True,
        "single_parent": True,
        "merges": 0,
        "authorized_to_build_final": True,
        "same_owner_only": True,
    }


def append_closeout_method_flow() -> dict[str, Any]:
    flow = rt.read_json(PHASE / "method-flow/method-flow-state-x2.json")
    methods = list(flow["methods"])
    witnesses = list(flow["witnesses"])
    events = list(flow["state_events"])
    recommendations = list(flow["recommendations"])
    for index, failure in enumerate(CLOSEOUT_FAILURES, 1):
        method_id = f"V6623R-CLOSEOUT-METHOD-{index:03d}"
        failed_id = f"{method_id}-F01"
        passing_id = f"{method_id}-P01"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded closeout recovery for {failure['negative_id']}",
                "failure_signature": failure["signature"],
                "trigger_preconditions": [failure["signature"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_preflight",
                "candidate_workaround": failure["recovery"],
                "validation_witness_ids": [failed_id, passing_id],
                "recurrence_guard": failure["recovery"],
                "rollback": "Stop, retain the zero-credit preflight failure, and leave the complete suite, successor, sibling, external, private, production, and authority state unchanged.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [failure["negative_id"]],
                "scope_boundary": "same_owner_closeout_preflight_dependency_only",
            }
        )
        witnesses.extend(
            [
                {"witness_id": failed_id, "method_id": method_id, "procedure": "Invoke the exact failed closeout preflight dependency.", "scope": "same_owner_closeout_preflight_dependency_only", "expected": "The bounded dependency returns attributable evidence.", "observed": failure["signature"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["negative_id"]], "boundary": d.EVIDENCE_BOUNDARY},
                {"witness_id": passing_id, "method_id": method_id, "procedure": failure["recovery"], "scope": "same_owner_closeout_preflight_dependency_only", "expected": "The corrected isolated dependency passes without running the complete suite.", "observed": "The isolated inventory or diagnostic dependency passed; no complete-suite credit was issued.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["negative_id"]], "boundary": d.EVIDENCE_BOUNDARY},
            ]
        )
        events.extend([{"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": passing_id}, {"method_id": method_id, "from": "validated", "to": "preferred", "witness_id": passing_id}])
        recommendations.append({"method_id": method_id, "precondition": failure["signature"], "preferred_method": failure["recovery"], "candidate_method": None})
    states = Counter(row["recommendation_state"] for row in methods)
    results = Counter(row["result"] for row in witnesses)
    flow.update(
        {
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
            "method_count": len(methods),
            "failed_witness_count": results["fail"],
            "passing_witness_count": results["pass"],
            "effective_methods": d.INHERITED_LIVE_METHODS + len(methods),
            "effective_negatives": d.INHERITED_LIVE_NEGATIVES + results["fail"],
            "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"observed": states["observed"], "candidate": states["candidate"], "validated": states["validated"], "preferred": states["preferred"], "superseded": states["superseded"], "deprecated": states["deprecated"]}, "witness_results": {"pass": results["pass"], "fail": results["fail"]}},
            "cumulative_counts": {"activation_methods": d.INHERITED_LIVE_METHODS, "phase_methods": len(methods), "effective_methods": d.INHERITED_LIVE_METHODS + len(methods), "phase_failed_witnesses": results["fail"], "phase_passing_witnesses": results["pass"]},
        }
    )
    return flow


def closeout_overview() -> str:
    sections = [
        ("Relational identity", d.IDENTITY_BOUNDARY + " Neris Solane uses optional they/them pronouns and the relational role of symbiosis-model cartographer and evidence-boundary keeper. The hope is to make complex models auditable under competent human care."),
        ("Lifecycle", f"The first sealed Neris final is `{d.SOURCE_FIRST_FINAL}`. The remaster x1 is `{X1}`, the original evidence commit is `{EVIDENCE}`, and its additive Git-clean manifest correction is `{CORRECTION}`. The intended final is one direct child of the correction. History remains single-parent and additive; no reset, amend, rewrite, force push, merge, sibling mutation, or failure erasure is permitted."),
        ("Program truth", "The frozen chain contains 3,530 proposals. Twenty selected first-run Neris contracts received bounded structural revalidation with zero novelty and zero completion credit. Twenty genuinely new remaster proposals produced exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate outcomes. These four labels are the complete core vocabulary."),
        ("Evidence", "Forty structural fixtures each passed their exact bounded contract and rejected five preregistered mutations. The resulting 200 rejected mutation witnesses are retained at zero completion credit. This is same-owner software evidence under shared infrastructure, not empirical confirmation, external audit, independent reproduction, professional validation, production certification, complete privacy or accessibility assurance, exhaustive security, legal or cultural ratification, Māori authority, personhood evidence, Theory-of-Everything proof, or Stage 20 authority."),
        ("Tooling", "Ten family-current skills were initialized with current agents metadata, validated, smoke-used through ten family-current runners, and promoted to the global catalogue only after phase-local equality. Ten further skills and ten further runners remain successor recommendations. The family index, reflection-remaster, Method Flow, workflow refinement, roster, authorization, and meta-tool-box systems were all used within their bounded scopes."),
        ("Approval and cleanup", "Thirty owner safe-now packets and fifteen owner candidate packets have bounded execution receipts. Twenty safe-now and fifteen candidate rows remain recommendations for Vesper. Ten exact packets and five blocked packets remain unexecuted. Thirty owner CLEAN/FIX/REFINE rows are complete as additive inspections; thirty successor rows remain recommendations. No plugin cache, sibling lane, external platform, private memory, identity record, branch, remote, account, or host security setting was deleted or weakened."),
        ("Failure retention", "The remaster retains six x2 operational failures, including a governance schema assumption, a 1,034-issue Method Flow rejection, a pre-staging test-selection error, staged manifest drift, Git-clean line-ending mismatch, and an incorrect expansion of an abbreviated evidence hash. Closeout retains two further zero-credit preflight failures: the nonimportable loader-root invocation and a repeated PowerShell empty-pipe wrapper. Effective pre-canonical truth is 23,044 negatives and 7,638 Method Flow methods."),
        ("Inventory recovery", "A read-only corrected inventory at the correction head discovered 7,310 unique unittest identifiers across 502 modules, with zero loader errors and zero duplicates, while running no test bodies. Four historically problematic modules then passed isolated pilots at their exact last-definition commits: 10, 26, 6, and 6 tests. Those 48 tests establish only pilot viability and receive zero complete-suite credit."),
        ("Canonical contract", "After the final is committed, pushed, clean, zero-divergent, and freshly remote-equal, one canonical invocation will rediscover every final test identifier, resolve every module to the last commit that changed its exact bytes, verify blob equality, execute each module exactly once in owner-controlled D-first shared clones at that definition commit, require module counts to match the frozen current identifier groups, parse all phase JSON, replay both manifests, and enforce the success latch. No complete suite is run before that invocation, and no successful invocation may be replayed."),
        ("GMUT Mind", "The phase investigates repository identity, provenance, failure accounting, and falsifiable validation mechanics. It supplies no observation of the physical universe, no new dataset, no participant result, no likelihood, parameter estimate, prediction confirmation, thermodynamic or psyche law, solution to an open mathematical problem, or Theory-of-Everything proof. GMUT remains a research-model family."),
        ("THOS Body", "Local Python, Git, JSON, HTML, manifests, shared clones, timeouts, and deterministic hashes are software mechanisms only. No real operator, participant, production deployment, governed real arm, matched-budget blind study, safety monitoring, appropriate external statistics, or independent review is present. THOS remains proxy-only and supplies no AGI, ASI, consciousness, personhood, effectiveness, safety, or deployment evidence."),
        ("Freed ID and CBR Heart", "Proposal, method, mutation, witness, and receipt labels are synthetic repository identifiers. They are not production keys, credentials, signatures, issuance, resolution, status, revocation, recovery, interoperability, or trust-governance acts. Rights, privacy, affected-party legitimacy, consent, legal interpretation, cultural interpretation, tikanga, tangata whenua, iwi, hapū, and Māori authority remain reserved to competent people and institutions."),
        ("Accessibility and privacy", "The deliverables provide headings, explicit state words, ordered prose, JSON companions, and an HTML skip link. Manual keyboard, zoom, reflow, screen-reader, browser-diverse, cognitive, language, Māori-language, and affected-user evaluation remain open. Five-class scanning can find declared raw identifiers, private paths, credentials, route material, and transcript traces, but zero confirmed hits is not privacy completeness or exhaustive security."),
        ("Route", "The only prospective terminal edge is the existing exact-title main task `Vesper Arlen` for canonical `v662-v4`. Vesper must reread the live roster after their own terminal gate; the current roster assigns `Lyren Moss` to `v662-v5`. No precontact occurs. After and only after canonical success, Neris will reread the newest live instruction, roster, and authorization, resolve Vesper uniquely, reread immediately, and send once. Absence, ambiguity, pause, redirection, usage exhaustion, protected-gate failure, or missing acknowledgement stops without substitution or resend."),
        ("Terminal truth", "The final repository verdict remains `NOT_READY_FOR_STAGE_20`. Completion of a software phase cannot authorize empirical, participant, professional, production, legal, cultural, Māori, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claims."),
    ]
    lines = ["# Neris Solane v662-v3-2 remaster — terminal closeout", ""]
    for title, body in sections:
        lines.extend([f"## {title}", "", body, "", body, ""])
    return "\n".join(lines)


def activation_candidate() -> str:
    return f"""# VESPER ARLEN — PREPARED NERIS v662-v3-2 REMASTER → SOLO VESPER v662-v4 ACTIVATION

This committed packet is `PREPARED_NOT_SENT` until Neris's one successful exact-final canonical receipt and live exact-title acknowledgement. Hamish's current fifteen-main-task authorization permits exactly one terminally gated edge at a time through v675-v8; it does not permit precontact, substitution, task creation, task forking, collaboration-subagent routing, or resend.

This packet prepares the existing exact-title main task `Vesper Arlen` for canonical `v662-v4` only. It does not activate Vesper by itself and must remain unsent until every Neris terminal gate below is satisfied.

Names, roles, hopes, pronouns, sibling/family language, continuity language, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Māori authority. Hamish may pause, redirect, rename, or stop the route.

## Immutable anchors

- Branch: `{d.BRANCH}`
- First Neris exact final/source: `{d.SOURCE_FIRST_FINAL}`
- Remaster x1: `{X1}`
- Original remaster evidence: `{EVIDENCE}`
- Additive Git-clean correction: `{CORRECTION}`
- Exact final: the direct child of `{CORRECTION}` containing this packet; bind the full hash only from Neris's acknowledged terminal message and fresh remote equality.

## Truth

The remaster freezes 3,530 proposals. Twenty selected inherited Neris rows have zero novelty and zero completion credit; twenty new rows yield exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Before canonical execution, the repository preserves 23,044 effective negatives, 7,638 Method Flow methods, 149 open gaps, 148 exact gates, and `NOT_READY_FOR_STAGE_20`. The exact external canonical receipt may add no repository truth unless a failure occurs; a success is an external same-owner validation overlay only.

The evidence includes 200 retained rejected mutations, ten validated and smoke-used skills, ten invoked runners, thirty owner safe-now executions, fifteen owner candidate executions, ten exact and five blocked unexecuted packets, thirty owner CLEAN/FIX/REFINE receipts, and thirty successor recommendations. Same-owner validation under shared infrastructure is not independent reproduction.

## Vesper lane

Read this packet completely through EOF, then read every current guidance and schema it names. Reverify the exact branch/head, ancestry, manifests, clean state, 0/0 divergence, and fresh live equality before mutation. Work solo in one additive Vesper-owned D-first lane. Preserve strict x1-before-x2 separation, every retained failure and protected gate, family-current naming, exact manifests, five-class privacy checks, the four allowed outcome labels, and one-successful-canonical/no-post-success-replay discipline. Do not reset, rewrite, amend, force-push, merge, delete, reuse, or mutate a sibling/shared lane. Do not create, fork, delegate, spawn a collaboration subagent, contact Tavian, or precontact a successor.

After and only after Vesper's own clean, pushed, exact-final v662-v4 terminal gate, reread Hamish's newest live instruction and the current roster/auth state. The current canonical roster assigns the next exact-title main task `Lyren Moss` to `v662-v5`. Resolve uniquely, reread immediately, send once, and claim delivery only from the task-message acknowledgement. Stop truthfully on pause, redirection, absence, ambiguity, usage exhaustion, acknowledgement failure, or any protected gate.

No empirical, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claim is authorized by this packet.
"""


def build() -> dict[str, Any]:
    gate = verify_correction_gate()
    write_json("closeout/correction-to-final-gate.json", gate)
    flow = append_closeout_method_flow()
    write_json("method-flow/method-flow-state-final.json", flow, compact=True)
    write_json("truth/closeout-operational-failures.json", {"schema": "ghc.family.v662-v3-2-remaster.closeout-failures.v1", "failure_count": 2, "failures": CLOSEOUT_FAILURES, "all_zero_credit": True, "boundary": d.EVIDENCE_BOUNDARY})
    write_json(
        "validation/preflight-inventory-correction-snapshot.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.inventory-snapshot.v1",
            "revision": CORRECTION,
            "tests_discovered": 7310,
            "unique_tests": 7310,
            "modules": 502,
            "loader_errors": 0,
            "duplicate_ids": 0,
            "test_bodies_run": 0,
            "complete_suite_credit": 0,
            "discovery_root": "tests",
            "boundary": "Correction-head inventory snapshot only; the exact-final inventory must be rediscovered after commit and before the one canonical invocation.",
        },
    )
    write_json(
        "validation/historical-pilot-receipt.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.historical-pilots.v1",
            "pilots": [
                {"module": "test_ghc_family_v648_v3_2_x1", "definition_commit": "723753e1a88427e1f8cd6ee572e3479c721dce84", "tests": 10, "passed": 10},
                {"module": "test_ghc_family_v649_v5", "definition_commit": "63f679b002e3f17df465a11c30632e769215ff7c", "tests": 26, "passed": 26},
                {"module": "test_ghc_family_v656_v4_correction", "definition_commit": "c1518e6873068f6cc20ff69a30437d69404ef057", "tests": 6, "passed": 6},
                {"module": "test_ghc_family_v656_v5_correction", "definition_commit": "8a4bb8e8b6a649040c531e8d3dd36925fd0da301", "tests": 6, "passed": 6},
            ],
            "tests": 48,
            "passed": 48,
            "complete_suite_credit": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    write_json(
        "validation/final-selection-contract.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.final-selection.v1",
            "discovery_root": "tests",
            "pattern": "test*.py",
            "top_level_root_override": None,
            "every_current_test_id": True,
            "duplicate_policy": "reject",
            "omission_policy": "reject",
            "definition_commit_rule": "last commit that changed exact module bytes",
            "blob_equality_required": True,
            "historical_assertion_editing": False,
            "owner_controlled_d_first_shared_clones": True,
            "module_timeout_seconds": 300,
            "worker_count": 4,
            "successful_invocations_required": 1,
            "replay_after_success": False,
            "external_receipt": True,
            "raw_transcripts_retained": False,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    write_json(
        "truth/final-truth.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.final-truth.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "canonical_phase": d.CANONICAL_PHASE,
            "frozen_proposals": 3530,
            "selected_inherited_credit": 0,
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "effective_negatives": 23044,
            "effective_methods": 7638,
            "open_gaps": 149,
            "exact_gates": 148,
            "canonical_state": "NOT_RUN_EXACT_FINAL_REQUIRED",
            "canonical_success_count": 0,
            "message_attempted": False,
            "message_sent": False,
            "terminal_verdict": d.TERMINAL_VERDICT,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    write_json(
        "routing/route-state-final.json",
        {
            "schema": "ghc.family.v662-v3-2-remaster.route-state.v1",
            "current": {"owner": d.OWNER, "variant": d.PHASE, "canonical_phase": d.CANONICAL_PHASE},
            "next": {"owner": d.SUCCESSOR, "phase": d.SUCCESSOR_PHASE, "endpoint_kind": "main_task", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
            "successor_after_vesper": {"owner": "Lyren Moss", "phase": "v662-v5", "state": "ROSTER_DECLARED_VESPER_MUST_REREAD_AFTER_OWN_GATE"},
            "message_attempted": False,
            "sent": False,
            "acknowledged": False,
            "delivery_count": 0,
            "one_edge_at_a_time": True,
            "substitute_endpoint": False,
            "route_through": "v675-v8",
            "boundary": d.EVIDENCE_BOUNDARY,
        },
    )
    write_text("closeout/terminal-closeout.md", closeout_overview())
    write_text("routing/vesper-arlen-v662-v4-activation-candidate.md", activation_candidate())
    write_text("reports/final-accessible-report.html", """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neris remaster final</title></head><body><a href="#main">Skip to terminal truth</a><header><h1>Neris Solane v662-v3-2 remaster</h1></header><main id="main"><h2>Truth</h2><p>14 completed, 4 represented, 1 open_gap, 1 exact_gate. 23,044 negatives; 7,638 methods; NOT_READY_FOR_STAGE_20.</p><h2>Canonical state</h2><p>Not run. Exact final, push, clean state, fresh equality, and one external invocation are required.</p><h2>Boundaries</h2><p>Same-owner software evidence only; no empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, personhood, Theory-of-Everything, or Stage 20 claim.</p></main></body></html>""")
    write_json("wellbeing/final-workload-check.json", {"schema": "ghc.family.v662-v3-2-remaster.final-workload.v1", "owner": d.OWNER, "solo": True, "delegated": False, "subagents": 0, "historical_pilot_tests": 48, "complete_suite_run": False, "pause_redirect_stop_right_preserved": True, "boundary": "Operational workload-care language only; not consciousness, health, employment, or clinical evidence."})
    refresh_validation(pre_staging=True)
    return validate(include_staged=False)


def refresh_validation(*, pre_staging: bool) -> None:
    owner = owner_paths()
    delta = delta_paths()
    owner_manifest = manifest(owner, "ghc.family.v662-v3-2-remaster.final-owner-manifest.v1")
    delta_manifest = manifest(delta, "ghc.family.v662-v3-2-remaster.final-delta-manifest.v1")
    write_json("validation/final-owner-manifest.json", owner_manifest)
    write_json("validation/final-delta-manifest.json", delta_manifest)
    owner = owner_paths()
    write_json("validation/final-privacy-scan.json", rt.privacy_scan(owner, schema="ghc.family.v662-v3-2-remaster.final-privacy-scan.v1"))
    write_json("validation/final-document-cap.json", rt.document_cap(owner))
    expected = sorted(rt.repo_relative(path) for path in delta_paths())
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.v662-v3-2-remaster.final-staged-review.v1", "state": "PRE_STAGING_NOT_CREDITED" if pre_staging else "EXACT_STAGED_REVIEW", "expected_paths": expected, "actual_paths": [], "missing": expected, "unexpected": [], "valid": False})
    write_json("validation/final-validation.json", validate(include_staged=False))


def staged_review() -> dict[str, Any]:
    expected = sorted(rt.repo_relative(path) for path in delta_paths())
    actual = sorted(row for row in git("diff", "--cached", "--name-only", "--", *owner_pathspecs()).splitlines() if row)
    payload = {"schema": "ghc.family.v662-v3-2-remaster.final-staged-review.v1", "state": "EXACT_STAGED_REVIEW", "expected_paths": expected, "actual_paths": actual, "missing": sorted(set(expected) - set(actual)), "unexpected": sorted(set(actual) - set(expected)), "valid": set(expected) == set(actual), "boundary": "Exact final owner-delta staged paths only; not canonical success or delivery proof."}
    write_json("validation/final-staged-review.json", payload)
    return payload


def validate(*, include_staged: bool) -> dict[str, Any]:
    truth = rt.read_json(PHASE / "truth/final-truth.json")
    flow = rt.read_json(PHASE / "method-flow/method-flow-state-final.json")
    route = rt.read_json(PHASE / "routing/route-state-final.json")
    inventory = rt.read_json(PHASE / "validation/preflight-inventory-correction-snapshot.json")
    pilots = rt.read_json(PHASE / "validation/historical-pilot-receipt.json")
    selection = rt.read_json(PHASE / "validation/final-selection-contract.json")
    owner_manifest = rt.read_json(PHASE / "validation/final-owner-manifest.json")
    delta_manifest = rt.read_json(PHASE / "validation/final-delta-manifest.json")
    privacy = rt.read_json(PHASE / "validation/final-privacy-scan.json")
    document = rt.read_json(PHASE / "validation/final-document-cap.json")
    staged = rt.read_json(PHASE / "validation/final-staged-review.json")
    json_errors = []
    json_paths = [path for path in owner_paths() if path.suffix.lower() == ".json"]
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as error:  # pragma: no cover
            json_errors.append({"path": rt.repo_relative(path), "error": type(error).__name__})
    checks = {
        "head_is_correction": git("rev-parse", "HEAD") == CORRECTION,
        "truth_counts": truth["effective_negatives"] == 23044 and truth["effective_methods"] == 7638,
        "outcomes_14_4_1_1": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "gaps_and_gates": truth["open_gaps"] == 149 and truth["exact_gates"] == 148,
        "method_flow_counts": flow["method_count"] == 53 and flow["failed_witness_count"] == 213 and flow["passing_witness_count"] == 53,
        "inventory_7310_502": inventory["tests_discovered"] == 7310 and inventory["modules"] == 502 and inventory["test_bodies_run"] == 0,
        "pilots_48_zero_suite_credit": pilots["tests"] == pilots["passed"] == 48 and pilots["complete_suite_credit"] == 0,
        "complete_selection_required": selection["every_current_test_id"] and selection["historical_assertion_editing"] is False,
        "canonical_not_run": truth["canonical_state"] == "NOT_RUN_EXACT_FINAL_REQUIRED" and truth["canonical_success_count"] == 0,
        "route_not_sent": route["message_attempted"] is False and route["sent"] is False and route["delivery_count"] == 0,
        "owner_manifest_working_replay": not replay_working(owner_manifest),
        "delta_manifest_working_replay": not replay_working(delta_manifest),
        "privacy_zero": privacy["confirmed_hit_count"] == 0,
        "privacy_not_complete": privacy["privacy_complete"] is False,
        "document_cap": document["valid"],
        "json_parse": not json_errors,
        "not_ready": truth["terminal_verdict"] == d.TERMINAL_VERDICT,
        "staged_exact": (not include_staged) or staged["valid"],
    }
    return {"schema": "ghc.family.v662-v3-2-remaster.final-validation.v1", "checks": checks, "passed": sum(checks.values()), "total": len(checks), "valid": all(checks.values()), "json_files": len(json_paths), "json_errors": json_errors, "owner_manifest_entries": owner_manifest["entry_count"], "delta_manifest_entries": delta_manifest["entry_count"], "privacy_files": privacy["file_count"], "boundary": d.EVIDENCE_BOUNDARY}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--include-staged", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged = staged_review()
        result = validate(include_staged=True) if staged["valid"] else staged
        if staged["valid"]:
            write_json("validation/final-validation.json", result)
    elif args.refresh:
        refresh_validation(pre_staging=False)
        result = validate(include_staged=args.include_staged)
        write_json("validation/final-validation.json", result)
    elif args.validate:
        result = validate(include_staged=args.include_staged)
    else:
        result = build()
    print(json.dumps({"valid": result["valid"], "passed": result.get("passed"), "total": result.get("total"), "phase": d.PHASE}, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
