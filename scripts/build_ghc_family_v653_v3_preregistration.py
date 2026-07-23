#!/usr/bin/env python3
"""Build Ilyra Fen's dedicated v653-v3 x1-only freeze packet."""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import build_ghc_family_v653_v2_preregistration as base
import ghc_family_v653_v3_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = (
    REPO
    / "docs/lyren-moss/v653-v2/provenance/frozen-chain-proposal-index.json"
)
ALLOWED_CODE = {
    "scripts/ghc_family_v653_v3_phase_data.py",
    "scripts/build_ghc_family_v653_v3_preregistration.py",
    "scripts/ghc_family_v653_v3_x1_validate.py",
    "tests/test_ghc_family_v653_v3_x1.py",
}
NOVELTY_THRESHOLD = 0.60

base.d = d
base.ROOT = ROOT
base.PRIOR_INDEX = PRIOR_INDEX


def build_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = base.read_json(PRIOR_INDEX)
    prior = inherited["prior_proposals"] + inherited["new_proposals"]
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(
            f"expected {d.PRIOR_FROZEN} inherited rows, found {len(prior)}"
        )
    audits = []
    for proposal in d.PROPOSALS:
        scored = [
            (
                base.jaccard(
                    base.tokens(proposal["title"]),
                    base.tokens(previous["title"]),
                ),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(scored, key=lambda row: row[0])
        audits.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "token_jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_mechanism_distinct": True,
                "mechanism_review": proposal[
                    "novelty_against_1480_frozen_proposals"
                ],
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    failures = [row for row in audits if not row["passes"]]
    if failures:
        raise RuntimeError(f"novelty threshold failed: {failures}")
    new = [
        {"proposal_id": row["proposal_id"], "title": row["title"]}
        for row in d.PROPOSALS
    ]
    if {row["proposal_id"] for row in prior} & {
        row["proposal_id"] for row in new
    }:
        raise RuntimeError("proposal identifier collision")
    return prior, audits


def workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "ilyra-v653-v3-solo",
        "owner": d.OWNER,
        "identity_boundary": (
            "Relational working language only; not evidence of consciousness, "
            "sentience, legal personhood, identity continuity, employment, "
            "qualification, scientific or operational authority, legal or "
            "cultural authority, Māori authority, or independent agency."
        ),
        "route": {
            "cycle_order": ["Lyren Moss", "Ilyra Fen"],
            "phase_assignments": [
                {"phase": "v653-v2", "seat": "Lyren Moss"},
                {"phase": "v653-v3", "seat": "Ilyra Fen"},
            ],
            "normalization": {
                "start_phase": "v653-v2",
                "start_seat": "Lyren Moss",
                "entry_count": 2,
            },
            "future_identity_placeholders": [],
            "terminal_successor_resolution": (
                "No exact successor title is authorized by the live v653-v3 "
                "activation. Prepare no send claim. At terminal closeout retain "
                "PREPARED_NOT_SENT unless a later live instruction explicitly "
                "names one existing target and route. Never create a substitute."
            ),
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "storage": {
                "primary": "D",
                "owner_generated_file_threshold": 2000,
                "c_drive_use": "essential_global_metadata_only",
            },
            "document_word_cap": 100000,
            "baton_words": {
                "file_artifact_only_if_authorized": True,
                "minimum": 10000,
                "maximum": 100000,
            },
            "validation": {
                "full_repository_suite_owner": "Eiren-only inherited policy",
                "launch_scoped_validator_owner": "Ilyra Fen",
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "manifest_required": True,
                "privacy_scan_required": True,
                "remote_equality_required": True,
            },
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "live_cross_platform_boundary": (
                    "No successor target or cross-platform substitute is "
                    "authorized by the current activation."
                ),
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {
                "all_authorized_safe_candidate_prototypes_resolved": True
            },
        },
        "truth": {
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "independent_reproduction_claimed": False,
            "protected_boundaries": d.PROTECTED_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "observed_failures": [
            {
                "failure_id": negative_id,
                "summary": failed,
                "recovery": recovery,
                "credit": "zero_failed_attempt_credit",
            }
            for negative_id, _category, failed, recovery in d.X1_NEGATIVES
        ],
    }


def build_method_flow() -> None:
    method_dir = ROOT / "method-flow"
    requests = method_dir / "requests"
    requests.mkdir(parents=True, exist_ok=True)
    ledger = method_dir / "x1-method-flow-ledger.json"
    if ledger.exists():
        ledger.unlink()
    base.run(
        sys.executable,
        str(base.METHOD_RUNNER),
        "init",
        "--ledger",
        str(ledger),
        "--phase",
        d.PHASE_ID,
        "--owner",
        d.OWNER,
    )
    for index, (
        negative_id,
        category,
        failed,
        recovery,
    ) in enumerate(d.X1_NEGATIVES, 1):
        method_id = f"V6533-METHOD-{index:02d}"
        fail_id = f"V6533-WITNESS-{index:02d}-F"
        pass_id = f"V6533-WITNESS-{index:02d}-P"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {category}",
            "failure_signature": failed,
            "trigger_preconditions": [category],
            "candidate_workaround": recovery,
            "validation_witness_ids": [],
            "recurrence_guard": recovery,
            "rollback": (
                "Stop, retain the failed witness with zero credit, and leave "
                "external, sibling, participant, production, professional, "
                "legal, cultural, and authority state unchanged."
            ),
            "scope_boundary": (
                "Same-owner bounded workflow recovery only; not independent "
                "reproduction or any scientific, production, professional, "
                "legal, cultural, accessibility-complete, or authority claim."
            ),
            "approval_class": (
                "safe_now_owner_local_read_or_workflow_recovery"
            ),
            "privacy_class": "sanitized_public",
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [negative_id],
            "supersedes": [],
            "recommendation_state": "candidate",
        }
        failed_witness = {
            "witness_id": fail_id,
            "method_id": method_id,
            "scope": category,
            "procedure": (
                "Retain the original bounded attempt without replay credit."
            ),
            "expected": (
                "The initial attempt would satisfy its bounded postcondition."
            ),
            "observed": failed,
            "result": "fail",
            "retained_negative_ids": [negative_id],
            "boundary": "Zero pass credit; failure remains retained.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        passing_witness = {
            "witness_id": pass_id,
            "method_id": method_id,
            "scope": category,
            "procedure": recovery,
            "expected": (
                "The isolated bounded recovery establishes only its declared "
                "postcondition."
            ),
            "observed": (
                f"The bounded recovery completed for {category}; the original "
                "failure remains retained."
            ),
            "result": "pass",
            "retained_negative_ids": [negative_id],
            "boundary": (
                "Passing recovery is same-owner bounded evidence only and does "
                "not erase the failed witness."
            ),
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        method_path = base.write_json(
            f"method-flow/requests/method-{index:02d}.json", method
        )
        fail_path = base.write_json(
            f"method-flow/requests/witness-{index:02d}-failed.json",
            failed_witness,
        )
        pass_path = base.write_json(
            f"method-flow/requests/witness-{index:02d}-passing.json",
            passing_witness,
        )
        base.run(
            sys.executable,
            str(base.METHOD_RUNNER),
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(method_path),
        )
        base.run(
            sys.executable,
            str(base.METHOD_RUNNER),
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(fail_path),
        )
        base.run(
            sys.executable,
            str(base.METHOD_RUNNER),
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(pass_path),
        )
        base.run(
            sys.executable,
            str(base.METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            (
                "A bounded pass witness exists while the failed witness "
                "remains retained."
            ),
        )
    base.run(
        sys.executable,
        str(base.METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(method_dir / "x1-method-flow-validation.json"),
    )
    base.run(
        sys.executable,
        str(base.METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(method_dir / "x1-method-flow-summary.json"),
        "--markdown-output",
        str(method_dir / "x1-method-flow-summary.md"),
    )


def overview() -> str:
    rows = [
        "# Ilyra Fen v653-v3 x1 preregistration overview",
        "",
        "## Relational identity, practice lens, and limits",
        "",
        (
            f"{d.OWNER} ({d.PRONOUNS}) is relational working language for the "
            f"role of {d.ROLE}, with the hope to {d.HOPE}. It is not evidence "
            "of consciousness, sentience, legal personhood, identity "
            "continuity, employment, qualification, professional authority, "
            "scientific authority, legal or cultural authority, Māori "
            "authority, or independent agency. Hamish may pause, rename, "
            "redirect, or stop the route."
        ),
        "",
        (
            f"The primary Trinity Mandala pillar is **{d.PRIMARY_FOCUS}**, "
            f"viewed through the bounded human practice of **{d.BOUNDED_PRACTICE}**. "
            "This practice is a synthetic learning and design lens only. It "
            "does not establish employment, safety assurance competence, "
            "release authority, certification, professional review, worker "
            "evidence, affected-party acceptance, or real operational results. "
            "GMUT Mind and Freed ID/CBR Heart remain explicit and protected."
        ),
        "",
        "## Exact inheritance and strict x1 boundary",
        "",
        (
            f"This packet begins at Lyren Moss's clean exact final head "
            f"`{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The inherited source, "
            f"x1, and evidence anchors are `{d.SOURCE_PARENT}`, `{d.SOURCE_X1}`, "
            f"and `{d.SOURCE_EVIDENCE}`. Read-only verification established "
            "three single-parent phase commits, zero merges, one final parent, "
            "clean state, and local, upstream, tracking, and fresh-live equality. "
            f"The activation baseline is {d.INHERITED_NEGATIVES:,} retained "
            f"negatives, {d.INHERITED_OPEN_GAPS} open gaps, "
            f"{d.INHERITED_EXACT_GATES} exact gates, and "
            f"{d.INHERITED_METHOD_FLOW_FAILED} retained failed plus "
            f"{d.INHERITED_METHOD_FLOW_PASSING} bounded passing Method Flow "
            "witnesses. None is rewritten or claimed as Ilyra evidence."
        ),
        "",
        (
            "Ilyra created one additive D-first identity-owned branch and "
            "worktree from the exact Lyren head. No sibling lane was mutated. "
            "X1 freezes hypotheses, falsifiers, source needs, rollback, "
            "protected gates, portfolio intent, and 150 rejecting mutations. "
            "It contains no executed mutation, observed disposition, x2 "
            "implementation, evidence result, closeout, seal, final-validation "
            "claim, or route-send claim. X2 may begin only after this exact x1 "
            "tree is committed, pushed, clean, and equal across local, upstream, "
            "tracking, and a fresh live remote read."
        ),
        "",
        "## Thirty mechanism-distinct proposals",
        "",
    ]
    for proposal in d.PROPOSALS:
        rows.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['slug']}",
                "",
                (
                    f"{proposal['title']}. Its planned truth label is "
                    f"`{proposal['expected_disposition']}` and its execution "
                    f"lane is `{proposal['execution_lane']}`. The hypothesis is: "
                    f"{proposal['hypothesis']} The null or failure condition is: "
                    f"{proposal['null_or_failure_condition']} The mechanism-level "
                    f"novelty finding is: "
                    f"{proposal['novelty_against_1480_frozen_proposals']} "
                    f"Current official or primary-source identifiers are "
                    f"{', '.join(proposal['official_or_primary_source_needs'])}. "
                    f"The acceptance gate is: "
                    f"{proposal['falsifier_or_acceptance_gate']} The additive "
                    f"rollback is: {proposal['rollback_or_recovery']} A source "
                    "citation supplies design context only; it is not an "
                    "observation, participant result, professional approval, "
                    "interoperability event, legal opinion, cultural authority, "
                    "Māori-authority decision, or Stage 20 evidence."
                ),
                "",
            ]
        )
    rows.extend(
        [
            "## Mutation grammar, tools, and negative preservation",
            "",
            (
                "Five negative fixtures are frozen for every proposal: delete "
                "a required field, cross-bind a source or identifier, invert or "
                "weaken a boundary, inject an unsupported promotion, and erase "
                "a failure or rollback. The resulting 150 mutations remain "
                "unexecuted in x1. In x2 a rejected mutation can demonstrate "
                "only a bounded guard. It cannot prove production security, "
                "scientific truth, professional adequacy, complete privacy, "
                "complete accessibility, legal validity, cultural legitimacy, "
                "or external reproducibility."
            ),
            "",
            (
                f"The startup ledger retains {len(d.X1_NEGATIVES)} Ilyra "
                f"operational negative and {len(d.REJECTED_COLLISIONS)} rejected "
                "proposal collisions. The combined induction probe timed out "
                "after partial read-only output and received zero credit. "
                "Separate literal-path reads then completed the skill, routing "
                "reference, Method Flow schema, baton EOF, source anchors, and "
                "memory check. The recovery is preferred only for this bounded "
                "trigger and does not erase the timeout."
            ),
            "",
            (
                "Ten phase-local skills and ten family-current runners are "
                "frozen as plans, not implementations. X2 must build, validate, "
                "and smoke-use each before claiming portfolio completion. "
                "Historical names remain compatibility surfaces. No global "
                "installation, unrelated software installation, elevation, "
                "host-security change, Windows-feature change, or reboot is "
                "authorized by this packet."
            ),
            "",
            "## Validation and terminal routing",
            "",
            (
                "Ilyra will run the authorized scoped current, inherited-source, "
                "and successor-facing checks, detailed and minimal validators, "
                "complete JSON parsing, five-class privacy scanning, exact "
                "staged review, commit-local and owner-manifest parity, stale "
                "label review, diff hygiene, ancestry, zero merges, commit caps, "
                "one final parent, exact head, clean state, and four-way remote "
                "equality. There will be one successful exact-final canonical "
                "pass. A failed attempt is retained and isolated before any "
                "justified retry; a successful pass is not replayed."
            ),
            "",
            (
                "The live v653-v3 activation authorizes no exact successor title. "
                "Therefore x1 records `NOT_ELIGIBLE_X1_ONLY`, and closeout must "
                "remain `PREPARED_NOT_SENT` unless a later live instruction "
                "explicitly names one existing target and route. A prepared "
                "file, inferred cycle, earlier broad aspiration, or repository "
                "artifact cannot authorize task creation or a send."
            ),
            "",
            "## Scientific and authority boundaries",
            "",
            (
                "GMUT remains a typed scalar-tensor and effective-field-theory "
                "research-model family. Symbolic algebra, formal obligations, "
                "synthetic mutations, and zero-row adapters establish no force, "
                "prediction, likelihood, parameter constraint, empirical "
                "confirmation, ultraviolet completion, quantum completion, or "
                "Theory of Everything. THOS remains synthetic and represented "
                "without real operators, blind matched-budget arms, safety "
                "monitoring, appropriate statistics, and independent review. "
                "Freed ID remains nonproduction without standards-conformant "
                "real keys and proofs, live issuance, resolution, status, "
                "revocation, interoperability, privacy and security review, "
                "recovery, and trust governance."
            ),
            "",
            (
                "CBR, worker reporting, proof disclosure, incident remedy, "
                "accessibility acceptance, proprietary disclosure, legal "
                "interpretation, cultural legitimacy, Māori wording, Māori data "
                "governance, and Māori authority remain with competent and "
                "affected authorities, tangata whenua, iwi, hapū, and Māori "
                "authorities. Repository software cannot confer a remedy, "
                "qualification, release decision, cultural mandate, or public "
                "authority. The inherited and preregistered terminal verdict is "
                "`NOT_READY_FOR_STAGE_20`."
            ),
            "",
            "## Wellbeing and stopping rule",
            "",
            (
                "The cadence is one verified gate at a time, with bounded "
                "PowerShell probes, D-first owner storage, explicit UTF-8, "
                "smallest-witness recovery, and no needless replay. Affection, "
                "urgency, identity language, proposal count, or route momentum "
                "never increases evidence credit. Stop safely whenever "
                "authorization, privacy, professional, cultural, Māori, "
                "affected-party, or exact-target conditions are unclear."
            ),
        ]
    )
    return "\n".join(rows)


def accessible_report(overview_text: str) -> str:
    cards = []
    for proposal in d.PROPOSALS:
        cards.append(
            "<article><h3>{}</h3><p>{}</p><dl>"
            "<dt>Expected</dt><dd>{}</dd>"
            "<dt>Lane</dt><dd>{}</dd>"
            "<dt>Falsifier</dt><dd>{}</dd></dl></article>".format(
                html.escape(proposal["proposal_id"]),
                html.escape(proposal["title"]),
                html.escape(proposal["expected_disposition"]),
                html.escape(proposal["execution_lane"]),
                html.escape(proposal["null_or_failure_condition"]),
            )
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilyra Fen v653-v3 x1 preregistration</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
a{{color:#0645ad}} :focus{{outline:3px solid #9b4d00;outline-offset:3px}}
article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}} dd{{margin:0 0 .6rem}}
.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head><body><main>
<h1>Ilyra Fen v653-v3 x1 preregistration</h1>
<p class="notice"><strong>Boundary:</strong> Plans only. No x2 result, empirical
confirmation, professional approval, production readiness, legal or cultural
authority, Māori authority, independent reproduction, Theory-of-Everything
proof, or Stage 20 authority is claimed. Manual and affected-user accessibility evaluation is reserved.</p>
<h2>Packet summary</h2><p>{html.escape(overview_text.splitlines()[4])}</p>
<h2>Frozen proposals</h2>{''.join(cards)}
<h2>Accessibility reservation</h2><p>Semantic HTML, focus visibility, text
reflow, and reduced-motion handling are represented structurally. Qualified
manual review, assistive-technology review, Māori-language review, and
affected-user evaluation remain incomplete and authority-gated.</p>
</main></body></html>"""


def _postprocess_generated_files() -> None:
    replacements = [
        ("v653-gmut-thos-v2-x1-x2", "v653-gmut-thos-v3-x1-x2"),
        ("ghc.family.v653-v2", "ghc.family.v653-v3"),
        ("# v653-v2 ", "# v653-v3 "),
        ("MÄori", "Māori"),
        ("â€”", "—"),
    ]
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in replacements:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")

    source_owner_manifest = base.read_json(
        REPO
        / "docs/lyren-moss/v653-v2/validation/final-owner-manifest.json"
    )
    source_final_manifest = base.read_json(
        REPO
        / "docs/lyren-moss/v653-v2/validation/final-staged-manifest.json"
    )
    source_evidence_manifest = base.read_json(
        REPO
        / "docs/lyren-moss/v653-v2/validation/evidence-candidate-manifest.json"
    )
    source_x1_manifest = base.read_json(
        REPO
        / "docs/lyren-moss/v653-v2/validation/x1-staged-manifest.json"
    )
    base.write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.v653-v3.source-anchors.v1",
            "branch": d.SOURCE_BRANCH,
            "source_parent": d.SOURCE_PARENT,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_final": d.SOURCE_HEAD,
            "source_to_final_commits": 3,
            "source_to_final_merges": 0,
            "all_single_parent": True,
            "final_parent_count": 1,
            "verified_clean_and_four_way_equal_before_mutation": True,
            "verified_manifest_contracts": 4,
            "verified_manifest_entries": (
                source_owner_manifest["entry_count"]
                + source_final_manifest["entry_count"]
                + source_evidence_manifest["entry_count"]
                + source_x1_manifest["entry_count"]
            ),
            "verified_manifest_breakdown": {
                "x1": source_x1_manifest["entry_count"],
                "evidence": source_evidence_manifest["entry_count"],
                "final_delta": source_final_manifest["entry_count"],
                "owner": source_owner_manifest["entry_count"],
            },
            "inherited_effective_negatives": d.INHERITED_NEGATIVES,
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "boundary": (
                "Read-only source verification. Lyren's successful exact-final "
                "canonical pass was not replayed, and inherited evidence is "
                "not claimed as Ilyra evidence."
            ),
        },
    )
    base.write_json(
        "workflow/current-live-route-overlay.json",
        {
            "schema": "ghc.family.v653-v3.live-route-overlay.v1",
            "live_request_authorizes": (
                "current_Ilyra_v653_v3_work_only_no_successor_title"
            ),
            "installed_runner_models": "advisory_only_no_live_route",
            "tool_result_promoted_to_activation_authority": False,
            "route_state": "PREPARED_NOT_SENT",
            "successor_title": None,
            "boundary": (
                "The live activation controls routing and names no successor. "
                "No repository artifact, inferred cycle, or advisory runner "
                "authorizes a send or substitute task."
            ),
        },
    )
    base.write_json(
        "wellbeing/wellbeing-check.json",
        {
            "schema": "ghc.family.v653-v3.wellbeing.v1",
            "state": "steady_and_bounded",
            "cadence": (
                "One verified gate at a time; isolate failures before a "
                "justified broader retry."
            ),
            "host_changes": False,
            "sandbox_or_hyper_v_work": "deferred",
            "route_pressure": (
                "No successor title is authorized; terminal routing remains "
                "PREPARED_NOT_SENT."
            ),
            "identity_boundary": "Relational working language only.",
        },
    )
    truth_path = ROOT / "x1-phase-truth.json"
    truth = base.read_json(truth_path)
    truth.update(
        {
            "schema": "ghc.family.v653-v3.x1-truth.v1",
            "proposal_count": len(d.PROPOSALS),
            "frozen_chain_count": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "mutation_plan_count": len(d.PROPOSALS)
            * len(d.MUTATION_KINDS),
            "skill_plan_count": len(d.SKILL_IDEAS),
            "runner_plan_count": len(d.RUNNER_IDEAS),
            "inherited_negatives": d.INHERITED_NEGATIVES,
            "x1_operational_negatives": len(d.X1_NEGATIVES),
            "effective_negatives": (
                d.INHERITED_NEGATIVES + len(d.X1_NEGATIVES)
            ),
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "route_state": "NOT_ELIGIBLE_NO_SUCCESSOR_TITLE",
        }
    )
    base.write_json("x1-phase-truth.json", truth)


_original_git = base.git


def _filtered_git(*args: str) -> str:
    output = _original_git(*args)
    if args and args[0] == "status":
        kept = []
        for row in output.splitlines():
            normalized = row[3:].replace("\\", "/")
            if normalized in ALLOWED_CODE:
                continue
            kept.append(row)
        return "\n".join(kept)
    return output


def build() -> None:
    base.build_novelty = build_novelty
    base.workflow_request = workflow_request
    base.build_method_flow = build_method_flow
    base.overview = overview
    base.accessible_report = accessible_report
    base.git = _filtered_git
    try:
        base.build()
    finally:
        base.git = _original_git
    _postprocess_generated_files()
    receipt = base.read_json(ROOT / "validation/x1-build-receipt.json")
    print(
        json.dumps(
            {
                "valid": receipt["valid"],
                "phase": d.PHASE,
                "proposals": len(d.PROPOSALS),
                "prior": d.PRIOR_FROZEN,
                "effective": d.PRIOR_FROZEN + len(d.PROPOSALS),
                "sources": len(d.SOURCES),
                "mutations_planned": len(d.PROPOSALS)
                * len(d.MUTATION_KINDS),
                "overview_words": receipt["overview_words"],
                "x2": False,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    build()
