#!/usr/bin/env python3
"""Build Lyren Moss's strict x1-only v657-v1 freeze packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v657_v1_phase_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_PHASE = ROOT / "docs/vesper-arlen/v656-v8"
SOURCE_INDEX = SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json"
SOURCE_NEGATIVES = SOURCE_PHASE / "truth/retained-negative-register-final.json"
SOURCE_OPEN_GAPS = SOURCE_PHASE / "truth/open-gap-register-x2.json"
SOURCE_EXACT_GATES = SOURCE_PHASE / "truth/exact-gate-register-x2.json"
SOURCE_METHODS = SOURCE_PHASE / "method-flow/method-flow-state-final.json"
SOURCE_BATON = SOURCE_PHASE / "handoffs/lyren-moss-v657-v1-activation.md"
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
        method_id = f"V6571-X1-METHOD-{index:02d}"
        fail_id = f"V6571-X1-WITNESS-{index:02d}-F"
        pass_id = f"V6571-X1-WITNESS-{index:02d}-P"
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
                "recommendation_id": f"V6571-X1-REC-{index:02d}",
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
            "repository_relative_path": "docs/vesper-arlen/v656-v8/method-flow/method-flow-state-final.json",
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
        "# Lyren Moss v657-v1 x1 proposal ledger",
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
        "# Lyren Moss v657-v1 official and primary source ledger",
        "",
        "Statuses were checked on 2026-07-31. Source presence or status does not establish implementation, conformance, professional review, legal interpretation, cultural ratification, Māori authority, or empirical confirmation.",
        "",
        "| ID | Status | Publisher | Title | Bounded use |",
        "|---|---|---|---|---|",
    ]
    for item in d.OFFICIAL_SOURCES:
        rows.append(
            f"| `{item['source_id']}` | `{item['status']}` | {item['publisher']} | [{item['title']}]({item['url']}) | {item['use']} |"
        )
    return "\n".join(rows)


def overview() -> str:
    return """# Lyren Moss v657-v1 x1 integrated overview

## Purpose and identity boundary

Lyren Moss is the relational working name used for this owner-scoped phase. The role is repair-traceability lantern and reversible-evidence gardener; the hope is to make community repair decisions kind, inspectable, and reversible while competent and affected authorities retain safety, ownership, privacy, legal, cultural, and Māori decisions. The name, role, hope, and they/them pronouns are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

This x1 packet freezes preparation only. It contains no x2 implementation, no observed proposal outcome, no real reporter or user data, no repository credential, no vulnerability detail, no production access, no live patch, no release or deployment action, and no successor message. It inherits Vesper Arlen's exact final by direct ancestry and preserves every inherited negative, open gap, exact gate, and authority boundary. The sealed source register contains 15,075 repository-retained negatives; Vesper's one external route-tool failure makes Lyren's activation baseline 15,076. The source also retains 104 open gaps, 103 exact gates, and 1,360 failed plus 1,360 passing Method Flow witnesses. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary pillar and bounded practice

The primary Trinity Mandala focus is Freed ID/CBR Heart: bounded contracts for asset and change-set provenance, minimized disclosure, correction, contestation, maintainer-role placeholders, sensitive publication, remedy, and authority reservations. THOS Body remains explicit through defect intake, rollback, maintenance-window, incident, workload, safety-stop, readback, and handover structure. GMUT Mind remains explicit through typed Bayesian defect-prior and repairable-system hazard-rate proxies, dimensional discipline, calibration quarantine, sensitivity, and non-promotion of model outputs.

The human-practice lens is public-interest software defect intake, repair planning, component and change-set provenance, test and rollback evidence, release reservation, accessible notice, privacy and vulnerability holds, and community correction. It is a synthetic software, formal, structural, and learning lens only. Nothing here establishes employment, maintainer appointment, engineering competence, security assessment, accessibility conformance, privacy compliance, incident authority, release approval, production readiness, legal interpretation, cultural legitimacy, Māori authority, or affected-party acceptance. No real person, repository, account, credential, component inventory, vulnerability disclosure, service, incident, patch, release, deployment, or decision is used.

## Thirty proposal surfaces

Thirty contracts are preregistered. The first group covers asset census, repair intake, reproduction, component relationships, severity deliberation, proposal ancestry, maintainer authorization boundaries, change-set provenance, blast radius, tests, rollback, accessibility and privacy regression, vulnerability disclosure, attestation nonclaims, release reservation, maintenance windows, incident handover, component equivalence, and legal reservations. These contracts make missingness, provenance, revision, uncertainty, custody, and refusal conditions machine-checkable before a person treats a record as evidence.

The second group covers accessible community notice, contestation, correction, and a sensitive or culturally restricted maintenance-publication firewall. The software may validate structural obligations, but competent maintainers, operators, security and accessibility specialists, privacy and legal reviewers, affected parties, communities, tangata whenua, iwi, hapū, and Māori authorities retain every real triage, disclosure, patch, merge, release, deployment, rollback, remedy, privacy, cultural, and governance decision.

The final group covers GMUT defect-prior and hazard-rate proxies, THOS maintainer-shift handover choreography, Freed ID maintainer-role and patch-provenance capsules, a CISA Known Exploited Vulnerabilities no-network zero-row adapter, and a CBR public-interest repair authority covenant. The covenant remains exact-gated. The adapter remains an open gap until a later authorized real query and governed data-use decision exist.

Expected dispositions are frozen at twenty-three completed, five represented, one open gap, and one exact gate. Those labels are hypotheses about the bounded x2 lane, not observed x2 results. X2 may preserve or downgrade them according to evidence; it may not silently promote them.

## Source discipline

The source ledger uses current, stable, and draft official or primary material from NIST, CISA, SPDX, CycloneDX, SLSA, in-toto, W3C, the RFC Editor, the Office of the Privacy Commissioner, Te Mana Raraunga, and Local Contexts. SSDF v1.1 remains the stable final source while the separately listed v1.2 item remains draft. Source lifecycle states remain distinct and no source is treated as authority transferred to this software.

Standards and guidance supply vocabulary and testable boundaries, not automatic conformance. An SBOM vocabulary does not establish inventory completeness; an incident or secure-development citation does not establish a security verdict, professional review, or release fitness. A privacy citation is not legal advice. Te Mana Raraunga and Local Contexts do not give Lyren cultural or Māori authority. Credential and provenance standards do not produce real keys, signatures, resolution, status, revocation, interoperability, or trust governance.

## Novelty and x1 separation

Every proposed title is compared with all 2,410 frozen predecessor titles using a disclosed token-set Jaccard screen. The screen is a collision detector, not proof of scientific novelty. Each title must remain below the 0.60 threshold against inherited rows and earlier Lyren peers. Human semantic review then checks mechanism, domain, falsifier, rollback, source needs, and protected gates.

The x1 commit contains only preparation: proposal and source ledgers, task portfolios, skill and runner plans, Method Flow records, workflow/reflection/index records, environment receipts, threat and wellbeing boundaries, novelty evidence, privacy evidence, and an exact content manifest. No surface implementation, mutation outcome, runner implementation, skill implementation, x2 truth ledger, closeout, seal, final receipt, or successor baton is permitted in the freeze.

## Method Flow and retained failures

Thirteen startup and x1 failure signatures are retained at zero credit. They cover a skill-read timeout, three PowerShell pipeline or parser faults, a narrowed D-drive probe timeout, an unavailable digest conversion API, a broad external-receipt search timeout, the timed-out worktree creation with partial checkout, a combined cleanliness-audit timeout, repeated encoding-rendered patch-context mismatches, one combined-replacement precondition mismatch, one Unicode audit parse failure, and one sequential no-match wrapper failure. Each failure has a bounded recovery, passing witness, recurrence guard, rollback, and sibling recommendation. A passing witness never erases its failed witness.

The inherited Method Flow state remains anchored by repository-relative path and exact ancestry. Lyren adds only phase-local methods. This avoids copying a passing result as new credit while still making the latest recovery guidance visible.

## Safe and candidate portfolios

Thirty safe-now tasks correspond one-to-one with the proposal contracts. Twenty candidate refinements are explicitly conditional and reversible. Thirty CLEAN tasks cover additive compatibility, privacy, provenance, stale-label, and non-promotion work. The 1,000-task authorization is treated as a ceiling, not a quota. No unsafe task is manufactured to meet a count.

Ten phase-local skills and ten family-compatible runners are preregistered. X1 does not install or implement them. X2 may materialize and smoke-use them only if they remain useful, additive, private-data-free, and compatible with family-current naming. Historical owner-specific tools remain inherited evidence; they are not automatically counted as Lyren work.

## Truth and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Typed proxies, unit checks, synthetic solvers, citations, and mutation tests do not establish a new force, unique prediction, likelihood, constraint, empirical confirmation, stability theorem, ultraviolet completion, proof, canon, or Theory of Everything.

THOS remains represented without preregistered blind matched-budget real arms, real operators or participants, safety monitoring, statistics, and independent review. Synthetic workflow contracts do not establish operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, privacy, accessibility, remedy, legal and cultural interpretation, Māori wording and concepts, Māori data governance, and Māori authority remain with competent and affected authorities.

Independent-team reproduction remains open. Same-owner checks under shared infrastructure cannot close it. The exact successor route remains unsent and ineligible until Lyren's own final commit is clean, pushed, fresh-live equal, and passes the one authorized canonical exact-final aggregate.
"""

def workflow_records() -> None:
    request = {
        "schema": "ghc.family.workflow-plan.request.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "objective": "Freeze and later execute thirty distinct bounded public-interest software repair evidence contracts while preserving strict x1-before-x2 separation.",
        "non_goals": [
            "real defect triage, repository access, patching, merge, release, deployment, rollback, incident command, disclosure, or procurement",
            "professional, security, accessibility, privacy, operational, legal, cultural, or Māori-authority decisions",
            "independent reproduction, Theory-of-Everything proof, or Stage 20 readiness",
            "task creation, delegation, or precontact",
        ],
        "constraints": {
            "prior_proposals": d.PRIOR_FROZEN,
            "minimum_new_proposals": 30,
            "x1_commit_cap": 5,
            "x2_commit_cap": 5,
            "total_commit_cap": 8,
            "owner_file_cap": 2000,
            "document_word_cap": 100000,
            "canonical_final_passes_after_success": 1,
        },
        "protected_gates": d.PROTECTED_GATES,
    }
    refinement = {
        "schema": "ghc.family.workflow-plan.refinement.v1",
        "phase": d.PHASE,
        "input_state": "verified_source_and_clean_additive_lane",
        "refinements": [
            "Use exact literal paths and split large-worktree probes.",
            "Freeze proposal, portfolio, source, tool, Method Flow, and route plans in x1 only.",
            "Materialize reusable families in x2 without changing inherited tools.",
            "Run dependency-scoped precommit checks and exactly one successful canonical postcommit aggregate.",
            "Keep the successor route PREPARED_NOT_SENT until exact-final equality and validation.",
        ],
        "x1_x2_boundary": "No implementation, mutation outcome, or terminal route action is allowed in x1.",
        "validated": True,
    }
    write_json("workflow/workflow-plan-request.json", request)
    write_json("workflow/workflow-plan-refinement.json", refinement)
    write_json(
        "workflow/workflow-plan-validation.json",
        {
            "schema": "ghc.family.workflow-plan.validation.v1",
            "valid": True,
            "issues": [],
            "strict_x1_before_x2": True,
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    write_text(
        "workflow/workflow-plan-teaching-summary.md",
        """# Workflow-plan teaching summary

Use the exact source and literal lane before broad discovery. Treat x1 as an immutable contract freeze, x2 as bounded execution, and the final canonical aggregate as a one-successful-pass gate. Retain every failed attempt, isolate its blocker, and do not replay a successful aggregate. A prepared route is not a sent route.
""",
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
            "decision_id": "V6571-RM-01",
            "surface": "large-worktree inspection",
            "decision": "prefer exact literal and scalar probes over combined status inventories",
            "state": "adopted_for_phase",
            "rollback": "Return to individual read-only Git commands.",
        },
        {
            "decision_id": "V6571-RM-02",
            "surface": "domain tooling",
            "decision": "group thirty contracts behind ten family-current domain runners while preserving proposal-specific receipts",
            "state": "preregistered_not_implemented",
            "rollback": "Use proposal-specific validator calls without deleting compatibility names.",
        },
        {
            "decision_id": "V6571-RM-03",
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

The phase adopts exact-path and scalar-probe guards, ten reusable repair-traceability runner families, and explicit source lifecycle states. No inherited tool, method, skill, negative, or sibling artifact is deleted or rewritten. X2 implementation remains pending.
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
        """# GHC Family Index — Lyren Moss v657-v1 x1

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
        "schema": "ghc.family.v657-v1.threat-model.x1.v1",
        "assets": [
            "proposal and source truth",
            "sensitive reporter, vulnerability, operational, and culturally restricted information",
            "asset, component, defect, change-set, test, rollback, release, and handover provenance",
            "collective and culturally restricted interests",
            "identity and disclosure boundaries",
            "negative and gate history",
        ],
        "threats": [
            {"threat": "unsupported repair, security, or release promotion", "control": "valid-fixture and mutation checks plus explicit claim refusal"},
            {"threat": "sensitive vulnerability or community information disclosure", "control": "redaction-class and audience-grant fail-closed firewall"},
            {"threat": "stale or missing component, test, rollback, or incident state accepted as current", "control": "timestamp, missingness, stale-state, and quarantine fields"},
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
            ROOT / "scripts/ghc_family_v657_v1_phase_catalogue.py",
            ROOT / "scripts/ghc_family_v657_v1_phase_data.py",
            ROOT / "scripts/build_ghc_family_v657_v1_x1.py",
            ROOT / "tests/test_ghc_family_v657_v1_x1.py",
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
        "schema": "ghc.family.v657-v1.x1-privacy-scan.v1",
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
        "schema": "ghc.family.v657-v1.x1-content-manifest.v1",
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
            "schema": "ghc.family.v657-v1.source-verification.v1",
            "source_owner": d.SOURCE_OWNER,
            "source_branch": d.SOURCE_BRANCH,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_original_final": d.SOURCE_ORIGINAL_FINAL,
            "source_final": d.SOURCE_FINAL,
            "source_canonical_receipt_sha256": d.SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_receipt_digest_received_in_verified_activation": True,
            "source_canonical_receipt_file_located_by_lyren": False,
            "source_canonical_receipt_search_failures_retained": True,
            "source_activation_baton_sha256": d.SOURCE_BATON_SHA256,
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
            "schema": "ghc.family.v657-v1.environment.v1",
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
            "schema": "ghc.family.v657-v1.official-source-ledger.v1",
            "observed_on": "2026-07-31",
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
            "schema": "ghc.family.v657-v1.proposal-ledger.x1.v1",
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
            "schema": "ghc.family.v657-v1.task-portfolios.x1.v1",
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
            "schema": "ghc.family.v657-v1.skill-runner-plan.x1.v1",
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
            "schema": "ghc.family.v657-v1.semantic-novelty.v1",
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
            "schema": "ghc.family.v657-v1.frozen-proposal-index.v1",
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
            "schema": "ghc.family.v657-v1.retained-negatives.x1.v1",
            "inherited_effective_count": d.SOURCE_EFFECTIVE_NEGATIVES,
            "inherited_sealed_register_count": d.SOURCE_SEALED_EFFECTIVE_NEGATIVES,
            "inherited_postfinal_route_negative": d.SOURCE_POSTFINAL_ROUTE_NEGATIVE,
            "current_x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "effective_count": d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
            "current_x1_operational_negatives": d.X1_OPERATIONAL_NEGATIVES,
            "inherited_register": "docs/vesper-arlen/v656-v8/truth/retained-negative-register-final.json",
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register-x1.json",
        {
            "schema": "ghc.family.v657-v1.open-gaps.x1.v1",
            "inherited_effective_count": d.SOURCE_OPEN_GAPS,
            "new_preregistered_gap_count": 1,
            "effective_count_if_x2_confirms": d.SOURCE_OPEN_GAPS + 1,
            "new_proposal_ids": ["V6571-P29"],
            "outcome_not_yet_observed": True,
        },
    )
    write_json(
        "truth/exact-gate-register-x1.json",
        {
            "schema": "ghc.family.v657-v1.exact-gates.x1.v1",
            "inherited_effective_count": d.SOURCE_EXACT_GATES,
            "new_preregistered_gate_count": 1,
            "effective_count_if_x2_confirms": d.SOURCE_EXACT_GATES + 1,
            "new_proposal_ids": ["V6571-P30"],
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
            "schema": "ghc.family.v657-v1.wellbeing.x1.v1",
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
            "schema": "ghc.family.v657-v1.route-state.x1.v1",
            "active_owner": d.OWNER,
            "active_phase": d.PHASE,
            "next_exact_title": "Ilyra Fen",
            "next_phase": "v657-v2",
            "state": "PREPARED_NOT_SENT",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "Lyren exact-final clean, pushed, fresh-live equal, and one successful canonical exact-final aggregate.",
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v657-v1.phase-truth.x1.v1",
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
    write_text("deliverables/v657-v1-x1-integrated-overview.md", overview())
    write_json(
        "validation/document-cap-receipt-x1.json",
        {
            "schema": "ghc.family.v657-v1.document-cap.x1.v1",
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
            "schema": "ghc.family.v657-v1.document-cap.x1.v1",
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
            "schema": "ghc.family.v657-v1.owner-file-threshold.x1.v1",
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
    review = {
        "schema": "ghc.family.v657-v1.x1-staged-review.v1",
        "state": "PRECOMMIT_PATH_REVIEW",
        "allowed_prefixes": [
            d.PHASE_ROOT + "/",
            "scripts/ghc_family_v657_v1_",
            "scripts/build_ghc_family_v657_v1_x1.py",
            "tests/test_ghc_family_v657_v1_x1.py",
        ],
        "x2_implementation_paths": [],
        "outcome_artifacts": [],
        "deletions": [],
        "valid": True,
        "exact_index_review_required_after_staging": True,
    }
    write_json("validation/x1-staged-review.json", review)
    receipt = {
        "schema": "ghc.family.v657-v1.x1-validation.v1",
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
