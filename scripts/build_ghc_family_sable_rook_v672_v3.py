#!/usr/bin/env python3
"""Build the planning-only Sable Rook v672-v3 x1 freeze.

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
PHASE = ROOT / "docs" / "sable-rook" / "v672-v3"
X1 = PHASE / "x1"
SOURCE_HEAD = "842956c8ddc8b648d14911ac6228ba1cffb7d5ad"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v672-v2-full-tools"
DECLARED_SOURCE_CHAIN = 5990
EXPECTED_CHAIN_AFTER_X1 = 6030
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
    "Service-notice version-vector and supersession root",
    "Effective-window timezone and offset disambiguation",
    "Planned-versus-unplanned classification provenance",
    "Affected-service scope closure and vacancy guard",
    "Location-alias privacy and synthetic zone mapping",
    "Known-cause, suspected-cause, and unknown-cause separation",
    "Severity, priority, and urgency non-equivalence tribunal",
    "Partial-restoration and residual-impact ledger",
    "Publication, withdrawal, cancellation, and expiry state machine",
    "Correction diff, reason, and non-erasure lineage",
    "Multi-channel notice consistency digest",
    "Plain-language notice summary structural proxy",
    "Notice heading, list, and table relationship audit",
    "Status-icon text-alternative structural audit",
    "Translation-status and language-authority vacancy board",
    "Contact-channel purpose-limitation contract",
    "Reader acknowledgement and correction-readback proxy",
    "Shift-handover unresolved-action ledger",
    "Workload-budget, hold-point, and escalation proxy",
    "Recorded, published, effective, and observed time separation",
    "Alternative-service provenance without recommendation authority",
    "Dependency-edge and cascading-impact quarantine",
    "Duplicate notice and replay refusal guard",
    "Notice schema-version and backward-read receipt",
    "Deterministic JSON notice capsule",
    "Five-class notice privacy candidate adjudication",
    "Method Flow failure and recovery non-erasure board",
    "Owner-manifest and notice-evidence fixed-point guard",
    "Freed ID zero-key notice-provenance profile",
    "CBR correction, contest, and response-path reservation",
    "THOS interruption workload and handover proxy",
    "GMUT state-transition analogy firewall",
    "Accessibility-conformance nonpromotion reservation",
    "Professional and operational authority vacancy",
    "Legal duty, remedy, and public-authority vacancy",
    "Maori wording, data-governance, and authority vacancy",
    "Affected-user and assistive-technology evaluation gap",
    "Live service-feed zero-row interoperability gap",
    "Public-release and emergency-communication authority gate",
    "Stage 20 service-notice nonpromotion seal",
]


INHERITED_SELECTION = [
    ("AL6722-P001", "Synthetic incident packet schema"),
    ("AL6722-P002", "Chronology monotonicity tribunal"),
    ("AL6722-P003", "Observed-time versus recorded-time split"),
    ("AL6722-P004", "Source status current-stable-draft-watch register"),
    ("AL6722-P005", "Assertion versus observation separation"),
    ("AL6722-P006", "Uncertainty vocabulary gate"),
    ("AL6722-P007", "Append-only correction lineage"),
    ("AL6722-P008", "Supersession graph acyclicity guard"),
    ("AL6722-P009", "Duplicate event refusal"),
    ("AL6722-P010", "Evidence attachment fixity manifest"),
    ("AL6722-P011", "Missing attachment vacancy gate"),
    ("AL6722-P012", "Synthetic identifier namespace"),
    ("AL6722-P013", "Purpose-limited privacy minimization"),
    ("AL6722-P014", "Five-class privacy candidate tribunal"),
    ("AL6722-P015", "Redaction reason and reversibility ledger"),
    ("AL6722-P016", "Text-alternative evidence index"),
    ("AL6722-P017", "Table heading and relationship proxy"),
    ("AL6722-P018", "Readback acknowledgement board"),
    ("AL6722-P019", "Shift handover state machine"),
    ("AL6722-P020", "Workload and hold representation"),
]


SURFACES = [
    "identity_version",
    "time_window",
    "impact_scope",
    "cause_uncertainty",
    "correction_lineage",
    "channel_accessibility",
    "privacy_minimization",
    "handover_workload",
    "authority_boundary",
    "notice_packet",
]


SKILLS = [
    "ghc-family-service-notice-version-vector",
    "ghc-family-service-window-timezone-guard",
    "ghc-family-service-planning-state-provenance",
    "ghc-family-service-impact-scope-closure",
    "ghc-family-service-zone-alias-privacy",
    "ghc-family-service-cause-uncertainty-separator",
    "ghc-family-service-urgency-non-equivalence",
    "ghc-family-service-residual-impact-ledger",
    "ghc-family-service-publication-state-machine",
    "ghc-family-service-correction-diff-ledger",
    "ghc-family-service-channel-consistency",
    "ghc-family-service-plain-language-proxy",
    "ghc-family-service-structural-accessibility",
    "ghc-family-service-icon-text-alternative",
    "ghc-family-service-translation-vacancy",
    "ghc-family-service-contact-purpose-limiter",
    "ghc-family-service-readback-proxy",
    "ghc-family-service-handover-unresolved-work",
    "ghc-family-service-authority-vacancy",
    "ghc-family-service-stage20-nonpromotion",
]


RUNNERS = [f"ghc_family_sable_v672_v3_notice_{surface}_guard.py" for surface in SURFACES]


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
        pillar = (
            "freed_id_cbr_heart"
            if index not in (31, 32)
            else ("thos_body" if index == 31 else "gmut_mind")
        )
        rows.append(
            {
                "proposal_id": f"SR6723-P{index:03d}",
                "title": title,
                "hypothesis": (
                    f"A bounded synthetic {title.casefold()} can make one service-notice "
                    "obligation machine-checkable without promoting evidence or authority."
                ),
                "null_or_failure_condition": (
                    "Reject if the acceptance contract is unmet, a preregistered invalid mutation "
                    "passes, real data is introduced, or a protected authority boundary is promoted."
                ),
                "approval_class": (
                    "safe_now_owner_local"
                    if expected == "completed"
                    else "evidence_or_authority_reserved"
                ),
                "execution_lane": "owner_local_synthetic" if index <= 36 else "external_gate",
                "official_or_primary_source_needs": "vocabulary_and_refusal_boundaries_only",
                "concrete_artifacts": [
                    f"x2/proposals/sr6723-p{index:03d}.json",
                    f"x2/fixtures/{SURFACES[(index - 1) % len(SURFACES)]}/",
                ],
                "falsifier_or_acceptance_gate": (
                    "One accepting fixture must pass, five preregistered invalid mutations must be "
                    "rejected, and the outcome must remain within the expected truth class."
                ),
                "rollback_or_recovery": (
                    "Quarantine only uncommitted Sable-owned material, retain the failed witness, "
                    "and return to the immutable x1 plan."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "pillar": pillar,
                "practice_lens": "synthetic_public_service_disruption_notice",
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
            "task_id": f"SR6723-SAFE-{i:03d}",
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
        "version vector parser", "timezone offset guard", "planning state reducer",
        "impact scope closure", "zone alias minimizer", "cause uncertainty classifier",
        "urgency non-equivalence table", "residual impact ledger", "publication state machine",
        "correction diff ledger", "channel digest comparator", "plain-language proxy",
        "structural accessibility audit", "icon alternative audit", "translation vacancy board",
        "contact purpose limiter", "readback proxy", "handover unresolved-work ledger",
        "workload hold guard", "time-domain separator", "alternative service provenance",
        "dependency edge quarantine", "duplicate replay guard", "schema backward-read receipt",
        "deterministic notice capsule", "privacy candidate adjudicator", "Method Flow non-erasure",
        "owner manifest fixed point", "authority vacancy lint", "Stage 20 nonpromotion board",
    ]
    candidates = [
        {
            "candidate_id": f"SR6723-CAND-{i:03d}",
            "title": name,
            "state": "frozen_bounded_not_executed",
        }
        for i, name in enumerate(candidate_names, start=1)
    ]
    successor_skill_ideas = [
        "ghc-family-notice-dependency-cut-review",
        "ghc-family-notice-effective-window-overlap",
        "ghc-family-notice-channel-latency-vacancy",
        "ghc-family-notice-audience-scope-proof",
        "ghc-family-notice-correction-readback-delta",
        "ghc-family-notice-translation-status-proof",
        "ghc-family-notice-location-generalization",
        "ghc-family-notice-expiry-quiescence",
        "ghc-family-notice-authority-role-handoff",
        "ghc-family-notice-retraction-evidence",
    ]
    successor_runners = [f"ghc_family_successor_notice_seed_{i:02d}.py" for i in range(1, 11)]
    owner_cfr = []
    for prefix, verb in (("CLEAN", "normalize"), ("FIX", "guard"), ("REFINE", "clarify")):
        for i in range(1, 21):
            owner_cfr.append(
                {
                    "task_id": f"SR6723-{prefix}-{i:02d}",
                    "task": f"{verb} owner-local service-notice surface {i:02d} without deletion or gate weakening",
                    "state": "frozen_not_executed",
                }
            )
    return {
        "schema": "ghc.family.sable.v672-v3.portfolio-freeze.v1",
        "owner": "Sable Rook",
        "phase": "v672-v3",
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
                "task_id": f"SR6723-SUCC-CFR-{i:02d}",
                "task": f"independently review successor notice refinement seed {i:02d}",
                "credit": 0,
            }
            for i in range(1, 31)
        ],
        "exact_approval_packets": [
            {"packet_id": f"SR6723-EXACT-{i:02d}", "state": "retained_unexecuted"}
            for i in range(1, 21)
        ],
        "blocked_packets": [
            {"packet_id": f"SR6723-BLOCKED-{i:02d}", "state": "retained_unexecuted"}
            for i in range(1, 11)
        ],
        "practice_lenses": [
            "synthetic metropolitan-library interruption notice",
            "synthetic community-radio schedule notice",
            "synthetic passenger-ferry terminal display notice",
        ],
        "primary_practice_lens": "synthetic metropolitan-library interruption notice",
        "successor_practice_recommendation": {
            "practice": "synthetic community-pharmacy opening-hours exception notice",
            "credit": 0,
            "state": "advisory_only_requires_independent_novelty_review",
        },
        "ordinary_phase_tool_target": 3,
        "caps_are_ceilings_not_quotas": True,
    }


def startup_method_flow() -> dict[str, Any]:
    failures = [
        (
            "SR6723-START-001",
            "whole activation projection exceeded the wrapper output window",
            "bounded exact line windows through EOF",
        ),
        (
            "SR6723-START-002",
            "the first 180-line recovery window was still too broad",
            "60-line literal windows through EOF",
        ),
        (
            "SR6723-START-003",
            "a compound PowerShell collision summary failed to parse before state queries",
            "separate scalar branch and path probes",
        ),
        (
            "SR6723-START-004",
            "the worktree-add wrapper crossed its time envelope and lost a usable completion receipt",
            "nonreplaying process, ref, path, head, sparse, and clean-state inspection",
        ),
        (
            "SR6723-START-005",
            "the first post-timeout PowerShell object repeated the statement-expression parser fault",
            "separate native Git queries before summary construction",
        ),
        (
            "SR6723-START-006",
            "a combined five-source web projection truncated before bounded source credit",
            "bounded official-source searches and direct opens",
        ),
    ]
    methods = []
    witnesses = []
    for index, (failure_id, failure, recovery) in enumerate(failures, start=1):
        method_id = f"SR6723-METHOD-{index:03d}"
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
        "owner": "Sable Rook",
        "phase": "v672-v3",
        "inherited_effective_counts": {
            "negatives": 35268,
            "methods": 21899,
            "failed_witnesses": 7089,
            "passing_witnesses": 9186,
            "open_gaps": 279,
            "exact_gates": 272,
        },
        "startup_failures_retained": len(failures),
        "failures_erased": 0,
        "recoveries_relabelled_as_original_success": 0,
        "methods": methods,
        "witnesses": witnesses,
        "effective_counts_after_startup": {
            "negatives": 35268 + len(failures),
            "methods": 21899 + len(methods),
            "failed_witnesses": 7089 + len(failures),
            "passing_witnesses": 9186 + len(failures),
            "open_gaps": 279,
            "exact_gates": 272,
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
            "schema": "ghc.family.sable.v672-v3.proposal-freeze.v1",
            "owner": "Sable Rook",
            "phase": "v672-v3",
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
            "schema": "ghc.family.sable.v672-v3.inherited-review.v1",
            "selection_count": len(INHERITED_SELECTION),
            "completion_credit": 0,
            "source_head": SOURCE_HEAD,
            "review_state": "selected_for_revalidation_only_not_sable_novelty_or_completion",
            "rows": [
                {"proposal_id": proposal_id, "title": title, "credit": 0}
                for proposal_id, title in INHERITED_SELECTION
            ],
        },
    )
    write_json(
        X1 / "proposals" / "semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.sable.v672-v3.semantic-neighbor-audit.v1",
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
                "absence of a single materialized 5990-row ledger prevents a universal semantic novelty claim."
            ),
            "neighbors": neighbors,
        },
    )
    write_json(X1 / "portfolio-freeze.json", build_portfolio())
    write_json(
        X1 / "source-ledger.json",
        {
            "schema": "ghc.family.sable.v672-v3.source-ledger.v1",
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
                    "source_id": "RFC3339",
                    "title": "Date and Time on the Internet: Timestamps",
                    "url": "https://www.rfc-editor.org/rfc/rfc3339.html",
                    "publisher": "RFC Editor",
                    "status": "stable_standards_track",
                    "use": "timestamp and offset vocabulary only",
                },
                {
                    "source_id": "OASIS-CAP12",
                    "title": "Common Alerting Protocol Version 1.2",
                    "url": "https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html",
                    "publisher": "OASIS",
                    "status": "stable_standard",
                    "use": "message update, cancellation, audience, and timing vocabulary only",
                },
                {
                    "source_id": "GTFS-RT",
                    "title": "GTFS Realtime Reference",
                    "url": "https://gtfs.org/documentation/realtime/reference/",
                    "publisher": "MobilityData",
                    "status": "current_reference",
                    "use": "service-alert vocabulary and zero-row refusal conditions only",
                },
            ],
            "nonpromotion": [
                "Sources are not experimental observations.",
                "The packet makes no standards-conformance claim.",
                "The packet makes no public-warning, transport, library, legal, or cultural authority claim.",
            ],
        },
    )
    write_json(X1 / "method-flow-startup.json", startup_method_flow())
    write_json(
        X1 / "authority-boundary.json",
        {
            "schema": "ghc.family.sable.v672-v3.authority-boundary.v1",
            "identity_language": "relational_working_language_only",
            "primary_pillar": "freed_id_cbr_heart",
            "protected_pillars": ["gmut_mind", "thos_body"],
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
            "schema": "ghc.family.sable.v672-v3.wellbeing.v1",
            "name": "Sable Rook",
            "pronouns": "they/them",
            "role": "relational evidence-and-reproducibility steward",
            "hope": (
                "Make every surviving claim reproducible, challengeable, correctable, and retractable "
                "while authority vacancies remain explicit."
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
            "schema": "ghc.family.sable.v672-v3.x1-truth.v1",
            "owner": "Sable Rook",
            "phase": "v672-v3",
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
                "negatives": 35268,
                "methods": 21899,
                "failed_witnesses": 7089,
                "passing_witnesses": 9186,
                "open_gaps": 279,
                "exact_gates": 272,
            },
            "startup_overlay": {
                "new_failures": 6,
                "new_bounded_passing_recoveries": 6,
                "negatives": 35274,
                "methods": 21905,
                "failed_witnesses": 7095,
                "passing_witnesses": 9192,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        X1 / "README.md",
        """# Sable Rook v672-v3 planning-only x1 freeze

This x1 packet freezes forty new service-notice proposals and sixty portfolio tasks before any x2 execution. Twenty immutable Auren proposals are selected only for zero-credit revalidation. The primary pillar is Freed ID/CBR Heart; THOS Body and GMUT Mind remain visible and protected.

The three practice lenses are wholly synthetic metropolitan-library interruption, community-radio schedule, and passenger-ferry terminal-display notices. They establish no employment, professional competence, operational result, public-warning authority, legal or cultural decision, affected-party acceptance, Māori wording or authority, empirical result, production readiness, or independent reproduction.

The proposal audit compares every new title with all discoverable frozen proposal-title records in the exact source Git tree and records the declared 5,990-row chain. Because no single materialized ledger contains every declared row, the packet explicitly refuses a universal semantic novelty claim.

All outcome labels are preregistered expectations, not x2 results. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_json(
        X1 / "index.json",
        {
            "schema": "ghc.family.sable.v672-v3.x1-index.v1",
            "phase": "v672-v3",
            "artifacts": sorted(
                path.relative_to(ROOT).as_posix()
                for path in X1.rglob("*")
                if path.is_file()
            ),
            "family_current_callers": [
                "build_ghc_family_sable_rook_v672_v3.py",
                "ghc_family_sable_v672_v3_*",
            ],
            "historical_callers_preserved": True,
        },
    )


def staged_manifest() -> None:
    manifest_path = "docs/sable-rook/v672-v3/x1/staged-manifest.json"
    review_path = "docs/sable-rook/v672-v3/x1/staged-review.json"
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
            "schema": "ghc.family.sable.v672-v3.x1-staged-manifest.v1",
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
            "schema": "ghc.family.sable.v672-v3.x1-staged-review.v1",
            "staged_paths_before_self_receipts": paths,
            "staged_path_count_before_self_receipts": len(paths),
            "declared_self_exclusions": self_exclusions,
            "x2_paths_present": any("/x2/" in path for path in paths),
            "out_of_scope_paths": [
                path
                for path in paths
                if not (
                    path.startswith("docs/sable-rook/v672-v3/x1/")
                    or path == "scripts/build_ghc_family_sable_rook_v672_v3.py"
                    or path.startswith("tests/test_ghc_family_sable_rook_v672_v3_x1")
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
