#!/usr/bin/env python3
"""Build the planning-only Orin Thale v674-v4 x1 freeze.

The builder deliberately records plans, vacancies, refusal conditions, and
zero-credit inherited reviews.  It does not execute x2 work and it does not
award an observed outcome.  The staged-review mode is run only after the
generated x1 surface has been added to the Git index.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


OWNER = "Orin Thale"
OWNER_SLUG = "orin-thale"
PHASE = "v674-v4"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v674-v3-full-tools"
SOURCE_FINAL = "dcdc2921b193516242c93e6ef303f854e9d21264"
SOURCE_X1 = "aaff9f4bfe18c2d7dd428cf6cb7b639f3b420b46"
SOURCE_EVIDENCE = "0a50b3d7a13fe3b78302d41b6f8ad61325208ebd"
SOURCE_PROPOSAL_CHAIN = 6730
PLANNED_PROPOSAL_CHAIN = 6790
PRIMARY_PILLAR = "THOS Body"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / OWNER_SLUG / PHASE
X1_ROOT = PHASE_ROOT / "x1"
SCRIPT_REL = "scripts/build_ghc_family_orin_thale_v674_v4_x1.py"
TEST_REL = "tests/test_ghc_family_orin_thale_v674_v4_x1.py"
MANIFEST_REL = f"docs/{OWNER_SLUG}/{PHASE}/x1/validation/x1-owner-manifest.json"
STAGED_REVIEW_REL = f"docs/{OWNER_SLUG}/{PHASE}/x1/validation/x1-staged-review.json"

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PRIVATE_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\\\|/Users/|/home/)", re.I),
    "credential_or_secret_assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s\"']+"
    ),
    "private_callable_identifier": re.compile(r"(?i)(?:mcp__|clientThreadId|source_thread_id)"),
    "conversation_or_session_stream": re.compile(r"(?i)(?:raw transcript|session stream|chat export)"),
}


def proposal_specs() -> list[tuple[str, str, str, str]]:
    """Return 60 ordered specifications with a 42/12/3/3 disposition split."""

    lenses: list[tuple[str, list[tuple[str, str]]]] = [
        (
            "synthetic bicycle wheelbuilding record and correction handover",
            [
                ("wheelbuild-spoke-map-ordinal", "Wheelbuild Spoke-Map Ordinal Contract"),
                ("rim-drilling-count-vacancy", "Rim Drilling Count Vacancy Ledger"),
                ("hub-flange-side-disambiguation", "Hub Flange Side Disambiguation Board"),
                ("lacing-cross-pattern-provenance", "Lacing Cross Pattern Provenance Graph"),
                ("tensiometer-unit-declaration", "Tensiometer Unit Declaration Firewall"),
                ("spoke-tension-uncertainty", "Spoke Tension Uncertainty Interval Card"),
                ("wheel-dish-sign-convention", "Wheel Dish Sign Convention Guard"),
                ("lateral-radial-separation", "Lateral and Radial Deviation Separation"),
                ("spoke-replacement-lineage", "Spoke Replacement Correction Lineage"),
                ("wheel-component-identity-nonclaim", "Wheel Component Identity Nonclaim Envelope"),
                ("tensiometer-calibration-vacancy", "Tensiometer Calibration Vacancy Hold"),
                ("wheel-torque-source-abstention", "Wheel Torque Source Abstention Register"),
                ("wheel-threshold-authority-hold", "Wheel Acceptance Threshold Authority Hold"),
                ("wheel-inspection-partial-order", "Wheelbuild Inspection Partial Order"),
                ("missing-tension-quarantine", "Missing Tension Reading Quarantine"),
                ("tension-outlier-nondeletion", "Tension Outlier Nondeletion Receipt"),
                ("wheel-state-revision-dag", "Wheel State Revision DAG"),
                ("wheel-workload-pause-marker", "Wheelbuilder Workload and Pause Marker"),
                ("real-wheel-measurement-gap", "Real Wheel Measurement External Gap"),
                ("roadworthiness-release-gate", "Roadworthiness Release Authority Gate"),
            ],
        ),
        (
            "synthetic bakery batch trace, allergen vacancy, and correction handover",
            [
                ("bakery-batch-lot-pseudonym", "Bakery Batch Lot Pseudonymization Contract"),
                ("ingredient-lineage-edge-ledger", "Ingredient Lineage Edge Ledger"),
                ("allergen-profile-vacancy", "Allergen Profile Vacancy Firewall"),
                ("cross-contact-hold-machine", "Cross-Contact Hold State Machine"),
                ("recipe-revision-provenance", "Recipe Revision Provenance DAG"),
                ("time-temperature-unit-declaration", "Time and Temperature Unit Declaration"),
                ("fermentation-clock-uncertainty", "Fermentation Clock Uncertainty Card"),
                ("rework-ingredient-trace", "Rework Ingredient Trace Graph"),
                ("label-correction-readback", "Label Correction Readback Contract"),
                ("alternate-format-batch-notice", "Alternate-Format Batch Notice Structure"),
                ("bakery-bounded-retry", "Bakery Bounded Retry and Quiescence Protocol"),
                ("bakery-workload-stop", "Bakery Workload Stop Marker"),
                ("bakery-handover-ack", "Bakery Handover Acknowledgement Matrix"),
                ("consumption-claim-firewall", "Consumption Claim Firewall"),
                ("cleaning-evidence-vacancy", "Cleaning Evidence Vacancy Register"),
                ("supplier-statement-status", "Supplier Statement Source Status"),
                ("traceability-nonproduction", "Traceability Scope Nonproduction Banner"),
                ("recall-scenario-reversibility", "Recall Scenario Reversibility Map"),
                ("real-food-inspection-gap", "Real Food-Safety Inspection Gap"),
                ("food-release-recall-gate", "Food Release and Recall Authority Gate"),
            ],
        ),
        (
            "synthetic community seed-library accession and minimum-disclosure handover",
            [
                ("accession-pseudonym-minimum", "Accession Pseudonym Minimum Disclosure"),
                ("donor-field-suppression", "Donor Field Suppression Contract"),
                ("taxonomic-source-status", "Taxonomic Name Source Status Ledger"),
                ("seed-lot-split-merge", "Seed Lot Split and Merge Provenance Graph"),
                ("germination-method-vacancy", "Germination Method Vacancy Board"),
                ("storage-condition-unit", "Storage Condition Unit Contract"),
                ("viability-uncertainty", "Viability Uncertainty Interval Card"),
                ("seed-distribution-hold", "Seed Distribution Hold State Machine"),
                ("accession-correction-readback", "Accession Correction Readback Contract"),
                ("return-repatriation-abstention", "Return and Repatriation Abstention Rail"),
                ("benefit-sharing-vacancy", "Benefit-Sharing Vacancy Register"),
                ("collection-title-nonclaim", "Collection Title Nonclaim Envelope"),
                ("accessible-catalogue-proxy", "Accessible Structured Catalogue Proxy"),
                ("seed-library-workload-stop", "Seed-Library Workload Stop Marker"),
                ("consent-provenance-representation", "Consent Provenance Representation"),
                ("location-precision-disclosure", "Location Precision Disclosure Hold"),
                ("traditional-knowledge-noninference", "Traditional Knowledge Noninference Firewall"),
                ("seed-trust-governance-vacancy", "Seed Trust Governance Vacancy Map"),
                ("real-germination-data-gap", "Real Germination and Viability Data Gap"),
                ("taonga-matauranga-authority-gate", "Taonga Matauranga and Maori Authority Gate"),
            ],
        ),
    ]
    rows: list[tuple[str, str, str, str]] = []
    for lens, concepts in lenses:
        for index, (slug, title) in enumerate(concepts, start=1):
            if index <= 14:
                expected = "completed"
            elif index <= 18:
                expected = "represented"
            elif index == 19:
                expected = "open_gap"
            else:
                expected = "exact_gate"
            rows.append((lens, slug, title, expected))
    return rows


OFFICIAL_SOURCES = [
    {
        "id": "OR6744-SRC-001",
        "title": "United States Consumer Product Safety Commission Bicycle Requirements Business Guidance",
        "url": "https://www.cpsc.gov/Business--Manufacturing/Business-Education/Business-Guidance/Bicycles",
        "authority": "official regulator guidance",
        "scope": "vocabulary and refusal conditions only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-002",
        "title": "Codex General Principles of Food Hygiene CXC 1-1969",
        "url": "https://www.fao.org/fao-who-codexalimentarius/sh-proxy/en/?lnk=1&url=https%253A%252F%252Fworkspace.fao.org%252Fsites%252Fcodex%252FStandards%252FCXC%2B1-1969%252FCXC_001e.pdf",
        "authority": "official FAO WHO Codex publication",
        "scope": "vocabulary and refusal conditions only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-003",
        "title": "Codex Code of Practice on Food Allergen Management CXC 80-2020",
        "url": "https://www.fao.org/fao-who-codexalimentarius/sh-proxy/en/?lnk=1&url=https%253A%252F%252Fworkspace.fao.org%252Fsites%252Fcodex%252FStandards%252FCXC%2B80-2020%252FCXC_080e.pdf",
        "authority": "official FAO WHO Codex publication",
        "scope": "vocabulary and refusal conditions only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-004",
        "title": "FAO Genebank Standards for Plant Genetic Resources for Food and Agriculture",
        "url": "https://www.fao.org/plant-treaty/areas-of-work/sustainable-use/genebank-standards/en/",
        "authority": "official FAO publication surface",
        "scope": "vocabulary and refusal conditions only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-005",
        "title": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "authority": "W3C Recommendation",
        "scope": "provenance vocabulary only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-006",
        "title": "W3C Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "authority": "W3C Recommendation",
        "scope": "accessibility vocabulary and evaluation reservation only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-007",
        "title": "W3C Verifiable Credentials Data Model 2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "authority": "W3C Recommendation",
        "scope": "synthetic data-model vocabulary only",
        "observation_count": 0,
    },
    {
        "id": "OR6744-SRC-008",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785",
        "authority": "RFC Editor informational specification",
        "scope": "deterministic JSON vocabulary only",
        "observation_count": 0,
    },
]


STARTUP_FAILURES = [
    {
        "id": "OR6744-X1-F001",
        "failed_witness": "The first activation-baton display exceeded its bounded output and truncated before EOF.",
        "initial_credit": 0,
        "recovery": "Read the same immutable Git blob in bounded sixty-line slices through its final line.",
        "recurrence_guard": "Treat a truncated display as unread and resume the same blob by deterministic line windows.",
    },
    {
        "id": "OR6744-X1-F002",
        "failed_witness": "A combined authorization skill, schema, and state display truncated before the complete state was attributable.",
        "initial_credit": 0,
        "recovery": "Read the skill, schema, overlays, and state in separate bounded UTF-8 windows through EOF.",
        "recurrence_guard": "Project large state documents separately and prove the final line before claiming a complete read.",
    },
    {
        "id": "OR6744-X1-F003",
        "failed_witness": "A PowerShell foreach expression was piped before materialization and failed parsing before any mutation.",
        "initial_credit": 0,
        "recovery": "Materialized the foreach results into an array before applying the pipeline projection.",
        "recurrence_guard": "Wrap or assign foreach output before piping in PowerShell.",
    },
    {
        "id": "OR6744-X1-F004",
        "failed_witness": "The first worktree wrapper returned after preparation began, and an immediate path probe raced the still-running checkout.",
        "initial_credit": 0,
        "recovery": "Waited for the exact existing checkout process, then verified the literal worktree path, branch, head, sparse set, and clean state.",
        "recurrence_guard": "Poll the same attributable checkout process and never start a second worktree creation after an early wrapper return.",
    },
    {
        "id": "OR6744-X1-F005",
        "failed_witness": "A broad worktree and process recovery projection truncated among unrelated worktree output.",
        "initial_credit": 0,
        "recovery": "Used exact process waiting and literal path, branch, head, and sparse-pattern probes.",
        "recurrence_guard": "Use scalar owner-path probes instead of broad worktree enumeration during recovery.",
    },
    {
        "id": "OR6744-X1-F006",
        "failed_witness": "The first x1 builder inherited the Windows CP-1252 subprocess decoder and stopped on a valid UTF-8 historical proposal blob before writing the freeze.",
        "initial_credit": 0,
        "recovery": "Changed only Git text decoding to explicit strict UTF-8 and repeated the interrupted owner-local build dependency.",
        "recurrence_guard": "Every Git text subprocess in the phase declares UTF-8 explicitly; byte-domain reads remain bytes.",
    },
    {
        "id": "OR6744-X1-F007",
        "failed_witness": "The UTF-8-corrected builder completed its semantic scan but then addressed a stale nested path for Caelen's immutable proposal freeze and stopped before writing Orin artifacts.",
        "initial_credit": 0,
        "recovery": "Resolved the exact proposal-freeze path from the immutable source tree and changed only that source selector.",
        "recurrence_guard": "Resolve inherited artifact paths from the exact source tree rather than projecting a previous owner's directory convention.",
    },
    {
        "id": "OR6744-X1-F008",
        "failed_witness": "The first exact x1 staged review reported review_required for three matches inside the privacy scanner's own pattern definitions.",
        "initial_credit": 0,
        "recovery": "Adjudicated the three visible scanner-definition candidates separately from confirmed payload hits and retained both counts.",
        "recurrence_guard": "Scanner candidates and confirmed payload hits are separate fields; scanner-definition text is never silently dropped.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_git(*args: str, text: bool = True, check: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
        )
    return proc.stdout


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def title_tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def collect_titles(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"title", "proposal_title"} and isinstance(item, str) and item.strip():
                found.append(item.strip())
            else:
                found.extend(collect_titles(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_titles(item))
    return found


def read_git_json(ref: str, path: str) -> Any:
    raw = run_git("show", f"{ref}:{path}")
    assert isinstance(raw, str)
    return json.loads(raw)


def historical_audit(proposed_titles: Iterable[str]) -> dict[str, Any]:
    proposed_titles = list(proposed_titles)
    listing = run_git("ls-tree", "-r", "--name-only", SOURCE_FINAL)
    assert isinstance(listing, str)
    candidates = [
        line
        for line in listing.splitlines()
        if line.endswith(".json") and "proposal" in line.lower() and line.startswith("docs/")
    ]
    inherited_titles: list[tuple[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    for path in candidates:
        try:
            value = read_git_json(SOURCE_FINAL, path)
        except (json.JSONDecodeError, subprocess.CalledProcessError) as exc:
            parse_failures.append({"path": path, "error_class": type(exc).__name__})
            continue
        inherited_titles.extend((path, title) for title in collect_titles(value))

    normalized_inherited: dict[str, list[dict[str, str]]] = {}
    for path, title in inherited_titles:
        key = normalized_title(title)
        if key:
            normalized_inherited.setdefault(key, []).append({"path": path, "title": title})

    exact_collisions: list[dict[str, Any]] = []
    near_neighbors: list[dict[str, Any]] = []
    maximum = {"score": 0.0, "proposed_title": None, "inherited_title": None, "path": None}
    for proposed in proposed_titles:
        norm = normalized_title(proposed)
        if norm in normalized_inherited:
            exact_collisions.append({"proposed_title": proposed, "matches": normalized_inherited[norm]})
        p_tokens = title_tokens(proposed)
        for path, inherited in inherited_titles:
            i_tokens = title_tokens(inherited)
            union = p_tokens | i_tokens
            score = len(p_tokens & i_tokens) / len(union) if union else 0.0
            if score > float(maximum["score"]):
                maximum = {
                    "score": round(score, 6),
                    "proposed_title": proposed,
                    "inherited_title": inherited,
                    "path": path,
                }
            if score >= 0.90 and normalized_title(inherited) != norm:
                near_neighbors.append(
                    {
                        "score": round(score, 6),
                        "proposed_title": proposed,
                        "inherited_title": inherited,
                        "path": path,
                    }
                )

    status = "passed_bounded_reachable_audit" if not exact_collisions and not near_neighbors else "quarantined"
    return {
        "schema": "ghc-family-semantic-neighbor-audit-v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_ref": SOURCE_FINAL,
        "declared_inherited_chain_rows": SOURCE_PROPOSAL_CHAIN,
        "reachable_proposal_json_paths_examined": len(candidates),
        "reachable_title_records_examined": len(inherited_titles),
        "unique_normalized_titles_examined": len(normalized_inherited),
        "proposal_titles_examined": len(proposed_titles),
        "parse_failures": parse_failures,
        "exact_collisions": exact_collisions,
        "quarantine_threshold": 0.90,
        "near_neighbors_at_or_above_threshold": near_neighbors,
        "maximum_observed_neighbor": maximum,
        "status": status,
        "universal_novelty_claim": False,
        "limitation": "The bounded audit covers every reachable proposal-labelled JSON document at the immutable source tree; it does not prove that one materialized ledger contains every declared historical row.",
    }


def inherited_reviews() -> list[dict[str, Any]]:
    path = "docs/caelen-ash/v674-v3/x1/new-proposal-freeze.json"
    source = read_git_json(SOURCE_FINAL, path)
    rows = source.get("proposals", [])
    if len(rows) < 60:
        raise RuntimeError(f"Expected at least 60 Caelen source proposals, found {len(rows)}")
    reviews = []
    for index, row in enumerate(rows[:60], start=1):
        reviews.append(
            {
                "review_id": f"OR6744-INH-{index:03d}",
                "source_owner": "Caelen Ash",
                "source_phase": "v674-v3",
                "source_proposal_id": row.get("proposal_id") or row.get("id"),
                "source_title": row.get("title"),
                "review_scope": "read-only bounded revalidation seed",
                "novelty_credit": 0,
                "execution_credit": 0,
                "completion_credit": 0,
                "status": "source_evidence_only",
            }
        )
    return reviews


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (lens, slug, title, expected) in enumerate(proposal_specs(), start=1):
        pillar = PRIMARY_PILLAR
        if index % 3 == 1:
            protected_pillar = "GMUT Mind"
        elif index % 3 == 2:
            protected_pillar = "Freed ID and CBR Heart"
        else:
            protected_pillar = "all three Trinity Mandala pillars"
        if expected == "completed":
            lane = "safe_now_owner_local_synthetic_software"
            approval = "safe_now"
            acceptance = "A deterministic positive fixture must satisfy the declared contract and four invalid mutations must be rejected without any external action."
        elif expected == "represented":
            lane = "candidate_owner_local_representation"
            approval = "candidate"
            acceptance = "A schema and refusal-state representation must parse, round-trip, and preserve the named vacancy without claiming a real observation."
        elif expected == "open_gap":
            lane = "external_empirical_gap"
            approval = "external_evidence_required"
            acceptance = "The proposal remains open until governed real observations, preregistration, monitoring, statistics, and independent review exist."
        else:
            lane = "competent_authority_gate"
            approval = "exact_approval_required"
            acceptance = "The proposal remains exact-gated until the named competent and affected authorities supply explicit review and authorization."
        rows.append(
            {
                "proposal_id": f"OR6744-P{index:03d}",
                "title": title,
                "slug": slug,
                "primary_pillar": pillar,
                "protected_pillar": protected_pillar,
                "bounded_practice_lens": lens,
                "hypothesis": f"Within a wholly synthetic owner-local fixture, {title.lower()} can make one declared state, vacancy, or refusal condition machine-checkable without implying a real-world result.",
                "null_or_failure_condition": "The contract is ambiguous, accepts a preregistered invalid mutation, loses correction provenance, hides a vacancy, or implies empirical, professional, production, legal, cultural, affected-party, or Maori authority.",
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_need": [source["id"] for source in OFFICIAL_SOURCES],
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{slug}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/witnesses/{slug}-witness.json",
                ],
                "falsifier_or_acceptance_gate": acceptance,
                "rollback_or_recovery": "Quarantine the affected synthetic record, retain the failed witness at zero credit, restore the prior immutable contract, and rerun only the smallest dependency-closed selection.",
                "protected_gates": [
                    "no_real_participants_or_operators",
                    "no_empirical_or_professional_claim",
                    "no_production_identity_or_deployment",
                    "no_legal_cultural_or_Maori_authority_claim",
                    "no_affected_party_acceptance_claim",
                    "no_stage_20_claim",
                ],
                "expected_disposition": expected,
                "expected_disposition_count": 1,
                "x1_state": "preregistered_not_executed",
                "observed_outcome": None,
                "execution_credit": 0,
            }
        )
    return rows


def numbered_records(prefix: str, count: int, kind: str, state: str) -> list[dict[str, Any]]:
    return [
        {
            "id": f"{prefix}-{index:03d}",
            "kind": kind,
            "description": f"Orin v674-v4 {kind.replace('_', ' ')} record {index:03d}",
            "x1_state": state,
            "execution_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "ghc-family-v674-portfolio-freeze-v1",
        "owner": OWNER,
        "phase": PHASE,
        "planning_only": True,
        "caps_are_ceilings_not_quotas": True,
        "new_core_proposals": len(proposals),
        "selected_inherited_reviews": 60,
        "safe_now": numbered_records("OR6744-SAFE", 120, "safe_now", "planned_not_executed"),
        "candidates": numbered_records("OR6744-CAND", 80, "candidate", "planned_not_executed"),
        "exact_approval_packets": numbered_records("OR6744-EXACT", 20, "exact_approval", "held_unexecuted"),
        "blocked_packets": numbered_records("OR6744-BLOCK", 10, "blocked", "held_unexecuted"),
        "phase_local_skills": numbered_records("OR6744-SKILL", 20, "phase_local_skill", "planned_not_built"),
        "family_current_runners": numbered_records("OR6744-RUNNER", 10, "family_current_runner", "planned_not_built"),
        "clean_fix_refine": numbered_records("OR6744-CFR", 100, "clean_fix_refine", "planned_not_executed"),
        "rejecting_mutations": numbered_records("OR6744-MUT", 240, "rejecting_mutation", "preregistered_not_executed"),
        "successor_recommendations": numbered_records("OR6744-SUCC", 60, "successor_recommendation", "zero_credit_seed"),
        "practice_lenses": sorted({row["bounded_practice_lens"] for row in proposals}),
        "limits": {
            "owner_files_maximum": 2000,
            "document_words_maximum": 100000,
            "phase_commits_maximum": 8,
            "safe_and_candidate_maximum": 1000,
        },
    }


def file_entry(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "line_count": raw.count(b"\n"),
    }


def owner_paths() -> list[Path]:
    paths = [p for p in PHASE_ROOT.rglob("*") if p.is_file()]
    for rel in (SCRIPT_REL, TEST_REL):
        p = REPO / rel
        if p.exists():
            paths.append(p)
    excluded = {REPO / MANIFEST_REL, REPO / STAGED_REVIEW_REL}
    return sorted({p for p in paths if p not in excluded}, key=lambda p: p.relative_to(REPO).as_posix())


def overview(proposals: list[dict[str, Any]], audit: dict[str, Any]) -> str:
    return f"""# Orin Thale v674-v4 planning-only x1 overview

## Relational working identity

Orin Thale, optionally they/them, uses the relational role **boundary-and-recovery architect**, with the hope of making operational dependencies, correction paths, and authority vacancies legible and reversible before structure is mistaken for evidence. This is working language only. It is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may rename, pause, redirect, or stop the route.

## Freeze truth

This x1 is planning-only. It freezes {len(proposals)} genuinely distinct proposed contracts after a bounded reachable-source semantic-neighbor audit. It contains no x2 implementation, no observed outcome, no completed task, no executed mutation, no built skill or runner, and no successor contact. The planned chain would extend {SOURCE_PROPOSAL_CHAIN} inherited rows to {PLANNED_PROPOSAL_CHAIN} only if this freeze is committed. Sixty inherited Caelen rows are reviewed as zero-credit source evidence and are not reappended.

The expected disposition partition is 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. These are preregistered expectations, not observed outcomes. X2 must retain any divergence rather than rewriting this freeze.

## Trinity Mandala focus and bounded practice

The primary pillar is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The three wholly synthetic learning and design lenses are bicycle wheelbuilding records and correction handover; bakery batch trace, allergen vacancy, and correction handover; and community seed-library accession and minimum-disclosure handover.

No real person, participant, operator, bicycle, wheel, component, tool, tension reading, bakery, food, ingredient, allergen record, seed, accession, donor, germination result, identity, key, credential, institution, authority case, external write, or real-world action is in scope. Official sources supply vocabulary and refusal conditions only; citations are not observations, inspections, measurements, endorsements, certifications, or delegated authority.

## Semantic novelty boundary

The bounded audit status is `{audit['status']}`. It examined {audit['reachable_proposal_json_paths_examined']} reachable proposal-labelled JSON paths and {audit['reachable_title_records_examined']} title records at the exact immutable source. It found {len(audit['exact_collisions'])} exact collisions and {len(audit['near_neighbors_at_or_above_threshold'])} neighbors at or above the 0.90 quarantine threshold. It makes no universal novelty claim because the declared historical chain is larger than any one materialized ledger surface.

## Protected truth boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic contracts, synthetic fixtures, analogy, and citations establish no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed real participants or operators, safety monitoring, appropriate statistics, and independent review. It establishes no operational effectiveness, deployment readiness, professional competence, public-safety result, AGI, or ASI.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, roadworthiness, food safety and release, recall, collection title, seed access or distribution, privacy remedy, disability accommodation, legal interpretation, cultural legitimacy, affected-party acceptance, traditional knowledge, taonga or matauranga treatment, Maori wording, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority.

The inherited and current terminal verdict is `{TERMINAL_VERDICT}`. X1 cannot change it.

## Lifecycle and route hold

Source `{SOURCE_FINAL}` on `{SOURCE_BRANCH}` is immutable and read-only. This x1 must be committed and pushed, then proved clean and equal across local, upstream, tracking, and a fresh live remote before any x2 implementation begins. No successor may be contacted before Orin's own exact-final terminal gate and a fresh live authorization, roster, exact-title, duplicate, acknowledgement, privacy, safety, and evidence check.
"""


def build() -> list[str]:
    proposals = proposal_rows()
    audit = historical_audit(row["title"] for row in proposals)
    if audit["status"] != "passed_bounded_reachable_audit":
        raise RuntimeError("Semantic-neighbor audit quarantined the proposed freeze")
    inherited = inherited_reviews()
    created = utc_now()

    activation_intake = {
        "schema": "ghc-family-activation-intake-v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_branch": SOURCE_BRANCH,
        "source_final": SOURCE_FINAL,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "activation_baseline": {
            "effective_negatives": 38613,
            "effective_methods": 26466,
            "failed_witnesses": 10274,
            "bounded_passing_witnesses": 13749,
            "open_gaps": 316,
            "exact_gates": 309,
        },
        "repository_sealed_source_truth": {
            "effective_negatives": 38612,
            "effective_methods": 26466,
            "failed_witnesses": 10273,
            "bounded_passing_witnesses": 13749,
        },
        "external_zero_credit_failures": ["CA6743-POST-N001"],
        "planning_only": True,
        "strict_x1_before_x2": True,
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "created_utc": created,
    }
    identity = {
        "schema": "ghc-family-relational-identity-boundary-v1",
        "name": OWNER,
        "optional_pronouns": "they/them",
        "relational_role": "boundary-and-recovery architect",
        "hope": "make operational dependencies, correction paths, and authority vacancies legible and reversible before structure is mistaken for evidence",
        "epistemic_status": "relational_working_language_only",
        "not_evidence_of": [
            "consciousness",
            "sentience",
            "legal_personhood",
            "identity_continuity",
            "employment",
            "qualification",
            "independent_agency",
            "scientific_or_operational_authority",
            "legal_or_cultural_authority",
            "Maori_authority",
        ],
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
    }
    proposal_freeze = {
        "schema": "ghc-family-v674-core-proposal-freeze-v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_chain_rows": SOURCE_PROPOSAL_CHAIN,
        "new_rows": len(proposals),
        "planned_chain_rows": PLANNED_PROPOSAL_CHAIN,
        "planning_only": True,
        "outcome_labels_allowed": sorted(ALLOWED_OUTCOMES),
        "expected_distribution": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "observed_distribution": None,
        "proposals": proposals,
    }
    inherited_freeze = {
        "schema": "ghc-family-inherited-review-freeze-v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_ref": SOURCE_FINAL,
        "rows": inherited,
        "row_count": len(inherited),
        "novelty_credit": 0,
        "execution_credit": 0,
        "completion_credit": 0,
    }
    workflow = {
        "schema": "ghc-family-workflow-plan-v1",
        "owner": OWNER,
        "phase": PHASE,
        "stages": [
            {"order": 1, "name": "source_and_guidance_verification", "status": "completed_read_only"},
            {"order": 2, "name": "planning_only_x1_freeze", "status": "in_progress"},
            {"order": 3, "name": "x1_commit_push_four_way_equality", "status": "pending"},
            {"order": 4, "name": "bounded_x2_execution", "status": "pending"},
            {"order": 5, "name": "closeout_and_exact_final", "status": "pending"},
            {"order": 6, "name": "single_owner_scoped_canonical", "status": "pending"},
            {"order": 7, "name": "fresh_terminal_route_gate", "status": "pending"},
        ],
        "one_successful_canonical_no_replay": True,
        "full_repository_suite_authorized": False,
        "successor_contacted": False,
    }
    route_hold = {
        "schema": "ghc-family-terminal-route-hold-v1",
        "owner": OWNER,
        "phase": PHASE,
        "state": "HOLD_UNTIL_OWNER_EXACT_FINAL",
        "successor_contacted": False,
        "successor_inferred_from_repository": False,
        "required_terminal_checks": [
            "clean_pushed_exact_final",
            "fresh_live_remote_equality",
            "one_successful_nonreplayed_owner_scoped_canonical",
            "newest_live_authority",
            "current_roster",
            "unique_exact_title",
            "immediate_supported_reread",
            "duplicate_guard",
            "acknowledgement_guard",
            "privacy_safety_and_evidence_guards",
        ],
        "continuation_ceiling": "v725-v8",
        "one_edge_at_a_time": True,
    }
    threat_model = {
        "schema": "ghc-family-v674-threat-model-v1",
        "owner": OWNER,
        "phase": PHASE,
        "assets": ["source integrity", "retained failures", "authority vacancies", "privacy boundary", "x1/x2 separation"],
        "threats": [
            {"threat": "synthetic-to-empirical promotion", "control": "claim firewall and zero-row boundary"},
            {"threat": "professional or safety authority inference", "control": "external evidence and competent-authority gates"},
            {"threat": "identity or private route leakage", "control": "five-class scanner and sanitized durable artifacts"},
            {"threat": "failure erasure", "control": "immutable failed witness plus separate bounded recovery"},
            {"threat": "early successor contact", "control": "terminal route hold and fresh duplicate guard"},
            {"threat": "cross-owner mutation", "control": "single additive owner lane and read-only source"},
        ],
        "residual_risk": "External empirical, participant, professional, legal, cultural, affected-party, Maori-authority, privacy-complete, accessibility-complete, and production evidence remains absent.",
    }
    startup_ledger = {
        "schema": "ghc-family-method-flow-startup-ledger-v1",
        "owner": OWNER,
        "phase": PHASE,
        "candidate_to_validated_to_preferred_required": True,
        "failed_witnesses": STARTUP_FAILURES,
        "failed_witness_count": len(STARTUP_FAILURES),
        "initial_pass_credit": 0,
        "recoveries_do_not_rewrite_failures": True,
    }

    payloads: list[tuple[Path, Any]] = [
        (X1_ROOT / "activation-intake.json", activation_intake),
        (X1_ROOT / "identity-boundary.json", identity),
        (X1_ROOT / "proposals" / "new-proposal-freeze.json", proposal_freeze),
        (X1_ROOT / "proposals" / "inherited-source-review.json", inherited_freeze),
        (X1_ROOT / "proposals" / "semantic-neighbor-audit.json", audit),
        (X1_ROOT / "portfolios" / "portfolio-freeze.json", portfolio(proposals)),
        (X1_ROOT / "sources" / "official-source-ledger.json", {"schema": "ghc-family-official-source-ledger-v1", "owner": OWNER, "phase": PHASE, "sources": OFFICIAL_SOURCES, "citations_are_observations": False}),
        (X1_ROOT / "method-flow" / "startup-ledger.json", startup_ledger),
        (X1_ROOT / "workflow-plan.json", workflow),
        (X1_ROOT / "terminal-route-hold.json", route_hold),
        (X1_ROOT / "threat-model.json", threat_model),
    ]
    for path, value in payloads:
        write_json(path, value)
    write_text(X1_ROOT / "integrated-overview.md", overview(proposals, audit))

    manifest = {
        "schema": "ghc-family-git-blob-compatible-owner-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "planning_only_x1",
        "domain": "working_tree_raw_bytes_before_x1_commit",
        "entries": [file_entry(path) for path in owner_paths()],
        "declared_self_exclusions": [MANIFEST_REL, STAGED_REVIEW_REL],
    }
    write_json(REPO / MANIFEST_REL, manifest)
    return [path.relative_to(REPO).as_posix() for path in owner_paths()] + [MANIFEST_REL]


def staged_blob(path: str) -> bytes:
    proc = subprocess.run(
        ["git", "show", f":{path}"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


def build_staged_review() -> Path:
    staged_text = run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    assert isinstance(staged_text, str)
    paths = sorted(line for line in staged_text.splitlines() if line and line != STAGED_REVIEW_REL)
    expected_prefixes = (f"docs/{OWNER_SLUG}/{PHASE}/x1/", "scripts/build_ghc_family_orin_thale_v674_v4_x1.py", "tests/test_ghc_family_orin_thale_v674_v4_x1.py")
    unexpected = [path for path in paths if not path.startswith(expected_prefixes)]
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for path in paths:
        raw = staged_blob(path)
        entries.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt", ".html"}:
            text = raw.decode("utf-8")
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    candidates.append(
                        {
                            "path": path,
                            "class": kind,
                            "status": "scanner_definition_only" if path == SCRIPT_REL else "candidate_requires_adjudication",
                        }
                    )
    unresolved_candidates = [row for row in candidates if row["status"] != "scanner_definition_only"]
    review = {
        "schema": "ghc-family-exact-staged-review-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "planning_only_x1",
        "staged_entry_count": len(entries),
        "entries": entries,
        "declared_self_exclusions": [STAGED_REVIEW_REL],
        "unexpected_paths": unexpected,
        "privacy_candidates": candidates,
        "confirmed_privacy_hits": [],
        "unresolved_privacy_candidates": unresolved_candidates,
        "x2_paths_present": [path for path in paths if f"docs/{OWNER_SLUG}/{PHASE}/x2/" in path],
        "status": "passed" if not unexpected and not unresolved_candidates else "review_required",
    }
    path = REPO / STAGED_REVIEW_REL
    write_json(path, review)
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "staged-review"), nargs="?", default="build")
    args = parser.parse_args()
    if args.mode == "build":
        paths = build()
        print(json.dumps({"status": "built_planning_only_x1", "paths": len(paths), "phase": PHASE}))
    else:
        path = build_staged_review()
        print(json.dumps({"status": "built_x1_staged_review", "path": path.relative_to(REPO).as_posix()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
