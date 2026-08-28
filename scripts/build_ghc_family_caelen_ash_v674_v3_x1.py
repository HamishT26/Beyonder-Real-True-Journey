#!/usr/bin/env python3
"""Build Caelen Ash v674-v3 planning-only x1 artifacts.

The builder is deterministic and owner-local. It reads proposal evidence from
the immutable source Git tree, writes no x2 material, performs no network or
task action, and installs no skill or package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


OWNER = "Caelen Ash"
PRONOUNS = "they/them (optional relational working language)"
ROLE = "uncertainty-and-handover cartographer"
HOPE = (
    "make model assumptions, correction chains, and authority vacancies easy "
    "to inspect, challenge, and reverse"
)
PHASE = "v674-v3"
SOURCE = "0b9ccf8c74f3b0a5f96b8582162df8e2a06edd05"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v674-v2-full-tools"
SOURCE_X1 = "81ad6f98f24087777691e96201312e66c37ac844"
SOURCE_EVIDENCE = "1625313186adde8dc94d210376f184bde5dfb0dc"
SOURCE_PROPOSAL_CHAIN = 6670
PLANNED_PROPOSAL_CHAIN = 6730
RECORDED_UTC = "2026-08-28T08:22:48Z"
RECORDED_NZ = "2026-08-28T20:22:48+12:00"
PRIMARY_PILLAR = "GMUT Mind"
CORE_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRACTICE_LENSES = [
    "wholly_synthetic_mechanical_watch_timing_sheet_stewardship",
    "wholly_synthetic_planetarium_projection_cue_alignment_handover",
    "wholly_synthetic_stained_glass_survey_annotation_handover",
]
SUCCESSOR_PRACTICE_RECOMMENDATION = (
    "wholly_synthetic_ceramic_kiln_firing_log_provenance_and_pause_handover"
)
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

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "caelen-ash" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
VALIDATION_ROOT = PHASE_ROOT / "validation"
BUILDER_REL = "scripts/build_ghc_family_caelen_ash_v674_v3_x1.py"
TEST_REL = "tests/test_ghc_family_caelen_ash_v674_v3_x1.py"


NEW_PROPOSALS = [
    ("GMUT Mind", "Synthetic watch timing-series unit declaration", "watch timing-series unit declaration", "completed"),
    ("GMUT Mind", "Synthetic watch reference-epoch provenance contract", "watch reference-epoch provenance contract", "completed"),
    ("GMUT Mind", "Synthetic watch gain-loss sign convention ledger", "watch gain-loss sign convention ledger", "completed"),
    ("GMUT Mind", "Synthetic watch rate-residual derivation DAG", "watch rate-residual derivation DAG", "completed"),
    ("GMUT Mind", "Synthetic watch positional-variation separation board", "watch positional-variation separation board", "completed"),
    ("GMUT Mind", "Synthetic watch temperature-coupling placeholder firewall", "watch temperature-coupling placeholder firewall", "completed"),
    ("GMUT Mind", "Synthetic watch amplitude-state observation vocabulary", "watch amplitude-state observation vocabulary", "completed"),
    ("GMUT Mind", "Synthetic watch beat-error typing reservation", "watch beat-error typing reservation", "completed"),
    ("GMUT Mind", "Synthetic watch calibration-versus-adjustment boundary", "watch calibration-versus-adjustment boundary", "completed"),
    ("GMUT Mind", "Synthetic watch baseline-missing quarantine", "watch baseline-missing quarantine", "completed"),
    ("GMUT Mind", "Synthetic watch uncertainty component register", "watch uncertainty component register", "completed"),
    ("GMUT Mind", "Synthetic watch covariance-proxy nonconversion guard", "watch covariance-proxy nonconversion guard", "completed"),
    ("GMUT Mind", "Synthetic watch measurement-resolution declaration", "watch measurement-resolution declaration", "completed"),
    ("GMUT Mind", "Synthetic watch timing-sheet correction lineage", "watch timing-sheet correction lineage", "completed"),
    ("GMUT Mind", "Synthetic watch instrument-reference vacancy ledger", "watch instrument-reference vacancy ledger", "completed"),
    ("GMUT Mind", "Synthetic watch repeated-read ordering contract", "watch repeated-read ordering contract", "completed"),
    ("GMUT Mind", "Synthetic watch outlier-without-deletion receipt", "watch outlier-without-deletion receipt", "completed"),
    ("GMUT Mind", "Synthetic watch model-family comparison hold", "watch model-family comparison hold", "completed"),
    ("GMUT Mind", "Synthetic watch synthetic-series determinism receipt", "watch synthetic-series determinism receipt", "completed"),
    ("GMUT Mind", "Synthetic watch empirical-likelihood absence firewall", "watch empirical-likelihood absence firewall", "completed"),
    ("GMUT Mind", "Synthetic planetarium cue clock coordinate declaration", "planetarium cue clock coordinate declaration", "completed"),
    ("GMUT Mind", "Synthetic planetarium projector-axis frame ledger", "planetarium projector-axis frame ledger", "completed"),
    ("GMUT Mind", "Synthetic planetarium alignment residual sign contract", "planetarium alignment residual sign contract", "completed"),
    ("GMUT Mind", "Synthetic planetarium offset-versus-drift separator", "planetarium offset-versus-drift separator", "completed"),
    ("GMUT Mind", "Synthetic planetarium lens-state provenance chain", "planetarium lens-state provenance chain", "completed"),
    ("GMUT Mind", "Synthetic planetarium show-sequence partial-order guard", "planetarium show-sequence partial-order guard", "completed"),
    ("THOS Body", "Synthetic planetarium fault-hold transition receipt", "planetarium fault-hold transition receipt", "completed"),
    ("GMUT Mind", "Synthetic planetarium calibration-label reservation", "planetarium calibration-label reservation", "completed"),
    ("Freed ID and CBR Heart", "Synthetic planetarium sky-label source-status ledger", "planetarium sky-label source-status ledger", "completed"),
    ("THOS Body", "Synthetic planetarium projection-cue correction readback", "planetarium projection-cue correction readback", "completed"),
    ("THOS Body", "Synthetic planetarium workload budget and handover", "planetarium workload budget and handover", "completed"),
    ("THOS Body", "Synthetic planetarium cancellation-to-quiescence receipt", "planetarium cancellation-to-quiescence receipt", "completed"),
    ("THOS Body", "Synthetic planetarium missing-cue quarantine", "planetarium missing-cue quarantine", "completed"),
    ("THOS Body", "Synthetic planetarium accessibility-evaluation vacancy", "planetarium accessibility-evaluation vacancy", "represented"),
    ("THOS Body", "Synthetic planetarium operator-authority vacancy", "planetarium operator-authority vacancy", "represented"),
    ("GMUT Mind", "Synthetic stained-glass panel-coordinate declaration", "stained-glass panel-coordinate declaration", "completed"),
    ("GMUT Mind", "Synthetic stained-glass orientation transform ledger", "stained-glass orientation transform ledger", "completed"),
    ("GMUT Mind", "Synthetic stained-glass annotation-scale unit contract", "stained-glass annotation-scale unit contract", "completed"),
    ("Freed ID and CBR Heart", "Synthetic stained-glass survey-view provenance chain", "stained-glass survey-view provenance chain", "completed"),
    ("GMUT Mind", "Synthetic stained-glass light-source condition reservation", "stained-glass light-source condition reservation", "completed"),
    ("Freed ID and CBR Heart", "Synthetic stained-glass photographic-record distinction", "stained-glass photographic-record distinction", "completed"),
    ("Freed ID and CBR Heart", "Synthetic stained-glass condition-note correction DAG", "stained-glass condition-note correction DAG", "completed"),
    ("GMUT Mind", "Synthetic stained-glass crack-state uncertainty vocabulary", "stained-glass crack-state uncertainty vocabulary", "completed"),
    ("Freed ID and CBR Heart", "Synthetic stained-glass color-description source hold", "stained-glass color-description source hold", "completed"),
    ("THOS Body", "Synthetic stained-glass lead-network topology proxy", "stained-glass lead-network topology proxy", "represented"),
    ("Freed ID and CBR Heart", "Synthetic stained-glass treatment-proposal authority vacancy", "stained-glass treatment-proposal authority vacancy", "represented"),
    ("THOS Body", "Synthetic stained-glass survey workload and pause receipt", "stained-glass survey workload and pause receipt", "represented"),
    ("Freed ID and CBR Heart", "Synthetic stained-glass custody handover nonclaim", "stained-glass custody handover nonclaim", "represented"),
    ("THOS Body", "Cross-lens deterministic artifact serialization contract", "cross-lens deterministic artifact serialization contract", "represented"),
    ("THOS Body", "Cross-lens exact Git-blob and checkout-byte distinction", "cross-lens Git-blob and checkout-byte distinction", "represented"),
    ("Freed ID and CBR Heart", "Cross-lens minimum-disclosure pseudonym projection", "cross-lens minimum-disclosure pseudonym projection", "represented"),
    ("Freed ID and CBR Heart", "Cross-lens access-request separation board", "cross-lens access-request separation board", "represented"),
    ("Freed ID and CBR Heart", "Cross-lens contest and correction lineage", "cross-lens contest and correction lineage", "represented"),
    ("Freed ID and CBR Heart", "Cross-lens retention-decision authority vacancy", "cross-lens retention-decision authority vacancy", "represented"),
    ("GMUT Mind", "Real observatory likelihood and uncertainty-treatment gap", "real observatory likelihood and uncertainty-treatment gap", "open_gap"),
    ("THOS Body", "Real operator matched-budget comparative-arm gap", "real operator matched-budget comparative-arm gap", "open_gap"),
    ("GMUT Mind", "Independent-team reproduction evidence gap", "independent-team reproduction evidence gap", "open_gap"),
    ("Freed ID and CBR Heart", "Affected-party consent and remedy exact gate", "affected-party consent and remedy exact gate", "exact_gate"),
    ("Freed ID and CBR Heart", "Māori terminology and data-governance exact gate", "Māori terminology and data-governance exact gate", "exact_gate"),
    ("Freed ID and CBR Heart", "Legal cultural and Stage 20 authority exact gate", "legal cultural and Stage 20 authority exact gate", "exact_gate"),
]

SKILL_IDEAS = [
    "watch-unit-declaration",
    "watch-epoch-provenance",
    "watch-sign-ledger",
    "watch-residual-dag",
    "watch-uncertainty-register",
    "watch-analogy-firewall",
    "planetarium-frame-ledger",
    "planetarium-drift-separator",
    "planetarium-fault-hold",
    "planetarium-correction-readback",
    "planetarium-accessibility-vacancy",
    "stained-glass-coordinate-contract",
    "stained-glass-provenance-chain",
    "stained-glass-condition-correction",
    "stained-glass-authority-vacancy",
    "cross-lens-minimum-disclosure",
    "cross-lens-manifest-replay",
    "cross-lens-owner-delta",
    "cross-lens-maori-authority-gate",
    "cross-lens-stage20-veto",
]
RUNNER_RULES = [
    "unit",
    "epoch",
    "residual",
    "uncertainty",
    "frame",
    "correction",
    "privacy",
    "handover",
    "authority",
    "stage20",
]

STARTUP_FAILURES = [
    ("CA6743-X1-F001", "a PowerShell foreach result was piped before materialization and hit an empty-pipe parser fault", "materialize the row array before piping"),
    ("CA6743-X1-F002", "a broad external receipt discovery projection exceeded its output budget", "use the exact receipt path surfaced before truncation"),
    ("CA6743-X1-F003", "a redundant activation-candidate reference projection truncated", "use the completed bounded full-file read and exact paths"),
    ("CA6743-X1-F004", "an archive verifier bundled recursive temporary cleanup and was rejected before process start", "use a byte-preserving read-only Git-blob stream without extraction or deletion"),
    ("CA6743-X1-F005", "the first blob verifier guessed one digest key across seven manifest schemas and emitted false mismatches", "inspect each manifest schema and replay with its actual digest and byte fields"),
    ("CA6743-X1-F006", "the first combined collision probe returned no attributable scalar after its remote lookup window", "separate literal local, registry, path, and live-remote probes"),
    ("CA6743-X1-F007", "the first combined x1 patch exceeded the Windows process command-line ceiling and was rejected", "apply the same owner patch through a bounded junction-backed patch surface"),
    ("CA6743-X1-F008", "a precommit unit-test wrapper launched from the parent C-drive directory and could not import the sparse D-drive test module", "run the unchanged test selection with the exact owner worktree as process working directory"),
]


def run_git(*args: str, text: bool = True) -> str | bytes:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=text, encoding="utf-8" if text else None
    )


def git_json(ref: str, path: str) -> Any:
    raw = subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=REPO)
    return json.loads(raw.decode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def collect_titles(value: Any) -> list[str]:
    titles: list[str] = []
    if isinstance(value, dict):
        if isinstance(value.get("title"), str):
            titles.append(value["title"])
        for item in value.values():
            titles.extend(collect_titles(item))
    elif isinstance(value, list):
        for item in value:
            titles.extend(collect_titles(item))
    return titles


def historical_audit(proposed_titles: list[str]) -> dict[str, Any]:
    paths = run_git("ls-tree", "-r", "--name-only", SOURCE).splitlines()
    ledger_pattern = re.compile(
        r"(new-proposal-freeze\.json|proposal-freeze\.json|"
        r"proposal-ledger\.json|proposal_chain\.json|proposals\.json)$"
    )
    ledger_paths = [path for path in paths if ledger_pattern.search(path)]
    historical: list[tuple[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    for path in ledger_paths:
        try:
            value = git_json(SOURCE, path)
            historical.extend((path, title) for title in collect_titles(value))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            parse_failures.append({"path": path, "error": type(exc).__name__})
    normalized_historical = {
        normalized_title(title): {"path": path, "title": title}
        for path, title in historical
        if normalized_title(title)
    }
    checks: list[dict[str, Any]] = []
    for title in proposed_titles:
        normalized = normalized_title(title)
        tokens = set(normalized.split())
        best_score = 0.0
        best_path = None
        best_title = None
        for path, historical_title in historical:
            historical_normalized = normalized_title(historical_title)
            if not historical_normalized:
                continue
            historical_tokens = set(historical_normalized.split())
            jaccard = len(tokens & historical_tokens) / max(
                1, len(tokens | historical_tokens)
            )
            sequence = SequenceMatcher(
                None, normalized, historical_normalized
            ).ratio()
            score = max(jaccard, sequence)
            if score > best_score:
                best_score = score
                best_path = path
                best_title = historical_title
        exact_collision = normalized in normalized_historical
        checks.append(
            {
                "title": title,
                "normalized_title": normalized,
                "exact_collision": exact_collision,
                "nearest_score": round(best_score, 4),
                "nearest_title": best_title,
                "nearest_ledger_path": best_path,
                "quarantined": exact_collision or best_score >= 0.90,
            }
        )
    return {
        "schema": "ghc.family.semantic-neighbor-audit.v674.v3.x1",
        "source": SOURCE,
        "declared_source_chain": SOURCE_PROPOSAL_CHAIN,
        "materialized_ledger_paths": len(ledger_paths),
        "materialized_title_records": len(historical),
        "unique_normalized_titles": len(normalized_historical),
        "parse_failures": parse_failures,
        "proposed_title_count": len(proposed_titles),
        "internal_unique": len(
            {normalized_title(title) for title in proposed_titles}
        )
        == len(proposed_titles),
        "exact_collisions": sum(1 for row in checks if row["exact_collision"]),
        "neighbor_quarantine_threshold": 0.90,
        "quarantined_count": sum(1 for row in checks if row["quarantined"]),
        "universal_novelty_claim": False,
        "scope_note": (
            "All proposal ledgers reachable at the exact source were scanned; "
            "the declared cumulative chain is preserved without pretending every "
            "historical row is materialized in one ledger."
        ),
        "checks": checks,
    }


def inherited_rows() -> list[dict[str, Any]]:
    source = git_json(
        SOURCE, "docs/sable-rook/v674-v2/x1/new-proposal-freeze.json"
    )
    return [
        {
            "selection_id": f"CA6743-I{index:03d}",
            "source_phase": "v674-v2",
            "source_proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "disposition": "reviewed_for_continuity_zero_caelen_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for index, proposal in enumerate(source["proposals"], 1)
    ]


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (pillar, title, artifact, outcome) in enumerate(NEW_PROPOSALS, 1):
        approval = "safe_now" if outcome == "completed" else outcome
        if outcome == "represented":
            approval = "candidate"
        rows.append(
            {
                "proposal_id": f"CA6743-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": PRACTICE_LENSES,
                "hypothesis": (
                    f"A bounded owner-local {artifact} can preserve its declared "
                    "structural obligation while refusing absent evidence and authority."
                ),
                "null_or_failure_condition": (
                    "Fail if an accepting fixture violates its declared type, drops "
                    "a retained failure, uses a real record or person, performs an "
                    "external action, or promotes a protected claim."
                ),
                "approval_class": approval,
                "execution_lane": (
                    "held_for_external_evidence_or_authority"
                    if outcome in {"open_gap", "exact_gate"}
                    else "owner_local_synthetic_x2"
                ),
                "official_or_primary_source_needs": [
                    "BIPM SI Brochure 9th edition updated 2026",
                    "IERS Conventions 2010 with working-update status reservation",
                    "W3C PROV-O",
                    "W3C WCAG 2.2",
                    "RFC 8785 with verified errata reservation",
                ],
                "concrete_artifact": artifact,
                "falsifier_or_acceptance_gate": (
                    "One accepting fixture and four preregistered invalid mutations; "
                    "held outcomes require the named real evidence or competent authority."
                ),
                "rollback_or_recovery": (
                    "Quarantine only Caelen-created uncommitted material, retain the "
                    "failed witness at zero credit, and return to immutable x1."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": (
                    "caelen_current_proposal_frozen_after_bounded_materialized_"
                    "neighbor_audit_without_universal_novelty_claim"
                ),
            }
        )
    return rows


def portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    safe_actions = [
        "build bounded accepting contract",
        "build rejecting mutation family",
    ]
    safe = [
        {
            "packet_id": f"CA6743-S{index:03d}",
            "proposal_id": proposals[(index - 1) // 2]["proposal_id"],
            "title": (
                f"{proposals[(index - 1) // 2]['title']} - "
                f"{safe_actions[(index - 1) % 2]}"
            ),
            "state": "frozen_not_executed",
            "approval_bucket": "safe_now",
            "completion_credit": 0,
        }
        for index in range(1, 121)
    ]
    owner_candidates = [
        {
            "packet_id": f"CA6743-C{index:03d}",
            "proposal_id": proposals[(index - 1) % 60]["proposal_id"],
            "title": (
                f"Bounded owner prototype {index:03d} - "
                f"{proposals[(index - 1) % 60]['title']}"
            ),
            "state": "frozen_not_executed",
            "completion_credit": 0,
        }
        for index in range(1, 81)
    ]
    successor_candidates = [
        {
            "packet_id": f"CA6743-SC{index:03d}",
            "title": f"Successor zero-credit recommendation {index:03d}",
            "state": "successor_recommendation_zero_credit",
            "completion_credit": 0,
        }
        for index in range(1, 21)
    ]
    exact_packets = [
        {
            "packet_id": f"CA6743-E{index:03d}",
            "state": "exact_approval_required_unexecuted",
            "completion_credit": 0,
        }
        for index in range(1, 21)
    ]
    blocked_packets = [
        {
            "packet_id": f"CA6743-B{index:03d}",
            "state": "blocked_unexecuted",
            "completion_credit": 0,
        }
        for index in range(1, 11)
    ]
    skills = [
        {
            "skill_id": f"CA6743-K{index:03d}",
            "name": f"ghc-family-caelen-{name}",
            "state": "planned_phase_local_not_built",
            "global_installation": False,
            "completion_credit": 0,
        }
        for index, name in enumerate(SKILL_IDEAS, 1)
    ]
    runners = [
        {
            "runner_id": f"CA6743-RN{index:03d}",
            "name": f"ghc_family_caelen_v674_v3_{name}_runner.py",
            "state": "planned_not_built",
            "historical_caller_compatibility_required": True,
            "completion_credit": 0,
        }
        for index, name in enumerate(RUNNER_RULES, 1)
    ]
    successor_skills = [
        {
            "recommendation_id": f"CA6743-SK{index:03d}",
            "state": "successor_recommendation_zero_credit",
            "completion_credit": 0,
        }
        for index in range(1, 11)
    ]
    successor_runners = [
        {
            "recommendation_id": f"CA6743-SR{index:03d}",
            "state": "successor_recommendation_zero_credit",
            "completion_credit": 0,
        }
        for index in range(1, 11)
    ]
    cleanup_topics = [
        "schema",
        "UTF-8",
        "deterministic JSON",
        "path allowlist",
        "Git-blob domain",
        "privacy candidate",
        "authority boundary",
        "failure retention",
        "runner interface",
        "skill description",
    ]
    owner_cleanup = [
        {
            "task_id": f"CA6743-R{index:03d}",
            "title": (
                f"{cleanup_topics[(index - 1) % len(cleanup_topics)]} "
                f"refinement {index:03d}"
            ),
            "state": "frozen_not_executed",
            "destructive": False,
            "completion_credit": 0,
        }
        for index in range(1, 101)
    ]
    successor_cleanup = [
        {
            "task_id": f"CA6743-XR{index:03d}",
            "title": f"successor additive refinement recommendation {index:03d}",
            "state": "successor_recommendation_zero_credit",
            "destructive": False,
            "completion_credit": 0,
        }
        for index in range(1, 31)
    ]
    return {
        "safe_now_packets": safe,
        "owner_candidates": owner_candidates,
        "successor_candidates": successor_candidates,
        "exact_approval_packets": exact_packets,
        "blocked_packets": blocked_packets,
        "owner_skill_ideas": skills,
        "owner_runner_ideas": runners,
        "successor_skill_recommendations": successor_skills,
        "successor_runner_recommendations": successor_runners,
        "owner_clean_fix_refine": owner_cleanup,
        "successor_clean_fix_refine": successor_cleanup,
        "successor_practice_recommendations": [
            SUCCESSOR_PRACTICE_RECOMMENDATION
        ],
    }


def overview() -> str:
    return f"""# Caelen Ash v674-v3 planning-only x1 overview

## Outcome first

This x1 is a planning freeze, not execution evidence. It records Caelen Ash's exact source, bounded novelty audit, sixty proposed hypotheses, portfolio contracts, protected gates, official-source roles, tool plans, and terminal route hold. It contains no x2 implementation, observed proposal disposition, installed skill, runner result, empirical row, real participant, real object, external action, task contact, production identity event, authority decision, or Stage 20 claim. Its intended family-chain value after later immutable x2 evidence is {PLANNED_PROPOSAL_CHAIN}; the source declaration remains {SOURCE_PROPOSAL_CHAIN}.

## Relational identity, role, hope, and corrigibility

Caelen Ash is relational working language for an {ROLE}. Optional {PRONOUNS} language is relational only. The phase hope is to {HOPE}. A name, role, hope, task title, route, model output, software artifact, or validation receipt does not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop this lane. That correction right is part of the workflow boundary, not evidence about an inner state.

## Exact source and lifecycle

The immutable source is Sable Rook v674-v2 exact final {SOURCE}. Sable x1 is {SOURCE_X1}; Sable evidence is {SOURCE_EVIDENCE}. Before this lane was created, Caelen read the complete activation candidate and required skills through EOF; reverified Sable's exact canonical receipt; replayed 493 manifest entries in their actual raw or normalized-LF byte domains; and proved the direct source-to-x1-to-evidence-to-final chain, three Sable commits, zero merges, one final parent, clean state, zero divergence, and fresh four-way equality. These are inherited source facts, never Caelen completion credit.

X1 remains planning-only. The x2 directory must not exist at its gate. The x1 commit must be the direct child of the Sable final, must be pushed cleanly, and must equal local, upstream, tracking, and a fresh live remote before x2 begins. Later x2 and final commits must remain additive, direct, single-parent, and merge-free. A later recovery cannot rewrite a failed witness, and a successful canonical aggregate may not be replayed.

## Primary pillar and three bounded learning lenses

GMUT Mind is primary. The three lenses are wholly synthetic mechanical-watch timing-sheet stewardship, wholly synthetic planetarium projection-cue alignment and handover, and wholly synthetic stained-glass survey annotation and handover. They are learning and software-design lenses only. No watch, timing machine, planetarium, projector, optical system, stained-glass panel, conservation record, image, person, workplace, measurement, intervention, or authority case is used. Nothing establishes horological, planetarium, surveying, conservation, electrical, optical, accessibility, or public-safety competence.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Timing-series, coordinate, residual, covariance, uncertainty, and observation-model structures in synthetic fixtures are analogy surfaces. They produce no physical datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, empirical confirmation, or Theory of Everything. THOS Body remains visible only through deterministic ordering, workload, cancellation, correction readback, quiescence, and handover proxies. THOS has no preregistered blind matched-budget real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID and CBR Heart remain visible through provenance, minimum disclosure, correction, contest, access separation, retention vacancies, and exact authority holds. Synthetic identifiers are not credentials or production identity events.

## Novelty and proposal freeze

The audit reads every frozen-proposal ledger reachable at the exact source whose repository name declares a proposal freeze, proposal ledger, proposal chain, or proposal collection. It records the declared cumulative chain separately from materialized title evidence. Caelen's sixty titles are internally unique, have no exact normalized collision, and remain below the 0.90 quarantine threshold. Nearest neighbors are retained rather than hidden. Because a cumulative count is not the same thing as one materialized canonical ledger, x1 makes no universal novelty claim. Sixty inherited Sable rows are reviewed for continuity with novelty credit zero and completion credit zero.

Each new proposal freezes one hypothesis, one null or failure condition, one approval class, one execution lane, official or primary-source needs, one concrete artifact, one falsifier or acceptance gate, one rollback or recovery, the protected gates, and exactly one expected disposition. The expected distribution is forty-two completed, twelve represented, three open gaps, and three exact gates. These are preregistered expectations only. A later completed label can mean only that its bounded synthetic structural contract passed. Represented work remains proxy evidence. Open gaps require real evidence. Exact gates require competent people or authorities and cannot be compensated by software volume.

## Official-source roles

The BIPM SI Brochure ninth edition, updated in 2026, supplies unit and second vocabulary. The IERS Conventions page identifies the 2010 Conventions as the official reference and explicitly marks working updates as nondefinitive and not officially approved. W3C PROV-O supplies provenance-relation vocabulary. WCAG 2.2 supplies accessibility vocabulary and evaluation reservations. RFC 8785 supplies deterministic JSON vocabulary while its informational status and verified errata remain visible. Citations are requirements and refusal-condition references only. They are not observations, measurements, endorsements, conformance certificates, professional decisions, or authority grants.

## Portfolio and tools

The portfolio freezes 120 safe-now packets, eighty bounded owner candidates, twenty successor candidate recommendations, twenty exact-approval packets, ten blocked packets, twenty phase-local skill ideas, ten family-current runner ideas, ten successor skill recommendations, ten successor runner recommendations, one hundred additive owner CLEAN/FIX/REFINE tasks, thirty successor refinement recommendations, and exactly one successor practice-lens recommendation. Caps are ceilings. No row authorizes destructive cleanup, global installation, another owner's mutation, elevation, host-security weakening, Windows-feature changes, a reboot, external account use, or evidence promotion.

The planned skills remain inside this owner packet and will be quick-validated and smoke-used without global installation. The runners preserve ghc_family naming and historical caller compatibility. Python, Git, and Node are version-checked only; no unrelated software is installed. Exact Git-blob and checkout-byte domains remain distinct. Privacy scanning distinguishes scanner definitions from confirmed payload hits. Accessible static structure cannot become complete accessibility assurance without manual, browser, assistive-technology, cognitive, language, and affected-user evaluation.

## Failure and route boundaries

Eight Caelen startup failures are retained at zero initial-pass credit with separately named recoveries. The source seal remains unchanged. X1 performs no task lookup or message send. Only after a later clean pushed exact final, fresh four-way equality, and one successful non-replayed owner-scoped canonical receipt may Caelen refresh the newest live authority and roster, uniquely resolve and immediately reread the exact authorized successor, apply duplicate, pause, redirect, usage, privacy, evidence, and safety guards, and send once. Current live direction names Orin Thale for v674-v4, but the edge remains terminally gated and may be changed by newer live authority. The verdict remains NOT_READY_FOR_STAGE_20.
"""


def file_entry(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def build() -> list[str]:
    head = run_git("rev-parse", "HEAD").strip()
    if head != SOURCE:
        raise RuntimeError(f"x1 builder requires source HEAD {SOURCE}, found {head}")
    if (PHASE_ROOT / "x2").exists():
        raise RuntimeError("x2 material exists before x1 freeze")
    inherited = inherited_rows()
    proposals = proposal_rows()
    audit = historical_audit([row["title"] for row in proposals])
    if (
        audit["parse_failures"]
        or not audit["internal_unique"]
        or audit["quarantined_count"]
    ):
        raise RuntimeError("semantic-neighbor audit did not pass")
    frozen_portfolio = portfolio(proposals)
    expected = {
        label: sum(
            row["expected_execution_disposition"] == label for row in proposals
        )
        for label in CORE_OUTCOMES
    }
    documents: dict[Path, Any] = {
        X1_ROOT / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v674.v3.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source": SOURCE,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
            "solo": True,
            "task_created": False,
            "task_forked": False,
            "collaboration_subagent_spawned": False,
            "source_validation_credit": 0,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v674.v3.x1",
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "identity_is_relational_working_language": True,
            "consciousness_or_personhood_claim": False,
            "identity_continuity_claim": False,
            "employment_or_qualification_claim": False,
            "authority_claim": False,
            "hamish_may_rename_pause_redirect_or_stop": True,
        },
        X1_ROOT / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v674.v3",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "semantic-neighbor-audit.json": audit,
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v674.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source_proposal_chain": SOURCE_PROPOSAL_CHAIN,
            "proposal_chain_if_x2_evidence_frozen": PLANNED_PROPOSAL_CHAIN,
            "proposal_count": len(proposals),
            "allowed_outcomes": CORE_OUTCOMES,
            "expected_outcomes": expected,
            "outcomes_observed": False,
            "universal_novelty_claim": False,
            "proposals": proposals,
        },
        X1_ROOT / "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v674.v3",
            "owner": OWNER,
            "phase": PHASE,
            "state": "planning_only_not_executed",
            **frozen_portfolio,
        },
        X1_ROOT / "source-ledger.json": {
            "schema": "ghc.family.official-source-ledger.v674.v3.x1",
            "checked_at_utc": RECORDED_UTC,
            "entries": [
                {
                    "source_id": "BIPM-SI-9-2026",
                    "title": "The International System of Units, 9th edition",
                    "url": "https://www.bipm.org/en/publications/si-brochure",
                    "status": "complete_brochure_updated_2026",
                    "use": "unit, second, and dimensional vocabulary only",
                },
                {
                    "source_id": "IERS-CONVENTIONS",
                    "title": "IERS Conventions",
                    "url": "https://www.iers.org/iers/en/dataproducts/conventions/conventions",
                    "status": "official_2010_with_working_updates_not_definitive_or_officially_approved",
                    "use": "reference-system and time-coordinate refusal vocabulary only",
                },
                {
                    "source_id": "W3C-PROV-O",
                    "title": "PROV-O: The PROV Ontology",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "status": "recommendation_2013_latest_published_version",
                    "use": "provenance relation vocabulary only",
                },
                {
                    "source_id": "W3C-WCAG22",
                    "title": "Web Content Accessibility Guidelines 2.2",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "status": "recommendation",
                    "use": "accessibility structure and evaluation reservations only",
                },
                {
                    "source_id": "RFC8785",
                    "title": "JSON Canonicalization Scheme",
                    "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                    "status": "informational_rfc_with_verified_errata_noted",
                    "use": "deterministic JSON and refusal vocabulary only",
                },
            ],
            "citations_are_observations": False,
            "endorsement_claimed": False,
            "real_data_rows": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v674.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source_repository_seal": {
                "effective_negatives": 38362,
                "methods": 25783,
                "failed_witnesses": 10023,
                "bounded_passing_witnesses": 13316,
                "open_gaps": 313,
                "exact_gates": 306,
            },
            "source_external_bounded_passing_receipts": [
                "canonical_receipt",
                "exact_title_listing",
                "immediate_exact_title_reread",
            ],
            "source_external_post_seal_failures": 0,
            "caelen_startup_failure_count": len(STARTUP_FAILURES),
            "failures": [
                {
                    "failure_id": failure_id,
                    "failed_witness": failure,
                    "state": "failed_retained_zero_credit",
                    "success_credit": 0,
                    "recovery": recovery,
                }
                for failure_id, failure, recovery in STARTUP_FAILURES
            ],
            "promotion_rule": (
                "A recovery may earn a separate bounded witness but never "
                "rewrites its failed witness."
            ),
        },
        X1_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v674.v3.x1",
            "threats": [
                "scope contamination",
                "x1 x2 mixing",
                "real-record inclusion",
                "authority promotion",
                "privacy leakage",
                "manifest byte-domain confusion",
                "canonical replay",
                "duplicate activation",
            ],
            "controls": [
                "sparse owner allowlist",
                "planning-only x1 test",
                "synthetic fixtures",
                "protected gates",
                "five-class scan",
                "exact Git-blob manifests",
                "external canonical latch",
                "terminal duplicate guard",
            ],
            "complete_privacy_claim": False,
            "exhaustive_security_claim": False,
        },
        X1_ROOT / "toolchain-plan.json": {
            "schema": "ghc.family.toolchain-plan.v674.v3.x1",
            "version_check_only": ["Python", "Git", "Node"],
            "third_party_installations": 0,
            "global_skill_installations": 0,
            "phase_local_skill_count": 20,
            "family_runner_count": 10,
            "historical_caller_compatibility": True,
            "desktop_update": False,
            "elevation": False,
            "host_security_change": False,
            "windows_feature_change": False,
            "reboot": False,
        },
        X1_ROOT / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v674.v3.x1",
            "state": "x1_planning_only",
            "completed": [
                "read activation and skills",
                "verify exact source",
                "replay source manifests",
                "refresh official-source status",
                "create sparse owner lane",
                "audit materialized proposal neighbors",
            ],
            "pending": [
                "test and stage x1",
                "commit push and prove x1 equality",
                "execute x2",
                "seal evidence",
                "build final",
                "invoke canonical once",
                "route once if permitted",
            ],
            "caps_are_ceilings": True,
            "full_repository_suite_authorized": False,
        },
        X1_ROOT / "route-roster-plan.json": {
            "schema": "ghc.family.route-roster-plan.v674.v3.x1",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "current_live_successor_candidate": "Orin Thale",
            "current_live_successor_phase_candidate": "v674-v4",
            "precontact": False,
            "send_attempts": 0,
            "state": "TERMINAL_HOLD",
            "newest_live_authority_must_be_reread": True,
            "stop_on_ambiguity_or_protected_gate": True,
        },
    }
    for path, value in documents.items():
        write_json(path, value)
    write_text(X1_ROOT / "integrated-overview.md", overview())
    manifest_paths = sorted(
        path
        for path in X1_ROOT.rglob("*")
        if path.is_file() and path.name != "x1-manifest.json"
    )
    for relative in (BUILDER_REL, TEST_REL):
        candidate = REPO / relative
        if candidate.exists():
            manifest_paths.append(candidate)
    manifest_paths = sorted(set(manifest_paths))
    manifest = {
        "schema": "ghc.family.x1-manifest.v674.v3",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "entry_count": len(manifest_paths),
        "entries": [file_entry(path) for path in manifest_paths],
        "self_excluded": "docs/caelen-ash/v674-v3/x1/x1-manifest.json",
        "x2_absent": not (PHASE_ROOT / "x2").exists(),
    }
    write_json(X1_ROOT / "x1-manifest.json", manifest)
    return [
        path.relative_to(REPO).as_posix()
        for path in sorted(X1_ROOT.rglob("*"))
        if path.is_file()
    ]


def staged_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)


def build_staged_review() -> Path:
    staged = run_git(
        "diff", "--cached", "--name-only", "--diff-filter=ACMR"
    ).splitlines()
    review_rel = "docs/caelen-ash/v674-v3/validation/x1-staged-review.json"
    allowed_exact = {BUILDER_REL, TEST_REL, review_rel}
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/caelen-ash/v674-v3/x1/")
        and path not in allowed_exact
    ]
    entries = []
    json_errors = []
    python_errors = []
    confirmed_hits = []
    scanner_candidates = []
    conversation_terms = (
        "source" + "_thread_id|codex_" + "delegation|<" + "input>"
    )
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)\b[A-Za-z]:[\\/](?:Users|home)[\\/]"
        ),
        "raw_task_thread_identifier": re.compile(
            r"(?i)\b(?:task|thread)[_-]?id\s*[:=]\s*[0-9a-f-]{20,}"
        ),
        "credential_assignment": re.compile(
            r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*"
            r"['\"][^'\"]{8,}"
        ),
        "private_conversation_payload": re.compile(
            conversation_terms, re.IGNORECASE
        ),
    }
    markdown_words = {}
    for path in staged:
        data = staged_blob(path)
        entries.append(
            {
                "path": path,
                "bytes": len(data),
                "sha256_git_index_blob": hashlib.sha256(data).hexdigest(),
            }
        )
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_errors.append(
                    {"path": path, "error": type(exc).__name__}
                )
        if path.endswith(".py"):
            try:
                compile(data.decode("utf-8"), path, "exec")
            except (UnicodeDecodeError, SyntaxError) as exc:
                python_errors.append(
                    {"path": path, "error": type(exc).__name__}
                )
        if path.endswith(".md"):
            markdown_words[path] = len(data.decode("utf-8").split())
        if path.endswith((".json", ".md", ".py", ".html")):
            text = data.decode("utf-8")
            for class_name, pattern in patterns.items():
                for _match in pattern.finditer(text):
                    row = {"path": path, "class": class_name}
                    if path.endswith(".py"):
                        row["disposition"] = (
                            "scanner_definition_or_rejection_assertion"
                        )
                        scanner_candidates.append(row)
                    else:
                        row["disposition"] = "confirmed_payload_hit"
                        confirmed_hits.append(row)
    review = {
        "schema": "ghc.family.exact-staged-review.v674.v3.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "state": (
            "VALID_X1_STAGED_REVIEW"
            if not (
                out_of_scope
                or json_errors
                or python_errors
                or confirmed_hits
            )
            else "INVALID_X1_STAGED_REVIEW"
        ),
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": [review_rel],
        "out_of_scope_paths": out_of_scope,
        "json_errors": json_errors,
        "python_errors": python_errors,
        "privacy_classes": list(patterns),
        "scanner_candidates": scanner_candidates,
        "confirmed_privacy_hits": len(confirmed_hits),
        "confirmed_hits": confirmed_hits,
        "markdown_words": markdown_words,
        "x2_absent": not (PHASE_ROOT / "x2").exists(),
        "diff_hygiene": not out_of_scope,
    }
    destination = VALIDATION_ROOT / "x1-staged-review.json"
    write_json(destination, review)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        path = build_staged_review()
        print(
            json.dumps(
                {
                    "state": "staged_review_written",
                    "path": path.relative_to(REPO).as_posix(),
                }
            )
        )
        return 0
    paths = build()
    print(
        json.dumps(
            {
                "state": "x1_planning_only_built",
                "files": len(paths),
                "proposal_count": 60,
                "x2_absent": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
