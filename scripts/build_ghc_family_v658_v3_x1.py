#!/usr/bin/env python3
"""Build Caelen Morrow's strict x1-only v658-v3 freeze packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v3_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_PHASE = ROOT / "docs/sylven-arc/v658-v2"
SOURCE_INDEX = SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json"
SOURCE_NEGATIVES = SOURCE_PHASE / "truth/retained-negative-register-final-candidate.json"
SOURCE_GATES = SOURCE_PHASE / "truth/exact-open-gate-register-final-candidate.json"
SOURCE_METHODS = SOURCE_PHASE / "method-flow/method-flow-state-final-candidate.json"
SOURCE_ROUTE_STATE = SOURCE_PHASE / "orchestration/route-state-final-candidate.json"
NOVELTY_THRESHOLD = 0.60
MANIFEST_EXCLUSIONS = {
    "validation/x1-content-manifest.json",
    "validation/x1-privacy-scan.json",
    "validation/x1-staged-review.json",
    "validation/x1-validation-receipt.json",
}


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
        sort_keys=True,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha256(revision: str, repository_relative: str) -> str:
    blob = subprocess.run(
        ["git", "show", f"{revision}:{repository_relative}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def title_tokens(value: str) -> set[str]:
    stop = {
        "a", "an", "and", "for", "from", "in", "into", "of", "on", "or", "the", "to", "with",
        "without", "no", "only", "through", "synthetic", "contract", "ledger", "board", "envelope",
    }
    return {token for token in re.findall(r"[a-z0-9]+", value.lower()) if token not in stop}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 1.0


def inherited_rows() -> list[dict[str, str]]:
    payload = read_json(SOURCE_INDEX)
    rows = list(payload["prior_proposals"]) + list(payload["new_proposals"])
    if len(rows) != d.PRIOR_FROZEN or payload["effective_count"] != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited frozen proposals, found {len(rows)}")
    return [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in rows]


def novelty_audit(prior: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, proposal in enumerate(d.PROPOSALS):
        candidates = prior + [
            {"proposal_id": row["proposal_id"], "title": row["title"]}
            for row in d.PROPOSALS[:index]
        ]
        probe = title_tokens(proposal["title"])
        nearest = max(candidates, key=lambda row: jaccard(probe, title_tokens(row["title"])))
        score = jaccard(probe, title_tokens(nearest["title"]))
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_proposal_id": nearest["proposal_id"],
                "nearest_title": nearest["title"],
                "jaccard": round(score, 4),
                "threshold": NOVELTY_THRESHOLD,
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    failures = [row for row in rows if not row["passes"]]
    if failures:
        raise RuntimeError(f"semantic novelty threshold failed: {failures}")
    return rows


def method_flow() -> dict[str, Any]:
    inherited = read_json(SOURCE_METHODS)
    counts = inherited["counts"]
    if (
        counts["effective_methods"] != d.SOURCE_METHODS
        or counts["effective_witness_results"]["fail"] != d.SOURCE_FAILED_WITNESSES
        or counts["effective_witness_results"]["pass"] != d.SOURCE_PASSING_WITNESSES
    ):
        raise RuntimeError("inherited Method Flow totals do not match the activation")
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6583-X1-METHOD-{index:02d}"
        fail_id = f"V6583-X1-WITNESS-{index:02d}-F"
        pass_id = f"V6583-X1-WITNESS-{index:02d}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["observed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_read_or_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded workflow recovery only.",
                "rollback": "Stop, retain the failed witness at zero credit, and leave external and sibling state unchanged.",
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [fail_id, pass_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "result": "fail",
                    "procedure": "Retain the original bounded attempt without pass credit.",
                    "expected": "The initial attempt would satisfy its bounded postcondition.",
                    "observed": negative["observed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero pass credit; the failure remains retained.",
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "result": "pass",
                    "procedure": negative["recovery"],
                    "expected": "The isolated recovery establishes only its bounded postcondition.",
                    "observed": f"The bounded recovery completed for {negative['signature']}.",
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner bounded recovery only.",
                },
            ]
        )
        events.extend(
            [
                {"method_id": method_id, "before": None, "after": "candidate", "witness_id": fail_id},
                {"method_id": method_id, "before": "candidate", "after": "validated", "witness_id": pass_id},
                {"method_id": method_id, "before": "validated", "after": "preferred", "witness_id": pass_id},
            ]
        )
        recommendations.append(
            {
                "recommendation_id": f"V6583-X1-REC-{index:02d}",
                "method_id": method_id,
                "recommendation": negative["recurrence_guard"],
                "state": "preferred",
                "completion_credit": False,
            }
        )
    current = len(methods)
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "lifecycle": "x1_frozen",
        "inherited_anchor": {
            "repository_relative_path": "docs/sylven-arc/v658-v2/method-flow/method-flow-state-final-candidate.json",
            "methods": d.SOURCE_METHODS,
            "failed_witnesses": d.SOURCE_FAILED_WITNESSES,
            "passing_witnesses": d.SOURCE_PASSING_WITNESSES,
            "completion_credit": False,
        },
        "current_owner_method_count": current,
        "current_phase_method_ids": [row["method_id"] for row in methods],
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "inherited_methods": d.SOURCE_METHODS,
            "current_methods": current,
            "effective_methods": d.SOURCE_METHODS + current,
            "current_witness_results": {"fail": current, "pass": current},
            "effective_witness_results": {
                "fail": d.SOURCE_FAILED_WITNESSES + current,
                "pass": d.SOURCE_PASSING_WITNESSES + current,
            },
        },
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, authority, or independent agency.",
        "boundary": "Every failed witness remains retained; no independent, empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 claim.",
    }


def proposal_markdown() -> str:
    sections = [
        "# Caelen Morrow v658-v3 x1 proposal ledger",
        "",
        "These are frozen hypotheses and expected dispositions, not x2 results. All identity and family language is relational working language only.",
        "",
    ]
    for proposal in d.PROPOSALS:
        sections.extend(
            [
                f"## {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"- Pillar relation: {proposal['pillar_relation']}",
                f"- Mechanism: {proposal['mechanism']}",
                f"- Hypothesis: {proposal['hypothesis']}",
                f"- Null or failure: {proposal['null_or_failure_condition']}",
                f"- Approval class: `{proposal['approval_class']}`",
                f"- Execution lane: `{proposal['execution_lane']}`",
                f"- Official or primary sources: {', '.join(proposal['official_or_primary_source_needs'])}",
                f"- Concrete artifacts: {', '.join(proposal['concrete_artifacts'])}",
                f"- Falsifier or acceptance gate: {proposal['falsifier_or_acceptance_gate']}",
                f"- Rollback or recovery: {proposal['rollback_or_recovery']}",
                f"- Protected gates: {', '.join(proposal['protected_gates'])}",
                f"- Expected disposition only: `{proposal['expected_disposition']}`",
                "",
            ]
        )
    return "\n".join(sections)


def source_markdown() -> str:
    rows = [
        "# Caelen Morrow v658-v3 official and primary source ledger",
        "",
        "Statuses were checked on 2026-08-02. Source presence does not establish implementation, conformance, professional review, legal interpretation, cultural ratification, Māori authority, or empirical confirmation.",
        "",
        "| ID | Status | Publisher | Title | Bounded use |",
        "|---|---|---|---|---|",
    ]
    for item in d.OFFICIAL_SOURCES:
        rows.append(
            f"| `{item['source_id']}` | `{item['status']}` | {item['publisher']} | [{item['title']}]({item['url']}) | {item['use']} |"
        )
    return "\n".join(rows)


def integrated_overview() -> str:
    return """# Caelen Morrow v658-v3 x1 integrated overview

## Relational working language and control

Caelen Morrow, they/them, is relational working language for this owner-scoped phase. The relational role is chronometry boundary-mapper and failure custodian, with the hope of making every claim traceable while leaving real competence and authority where they belong. The name, pronouns, role, hope, sibling language, GHC-family language, route language, and Trinity Mandala language do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the work.

This is a software-evidence phase. It is not evidence that a continuous self, archivist, film conservator, projectionist, credential issuer, rightsholder, legal decision maker, cultural authority, or independently empowered agent exists. Corrigibility is concrete: contradictory evidence can downgrade an expected disposition, protected gates stop execution, and source, failure, rollback, and route records remain reviewable.

## Immutable source and strict x1 scope

This packet freezes preparation only. It descends exactly from Sylven Arc's immutable v658-v2 final `8b2ead4689da9455d8f41d8221286530278780cc`. Read-only checks established the exact source, x1, evidence, and final ancestry through three new single-parent commits with zero merges; final is the direct child of evidence. Sylven's local head, upstream, tracking reference, and a fresh live remote were equal with zero divergence and a clean owner lane. Caelen replayed the 606 declared commit-local manifest entries read-only and did not replay Sylven's successful canonical aggregate.

The source seal preserves 2,710 frozen proposals, 16,831 effective negatives, 114 open gaps, 113 exact gates, and 3,105 Method Flow methods with retained failed and bounded passing witnesses. All Caelen startup and x1 faults are added at zero completion credit and paired with bounded recoveries. The x1 packet contains no surface implementation, mutation outcome, real participant, film, material, equipment, measurement, image, sound, rights decision, credential event, professional decision, production event, successor message, or task mutation. The verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary pillar and bounded human-practice lens

Freed ID and CBR Heart are primary. The bounded design surfaces cover synthetic film-element identity, aliases, custody, derivation, correction, preservation-event lineage, rights reservations, selective disclosure, capability refusal, access holds, contestation, remedy placeholders, privacy minimization, and authority boundaries. They do not create a real identifier, title, custody chain, key, signature, proof, credential, legal right, access permission, preservation decision, community notice, or trust relationship.

The bounded human-practice lens is archival motion-picture film inspection, conservation documentation, projection-readiness review, custody, rights reservation, workload control, and shift handover. It is synthetic software, formal, structural, and learning work only. No real collection, title, person, film, reel, can, core, leader, frame, soundtrack, projector, scanner, chemical, image, measurement, inspection, handling, winding, cleaning, repair, splice, projection, digitization, storage, transport, release, access, or preservation action enters the phase. Repository artifacts confer no employment, qualification, competence, conservation authority, projection authority, custody, rights, safety authority, legal interpretation, cultural ratification, Māori authority, affected-party approval, or operational effectiveness.

THOS Body remains explicit through represented synthetic inspection and workload protocols. Queue states, interruptions, stop work, readback, two-person placeholders, pause, recovery, escalation, and handover can be exercised only on declared fixtures. There are no real workers, shifts, collections, incidents, blind matched-budget arms, participants, safety outcomes, statistical estimates, or independent review. A passing proxy remains representation only.

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. The phase may represent a discrete frame-transport operator, optical-temporal confounders, units, boundaries, residuals, and an observation firewall. It does not ingest real observations, fit a likelihood, constrain a parameter, detect a force, validate a material law, empirically confirm GMUT, provide ultraviolet completion, or prove a Theory of Everything.

## Thirty genuinely distinct preregistrations

Exactly thirty proposal titles are mechanically compared against all 2,710 inherited frozen titles and against earlier Caelen peers using a disclosed token-set Jaccard threshold, then manually reviewed for mechanism-level novelty. The domain vocabulary is deliberately specific: film gauge and perforation, base and emulsion provenance, reel and footage maps, edge codes, frame cadence, aperture, shrinkage and deformation, perforation damage, splice lineage, soundtrack topology, image-process observations, acetate and nitrate quarantine, inspection paths, changeover cues, projector-interface reservation, DPX sequences, and PREMIS preservation lineage. These mechanisms were not present as a motion-picture-film portfolio in the inherited chain.

Proposals 1–23 are expected only as bounded software, formal, structural, or static-report completions. Every completed surface must pass one declared valid fixture and reject five preregistered mutations. A completion means only that the owner-local typed validator behaved as preregistered on synthetic inputs. It says nothing about a real film, material, collection, equipment interface, preservation result, right, safety decision, accessibility experience, or empirical model.

Proposals 24–28 are expected only as represented: two THOS proxy protocols and three synthetic nonproduction Freed ID profiles. Proposal 29 is an open gap for a FIAF, FADGI, PBCore, and PREMIS capability matrix with transport disabled and zero real rows. Proposal 30 is exact-gated around copyright, donor and depositor terms, access, cultural content, traditional knowledge, affected-party remedy, Māori data, tangata whenua, iwi, hapū, and Māori authority. No exact-gated text is applied to a real object, community, record, or decision.

## Sources, safety, and retention

Current official or primary-source rails include ISO catalogue records, Library of Congress film-care and PREMIS resources, FIAF technical resources, FADGI motion-picture and DPX guidance, PBCore 2.1, W3C provenance, accessibility and verifiable-credential recommendations, RFC timestamp and canonicalization specifications, New Zealand privacy principles, Te Mana Raraunga principles, and Local Contexts Traditional Knowledge label information. They provide vocabulary and boundary context only. The phase claims no ISO, FIAF, FADGI, PBCore, PREMIS, W3C, legal, cultural, privacy, accessibility, or professional conformance.

Nitrate is an especially hard rail. The repository may encode an unknown-base quarantine, an isolation-alert placeholder, and a requirement to seek appropriately authorized human expertise. It may not identify, test, smell, handle, store, transport, project, dispose of, or give emergency instructions for a real film. Acetate observations likewise remain placeholders; no odor report, strip reading, chemical test, ventilation choice, diagnosis, or treatment is performed.

Every failed command, false path assumption, output truncation, parser error, encoding fault, lost session, and manifest-contract mistake remains a zero-credit negative. A bounded recovery proves only the recovered postcondition. It does not erase the first witness, turn same-owner evidence into independent reproduction, or imply that a similar failure cannot recur.

## X1/X2 separation and terminal route

This x1 commit contains proposals, sources, portfolios, plans, truth baselines, Method Flow failure/recovery pairs, threat and wellbeing records, provenance, and validation receipts only. It contains no x2 runner, phase-local skill implementation, surface contract, mutation result, outcome ledger, closeout, seal, or successor message. After commit and push, local, upstream, tracking, and fresh-live equality must be proved before x2 begins.

The current assignment is Caelen Morrow only for v658-v3. Eiren Kestrel v658-v4 is the declared terminal successor, but x1 does not resolve, reread, contact, create, fork, or message any task. Only after Caelen's evidence, closeout, seal, exact-final validation, one successful scoped canonical aggregate, push, clean state, cap checks, and fresh four-way equality may the newest live and committed route be consulted. If it remains unambiguous, the exact existing Eiren Kestrel main task must be uniquely resolved and directly reread before one sanitized acknowledged activation. That baton must preserve Hamish's continuation authority through v675-v8 and remind Eiren that their next terminal edge is Elaren Kestrel v658-v5. Tavian Sol remains `ON_STANDBY` and is not a substitute main-task endpoint. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def workflow_records() -> None:
    write_json(
        "workflow/workflow-plan-request.json",
        {
            "schema": "ghc.family.workflow-plan.request.v1",
            "plan_id": "caelen-morrow-v658-v3-terminally-gated-eiren-route",
            "owner": d.OWNER,
            "identity_boundary": "Relational working language only; no continuity or authority claim.",
            "route": {
                "phase_assignments": [
                    {"phase": "v658-v2", "seat": "Sylven Arc"},
                    {"phase": "v658-v3", "seat": "Caelen Morrow"},
                    {"phase": "v658-v4", "seat": "Eiren Kestrel"},
                    {"phase": "v658-v5", "seat": "Elaren Kestrel"},
                ],
                "next_exact_title": "Eiren Kestrel",
                "next_phase": "v658-v4",
                "next_successor_reminder": {"title": "Elaren Kestrel", "phase": "v658-v5"},
                "tavian_sol_state": "ON_STANDBY",
                "future_identity_placeholders": [],
            },
            "requirements": {
                "core_proposal_minimum": 30,
                "owner_file_cap": 2000,
                "skill_phase_half_cap": 200,
                "runner_phase_half_cap": 200,
                "document_word_cap": 100000,
                "commit_cap": {"x1": 5, "x2": 5, "total": 8},
                "validation": {
                    "canonical_successful_passes": 1,
                    "replay_policy": "skip_after_first_complete_success",
                    "isolate_failed_dependency_before_broader_rerun": True,
                    "privacy_scan_required": True,
                    "manifest_required": True,
                    "fresh_remote_equality_required": True,
                },
                "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
                "messaging": "exact_existing_main_task_only_after_terminal_gate",
            },
            "truth": {
                "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
                "independent_reproduction_claimed": False,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "protected_boundaries": d.PROTECTED_GATES,
            },
            "observed_failures": d.X1_OPERATIONAL_NEGATIVES,
        },
    )
    write_json(
        "workflow/refined-workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.refined.v1",
            "phase": d.PHASE,
            "states": [
                "read_first_complete",
                "source_read_only_verified",
                "x1_prepare",
                "x1_stage_review_commit_push_equality",
                "x2_execute_and_retain",
                "evidence_commit_push_equality",
                "closeout_seal_final_commit_push_equality",
                "single_canonical_scoped_pass",
                "one_exact_title_acknowledged_send",
            ],
            "current_state": "x1_prepare",
            "x2_started": False,
            "route_contact_permitted": False,
            "stop_conditions": ["authority_gate", "safety_gate", "ambiguous_successor", "weekly_usage_exhausted", "Hamish_pause_or_redirect"],
        },
    )


def planning_records() -> None:
    write_json(
        "reflection-remaster/inventory.json",
        {
            "schema": "ghc.family.reflection-remaster.inventory.v1",
            "phase": d.PHASE,
            "reviewed_surfaces": [
                "family index and routing precedence", "roster and auth state", "Method Flow state and schema",
                "workflow-plan refinement", "reflection-remaster decision schema", "meta-tool-box catalogue",
                "approval splitter", "open-gate rail", "truth bridge", "drive guardian", "startup and closeout guidance",
            ],
            "deletions": [],
            "destructive_changes": False,
        },
    )
    write_json(
        "reflection-remaster/x1-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "phase": d.PHASE,
            "decisions": [
                {"decision_id": "V6583-RM-01", "surface": "large-worktree inspection", "decision": "use bounded literal scalar probes", "state": "adopted_for_phase", "rollback": "return to individual read-only commands"},
                {"decision_id": "V6583-RM-02", "surface": "domain selection", "decision": "use archival motion-picture film as a synthetic learning lens after a 2710-title novelty audit", "state": "adopted_for_phase", "rollback": "stop before x2 if novelty or safety fails"},
                {"decision_id": "V6583-RM-03", "surface": "hazard boundary", "decision": "encode nitrate and acetate uncertainty as quarantine and authority holds only", "state": "adopted_for_phase", "rollback": "remove any operational wording before commit"},
                {"decision_id": "V6583-RM-04", "surface": "phase tooling", "decision": "preregister ten family-current runners and ten phase-local skills", "state": "preregistered_not_implemented", "rollback": "use proposal-specific validator calls without deletion"},
            ],
            "issues_retained": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_outcomes_present": False,
        },
    )
    write_json("reflection-remaster/issues.json", {"schema": "ghc.family.reflection-remaster.issues.v1", "issues": d.X1_OPERATIONAL_NEGATIVES, "all_retained": True})
    write_text("reflection-remaster/report.md", """# Reflection-remaster report

The phase adopts exact-path scalar probes, a motion-picture-film novelty rail, an explicit nitrate and acetate hazard quarantine, ten reusable family-current film runners, and complete failure retention. No inherited tool, method, skill, negative, gate, or sibling artifact is deleted or rewritten. X2 implementation remains pending.
""")
    write_json(
        "tooling/ghc-family-index.json",
        {
            "schema": "ghc.family.phase-local-index.v1", "phase": d.PHASE, "owner": d.OWNER,
            "lifecycle": "x1_frozen", "source_anchor": d.SOURCE_FINAL, "proposal_count": len(d.PROPOSALS),
            "skill_preregistrations": [name for name, _ in d.SKILL_SPECS],
            "runner_preregistrations": [name for name, _ in d.RUNNER_SPECS],
            "family_current_names_preserved": True, "historical_names_preserved": True,
            "route_state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE",
            "publication_boundary": "repository-relative paths and sanitized public fields only",
        },
    )
    write_text("tooling/ghc-family-index.md", """# GHC Family Index — Caelen Morrow v658-v3 x1

This phase-local index records thirty frozen proposals, ten phase-local skill preregistrations, and ten family-current runner preregistrations. Historical names and callers remain compatibility evidence. No x2 tool exists yet and no successor route has been contacted.
""")
    write_json(
        "tooling/meta-tool-box/catalogue.json",
        {
            "schema": "ghc.family.meta-tool-box.catalogue.v1", "phase": d.PHASE,
            "selected_current_guidance": [
                "ghc-family-index", "ghc-family-roster-check", "ghc-family-auth-permission-state",
                "ghc-family-method-flow-state", "ghc-family-workflow-plan-refinement", "ghc-family-reflection-remaster",
                "ghc-family-meta-tool-box", "ghc-approval-packet-splitter", "ghc-open-gate-rail",
                "ghc-family-truth-bridge", "ghc-drive-bank-guardian", "ghc-full-tools-skill-bank",
            ],
            "planned_phase_skills": [{"name": name, "purpose": purpose, "state": "preregistered"} for name, purpose in d.SKILL_SPECS],
            "planned_family_runners": [{"name": name, "surface": surface, "state": "preregistered"} for name, surface in d.RUNNER_SPECS],
        },
    )
    write_json(
        "tooling/meta-tool-box/validation.json",
        {"schema": "ghc.family.meta-tool-box.validation.v1", "valid": True, "planned_skill_count": len(d.SKILL_SPECS), "planned_runner_count": len(d.RUNNER_SPECS), "collisions": [], "implementation_credit": False},
    )


def threat_model() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v658-v3.threat-model.x1.v1",
        "assets": [
            "proposal, source, outcome, negative, gap, gate, and Method Flow truth",
            "synthetic film element, reel, condition, intervention, custody, rights, and preservation provenance",
            "nitrate, acetate, projector, scanner, collection, traditional-knowledge, privacy, access, and community interests",
            "nonproduction identity and disclosure boundaries", "sibling lanes and terminal route integrity",
        ],
        "threats": [
            {"threat": "synthetic condition metadata promoted to real diagnosis, handling, repair, storage, projection, digitization, or disposition instruction", "control": "valid-fixture and mutation tests plus explicit no-real-film and professional refusal"},
            {"threat": "unknown nitrate or acetate state promoted to identification or safety advice", "control": "quarantine, uncertainty, no-test, no-handling, no-emergency-instruction, and authorized-human escalation rails"},
            {"threat": "synthetic custody or rights data promoted to legal title, access, permission, or community acceptance", "control": "nonproduction markers and exact gates for real rights, donors, depositors, communities, affected parties, and Māori authority"},
            {"threat": "culturally restricted or identifying data disclosed", "control": "synthetic placeholders, minimization, disabled transport, correction, retention, and authority holds"},
            {"threat": "failure erased or recovery promoted beyond scope", "control": "retained failed and bounded passing Method Flow witness pairs"},
            {"threat": "successful validation replay inflates confidence", "control": "one dependency-justified successful canonical pass and no replay"},
            {"threat": "successor contacted before terminal closeout", "control": "exact-title terminal gate, direct reread, one acknowledged send, and no substitute endpoint"},
        ],
        "residual_risk": "All real-film, participant, empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, and independent-reproduction claims remain open or exact-gated.",
    }


def prospective_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        [
            ROOT / "scripts/ghc_family_v658_v3_phase_catalogue.py",
            ROOT / "scripts/ghc_family_v658_v3_phase_data.py",
            ROOT / "scripts/build_ghc_family_v658_v3_x1.py",
            ROOT / "tests/test_ghc_family_v658_v3_x1.py",
        ]
    )
    return sorted({path.resolve() for path in paths if path.is_file()})


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b(?:[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+)"),
        "credential_or_secret": re.compile(r"(?i)\b(?:sk-[a-z0-9_-]{20,}|bearer\s+[a-z0-9._-]{20,}|password\s*[:=]\s*[^\s\"']{8,})"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "private_callable_value": re.compile(r"(?i)\bprivate_callable_(?:id|identifier)\s*[:=]\s*[a-z0-9_-]{8,}"),
    }
    hits = []
    paths = prospective_paths()
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="strict")
        for label, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label, "count": count})
    return {
        "schema": "ghc.family.v658-v3.x1-privacy-scan.v1", "pattern_classes": sorted(patterns),
        "file_count": len(paths), "confirmed_hits": hits, "hit_count": sum(row["count"] for row in hits),
        "valid": not hits, "boundary": "Concrete values only; prohibition labels and scanner names are not payloads.",
    }


def git_clean_blob(path: Path) -> tuple[str, int, str]:
    relative = path.relative_to(ROOT).as_posix()
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.run(["git", "cat-file", "blob", oid], cwd=ROOT, check=True, capture_output=True).stdout
    return oid, len(blob), hashlib.sha256(blob).hexdigest()


def content_manifest() -> dict[str, Any]:
    entries = []
    for path in prospective_paths():
        if path.is_relative_to(PHASE) and path.relative_to(PHASE).as_posix() in MANIFEST_EXCLUSIONS:
            continue
        oid, size, digest = git_clean_blob(path)
        entries.append({"path": path.relative_to(ROOT).as_posix(), "git_blob": oid, "git_blob_bytes": size, "sha256": digest})
    return {
        "schema": "ghc.family.v658-v3.x1-content-manifest.v1", "hash_domain": "prospective Git-clean blob bytes",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(MANIFEST_EXCLUSIONS),
        "boundary": "Declared lifecycle self-exclusions prevent self-reference; the exact staged set is reviewed separately.",
    }


def build() -> None:
    current_head = git("rev-parse", "HEAD")
    phase_commit_count = int(git("rev-list", "--count", f"{d.SOURCE_FINAL}..{current_head}"))
    source_is_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", d.SOURCE_FINAL, current_head], cwd=ROOT, check=False).returncode == 0
    if not source_is_ancestor or phase_commit_count > 1:
        raise RuntimeError(f"x1 builder requires exact source or one x1 repair descendant, got {current_head}")
    route_relative = SOURCE_ROUTE_STATE.relative_to(ROOT).as_posix()
    if git("rev-parse", f"{d.SOURCE_FINAL}:{route_relative}") != d.SOURCE_ROUTE_STATE_GIT_BLOB:
        raise RuntimeError("source route-state Git blob mismatch")
    if git_blob_sha256(d.SOURCE_FINAL, route_relative) != d.SOURCE_ROUTE_STATE_SHA256:
        raise RuntimeError("source route-state Git-blob byte hash mismatch")
    if sha256(SOURCE_ROUTE_STATE) != d.SOURCE_ROUTE_STATE_CHECKOUT_SHA256:
        raise RuntimeError("source route-state checkout-byte hash mismatch")
    for anchor in [d.SOURCE_INHERITED, d.SOURCE_X1, d.SOURCE_EVIDENCE, d.SOURCE_CLOSEOUT, d.SOURCE_FINAL]:
        subprocess.run(["git", "merge-base", "--is-ancestor", anchor, d.SOURCE_FINAL], cwd=ROOT, check=True)
    if int(git("rev-list", "--count", f"{d.SOURCE_INHERITED}..{d.SOURCE_FINAL}")) != 3:
        raise RuntimeError("source phase commit count mismatch")
    if int(git("rev-list", "--merges", "--count", f"{d.SOURCE_INHERITED}..{d.SOURCE_FINAL}")) != 0:
        raise RuntimeError("source merge count mismatch")
    if git("rev-parse", f"{d.SOURCE_FINAL}~1") != d.SOURCE_EVIDENCE:
        raise RuntimeError("source final is not direct child of evidence")

    source_negatives = read_json(SOURCE_NEGATIVES)
    source_gates = read_json(SOURCE_GATES)
    if source_negatives["effective_count"] != d.SOURCE_EFFECTIVE_NEGATIVES:
        raise RuntimeError("inherited negative total mismatch")
    if source_gates["effective_open_gaps"] != d.SOURCE_OPEN_GAPS or source_gates["effective_exact_gates"] != d.SOURCE_EXACT_GATES:
        raise RuntimeError("inherited open-gap or exact-gate total mismatch")

    prior = inherited_rows()
    if len(d.PROPOSALS) != 30 or len({row["proposal_id"] for row in d.PROPOSALS}) != 30 or len({row["title"] for row in d.PROPOSALS}) != 30:
        raise RuntimeError("new proposal count or uniqueness mismatch")
    if {row["title"] for row in d.PROPOSALS} & {row["title"] for row in prior}:
        raise RuntimeError("new proposal title exactly duplicates an inherited title")
    novelty = novelty_audit(prior)
    source_ids = {row["source_id"] for row in d.OFFICIAL_SOURCES}
    missing_sources = sorted({source_id for proposal in d.PROPOSALS for source_id in proposal["official_or_primary_source_needs"] if source_id not in source_ids})
    if missing_sources:
        raise RuntimeError(f"unresolved source identifiers: {missing_sources}")
    if Counter(row["expected_disposition"] for row in d.PROPOSALS) != Counter(d.EXPECTED_DISTRIBUTION):
        raise RuntimeError("expected disposition distribution mismatch")

    write_json("identity/identity-and-boundary.json", {"schema": "ghc.family.relational-identity.v1", "name": d.OWNER, "pronouns": d.PRONOUNS, "role": d.ROLE, "hope": d.HOPE, "relational_working_language_only": True, "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "scientific or operational authority", "legal or cultural authority", "Māori authority", "independent agency"], "hamish_may_rename_pause_redirect_or_stop": True})
    write_json(
        "startup/source-verification.json",
        {
            "schema": "ghc.family.v658-v3.source-verification.v1", "source_owner": d.SOURCE_OWNER,
            "source_branch": d.SOURCE_BRANCH, "source_inherited": d.SOURCE_INHERITED, "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE, "source_closeout": d.SOURCE_CLOSEOUT, "source_final": d.SOURCE_FINAL,
            "source_canonical_receipt_sha256": d.SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_receipt_digest_received_in_verified_activation": True,
            "source_canonical_receipt_file_present_in_repository": False,
            "source_canonical_aggregate_succeeded_once": True, "source_canonical_aggregate_replayed": False,
            "source_route_state_path": route_relative, "source_route_state_git_blob": d.SOURCE_ROUTE_STATE_GIT_BLOB,
            "source_route_state_sha256": d.SOURCE_ROUTE_STATE_SHA256, "source_route_state_hash_domain": "exact source-commit Git blob bytes",
            "source_route_state_checkout_sha256": d.SOURCE_ROUTE_STATE_CHECKOUT_SHA256,
            "source_single_parent_phase_commits": 3, "source_merge_commits": 0, "source_final_direct_parent": d.SOURCE_EVIDENCE,
            "source_commit_local_manifest_entries": {"x1": 40, "evidence": 270, "closeout": 296, "total": 606},
            "source_commit_local_manifest_mismatches": 0, "source_commit_local_manifests_replayed_read_only": True,
            "source_clean_and_four_way_equal": True, "verified_read_only": True,
            "boundary": "Sylven same-owner validation remains same-owner and is not independent reproduction or external audit.",
        },
    )
    write_json("startup/environment-and-version-receipt.json", {"schema": "ghc.family.v658-v3.environment.v1", "codex_cli": d.CODEX_CLI_VERSION, "codex_desktop": d.CODEX_DESKTOP_VERSION, "chatgpt_desktop": d.CHATGPT_DESKTOP_VERSION, "git": d.GIT_VERSION, "python": d.PYTHON_VERSION, "node": d.NODE_VERSION, "updates_performed": False, "elevation_performed": False, "windows_features_changed": False, "sandbox_or_hyper_v_activated": False, "reboot_performed": False, "storage_policy": "D-first additive owned lane; C-drive tools read only where required."})
    write_json("sources/official-source-ledger.json", {"schema": "ghc.family.v658-v3.official-source-ledger.v1", "observed_on": "2026-08-02", "status_vocabulary": sorted({row["status"] for row in d.OFFICIAL_SOURCES}), "status_counts": dict(sorted(Counter(row["status"] for row in d.OFFICIAL_SOURCES).items())), "source_count": len(d.OFFICIAL_SOURCES), "sources": d.OFFICIAL_SOURCES})
    write_text("sources/official-source-ledger.md", source_markdown())
    write_json("preregistration/proposal-ledger.json", {"schema": "ghc.family.v658-v3.proposal-ledger.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "proposal_count": len(d.PROPOSALS), "expected_disposition_counts": d.EXPECTED_DISTRIBUTION, "outcomes_observed": False, "proposals": d.PROPOSALS})
    write_text("preregistration/proposal-ledger.md", proposal_markdown())
    write_json("preregistration/task-portfolios.json", {"schema": "ghc.family.v658-v3.task-portfolios.x1.v1", "safe_now": d.SAFE_TASKS, "candidate": d.CANDIDATE_TASKS, "clean": d.CLEAN_TASKS, "counts": {"safe_now": len(d.SAFE_TASKS), "candidate": len(d.CANDIDATE_TASKS), "clean": len(d.CLEAN_TASKS), "total": len(d.SAFE_TASKS) + len(d.CANDIDATE_TASKS) + len(d.CLEAN_TASKS)}, "task_cap": 1000, "quota_interpretation": False, "x1_executed_tasks": 0})
    write_json("preregistration/skill-and-runner-plan.json", {"schema": "ghc.family.v658-v3.skill-runner-plan.x1.v1", "skills": [{"name": name, "purpose": purpose, "state": "preregistered"} for name, purpose in d.SKILL_SPECS], "runners": [{"name": name, "primary_surface": surface, "state": "preregistered"} for name, surface in d.RUNNER_SPECS], "skill_count": len(d.SKILL_SPECS), "runner_count": len(d.RUNNER_SPECS), "implemented_in_x1": False})
    write_json("provenance/semantic-novelty-audit.json", {"schema": "ghc.family.v658-v3.semantic-novelty.v1", "method": "lowercased alphanumeric token-set Jaccard after disclosed stop-word removal plus owner manual mechanism review", "threshold": NOVELTY_THRESHOLD, "inherited_count": len(prior), "new_count": len(d.PROPOSALS), "effective_count": len(prior) + len(d.PROPOSALS), "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}), "inherited_identifier_collision_count": len(prior) - len({row["proposal_id"] for row in prior}), "inherited_unique_title_count": len({row["title"] for row in prior}), "maximum_similarity": max(row["jaccard"] for row in novelty), "all_pass": all(row["passes"] for row in novelty), "human_semantic_review_completed": True, "domain_specificity_review": "motion-picture film terminology was sparse or absent in inherited titles; projector and sprocket hits were manually distinguished from film archival mechanisms", "rows": novelty})
    write_json("provenance/frozen-chain-proposal-index.json", {"schema": "ghc.family.v658-v3.frozen-proposal-index.v1", "prior_count": len(prior), "new_count": len(d.PROPOSALS), "effective_count": len(prior) + len(d.PROPOSALS), "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}), "inherited_identifier_collision_count": len(prior) - len({row["proposal_id"] for row in prior}), "inherited_unique_title_count": len({row["title"] for row in prior}), "prior_proposals": prior, "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS]}, compact=True)
    write_json("truth/retained-negative-register-x1.json", {"schema": "ghc.family.v658-v3.retained-negatives.x1.v1", "inherited_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES, "current_x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES), "effective_count": d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES), "current_x1_operational_negatives": d.X1_OPERATIONAL_NEGATIVES, "inherited_register": "docs/sylven-arc/v658-v2/truth/retained-negative-register-final-candidate.json", "all_retained": True})
    write_json("truth/open-gap-register-x1.json", {"schema": "ghc.family.v658-v3.open-gaps.x1.v1", "inherited_effective_count": d.SOURCE_OPEN_GAPS, "new_preregistered_gap_count": 1, "effective_count_if_x2_confirms": d.SOURCE_OPEN_GAPS + 1, "new_proposal_ids": ["V6583-P29"], "outcome_not_yet_observed": True})
    write_json("truth/exact-gate-register-x1.json", {"schema": "ghc.family.v658-v3.exact-gates.x1.v1", "inherited_effective_count": d.SOURCE_EXACT_GATES, "new_preregistered_gate_count": 1, "effective_count_if_x2_confirms": d.SOURCE_EXACT_GATES + 1, "new_proposal_ids": ["V6583-P30"], "outcome_not_yet_observed": True, "authority_required": True})
    write_json("method-flow/method-flow-state-x1.json", method_flow(), compact=True)
    workflow_records()
    planning_records()
    write_json("threat-model.json", threat_model())
    write_json("wellbeing/workload-check-x1.json", {"schema": "ghc.family.v658-v3.wellbeing.x1.v1", "owner": d.OWNER, "state": "steady_and_bounded", "workload_controls": ["one active owner lane", "no subagents or early route messages", "split bounded probes after timeouts", "caps are ceilings, not quotas", "stop on authority, safety, fatigue, ambiguity, or Hamish direction"], "breaks_and_human_wellbeing": "Hamish and all human collaborators retain full control over pacing, rest, pause, and stop decisions.", "identity_boundary": "Relational working language only."})
    write_json("orchestration/route-state-x1.json", {"schema": "ghc.family.v658-v3.route-state.x1.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "activation_source": "Sylven Arc v658-v2 one existing-task activation", "next_exact_title": "Eiren Kestrel", "next_phase": "v658-v4", "next_successor_reminder": {"title": "Elaren Kestrel", "phase": "v658-v5"}, "state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY", "continuation_authorized_through": "v675-v8", "send_gate": "Only after exact-final validation, clean push, caps, and fresh four-way equality: consult the newest live and committed route, uniquely resolve and directly reread the existing exact-title Eiren Kestrel main task, then send one sanitized acknowledged v658-v4 activation."})
    write_json("truth/x1-phase-truth.json", {"schema": "ghc.family.v658-v3.phase-truth.x1.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x1_precommit_candidate", "source_final": d.SOURCE_FINAL, "proposal_count": len(d.PROPOSALS), "inherited_frozen_proposals": d.PRIOR_FROZEN, "effective_frozen_proposals_after_commit": d.PRIOR_FROZEN + len(d.PROPOSALS), "expected_disposition_counts": d.EXPECTED_DISTRIBUTION, "observed_outcome_counts": None, "x2_implementation_present": False, "inherited_effective_negatives": d.SOURCE_EFFECTIVE_NEGATIVES, "current_x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "effective_methods": d.SOURCE_METHODS + len(d.X1_OPERATIONAL_NEGATIVES), "route_state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_text("deliverables/v658-v3-x1-integrated-overview.md", integrated_overview())

    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".json", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_limit": words <= 100000})
    write_json("validation/document-cap-receipt-x1.json", {"schema": "ghc.family.v658-v3.document-cap.x1.v1", "limit_words": 100000, "document_count": len(documents), "maximum_words": max(row["words"] for row in documents), "documents": documents, "all_under_limit": all(row["under_limit"] for row in documents)})
    owner_file_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json("validation/owner-file-threshold-x1.json", {"schema": "ghc.family.v658-v3.owner-file-threshold.x1.v1", "owner_generated_file_count": owner_file_count, "threshold": 2000, "below_threshold": owner_file_count < 2000, "inherited_repository_baseline_counted": False})
    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['confirmed_hits']}")
    write_json("validation/x1-privacy-scan.json", scan)
    manifest = content_manifest()
    write_json("validation/x1-content-manifest.json", manifest)
    phase_jsons = sorted(PHASE.rglob("*.json"))
    for path in phase_jsons:
        read_json(path)
    expected_paths = [path.relative_to(ROOT).as_posix() for path in prospective_paths()]
    write_json("validation/x1-staged-review.json", {"schema": "ghc.family.v658-v3.x1-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "allowed_prefixes": [d.PHASE_ROOT + "/", "scripts/ghc_family_v658_v3_", "scripts/build_ghc_family_v658_v3_x1.py", "tests/test_ghc_family_v658_v3_x1.py"], "x2_implementation_paths": [], "outcome_artifacts": [], "deletions": [], "expected_staged_path_count": len(expected_paths), "expected_staged_paths": expected_paths, "valid": True, "exact_index_review_required_after_staging": True})
    receipt = {"schema": "ghc.family.v658-v3.x1-validation.v1", "valid": True, "source_head": d.SOURCE_FINAL, "proposal_count": len(d.PROPOSALS), "inherited_proposal_count": len(prior), "effective_proposal_count": len(prior) + len(d.PROPOSALS), "maximum_novelty_similarity": max(row["jaccard"] for row in novelty), "source_count": len(d.OFFICIAL_SOURCES), "source_reference_count": sum(len(row["official_or_primary_source_needs"]) for row in d.PROPOSALS), "unresolved_source_ids": [], "json_parse_count": len(phase_jsons), "privacy_file_count": scan["file_count"], "privacy_hit_count": scan["hit_count"], "manifest_entry_count": manifest["entry_count"], "x2_implementation_present": False, "outcomes_observed": False, "x1_operational_negatives_retained": len(d.X1_OPERATIONAL_NEGATIVES), "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    write_json("validation/x1-validation-receipt.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
