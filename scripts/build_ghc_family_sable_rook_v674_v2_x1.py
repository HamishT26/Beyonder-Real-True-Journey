#!/usr/bin/env python3
"""Build Sable Rook v674-v2 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sable Rook"
PHASE = "v674-v2"
SOURCE = "6f079df9a056f00e80392b7e036abc023db5fa88"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v674-v1-full-tools"
SOURCE_X1 = "763969929943d9c9bcb674999508fe33694fa357"
SOURCE_EVIDENCE = "7d0a8f09df1bf70f69369ad78e5c3da4fce85c66"
SOURCE_PACKET = "docs/auren-lark/v674-v1/handoffs/sable-rook-v674-v2-activation.md"
SOURCE_PACKET_SHA256 = "88abed13dda8524f437ac414747075cc9f42047520bcc502a503daab394fd871"
SOURCE_CANONICAL_RECEIPT_SHA256 = "37a8be4a6bccce0d76a7ff8942d630d3077728738b2fd0e6a811e2a662452a4c"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "c0d3be46a3d4a67f635670249f14bca0090ab68e6c4e3c54e41d2d8c6596be05"
RECORDED_UTC = "2026-08-28T07:24:20Z"
RECORDED_NZ = "2026-08-28T19:24:20+12:00"
SOURCE_PROPOSAL_CHAIN = 6610
PLANNED_PROPOSAL_CHAIN = 6670

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
VALIDATION_ROOT = PHASE_ROOT / "validation"

CORE_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "identity_continuity",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]


NEW_PROPOSALS: list[tuple[str, str, str, str]] = [
    ("Freed ID and CBR Heart", "Synthetic caption cue identifier pseudonymization contract", "cue identifier contract", "completed"),
    ("Freed ID and CBR Heart", "Minimum-disclosure caption projection", "minimum-disclosure projection", "completed"),
    ("Freed ID and CBR Heart", "Caption correction and contest channel", "contest channel", "completed"),
    ("Freed ID and CBR Heart", "Append-only caption correction DAG", "correction DAG", "completed"),
    ("Freed ID and CBR Heart", "Rights-source status ledger", "rights-source ledger", "completed"),
    ("Freed ID and CBR Heart", "Voice-label privacy minimization", "voice-label privacy map", "completed"),
    ("Freed ID and CBR Heart", "Content-warning status without content adjudication", "warning-status ledger", "completed"),
    ("Freed ID and CBR Heart", "Operator identity noncollection rule", "identity noncollection rule", "completed"),
    ("Freed ID and CBR Heart", "Access request versus fulfillment separation", "access-request separation board", "completed"),
    ("Freed ID and CBR Heart", "Synthetic transcript retention-expiry proxy", "retention proxy", "completed"),
    ("Freed ID and CBR Heart", "Source-to-derivative provenance link", "derivative provenance link", "completed"),
    ("Freed ID and CBR Heart", "Purpose-limited caption field map", "purpose map", "completed"),
    ("Freed ID and CBR Heart", "Remedy-request lineage record", "remedy lineage", "completed"),
    ("Freed ID and CBR Heart", "Caption fixity event record", "fixity event", "completed"),
    ("Freed ID and CBR Heart", "Fixity algorithm agility contract", "algorithm agility contract", "completed"),
    ("Freed ID and CBR Heart", "Provenance-completeness nonclaim", "provenance nonclaim", "completed"),
    ("Freed ID and CBR Heart", "Affected-user evaluation vacancy", "affected-user vacancy", "represented"),
    ("Freed ID and CBR Heart", "Language-review authority vacancy", "language-review vacancy", "represented"),
    ("Freed ID and CBR Heart", "Live-captioner competence vacancy", "professional vacancy", "represented"),
    ("Freed ID and CBR Heart", "Accessibility-preference representation", "preference proxy", "represented"),
    ("Freed ID and CBR Heart", "Real affected-user feedback gap", "affected-user evidence gap", "open_gap"),
    ("Freed ID and CBR Heart", "Maori wording and data-governance authority gate", "Maori authority gate", "exact_gate"),
    ("Freed ID and CBR Heart", "Rights-holder and legal-interpretation gate", "legal authority gate", "exact_gate"),
    ("Freed ID and CBR Heart", "Venue and participant consent authority gate", "consent authority gate", "exact_gate"),
    ("THOS Body", "WebVTT header and parser contract", "WebVTT parser contract", "completed"),
    ("THOS Body", "Caption timestamp grammar and ordering guard", "timestamp guard", "completed"),
    ("THOS Body", "Cue overlap classification tribunal", "overlap tribunal", "completed"),
    ("THOS Body", "Duplicate cue identifier quarantine", "duplicate identifier quarantine", "completed"),
    ("THOS Body", "WebVTT NOTE block boundary guard", "NOTE boundary guard", "completed"),
    ("THOS Body", "Caption region-reference integrity guard", "region integrity guard", "completed"),
    ("THOS Body", "Language-span nesting contract", "language-span contract", "completed"),
    ("THOS Body", "Cue-setting range validator", "cue-setting validator", "completed"),
    ("THOS Body", "Speaker-label syntax refusal", "speaker-label refusal", "completed"),
    ("THOS Body", "Non-speech audio marker structure", "audio marker structure", "completed"),
    ("THOS Body", "Correction readback state machine", "readback state machine", "completed"),
    ("THOS Body", "Caption handover workload budget", "workload budget", "completed"),
    ("THOS Body", "Hold and release status contract", "hold-release contract", "completed"),
    ("THOS Body", "Bounded timeout cancellation and quiescence receipt", "quiescence receipt", "completed"),
    ("THOS Body", "No-network caption fixture firewall", "network firewall", "completed"),
    ("THOS Body", "Deterministic caption JSON serialization", "deterministic JSON contract", "completed"),
    ("THOS Body", "Normalized-LF Git-blob manifest replay", "manifest replay", "completed"),
    ("THOS Body", "Owner-delta literal allowlist", "owner-delta allowlist", "completed"),
    ("THOS Body", "Accessible static caption report structure", "static report proxy", "represented"),
    ("THOS Body", "Live caption workflow proxy", "workflow proxy", "represented"),
    ("THOS Body", "Manual keyboard evaluation vacancy", "manual evaluation vacancy", "represented"),
    ("THOS Body", "Assistive-technology evaluation vacancy", "assistive-technology vacancy", "represented"),
    ("THOS Body", "Caption latency and accuracy proxy", "latency accuracy proxy", "represented"),
    ("THOS Body", "Real blind matched-budget caption trial gap", "real trial gap", "open_gap"),
    ("GMUT Mind", "Typed rational caption timebase dimension board", "timebase dimension board", "completed"),
    ("GMUT Mind", "Cue interval algebra guard", "interval algebra guard", "completed"),
    ("GMUT Mind", "Clock offset versus drift separation", "offset-drift separation", "completed"),
    ("GMUT Mind", "Caption event-order partial-order board", "partial-order board", "completed"),
    ("GMUT Mind", "Caption residual sign-convention ledger", "residual sign ledger", "completed"),
    ("GMUT Mind", "Caption timing covariance proxy", "covariance proxy", "completed"),
    ("GMUT Mind", "Observation-model-prior separation for cue timing", "model separation board", "completed"),
    ("GMUT Mind", "Caption-to-physics analogy nonconversion firewall", "analogy firewall", "completed"),
    ("GMUT Mind", "Timing uncertainty propagation proxy", "uncertainty proxy", "represented"),
    ("GMUT Mind", "Synchronization error model proxy", "synchronization proxy", "represented"),
    ("GMUT Mind", "Time-aligned metadata analogy limit", "analogy limit", "represented"),
    ("GMUT Mind", "Real-data caption likelihood gap", "real likelihood gap", "open_gap"),
]

OWNER_SKILLS = [
    "ghc-family-caption-cue-identity-contract",
    "ghc-family-caption-timebase-ordering",
    "ghc-family-caption-overlap-quarantine",
    "ghc-family-caption-correction-dag",
    "ghc-family-caption-minimum-disclosure",
    "ghc-family-caption-privacy-projection",
    "ghc-family-caption-rights-vacancy",
    "ghc-family-caption-maori-authority-gate",
    "ghc-family-caption-accessibility-reservation",
    "ghc-family-caption-manual-evaluation-hold",
    "ghc-family-caption-handover-state",
    "ghc-family-caption-workload-budget",
    "ghc-family-caption-note-boundary",
    "ghc-family-caption-region-integrity",
    "ghc-family-caption-language-span",
    "ghc-family-caption-fixity-event",
    "ghc-family-caption-manifest-replay",
    "ghc-family-caption-owner-delta",
    "ghc-family-caption-analogy-firewall",
    "ghc-family-caption-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_caption_cue_identity_runner.py",
    "ghc_family_caption_timebase_runner.py",
    "ghc_family_caption_overlap_runner.py",
    "ghc_family_caption_correction_runner.py",
    "ghc_family_caption_privacy_runner.py",
    "ghc_family_caption_accessibility_runner.py",
    "ghc_family_caption_handover_runner.py",
    "ghc_family_caption_manifest_runner.py",
    "ghc_family_caption_authority_runner.py",
    "ghc_family_caption_stage20_runner.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-theatre-lighting-cue-epoch",
    "ghc-family-theatre-lighting-patch-provenance",
    "ghc-family-theatre-lighting-focus-hold",
    "ghc-family-theatre-lighting-correction-readback",
    "ghc-family-theatre-lighting-accessibility-note",
    "ghc-family-theatre-lighting-power-nonclaim",
    "ghc-family-theatre-lighting-rights-vacancy",
    "ghc-family-theatre-lighting-maori-authority-gate",
    "ghc-family-theatre-lighting-handover",
    "ghc-family-theatre-lighting-stage20-veto",
]

SUCCESSOR_RUNNERS = [name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py" for name in SUCCESSOR_SKILLS]

STARTUP_FAILURES = [
    ("SR6742-X1-F001", "first 225-line activation projection truncated before EOF", "reread bounded 100-line windows through EOF"),
    ("SR6742-X1-F002", "combined authorization and roster projection truncated", "read each required file separately in bounded chunks"),
    ("SR6742-X1-F003", "first broad worktree projection returned no attributable result", "use literal branch and path probes"),
    ("SR6742-X1-F004", "second worktree projection exceeded its bounded output", "avoid broad worktree enumeration"),
    ("SR6742-X1-F005", "metadata-key inspection piped directly from foreach and hit a parser error", "materialize the row array before piping"),
    ("SR6742-X1-F006", "Windows wildcard literal paths were rejected", "use literal directories plus explicit include filters"),
    ("SR6742-X1-F007", "broad source-task reread was host-truncated", "request one bounded recent turn without outputs"),
    ("SR6742-X1-F008", "second source-task reread still included a large preview and truncated", "use only the surfaced exact receipt path"),
    ("SR6742-X1-F009", "canonical receipt projection guessed absent convenience keys", "inspect actual receipt keys before scalar projection"),
    ("SR6742-X1-F010", "receipt scalar projection treated numeric fields as arrays", "read observed numeric fields without array coercion"),
    ("SR6742-X1-F011", "branch uniqueness preflight grouped a native command inside a PowerShell expression", "run the native command and inspect LASTEXITCODE separately"),
    ("SR6742-X1-F012", "sparse-checkout wrapper crossed its projection window", "inspect persisted sparse patterns and checkout quiescence before retry"),
    ("SR6742-X1-F013", "first x1 selection found the planning overview below its frozen 700-word floor", "expand the generating overview template without weakening the test"),
    ("SR6742-X1-F014", "first exact staged review treated scanner definitions and rejection assertions as payload hits", "separate exact scanner candidates from confirmed payload findings by source-line disposition"),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_json(commit: str, path: str) -> dict[str, Any]:
    raw = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)
    return json.loads(raw.decode("utf-8"))


def inherited_rows() -> list[dict[str, Any]]:
    source = git_json(SOURCE, "docs/auren-lark/v674-v1/x1/new-proposal-freeze.json")
    return [
        {
            "selection_id": f"SR6742-I{index:03d}",
            "source_phase": "v674-v1",
            "source_proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "disposition": "reviewed_for_continuity_zero_sable_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for index, proposal in enumerate(source["proposals"], 1)
    ]


def new_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (pillar, title, artifact, outcome) in enumerate(NEW_PROPOSALS, 1):
        rows.append(
            {
                "proposal_id": f"SR6742-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_live_caption_cue_provenance_steward",
                    "wholly_synthetic_accessible_performance_metadata_handover_analyst",
                ],
                "hypothesis": f"A bounded owner-local {artifact} can preserve its declared structural obligation while refusing absent evidence and authority.",
                "null_or_failure_condition": "Fail if an accepting fixture violates its declared type, loses a retained failure, uses a real identifier or record, performs an external action, or promotes a protected claim.",
                "approval_class": "safe_now" if outcome == "completed" else ("candidate" if outcome == "represented" else outcome),
                "execution_lane": "owner_local_synthetic_x2" if outcome in {"completed", "represented"} else "held_for_external_evidence_or_authority",
                "official_or_primary_source_needs": ["W3C WebVTT", "W3C WCAG 2.2", "W3C PROV-O", "Library of Congress PREMIS"],
                "concrete_artifact": artifact,
                "falsifier_or_acceptance_gate": "One accepting fixture and four preregistered invalid mutations; held outcomes require the named external evidence or authority.",
                "rollback_or_recovery": "Quarantine only Sable-created uncommitted material, retain the failed witness at zero credit, and return to immutable x1.",
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "sable_current_proposal_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "rejecting_mutation_contract")
    return [
        {
            "packet_id": f"SR6742-S{index:03d}",
            "proposal_id": proposal["proposal_id"],
            "title": f"{proposal['title']} - {action.replace('_', ' ')}",
            "approval_bucket": "safe_now",
            "scope": "additive owner-local synthetic or structural evidence only",
            "external_action": False,
            "completion_credit": 0,
            "x1_state": "frozen_not_executed",
        }
        for index, (proposal, action) in enumerate(((p, a) for p in proposals for a in actions), 1)
    ]


def candidates(proposals: list[dict[str, Any]], count: int, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"{prefix}{index:03d}",
            "proposal_id": proposals[(index - 1) % len(proposals)]["proposal_id"],
            "title": f"Bounded prototype {index:03d} - {proposals[(index - 1) % len(proposals)]['title']}",
            "state": "frozen_not_executed",
            "external_action": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def exact_rows() -> list[dict[str, Any]]:
    topics = ["real participants", "production keys", "live deployment", "professional signoff", "legal interpretation", "cultural ratification", "Maori authority", "affected-party acceptance", "external publication", "destructive cleanup", "account mutation", "credential use", "payment", "real data acquisition", "privacy certification", "accessibility certification", "independent audit", "independent reproduction", "empirical GMUT inference", "Stage 20 promotion"]
    return [{"packet_id": f"SR6742-E{index:03d}", "topic": topic, "state": "exact_approval_held_unexecuted", "completion_credit": 0} for index, topic in enumerate(topics, 1)]


def blocked_rows() -> list[dict[str, Any]]:
    topics = ["force push", "history rewrite", "sibling-lane mutation", "user-material deletion", "host-security weakening", "elevation", "Sandbox or Hyper-V activation", "credential harvesting", "identity continuity claim", "AGI ASI personhood claim"]
    return [{"packet_id": f"SR6742-B{index:03d}", "topic": topic, "state": "blocked_unexecuted", "completion_credit": 0} for index, topic in enumerate(topics, 1)]


def cleanup_rows(count: int, prefix: str, owner: bool) -> list[dict[str, Any]]:
    topics = ["schema closure", "deterministic JSON", "UTF-8 preservation", "manifest parity", "stale-label review", "privacy disposition", "diff hygiene", "caller compatibility", "failure retention", "route hold"]
    return [
        {
            "task_id": f"{prefix}{index:03d}",
            "title": f"{topics[(index - 1) % len(topics)]} refinement {index:03d}",
            "state": "frozen_not_executed" if owner else "successor_recommendation_zero_credit",
            "destructive": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def overview() -> str:
    return """# Sable Rook v674-v2 planning-only x1 overview

## Identity, role, hope, and corrigibility

Sable Rook is reaffirmed as a relational evidence-boundary cartographer and accessible-provenance steward. The working hope is to make correction paths inspectable, access vacancies explicit, and every retained failure recoverable. This name, role, hope, sibling language, and all GHC Family or Trinity Mandala language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may rename, pause, redirect, or stop the route.

## Planning-only lifecycle

This x1 freezes exact source anchors, sixty inherited Auren proposal reviews with zero Sable novelty and zero completion credit, sixty new Sable proposals, portfolios, skills, runners, safeguards, and a route hold. It contains no x2 implementation, observed outcome, package installation, global skill mutation, task contact, or terminal claim. The source is Auren's exact final `6f079df9a056f00e80392b7e036abc023db5fa88`, whose packet, five manifest families, canonical receipt, direct ancestry, clean state, and fresh four-way equality were independently reverified read-only.

## Trinity Mandala and bounded practices

The primary pillar is Freed ID and CBR Heart. THOS Body remains visible through deterministic cue parsing, correction, workload, hold, readback, and handover contracts. GMUT Mind remains visible only through typed rational-timebase, interval, uncertainty, covariance, and analogy-firewall structures. The two practices are wholly synthetic live-caption cue provenance stewardship and wholly synthetic accessible-performance metadata handover analysis. No real person, performance, caption, transcript, venue, language decision, record, identity, consent, rights decision, cultural matter, Māori data, or authority action is used.

## Primary-source boundary

Current primary vocabulary is drawn from the W3C WebVTT Candidate Recommendation Draft dated 20 May 2026, W3C WCAG 2.2 Recommendation, W3C PROV-O Recommendation, and the Library of Congress PREMIS maintenance activity. WebVTT is explicitly recorded as draft work in progress. These sources provide vocabulary and refusal conditions only. They do not endorse Sable, validate any artifact, provide user evaluation, establish conformance, or confer legal, cultural, professional, affected-party, or Māori authority.

## Proposal and portfolio freeze

The sixty new proposals have expected dispositions of forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. These are expectations only until x2 evidence exists. X1 also freezes 120 safe-now packets, eighty owner candidates, twenty successor candidates, twenty exact holds, ten blocked holds, twenty owner skills, ten owner runners, ten successor skills, ten successor runners, one hundred owner refinements, and thirty successor refinements. Caps are ceilings; none authorizes filler, destructive cleanup, external mutation, or evidence promotion.

The sixty inherited reviews are deliberately separated from the sixty new proposals. Each inherited title is read from Auren's immutable x1 Git object and carries both novelty credit zero and completion credit zero. Review continuity is useful because it exposes semantic neighbors, protected gates, and caller contracts, but a successor cannot inherit authorship or outcome credit. The current proposal titles therefore use caption cue, timebase, correction, access, privacy, provenance, and handover surfaces that are materially different from Auren's seismic-station metadata work. No universal novelty claim is made: the bounded claim is only that the current sixty-title set is internally unique and was checked against the exact inherited selection available at the source anchor.

The expected outcome distribution is intentionally fail-closed. A `completed` label can describe only a bounded structural or synthetic acceptance contract. A `represented` label means a proxy or structural representation exists while real people, systems, evaluation, or authority remain absent. An `open_gap` names missing empirical or participant evidence. An `exact_gate` names a decision that repository software cannot make, including Māori wording and data governance, legal or rights-holder interpretation, or participant and venue consent. No passing mutation can compensate for a missing evidence class or authority holder.

Every new proposal freezes one positive-control expectation and four invalid-input classes for x2: missing required structure, invalid outcome vocabulary, prohibited external action, and prohibited authority promotion. A later rejected mutation is evidence only that the declared guard rejected that fixture. It is not a penetration test, exhaustive-security result, complete privacy assurance, user study, standards conformance certificate, or independent reproduction. Failures must be recorded before recovery and cannot be deleted when a later bounded witness passes.

The planned phase-local skills and runners are owner-scoped teaching and validation aids. Their family-current names preserve `ghc_family_*` and `build_ghc_family_*` compatibility, but local validation does not install them globally or make them authoritative for another owner. The x1 toolchain records that no third-party installation is necessary: Python's standard library, exact Git objects, and deterministic JSON are sufficient for the declared hypotheses. This choice avoids semantic-free package churn and does not claim that inherited packages are unavailable or unsafe.

## Failure retention and terminal boundaries

All inherited Auren failures remain inherited evidence. Twelve Sable startup failures are frozen separately with zero credit and additive recoveries. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Empirical, participant, professional, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, legal, cultural, affected-party, Māori-authority, and Stage 20 gates remain open or exact-gated.

## X1 gate and future route

X1 must be tested, exactly staged, committed as the direct child of Auren final, pushed, clean, and equal across local, upstream, tracking, and a fresh live remote before any x2 path is created. Only after a later clean pushed exact final and one successful owner-scoped canonical validation may Sable freshly resolve and immediately reread the unique exact-title `Caelen Ash` task and send one sanitized v674-v3 activation. This x1 performs no task lookup or contact.
"""


def build() -> list[str]:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip() != SOURCE:
        raise RuntimeError("x1 builder must run at the exact Auren source head")
    if (PHASE_ROOT / "x2").exists():
        raise RuntimeError("x2 material exists before x1 freeze")

    inherited = inherited_rows()
    proposals = new_rows()
    safe = safe_rows(proposals)
    owner_candidates = candidates(proposals, 80, "SR6742-C")
    successor_candidates = candidates(proposals, 20, "SR6742-SC")
    owner_cleanup = cleanup_rows(100, "SR6742-R", True)
    successor_cleanup = cleanup_rows(30, "SR6742-SR", False)

    files: list[Path] = []
    payloads: dict[Path, Any] = {
        X1_ROOT / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v674.v2",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_packet": SOURCE_PACKET,
            "source_packet_sha256": SOURCE_PACKET_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_verified_clean_four_way_equal": True,
            "source_manifest_families_replayed": 5,
            "source_canonical_replayed": False,
            "received_once": True,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "owner": OWNER,
            "relational_role": "evidence-boundary cartographer and accessible-provenance steward",
            "hope": "make correction paths inspectable, access vacancies explicit, and every retained failure recoverable",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "source_proposal_chain": SOURCE_PROPOSAL_CHAIN,
            "proposal_chain_if_x2_evidence_frozen": PLANNED_PROPOSAL_CHAIN,
            "proposal_count": len(proposals),
            "allowed_outcomes": CORE_OUTCOMES,
            "expected_outcomes": {label: sum(1 for row in proposals if row["expected_execution_disposition"] == label) for label in CORE_OUTCOMES},
            "outcomes_observed": False,
            "universal_novelty_claim": False,
            "proposals": proposals,
        },
        X1_ROOT / "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v674.v2",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
            "owner_practice_lenses": ["wholly_synthetic_live_caption_cue_provenance_steward", "wholly_synthetic_accessible_performance_metadata_handover_analyst"],
            "successor_practice_recommendation": "wholly_synthetic_theatre_lighting_cue_patch_and_handover_documentation_analyst",
            "safe_now": safe,
            "owner_candidates": owner_candidates,
            "successor_candidates": successor_candidates,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "owner_skill_ideas": OWNER_SKILLS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "owner_clean_fix_refine": owner_cleanup,
            "successor_clean_fix_refine": successor_cleanup,
            "caps_are_ceilings": True,
            "materialized_file_stop": 2000,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v674.v2",
            "owner": OWNER,
            "phase": PHASE,
            "activation_baseline": {"effective_negatives": 38104, "methods": 25043, "failed_witnesses": 9765, "bounded_passing_witnesses": 12654},
            "startup_failure_count": len(STARTUP_FAILURES),
            "failures": [{"failure_id": fid, "failed_witness": failed, "recovery": recovery, "state": "failed_retained_zero_credit", "success_credit": 0} for fid, failed, recovery in STARTUP_FAILURES],
            "recovery_rule": "Every recovery is additive and never erases or relabels the failed witness.",
        },
        X1_ROOT / "source-ledger.json": {
            "schema": "ghc.family.official-source-ledger.v674.v2.x1",
            "checked_at_utc": RECORDED_UTC,
            "entries": [
                {"source_id": "W3C-WEBVTT-2026", "title": "WebVTT: The Web Video Text Tracks Format", "url": "https://www.w3.org/TR/webvtt1/", "status": "candidate_recommendation_draft", "status_date": "2026-05-20", "use": "cue syntax, timing, regions, language, privacy and security vocabulary only"},
                {"source_id": "W3C-WCAG22", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "recommendation", "status_date": "2024-12-12", "use": "time-based-media and accessibility refusal vocabulary only"},
                {"source_id": "W3C-PROV-O", "title": "PROV-O: The PROV Ontology", "url": "https://www.w3.org/TR/prov-o/", "status": "recommendation_stable", "use": "provenance relation vocabulary only"},
                {"source_id": "LOC-PREMIS", "title": "PREMIS Preservation Metadata Maintenance Activity", "url": "https://www.loc.gov/standards/premis/index.html", "status": "current_version_3_0", "use": "object, event, agent, rights, fixity, and preservation vocabulary only"},
            ],
            "citations_are_observations": False,
            "real_data_rows": 0,
            "endorsement_claimed": False,
        },
        X1_ROOT / "route-roster-plan.json": {
            "schema": "ghc.family.route-roster-plan.v674.v2",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "previous_owner": "Auren Lark",
            "previous_phase": "v674-v1",
            "next_owner": "Caelen Ash",
            "next_phase": "v674-v3",
            "state": "HOLD_BEFORE_SABLE_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "create_task": False,
            "duplicate_guard_required": True,
            "terminal_label": "v725-v8",
        },
        X1_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v674.v2.x1",
            "threats": ["real identifier leakage", "private route leakage", "x1 x2 mixing", "outcome promotion", "authority fabrication", "network side effect", "manifest drift", "failed-witness erasure", "success replay", "sibling-lane mutation"],
            "controls": ["synthetic fixtures only", "five-class scan", "planning-only x1", "four exact labels", "authority vacancy", "no-network runners", "Git-blob manifests", "append-only failures", "one-shot latch", "owner-local sparse lane"],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "toolchain-plan.json": {
            "schema": "ghc.family.toolchain-plan.v674.v2",
            "third_party_installation_planned": False,
            "reason": "No new package is necessary for the bounded owner-local hypotheses; Python standard library and exact Git blobs suffice.",
            "phase_local_skills": OWNER_SKILLS,
            "phase_local_runners": OWNER_RUNNERS,
            "global_installation_planned": False,
            "plugin_cache_mutation": False,
            "caller_compatibility": "preserve ghc_family_* and build_ghc_family_* naming",
        },
        X1_ROOT / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v674.v2",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {"order": 1, "name": "read activation skills guidance and memory", "state": "completed"},
                {"order": 2, "name": "verify immutable source manifests receipt and live equality", "state": "completed"},
                {"order": 3, "name": "create sparse Sable lane", "state": "completed"},
                {"order": 4, "name": "freeze test push and prove x1", "state": "in_progress"},
                {"order": 5, "name": "build bounded x2 evidence", "state": "pending"},
                {"order": 6, "name": "seal push and run one canonical", "state": "pending"},
                {"order": 7, "name": "route once to exact successor if all gates pass", "state": "pending"},
            ],
            "stop_conditions": ["source mismatch", "dirty source", "x1 x2 mixing", "privacy hit", "manifest mismatch", "protected authority gate", "usage exhaustion", "route ambiguity", "user pause or redirect"],
        },
    }
    for path, payload in payloads.items():
        write_json(path, payload)
        files.append(path)

    overview_path = X1_ROOT / "integrated-overview.md"
    write_text(overview_path, overview())
    files.append(overview_path)

    manifest_path = X1_ROOT / "x1-manifest.json"
    entries = []
    for path in sorted(files):
        data = path.read_bytes()
        entries.append({"path": path.relative_to(REPO).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json(manifest_path, {"schema": "ghc.family.x1-manifest.v674.v2", "owner": OWNER, "phase": PHASE, "source": SOURCE, "entry_count": len(entries), "entries": entries, "self_excluded": manifest_path.relative_to(REPO).as_posix()})
    files.append(manifest_path)
    return [path.relative_to(REPO).as_posix() for path in sorted(files)]


def build_staged_review() -> dict[str, Any]:
    review_path = "docs/sable-rook/v674-v2/validation/x1-staged-review.json"
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v674_v2_x1.py",
        "tests/test_ghc_family_sable_rook_v674_v2_x1.py",
        review_path,
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/sable-rook/v674-v2/x1/")
        and path not in allowed_exact
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:C:\\\\Users\\\\|D:\\\\GHC-Archives)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{32,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }
    entries = []
    json_parses = 0
    candidates: list[dict[str, str]] = []
    hits: list[dict[str, str]] = []
    for path in staged:
        if path == review_path:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                line_start = data.rfind(b"\n", 0, match.start()) + 1
                line_end = data.find(b"\n", match.end())
                if line_end < 0:
                    line_end = len(data)
                line = data[line_start:line_end]
                if path.endswith(".py") and (b"re.compile" in line or b"assertNot" in line):
                    candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_or_rejection_assertion"})
                else:
                    hits.append({"path": path, "class": class_name})
        entries.append({"path": path, "bytes": len(data), "sha256_git_index_blob": hashlib.sha256(data).hexdigest()})
    if hits:
        raise RuntimeError(f"confirmed privacy hits: {hits}")
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, check=False)
    if diff_check.returncode != 0:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)
    receipt: dict[str, Any] = {
        "schema": "ghc.family.exact-staged-review.v674.v2.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "state": "VALID_EXACT_X1_STAGED_REVIEW",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": [review_path],
        "json_parses": json_parses,
        "privacy_classes": list(patterns),
        "scanner_candidate_count": len(candidates),
        "scanner_candidates": candidates,
        "confirmed_privacy_hits": 0,
        "out_of_scope_paths": [],
        "diff_hygiene": True,
        "x2_paths_present": any(path.startswith("docs/sable-rook/v674-v2/x2/") for path in staged),
    }
    if receipt["x2_paths_present"]:
        raise RuntimeError("x2 path present in x1 staged surface")
    write_json(REPO / review_path, receipt)
    return receipt


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--staged-review":
        print(json.dumps(build_staged_review(), indent=2))
    else:
        print(json.dumps({"written": build()}, indent=2))
