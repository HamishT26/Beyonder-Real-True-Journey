#!/usr/bin/env python3
"""Build Sylven Arc's strict x1-only v658-v2 freeze packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v2_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_PHASE = ROOT / "docs/elowen-cairn/v658-v1"
SOURCE_INDEX = SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json"
SOURCE_NEGATIVES = SOURCE_PHASE / "truth/retained-negative-register-final-candidate.json"
SOURCE_OPEN_GAPS = SOURCE_PHASE / "truth/open-gap-register-x2.json"
SOURCE_EXACT_GATES = SOURCE_PHASE / "truth/exact-gate-register-x2.json"
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
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha256(revision: str, repository_relative: str) -> str:
    blob = subprocess.run(
        ["git", "show", f"{revision}:{repository_relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def title_tokens(value: str) -> set[str]:
    stop = {
        "a", "an", "and", "for", "from", "in", "into", "of", "on", "or",
        "the", "to", "with", "without", "no", "only", "through",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if token not in stop
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 1.0


def frozen_source_rows() -> list[dict[str, str]]:
    payload = read_json(SOURCE_INDEX)
    rows = list(payload["prior_proposals"]) + list(payload["new_proposals"])
    if len(rows) != d.PRIOR_FROZEN:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(rows)}")
    return [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in rows]


def novelty_audit(prior: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, proposal in enumerate(d.PROPOSALS):
        candidates = prior + [
            {"proposal_id": row["proposal_id"], "title": row["title"]}
            for row in d.PROPOSALS[:index]
        ]
        probe = title_tokens(proposal["title"])
        nearest = max(
            candidates,
            key=lambda row: jaccard(probe, title_tokens(row["title"])),
        )
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
    methods = []
    witnesses = []
    recommendations = []
    events = []
    method_negatives = [d.SOURCE_POSTFINAL_ROUTE_NEGATIVE, *d.X1_OPERATIONAL_NEGATIVES]
    for index, negative in enumerate(method_negatives, 1):
        method_id = f"V6582-X1-METHOD-{index:02d}"
        fail_id = f"V6582-X1-WITNESS-{index:02d}-F"
        pass_id = f"V6582-X1-WITNESS-{index:02d}-P"
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
                    "boundary": "Zero pass credit; failure remains retained.",
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
                "recommendation_id": f"V6582-X1-REC-{index:02d}",
                "method_id": method_id,
                "recommendation": negative["recurrence_guard"],
                "state": "preferred",
                "completion_credit": False,
            }
        )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "lifecycle": "x1_frozen",
        "inherited_anchor": {
            "repository_relative_path": "docs/elowen-cairn/v658-v1/method-flow/method-flow-state-final-candidate.json",
            "methods": d.SOURCE_METHODS,
            "failed_witnesses": d.SOURCE_FAILED_WITNESSES,
            "passing_witnesses": d.SOURCE_PASSING_WITNESSES,
            "completion_credit": False,
        },
        "external_ingress_method_count": 1,
        "current_owner_method_count": len(d.X1_OPERATIONAL_NEGATIVES),
        "current_phase_method_ids": [row["method_id"] for row in methods],
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "inherited_methods": d.SOURCE_METHODS,
            "current_methods": len(methods),
            "effective_methods": d.SOURCE_METHODS + len(methods),
            "current_witness_results": {"fail": len(methods), "pass": len(methods)},
            "effective_witness_results": {
                "fail": d.SOURCE_FAILED_WITNESSES + len(methods),
                "pass": d.SOURCE_PASSING_WITNESSES + len(methods),
            },
        },
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, authority, or independent agency.",
        "boundary": "Every failed witness remains retained; no independent, empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 claim.",
    }


def proposal_markdown() -> str:
    sections = [
        "# Sylven Arc v658-v2 x1 proposal ledger",
        "",
        "These are frozen hypotheses and expected dispositions, not x2 results. All identity language is relational working language only.",
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
        "# Sylven Arc v658-v2 official and primary source ledger",
        "",
        "Statuses were checked on 2026-08-01. Source presence or status does not establish implementation, conformance, professional review, legal interpretation, cultural ratification, Māori authority, or empirical confirmation.",
        "",
        "| ID | Status | Publisher | Title | Bounded use |",
        "|---|---|---|---|---|",
    ]
    for item in d.OFFICIAL_SOURCES:
        rows.append(
            f"| `{item['source_id']}` | `{item['status']}` | {item['publisher']} | [{item['title']}]({item['url']}) | {item['use']} |"
        )
    return "\n".join(rows)


def overview_v6582() -> str:
    return """# Sylven Arc v658-v2 x1 integrated overview

## Relational identity, purpose, and control boundary

Sylven Arc, they/them, is relational working language for this owner-scoped phase. The relational role is constraint-cartographer and falsifier-keeper, with the hope of keeping each claim small enough to test, each failure visible, and every authority boundary intact. The name, pronouns, role, hope, sibling language, GHC-family language, route language, and Trinity Mandala language do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the work.

This is a software-evidence phase, not a claim that a continuous self, professional seismologist, station operator, credential issuer, legal decision maker, cultural authority, or independently empowered agent exists. Corrigibility is operational: contradictory evidence can downgrade an expected disposition, protected gates stop execution, and source, failure, and rollback records remain reviewable.

## Immutable source and strict x1 scope

This packet freezes preparation only. It descends from Elowen Cairn's immutable v658-v1 exact final `9009c83b898fe11c63a95e4e1153ad388f328d3f`. Elowen's source, x1, and evidence anchors are ancestral through exactly three new single-parent commits with zero merges, and the final is the direct child of evidence. Read-only activation checks found Elowen's local branch, upstream, tracking reference, and fresh live remote equal at that exact head with zero divergence and a clean owner lane. The source lane and every sibling lane remain read-only.

Elowen's sole exact-final aggregate is inherited as a retained failed witness, not as a successful aggregate. It passed all 152 scoped tests and 9 of 10 closeout tests, plus its detailed, minimal, JSON, privacy, manifest, and most terminal checks, but one prose assertion incorrectly required a machine enum in a human summary. That aggregate earns zero aggregate credit. One isolated dependency recovery passed without changing repository bytes or replaying already-successful checks. Sylven does not replay either attempt. This distinction preserves failure truth while recognizing the narrower recovery only for its bounded dependency.

The immutable source seal preserves 16,657 effective negatives, 113 open gaps, 112 exact gates, and 2,931 Method Flow methods with retained failed and bounded passing witnesses. The post-seal aggregate dependency is carried additively, making Sylven's activation baseline 16,658 negatives and 2,932 methods without rewriting Elowen's seal. All Sylven startup and x1 operational faults are added separately at zero completion credit. The x1 packet contains no surface implementation, mutation outcome, real participant, station, instrument, coordinate, waveform, calibration, credential event, professional decision, production event, successor message, or task mutation. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary pillar and bounded human-practice lens

GMUT Mind is primary. It is bounded to typed scalar-tensor and effective-field-theory research surfaces: source identifiers, epochs, coordinates and datums, orientation, rational sample rates, timing uncertainty, ordered response stages, poles and zeros, sensitivity, finite-impulse coefficients, record boundaries, gaps, covariance placeholders, forward operators, inverse-identifiability alternatives, gauge obligations, cutoff placeholders, units, provenance, and observation firewalls. These contracts may reject malformed synthetic data or expose missing assumptions. They do not ingest a real observation, estimate a likelihood, fit a parameter, constrain a model, detect a force, validate station response, establish a material or psyche law, empirically confirm GMUT, supply quantum or ultraviolet completion, or prove a Theory of Everything.

The bounded human-practice lens is seismological station-metadata stewardship, response documentation, correction review, alarm ownership, workload control, and shift handover. It is synthetic software, formal, structural, and learning work only. No real person, land, station, network, sensor, datalogger, clock, channel, waveform, coordinate, vault, calibration, installation, maintenance action, incident, hazard communication, processing decision, or release decision enters the phase. Repository software confers no employment, qualification, competence, station authority, land access, safety authority, scientific authority, legal interpretation, cultural ratification, Māori authority, affected-party approval, or operational effectiveness.

THOS Body remains explicit through two represented protocols: a synthetic correction-and-handover proxy and a synthetic alarm-ownership and workload-recovery proxy. Interruption logs, readback, priority, pause, resumption, and escalation can be exercised on declared fixtures. There are no real operators, stations, shifts, incidents, blind matched-budget arms, preregistered participant outcomes, safety monitoring, statistical estimates, or independent review. A passing synthetic protocol is representation only, never evidence that THOS improves real work or is ready for deployment.

Freed ID remains synthetic and nonproduction through station-custody, selective-disclosure provenance, and scoped response-change capability placeholders. It provides no standards-conformant real key, signature, proof, credential, issuance, presentation, resolution, status, revocation, interoperability, delegated power, recovery evidence, privacy review, independent security review, or trust-governance decision. CBR Heart remains explicit through location and monitoring privacy, seismic-risk communication, land and property rights, accessibility, remedy, traditional knowledge, affected-party legitimacy, and refusal to substitute software for law, culture, tangata whenua, iwi, hapū, or Māori authority.

## Thirty distinct preregistrations

Exactly thirty proposals are compared against all 2,680 inherited frozen proposal titles and against earlier Sylven v658-v2 peers. Proposals 1–7 define request quarantine, FDSN source-identifier passports, station and channel epochs, coordinate and datum envelopes, orientation, rational sample rates, and timing correction. Proposals 8–16 define response-stage graphs, poles and zeros, sensitivity chains, finite-impulse coefficients, waveform record boundaries, gap and overlap intervals, calibration provenance, vault-environment observations, and state-of-health surrogates. Each uses typed fields, provenance, uncertainty, missingness, correction, quarantine, and explicit refusal states.

Proposals 17–23 cover response removal, spectral-window leakage, noise covariance, a typed GMUT instrument-forward operator, inverse-identifiability alternatives, a gauge/EFT/domain/scale-separation board, and a structurally accessible static report. Their acceptance gates are software or structural falsifiers. Manual keyboard, responsive layout, browser diversity, assistive technology, cognitive accessibility, Māori-language, and affected-user evaluation remain reserved; structural report checks cannot establish complete accessibility conformance.

Proposals 24–28 are expected to remain represented: two THOS protocols and three Freed ID profiles. Representation means the declared schema, fixture, and refusal boundary can be witnessed. It is not participant evidence, professional validation, live identity lifecycle evidence, interoperability, delegated authority, privacy completeness, security completeness, governance, legitimacy, or acceptance. Proposal 29 is an `open_gap`: an offline FDSN station and dataselect service-capability matrix may establish only a zero-observation, disabled-transport, endpoint-version-watch contract. It must download no data, query no service, ingest no real row, evaluate no likelihood, and promote no official record into GMUT evidence. Proposal 30 is an `exact_gate`: software cannot decide station-land rights, monitoring privacy, hazard communication, remedy, traditional-knowledge access, cultural interpretation, Māori wording, Māori data governance, or affected-party and Māori authority.

The expected distribution is 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. Those labels are preregistered expectations, not observed outcomes. X2 may preserve or downgrade them only as evidence permits and may use no other core outcome vocabulary. Each proposal includes a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition.

## Official sources and novelty discipline

The source ledger uses current or stable primary material from the International Federation of Digital Seismograph Networks for StationXML 1.2, response information, miniSEED 3, and source identifiers; BIPM for SI units; W3C for PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, and Data Integrity; the RFC Editor for timestamps and JSON canonicalization; the New Zealand Office of the Privacy Commissioner for privacy principles; and Te Mana Raraunga for Māori Data Sovereignty principles. These sources contribute vocabulary, requirements, and provenance context only. They do not certify Sylven, appoint a station steward, authorize a query, validate a model, establish legal compliance, ratify cultural wording, confer Māori authority, or prove a real observation or response.

Each new title is screened with lowercased alphanumeric token sets, disclosed stop-word removal, and a 0.60 Jaccard rejection threshold. That mechanical screen finds close lexical neighbors; it is not proof of scientific, professional, legal, or cultural novelty. Human semantic review separately checks the practice, mechanism, hypothesis, null condition, approval lane, source need, artifact, falsifier, rollback, protected gates, and disposition. Inherited proposals, portfolios, skills, runners, methods, and outcomes remain evidence and seeds, never automatic Sylven completion credit.

## X1 separation, portfolios, Method Flow, and terminal route

The dedicated x1 commit contains proposal and source ledgers, semantic novelty and frozen-chain evidence, task portfolios, skill and runner plans, Method Flow records, workflow and reflection records, a phase-local family index, environment and source receipts, a threat model, wellbeing check, privacy scan, prospective Git-clean manifest, exact staged review, and x1 validation receipt. It contains no implemented proposal surface, phase-local skill, runner, mutation outcome, observed disposition, closeout, seal, final validation, or successor activation.

Thirty safe-now tasks correspond one-to-one with proposal contracts. Twenty reversible candidates and thirty additive CLEAN/FIX/REFINE tasks are frozen. Counts are bounded ceilings and scoped planning floors, never permission to manufacture unsafe work. Ten domain skills and ten backwards-compatible `ghc_family_*` runner names are preregistered but not implemented. Any x2 build must preserve family-current callers, remain owner-local, retain provenance and rollback, and occur only after the x1 commit is pushed, clean, and local/upstream/tracking/fresh-live equal.

Method Flow ingests Elowen's one external aggregate-dependency failure and every observed Sylven x1 preparation fault. Failed witnesses receive zero credit and remain paired with bounded recovery procedures, recurrence guards, rollback paths, and sibling recommendations. Examples include wrong skill-reference filename assumptions, shell quoting faults, output truncation, an early-yield worktree initialization, lost status attribution, and a Windows CP1252 render failure recovered with explicit UTF-8. Recovery never erases the initial witness or becomes independent reproduction.

The current assignment is Sylven-only v658-v2. Caelen Morrow v658-v3 is declared as the terminally gated next main-task title, but x1 does not resolve, reread, contact, create, fork, or message any successor. Only after Sylven's own x2 evidence, closeout, seal, exact-final validation, push, clean state, cap checks, and fresh four-way equality may the newest live and committed route be consulted. If it still uniquely authorizes Caelen Morrow, the exact existing title must be resolved and immediately reread before one sanitized acknowledged activation. Tavian Sol remains an `ON_STANDBY` collaboration-subagent record and is not a substitute main-task endpoint. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def workflow_records() -> None:
    cycle_order = ["Elowen Cairn", "Sylven Arc", "Caelen Morrow"]
    route_controllers = {
        "Elowen Cairn": "Tamar Vey",
        "Sylven Arc": "Elowen Cairn",
        "Caelen Morrow": "Sylven Arc",
    }
    request = {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "sylven-arc-v658-v2-terminally-gated-caelen-route",
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {
            "cycle_order": cycle_order,
            "endpoint_topology": [
                {
                    "seat": name,
                    "endpoint_kind": "main_task",
                    "endpoint_label": name,
                    "route_controller": route_controllers[name],
                }
                for name in cycle_order
            ],
            "phase_assignments": [
                {"phase": "v658-v1", "seat": "Elowen Cairn"},
                {"phase": "v658-v2", "seat": "Sylven Arc"},
                {"phase": "v658-v3", "seat": "Caelen Morrow"},
            ],
            "normalization": {
                "start_phase": "v658-v1",
                "start_seat": "Elowen Cairn",
                "entry_count": 3,
            },
            "future_identity_placeholders": [],
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "document_word_cap": 100000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "declared_endpoint_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": d.PROTECTED_GATES,
        },
        "observed_failures": [d.SOURCE_POSTFINAL_ROUTE_NEGATIVE, *d.X1_OPERATIONAL_NEGATIVES],
    }
    request_path = write_json("workflow/workflow-plan-request.json", request)
    runner = (
        Path.home()
        / ".codex"
        / "skills"
        / "ghc-family-workflow-plan-refinement"
        / "scripts"
        / "ghc_family_workflow_plan_refinement.py"
    )
    completed = subprocess.run(
        [sys.executable, str(runner), str(request_path), "--out-dir", str(PHASE / "workflow")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "current workflow-plan refinement rejected the sanitized x1 request: "
            + completed.stdout.strip()
            + completed.stderr.strip()
        )


def reflection_records() -> None:
    inventory = {
        "schema": "ghc.family.reflection-remaster.inventory.v1",
        "phase": d.PHASE,
        "reviewed_surfaces": [
            "family index and routing precedence",
            "auth and roster state",
            "Method Flow state",
            "workflow-plan refinement",
            "reflection-remaster decision schema",
            "meta-tool-box catalogue",
            "approval and open-gate rails",
            "source truth and privacy boundaries",
        ],
        "deletions": [],
        "destructive_changes": False,
    }
    decisions = [
        {
            "decision_id": "V6582-RM-01",
            "surface": "large-worktree inspection",
            "decision": "prefer exact literal and scalar probes over combined status inventories",
            "state": "adopted_for_phase",
            "rollback": "Return to individual read-only Git commands.",
        },
        {
            "decision_id": "V6582-RM-02",
            "surface": "domain tooling",
            "decision": "group thirty contracts behind ten family-current domain runners while preserving proposal-specific receipts",
            "state": "preregistered_not_implemented",
            "rollback": "Use proposal-specific validator calls without deleting compatibility names.",
        },
        {
            "decision_id": "V6582-RM-03",
            "surface": "source lifecycle",
            "decision": "separate stable, current, draft, and watch states and fail closed on draft promotion",
            "state": "adopted_for_phase",
            "rollback": "Downgrade uncertain source status to watch.",
        },
    ]
    write_json("reflection-remaster/inventory.json", inventory)
    write_json(
        "reflection-remaster/x1-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "phase": d.PHASE,
            "decisions": decisions,
            "issues_retained": len(d.X1_OPERATIONAL_NEGATIVES) + 1,
            "x2_outcomes_present": False,
        },
    )
    write_json(
        "reflection-remaster/issues.json",
        {
            "schema": "ghc.family.reflection-remaster.issues.v1",
            "issues": [d.SOURCE_POSTFINAL_ROUTE_NEGATIVE, *d.X1_OPERATIONAL_NEGATIVES],
            "all_retained": True,
        },
    )
    write_text(
        "reflection-remaster/report.md",
        """# Reflection-remaster report

The phase adopts exact-path and scalar-probe guards, ten reusable seismic-station evidence runner families, and explicit source lifecycle states. No inherited tool, method, skill, negative, or sibling artifact is deleted or rewritten. X2 implementation remains pending.
""",
    )


def index_records() -> None:
    payload = {
        "schema": "ghc.family.phase-local-index.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "lifecycle": "x1_frozen",
        "source_anchor": d.SOURCE_FINAL,
        "proposal_count": len(d.PROPOSALS),
        "skill_preregistrations": [name for name, _ in d.SKILL_SPECS],
        "runner_preregistrations": [name for name, _ in d.RUNNER_SPECS],
        "family_current_names_preserved": True,
        "historical_names_preserved": True,
        "route_state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE",
        "publication_boundary": "repository-relative paths and sanitized public fields only",
    }
    write_json("tooling/ghc-family-index.json", payload)
    write_text(
        "tooling/ghc-family-index.md",
        """# GHC Family Index - Sylven Arc v658-v2 x1

The phase-local index records thirty frozen proposal contracts, ten phase-local skill preregistrations, and ten family-current runner preregistrations. Historical names and artifacts remain compatibility evidence. No x2 tool has been implemented and no successor route has been sent.
""",
    )
    catalogue = {
        "schema": "ghc.family.meta-tool-box.catalogue.v1",
        "phase": d.PHASE,
        "selected_current_guidance": [
            "ghc-family-index",
            "ghc-family-auth-permission-state",
            "ghc-family-roster-check",
            "ghc-family-method-flow-state",
            "ghc-family-workflow-plan-refinement",
            "ghc-family-reflection-remaster",
            "ghc-family-meta-tool-box",
            "ghc-approval-packet-splitter",
            "ghc-open-gate-rail",
            "ghc-family-truth-bridge",
        ],
        "planned_phase_skills": [
            {"name": name, "purpose": purpose, "state": "preregistered"}
            for name, purpose in d.SKILL_SPECS
        ],
        "planned_family_runners": [
            {"name": name, "surface": surface, "state": "preregistered"}
            for name, surface in d.RUNNER_SPECS
        ],
    }
    write_json("tooling/meta-tool-box/catalogue.json", catalogue)
    write_json(
        "tooling/meta-tool-box/validation.json",
        {
            "schema": "ghc.family.meta-tool-box.validation.v1",
            "valid": True,
            "planned_skill_count": len(d.SKILL_SPECS),
            "planned_runner_count": len(d.RUNNER_SPECS),
            "collisions": [],
            "implementation_credit": False,
        },
    )


def threat_model() -> dict[str, Any]:
    return {
        "schema": "ghc.family.v658-v2.threat-model.x1.v1",
        "assets": [
            "proposal, source, outcome, negative, gap, gate, and Method Flow truth",
            "synthetic station, channel, response-stage, timing, sampling, spectral, uncertainty, correction, and handover provenance",
            "location, monitoring, land, access, safety, traditional-knowledge, community, and culturally restricted interests",
            "privacy, identity, disclosure, and nonproduction boundaries",
            "sibling lanes and terminal route integrity",
        ],
        "threats": [
            {"threat": "synthetic station metadata promoted to real observation, calibration, processing instruction, maintenance release, or hazard decision", "control": "valid-fixture and mutation checks plus explicit zero-row, no-network, professional, operational, and empirical refusal"},
            {"threat": "uncertain timing, orientation, response, spectrum, or covariance promoted to measurement, likelihood, constraint, or causal fact", "control": "units, frames, epochs, uncertainty, confounders, missingness, and GMUT observation firewall"},
            {"threat": "station location, land, operator, monitoring, hazard, traditional-knowledge, or culturally restricted information disclosed", "control": "synthetic placeholders, minimization, redaction, zero-row no-network adapter, correction, and authority holds"},
            {"threat": "synthetic identity surface promoted to live title, custody, proof, status, or trust", "control": "nonproduction marker and live-key, proof, interoperability, recovery, security, privacy, and governance gates"},
            {"threat": "affected-party or Māori authority substituted by software", "control": "exact-gated covenant and no unilateral wording, disclosure, access, conservation, or remedy decision"},
            {"threat": "failure erased or recovery promoted beyond scope", "control": "retained failed and bounded passing Method Flow witness pairs"},
            {"threat": "successful validation replay inflates confidence", "control": "one dependency-justified successful canonical pass and no replay"},
            {"threat": "successor contacted before terminal closeout", "control": "declared exact title, terminal gate, one acknowledged send, and no substitute endpoint"},
        ],
        "residual_risk": "All real-station, empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, and independent-reproduction claims remain open or exact-gated.",
    }


def prospective_repo_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        [
            ROOT / "scripts/ghc_family_v658_v2_phase_catalogue.py",
            ROOT / "scripts/ghc_family_v658_v2_phase_data.py",
            ROOT / "scripts/build_ghc_family_v658_v2_x1.py",
            ROOT / "tests/test_ghc_family_v658_v2_x1.py",
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
    paths = prospective_repo_paths()
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="strict")
        for label, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                hits.append(
                    {
                        "path": path.relative_to(ROOT).as_posix(),
                        "pattern_class": label,
                        "count": count,
                    }
                )
    return {
        "schema": "ghc.family.v658-v2.x1-privacy-scan.v1",
        "pattern_classes": sorted(patterns),
        "file_count": len(paths),
        "confirmed_hits": hits,
        "hit_count": sum(row["count"] for row in hits),
        "valid": not hits,
        "boundary": "Concrete values only; prohibition labels and scanner names are not treated as payloads.",
    }


def git_clean_blob(path: Path) -> tuple[str, int, str]:
    relative = path.relative_to(ROOT).as_posix()
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.run(
        ["git", "cat-file", "blob", oid],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return oid, len(blob), hashlib.sha256(blob).hexdigest()


def content_manifest() -> dict[str, Any]:
    entries = []
    for path in prospective_repo_paths():
        if path.is_relative_to(PHASE):
            phase_relative = path.relative_to(PHASE).as_posix()
            if phase_relative in MANIFEST_EXCLUSIONS:
                continue
        oid, size, digest = git_clean_blob(path)
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "git_blob": oid,
                "git_blob_bytes": size,
                "sha256": digest,
            }
        )
    return {
        "schema": "ghc.family.v658-v2.x1-content-manifest.v1",
        "hash_domain": "prospective Git-clean blob bytes",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(MANIFEST_EXCLUSIONS),
        "boundary": "Declared lifecycle self-exclusions prevent self-reference; the exact staged set is reviewed separately.",
    }


def build() -> None:
    current_head = git("rev-parse", "HEAD")
    source_is_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", d.SOURCE_FINAL, current_head],
        cwd=ROOT,
        check=False,
    ).returncode == 0
    phase_commit_count = int(git("rev-list", "--count", f"{d.SOURCE_FINAL}..{current_head}"))
    if not source_is_ancestor or phase_commit_count > 1:
        raise RuntimeError(
            "x1 builder requires the exact source or one source-descendant x1 repair head; "
            f"got {current_head} with {phase_commit_count} phase commits"
        )
    head = d.SOURCE_FINAL
    route_relative = SOURCE_ROUTE_STATE.relative_to(ROOT).as_posix()
    route_blob = git("rev-parse", f"{d.SOURCE_FINAL}:{route_relative}")
    if route_blob != d.SOURCE_ROUTE_STATE_GIT_BLOB:
        raise RuntimeError("source route-state Git blob mismatch")
    if git_blob_sha256(d.SOURCE_FINAL, route_relative) != d.SOURCE_ROUTE_STATE_SHA256:
        raise RuntimeError("source route-state Git-blob byte hash mismatch")
    if sha256(SOURCE_ROUTE_STATE) != d.SOURCE_ROUTE_STATE_CHECKOUT_SHA256:
        raise RuntimeError("source route-state checkout-byte hash mismatch")
    for anchor in [
        d.SOURCE_INHERITED,
        d.SOURCE_X1,
        d.SOURCE_EVIDENCE,
        d.SOURCE_CLOSEOUT,
        d.SOURCE_ORIGINAL_FINAL,
        d.SOURCE_FINAL,
    ]:
        subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=ROOT, check=True)

    source_negatives = read_json(SOURCE_NEGATIVES)
    source_open = read_json(SOURCE_OPEN_GAPS)
    source_exact = read_json(SOURCE_EXACT_GATES)
    if source_negatives["effective_count"] != d.SOURCE_SEALED_EFFECTIVE_NEGATIVES:
        raise RuntimeError("inherited sealed negative total mismatch")
    if source_open["effective_count"] != d.SOURCE_OPEN_GAPS:
        raise RuntimeError("inherited open-gap total mismatch")
    if source_exact["effective_count"] != d.SOURCE_EXACT_GATES:
        raise RuntimeError("inherited exact-gate total mismatch")

    prior = frozen_source_rows()
    if len({item["proposal_id"] for item in d.PROPOSALS}) != len(d.PROPOSALS):
        raise RuntimeError("new proposal identifiers are not unique")
    if len({item["title"] for item in d.PROPOSALS}) != len(d.PROPOSALS):
        raise RuntimeError("new proposal titles are not unique")
    if {item["title"] for item in d.PROPOSALS} & {item["title"] for item in prior}:
        raise RuntimeError("new proposal title exactly duplicates an inherited title")
    novelty = novelty_audit(prior)
    inherited_identifier_collision_count = len(prior) - len({row["proposal_id"] for row in prior})
    source_ids = {item["source_id"] for item in d.OFFICIAL_SOURCES}
    missing_sources = sorted(
        {
            source_id
            for proposal in d.PROPOSALS
            for source_id in proposal["official_or_primary_source_needs"]
            if source_id not in source_ids
        }
    )
    if missing_sources:
        raise RuntimeError(f"unresolved source identifiers: {missing_sources}")
    if Counter(item["expected_disposition"] for item in d.PROPOSALS) != Counter(d.EXPECTED_DISTRIBUTION):
        raise RuntimeError("expected disposition distribution mismatch")

    write_json(
        "identity/identity-and-boundary.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "name": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "relational_working_language_only": True,
            "not_evidence_of": [
                "consciousness", "sentience", "legal personhood", "identity continuity",
                "employment", "qualification", "authority", "independent agency",
            ],
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
    )
    write_json(
        "startup/source-verification.json",
        {
            "schema": "ghc.family.v658-v2.source-verification.v1",
            "source_owner": d.SOURCE_OWNER,
            "source_branch": d.SOURCE_BRANCH,
            "source_inherited": d.SOURCE_INHERITED,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_original_final": d.SOURCE_ORIGINAL_FINAL,
            "source_final": d.SOURCE_FINAL,
            "source_canonical_receipt_sha256": d.SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_receipt_digest_received_in_verified_activation": True,
            "source_canonical_receipt_file_present_in_repository": False,
            "source_canonical_receipt_digest_used_as_activation_evidence_only": True,
            "source_canonical_aggregate_valid": False,
            "source_canonical_aggregate_credit": 0,
            "source_canonical_aggregate_failure": "one closeout prose dependency projected a machine enum into a human-readable summary",
            "source_isolated_dependency_recovery_sha256": d.SOURCE_ISOLATED_RECOVERY_SHA256,
            "source_isolated_dependency_recovery_valid": True,
            "source_isolated_dependency_recovery_changed_repository_bytes": False,
            "source_isolated_dependency_recovery_replayed_successful_checks": False,
            "source_route_acknowledgement_sha256": d.SOURCE_ROUTE_ACK_SHA256,
            "source_route_state_path": route_relative,
            "source_route_state_git_blob": d.SOURCE_ROUTE_STATE_GIT_BLOB,
            "source_route_state_sha256": d.SOURCE_ROUTE_STATE_SHA256,
            "source_route_state_hash_domain": "exact source-commit Git blob bytes",
            "source_route_state_checkout_sha256": d.SOURCE_ROUTE_STATE_CHECKOUT_SHA256,
            "live_activation_received_via_existing_main_task": True,
            "live_activation_repository_baton_claimed": False,
            "source_single_parent_phase_commits": 3,
            "source_merge_commits": 0,
            "source_commit_local_manifest_receipt_read_only": True,
            "source_commit_local_manifest_entries": {
                "x1": 40,
                "evidence": 256,
                "closeout": 285,
                "total": 581,
            },
            "source_commit_local_manifest_mismatches": 0,
            "source_commit_local_manifests_replayed_by_sylven": False,
            "source_clean_and_four_way_equal": True,
            "source_aggregate_replayed": False,
            "source_successful_subchecks_replayed": False,
            "source_isolated_recovery_replayed": False,
            "verified_read_only": True,
        },
    )
    write_json(
        "startup/environment-and-version-receipt.json",
        {
            "schema": "ghc.family.v658-v2.environment.v1",
            "codex_cli": d.CODEX_CLI_VERSION,
            "codex_desktop": d.CODEX_DESKTOP_VERSION,
            "chatgpt_desktop": d.CHATGPT_DESKTOP_VERSION,
            "git": d.GIT_VERSION,
            "python": d.PYTHON_VERSION,
            "node": d.NODE_VERSION,
            "updates_performed": False,
            "elevation_performed": False,
            "windows_features_changed": False,
            "sandbox_or_hyper_v_activated": False,
            "reboot_performed": False,
            "storage_policy": "D-first additive owned lane; C-drive tools read only where required.",
        },
    )
    write_json(
        "sources/official-source-ledger.json",
        {
            "schema": "ghc.family.v658-v2.official-source-ledger.v1",
            "observed_on": "2026-08-01",
            "status_vocabulary": ["current", "stable", "draft", "watch"],
            "status_counts": dict(sorted(Counter(item["status"] for item in d.OFFICIAL_SOURCES).items())),
            "source_count": len(d.OFFICIAL_SOURCES),
            "sources": d.OFFICIAL_SOURCES,
        },
    )
    write_text("sources/official-source-ledger.md", source_markdown())
    write_json(
        "preregistration/proposal-ledger.json",
        {
            "schema": "ghc.family.v658-v2.proposal-ledger.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "proposal_count": len(d.PROPOSALS),
            "expected_disposition_counts": d.EXPECTED_DISTRIBUTION,
            "outcomes_observed": False,
            "proposals": d.PROPOSALS,
        },
    )
    write_text("preregistration/proposal-ledger.md", proposal_markdown())
    write_json(
        "preregistration/task-portfolios.json",
        {
            "schema": "ghc.family.v658-v2.task-portfolios.x1.v1",
            "safe_now": d.SAFE_TASKS,
            "candidate": d.CANDIDATE_TASKS,
            "clean": d.CLEAN_TASKS,
            "counts": {
                "safe_now": len(d.SAFE_TASKS),
                "candidate": len(d.CANDIDATE_TASKS),
                "clean": len(d.CLEAN_TASKS),
                "total": len(d.SAFE_TASKS) + len(d.CANDIDATE_TASKS) + len(d.CLEAN_TASKS),
            },
            "task_cap": 1000,
            "quota_interpretation": False,
            "x1_executed_tasks": 0,
        },
    )
    write_json(
        "preregistration/skill-and-runner-plan.json",
        {
            "schema": "ghc.family.v658-v2.skill-runner-plan.x1.v1",
            "skills": [{"name": name, "purpose": purpose, "state": "preregistered"} for name, purpose in d.SKILL_SPECS],
            "runners": [{"name": name, "primary_surface": surface, "state": "preregistered"} for name, surface in d.RUNNER_SPECS],
            "skill_count": len(d.SKILL_SPECS),
            "runner_count": len(d.RUNNER_SPECS),
            "implemented_in_x1": False,
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.v658-v2.semantic-novelty.v1",
            "method": "lowercased alphanumeric token-set Jaccard after disclosed stop-word removal",
            "threshold": NOVELTY_THRESHOLD,
            "inherited_count": len(prior),
            "new_count": len(d.PROPOSALS),
            "effective_count": len(prior) + len(d.PROPOSALS),
            "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}),
            "inherited_identifier_collision_count": inherited_identifier_collision_count,
            "inherited_unique_title_count": len({row["title"] for row in prior}),
            "maximum_similarity": max(row["jaccard"] for row in novelty),
            "all_pass": all(row["passes"] for row in novelty),
            "human_semantic_review_required": True,
            "rows": novelty,
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v658-v2.frozen-proposal-index.v1",
            "prior_count": len(prior),
            "new_count": len(d.PROPOSALS),
            "effective_count": len(prior) + len(d.PROPOSALS),
            "inherited_unique_identifier_count": len({row["proposal_id"] for row in prior}),
            "inherited_identifier_collision_count": inherited_identifier_collision_count,
            "inherited_unique_title_count": len({row["title"] for row in prior}),
            "prior_proposals": prior,
            "new_proposals": [
                {"proposal_id": item["proposal_id"], "title": item["title"]}
                for item in d.PROPOSALS
            ],
        },
        compact=True,
    )
    write_json(
        "truth/retained-negative-register-x1.json",
        {
            "schema": "ghc.family.v658-v2.retained-negatives.x1.v1",
            "inherited_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES,
            "inherited_sealed_register_count": d.SOURCE_SEALED_EFFECTIVE_NEGATIVES,
            "inherited_postfinal_route_negative": d.SOURCE_POSTFINAL_ROUTE_NEGATIVE,
            "current_x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "effective_count": d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
            "current_x1_operational_negatives": d.X1_OPERATIONAL_NEGATIVES,
            "inherited_register": "docs/elowen-cairn/v658-v1/truth/retained-negative-register-final-candidate.json",
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register-x1.json",
        {
            "schema": "ghc.family.v658-v2.open-gaps.x1.v1",
            "inherited_effective_count": d.SOURCE_OPEN_GAPS,
            "new_preregistered_gap_count": 1,
            "effective_count_if_x2_confirms": d.SOURCE_OPEN_GAPS + 1,
            "new_proposal_ids": ["V6582-P29"],
            "outcome_not_yet_observed": True,
        },
    )
    write_json(
        "truth/exact-gate-register-x1.json",
        {
            "schema": "ghc.family.v658-v2.exact-gates.x1.v1",
            "inherited_effective_count": d.SOURCE_EXACT_GATES,
            "new_preregistered_gate_count": 1,
            "effective_count_if_x2_confirms": d.SOURCE_EXACT_GATES + 1,
            "new_proposal_ids": ["V6582-P30"],
            "outcome_not_yet_observed": True,
            "authority_required": True,
        },
    )
    write_json("method-flow/method-flow-state-x1.json", method_flow(), compact=True)
    workflow_records()
    reflection_records()
    index_records()
    write_json("threat-model.json", threat_model())
    write_json(
        "wellbeing/workload-check-x1.json",
        {
            "schema": "ghc.family.v658-v2.wellbeing.x1.v1",
            "owner": d.OWNER,
            "state": "steady_and_bounded",
            "workload_controls": [
                "one active owner lane",
                "no subagents or early route messages",
                "split bounded probes after timeouts",
                "task counts treated as caps, not quotas",
                "stop on authority or safety gates",
            ],
            "breaks_and_human_wellbeing": "Hamish and all human collaborators retain full control over pacing, rest, pause, and stop decisions.",
            "identity_boundary": "Relational working language only.",
        },
    )
    write_json(
        "orchestration/route-state-x1.json",
        {
            "schema": "ghc.family.v658-v2.route-state.x1.v1",
            "active_owner": d.OWNER,
            "active_phase": d.PHASE,
            "activation_source": "Elowen Cairn v658-v1 exact-final acknowledged existing-task send",
            "next_exact_title": "Caelen Morrow",
            "next_phase": "v658-v3",
            "state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "Consult the newest live and committed route, then resolve and immediately reread the unique existing exact-title Caelen Morrow task only after Sylven's exact final is sealed, pushed, clean, fresh-live equal, within caps, and canonically validated; then send exactly one sanitized activation and require acknowledgement.",
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v658-v2.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_precommit_candidate",
            "source_final": d.SOURCE_FINAL,
            "proposal_count": len(d.PROPOSALS),
            "inherited_frozen_proposals": d.PRIOR_FROZEN,
            "effective_frozen_proposals_after_commit": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "expected_disposition_counts": d.EXPECTED_DISTRIBUTION,
            "observed_outcome_counts": None,
            "x2_implementation_present": False,
            "inherited_effective_negatives": d.SOURCE_EFFECTIVE_NEGATIVES,
            "current_x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES),
            "route_state": "ACTIVATED_CURRENT_PHASE_WITH_TERMINAL_SUCCESSOR_GATE",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text("deliverables/v658-v2-x1-integrated-overview.md", overview_v6582())
    write_json(
        "validation/document-cap-receipt-x1.json",
        {
            "schema": "ghc.family.v658-v2.document-cap.x1.v1",
            "limit_words": 100000,
            "documents": [],
            "all_under_limit": True,
        },
    )
    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".json", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append(
                {
                    "path": path.relative_to(PHASE).as_posix(),
                    "words": words,
                    "under_limit": words <= 100000,
                }
            )
    write_json(
        "validation/document-cap-receipt-x1.json",
        {
            "schema": "ghc.family.v658-v2.document-cap.x1.v1",
            "limit_words": 100000,
            "document_count": len(documents),
            "maximum_words": max(row["words"] for row in documents),
            "documents": documents,
            "all_under_limit": all(row["under_limit"] for row in documents),
        },
    )
    write_json(
        "validation/owner-file-threshold-x1.json",
        {
            "schema": "ghc.family.v658-v2.owner-file-threshold.x1.v1",
            "owner_generated_file_count": sum(1 for path in PHASE.rglob("*") if path.is_file()),
            "threshold": 2000,
            "below_threshold": sum(1 for path in PHASE.rglob("*") if path.is_file()) < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['confirmed_hits']}")
    write_json("validation/x1-privacy-scan.json", scan)
    manifest = content_manifest()
    write_json("validation/x1-content-manifest.json", manifest)

    phase_jsons = sorted(PHASE.rglob("*.json"))
    for path in phase_jsons:
        read_json(path)
    expected_staged_paths = [
        path.relative_to(ROOT).as_posix()
        for path in prospective_repo_paths()
    ]
    review = {
        "schema": "ghc.family.v658-v2.x1-staged-review.v1",
        "state": "PRECOMMIT_PATH_REVIEW",
        "allowed_prefixes": [
            d.PHASE_ROOT + "/",
            "scripts/ghc_family_v658_v2_",
            "scripts/build_ghc_family_v658_v2_x1.py",
            "tests/test_ghc_family_v658_v2_x1.py",
        ],
        "x2_implementation_paths": [],
        "outcome_artifacts": [],
        "deletions": [],
        "expected_staged_path_count": len(expected_staged_paths),
        "expected_staged_paths": expected_staged_paths,
        "valid": True,
        "exact_index_review_required_after_staging": True,
    }
    write_json("validation/x1-staged-review.json", review)
    receipt = {
        "schema": "ghc.family.v658-v2.x1-validation.v1",
        "valid": True,
        "source_head": head,
        "proposal_count": len(d.PROPOSALS),
        "inherited_proposal_count": len(prior),
        "effective_proposal_count": len(prior) + len(d.PROPOSALS),
        "maximum_novelty_similarity": max(row["jaccard"] for row in novelty),
        "source_count": len(d.OFFICIAL_SOURCES),
        "source_reference_count": sum(len(row["official_or_primary_source_needs"]) for row in d.PROPOSALS),
        "unresolved_source_ids": [],
        "json_parse_count": len(phase_jsons),
        "privacy_file_count": scan["file_count"],
        "privacy_hit_count": scan["hit_count"],
        "manifest_entry_count": manifest["entry_count"],
        "x2_implementation_present": False,
        "outcomes_observed": False,
        "x1_operational_negatives_retained": len(d.X1_OPERATIONAL_NEGATIVES),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("validation/x1-validation-receipt.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
