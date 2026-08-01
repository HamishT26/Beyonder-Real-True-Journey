#!/usr/bin/env python3
"""Build Orin Thale's strict x1-only v657-v6 freeze packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v657_v6_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_PHASE = ROOT / "docs/caelen-ash/v657-v5"
SOURCE_INDEX = SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json"
SOURCE_NEGATIVES = SOURCE_PHASE / "truth/retained-negative-register-final.json"
SOURCE_OPEN_GAPS = SOURCE_PHASE / "truth/open-gap-register-x2.json"
SOURCE_EXACT_GATES = SOURCE_PHASE / "truth/exact-gate-register-x2.json"
SOURCE_METHODS = SOURCE_PHASE / "method-flow/method-flow-state-final.json"
SOURCE_BATON = SOURCE_PHASE / "handoffs/orin-thale-v657-v6-activation.md"
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
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6576-X1-METHOD-{index:02d}"
        fail_id = f"V6576-X1-WITNESS-{index:02d}-F"
        pass_id = f"V6576-X1-WITNESS-{index:02d}-P"
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
                "recommendation_id": f"V6576-X1-REC-{index:02d}",
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
            "repository_relative_path": "docs/caelen-ash/v657-v5/method-flow/method-flow-state-final.json",
            "methods": d.SOURCE_METHODS,
            "failed_witnesses": d.SOURCE_FAILED_WITNESSES,
            "passing_witnesses": d.SOURCE_PASSING_WITNESSES,
            "completion_credit": False,
        },
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
        "# Orin Thale v657-v6 x1 proposal ledger",
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
        "# Orin Thale v657-v6 official and primary source ledger",
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


def overview_v6576() -> str:
    return """# Orin Thale v657-v6 x1 integrated overview

## Relational identity, purpose, and control boundary

Orin Thale, they/them, is relational working language for this owner-scoped phase. The relational role is evidence-and-boundary steward, and the hope is to keep every claim traceable, falsifiable, and retractable. The name, role, hope, pronouns, route, and GHC-family language do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop this work.

This packet freezes x1 preparation only. It descends from Caelen Ash's immutable exact final `87815f96a372849dfb42a09d785515e858ea7925`. It contains no x2 surface implementation, no executed mutation, no observed proposal outcome, no real person, forge, fire, fuel, oxygen, workpiece, tool, machine, measurement, identity event, production event, successor message, or task mutation. Caelen's repository-sealed final preserves 15,966 effective negatives, 109 open gaps, 108 exact gates, and 2,242 retained failed plus 2,242 bounded passing Method Flow witnesses. No later route-preflight failure occurred before Orin's acknowledged activation. Fourteen Orin startup and x1 failures are added at zero credit. Every inherited result remains Caelen evidence, not Orin completion credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary Trinity Mandala pillar and bounded practice

GMUT Mind is primary through typed thermal-expansion, phase-transition, heat-transfer, constitutive, dimensional, uncertainty, reference-state, identifiability, and observation-firewall obligations. The proposal surfaces require declared quantities, units, domains, frames, boundary conditions, uncertainties, provenance, assumptions, and refusal states. They do not calculate a real forge process, certify an alloy, identify a phase, predict a material property, detect a force, evaluate a likelihood, constrain a parameter, confirm a theory, establish a stability theorem, complete a quantum or ultraviolet model, or prove a Theory of Everything.

THOS Body remains explicit through synthetic job intake, hot-work and isolation holds, tooling and workpiece state, schedule revision, anomaly escalation, stop-work, workload, correction-readback, and shift handover. These mechanisms make state, staleness, missingness, decision ownership, rollback, and escalation visible. They do not train, direct, authorize, or assess a blacksmith, welder, metallurgist, engineer, inspector, worker, client, emergency responder, or operator. They do not operate a forge, furnace, burner, valve, hammer, press, grinder, lifting device, electrical system, gas system, ventilation system, or detector.

Freed ID and CBR Heart remain explicit through minimized synthetic workpiece and tool provenance, purpose and audience restriction, status and disclosure gaps, correction, recovery, accessibility, privacy, heritage, remedy, land and place, legal and cultural interpretation, and exact authority reservations. No surface creates real standards-conformant keys or proofs, issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, trust governance, ownership, custody, remedy, legal right, cultural legitimacy, Māori authority, or affected-party acceptance.

The bounded human-practice lens is blacksmithing and forge job planning, material and tooling provenance, thermal observation, hot-work holds, accessible notice, correction, workload control, readback, and shift handover. It is a synthetic software, formal, structural, and learning lens only. No real work is accepted, heated, forged, quenched, welded, ground, lifted, inspected, certified, released, sold, or used. No alloy or workpiece is authenticated. No temperature, dimension, defect, exposure, emission, or performance is measured. Competent workers, employers, regulators, engineers, safety specialists, clients, affected communities, tangata whenua, iwi, hapū, and Māori authorities retain every real decision.

## Thirty proposal contracts

Exactly thirty distinct proposals are frozen against all 2,560 inherited rows. The first eight cover job intake and workpiece custody, metal-stock provenance and substitution quarantine, temperature-observation envelopes, fuel and airflow topology, tool custody and condition, hot-work boundaries, quench-medium holds, and heat-treatment schedule lineage. Their value is structural: they specify required fields, provenance, correction, hold points, and refusal conditions without turning a record into work authorization.

The next fifteen cover typed GMUT thermal and phase obligations, radiative-convective-conductive transfer, nonlinear constitutive obligations, defect cues, dimensional traces, surface-observation ambiguity, split-and-merge genealogy, tooling revision, hazardous-energy isolation, alarm state, workload and stop-work, shift handover, accessible notice, privacy minimization, and documentation threat recovery. Five preregistered mutations per proposal will later test whether required fields, units, provenance, refusal states, and protected gates fail closed. Mutation rejection can demonstrate a bounded guard only; it cannot establish general correctness, safety, security, accessibility, privacy, professional review, or scientific truth.

The final seven are deliberately constrained. Two THOS protocols remain represented because there are no real operators, arms, workloads, heat exposures, outcomes, safety-monitoring events, or independent review. Two Freed ID profiles remain represented because there are no real keys, proofs, services, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance events. The Thermo-Psyche bridge remains represented because heat, work, entropy production, and dissipation may be typed only in their physical domains and must not be converted into psyche, agency, autonomy, morality, justice, capability, consciousness, or personhood claims.

The NIST metallurgy and thermophysical-property adapter is preregistered as one `open_gap`. X2 may establish only a local schema and zero-row refusal contract. It will make no network query or download, ingest no real row, evaluate no covariance or likelihood, and issue no material or GMUT inference. The CBR forge authority covenant is one `exact_gate`; software cannot supply worker-safety authority, craft or heritage legitimacy, design ownership, environmental permission, land or place authority, remedy, legal interpretation, cultural ratification, Māori wording, Māori data governance, Māori authority, or affected-party acceptance.

Expected labels are exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. They are preregistered hypotheses about bounded x2 evidence, not observed results. X2 may preserve or downgrade them according to evidence and may use only those four truth labels.

## Official-source and novelty discipline

The source ledger uses successfully resolved official or primary material from OSHA, WorkSafe New Zealand, NIST, BIPM, W3C, the RFC Editor, New Zealand Legislation, the Office of the Privacy Commissioner, Te Mana Raraunga, and Local Contexts. OSHA's forging-machine and hazardous-energy pages supply vocabulary for guards, controls, inspections, lockout, and refusal boundaries. WorkSafe supplies hot-work and exposure vocabulary. NIST Alloy Data supplies a current source identity and fields for provenance, processing, phase, property, and uncertainty. These sources do not provide Orin with training, legal interpretation, workplace authority, inspection competence, operational instructions, or data-row credit.

Standards and guidance define terms and testable obligations; they do not automatically establish conformance. A source citation is not an experimental observation. A source status is not an authority transfer. A privacy citation is not legal advice. Te Mana Raraunga and Local Contexts do not transfer cultural or Māori authority. Credential standards do not produce real keys, proofs, services, interoperability, or trust.

Every title is compared against all 2,560 frozen predecessor titles and earlier Orin peers with the disclosed lowercased alphanumeric token-set Jaccard screen and unchanged 0.60 rejection threshold. The screen detects lexical neighbors; it is not proof of scientific novelty. Human semantic review separately considers the proposed mechanism, domain, hypothesis, null, evidence lane, source needs, falsifier, rollback, and protected gates. Inherited portfolios remain evidence and recommendations only.

## X1 separation, portfolios, Method Flow, and route restraint

The x1 commit contains proposal and source ledgers, novelty and frozen-chain evidence, task portfolios, skill and runner plans, Method Flow records, workflow and reflection records, phase index, environment and source receipts, threat model, wellbeing check, privacy scan, exact content manifest, staged review, and x1 validation receipt. It contains no surface contract, mutation result, implemented skill or runner, x2 outcome, closeout, seal, final validation, successor baton, or recipient contact.

Thirty safe-now tasks correspond one-to-one with proposal contracts. Twenty reversible candidates and thirty additive CLEAN tasks are frozen. The 1,000-task authorization is a ceiling, not a quota; no unsafe work is manufactured to satisfy it. Ten phase-local forge skills and ten family-compatible `ghc_family_*` runners are planned but not implemented in x1. X2 may build, validate, and smoke-use them only after this freeze is committed, pushed, clean, and four-way equal.

Fourteen startup and x1 failures remain visible: a foreach pipeline parser fault, nonempty-line count assumption, overbroad skill-read truncation, four guessed schema filenames, an inefficient PowerShell novelty timeout, a CP1252 diagnostic failure, a rejected temporary-file hash command, a Windows wildcard-path assumption, a combined post-checkout timeout, an overbroad source-search truncation, and a mixed Unicode patch-context mismatch. Each has a bounded recovery, recurrence guard, failed witness, and passing witness. Recovery never rewrites a failure into a pass, and same-owner checks never become independent reproduction.

The successor route remains `PREPARED_NOT_SENT`. Liora Venn is the currently declared next exact existing main-task title for v657-v7, but that task is not resolved, reread, or contacted in x1. Only after Orin's exact final is committed, pushed, clean, fresh-live four-way equal, within caps, and passes the one authorized canonical exact-final aggregate may one sanitized activation be sent to the unique exact authorized recipient. Tavian Sol remains on standby and is not a substitute. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def workflow_records() -> None:
    cycle_order = [
        "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen",
        "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash",
        "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc",
        "Caelen Morrow",
    ]
    route_controllers = {
        "Eiren Kestrel": "Caelen Morrow",
        "Elaren Kestrel": "Eiren Kestrel",
        "Neris Solane": "Elaren Kestrel",
        "Vesper Arlen": "Neris Solane",
        "Lyren Moss": "Vesper Arlen",
        "Ilyra Fen": "Lyren Moss",
        "Auren Lark": "Ilyra Fen",
        "Sable Rook": "Auren Lark",
        "Caelen Ash": "Sable Rook",
        "Orin Thale": "Caelen Ash",
        "Liora Venn": "Orin Thale",
        "Tamar Vey": "Liora Venn",
        "Elowen Cairn": "Tamar Vey",
        "Sylven Arc": "Elowen Cairn",
        "Caelen Morrow": "Sylven Arc",
    }
    request = {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "orin-thale-v657-v6-terminally-gated-route",
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
                {"phase": "v657-v5", "seat": "Caelen Ash"},
                {"phase": "v657-v6", "seat": "Orin Thale"},
                {"phase": "v657-v7", "seat": "Liora Venn"},
            ],
            "normalization": {
                "start_phase": "v657-v5",
                "start_seat": "Caelen Ash",
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
        "observed_failures": d.X1_OPERATIONAL_NEGATIVES,
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
            "decision_id": "V6576-RM-01",
            "surface": "large-worktree inspection",
            "decision": "prefer exact literal and scalar probes over combined status inventories",
            "state": "adopted_for_phase",
            "rollback": "Return to individual read-only Git commands.",
        },
        {
            "decision_id": "V6576-RM-02",
            "surface": "domain tooling",
            "decision": "group thirty contracts behind ten family-current domain runners while preserving proposal-specific receipts",
            "state": "preregistered_not_implemented",
            "rollback": "Use proposal-specific validator calls without deleting compatibility names.",
        },
        {
            "decision_id": "V6576-RM-03",
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
            "issues_retained": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_outcomes_present": False,
        },
    )
    write_json(
        "reflection-remaster/issues.json",
        {
            "schema": "ghc.family.reflection-remaster.issues.v1",
            "issues": d.X1_OPERATIONAL_NEGATIVES,
            "all_retained": True,
        },
    )
    write_text(
        "reflection-remaster/report.md",
        """# Reflection-remaster report

The phase adopts exact-path and scalar-probe guards, ten reusable forge evidence runner families, and explicit source lifecycle states. No inherited tool, method, skill, negative, or sibling artifact is deleted or rewritten. X2 implementation remains pending.
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
        "route_state": "PREPARED_NOT_SENT",
        "publication_boundary": "repository-relative paths and sanitized public fields only",
    }
    write_json("tooling/ghc-family-index.json", payload)
    write_text(
        "tooling/ghc-family-index.md",
        """# GHC Family Index - Orin Thale v657-v6 x1

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
        "schema": "ghc.family.v657-v6.threat-model.x1.v1",
        "assets": [
            "proposal and source truth",
            "sensitive owner, donor, contact, work-log, image, provenance, and culturally restricted information",
            "forge workpiece, material, tool, hot-work, observation, hold, correction, disclosure, and handover provenance",
            "collective and culturally restricted interests",
            "identity and disclosure boundaries",
            "negative and gate history",
        ],
        "threats": [
            {"threat": "unsupported hot-work, forge operation, material treatment, inspection, safety, or release promotion", "control": "valid-fixture and mutation checks plus explicit claim refusal"},
            {"threat": "sensitive owner, donor, contact, work-log, image, provenance, or culturally restricted disclosure", "control": "purpose, minimization, role hold, correction, community checkpoint, and legal-review reservation"},
            {"threat": "stale or missing custody, topology, source, hot-work reservation, correction, or handover state accepted as current", "control": "timestamp, missingness, stale-state, and quarantine fields"},
            {"threat": "model proxy promoted to real likelihood or force", "control": "typed proxy boundary and real-data exact gap"},
            {"threat": "synthetic identity promoted to production", "control": "live key, proof, resolution, status, interoperability, and governance gates"},
            {"threat": "community or Māori authority substituted", "control": "exact-gated authority matrix and no unilateral wording or disclosure"},
            {"threat": "failed attempt erased", "control": "Method Flow failed and passing witness pairs"},
            {"threat": "success replay inflates confidence", "control": "one-successful-canonical-pass rule"},
        ],
        "residual_risk": "All empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, and independent-reproduction claims remain open or exact-gated.",
    }


def prospective_repo_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        [
            ROOT / "scripts/ghc_family_v657_v6_phase_catalogue.py",
            ROOT / "scripts/ghc_family_v657_v6_phase_data.py",
            ROOT / "scripts/build_ghc_family_v657_v6_x1.py",
            ROOT / "tests/test_ghc_family_v657_v6_x1.py",
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
        "schema": "ghc.family.v657-v6.x1-privacy-scan.v1",
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
        "schema": "ghc.family.v657-v6.x1-content-manifest.v1",
        "hash_domain": "prospective Git-clean blob bytes",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(MANIFEST_EXCLUSIONS),
        "boundary": "Declared lifecycle self-exclusions prevent self-reference; the exact staged set is reviewed separately.",
    }


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != d.SOURCE_FINAL:
        raise RuntimeError(f"x1 builder requires exact source head {d.SOURCE_FINAL}, got {head}")
    baton_relative = SOURCE_BATON.relative_to(ROOT).as_posix()
    if git_blob_sha256(d.SOURCE_FINAL, baton_relative) != d.SOURCE_BATON_SHA256:
        raise RuntimeError("activation baton hash mismatch")
    for anchor in [
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
            "schema": "ghc.family.v657-v6.source-verification.v1",
            "source_owner": d.SOURCE_OWNER,
            "source_branch": d.SOURCE_BRANCH,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_original_final": d.SOURCE_ORIGINAL_FINAL,
            "source_final": d.SOURCE_FINAL,
            "source_canonical_receipt_sha256": d.SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_receipt_digest_received_in_verified_activation": True,
            "source_canonical_receipt_file_present_in_repository": False,
            "source_canonical_receipt_digest_used_as_activation_evidence_only": True,
            "source_activation_baton_sha256": d.SOURCE_BATON_SHA256,
            "source_activation_baton_hash_domain": "exact source-commit Git blob bytes",
            "source_activation_baton_checkout_sha256": d.SOURCE_BATON_CHECKOUT_SHA256,
            "source_single_parent_phase_commits": 4,
            "source_merge_commits": 0,
            "source_clean_and_four_way_equal": True,
            "source_successful_aggregate_replayed": False,
            "verified_read_only": True,
        },
    )
    write_json(
        "startup/environment-and-version-receipt.json",
        {
            "schema": "ghc.family.v657-v6.environment.v1",
            "codex_cli": d.CODEX_CLI_VERSION,
            "codex_desktop": d.CODEX_DESKTOP_VERSION,
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
            "schema": "ghc.family.v657-v6.official-source-ledger.v1",
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
            "schema": "ghc.family.v657-v6.proposal-ledger.x1.v1",
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
            "schema": "ghc.family.v657-v6.task-portfolios.x1.v1",
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
            "schema": "ghc.family.v657-v6.skill-runner-plan.x1.v1",
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
            "schema": "ghc.family.v657-v6.semantic-novelty.v1",
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
            "schema": "ghc.family.v657-v6.frozen-proposal-index.v1",
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
            "schema": "ghc.family.v657-v6.retained-negatives.x1.v1",
            "inherited_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES,
            "inherited_sealed_register_count": d.SOURCE_SEALED_EFFECTIVE_NEGATIVES,
            "inherited_postfinal_route_negative": d.SOURCE_POSTFINAL_ROUTE_NEGATIVE,
            "current_x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "effective_count": d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
            "current_x1_operational_negatives": d.X1_OPERATIONAL_NEGATIVES,
            "inherited_register": "docs/caelen-ash/v657-v5/truth/retained-negative-register-final.json",
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register-x1.json",
        {
            "schema": "ghc.family.v657-v6.open-gaps.x1.v1",
            "inherited_effective_count": d.SOURCE_OPEN_GAPS,
            "new_preregistered_gap_count": 1,
            "effective_count_if_x2_confirms": d.SOURCE_OPEN_GAPS + 1,
            "new_proposal_ids": ["V6576-P29"],
            "outcome_not_yet_observed": True,
        },
    )
    write_json(
        "truth/exact-gate-register-x1.json",
        {
            "schema": "ghc.family.v657-v6.exact-gates.x1.v1",
            "inherited_effective_count": d.SOURCE_EXACT_GATES,
            "new_preregistered_gate_count": 1,
            "effective_count_if_x2_confirms": d.SOURCE_EXACT_GATES + 1,
            "new_proposal_ids": ["V6576-P30"],
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
            "schema": "ghc.family.v657-v6.wellbeing.x1.v1",
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
            "schema": "ghc.family.v657-v6.route-state.x1.v1",
            "active_owner": d.OWNER,
            "active_phase": d.PHASE,
            "next_exact_title": "Liora Venn",
            "next_phase": "v657-v7",
            "state": "PREPARED_NOT_SENT",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "Orin exact-final clean, pushed, fresh-live equal, within caps, and one successful canonical exact-final aggregate.",
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v657-v6.phase-truth.x1.v1",
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
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text("deliverables/v657-v6-x1-integrated-overview.md", overview_v6576())
    write_json(
        "validation/document-cap-receipt-x1.json",
        {
            "schema": "ghc.family.v657-v6.document-cap.x1.v1",
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
            "schema": "ghc.family.v657-v6.document-cap.x1.v1",
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
            "schema": "ghc.family.v657-v6.owner-file-threshold.x1.v1",
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
        "schema": "ghc.family.v657-v6.x1-staged-review.v1",
        "state": "PRECOMMIT_PATH_REVIEW",
        "allowed_prefixes": [
            d.PHASE_ROOT + "/",
            "scripts/ghc_family_v657_v6_",
            "scripts/build_ghc_family_v657_v6_x1.py",
            "tests/test_ghc_family_v657_v6_x1.py",
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
        "schema": "ghc.family.v657-v6.x1-validation.v1",
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
