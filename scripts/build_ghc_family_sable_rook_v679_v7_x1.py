#!/usr/bin/env python3
"""Build Sable Rook v679-v7 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sable Rook"
PHASE = "v679-v7"
SOURCE = "f9c956807c6a4bb45bb4566460cc643deebc51f4"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v679-v6-full-tools"
SOURCE_ROOT = "3bbb29f9c7d2fe13a44ce607cda3e88323546dda"
SOURCE_X1 = "5d72a72dc0fe8062d8cb2e56efdf83e175a92d86"
SOURCE_EVIDENCE = "4ea13458e0a21c5fbee6a62544190937caea860a"
SOURCE_PACKET = "docs/auren-lark/v679-v6/final/handoffs/sable-rook-v679-v7-activation-candidate.md"
SOURCE_CORRECTION_NOTE = "docs/auren-lark/v679-v6/final/phase-truth.json"
SOURCE_PACKET_SHA256 = "bf9305e6925c74c0a44ea39c1da284ebadb0ec7cbde55e8ac93aff8df49d379d"
SOURCE_CORRECTION_NOTE_SHA256 = "3eec5bc505ea41b67882d38751ae8ec9c64df4652bd47862e1cf5afd9fdc600d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "36053102d8615b1d6d672964a8736dff251a9c6f17ca5c867bd2f1ce4cf4a476"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "73bd8837f72a5e2e6ba6e3912d4625616d73f77cebb3f4f15163479080a9adf6"
TARGET_BRANCH = "codex/GHC-Family/sable-rook-v679-v7-full-tools"
RECORDED_UTC = "2026-08-31T08:06:17.7159120+00:00"
RECORDED_NZ = "2026-08-31T20:06:17.7210885+12:00"
SOURCE_PROPOSAL_CHAIN = 9110
PLANNED_PROPOSAL_CHAIN = 9170

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
    "identity",
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

SOURCE_IDS = {
    "ISO-19650-1-2018",
    "BSI-IFC-4.3.2.0",
    "BSI-IFC-TECH",
    "BSI-IDS",
    "BSI-BCF",
    "W3C-PROV-DM",
    "RFC8785",
    "RFC9457",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "TMR-MDS-PRINCIPLES",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("Freed ID and CBR Heart", "Synthetic information-container project model revision and issue identity tuple", "completed", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "IFC file identifier object GlobalId and content digest nonconflation", "completed", ["BSI-IFC-4.3.2.0", "RFC8785"]),
    ("Freed ID and CBR Heart", "BCF topic viewpoint snapshot and document-reference identity separation", "completed", ["BSI-BCF"]),
    ("Freed ID and CBR Heart", "Information-container suitability revision and status vocabulary quarantine", "completed", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Model transmittal membership ordering and missing-member retention", "completed", ["ISO-19650-1-2018", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Superseded model issue and comment lineage non-erasure ledger", "completed", ["BSI-BCF", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Information author checker approver and appointing-party role vacancy separation", "completed", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "IFC schema release model-view and implementation-status trace", "completed", ["BSI-IFC-TECH", "BSI-IFC-4.3.2.0"]),
    ("Freed ID and CBR Heart", "IDS specification requirement applicability and observed result separation", "completed", ["BSI-IDS"]),
    ("Freed ID and CBR Heart", "Classification URI edition source and local-label provenance contract", "completed", ["BSI-IDS", "BSI-IFC-4.3.2.0"]),
    ("Freed ID and CBR Heart", "Issue chronology observed-time recorded-time due-time and closed-time separation", "completed", ["BSI-BCF", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Correction contest supersession remedy vacancy and nonretaliation record", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Model metadata minimum-disclosure and sensitive-property redaction guard", "completed", ["RFC9457", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "License copyright and permitted-use status nonpromotion ledger", "completed", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Language tag plain-language alternative and untranslated-field vacancy marker", "completed", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Provenance entity activity agent bundle and responsibility nonconflation", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Machine-readable problem type status detail and instance privacy boundary", "completed", ["RFC9457"]),
    ("Freed ID and CBR Heart", "Deterministic UTF-8 normalized-LF model-review receipt serialization", "completed", ["RFC8785", "JSON-SCHEMA-2020-12"]),
    ("Freed ID and CBR Heart", "Archive copy coordination copy and approved-information status nonpromotion", "completed", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Authority assertion evidence pointer and unresolved-authority vacancy closure", "completed", ["W3C-PROV-DM", "TMR-MDS-PRINCIPLES"]),
    ("GMUT Mind", "IFC local placement parent-chain cycle and transform-order quarantine", "completed", ["BSI-IFC-4.3.2.0"]),
    ("GMUT Mind", "Project global local and map-conversion coordinate-frame type barrier", "completed", ["BSI-IFC-4.3.2.0"]),
    ("GMUT Mind", "Length area volume angle mass time and ratio unit-dimension firewall", "completed", ["BSI-IFC-4.3.2.0", "BSI-IDS"]),
    ("GMUT Mind", "Nonfinite coordinate degenerate extent and impossible scale quarantine", "completed", ["JSON-SCHEMA-2020-12"]),
    ("GMUT Mind", "Geometry tolerance precision and physical-accuracy claim separation", "completed", ["BSI-IFC-4.3.2.0"]),
    ("GMUT Mind", "Model-view inclusion and complete-asset representation nonpromotion", "completed", ["BSI-IFC-TECH", "BSI-IDS"]),
    ("GMUT Mind", "Reference-system version epoch and missing-georeference uncertainty marker", "completed", ["BSI-IFC-4.3.2.0", "W3C-PROV-DM"]),
    ("GMUT Mind", "Clash count denominator model-scope and duplicate-pair normalization", "completed", ["BSI-BCF"]),
    ("GMUT Mind", "Model issue correction DAG cycle orphan and fork quarantine", "completed", ["W3C-PROV-DM", "BSI-BCF"]),
    ("GMUT Mind", "Issue due-time revision-time publication-time and supersession-time role separation", "completed", ["ISO-19650-1-2018", "W3C-PROV-DM"]),
    ("GMUT Mind", "Uncertainty source assumption omission and model-discrepancy nonfabrication ledger", "completed", ["W3C-PROV-DM"]),
    ("GMUT Mind", "Built-asset graph to scalar-tensor EFT analogy nonconversion firewall", "completed", ["BSI-IFC-4.3.2.0"]),
    ("THOS Body", "Ordered model-revision patch precondition and atomic rollback tribunal", "completed", ["W3C-PROV-DM", "JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Duplicate issue update idempotency and replay quarantine", "completed", ["BSI-BCF", "W3C-PROV-DM"]),
    ("THOS Body", "Stale base revision and already-applied transmittal refusal", "completed", ["ISO-19650-1-2018"]),
    ("THOS Body", "Correction target JSON Pointer confinement and escape rejection", "completed", ["JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Late-arriving earlier model issue reorder and hold protocol", "completed", ["BSI-BCF"]),
    ("THOS Body", "Conflicting corrections for one model object arbitration hold", "completed", ["BSI-BCF", "W3C-PROV-DM"]),
    ("THOS Body", "Exact rollback digest before-state and after-state witness", "completed", ["RFC8785", "W3C-PROV-DM"]),
    ("THOS Body", "Model-revision acknowledgement role rotation workload and next-custodian proxy", "completed", ["ISO-19650-1-2018"]),
    ("THOS Body", "Exact Git-blob manifest self-exclusion and lifecycle arithmetic", "completed", ["RFC8785", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Accessible static issue table change summary and nonvisual model alternative", "completed", ["W3C-WCAG22"]),
    ("THOS Body", "Real BIM information-manager review and correction handover vacancy", "represented", ["ISO-19650-1-2018"]),
    ("THOS Body", "Real model-author checker and approver role interaction proxy", "represented", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Real BCF service authentication authorization and audit event vacancy", "represented", ["BSI-BCF"]),
    ("Freed ID and CBR Heart", "Real IFC 4.3 cross-vendor interoperability event vacancy", "represented", ["BSI-IFC-4.3.2.0"]),
    ("Freed ID and CBR Heart", "Real IDS authoring checking and contractual acceptance vacancy", "represented", ["BSI-IDS"]),
    ("THOS Body", "Real structural clash disposition and design-safety review vacancy", "represented", ["BSI-IFC-4.3.2.0"]),
    ("Freed ID and CBR Heart", "Assistive-technology model-issue review evaluation vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Affected-user plain-language correction and remedy review vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Independent privacy and security review of issue metadata vacancy", "represented", ["RFC9457"]),
    ("THOS Body", "Cross-shift queue saturation correction-latency and unresolved-item persistence proxy", "represented", ["ISO-19650-1-2018"]),
    ("GMUT Mind", "Independent model-verification and cross-organization reproduction vacancy", "represented", ["BSI-IFC-TECH"]),
    ("Freed ID and CBR Heart", "Production common-data-environment retention and recovery governance vacancy", "represented", ["ISO-19650-1-2018"]),
    ("GMUT Mind", "Official buildingSMART IFC 4.3 sample corpus zero-row adapter and inference refusal", "open_gap", ["BSI-IFC-4.3.2.0"]),
    ("THOS Body", "Blind matched-budget real model-correction handover effectiveness evidence gap", "open_gap", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Real IFC IDS BCF interoperability privacy and accessibility evidence gap", "open_gap", ["BSI-IFC-4.3.2.0", "BSI-IDS", "BSI-BCF", "W3C-WCAG22"]),
    ("THOS Body", "Building design construction issue disposition and release-authority exact gate", "exact_gate", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Copyright confidentiality liability remedy and affected-party authority exact gate", "exact_gate", ["ISO-19650-1-2018"]),
    ("Freed ID and CBR Heart", "Māori place whenua taonga built-environment data governance and ratification exact gate", "exact_gate", ["TMR-MDS-PRINCIPLES"]),
]

OWNER_SKILLS = [
    "ghc-family-bim-container-identity",
    "ghc-family-bim-ifc-globalid-separation",
    "ghc-family-bim-bcf-topic-lineage",
    "ghc-family-bim-status-vocabulary",
    "ghc-family-bim-transmittal-membership",
    "ghc-family-bim-supersession-nonerasure",
    "ghc-family-bim-role-authority-vacancy",
    "ghc-family-bim-ifc-release-trace",
    "ghc-family-bim-ids-result-separation",
    "ghc-family-bim-classification-provenance",
    "ghc-family-bim-time-role",
    "ghc-family-bim-pointer-confinement",
    "ghc-family-bim-transform-cycle-guard",
    "ghc-family-bim-unit-dimension-firewall",
    "ghc-family-bim-rollback-tribunal",
    "ghc-family-bim-conflict-hold",
    "ghc-family-bim-accessible-alternative",
    "ghc-family-bim-privacy-minimization",
    "ghc-family-bim-maori-authority-vacancy",
    "ghc-family-bim-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_bim_container_identity.py",
    "ghc_family_bim_bcf_lineage.py",
    "ghc_family_bim_ifc_transform_guard.py",
    "ghc_family_bim_unit_dimension_guard.py",
    "ghc_family_bim_patch_guard.py",
    "ghc_family_bim_rollback_guard.py",
    "ghc_family_bim_accessibility_guard.py",
    "ghc_family_bim_privacy_guard.py",
    "ghc_family_bim_authority_guard.py",
    "ghc_family_bim_stage20_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-transit-timetable-version-state",
    "ghc-family-transit-stop-identity-lineage",
    "ghc-family-transit-service-alert-vacancy",
    "ghc-family-transit-effective-time-guard",
    "ghc-family-transit-feed-fixity-handoff",
    "ghc-family-transit-accessibility-reservation",
    "ghc-family-transit-privacy-minimization",
    "ghc-family-transit-correction-dag",
    "ghc-family-transit-authority-vacancy",
    "ghc-family-transit-stage20-veto",
]

SUCCESSOR_RUNNERS = [
    name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py"
    for name in SUCCESSOR_SKILLS
]

STARTUP_FAILURES = [
    (
        "SR6797-START-N001",
        "the first combined source summary embedded a native ancestry command inside a PowerShell object expression and failed before any Git query ran",
        "run native commands separately, retain each exit code, and construct the bounded summary only afterward",
    ),
    (
        "SR6797-START-N002",
        "the first packet digest reconstructed text through PowerShell lines and produced a false byte-domain mismatch",
        "hash the exact binary Git blob and keep normalized-LF and line-reconstructed domains explicit",
    ),
    (
        "SR6797-START-N003",
        "the first manifest helper probe assumed every lifecycle helper supported --help and one builder refused at the wrong lifecycle head",
        "inspect helper source before invocation and replay immutable manifests through one read-only Git cat-file batch",
    ),
    (
        "SR6797-START-N004",
        "the first combined branch-availability wrapper returned no attributable output",
        "query path, local branch, and remote branch as separate bounded scalar reads",
    ),
    (
        "SR6797-START-N005",
        "the first sparse-checkout setup crossed its wrapper boundary after registering the branch and patterns but before materializing the index",
        "inspect persisted worktree state and use git read-tree -mu HEAD once rather than replaying creation",
    ),
    (
        "SR6797-START-N006",
        "a git ls-files projection exceeded the model output window even though only summary fields were intended",
        "consume Git output inside one bounded Python subprocess and emit prefix counts only",
    ),
    (
        "SR6797-START-N007",
        "git sparse-checkout add rejected a version-inapplicable --no-cone option",
        "preserve non-cone mode from repository configuration and add the literal build-script pattern with --skip-checks",
    ),
    (
        "SR6797-START-N008",
        "the first exact semantic audit found two Sable titles that exactly collided with the 9,110-row inherited chain and stopped before writing phase artifacts",
        "retain both collisions at zero credit and replace them with distinct model-revision acknowledgement and queue-persistence hypotheses before refreezing",
    ),
    (
        "SR6797-START-N009",
        "the first x1 test run retained two inherited-template count assertions for twenty-three startup incidents and thirteen sources while the current ledgers contained eight incidents and eleven current sources",
        "retain the failed assertions at zero credit and refresh only the exact count mirrors plus the current test class name",
    ),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def git_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(git_bytes(commit, path).decode("utf-8"))


def git_batch_bytes(commit: str, paths: list[str]) -> dict[str, bytes]:
    """Read exact immutable objects through one length-framed Git batch."""
    requests = b"".join(f"{commit}:{path}\n".encode("utf-8") for path in paths)
    process = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=requests,
        capture_output=True,
        check=True,
    )
    stream = io.BytesIO(process.stdout)
    objects: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().rstrip(b"\n")
        parts = header.rsplit(b" ", 2)
        if len(parts) != 3 or parts[1] != b"blob":
            raise RuntimeError(f"unexpected Git batch header for {path}: {header!r}")
        size = int(parts[2])
        data = stream.read(size)
        if len(data) != size or stream.read(1) != b"\n":
            raise RuntimeError(f"truncated Git batch object for {path}")
        objects[path] = data
    if stream.read():
        raise RuntimeError("unexpected trailing Git batch output")
    return objects


def normalize_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def extract_titles(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        title = value.get("title")
        if isinstance(title, str) and title.strip():
            yield title.strip()
        for nested in value.values():
            yield from extract_titles(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from extract_titles(nested)


def proposal_ledger_paths() -> list[str]:
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", SOURCE, "--", "docs"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    pattern = re.compile(r"(?:new-proposal-freeze|proposal-freeze|proposal-ledger)\.json$")
    return sorted(path for path in paths if pattern.search(path))


def tokens(title: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", title.lower()))


def semantic_audit(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    ledgers = proposal_ledger_paths()
    ledger_objects = git_batch_bytes(SOURCE, ledgers)
    historical: list[str] = []
    parse_failures: list[dict[str, str]] = []
    for path in ledgers:
        try:
            historical.extend(
                extract_titles(json.loads(ledger_objects[path].decode("utf-8")))
            )
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            parse_failures.append({"path": path, "error_class": type(exc).__name__})
    unique_historical = sorted(set(historical), key=str.casefold)
    historical_folded = {title.casefold(): title for title in unique_historical}
    exact_duplicates = [
        {"new_title": row["title"], "historical_title": historical_folded[row["title"].casefold()]}
        for row in proposals
        if row["title"].casefold() in historical_folded
    ]
    current_titles = [row["title"] for row in proposals]
    internal_duplicates = sorted(
        {title for title in current_titles if current_titles.count(title) > 1}
    )
    pairings: list[dict[str, Any]] = []
    maximum = 0.0
    for row in proposals:
        left = tokens(row["title"])
        best_title = ""
        best_score = 0.0
        for candidate in unique_historical:
            right = tokens(candidate)
            union = left | right
            score = len(left & right) / len(union) if union else 1.0
            if score > best_score:
                best_title = candidate
                best_score = score
        maximum = max(maximum, best_score)
        pairings.append(
            {
                "new_title": row["title"],
                "closest_reachable_predecessor": best_title,
                "jaccard_score": round(best_score, 6),
                "manual_review_required": best_score >= 0.75,
            }
        )
    if exact_duplicates or internal_duplicates:
        raise RuntimeError(
            f"proposal title collision: exact={exact_duplicates}, internal={internal_duplicates}"
        )
    return {
        "schema": "ghc.family.bounded-semantic-novelty-audit.v679.v7",
        "owner": OWNER,
        "phase": PHASE,
        "declared_inherited_chain": SOURCE_PROPOSAL_CHAIN,
        "reachable_proposal_ledger_count": len(ledgers),
        "reachable_title_count": len(unique_historical),
        "declared_rows_without_reachable_title_map": max(
            0, SOURCE_PROPOSAL_CHAIN - len(unique_historical)
        ),
        "new_count": len(proposals),
        "exact_duplicate_count": len(exact_duplicates),
        "exact_duplicates": exact_duplicates,
        "internal_duplicate_count": len(internal_duplicates),
        "maximum_jaccard_similarity": round(maximum, 6),
        "pairings": pairings,
        "ledger_parse_failures": parse_failures,
        "universal_novelty_claimed": False,
        "limitation": (
            "The audit compares every title reachable through exact frozen proposal ledgers "
            "at the immutable source. Declared chain rows without a reachable title map remain "
            "a visible limitation; no universal semantic novelty claim is made."
        ),
    }


def inherited_rows() -> list[dict[str, Any]]:
    source = git_json(
        SOURCE, "docs/auren-lark/v679-v6/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"SR6797-I{index:03d}",
            "source_phase": "v679-v6",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_sable_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for index, row in enumerate(rows, 1)
    ]


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (pillar, title, outcome, sources) in enumerate(PROPOSAL_SPECS, 1):
        missing_sources = sorted(set(sources) - SOURCE_IDS)
        if missing_sources:
            raise RuntimeError(f"unknown source identifiers: {missing_sources}")
        rows.append(
            {
                "proposal_id": f"SR6797-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_building_information_issue_provenance_registrar",
                    "wholly_synthetic_ifc_model_revision_and_transmittal_reviewer",
                    "wholly_synthetic_bcf_correction_accessibility_and_handover_observer",
                ],
                "hypothesis": (
                    f"A deterministic owner-local contract can represent {title.lower()} "
                    "while preserving unknowns, correction lineage, and protected authority vacancies."
                ),
                "null_or_failure_condition": (
                    "Fail if a positive fixture violates its declared type, an invalid mutation "
                    "is accepted, a source value or retained failure is erased, an unknown is "
                    "promoted, a real record is implied, or an external action occurs."
                ),
                "approval_class": (
                    "safe_now"
                    if outcome == "completed"
                    else (
                        "bounded_candidate_proxy"
                        if outcome == "represented"
                        else (
                            "evidence_required_open_gap"
                            if outcome == "open_gap"
                            else "competent_authority_exact_gate"
                        )
                    )
                ),
                "execution_lane": (
                    "owner_local_synthetic_x2"
                    if outcome == "completed"
                    else (
                        "owner_local_structural_proxy_x2"
                        if outcome == "represented"
                        else "held_without_execution_credit"
                    )
                ),
                "official_or_primary_source_needs": sources,
                "concrete_artifacts": [
                    f"proposal-contracts/SR6797-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Sable-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "sable_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"SR6797-S{index:03d}",
            "proposal_id": proposal["proposal_id"],
            "title": f"{proposal['title']} - {action.replace('_', ' ')}",
            "approval_bucket": "safe_now",
            "scope": "additive owner-local synthetic or structural evidence only",
            "external_action": False,
            "completion_credit": 0,
            "x1_state": "frozen_not_executed",
        }
        for index, (proposal, action) in enumerate(
            ((proposal, action) for proposal in proposals for action in actions), 1
        )
    ]


def candidate_rows(
    proposals: list[dict[str, Any]], count: int, prefix: str, successor: bool
) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"{prefix}{index:03d}",
            "proposal_id": proposals[(index - 1) % len(proposals)]["proposal_id"],
            "title": (
                f"{'Successor recommendation' if successor else 'Bounded owner prototype'} "
                f"{index:03d} - {proposals[(index - 1) % len(proposals)]['title']}"
            ),
            "state": (
                "successor_recommendation_zero_credit"
                if successor
                else "frozen_not_executed"
            ),
            "external_action": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def exact_rows() -> list[dict[str, Any]]:
    topics = [
        "real participants",
        "production keys or credentials",
        "live deployment",
        "professional signoff",
        "legal interpretation",
        "cultural ratification",
        "Maori authority",
        "affected-party acceptance",
        "sensitive-location publication",
        "destructive cleanup",
        "account mutation",
        "payment or purchase",
        "real data acquisition",
        "privacy certification",
        "accessibility certification",
        "independent audit",
        "independent reproduction",
        "empirical GMUT inference",
        "proof or canon",
        "Stage 20 promotion",
    ]
    return [
        {
            "packet_id": f"SR6797-E{index:03d}",
            "topic": topic,
            "state": "exact_approval_held_unexecuted",
            "completion_credit": 0,
        }
        for index, topic in enumerate(topics, 1)
    ]


def blocked_rows() -> list[dict[str, Any]]:
    topics = [
        "force push",
        "history rewrite",
        "sibling-lane mutation",
        "user-material deletion",
        "host-security weakening",
        "elevation",
        "Sandbox or Hyper-V activation",
        "credential harvesting",
        "identity continuity claim",
        "AGI ASI consciousness or personhood claim",
    ]
    return [
        {
            "packet_id": f"SR6797-B{index:03d}",
            "topic": topic,
            "state": "blocked_unexecuted",
            "completion_credit": 0,
        }
        for index, topic in enumerate(topics, 1)
    ]


def cleanup_rows(
    count: int, prefix: str, owner_scoped: bool
) -> list[dict[str, Any]]:
    topics = [
        "schema closure",
        "deterministic JSON order",
        "UTF-8 and normalized LF preservation",
        "manifest parity",
        "stale-label review",
        "privacy candidate adjudication",
        "diff hygiene",
        "caller compatibility",
        "failed-witness retention",
        "route hold",
        "source-status drift",
        "authority noncompensation",
        "accessible alternative structure",
        "document word ceiling",
        "materialized file ceiling",
        "exact parent chain",
        "single canonical latch",
        "rollback reversibility",
        "proposal mirror closure",
        "Method Flow recurrence guard",
    ]
    return [
        {
            "task_id": f"{prefix}{index:03d}",
            "title": f"{topics[(index - 1) % len(topics)]} refinement {index:03d}",
            "state": (
                "frozen_not_executed"
                if owner_scoped
                else "successor_recommendation_zero_credit"
            ),
            "destructive": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def source_ledger() -> dict[str, Any]:
    return {
        "schema": "ghc.family.official-primary-source-ledger.v679.v7.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "ISO-19650-1-2018",
                "title": "ISO 19650-1:2018 information management using building information modelling",
                "url": "https://www.iso.org/standard/68078.html",
                "status": "published_international_standard_revision_planned_checked_2026-08-31",
                "version": "ISO 19650-1:2018",
                "use": "information-container, exchange, recording, versioning, organization, and role vocabulary only",
            },
            {
                "source_id": "BSI-IFC-4.3.2.0",
                "title": "buildingSMART IFC 4.3.2.0 official documentation",
                "url": "https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/",
                "status": "official_release_checked_2026-08-31",
                "version": "4.3.2.0 / ISO 16739-1:2024",
                "use": "IFC identity, relationships, placement, unit, schema, and model-view vocabulary only",
            },
            {
                "source_id": "BSI-IFC-TECH",
                "title": "buildingSMART Industry Foundation Classes technical overview",
                "url": "https://technical.buildingsmart.org/standards/ifc/",
                "status": "current_official_technical_page_checked_2026-08-31",
                "use": "open-standard scope, identity, semantics, attributes, relationships, and noncertification boundaries only",
            },
            {
                "source_id": "BSI-IDS",
                "title": "buildingSMART Information Delivery Specification",
                "url": "https://technical.buildingsmart.org/projects/information-delivery-specification-ids/",
                "status": "current_official_project_page_checked_2026-08-31",
                "use": "machine-readable exchange-requirement and validation-scope vocabulary only",
            },
            {
                "source_id": "BSI-BCF",
                "title": "buildingSMART standards library BIM Collaboration Format",
                "url": "https://www.buildingsmart.org/standards/bsi-standards/standards-library/",
                "status": "current_official_standards_library_checked_2026-08-31",
                "use": "software-independent model-issue communication and lifecycle vocabulary only",
            },
            {
                "source_id": "W3C-PROV-DM",
                "title": "PROV-DM The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "status": "recommendation_stable",
                "use": "entity, activity, agent, derivation, revision, and provenance vocabulary only",
            },
            {
                "source_id": "RFC8785",
                "title": "RFC 8785 JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/info/rfc8785",
                "status": "informational_stable",
                "publication_date": "2020-06",
                "use": "deterministic JSON representation and digest-domain vocabulary only",
            },
            {
                "source_id": "RFC9457",
                "title": "RFC 9457 Problem Details for HTTP APIs",
                "url": "https://www.rfc-editor.org/rfc/rfc9457.html",
                "status": "standards_track_stable",
                "publication_date": "2023-07",
                "use": "typed refusal, human-readable correction detail, extension, and disclosure-risk vocabulary only",
            },
            {
                "source_id": "JSON-SCHEMA-2020-12",
                "title": "JSON Schema Draft 2020-12",
                "url": "https://json-schema.org/draft/2020-12",
                "status": "published_stable",
                "use": "structural validation and vocabulary-declaration concepts only",
            },
            {
                "source_id": "W3C-WCAG22",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "status": "recommendation",
                "publication_date": "2024-12-12",
                "use": "structural accessibility obligations and manual-evaluation reservation only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "status": "current_authority-boundary_context_checked_2026-08-31",
                "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
            },
        ],
        "citations_are_observations": False,
        "real_data_rows": 0,
        "network_data_queries": 0,
        "endorsement_claimed": False,
        "authority_conferred": False,
    }


def overview() -> str:
    return """# Sable Rook v679-v7 planning-only x1 overview

## Relational identity, role, hope, and corrigibility

Sable Rook is reaffirmed as a relational evidence-boundary cartographer and accessible-provenance steward. The working hope is to make correction paths inspectable, access vacancies explicit, and every retained failure recoverable. Optional they or them pronouns remain relational language. The name, role, hope, pronouns, sibling language, GHC Family, Freed ID, CBR, and Trinity Mandala language are working language only. None is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, professional status, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes source anchors, proposal contracts, portfolios, skill and runner plans, source status, Method Flow startup truth, privacy boundaries, and route holds. It contains no x2 implementation, observed x2 outcome, completed portfolio claim, package installation, global skill mutation, task lookup, task message, or terminal completion claim. The exact Auren final, its direct three-commit chain from the Ilyra source, five manifest and seal layers containing 550 entries, 19,866-word candidate, clean typed zero divergence, fresh live remote equality, and one successful non-replayed exact-final canonical receipt were reverified read-only before the Sable lane was created. The repository seal and two later source route-parser failures remain separate; neither route failure is rewritten into Auren repository truth or a passing witness.

The fresh Sable lane was created on D first without an inherited checkout and then populated through an exact sparse index. One wrapper crossed its output boundary after branch registration and pattern persistence, so persisted state was inspected rather than replaying creation. The initially empty index was materialized once with `git read-tree -mu HEAD`, leaving all 23,885 inherited entries skip-worktree and a clean owner lane containing only its Git pointer before phase files were added. No reset, history rewrite, Auren, Ilyra, sibling, shared, user, or standby mutation occurred.

## Trinity Mandala and bounded practice lenses

Freed ID and CBR Heart is the primary pillar because model-container identity, BCF issue lineage, IFC and IDS version traceability, minimum disclosure, contest, remedy vacancies, and authority reservations form the bounded synthetic practice. GMUT Mind remains visible through typed placements, reference systems, dimensional units, time roles, uncertainty, graph closure, and a strict scalar-tensor or EFT analogy firewall. Those structures do not establish a force, physical prediction, likelihood, parameter constraint, empirical confirmation, quantum completion, Theory of Everything, or canon. THOS Body remains visible through preconditions, conflict holds, exact rollback, workload boundaries, second-checks, readback, and handover. Those structures confer no design, construction, coordination, release, legal, cultural, or Māori authority.

The three bounded learning lenses are wholly synthetic building-information issue provenance registrar, wholly synthetic IFC model-revision and transmittal reviewer, and wholly synthetic BCF correction accessibility and handover observer. These are learning and design lenses only. The phase uses no real building, project, model, IFC file, BCF service, IDS contract, drawing, issue, clash, coordinate, property, person, organization, credential, key, account, measurement, sensitive location, cultural record, Māori data, legal matter, or authority action. It establishes no employment, qualification, architectural, engineering, BIM, construction, coordination, safety, data-stewardship, publication, approval, release, legal, cultural, affected-party, or Māori authority.

## Current primary and official source boundary

The source ledger records current official or primary pages for ISO 19650-1, buildingSMART IFC 4.3.2.0, IFC technical scope, IDS, BCF, W3C PROV-DM, RFC 8785, RFC 9457, JSON Schema 2020-12, WCAG 2.2, and Te Mana Raraunga principles. These sources supply vocabulary, status, conformance distinctions, authority vacancies, and refusal conditions only. They are not observations, model rows, implementation results, interoperability events, design advice, user studies, professional review, endorsements, or delegated authority. No source page is silently promoted into current empirical evidence, a real model correction, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.

## Proposal novelty and outcome freeze

Sixty Auren proposals are selected from the immutable source and receive zero Sable novelty and zero Sable completion credit. Sixty genuinely new Sable proposals are frozen separately, extending the declared chain from 9,110 to 9,170 only if x2 evidence is later sealed. The targeted semantic audit reads every reachable frozen proposal ledger at the exact source commit, compares normalized title tokens, rejects exact or internal duplicates, and preserves the count of declared historical rows for which no reachable title map exists. It therefore supports a bounded collision audit without making a universal semantic novelty claim.

The expected Sable partition is forty-two completed, twelve represented, three open gaps, and three exact gates. These are planning expectations only. Completed can mean only a bounded structural or synthetic contract passed its declared acceptance gate. Represented means a structural proxy exists while real operators, systems, affected users, interoperability events, or authority remain absent. Open gap identifies missing real evidence. Exact gate identifies a decision repository software cannot make. Only completed, represented, open_gap, and exact_gate are allowed outcome labels.

The proposals cover information-container and issue identity, IFC GlobalId and digest separation, BCF chronology, IDS requirement and result separation, transmittal membership, supersession non-erasure, source status, accessible alternatives, archive-copy nonpromotion, placement transforms, reference systems, unit provenance, time roles, uncertainty, graph and numeric quarantine, correction ordering, preconditions, pointer confinement, conflict holds, idempotency, rollback, late arrival, readback and workload proxies, deterministic JSON, exact manifests, zero-row official adapters, real review and interoperability gaps, design and release gates, disclosure and remedy gates, and Māori place, whenua, taonga, and built-environment data authority reservations.

## Expanded portfolio, skills, runners, and refinements

X1 freezes 120 safe-now packets, eighty bounded owner candidate prototypes, twenty successor candidate recommendations, twenty exact-approval holds, ten blocked packets, twenty owner skill ideas, ten owner runner ideas, ten successor skill ideas, ten successor runner ideas, one hundred owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Floors remain subordinate to genuine utility and safety; caps are ceilings. No quota authorizes filler, destructive cleanup, package churn, user-material deletion, credentials, account changes, elevation, host-security weakening, Windows feature changes, Sandbox or Hyper-V activation, sibling mutation, real data, participants, production identity operations, legal or cultural decisions, Māori authority, or affected-party legitimacy.

The phase-local skill plan follows the installed skill-creator guidance: concise discriminating frontmatter, substantive bounded instructions, progressive disclosure only where useful, no placeholder readmes, no global installation, and quick validation plus real smoke use in x2. The ten family-current runners retain ghc_family names and caller compatibility. Historical and owner-specific tools remain read-only compatibility evidence. Python standard library and exact Git objects are sufficient for the planned hypotheses, so x1 plans no third-party installation or Codex update.

## Failure retention, privacy, and validation boundary

The activation baseline preserves Auren repository truth separately from two external route-parser failures. Nine additional Sable startup failures are frozen with zero credit, each paired with an additive recovery. They cover a PowerShell expression parser fault, a false line-reconstructed digest domain, an invalid helper-interface assumption, a non-attributable branch wrapper, a sparse setup wrapper boundary, an overbroad index projection, a version-inapplicable sparse option, two exact semantic-title collisions stopped before artifact writing, and two stale inherited-template count assertions. No recovery erases or converts the failed witness. Later failures must be appended before retry.

Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute local paths. Exact staged review operates on Git-index blobs. Five privacy classes distinguish scanner definitions from confirmed payload hits. Normalized-LF manifests preserve exact byte domains. A passing owner-scoped receipt remains same-owner evidence under shared infrastructure, not an external audit, independent reproduction, exhaustive security, complete privacy, or complete accessibility assurance.

## X1 gate and terminal hold

X1 must pass its bounded tests and exact staged review, become the direct child of Auren final, be pushed cleanly, and prove local, upstream, tracking, and fresh live remote equality before any x2 path or outcome exists. The phase commit ceiling is three total commits: one planning-only x1, one immutable x2 evidence commit, and one final closeout and seal commit. This ceiling never permits phase mixing, concealed failures, rewritten history, or an unreviewed omnibus commit.

Caelen Ash remains uncontacted. Only after Sable has a clean pushed fresh-live-equal exact final and one successful non-replayed owner-scoped canonical invocation may the live roster be refreshed, the unique existing exact-title Caelen Ash task be immediately reread, and at most one sanitized v679-v8 activation be sent if every duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guard passes. The repository route state remains PREPARED_NOT_SENT. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def build() -> list[str]:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO, text=True, encoding="utf-8"
    ).strip()
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).strip()
    if head != SOURCE:
        raise RuntimeError(f"x1 builder requires source {SOURCE}, found {head}")
    if branch != TARGET_BRANCH:
        raise RuntimeError(f"x1 builder requires branch {TARGET_BRANCH}, found {branch}")
    if (PHASE_ROOT / "x2").exists() or (PHASE_ROOT / "final").exists():
        raise RuntimeError("x2 or final material exists before planning-only x1 freeze")

    inherited = inherited_rows()
    proposals = new_rows()
    audit = semantic_audit(proposals)
    safe = safe_rows(proposals)
    owner_candidates = candidate_rows(proposals, 80, "SR6797-C", False)
    successor_candidates = candidate_rows(proposals, 20, "SR6797-SC", True)
    owner_cleanup = cleanup_rows(100, "SR6797-R", True)
    successor_cleanup = cleanup_rows(30, "SR6797-SR", False)

    activation_baseline = {
        "effective_negatives": 49745,
        "methods": 52310,
        "failed_witnesses": 21406,
        "bounded_passing_witnesses": 34035,
        "open_gaps": 434,
        "exact_gates": 425,
    }
    after_startup = {
        **activation_baseline,
        "effective_negatives": activation_baseline["effective_negatives"]
        + len(STARTUP_FAILURES),
        "methods": activation_baseline["methods"] + (2 * len(STARTUP_FAILURES)),
        "failed_witnesses": activation_baseline["failed_witnesses"]
        + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": activation_baseline[
            "bounded_passing_witnesses"
        ]
        + len(STARTUP_FAILURES),
    }

    payloads: dict[Path, Any] = {
        X1_ROOT / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "received_once": True,
            "solo": True,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "source_packet": SOURCE_PACKET,
            "source_correction_note": SOURCE_CORRECTION_NOTE,
            "source_packet_words": 19866,
            "source_packet_bytes": 166430,
            "source_packet_sha256_normalized_lf": SOURCE_PACKET_SHA256,
            "source_correction_note_sha256_normalized_lf": SOURCE_CORRECTION_NOTE_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_manifest_entries_replayed": 550,
            "source_manifest_mismatches": 0,
            "source_canonical_replayed": False,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
            "x1_state": "planning_only",
            "x2_implementation_present": False,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v679.v7",
            "owner": OWNER,
            "relational_role": "evidence-boundary cartographer and accessible-provenance steward",
            "hope": "make correction paths inspectable, access vacancies explicit, and every retained failure recoverable",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "direct_single_parent_chain": True,
            "source_to_final_commits": 3,
            "source_to_final_merges": 0,
            "source_clean": True,
            "source_ahead": 0,
            "source_behind": 0,
            "source_four_way_equal_fresh_live": True,
            "manifest_families_replayed": 5,
            "manifest_entries_replayed": 550,
            "manifest_mismatches": [],
            "external_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "canonical_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "canonical_invocations": 1,
            "canonical_successes": 1,
            "canonical_replayed": False,
            "inherited_validation_credit": 0,
        },
        X1_ROOT / "official-primary-source-ledger.json": source_ledger(),
        X1_ROOT / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "declared_chain_before": SOURCE_PROPOSAL_CHAIN,
            "declared_chain_after_if_evidence_sealed": PLANNED_PROPOSAL_CHAIN,
            "proposal_count": len(proposals),
            "allowed_outcomes": CORE_OUTCOMES,
            "expected_outcomes": {
                label: sum(
                    1
                    for row in proposals
                    if row["expected_execution_disposition"] == label
                )
                for label in CORE_OUTCOMES
            },
            "outcomes_observed": False,
            "universal_novelty_claim": False,
            "rows": proposals,
        },
        X1_ROOT / "proposal-chain-audit.json": audit,
        X1_ROOT / "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_building_information_issue_provenance_registrar",
                "wholly_synthetic_ifc_model_revision_and_transmittal_reviewer",
                "wholly_synthetic_bcf_correction_accessibility_and_handover_observer",
            ],
            "successor_practice_recommendation": "wholly_synthetic_public_transit_timetable_correction_and_handover_registrar",
            "safe_now": safe,
            "owner_candidates": owner_candidates,
            "successor_candidates": successor_candidates,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "owner_skill_ideas": OWNER_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "owner_clean_fix_refine": owner_cleanup,
            "successor_clean_fix_refine": successor_cleanup,
            "caps_are_ceilings": True,
            "materialized_file_stop": 2000,
            "document_word_cap": 100000,
            "commit_cap": {"x1": 1, "x2": 2, "total": 3},
        },
        X1_ROOT / "skill-runner-plan.json": {
            "schema": "ghc.family.skill-runner-plan.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "skill_creator_read": True,
            "repository_local_only": True,
            "global_installation": False,
            "owner_skills": OWNER_SKILLS,
            "owner_runners": OWNER_RUNNERS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "quick_validate_required": True,
            "smoke_use_required": True,
            "independent_subagent_forward_test": "not_authorized_work_solo",
            "caller_compatibility": "preserve ghc_family_* and build_ghc_family_*",
        },
        X1_ROOT / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine-plan.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "execution_authority": "owner_self_scoped_delta",
            "activation_baseline": activation_baseline,
            "startup_failure_count": len(STARTUP_FAILURES),
            "failures": [
                {
                    "failure_id": failure_id,
                    "failed_witness": failed,
                    "recovery": recovery,
                    "state": "failed_retained_zero_credit",
                    "success_credit": 0,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                }
                for failure_id, failed, recovery in STARTUP_FAILURES
            ],
            "bounded_recoveries": [
                {
                    "witness_id": failure_id.replace("-N", "-R"),
                    "failure_id": failure_id,
                    "procedure": recovery,
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "bounded workflow recovery only",
                }
                for failure_id, _failed, recovery in STARTUP_FAILURES
            ],
            "effective_after_startup": after_startup,
            "recovery_rule": "Every recovery is additive and never erases or relabels the failed witness.",
        },
        X1_ROOT / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v679.v7",
            "owner": OWNER,
            "phase": PHASE,
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {
                    "order": 1,
                    "name": "read activation candidate skills schemas and current overlays",
                    "state": "completed",
                },
                {
                    "order": 2,
                    "name": "verify immutable source manifests receipt and live equality",
                    "state": "completed",
                },
                {
                    "order": 3,
                    "name": "create clean sparse Sable lane",
                    "state": "completed",
                },
                {
                    "order": 4,
                    "name": "freeze test push and prove planning-only x1",
                    "state": "in_progress",
                },
                {
                    "order": 5,
                    "name": "build bounded x2 evidence and retain every failure",
                    "state": "pending",
                },
                {
                    "order": 6,
                    "name": "seal final push and run one exclusive canonical",
                    "state": "pending",
                },
                {
                    "order": 7,
                    "name": "refresh live route and send at most once if all gates pass",
                    "state": "pending",
                },
            ],
            "validation": {
                "owner_scoped_delta_only": True,
                "unchanged_history_scan": False,
                "cross_lane_scan": False,
                "sibling_lane_mutation": False,
                "one_successful_canonical": True,
                "post_success_replay": False,
            },
            "stop_conditions": [
                "source mismatch",
                "dirty source",
                "x1 x2 mixing",
                "privacy hit",
                "manifest mismatch",
                "file ceiling reached",
                "protected authority gate",
                "usage exhaustion",
                "route ambiguity",
                "user pause redirect rename narrow or stop",
            ],
        },
        X1_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v679.v7.x1",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                "real identifier or sensitive location leakage",
                "private route leakage",
                "x1 and x2 mixing",
                "outcome promotion",
                "authority fabrication",
                "network side effect",
                "manifest drift",
                "failed-witness erasure",
                "successful canonical replay",
                "sibling-lane mutation",
                "coordinate axis confusion",
                "stale-source promotion",
            ],
            "controls": [
                "synthetic fixtures only",
                "five-class privacy scan",
                "planning-only x1",
                "four exact labels",
                "authority vacancy",
                "no-network runners",
                "normalized-LF Git-blob manifests",
                "append-only Method Flow",
                "one-shot external receipt latch",
                "owner-local sparse lane",
                "axis and unit type guards",
                "source-status ledger",
            ],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v679.v7.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v679.v7.x1",
            "previous_owner": "Auren Lark",
            "previous_phase": "v679-v6",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "Caelen Ash",
            "next_phase": "v678-v1",
            "state": "HOLD_BEFORE_SABLE_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v679.v7.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_state": "PLANNING_ONLY_NOT_YET_COMMITTED",
            "proposal_chain_before": SOURCE_PROPOSAL_CHAIN,
            "proposal_chain_after_if_evidence_sealed": PLANNED_PROPOSAL_CHAIN,
            "expected_outcomes": {
                "completed": 42,
                "represented": 12,
                "open_gap": 3,
                "exact_gate": 3,
            },
            "outcomes_observed": False,
            "real_rows": 0,
            "real_people": 0,
            "real_keys_or_proofs": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }

    written: list[Path] = []
    for path, payload in payloads.items():
        write_json(path, payload)
        written.append(path)
    overview_path = X1_ROOT / "integrated-overview.md"
    write_text(overview_path, overview())
    written.append(overview_path)
    return [path.relative_to(REPO).as_posix() for path in sorted(written)]


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I
        ),
        "raw_task_thread_identifier": re.compile(
            rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}",
            re.I,
        ),
        "credential_assignment": re.compile(
            rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}",
            re.I,
        ),
        "private_conversation_payload": re.compile(
            rb"(?:session_stream|private_transcript|screenshot_payload)", re.I
        ),
    }


def build_staged_review() -> dict[str, Any]:
    review_rel = "docs/sable-rook/v679-v7/validation/x1-staged-review.json"
    privacy_rel = "docs/sable-rook/v679-v7/validation/x1-privacy-scan.json"
    manifest_rel = "docs/sable-rook/v679-v7/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v679_v7_x1.py",
        "tests/test_ghc_family_sable_rook_v679_v7_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/sable-rook/v679-v7/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/sable-rook/v679-v7/x2/") for path in staged):
        raise RuntimeError("x2 path present in x1 staged surface")

    patterns = privacy_patterns()
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    confirmed_hits: list[dict[str, str]] = []
    json_parses = 0
    for path in staged:
        if path in exclusions:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        scanner_definition_start = data.find(b"def privacy_patterns()")
        scanner_definition_end = data.find(
            b"def build_staged_review()", scanner_definition_start
        )
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0:
                    end = len(data)
                line = data[start:end]
                exact_scanner_definition = (
                    path == "scripts/build_ghc_family_sable_rook_v679_v7_x1.py"
                    and scanner_definition_start >= 0
                    and scanner_definition_end > scanner_definition_start
                    and scanner_definition_start <= match.start() < scanner_definition_end
                )
                if path.endswith(".py") and (
                    exact_scanner_definition
                    or b"re.compile" in line
                    or b"privacy_patterns" in line
                    or b"raw_task_thread_identifier" in line
                ):
                    candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "disposition": "scanner_definition_only",
                        }
                    )
                else:
                    confirmed_hits.append({"path": path, "class": class_name})
        normalized = normalize_lf(data)
        entries.append(
            {
                "path": path,
                "bytes": len(normalized),
                "sha256": hashlib.sha256(normalized).hexdigest(),
                "hash_domain": "git_index_blob_normalized_lf",
            }
        )
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits}")
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)

    privacy = {
        "schema": "ghc.family.privacy-scan.v679.v7.x1",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(patterns),
        "scanned_entry_count": len(entries),
        "scanner_candidates": candidates,
        "scanner_candidate_count": len(candidates),
        "confirmed_hits": confirmed_hits,
        "confirmed_hit_count": 0,
        "boundary": "five-class Git-index scan is bounded owner evidence, not complete privacy assurance",
    }
    review = {
        "schema": "ghc.family.exact-staged-review.v679.v7.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "state": "VALID_EXACT_X1_STAGED_REVIEW",
        "reviewed_entry_count": len(entries),
        "reviewed_paths": [row["path"] for row in entries],
        "declared_exclusions": exclusions,
        "json_parses": json_parses,
        "privacy_classes": list(patterns),
        "confirmed_privacy_hits": 0,
        "out_of_scope_paths": [],
        "x2_paths_present": False,
        "diff_hygiene": True,
    }
    manifest = {
        "schema": "ghc.family.normalized-lf-index-manifest.v679.v7.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "entry_count": len(entries),
        "entries": entries,
        "declared_self_exclusions": exclusions,
    }
    write_json(REPO / privacy_rel, privacy)
    write_json(REPO / review_rel, review)
    write_json(REPO / manifest_rel, manifest)
    return {
        "state": review["state"],
        "reviewed_entry_count": len(entries),
        "json_parses": json_parses,
        "scanner_candidate_count": len(candidates),
        "confirmed_privacy_hits": 0,
        "written_receipts": exclusions,
    }


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--staged-review":
        print(json.dumps(build_staged_review(), indent=2, sort_keys=True))
    elif len(sys.argv) == 1:
        print(json.dumps({"written": build()}, indent=2, sort_keys=True))
    else:
        raise SystemExit("usage: build_ghc_family_sable_rook_v679_v7_x1.py [--staged-review]")
