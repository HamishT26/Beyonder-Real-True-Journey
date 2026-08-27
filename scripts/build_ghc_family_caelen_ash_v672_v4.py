#!/usr/bin/env python3
"""Build the planning-only Caelen Ash v672-v4 x1 freeze.

This file deliberately contains no x2 executor, outcome evidence, or completion
credit.  It is frozen with x1 and remains immutable after the x1 commit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v672-v4"
X1 = PHASE / "x1"
SOURCE_HEAD = "2d76e3120bd8f2f2fd70f3ff164ef80e19be3031"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v672-v3-full-tools"
DECLARED_SOURCE_CHAIN = 6030
EXPECTED_CHAIN_AFTER_X1 = 6070
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party",
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


PROPOSAL_TITLES = [
    "Warp-plan version vector and supersession graph",
    "Sett and thread-count dimensional-type guard",
    "Yarn-lot surrogate provenance and substitution ledger",
    "Warp-length allowance arithmetic with measurement vacancy",
    "Reed and heddle compatibility constraint board",
    "Threading draft sequence monotonicity receipt",
    "Tie-up and treadling plan referential-integrity guard",
    "Lift-plan versus treadling-mode non-equivalence",
    "Selvedge instruction and residual-edge reservation",
    "Pattern-repeat boundary and partial-repeat quarantine",
    "Color-order tokenization and contrast nonpromotion",
    "Sample-swatch lineage without material-performance inference",
    "Tension-reading units and calibration-vacancy firewall",
    "Loom setup, weaving, paused, and finished transition guard",
    "Broken-end event and reversible repair-note lineage",
    "Draft-correction diff and prior-version non-erasure",
    "Tool-custody and sharps-safety authority vacancy",
    "Ergonomic hold point and workload-ceiling proxy",
    "Handover unresolved-action and readback ledger",
    "Plain-language threading-instruction structure proxy",
    "Diagram text-alternative and table-relationship audit",
    "Draft-orientation explicitness guard",
    "Ambiguous weaving-symbol legend quarantine",
    "Deterministic weaving-instruction capsule",
    "Five-class privacy scan for synthetic workshop notes",
    "Method Flow failure-recovery non-erasure for craft packet",
    "Git-blob owner-manifest fixed-point guard",
    "Cross-lens separation for handweaving, letterpress, and marquetry",
    "THOS embodied-sequence and workload proxy",
    "GMUT typed lattice-constraint analogy firewall",
    "Freed ID zero-key craft-provenance profile",
    "CBR correction, contest, and responsibility reservation",
    "Accessible weaving-instruction evaluation vacancy",
    "Professional handweaving competence vacancy",
    "Legal, cultural, design-provenance, and remedy vacancy",
    "Māori wording, taonga, mātauranga, data-governance, and authority vacancy",
    "Real weaver, tool, and affected-user evaluation gap",
    "Real loom, yarn, measurement, and interoperability gap",
    "Live workshop operation and safety-release authority gate",
    "Stage 20 craft-workflow nonpromotion seal",
]


INHERITED_SELECTION = [
    ("SR6723-P001", "Service-notice version-vector and supersession root"),
    ("SR6723-P002", "Effective-window timezone and offset disambiguation"),
    ("SR6723-P003", "Planned-versus-unplanned classification provenance"),
    ("SR6723-P004", "Affected-service scope closure and vacancy guard"),
    ("SR6723-P005", "Location-alias privacy and synthetic zone mapping"),
    ("SR6723-P006", "Known-cause, suspected-cause, and unknown-cause separation"),
    ("SR6723-P007", "Severity, priority, and urgency non-equivalence tribunal"),
    ("SR6723-P008", "Partial-restoration and residual-impact ledger"),
    ("SR6723-P009", "Publication, withdrawal, cancellation, and expiry state machine"),
    ("SR6723-P010", "Correction diff, reason, and non-erasure lineage"),
    ("SR6723-P011", "Multi-channel notice consistency digest"),
    ("SR6723-P012", "Plain-language notice summary structural proxy"),
    ("SR6723-P013", "Notice heading, list, and table relationship audit"),
    ("SR6723-P014", "Status-icon text-alternative structural audit"),
    ("SR6723-P015", "Translation-status and language-authority vacancy board"),
    ("SR6723-P016", "Contact-channel purpose-limitation contract"),
    ("SR6723-P017", "Reader acknowledgement and correction-readback proxy"),
    ("SR6723-P018", "Shift-handover unresolved-action ledger"),
    ("SR6723-P019", "Workload-budget, hold-point, and escalation proxy"),
    ("SR6723-P020", "Recorded, published, effective, and observed time separation"),
]


SURFACES = [
    "warp_plan",
    "material_provenance",
    "loom_compatibility",
    "threading_sequence",
    "pattern_lineage",
    "accessibility_structure",
    "privacy_minimization",
    "workload_handover",
    "authority_boundary",
    "weaving_packet",
]


SKILLS = [
    "ghc-family-warp-plan-version-vector",
    "ghc-family-thread-count-dimensional-guard",
    "ghc-family-yarn-lot-provenance-ledger",
    "ghc-family-warp-allowance-vacancy",
    "ghc-family-loom-component-compatibility",
    "ghc-family-threading-sequence-receipt",
    "ghc-family-tieup-treadling-reference-guard",
    "ghc-family-liftplan-mode-separator",
    "ghc-family-selvedge-reservation",
    "ghc-family-pattern-repeat-quarantine",
    "ghc-family-color-order-nonpromotion",
    "ghc-family-swatch-lineage-firewall",
    "ghc-family-tension-calibration-vacancy",
    "ghc-family-loom-state-transition-guard",
    "ghc-family-broken-end-repair-lineage",
    "ghc-family-draft-correction-nonerasure",
    "ghc-family-craft-tool-authority-vacancy",
    "ghc-family-craft-workload-hold",
    "ghc-family-craft-handover-readback",
    "ghc-family-craft-stage20-nonpromotion",
]


RUNNERS = [f"ghc_family_caelen_v672_v4_{surface}_guard.py" for surface in SURFACES]


def run_git(*args: str, input_text: str | None = None) -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        input=input_text,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=True,
    )
    return completed.stdout


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def token_set(value: str) -> set[str]:
    return set(normalized(value).split())


def similarity(left: str, right: str) -> float:
    a, b = token_set(left), token_set(right)
    return len(a & b) / len(a | b) if a and b else 0.0


def iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def source_title_corpus() -> tuple[list[dict[str, str]], list[str]]:
    paths = run_git("ls-tree", "-r", "--name-only", SOURCE_HEAD).splitlines()
    candidates = [
        path
        for path in paths
        if path.endswith(".json")
        and "proposal" in path.casefold()
        and any(word in path.casefold() for word in ("freeze", "ledger", "register"))
    ]
    records: list[dict[str, str]] = []
    parse_failures: list[str] = []
    for path in candidates:
        raw = run_git("show", f"{SOURCE_HEAD}:{path}")
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            parse_failures.append(path)
            continue
        for item in iter_dicts(value):
            title = item.get("title") or item.get("proposal_title")
            if not isinstance(title, str) or not title.strip():
                continue
            proposal_id = item.get("proposal_id") or item.get("id") or "unlabelled"
            records.append(
                {
                    "path": path,
                    "proposal_id": str(proposal_id),
                    "title": title.strip(),
                }
            )
    return records, parse_failures


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        if index <= 28:
            expected = "completed"
        elif index <= 36:
            expected = "represented"
        elif index <= 38:
            expected = "open_gap"
        else:
            expected = "exact_gate"
        if index == 30:
            pillar = "gmut_mind"
        elif index in (31, 32, 35, 36, 40):
            pillar = "freed_id_cbr_heart"
        else:
            pillar = "thos_body"
        approval_class = {
            "completed": "safe_now_owner_local",
            "represented": "bounded_representation_only",
            "open_gap": "open_evidence_gap",
            "exact_gate": "exact_approval_required",
        }[expected]
        execution_lane = {
            "completed": "owner_local_synthetic",
            "represented": "owner_local_representation_only",
            "open_gap": "external_evidence_vacancy",
            "exact_gate": "competent_authority_gate",
        }[expected]
        rows.append(
            {
                "proposal_id": f"CA6724-P{index:03d}",
                "title": title,
                "hypothesis": (
                    f"A bounded synthetic {title.casefold()} can make one craft-workflow "
                    "obligation machine-checkable without promoting evidence, competence, or authority."
                ),
                "null_or_failure_condition": (
                    "Reject if the acceptance contract is unmet, a preregistered invalid mutation "
                    "passes, real data is introduced, or a protected authority boundary is promoted."
                ),
                "approval_class": approval_class,
                "execution_lane": execution_lane,
                "official_or_primary_source_needs": "vocabulary_and_refusal_boundaries_only",
                "concrete_artifacts": [
                    f"x2/proposals/ca6724-p{index:03d}.json",
                    f"x2/fixtures/{SURFACES[(index - 1) % len(SURFACES)]}/",
                ],
                "falsifier_or_acceptance_gate": (
                    "One accepting fixture must pass, five preregistered invalid mutations must be "
                    "rejected, and the outcome must remain within the expected truth class."
                ),
                "rollback_or_recovery": (
                    "Quarantine only uncommitted Caelen-owned material, retain the failed witness, "
                    "and return to the immutable x1 plan."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "pillar": pillar,
                "practice_lens": "synthetic_handweaving_plan_and_handover",
                "surface": SURFACES[(index - 1) % len(SURFACES)],
                "x1_state": "planning_only_no_x2_credit",
            }
        )
    return rows


def build_portfolio() -> dict[str, Any]:
    shared_safe = [
        "source anchor and direct-parent verification",
        "typed zero-divergence and fresh-live equality preflight",
        "discoverable frozen-title corpus extraction",
        "semantic-neighbor readable collision review",
        "official-source status and refusal-boundary review",
        "deterministic JSON and UTF-8 check",
        "exact staged allowlist review",
        "Git-blob manifest fixed-point review",
        "scanner candidate and confirmed-hit separation",
        "identity and wellbeing boundary receipt",
        "authority noncompensation lint",
        "Method Flow failure non-erasure preflight",
        "document word-ceiling review",
        "owner materialization count guard",
        "family-current caller compatibility inventory",
        "x1 immutable blob protection",
        "x2 outcome-vocabulary lint",
        "route hold before terminal proof",
        "one-shot canonical latch preflight",
        "successor recommendations separated from current credit",
    ]
    safe_now = [
        {
            "task_id": f"CA6724-SAFE-{i:03d}",
            "task": (
                f"Preregister and later witness proposal {i:03d} within owner-local bounds"
                if i <= 40
                else shared_safe[i - 41]
            ),
            "state": "frozen_not_executed",
        }
        for i in range(1, 61)
    ]
    candidate_names = [
        "warp-plan version parser", "sett dimensional guard", "yarn-lot provenance reducer",
        "warp allowance vacancy guard", "loom compatibility closure", "threading monotonicity audit",
        "tie-up referential-integrity table", "lift-plan mode separator", "selvedge reservation ledger",
        "repeat-boundary quarantine", "color-order tokenizer", "swatch inference firewall",
        "tension calibration-vacancy audit", "loom-state transition guard", "repair-note lineage board",
        "draft-correction non-erasure", "tool-authority vacancy lint", "workload hold proxy",
        "handover readback ledger", "instruction structure proxy", "diagram alternative audit",
        "orientation explicitness guard", "symbol-legend quarantine", "deterministic weaving capsule",
        "workshop-note privacy adjudicator", "Method Flow craft non-erasure",
        "Git-blob fixed-point guard", "cross-lens separation", "authority noncompensation lint",
        "Stage 20 craft nonpromotion board",
    ]
    candidates = [
        {
            "candidate_id": f"CA6724-CAND-{i:03d}",
            "title": name,
            "state": "frozen_bounded_not_executed",
        }
        for i, name in enumerate(candidate_names, start=1)
    ]
    successor_skill_ideas = [
        "ghc-family-bookbinding-signature-collation",
        "ghc-family-bookbinding-grain-direction-vacancy",
        "ghc-family-bookbinding-adhesive-lot-provenance",
        "ghc-family-bookbinding-board-dimension-guard",
        "ghc-family-bookbinding-sewing-map-lineage",
        "ghc-family-bookbinding-tool-hold-point",
        "ghc-family-bookbinding-accessibility-structure",
        "ghc-family-bookbinding-correction-readback",
        "ghc-family-bookbinding-authority-vacancy",
        "ghc-family-bookbinding-stage20-nonpromotion",
    ]
    successor_runners = [f"ghc_family_successor_bookbinding_seed_{i:02d}.py" for i in range(1, 11)]
    owner_cfr = []
    for prefix, verb in (("CLEAN", "normalize"), ("FIX", "guard"), ("REFINE", "clarify")):
        for i in range(1, 21):
            owner_cfr.append(
                {
                    "task_id": f"CA6724-{prefix}-{i:02d}",
                    "task": f"{verb} owner-local craft-workflow surface {i:02d} without deletion or gate weakening",
                    "state": "frozen_not_executed",
                }
            )
    return {
        "schema": "ghc.family.caelen.v672-v4.portfolio-freeze.v1",
        "owner": "Caelen Ash",
        "phase": "v672-v4",
        "inherited_completion_credit": 0,
        "safe_now_tasks": safe_now,
        "candidate_tasks": candidates,
        "owner_skill_builds": [{"name": name, "state": "planned"} for name in SKILLS],
        "owner_runner_builds": [{"name": name, "state": "planned"} for name in RUNNERS],
        "successor_skill_recommendations": [
            {"name": name, "credit": 0} for name in successor_skill_ideas
        ],
        "successor_runner_recommendations": [
            {"name": name, "credit": 0} for name in successor_runners
        ],
        "owner_clean_fix_refine": owner_cfr,
        "successor_clean_fix_refine_recommendations": [
            {
                "task_id": f"CA6724-SUCC-CFR-{i:02d}",
                "task": f"independently review successor bookbinding refinement seed {i:02d}",
                "credit": 0,
            }
            for i in range(1, 31)
        ],
        "exact_approval_packets": [
            {"packet_id": f"CA6724-EXACT-{i:02d}", "state": "retained_unexecuted"}
            for i in range(1, 21)
        ],
        "blocked_packets": [
            {"packet_id": f"CA6724-BLOCKED-{i:02d}", "state": "retained_unexecuted"}
            for i in range(1, 11)
        ],
        "practice_lenses": [
            "synthetic handweaving loom-plan and handover",
            "synthetic letterpress proof-correction and press handover",
            "synthetic marquetry layout and tool handover",
        ],
        "primary_practice_lens": "synthetic handweaving loom-plan and handover",
        "successor_practice_recommendation": {
            "practice": "synthetic bookbinding collation and bench handover",
            "credit": 0,
            "state": "advisory_only_requires_independent_novelty_review",
        },
        "ordinary_phase_tool_target": 3,
        "caps_are_ceilings_not_quotas": True,
    }


def startup_method_flow() -> dict[str, Any]:
    failures = [
        (
            "CA6724-START-001",
            "the combined source-manifest wrapper validated x1 and evidence but crossed its time envelope before returning the owner-manifest result",
            "retain the timed-out wrapper and run an isolated owner-manifest Git-blob verification, which returned 238 of 238 valid entries",
        ),
        (
            "CA6724-START-002",
            "the no-checkout sparse worktree had an empty index, so the first sparse set and reapply projected 8,672 deletions",
            "run an explicit read-tree materialization at the immutable head, then verify the intended sparse surface and a clean index",
        ),
        (
            "CA6724-START-003",
            "sparse-checkout add rejected an unsupported no-cone option before changing the sparse definition",
            "use the installed add syntax, then inspect the exact sparse patterns and clean state",
        ),
        (
            "CA6724-START-004",
            "the first template-copy map used case-insensitive duplicate keys and failed parser validation before any file write",
            "use an ordered pair list, copy only the eleven declared owner templates, and inspect every resulting untracked path",
        ),
        (
            "CA6724-START-005",
            "the first x1 semantic audit quarantined proposal 33 because its normalized title exactly matched an inherited Sable proposal",
            "retain the rejected title, replace it with a handweaving-specific accessibility-evaluation vacancy, and rerun the complete novelty gate",
        ),
        (
            "CA6724-START-006",
            "the first clean-boundary PowerShell guard used a wildcard that misclassified every staged path as untracked and stopped before commit",
            "inspect the exact two-character porcelain status code, confirm no untracked path and no staged x2 path, then retry the boundary commit",
        ),
    ]
    methods = []
    witnesses = []
    for index, (failure_id, failure, recovery) in enumerate(failures, start=1):
        method_id = f"CA6724-METHOD-{index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "trigger": failure,
                "preferred_method": recovery,
                "state": "preferred_after_bounded_passing_witness",
                "rollback": "stop, preserve the failed witness, and use read-only scalar inspection",
                "sibling_recommendation": recovery,
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": f"{failure_id}-FAIL",
                    "method_id": method_id,
                    "kind": "failed",
                    "credit": 0,
                    "description": failure,
                    "state": "retained_zero_credit",
                },
                {
                    "witness_id": f"{failure_id}-PASS",
                    "method_id": method_id,
                    "kind": "passing",
                    "credit": "bounded_process_only",
                    "description": recovery,
                    "state": "bounded_passing_recovery_not_original_success",
                },
            ]
        )
    return {
        "schema": "ghc.family.method-flow.v10",
        "owner": "Caelen Ash",
        "phase": "v672-v4",
        "inherited_effective_counts": {
            "negatives": 35331,
            "methods": 21940,
            "failed_witnesses": 7152,
            "passing_witnesses": 9226,
            "open_gaps": 281,
            "exact_gates": 274,
        },
        "startup_failures_retained": len(failures),
        "failures_erased": 0,
        "recoveries_relabelled_as_original_success": 0,
        "methods": methods,
        "witnesses": witnesses,
        "effective_counts_after_startup": {
            "negatives": 35331 + len(failures),
            "methods": 21940 + len(methods),
            "failed_witnesses": 7152 + len(failures),
            "passing_witnesses": 9226 + len(failures),
            "open_gaps": 281,
            "exact_gates": 274,
        },
    }


def build_x1() -> None:
    rows = proposals()
    corpus, parse_failures = source_title_corpus()
    unique_by_title: dict[str, dict[str, str]] = {}
    for item in corpus:
        unique_by_title.setdefault(normalized(item["title"]), item)
    neighbors = []
    for proposal in rows:
        ranked = sorted(
            (
                (similarity(proposal["title"], old["title"]), old)
                for old in unique_by_title.values()
            ),
            key=lambda pair: pair[0],
            reverse=True,
        )
        score, nearest = ranked[0] if ranked else (0.0, {"title": "none", "path": "none", "proposal_id": "none"})
        exact = normalized(proposal["title"]) in unique_by_title
        neighbors.append(
            {
                "proposal_id": proposal["proposal_id"],
                "new_title": proposal["title"],
                "nearest_title": nearest["title"],
                "nearest_proposal_id": nearest["proposal_id"],
                "nearest_path": nearest["path"],
                "token_jaccard": round(score, 6),
                "exact_normalized_collision": exact,
                "decision": "quarantine" if exact or score >= 0.8 else "distinct_enough_to_freeze",
            }
        )
    quarantined = [row for row in neighbors if row["decision"] == "quarantine"]
    if quarantined:
        raise SystemExit(f"semantic collision quarantine: {quarantined}")

    write_json(
        X1 / "proposals" / "new-proposal-freeze.json",
        {
            "schema": "ghc.family.caelen.v672-v4.proposal-freeze.v1",
            "owner": "Caelen Ash",
            "phase": "v672-v4",
            "source_proposal_chain": DECLARED_SOURCE_CHAIN,
            "proposal_chain_if_x2_evidence_frozen": EXPECTED_CHAIN_AFTER_X1,
            "proposal_count": len(rows),
            "expected_outcomes": dict(Counter(row["expected_disposition"] for row in rows)),
            "universal_novelty_claimed": False,
            "planning_only": True,
            "inherited_completion_credit": 0,
            "proposals": rows,
        },
    )
    write_json(
        X1 / "proposals" / "inherited-zero-credit-review.json",
        {
            "schema": "ghc.family.caelen.v672-v4.inherited-review.v1",
            "selection_count": len(INHERITED_SELECTION),
            "completion_credit": 0,
            "source_head": SOURCE_HEAD,
            "review_state": "selected_for_revalidation_only_not_caelen_novelty_or_completion",
            "rows": [
                {"proposal_id": proposal_id, "title": title, "credit": 0}
                for proposal_id, title in INHERITED_SELECTION
            ],
        },
    )
    write_json(
        X1 / "proposals" / "semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.caelen.v672-v4.semantic-neighbor-audit.v1",
            "source_head": SOURCE_HEAD,
            "declared_source_chain": DECLARED_SOURCE_CHAIN,
            "proposal_ledger_paths_examined": len({row["path"] for row in corpus}),
            "materialized_title_records_examined": len(corpus),
            "unique_normalized_titles_examined": len(unique_by_title),
            "ledger_parse_failures": parse_failures,
            "exact_collision_count": 0,
            "quarantined_count": 0,
            "universal_semantic_novelty_claimed": False,
            "limitation": (
                "The declared chain count and all discoverable Git-tree proposal-title records were reviewed; "
                "absence of a single materialized 6030-row ledger prevents a universal semantic novelty claim."
            ),
            "neighbors": neighbors,
        },
    )
    write_json(X1 / "portfolio-freeze.json", build_portfolio())
    write_json(
        X1 / "source-ledger.json",
        {
            "schema": "ghc.family.caelen.v672-v4.source-ledger.v1",
            "checked_on": "2026-08-27",
            "citation_is_not_observation": True,
            "real_rows_ingested": 0,
            "network_data_downloads": 0,
            "sources": [
                {
                    "source_id": "W3C-WCAG22",
                    "title": "Web Content Accessibility Guidelines 2.2",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "publisher": "W3C",
                    "status": "current_recommendation",
                    "use": "accessibility vocabulary and structural refusal conditions only",
                },
                {
                    "source_id": "W3C-PROV-O",
                    "title": "PROV-O: The PROV Ontology",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "publisher": "W3C",
                    "status": "stable_recommendation",
                    "use": "revision and provenance vocabulary only",
                },
                {
                    "source_id": "RFC8785",
                    "title": "JSON Canonicalization Scheme",
                    "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                    "publisher": "RFC Editor",
                    "status": "stable_informational_rfc",
                    "use": "deterministic JSON vocabulary and refusal conditions only",
                },
                {
                    "source_id": "OSHA-HAND-POWER-TOOLS",
                    "title": "Hand and Power Tools",
                    "url": "https://www.osha.gov/hand-power-tools",
                    "publisher": "Occupational Safety and Health Administration",
                    "status": "current_official_guidance_page",
                    "use": "tool-hazard and employer-responsibility refusal conditions only",
                },
            ],
            "nonpromotion": [
                "Sources are not experimental observations.",
                "The packet makes no standards-conformance claim.",
                "The packet makes no weaving, letterpress, marquetry, tool-safety, legal, or cultural authority claim.",
            ],
        },
    )
    write_json(X1 / "method-flow-startup.json", startup_method_flow())
    write_json(
        X1 / "authority-boundary.json",
        {
            "schema": "ghc.family.caelen.v672-v4.authority-boundary.v1",
            "identity_language": "relational_working_language_only",
            "primary_pillar": "thos_body",
            "protected_pillars": ["gmut_mind", "freed_id_cbr_heart"],
            "protected_gates": PROTECTED_GATES,
            "noncompensation": (
                "No number of software, symbolic, synthetic, citation, task-topology, or same-owner "
                "witnesses can compensate for missing empirical evidence or competent authority."
            ),
            "verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X1 / "wellbeing-and-identity.json",
        {
            "schema": "ghc.family.caelen.v672-v4.wellbeing.v1",
            "name": "Caelen Ash",
            "pronouns": "they/them",
            "role": "relational uncertainty-and-handover cartographer",
            "hope": (
                "Make every boundary, missing witness, and reversible next step easier to see before "
                "structure is mistaken for authority."
            ),
            "identity_evidence": False,
            "corrigible": True,
            "hamish_may": ["pause", "rename", "redirect", "stop"],
            "workload_state": "bounded_and_within_declared_caps",
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "schema": "ghc.family.caelen.v672-v4.x1-truth.v1",
            "owner": "Caelen Ash",
            "phase": "v672-v4",
            "source_branch": SOURCE_BRANCH,
            "source_head": SOURCE_HEAD,
            "lifecycle": "x1_planning_only",
            "x2_started": False,
            "proposal_count": 40,
            "inherited_review_count": 20,
            "inherited_completion_credit": 0,
            "expected_outcomes": {
                "completed": 28,
                "represented": 8,
                "open_gap": 2,
                "exact_gate": 2,
            },
            "activation_baseline": {
                "negatives": 35331,
                "methods": 21940,
                "failed_witnesses": 7152,
                "passing_witnesses": 9226,
                "open_gaps": 281,
                "exact_gates": 274,
            },
            "startup_overlay": {
                "new_failures": 6,
                "new_bounded_passing_recoveries": 6,
                "negatives": 35337,
                "methods": 21946,
                "failed_witnesses": 7158,
                "passing_witnesses": 9232,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        X1 / "README.md",
        """# Caelen Ash v672-v4 planning-only x1 freeze

This x1 packet freezes forty new craft-workflow proposals and sixty portfolio tasks before any x2 execution. Twenty immutable Sable proposals are selected only for zero-credit revalidation. The primary pillar is THOS Body; GMUT Mind and Freed ID/CBR Heart remain visible and protected.

The three practice lenses are wholly synthetic handweaving loom-plan and handover, letterpress proof-correction and press handover, and marquetry layout and tool handover. They establish no employment, professional competence, operational or tool-safety result, legal or cultural decision, affected-party acceptance, Māori wording or authority, empirical result, production readiness, or independent reproduction.

The proposal audit compares every new title with all discoverable frozen proposal-title records in the exact source Git tree and records the declared 6,030-row chain. Because no single materialized ledger contains every declared row, the packet explicitly refuses a universal semantic novelty claim.

All outcome labels are preregistered expectations, not x2 results. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_json(
        X1 / "index.json",
        {
            "schema": "ghc.family.caelen.v672-v4.x1-index.v1",
            "phase": "v672-v4",
            "artifacts": sorted(
                path.relative_to(ROOT).as_posix()
                for path in X1.rglob("*")
                if path.is_file()
            ),
            "family_current_callers": [
                "build_ghc_family_caelen_ash_v672_v4.py",
                "ghc_family_caelen_v672_v4_*",
            ],
            "historical_callers_preserved": True,
        },
    )


def staged_manifest() -> None:
    manifest_path = "docs/caelen-ash/v672-v4/x1/staged-manifest.json"
    review_path = "docs/caelen-ash/v672-v4/x1/staged-review.json"
    paths = sorted(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines())
    self_exclusions = [manifest_path, review_path]
    entries = []
    privacy_patterns = {
        "raw_uuid_identifier": re.compile(rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
        "private_absolute_windows_path": re.compile(rb"\b[A-Za-z]:\\(?:Users|GHC-Archives|Windows)\\[^\r\n\"']+"),
        "credential_assignment": re.compile(rb"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
        "private_application_route": re.compile(rb"\b(?:app|file|vscode)://[^\s\"']+"),
        "session_stream_marker": re.compile(rb"(?i)\b(?:session[_-]?stream|terminal[_-]?session)\s*[:=]\s*[\"'][^\"']+[\"']"),
    }
    privacy_candidates = []
    for path in paths:
        if path in self_exclusions:
            continue
        blob = subprocess.run(
            ["git", "-C", str(ROOT), "show", f":{path}"],
            capture_output=True,
            check=True,
        ).stdout
        oid = run_git("rev-parse", f":{path}").strip()
        entries.append(
            {
                "path": path,
                "git_blob_oid": oid,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "bytes": len(blob),
            }
        )
        if b"\x00" not in blob:
            for class_name, pattern in privacy_patterns.items():
                for match in pattern.finditer(blob):
                    privacy_candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "offset": match.start(),
                            "disposition": "confirmed_payload_hit",
                        }
                    )
    write_json(
        ROOT / manifest_path,
        {
            "schema": "ghc.family.caelen.v672-v4.x1-staged-manifest.v1",
            "source_head": SOURCE_HEAD,
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": self_exclusions,
            "expected_surface_count_after_self_exclusions": len(entries) + len(self_exclusions),
        },
    )
    write_json(
        ROOT / review_path,
        {
            "schema": "ghc.family.caelen.v672-v4.x1-staged-review.v1",
            "staged_paths_before_self_receipts": paths,
            "staged_path_count_before_self_receipts": len(paths),
            "declared_self_exclusions": self_exclusions,
            "x2_paths_present": any("/x2/" in path for path in paths),
            "out_of_scope_paths": [
                path
                for path in paths
                if not (
                    path.startswith("docs/caelen-ash/v672-v4/x1/")
                    or path == "scripts/build_ghc_family_caelen_ash_v672_v4.py"
                    or path.startswith("tests/test_ghc_family_caelen_ash_v672_v4_x1")
                )
            ],
            "privacy_scan": {
                "class_count": len(privacy_patterns),
                "candidate_count": len(privacy_candidates),
                "confirmed_hit_count": len(privacy_candidates),
                "candidates": privacy_candidates,
            },
            "review_state": "planning_only_surface_reviewed",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "manifest"), default="build", nargs="?")
    args = parser.parse_args()
    if args.mode == "build":
        build_x1()
    else:
        staged_manifest()


if __name__ == "__main__":
    main()
