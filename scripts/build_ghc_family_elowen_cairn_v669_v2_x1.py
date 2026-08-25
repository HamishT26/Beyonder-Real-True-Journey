from __future__ import annotations

import json
import platform
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_elowen_cairn_v669_v2_archive import (
    ACTIVATION_OVERLAY,
    ALLOWED_OUTCOMES,
    BRANCH,
    DOCUMENT_WORD_CEILING,
    EVIDENCE_BOUNDARY,
    FILE_CEILING,
    IDENTITY_BOUNDARY,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PORTFOLIO_COUNTS,
    PRACTICE,
    PRIMARY_PILLAR,
    PRONOUNS,
    PROPOSAL_BLUEPRINTS,
    PROTECTED_GATES,
    RECOVERED_HISTORICAL_ROWS,
    RECOVERED_UNIQUE_NORMALIZED_TITLES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_BRANCH,
    SOURCE_CANONICAL_PAYLOAD_SHA256,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_EVIDENCE,
    SOURCE_FINAL,
    SOURCE_LEDGER,
    SOURCE_OVERLAY,
    SOURCE_START,
    SOURCE_TERMINAL_STATUS,
    SOURCE_X1,
    STARTUP_FAILURES,
    TERMINAL_VERDICT,
    UNRECOVERED_DECLARED_ROWS,
    assert_x1_start,
    generated_portfolios,
    historical_proposal_inventory,
    manifest_rows,
    phase_owner_files,
    proposal_rows,
    successor_recommendations,
    utc_now,
    word_count,
)


def write_json(relative: str | Path, value: Any) -> Path:
    path = ROOT / Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_text(relative: str | Path, value: str) -> Path:
    path = ROOT / Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")
    return path


def command_version(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    output = (completed.stdout or completed.stderr).strip().splitlines()
    return {"command": command, "return_code": completed.returncode, "first_line": output[0] if output else ""}


def shard_rows(prefix: str, rows: list[dict[str, Any]], size: int = 5) -> list[str]:
    paths: list[str] = []
    for offset in range(0, len(rows), size):
        number = offset // size + 1
        relative = f"{prefix}-{number:02d}.json"
        write_json(relative, {"rows": rows[offset : offset + size], "schema": "ghc.family.proposal-freeze-shard.v1"})
        paths.append(relative)
    return paths


def method_flow(now: str) -> tuple[dict[str, Any], dict[str, Any]]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    for index, (negative_id, observed, workaround, guard) in enumerate(STARTUP_FAILURES, 1):
        method_id = f"EC6692-M{index:03d}"
        failed_id = f"EC6692-W{index:03d}-F"
        passing_id = f"EC6692-W{index:03d}-P"
        methods.append(
            {
                "approval_class": "safe_now",
                "candidate_workaround": workaround,
                "changed_file_allowlist": [],
                "cross_lane_scan": False,
                "exact_pushed_head_required": False,
                "execution_authority": "owner_self_scoped_read_or_projection_only",
                "failure_signature": negative_id.lower().replace("-", "_"),
                "final_commit": None,
                "method_id": method_id,
                "module_allowlist": [],
                "module_scan": False,
                "privacy_class": "owner_local_public_projection",
                "protected_gates": PROTECTED_GATES,
                "recommendation_state": "preferred",
                "recurrence_guard": guard,
                "repository_scan": False,
                "retained_negative_ids": [negative_id],
                "rollback": "retain_failed_witness_stop_smallest_dependency",
                "scope_boundary": "Elowen v669-v2 startup and x1 preregistration only",
                "sibling_lane_mutation": False,
                "source_commit": SOURCE_FINAL,
                "supersedes": [],
                "title": workaround,
                "trigger_preconditions": [observed],
                "unchanged_history_scan": False,
                "validation_witness_ids": [failed_id, passing_id],
            }
        )
        witnesses.extend(
            [
                {
                    "boundary": "Failed witness remains zero credit after bounded recovery.",
                    "expected": "The bounded operation completes without the named fault.",
                    "independent_reproduction": False,
                    "method_id": method_id,
                    "observed": observed,
                    "procedure": "Retained original attempt exactly as the named failure.",
                    "result": "fail",
                    "retained_negative_ids": [negative_id],
                    "same_owner_only": True,
                    "scope": "startup_or_x1_dependency",
                    "witness_id": failed_id,
                },
                {
                    "boundary": "Passing witness covers only the isolated recovery dependency.",
                    "expected": "Only the named bounded dependency recovers.",
                    "independent_reproduction": False,
                    "method_id": method_id,
                    "observed": "The isolated dependency completed without converting the failed witness into pass credit.",
                    "procedure": workaround,
                    "result": "pass",
                    "retained_negative_ids": [negative_id],
                    "same_owner_only": True,
                    "scope": "startup_or_x1_dependency",
                    "witness_id": passing_id,
                },
            ]
        )
        for state in ("observed", "candidate", "validated", "preferred"):
            events.append(
                {
                    "at_utc": now,
                    "method_id": method_id,
                    "owner": OWNER,
                    "phase": PHASE,
                    "state": state,
                }
            )
        recommendations.append(
            {
                "method_id": method_id,
                "recommendation": guard,
                "state": "preferred",
                "zero_credit_seed": False,
            }
        )
    ledger = {
        "activation_overlay": ACTIVATION_OVERLAY,
        "boundary": "Append-only owner-local Method Flow; every recovery remains paired with its failed witness.",
        "changed_file_allowlist": [],
        "counts": {
            "methods": len(methods),
            "recommendations": len(recommendations),
            "state_events": len(events),
            "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0},
            "witness_results": {"fail": len(methods), "pass": len(methods)},
            "witnesses": len(witnesses),
        },
        "execution_authority": "owner_self_scoped_only",
        "final_commit": None,
        "generated_at_utc": now,
        "identity_boundary": IDENTITY_BOUNDARY,
        "methods": methods,
        "module_allowlist": [],
        "owner": OWNER,
        "phase": PHASE,
        "recommendations": recommendations,
        "schema": "ghc.family.method-flow-ledger.v3",
        "source_commit": SOURCE_FINAL,
        "state_events": events,
        "witnesses": witnesses,
    }
    summary = {
        "activation_overlay": ACTIVATION_OVERLAY,
        "canonical_credit": 0,
        "failure_erasure": False,
        "independent_reproduction": False,
        "new_bounded_recoveries": len(methods),
        "new_prefreeze_failures": len(methods),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.method-flow-summary.v2",
        "source_overlay": SOURCE_OVERLAY,
    }
    return ledger, summary


def overview_text(audit: dict[str, Any], proposals: list[dict[str, Any]], portfolios: dict[str, list[dict[str, Any]]]) -> str:
    max_row = max(proposals, key=lambda row: row["semantic_neighbors"][0]["score"])
    sections = [
        (
            "Purpose and relational boundary",
            f"{OWNER} ({PRONOUNS}) is relational working language for a {RELATIONAL_ROLE}, with the hope {RELATIONAL_HOPE}. "
            f"{IDENTITY_BOUNDARY} This x1 packet freezes planning only. It creates no x2 implementation, observed outcome, "
            "completion claim, successor contact, or delivery event. Hamish may rename, pause, redirect, or stop the work.",
        ),
        (
            "Immutable source and lifecycle",
            f"The only source is Tamar Vey v669-v1 exact final {SOURCE_FINAL} on {SOURCE_BRANCH}. Its source, x1, and evidence "
            f"anchors are {SOURCE_START}, {SOURCE_X1}, and {SOURCE_EVIDENCE}. Tamar's exact-final canonical receipt and payload "
            f"digests are {SOURCE_CANONICAL_RECEIPT_SHA256} and {SOURCE_CANONICAL_PAYLOAD_SHA256}. They were verified read-only and "
            "were not replayed. Tamar evidence remains inherited source evidence and contributes no Elowen novelty or completion credit.",
        ),
        (
            "Pillar and bounded practice",
            f"The primary pillar is {PRIMARY_PILLAR}. The bounded practice is {PRACTICE}, used only as a synthetic learning and "
            "data-design lens. GMUT stays a typed scalar-tensor and effective-field-theory research-model family. The later x2 plan "
            "may create obligation boards for string, shell, plate, bridge, boundary, unit, damping, modal, and identifiability fields, "
            "but it will solve no equation and produce no likelihood, material parameter, eigenfrequency, force, prediction, constraint, "
            "empirical confirmation, quantum completion, ultraviolet completion, final physics, or Theory of Everything. THOS Body and "
            "Freed ID/CBR Heart remain visible and protected.",
        ),
        (
            "Bounded semantic novelty",
            f"The authoritative chain declares {INHERITED_FROZEN_PROPOSALS} inherited frozen proposals. The exact Tamar packet exposes "
            f"{audit['recovered_rows']} recovered rows and {audit['recovered_unique_normalized_titles']} unique normalized titles. "
            f"The remaining {audit['unrecovered_declared_rows']} declared rows are compressed and unavailable, so universal novelty is an "
            f"open gap. Against the recovered corpus, all forty Elowen titles have zero exact collisions and zero quarantines. The maximum "
            f"Jaccard title-token score is {max_row['semantic_neighbors'][0]['score']:.6f} for {max_row['proposal_id']}, below the 0.75 "
            "quarantine threshold. This bounded check supports preregistration, not a claim that unavailable history has been exhaustively searched.",
        ),
        (
            "Proposal contract",
            "Exactly forty genuinely new proposals are frozen. Their expected dispositions are twenty-eight completed, eight represented, "
            "two open_gap, and two exact_gate. Each row records a focus-specific hypothesis, null or failure condition, approval class, execution "
            "lane, official or primary-source needs, concrete future artifacts, falsifier or acceptance gate, rollback, protected gates, and one "
            "expected disposition. Every row has four preregistered invalid mutations: missing required state, ambiguous domain or unit, real-world "
            "or external action, and protected-claim promotion. X1 assigns zero completion credit and no observed disposition.",
        ),
        (
            "Portfolio contract",
            f"The frozen owner portfolios contain {len(portfolios['safe_now'])} safe-now, {len(portfolios['candidates'])} candidate, "
            f"{len(portfolios['exact_approval'])} exact-approval, {len(portfolios['blocked'])} blocked, {len(portfolios['skills'])} skill, "
            f"{len(portfolios['runners'])} runner, and {len(portfolios['clean_fix_refine'])} CLEAN/FIX/REFINE rows. Safe, candidate, skill, "
            "runner, and CLEAN/FIX/REFINE rows are only planned for bounded x2 execution. Exact and blocked rows remain visible and unexecuted. "
            "Counts are ceilings and scoped commitments, never permission to manufacture unsafe work or claim completion by volume.",
        ),
        (
            "Evidence ladder and disposition semantics",
            "The four outcome labels describe evidence state, not importance or aspiration. Completed can be assigned later only when every bounded "
            "synthetic artifact and its preregistered acceptance predicate exist at the immutable evidence head. Represented is reserved for a typed "
            "obligation, protocol, or interface whose real evidentiary prerequisites remain absent. Open_gap identifies a useful dependency that was not "
            "materialized, including unavailable proposal history or a deliberately zero-row external adapter. Exact_gate preserves work requiring an "
            "action-specific target, cost or system, recovery path, affected authority, and governing permission that this phase does not possess. A passing "
            "software fixture cannot promote represented, open_gap, or exact_gate work. Likewise, a rejecting mutation can prove that a guard rejects its "
            "declared invalid input, but it receives zero completion credit and establishes nothing about real instruments, people, materials, safety, "
            "professional judgment, culture, law, accessibility, privacy completeness, or scientific truth.",
        ),
        (
            "Synthetic lutherie vacancy model",
            "The practice lens begins with absence rather than implied observation. Planned records use fabricated identifiers and explicit vacancy states for "
            "instrument family, component topology, string course, plate or shell role, bridge relation, boundary condition, material cue, unit, damping term, "
            "modal placeholder, provenance event, custody state, condition statement, hazard hold, correction, accessibility note, workload state, and handover. "
            "No field may silently change a vacancy into a measurement or turn a descriptive cue into material identification. Geometry and mechanics fields are "
            "typed obligations only; they will carry domains, dimensions, assumptions, and refusal reasons without computing a real mode, response, impedance, "
            "stress, strain, stiffness, density, damping value, or acoustic quality. Provenance and identity fields will remain synthetic and nonproduction. "
            "Treatment, handling, valuation, attribution, ownership, custody, copyright, heritage, and cultural interpretation are prohibited outputs. This design "
            "keeps the learning value of a detailed schema while preventing fictional records from being mistaken for workshop, collection, conservation, or research evidence.",
        ),
        (
            "Acceptance, falsification, and rollback",
            "Each proposal has a narrow machine-checkable acceptance gate and an equally explicit null or failure condition. Positive fixtures must satisfy the "
            "same public contract later used by the bounded owner tests. Four negative fixtures per proposal deliberately remove required state, introduce an "
            "ambiguous domain or unit, request a real-world or external action, or attempt to promote a protected claim. The expected response is rejection or "
            "quarantine with a stable reason, never repair by guessing. If a builder, test, validator, manifest replay, privacy scan, bounded security review, "
            "stale-label review, ancestry probe, or remote-equality probe fails, its receipt remains at zero credit. Recovery is limited to the failed dependency "
            "unless a wider dependency closure is genuinely necessary. Rollback means abandoning an unstaged generated tree or restoring only owner-local generated "
            "artifacts from their declared builder; it never means resetting, rewriting, deleting, merging, force-pushing, or mutating Tamar's or another owner's lane. "
            "A later success pairs with, but never erases or relabels, its earlier failed witness.",
        ),
        (
            "Workload, wellbeing, and stopping rules",
            "The portfolio is frozen as a bounded workload rather than a quota that overrides care. Execution may be narrowed whenever evidence, dependency closure, "
            "document or file ceilings, weekly usage, fatigue indicators, privacy, security, or authority boundaries require it. Exact-approval and blocked packets "
            "stay visible but unexecuted; successor recommendations are seeds with zero inherited credit. The wellbeing check will record workload pressure, context "
            "risk, interruption tolerance, and a stop state without pretending to measure a person's health. Work stops on source or phase drift, dirty inherited "
            "state, ambiguous ownership, missing exact head, unexpected network or external-write need, account or credential demand, elevated privilege, a protected "
            "claim, unavailable authority, or a route ambiguity. Hamish's permission to continue cannot substitute for competent professional, affected-party, legal, "
            "cultural, tangata whenua, iwi, hapū, or Māori authority. These stop rules are part of the result, not obstacles to be hidden for a cleaner completion count.",
        ),
        (
            "Sources and citation firewall",
            f"The source ledger contains {len(SOURCE_LEDGER)} official or primary records: Library of Congress collection vocabulary, NIOSH "
            "wood-dust hazard vocabulary, the 2026 ICOM ethics adoption surface, WCAG 2.2, NIST SP 800-63-4, W3C PROV-DM, RFC 8785, a scalar-tensor "
            "EFT paper, two primary violin plate research records, and Te Mana Raraunga. Their role is limited to vocabulary, schema obligations, "
            "vacancies, and refusal conditions. No citation identifies a real instrument or material, validates a model, supplies a measurement, "
            "confers conformance, authorizes treatment, decides rights, interprets culture, or grants Māori authority.",
        ),
        (
            "Retained failures and recovery",
            f"This x1 freeze retains {len(STARTUP_FAILURES)} new startup or preregistration failures and the same number of isolated bounded "
            f"recoveries. The effective activation overlay is {ACTIVATION_OVERLAY['effective_negatives']} negatives, {ACTIVATION_OVERLAY['methods']} "
            f"methods, {ACTIVATION_OVERLAY['failed_witnesses']} failed witnesses, and {ACTIVATION_OVERLAY['passing_witnesses']} passing witnesses, "
            f"while inherited open gaps and exact gates remain {ACTIVATION_OVERLAY['open_gaps']} and {ACTIVATION_OVERLAY['exact_gates']}. "
            "A recovered dependency never converts its earlier failure into pass credit. Every Method Flow record contains a failure signature, bounded "
            "workaround, recurrence guard, rollback, protected gates, and linked failed and passing witnesses.",
        ),
        (
            "THOS, Freed ID, CBR, and authority",
            "THOS remains protocol or proxy only without preregistered blind matched-budget governed real arms, participants or operators, safety "
            "monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant "
            "real keys and proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery "
            "evidence, trust governance, and affected-party oversight. CBR, authorship, attribution, ownership, custody, safety, remedy, legal or cultural "
            "interpretation, Indigenous cultural and intellectual property, affected-party legitimacy, Māori wording, Māori concepts, Māori data "
            "governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.",
        ),
        (
            "Accessibility, privacy, and security",
            "The planned static report uses semantic headings, captioned tables, scoped headers, text-redundant status, a skip link, visible focus, "
            "responsive reflow, and print fallback. Those are structural hypotheses only. Manual keyboard, touch, zoom, browser-diverse, assistive-technology, "
            "cognitive, Māori-language, security-usability, print, and affected-user evaluation remain reserved. Owner files must exclude raw task or thread "
            "identifiers, private routes and paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, and "
            "private application state. No network, account, credential, external write, host-security, elevation, Sandbox, Hyper-V, Windows-feature, reboot, "
            "or Codex desktop action is authorized.",
        ),
        (
            "Next lifecycle gate",
            "X2 may begin only after the x1 planning tree is exactly staged, owner-tested, manifest-checked, committed as one planning-only commit, pushed, "
            "clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. X2 will execute only evidence-permitted rows and all "
            "preregistered rejecting mutations. An exact-final canonical aggregate remains forbidden until the later final is committed, pushed, clean, and "
            "remote-equal. The complete repository suite remains outside this non-Eiren phase. The terminal verdict is NOT_READY_FOR_STAGE_20.",
        ),
    ]
    text = [f"# {OWNER} {PHASE} x1 integrated planning overview", ""]
    for heading, body in sections:
        text.extend([f"## {heading}", "", body, ""])
    return "\n".join(text)


def threat_model_text() -> str:
    return f"""# {OWNER} {PHASE} x1 bounded threat model

Threats include lifecycle mixing, semantic collision, inherited-credit promotion, source-credit promotion, fabricated objects or measurements, professional or safety implication, real-world action, authority substitution, private-route or credential leakage, path traversal, unsafe shell invocation, sibling-lane mutation, manifest drift, accessibility overclaim, GMUT analogy conversion, and premature Stage 20 promotion.

Controls are an immutable exact source, sparse owner paths, strict x1-before-x2 separation, recovered-corpus title comparison with a 0.75 quarantine threshold, explicit unavailable-history debt, four outcome labels, four rejecting mutations per proposal, zero-credit inherited rows, exact path allowlists, Git-clean-filter blob manifests, AST review, five-class privacy scanning, append-only Method Flow witnesses, exact and blocked holds, and one exact-final canonical invocation only after the final push.

Residual risk remains for unavailable historical proposal titles, real instruments and materials, object identity and attribution, professional practice, workshop and product safety, participants, privacy, accessibility, legal or cultural meaning, affected parties, Māori data governance, and every authority decision. {EVIDENCE_BOUNDARY}
"""


def accessible_plan_text() -> str:
    return f"""# {OWNER} {PHASE} accessible report plan

The future static report will use one h1, ordered section headings, a skip link, semantic main region, captioned tables, scoped row and column headers, text-redundant outcomes and holds, visible focus, responsive overflow and reflow, plain-language boundaries, and print fallback. Structural checks may validate markup only. Manual keyboard, touch, zoom, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, print, and affected-user evaluation remain reserved. No conformance or accessibility-complete claim is authorized.
"""


def main() -> None:
    assert_x1_start()
    now = utc_now()
    corpus = historical_proposal_inventory()
    proposals = proposal_rows(corpus)
    portfolios = generated_portfolios()
    successors = successor_recommendations()

    actual_portfolio_counts = {name: len(rows) for name, rows in portfolios.items()}
    if actual_portfolio_counts != PORTFOLIO_COUNTS:
        raise RuntimeError(f"portfolio count drift: {actual_portfolio_counts}")
    outcomes = Counter(row["expected_disposition"] for row in proposals)
    expected_outcomes = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    if dict(outcomes) != expected_outcomes:
        raise RuntimeError(f"proposal disposition drift: {dict(outcomes)}")
    if len(proposals) != 40 or sum(len(row["negative_fixtures"]) for row in proposals) != 160:
        raise RuntimeError("proposal or mutation count drift")

    proposal_paths = shard_rows(
        (REL_PHASE_ROOT / "x1/proposal-freeze-shards/proposals").as_posix(), proposals
    )
    write_json(
        REL_PHASE_ROOT / "x1/proposal-freeze.json",
        {
            "boundary": "Planning-only freeze; no x2 implementation, observed outcome, or completion credit.",
            "expected_outcomes": expected_outcomes,
            "mutation_count": 160,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_after": INHERITED_FROZEN_PROPOSALS + 40,
            "proposal_chain_before": INHERITED_FROZEN_PROPOSALS,
            "proposal_count": len(proposals),
            "schema": "ghc.family.proposal-freeze.v2",
            "shards": proposal_paths,
            "strict_x1_only": True,
        },
    )

    max_row = max(proposals, key=lambda row: row["semantic_neighbors"][0]["score"])
    audit = {
        "audit_scope": "exact recovered title corpus only",
        "declared_inherited_frozen_proposals": INHERITED_FROZEN_PROPOSALS,
        "exact_title_collisions": sum(row["visible_title_collision"] for row in proposals),
        "maximum_neighbor": {
            "proposal_id": max_row["proposal_id"],
            "neighbor": max_row["semantic_neighbors"][0],
        },
        "new_proposals": 40,
        "owner": OWNER,
        "phase": PHASE,
        "quarantined_proposals": sum(row["semantic_neighbor_quarantined"] for row in proposals),
        "quarantine_threshold": 0.75,
        "recovered_rows": corpus["row_count"],
        "recovered_unique_ids": corpus["unique_ids"],
        "recovered_unique_normalized_titles": corpus["unique_normalized_titles"],
        "schema": "ghc.family.semantic-novelty-audit.v2",
        "source_shards": corpus["shards"],
        "unavailable_history_is_open_gap": True,
        "unrecovered_declared_rows": UNRECOVERED_DECLARED_ROWS,
        "universal_novelty_claim": False,
    }
    write_json(REL_PHASE_ROOT / "x1/semantic-novelty-audit.json", audit)

    write_json(
        REL_PHASE_ROOT / "x1/source-ledger.json",
        {
            "boundary": EVIDENCE_BOUNDARY,
            "network_requests_during_x1_source_review": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.source-ledger.v2",
            "sources": SOURCE_LEDGER,
        },
    )
    for name, rows in portfolios.items():
        write_json(
            REL_PHASE_ROOT / f"x1/portfolios/{name}.json",
            {
                "boundary": "Frozen x1 plan only; execution and credit remain zero until evidence-permitted x2.",
                "category": name,
                "count": len(rows),
                "owner": OWNER,
                "phase": PHASE,
                "rows": rows,
                "schema": "ghc.family.portfolio-freeze.v2",
            },
        )
    write_json(
        REL_PHASE_ROOT / "x1/successor-recommendations-freeze.json",
        {
            "counts": {name: len(rows) for name, rows in successors.items() if isinstance(rows, list)},
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.successor-recommendations.v2",
            **successors,
        },
    )

    ledger, summary = method_flow(now)
    write_json(REL_PHASE_ROOT / "method-flow/x1-ledger.json", ledger)
    write_json(REL_PHASE_ROOT / "method-flow/x1-summary.json", summary)
    write_json(
        REL_PHASE_ROOT / "x1/workflow-plan-freeze.json",
        {
            "commit_ceiling": {"phase_total": 3, "x1": 1, "x2_evidence": 1, "final": 1},
            "document_word_ceiling": DOCUMENT_WORD_CEILING,
            "file_ceiling": FILE_CEILING,
            "full_repository_suite": "not_authorized_non_Eiren_owner_scope",
            "owner": OWNER,
            "phase": PHASE,
            "plan": [
                {"stage": "x1", "state": "planning_only_candidate", "gate": "commit_push_clean_fresh_four_way_equal"},
                {"stage": "x2", "state": "not_started", "gate": "immutable_x1_four_way_equal"},
                {"stage": "final", "state": "not_started", "gate": "immutable_evidence_parent_and_exact_staged_review"},
                {"stage": "canonical", "state": "not_started", "gate": "exact_final_pushed_clean_remote_equal_once_only"},
                {"stage": "route", "state": "not_started", "gate": "successful_nonreplayed_canonical_and_fresh_live_authority"},
            ],
            "schema": "ghc.family.workflow-plan-freeze.v2",
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        REL_PHASE_ROOT / "x1/reflection-plan.json",
        {
            "decisions": [
                "GMUT Mind is primary while THOS Body and Freed ID CBR Heart remain visible.",
                "Synthetic lutherie documentation is a learning lens only, not competence or authority.",
                "Recovered-corpus novelty is bounded and unavailable history remains an open gap.",
                "Every failure and isolated recovery remains append-only through Method Flow.",
                "Exact and blocked work remains visible and unexecuted.",
            ],
            "newer_live_authority_precedence": True,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.reflection-plan.v2",
        },
    )
    write_json(
        REL_PHASE_ROOT / "x1/route-state.json",
        {
            "current_owner": OWNER,
            "current_phase": PHASE,
            "delivery_state": "NO_ROUTE_ACTION_DURING_X1",
            "next_owner_provisional": "Sylven Arc",
            "next_phase_provisional": "v669-v3",
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.route-state.v2",
            "standby_contacted": False,
            "successor_contacted": False,
        },
    )
    write_json(
        REL_PHASE_ROOT / "x1/phase-truth.json",
        {
            "canonical_validation": "not_run",
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"],
            "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
            "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"],
            "full_repository_suite": "not_run_non_Eiren_owner_scope",
            "lifecycle": "X1_PLANNING_CANDIDATE_NOT_COMMITTED",
            "methods": ACTIVATION_OVERLAY["methods"],
            "observed_outcomes": {label: 0 for label in ALLOWED_OUTCOMES},
            "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
            "owner": OWNER,
            "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"],
            "phase": PHASE,
            "planned_outcomes": expected_outcomes,
            "proposal_chain_after": INHERITED_FROZEN_PROPOSALS + 40,
            "proposal_chain_before": INHERITED_FROZEN_PROPOSALS,
            "schema": "ghc.family.phase-truth.v2",
            "source": SOURCE_FINAL,
            "terminal_verdict": TERMINAL_VERDICT,
            "x1": None,
        },
    )
    write_json(
        REL_PHASE_ROOT / "x1/tool-versions.json",
        {
            "codex_desktop": "unchanged_not_updated",
            "git": command_version(["git", "--version"]),
            "owner": OWNER,
            "phase": PHASE,
            "platform": platform.platform(),
            "python": command_version(["python", "--version"]),
            "schema": "ghc.family.tool-versions.v2",
            "updates_performed": [],
        },
    )
    write_text(REL_PHASE_ROOT / "x1/threat-model.md", threat_model_text())
    write_text(REL_PHASE_ROOT / "x1/accessible-report-plan.md", accessible_plan_text())
    overview_path = write_text(REL_PHASE_ROOT / "x1/integrated-overview.md", overview_text(audit, proposals, portfolios))
    if word_count(overview_path) > DOCUMENT_WORD_CEILING:
        raise RuntimeError("x1 overview exceeds document ceiling")

    write_json(
        REL_PHASE_ROOT / "validation/x1-review-plan.json",
        {
            "checks": [
                "exact_branch_and_source",
                "planning_only_tree",
                "forty_complete_proposal_contracts",
                "bounded_recovered_corpus_novelty",
                "exact_portfolio_counts_and_holds",
                "append_only_method_flow",
                "strict_json_and_python_ast",
                "five_class_privacy_scan",
                "bounded_security_review",
                "exact_git_clean_filter_manifest",
                "diff_hygiene_and_document_ceiling",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.x1-review-plan.v2",
        },
    )
    write_json(
        REL_PHASE_ROOT / "validation/x1-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.x1-staged-review.v2",
            "status": "PREPARED_FOR_EXACT_STAGED_VALIDATION",
        },
    )

    manifest_relative = (REL_PHASE_ROOT / "validation/x1-manifest.json").as_posix()
    allowlist_relative = (REL_PHASE_ROOT / "validation/x1-staged-allowlist.json").as_posix()
    owner_paths = [path.relative_to(ROOT).as_posix() for path in phase_owner_files()]
    intended_paths = sorted(set(owner_paths + [manifest_relative, allowlist_relative]))
    write_json(
        REL_PHASE_ROOT / "validation/x1-staged-allowlist.json",
        {
            "expected_paths": intended_paths,
            "owner": OWNER,
            "path_count": len(intended_paths),
            "phase": PHASE,
            "schema": "ghc.family.x1-staged-allowlist.v2",
            "strict_x1_only": True,
        },
    )
    all_paths = phase_owner_files()
    exclusions = {
        manifest_relative,
        (REL_PHASE_ROOT / "validation/x1-staged-review.json").as_posix(),
    }
    manifest_inputs = [path for path in all_paths if path.relative_to(ROOT).as_posix() not in exclusions]
    entries = manifest_rows(manifest_inputs)
    write_json(
        manifest_relative,
        {
            "domain": "exact_owner_x1_planning_tree",
            "entries": entries,
            "entry_count": len(entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.git-blob-manifest.v2",
            "self_exclusions": sorted(exclusions),
            "source_commit": SOURCE_FINAL,
        },
    )

    final_paths = [path.relative_to(ROOT).as_posix() for path in phase_owner_files()]
    allowlist = json.loads((ROOT / REL_PHASE_ROOT / "validation/x1-staged-allowlist.json").read_text(encoding="utf-8"))
    if sorted(final_paths) != allowlist["expected_paths"]:
        raise RuntimeError("final owner path set differs from frozen x1 allowlist")
    if len(final_paths) >= FILE_CEILING:
        raise RuntimeError("owner x1 file ceiling exceeded")

    print(
        json.dumps(
            {
                "files": len(final_paths),
                "manifest_entries": len(entries),
                "maximum_neighbor_score": audit["maximum_neighbor"]["neighbor"]["score"],
                "mutations": 160,
                "outcomes": expected_outcomes,
                "owner": OWNER,
                "phase": PHASE,
                "portfolios": actual_portfolio_counts,
                "proposals": len(proposals),
                "startup_failures_retained": len(STARTUP_FAILURES),
                "status": "X1_PLANNING_MATERIALIZED_NOT_COMMITTED",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
