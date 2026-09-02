from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
OWNER = "Auren Lark"
PHASE = "v684-v4"
BRANCH = "codex/GHC-Family/auren-lark-v684-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v683-v3-full-tools"
SOURCE = "0134e277a7f573e24e697037749d61d577163637"
ILYRA_SOURCE = "0f5210fc4899a3c36e1ca1e5c1b5c897eb9acc68"
ILYRA_X1 = "2bbdaa6b0a6c038bf1233448202dc161f92037ce"
ILYRA_EVIDENCE = "0200d19b4c6fb7947eed664283ead648964d10c1"
ILYRA_RECEIPT_SHA256 = "246be0f3a232c46d07e3c4a97167b66a5c3319414a63e25eca57a05bb5e7bc92"
PACKET_SHA256 = "5e53d1af51d7329492e5136e28c140f6cd59ba7254facab4dc3db81140022293"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


IDENTITY_BOUNDARY = (
    "Auren Lark, the role of evidence-boundary cartographer and reversible "
    "scientific-workflow steward, the hope of turning ambitious ideas into "
    "inspectable corrigible questions, pronouns, names, sibling or family language, "
    "continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational "
    "working language only. They are not evidence of consciousness, sentience, "
    "legal personhood, identity continuity, employment, qualification, independent "
    "agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Maori authority. Hamish may rename, pause, narrow, redirect, "
    "or stop the route."
)


TOPICS = [
    "Coordinate-token taxonomy with every real position absent",
    "Axis-order declaration with no coordinate values",
    "Unit-symbol custody without a measurement",
    "Coordinate-reference-system identifier presence and namespace separation",
    "Datum and reference-frame distinction without a real frame realization",
    "Dynamic reference epoch vacancy and refusal",
    "Coordinate-operation provenance without transformation execution",
    "Transformation-method identifier documentation without parameters",
    "Grid-resource digest field with every grid absent",
    "Vertical-coordinate semantics without height observations",
    "Compound-coordinate-reference-system component ordering",
    "Temporal-coordinate schema without timestamps",
    "Coordinate metadata completeness board with zero data rows",
    "Ambiguous coordinate interpretation refusal",
    "Area-of-use field hold without geographic extent",
    "Accuracy and uncertainty vocabulary separation",
    "Observation-absence latch for synthetic position records",
    "Synthetic-dataset marker and non-empirical gate",
    "Provenance entity activity and agent vacancy",
    "Revision invalidation lineage without an accountable real actor",
    "Uncertainty-component registry without numerical components",
    "Type-A and Type-B evaluation label separation without samples",
    "Covariance placeholder with calculation disabled",
    "Probability-distribution assumption label with every assumption open",
    "Coverage-factor semantics without expanded uncertainty",
    "Expanded-uncertainty refusal when inputs are absent",
    "Significant-digit policy without a reported result",
    "Unit-conversion record without conversion execution",
    "Rounding-decision trace without a numeric quantity",
    "Calibration-certificate absence and non-substitution gate",
    "Measurement-method absence and measurand vacancy",
    "Metrological-traceability chain absence",
    "Software-version and digest provenance",
    "Transformation-parameter provenance without parameter values",
    "Coordinate-operation pipeline serialization without execution",
    "Missing-grid resource refusal",
    "Axis-swap invalid-state rejection",
    "Unit-mismatch invalid-state rejection",
    "Epoch-mismatch invalid-state rejection",
    "Datum-name collision invalid-state rejection",
    "Coordinate-reference code namespace collision rejection",
    "WKT and JSON representation-difference ledger",
    "Reversible metadata normalization representation",
    "Immutable-input checksum representation",
    "Uncertainty-budget revision representation",
    "Derivation-graph cycle representation and rejection boundary",
    "Responsible-authority vacancy representation",
    "Consent and rights fields held for affected people",
    "Maori-data-governance field held for competent Maori authority",
    "Personal-information minimization representation",
    "Retention and deletion boundary representation",
    "Accessibility-status labels without conformance claim",
    "Keyboard-navigation review placeholder without user evaluation",
    "Plain-language scientific-boundary summary",
    "Machine-readable four-label outcome contract requiring external evidence",
    "Failure-receipt non-erasure requiring later independent review",
    "Rollback-map completeness requiring fault-injection evidence",
    "Production-execution authority gate",
    "Scientific-claim promotion and Theory-of-Everything authority gate",
    "Stage-20 nonpromotion and independent-reproduction authority gate",
]


STARTUP_FAILURES = [
    ("AL6844-SF001", "optional update-plan tool was unavailable", "continued with an explicit owner-local ledger"),
    ("AL6844-SF002", "three guessed historical skill names were absent", "used only the exact installed skill inventory"),
    ("AL6844-SF003", "one grouped skill read truncated before EOF", "reread each required skill and reference in bounded windows"),
    ("AL6844-SF004", "one malformed JavaScript tool wrapper treated PowerShell as JavaScript", "used the documented nested exec-command call"),
    ("AL6844-SF005", "one PowerShell inventory wrapper piped directly from foreach and failed parsing", "materialized rows before piping"),
    ("AL6844-SF006", "a second PowerShell inventory wrapper repeated the empty-pipe parser fault", "used a scalar bounded inventory"),
    ("AL6844-SF007", "one combined authorization display truncated", "reread the exact state file in bounded windows"),
    ("AL6844-SF008", "one broad receipt search returned no usable bounded result", "enumerated exact receipt roots and located the named file"),
    ("AL6844-SF009", "one parallel fresh-equality wrapper returned an empty envelope", "recovered through explicit local and fresh-live probes"),
    ("AL6844-SF010", "one guessed evidence-test filename did not exist", "listed the exact Git tree and used the real x2 filename"),
    ("AL6844-SF011", "one target-lane preflight expression had a PowerShell parenthesis error", "reran a corrected scalar preflight"),
    ("AL6844-SF012", "one roster assignment call supplied the structural roster to a projection command", "reran against the exact projection document"),
    ("AL6844-SF013", "one startup-builder help probe executed its default open-gap preflight", "retained the read-only result and did not claim startup completion"),
    ("AL6844-SF014", "one Git cat-file wrapper deadlocked on pipe backpressure", "terminated only its exact orphaned processes and changed the transport"),
    ("AL6844-SF015", "a second batch wrapper inherited the Windows Git shim EOF fault", "invoked the exact mingw Git binary with communicate semantics"),
    ("AL6844-SF016", "one Git archive wrapper inherited the Windows Git shim pipe fault", "terminated only its exact orphaned processes and used direct cat-file transport"),
    ("AL6844-SF017", "Ilyra canonical receipt displayed four stale inherited Eiren manifest path labels", "independently replayed all Ilyra manifests and will not copy the label defect"),
    ("AL6844-SF018", "the structurally valid historical projection assigns v684-v4 to Vesper and carries no activation authority", "preserved the mismatch while following Hamish's newer live Auren correction"),
    ("AL6844-X1F001", "the first x1 source-ledger test required every refusal boundary to begin with the literal word No", "retained the failed run and normalized the Te Mana Raraunga refusal wording without changing its meaning"),
]


SOURCES = [
    {
        "source_id": "AL6844-SRC01",
        "title": "OGC Abstract Specification Topic 2: Referencing by coordinates",
        "url": "https://www.ogc.org/standards/abstract-specification/",
        "use": "Vocabulary for coordinate-reference metadata, ambiguity, and coordinate operations only.",
        "boundary": "No OGC conformance, endorsement, geodetic competence, or real-coordinate validation is claimed.",
    },
    {
        "source_id": "AL6844-SRC02",
        "title": "NIST Technical Note 1297",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297",
        "use": "Vocabulary for uncertainty-component and reporting distinctions only.",
        "boundary": "No NIST policy claim, calibration, measurement, numerical uncertainty, or traceability is established.",
    },
    {
        "source_id": "AL6844-SRC03",
        "title": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "use": "Vocabulary for entity, activity, agent, derivation, revision, and invalidation only.",
        "boundary": "No W3C endorsement or provenance completeness is claimed.",
    },
    {
        "source_id": "AL6844-SRC04",
        "title": "BIPM SI Brochure, ninth edition",
        "url": "https://www.bipm.org/en/publications/si-brochure",
        "use": "Vocabulary for quantities, units, and symbols only.",
        "boundary": "No measurement, unit realization, metrological traceability, or BIPM endorsement is claimed.",
    },
    {
        "source_id": "AL6844-SRC05",
        "title": "W3C Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "use": "Vocabulary for explicit status, navigation, and non-colour-only presentation planning.",
        "boundary": "No accessibility conformance or disabled-user evaluation is claimed.",
    },
    {
        "source_id": "AL6844-SRC06",
        "title": "Office of the Privacy Commissioner New Zealand privacy principles",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "use": "Privacy-minimization and purpose-limitation boundary vocabulary only.",
        "boundary": "No legal advice, compliance determination, or personal-information processing occurred.",
    },
    {
        "source_id": "AL6844-SRC07",
        "title": "Te Mana Raraunga Principles of Maori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "use": "A refusal boundary reserving Maori data decisions to Maori people and competent Maori authority.",
        "boundary": "No cultural ratification, affected-party approval, or Maori authority follows from vocabulary citation.",
    },
]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    rel = path.relative_to(ROOT).as_posix()
    return {"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def inherited_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_proposal_id": f"IF6833-N{i:03d}",
            "review_id": f"AL6844-I{i:03d}",
            "source_owner": "Ilyra Fen",
            "source_phase": "v683-v3",
            "current_novelty_credit": 0,
            "automatic_completion_credit": 0,
            "disposition": "revalidated_as_inherited_context_only",
            "boundary": "Read-only inherited context; no Auren evidence, novelty, competence, or authority.",
        }
        for i in range(1, 61)
    ]


def new_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(TOPICS, 1):
        if index <= 42:
            expected = "completed"
        elif index <= 54:
            expected = "represented"
        elif index <= 57:
            expected = "open_gap"
        else:
            expected = "exact_gate"
        mutations = [
            {
                "mutation_id": f"AL6844-N{index:03d}-M{j:02d}",
                "mutation_type": kind,
                "expected_result": "reject_and_retain_zero_credit",
            }
            for j, kind in enumerate(
                ("remove_synthetic_marker", "inject_real_row", "promote_claim", "erase_failure", "bypass_authority_hold"),
                1,
            )
        ]
        rows.append(
            {
                "proposal_id": f"AL6844-N{index:03d}",
                "title": title,
                "pillar": "GMUT Mind primary; THOS Body and Freed ID/CBR Heart explicit",
                "practice_lenses": [
                    "synthetic geospatial metadata quality analyst",
                    "synthetic uncertainty-budget documentation analyst",
                ],
                "hypothesis": (
                    "A wholly synthetic zero-row contract can preserve the named metadata distinction, "
                    "reject preregistered invalid states, and keep every empirical and authority boundary open."
                ),
                "planning_only": True,
                "expected_execution_disposition": expected,
                "permitted_evidence": "owner-local software, schema, documentation, and synthetic fixture evidence only",
                "forbidden_promotions": [
                    "empirical confirmation",
                    "professional or scientific authority",
                    "production readiness",
                    "legal or cultural ratification",
                    "Maori authority",
                    "independent reproduction",
                    "AGI or ASI",
                    "consciousness or personhood",
                    "Theory of Everything proof",
                    "Stage 20 authority",
                ],
                "preregistered_rejecting_mutations": mutations,
                "rollback": f"Quarantine only AL6844-N{index:03d}, retain its failed receipt, and regenerate from frozen x1.",
            }
        )
    return rows


def portfolio(new: list[dict[str, Any]]) -> dict[str, Any]:
    safe = []
    for row in new:
        for suffix, action in (("A", "schema-shape and vocabulary review"), ("B", "nonpromotion and rollback review")):
            safe.append(
                {
                    "packet_id": f"AL6844-SAFE-{row['proposal_id'][-3:]}{suffix}",
                    "proposal_id": row["proposal_id"],
                    "task": action,
                    "x1_disposition": "approved_for_bounded_x2_execution",
                    "real_world_action": False,
                }
            )
    candidates = [
        {
            "packet_id": f"AL6844-CAND-{i:03d}",
            "task": f"Execute bounded synthetic candidate review {i:03d} with zero real rows",
            "proposal_id": f"AL6844-N{((i - 1) % 60) + 1:03d}",
            "x1_disposition": "candidate_for_x2_execution",
        }
        for i in range(1, 81)
    ]
    successor = [
        {
            "packet_id": f"AL6844-SUCC-CAND-{i:03d}",
            "prospective_owner": "Sable Rook",
            "prospective_phase": "v684-v5",
            "task": f"Advisory museum environmental-monitoring documentation candidate {i:03d}",
            "status": "recommendation_only_not_executed_not_authority",
        }
        for i in range(1, 21)
    ]
    exact = [
        {
            "packet_id": f"AL6844-EXACT-{i:03d}",
            "gate": f"Competent human or affected-party exact approval gate {i:03d}",
            "status": "held_unexecuted",
        }
        for i in range(1, 21)
    ]
    blocked = [
        {
            "packet_id": f"AL6844-BLOCK-{i:03d}",
            "reason": f"Empirical, professional, production, legal, cultural, or authority evidence absent {i:03d}",
            "status": "blocked_unexecuted",
        }
        for i in range(1, 11)
    ]
    return {
        "schema": "ghc.family.approval-portfolio.v1",
        "owner": OWNER,
        "phase": PHASE,
        "planning_only": True,
        "caps_are_ceilings_not_quotas": True,
        "safe_now": safe,
        "owner_candidates": candidates,
        "successor_candidate_recommendations": successor,
        "exact_approval_holds": exact,
        "blocked_holds": blocked,
        "counts": {
            "safe_now": len(safe),
            "owner_candidates": len(candidates),
            "successor_candidates": len(successor),
            "exact": len(exact),
            "blocked": len(blocked),
        },
        "caps": {"safe_now": 200, "combined_candidates": 200, "exact": 100, "blocked": 50},
    }


def skill_runner_plan() -> dict[str, Any]:
    skill_names = [
        "coordinate-metadata-vacancy-guard", "axis-order-refusal-board", "unit-symbol-custody-ledger",
        "reference-frame-epoch-separator", "coordinate-operation-nonexecution", "grid-resource-digest-hold",
        "vertical-coordinate-nonobservation", "compound-crs-order-review", "uncertainty-component-vacancy",
        "coverage-factor-noncalculation", "metrological-traceability-open-gate", "rounding-decision-provenance",
        "prov-derivation-cycle-guard", "responsible-agent-vacancy", "privacy-minimization-boundary",
        "maori-data-authority-hold", "accessibility-conformance-refusal", "four-label-outcome-linter",
        "retained-failure-nonerasure", "stage20-nonpromotion-latch",
    ]
    runner_names = [
        "ghc_family_coordinate_metadata_contract_runner.py",
        "ghc_family_axis_unit_rejection_runner.py",
        "ghc_family_reference_frame_vacancy_runner.py",
        "ghc_family_coordinate_operation_lineage_runner.py",
        "ghc_family_uncertainty_documentation_runner.py",
        "ghc_family_provenance_cycle_guard_runner.py",
        "ghc_family_privacy_authority_hold_runner.py",
        "ghc_family_accessibility_boundary_runner.py",
        "ghc_family_failure_retention_runner.py",
        "ghc_family_stage20_nonpromotion_runner.py",
    ]
    return {
        "schema": "ghc.family.skill-runner-plan.v1",
        "owner": OWNER,
        "phase": PHASE,
        "planning_only": True,
        "owner_skill_ideas": [{"skill": n, "status": "planned_phase_local"} for n in skill_names],
        "owner_runner_ideas": [{"runner": n, "status": "planned_phase_local"} for n in runner_names],
        "successor_skill_ideas": [
            {"skill": f"museum-environmental-documentation-skill-{i:02d}", "status": "recommendation_only"}
            for i in range(1, 11)
        ],
        "successor_runner_ideas": [
            {"runner": f"ghc_family_museum_environmental_candidate_runner_{i:02d}.py", "status": "recommendation_only"}
            for i in range(1, 11)
        ],
        "caps": {"skills": 50, "runners": 50},
        "global_installation": "not_authorized_by_count_alone; promotion requires exact validation and collision review",
    }


def cfr_plan() -> dict[str, Any]:
    verbs = ("CLEAN", "FIX", "REFINE", "VERIFY")
    owner_rows = [
        {
            "task_id": f"AL6844-CFR-{i:03d}",
            "mode": verbs[(i - 1) % len(verbs)],
            "task": f"Owner-local schema, documentation, runner, rollback, or boundary refinement {i:03d}",
            "scope": "Auren v684-v4 only",
            "x1_status": "planned_for_x2",
            "destructive_action": False,
        }
        for i in range(1, 101)
    ]
    successor_rows = [
        {
            "task_id": f"AL6844-SUCC-CFR-{i:03d}",
            "task": f"Advisory successor documentation refinement {i:03d}",
            "status": "recommendation_only_not_executed",
        }
        for i in range(1, 31)
    ]
    return {
        "schema": "ghc.family.clean-fix-refine-plan.v1",
        "owner": OWNER,
        "phase": PHASE,
        "planning_only": True,
        "owner_rows": owner_rows,
        "successor_rows": successor_rows,
        "counts": {"owner": 100, "successor": 30},
        "caps": {"owner": 500, "successor": 200},
        "deletion_authority": False,
        "sibling_lane_mutation_authority": False,
    }


def method_failures() -> list[dict[str, Any]]:
    return [
        {
            "failure_id": fid,
            "failed_witness": failed,
            "recovery": recovery,
            "retained_zero_credit": True,
            "state_change": False,
        }
        for fid, failed, recovery in STARTUP_FAILURES
    ]


def overview(new: list[dict[str, Any]], failures: list[dict[str, Any]]) -> str:
    expected = Counter(row["expected_execution_disposition"] for row in new)
    return f"""# Auren Lark v684-v4 planning-only x1

## Identity, role, hope, and corrigibility

{IDENTITY_BOUNDARY}

## Frozen scope

This x1 is planning only. It freezes sixty inherited Ilyra proposals at zero Auren novelty or completion credit and sixty new Auren proposals for later bounded x2 review. It contains no Auren x2 outcome, no production execution, no empirical observation, no participant data, and no authority action.

The primary pillar is GMUT Mind, with THOS Body and Freed ID/CBR Heart explicit and protected. The two wholly synthetic learning lenses are geospatial metadata quality analyst and uncertainty-budget documentation analyst. These are practice lenses, not employment, qualification, professional competence, or authorization. The advisory next-owner practice is museum environmental-monitoring data documentation analyst; it earns no Sable credit unless independently reviewed and frozen.

## Frozen portfolio

- 60 inherited proposals revalidated with zero novelty and zero automatic completion credit.
- 60 new proposals, giving 120 reviewed proposal records.
- 120 safe-now planning packets, cap 200.
- 80 owner candidate packets plus 20 successor recommendations, combined cap 200.
- 20 exact-approval holds and 10 blocked holds, all unexecuted.
- 20 owner skill ideas, 10 owner runner ideas, 10 successor skill ideas, and 10 successor runner ideas.
- 100 owner CLEAN/FIX/REFINE/VERIFY tasks and 30 successor recommendations.
- 300 preregistered rejecting mutations for later x2 execution.

Expected later dispositions are planning fields only: completed {expected['completed']}, represented {expected['represented']}, open_gap {expected['open_gap']}, and exact_gate {expected['exact_gate']}. The only permitted labels are completed, represented, open_gap, and exact_gate.

## Source and route truth

Ilyra exact final {SOURCE} was clean and equal across local, upstream, tracking, and a fresh live remote. The direct chain is {ILYRA_SOURCE} to {ILYRA_X1} to {ILYRA_EVIDENCE} to {SOURCE}, exactly three single-parent commits and zero merges. All 232 manifest entries and 10 content-seal targets replayed from the named Git trees. The external receipt hash equals {ILYRA_RECEIPT_SHA256}; its four stale inherited display labels remain a retained zero-credit receipt defect.

The historical route projection is structurally valid but stale and non-authoritative. It assigns v684-v4 to Vesper. Hamish's newer live correction assigns this phase to Auren. This discontinuity is retained rather than rewritten. Prospective Sable v684-v5 routing remains prohibited until Auren's own exact terminal gate and a fresh live reread.

## Retained failures and terminal status

This x1 retains {len(failures)} Auren startup failures at zero credit. Every inherited negative, gap, and gate remains. Same-owner software or synthetic evidence is not independent reproduction. The terminal verdict remains {TERMINAL_VERDICT}.
"""


def main() -> int:
    X1.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)
    inherited = inherited_rows()
    new = new_rows()
    failures = method_failures()
    expected = Counter(row["expected_execution_disposition"] for row in new)

    documents: dict[str, Any] = {
        "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v1", "owner": OWNER, "phase": PHASE,
            "branch": BRANCH, "source_branch": SOURCE_BRANCH, "source": SOURCE,
            "packet_sha256": PACKET_SHA256, "activation_authority": "Hamish newer live correction",
            "work_mode": "solo", "planning_only_x1": True, "successor_precontact": False,
        },
        "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v1", "owner": OWNER, "phase": PHASE,
            "role": "evidence-boundary cartographer and reversible scientific-workflow steward",
            "hope": "turn ambitious ideas into inspectable corrigible questions without erasing wonder or reserved human authority",
            "pronouns": "unspecified", "relational_working_language_only": True,
            "boundary": IDENTITY_BOUNDARY,
        },
        "source-verification.json": {
            "schema": "ghc.family.source-verification.v1", "owner": OWNER, "phase": PHASE,
            "source_branch": SOURCE_BRANCH, "exact_final": SOURCE, "clean": True,
            "local_equals_upstream_equals_tracking_equals_fresh_live": True, "divergence": {"ahead": 0, "behind": 0},
            "direct_chain": [ILYRA_SOURCE, ILYRA_X1, ILYRA_EVIDENCE, SOURCE],
            "new_commit_count": 3, "merge_count": 0,
            "manifest_replay": {"x1": [20, 20], "evidence": [75, 75], "final_delta": [23, 23], "final_owner": [114, 114]},
            "content_seal_replay": [10, 10], "external_receipt_sha256": ILYRA_RECEIPT_SHA256,
            "external_receipt_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "external_receipt_display_defect": "four manifest path labels remained inherited from Eiren while mapped checks ran on Ilyra paths",
            "same_owner_not_independent_reproduction": True,
        },
        "route-plan.json": {
            "schema": "ghc.family.route-plan.v1", "owner": OWNER, "phase": PHASE,
            "historical_projection_owner": "Vesper Arlen", "historical_projection_activation_authority": False,
            "newest_live_owner": OWNER, "route_discontinuity_retained": True,
            "prospective_successor": {"title": "Sable Rook", "phase": "v684-v5", "status": "not_contacted_terminally_gated"},
            "terminal_guards": ["fresh authority", "unique exact title", "immediate reread", "duplicate guard", "privacy", "usage", "safety", "acknowledgement"],
        },
        "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v1", "owner": OWNER, "phase": PHASE,
            "state": "x1_planning_frozen", "steps": [
                "verify immutable source and receipt", "freeze x1", "push and prove x1 equality",
                "materialize bounded x2 only after x1 gate", "freeze and push immutable evidence",
                "close out exact final", "invoke one canonical aggregate once", "route only after terminal guards",
            ],
            "strict_x1_before_x2": True, "one_success_no_replay": True, "file_ceiling": 2000,
        },
        "proposal-chain-audit.json": {
            "schema": "ghc.family.proposal-chain-audit.v1", "owner": OWNER, "phase": PHASE,
            "declared_chain_before": 10850, "inherited_revalidated": 60, "inherited_novelty_credit": 0,
            "new_proposals": 60, "declared_chain_after_x1_freeze": 10910,
            "universal_novelty_claim": False,
        },
        "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v1", "owner": OWNER, "phase": PHASE,
            "planning_only": True, "entry_count": len(inherited), "entries": inherited,
        },
        "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v1", "owner": OWNER, "phase": PHASE,
            "planning_only": True, "entry_count": len(new), "expected_label_counts": dict(expected),
            "allowed_labels": list(ALLOWED_LABELS), "mutation_count": sum(len(r["preregistered_rejecting_mutations"]) for r in new),
            "entries": new,
        },
        "portfolio-freeze.json": portfolio(new),
        "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v1", "owner": OWNER, "phase": PHASE,
            "exact_holds": 20, "blocked_holds": 10, "executed": 0,
            "boundary": "Approval levels organize work; they do not supply evidence, competence, consent, or authority.",
        },
        "skill-runner-plan.json": skill_runner_plan(),
        "clean-fix-refine-plan.json": cfr_plan(),
        "official-primary-source-ledger.json": {
            "schema": "ghc.family.primary-source-ledger.v1", "owner": OWNER, "phase": PHASE,
            "retrieved_date": "2026-09-03", "source_count": len(SOURCES), "sources": SOURCES,
            "citation_is_not_endorsement_or_artifact_validation": True,
        },
        "profession-practice-plan.json": {
            "schema": "ghc.family.practice-plan.v1", "owner": OWNER, "phase": PHASE,
            "primary_pillar": "GMUT Mind", "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "owner_practices": ["synthetic geospatial metadata quality analyst", "synthetic uncertainty-budget documentation analyst"],
            "successor_recommendation": "synthetic museum environmental-monitoring data documentation analyst",
            "employment_or_qualification_claim": False, "real_practice_performed": False,
        },
        "flashcard-plan.json": {
            "schema": "ghc.family.freed-id-four-tier-plan.v1", "owner": OWNER, "phase": PHASE,
            "tiers": ["Auren Lark relational working identity", "GMUT/THOS/Freed-ID-CBR pillars", "two bounded practice lenses", "tasks proposals skills runners failures gates"],
            "minimum_categories": 10, "supersession_is_not_erasure": True,
        },
        "threat-model.json": {
            "schema": "ghc.family.threat-model.v1", "owner": OWNER, "phase": PHASE,
            "threats": ["claim promotion", "real-coordinate ingestion", "identifier leakage", "authority substitution", "failure erasure", "cross-owner mutation", "canonical replay"],
            "controls": ["zero-row fixtures", "synthetic markers", "privacy scan", "held exact gates", "append-only failures", "owner scope", "one-shot latch"],
            "residual_status": "open_gaps_and_exact_gates_remain",
        },
        "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v1", "owner": OWNER, "phase": PHASE,
            "relational_language_only": True, "pause_supported": True, "redirect_supported": True,
            "no_continuity_claim": True, "no_independent_agency_claim": True,
        },
        "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-state.v1", "owner": OWNER, "phase": PHASE,
            "state": "x1_planning", "inherited_sealed_negatives": 58761, "inherited_sealed_methods": 72941,
            "phase_start_failure_count": len(failures), "activation_overlay_negatives": 58761 + len(failures),
            "activation_overlay_methods": 72941 + len(failures), "failures": failures,
            "failed_witnesses_are_zero_credit": True,
        },
        "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v1", "owner": OWNER, "phase": PHASE,
            "state": "PLANNING_ONLY_X1_FROZEN", "terminal_verdict": TERMINAL_VERDICT,
            "allowed_labels": list(ALLOWED_LABELS), "outcomes_claimed": False,
            "empirical_confirmation": False, "professional_authority": False, "production_readiness": False,
            "legal_or_cultural_ratification": False, "maori_authority": False,
            "independent_reproduction": False, "agi_or_asi": False, "consciousness_or_personhood": False,
            "theory_of_everything_proof": False, "stage20_authority": False,
        },
    }

    written: list[Path] = []
    for name, value in documents.items():
        path = X1 / name
        write_json(path, value)
        written.append(path)
    overview_path = X1 / "integrated-overview.md"
    write_text(overview_path, overview(new, failures))
    written.append(overview_path)

    privacy_patterns = {
        "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "secret_marker": re.compile(r"(?i)(api[_-]?key|password|bearer\s+[a-z0-9])"),
        "real_coordinate_pair": re.compile(r"(?i)\b(?:lat(?:itude)?|lon(?:gitude)?)\s*[:=]\s*-?\d"),
        "raw_person_identifier": re.compile(r"(?i)\b(passport|driver.?licen[cs]e|ird)\s*(?:number|no\.?|:)\s*[a-z0-9]"),
    }
    candidates = []
    for path in written:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in privacy_patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name, "text": match.group(0)[:80]})
    confirmed = []
    write_json(
        VALIDATION / "x1-privacy-scan.json",
        {
            "schema": "ghc.family.five-class-privacy-scan.v1", "owner": OWNER, "phase": PHASE,
            "scanned_file_count": len(written), "candidate_count": len(candidates), "candidates": candidates,
            "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
            "bounded_not_complete_privacy_assurance": True,
        },
    )
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v1", "owner": OWNER, "phase": PHASE,
            "review_state": "precommit_exact_allowlist_prepared", "planning_only": True,
            "generated_path_count": len(written) + 3, "x2_paths_present": False, "final_paths_present": False,
            "decision": "eligible_for_exact_x1_staging_after_tests",
        },
    )

    index_paths = written + [
        ROOT / "scripts" / "build_ghc_family_auren_lark_v684_v4_x1.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v684_v4_x1.py",
    ]
    entries = [digest(path) for path in sorted(index_paths, key=lambda item: item.as_posix())]
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1", "owner": OWNER, "phase": PHASE,
            "source": SOURCE, "entry_count": len(entries), "entries": entries,
            "declared_self_exclusions": [
                "docs/auren-lark/v684-v4/validation/x1-index-manifest.json",
                "docs/auren-lark/v684-v4/validation/x1-staged-review.json",
                "docs/auren-lark/v684-v4/validation/x1-privacy-scan.json",
            ],
        },
    )
    print(json.dumps({"status": "AUREN_V684_V4_X1_BUILT", "documents": len(written), "manifest_entries": len(entries), "startup_failures": len(failures)}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
