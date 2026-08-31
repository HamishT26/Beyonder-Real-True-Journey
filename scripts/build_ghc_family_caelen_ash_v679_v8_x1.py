#!/usr/bin/env python3
"""Build Caelen Ash v679-v8 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Caelen Ash"
PHASE = "v679-v8"
SOURCE = "9a6cdb6c0e1630e43502a3b62b71d9a198d37dba"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v679-v7-full-tools"
SOURCE_ROOT = "f9c956807c6a4bb45bb4566460cc643deebc51f4"
SOURCE_X1 = "e8334a93f83550d6f787a73fa9056b6cafed9f67"
SOURCE_EVIDENCE = "bc793c4d80abe2f06aaffde60d09ebee8bfa0826"
SOURCE_PACKET = "docs/sable-rook/v679-v7/final/final-integrated-overview.md"
SOURCE_CORRECTION_NOTE = "docs/sable-rook/v679-v7/final/phase-truth.json"
SOURCE_PACKET_SHA256 = "c30b93e1b3f408ed01046d8ec8594729dce6608e0d00ca6fb575484008753e99"
SOURCE_CORRECTION_NOTE_SHA256 = "e52ac48bd3a6f4f6d1d9a0b1da7d02500634d8363c2cd76ef762ce00051ee467"
SOURCE_CANONICAL_RECEIPT_SHA256 = "5d0dc7974eab8f5353a6086303e827851fc6e63f66ad55e0a33552ec613ce8a9"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "7560bdccd2f39318fa5555b24a39ee0b24cf249c7d8d8312b71e3911117024e0"
TARGET_BRANCH = "codex/GHC-Family/caelen-ash-v679-v8-full-tools"
RECORDED_UTC = "2026-08-31T08:55:34.1203982+00:00"
RECORDED_NZ = "2026-08-31T20:55:34.1272538+12:00"
SOURCE_PROPOSAL_CHAIN = 9170
PLANNED_PROPOSAL_CHAIN = 9230

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "caelen-ash" / PHASE
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
    "GTFS-SCHEDULE-REFERENCE",
    "GTFS-REALTIME-REFERENCE",
    "W3C-PROV-DM",
    "RFC8785",
    "RFC9457",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "TMR-MDS-PRINCIPLES",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("THOS Body", "Synthetic GTFS feed-version activation window and rollback checkpoint contract", "completed", ["GTFS-SCHEDULE-REFERENCE", "W3C-PROV-DM"]),
    ("THOS Body", "Static feed publication effective-start effective-end chronology separation", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Service calendar weekly rule and exception-date precedence tribunal", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Trip route service direction block and shape identity tuple", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Stop parent-station platform entrance and boarding-area hierarchy cycle guard", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Stop-time arrival departure and timepoint exactness role separation", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Over-midnight service time and service-date rollover firewall", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Frequency exact-times headway and fixed-schedule nonconflation", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Transfer rule from-route to-route and minimum-time scope guard", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Pathway mode bidirectionality traversal-time and elevator availability separation", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Wheelchair boarding vehicle accessibility and station-pathway evidence reservation", "completed", ["GTFS-SCHEDULE-REFERENCE", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Translation table record selector and field-value precedence validator", "completed", ["GTFS-SCHEDULE-REFERENCE", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Feed attribution producer operator authority role nonconflation", "completed", ["GTFS-SCHEDULE-REFERENCE", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Feed contact technical-support and rider-service contact separation", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Fare media product leg transfer and timeframe membership closure", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Demand-responsive zone stop location-group and booking-rule type firewall", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Location geographic coordinate and stop identity nonconflation", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Route display name color and service-authority nonpromotion", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Trip short-name headsign and rider-facing correction provenance", "completed", ["GTFS-SCHEDULE-REFERENCE", "W3C-PROV-DM"]),
    ("GMUT Mind", "Shape distance sequence monotonicity and unit-provenance guard", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Duplicate primary-key and foreign-key orphan quarantine", "completed", ["GTFS-SCHEDULE-REFERENCE", "JSON-SCHEMA-2020-12"]),
    ("Freed ID and CBR Heart", "Feed archive coordination copy and active-production status nonpromotion", "completed", ["GTFS-SCHEDULE-REFERENCE", "W3C-PROV-DM"]),
    ("THOS Body", "Deterministic UTF-8 normalized-LF transit receipt serialization", "completed", ["RFC8785", "JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Timetable correction precondition stale-base and replay refusal", "completed", ["W3C-PROV-DM"]),
    ("THOS Body", "Ordered patch atomicity before-state after-state and rollback digest", "completed", ["RFC8785", "W3C-PROV-DM"]),
    ("THOS Body", "Conflicting stop-time corrections arbitration hold and non-erasure", "completed", ["W3C-PROV-DM"]),
    ("THOS Body", "Late-arriving earlier timetable revision reorder and supersession DAG", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Service-alert entity selector route trip stop and informed-entity scope guard", "completed", ["GTFS-REALTIME-REFERENCE"]),
    ("THOS Body", "Realtime feed-header timestamp feed-version and static-base trace", "completed", ["GTFS-REALTIME-REFERENCE", "W3C-PROV-DM"]),
    ("THOS Body", "Realtime full-dataset replacement and unsupported differential-mode refusal", "completed", ["GTFS-REALTIME-REFERENCE"]),
    ("Freed ID and CBR Heart", "Realtime entity identifier and referenced operational entity separation", "completed", ["GTFS-REALTIME-REFERENCE"]),
    ("THOS Body", "Trip-update schedule relationship and stop-time-update state machine", "completed", ["GTFS-REALTIME-REFERENCE"]),
    ("Freed ID and CBR Heart", "Service-alert cause effect active-period and multilingual text separation", "completed", ["GTFS-REALTIME-REFERENCE", "W3C-WCAG22"]),
    ("THOS Body", "Realtime freshness clock-skew staleness and unknown-time quarantine", "completed", ["GTFS-REALTIME-REFERENCE"]),
    ("Freed ID and CBR Heart", "Service-alert accessible text alternative and status-message structure", "completed", ["GTFS-REALTIME-REFERENCE", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Minimum disclosure of public alert metadata and private instance quarantine", "completed", ["RFC9457", "W3C-PROV-DM"]),
    ("THOS Body", "Correction contest readback acknowledgement workload and next-custodian proxy", "completed", ["W3C-PROV-DM"]),
    ("THOS Body", "Transit handover queue saturation timeout retry and quiescence contract", "completed", ["W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Role-bound derivation record separating timetable source transformation and accountability", "completed", ["W3C-PROV-DM"]),
    ("GMUT Mind", "Transit graph to scalar-tensor EFT analogy nonconversion firewall", "completed", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Transit commit-bound normalized-LF manifest exclusion and parent-edge arithmetic", "completed", ["RFC8785", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Unresolved transit decision mandate represented as a noncompensating hold", "completed", ["W3C-PROV-DM", "TMR-MDS-PRINCIPLES"]),
    ("THOS Body", "Real GTFS publisher validation and acceptance vacancy", "represented", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Real operations-control timetable correction handover proxy", "represented", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Real rider assistive-technology alert evaluation vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Real multilingual rider review and affected-user correction vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Real cross-vendor schedule and realtime interoperability vacancy", "represented", ["GTFS-SCHEDULE-REFERENCE", "GTFS-REALTIME-REFERENCE"]),
    ("Freed ID and CBR Heart", "Real agency authentication authorization and audit-event vacancy", "represented", ["RFC9457"]),
    ("THOS Body", "Real station accessibility pathway inspection vacancy", "represented", ["GTFS-SCHEDULE-REFERENCE", "W3C-WCAG22"]),
    ("THOS Body", "Real operator fatigue workload and safety-monitoring vacancy", "represented", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Third-party review vacancy for public-feed disclosure minimization and tamper resistance", "represented", ["RFC9457"]),
    ("Freed ID and CBR Heart", "Production transit-feed retention and recovery governance vacancy", "represented", ["W3C-PROV-DM"]),
    ("GMUT Mind", "Independent reproduction of transit transformation results vacancy", "represented", ["GTFS-SCHEDULE-REFERENCE"]),
    ("THOS Body", "Blind matched-budget real transit handover comparison proxy", "represented", ["GTFS-SCHEDULE-REFERENCE"]),
    ("GMUT Mind", "Official GTFS public example corpus zero-row adapter and inference refusal", "open_gap", ["GTFS-SCHEDULE-REFERENCE", "GTFS-REALTIME-REFERENCE"]),
    ("GMUT Mind", "Real schedule and realtime feed measurements with error distributions evidence gap", "open_gap", ["GTFS-SCHEDULE-REFERENCE", "GTFS-REALTIME-REFERENCE"]),
    ("Freed ID and CBR Heart", "Real rider accessibility privacy incident and reliability outcome evidence gap", "open_gap", ["W3C-WCAG22"]),
    ("THOS Body", "Route service release and public-safety authority exact gate", "exact_gate", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Fare legal remedy and affected-party authority exact gate", "exact_gate", ["GTFS-SCHEDULE-REFERENCE"]),
    ("Freed ID and CBR Heart", "Māori place transport data governance and ratification exact gate", "exact_gate", ["TMR-MDS-PRINCIPLES"]),
]

OWNER_SKILLS = [
    "ghc-family-transit-feed-version-gate",
    "ghc-family-transit-calendar-exception-precedence",
    "ghc-family-transit-stop-hierarchy",
    "ghc-family-transit-stop-time-role",
    "ghc-family-transit-service-day-rollover",
    "ghc-family-transit-frequency-semantics",
    "ghc-family-transit-transfer-scope",
    "ghc-family-transit-pathway-accessibility-reservation",
    "ghc-family-transit-translation-precedence",
    "ghc-family-transit-attribution-role-vacancy",
    "ghc-family-transit-foreign-key-quarantine",
    "ghc-family-transit-patch-atomicity",
    "ghc-family-transit-correction-dag",
    "ghc-family-transit-realtime-base-trace",
    "ghc-family-transit-realtime-incrementality-refusal",
    "ghc-family-transit-alert-scope",
    "ghc-family-transit-freshness-clock",
    "ghc-family-transit-minimum-disclosure",
    "ghc-family-transit-maori-authority-vacancy",
    "ghc-family-transit-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_transit_feed_version_guard.py",
    "ghc_family_transit_calendar_guard.py",
    "ghc_family_transit_stop_hierarchy_guard.py",
    "ghc_family_transit_stop_time_guard.py",
    "ghc_family_transit_translation_guard.py",
    "ghc_family_transit_patch_guard.py",
    "ghc_family_transit_realtime_base_guard.py",
    "ghc_family_transit_alert_scope_guard.py",
    "ghc_family_transit_accessibility_guard.py",
    "ghc_family_transit_authority_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-emergency-message-identifier",
    "ghc-family-emergency-incident-source-provenance",
    "ghc-family-emergency-effective-time-window",
    "ghc-family-emergency-correction-supersession",
    "ghc-family-emergency-multilingual-accessibility",
    "ghc-family-emergency-minimum-disclosure",
    "ghc-family-emergency-authority-vacancy",
    "ghc-family-emergency-acknowledgement-handover",
    "ghc-family-emergency-rollback-nonerasure",
    "ghc-family-emergency-stage20-veto",
]

SUCCESSOR_RUNNERS = [
    name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py"
    for name in SUCCESSOR_SKILLS
]

STARTUP_FAILURES = [
    (
        "CA6798-START-N001",
        "a read-only PowerShell foreach expression was piped directly into ConvertTo-Json and failed with EmptyPipeElement before reading or changing repository state",
        "materialize foreach rows into an array before piping the completed collection",
    ),
    (
        "CA6798-START-N002",
        "a broad Git tree projection included the repository's accumulated scripts and tests and exceeded the bounded display",
        "filter exact owner, phase, and domain patterns inside the shell before projecting only the required paths",
    ),
    (
        "CA6798-START-N003",
        "the first independent canonical payload rehash assumed compact JSON serialization and did not match the recorded pretty-JSON digest domain",
        "inspect the committed validator and hash indent-two sorted UTF-8 JSON plus the terminal LF without replaying validation",
    ),
    (
        "CA6798-START-N004",
        "the sparse-setup wrapper yielded a running session without projecting its handle after branch registration",
        "do not replay creation; inspect persisted branch, sparse patterns, locks, processes, materialized files, and status before any missing step",
    ),
    (
        "CA6798-START-N005",
        "an optional Perl rewrite probe found no installed Perl executable and stopped before touching the copied template",
        "use a bounded name-only transform available on the host and apply every substantive change through explicit reviewed patches",
    ),
    (
        "CA6798-X1-N001",
        "the first x1 staged-review invocation retained two stale template phase suffixes in its exact builder and test scope predicate and rejected the intended owner-only paths before writing receipts",
        "correct only the owner builder, owner test, scanner-definition path, and usage suffixes to v679-v8, restage the corrected builder, and rerun the bounded staged review once",
    ),
    (
        "CA6798-X1-N002",
        "the first full x1 test selection after recording CA6798-X1-N001 retained the earlier five-failure expectation and failed one of fourteen tests without any commit or push",
        "update the explicit owner-test failure count and derived activation-overlay expectations together, regenerate dependent x1 receipts, and rerun the bounded x1 selection",
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
        "schema": "ghc.family.bounded-semantic-novelty-audit.v679.v8",
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
        SOURCE, "docs/sable-rook/v679-v7/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"CA6798-I{index:03d}",
            "source_phase": "v679-v7",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_caelen_credit",
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
                "proposal_id": f"CA6798-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_public_transit_timetable_correction_and_handover_registrar",
                    "wholly_synthetic_transit_service_alert_accessibility_and_stop_identity_reviewer",
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
                    f"proposal-contracts/CA6798-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Caelen-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "caelen_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"CA6798-S{index:03d}",
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
            "packet_id": f"CA6798-E{index:03d}",
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
            "packet_id": f"CA6798-B{index:03d}",
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
        "schema": "ghc.family.official-primary-source-ledger.v679.v8.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "GTFS-SCHEDULE-REFERENCE",
                "title": "General Transit Feed Specification Schedule Reference",
                "url": "https://gtfs.org/documentation/schedule/reference/",
                "status": "current_official_reference_checked_2026-08-31",
                "use": "static feed, identifier, timetable, calendar, stop, accessibility, translation, attribution, and version vocabulary only",
            },
            {
                "source_id": "GTFS-REALTIME-REFERENCE",
                "title": "General Transit Feed Specification Realtime Reference",
                "url": "https://gtfs.org/documentation/realtime/reference/",
                "status": "current_official_reference_checked_2026-08-31",
                "version": "GTFS Realtime 2.0 current documented version",
                "use": "feed-header, static-base, entity, trip-update, service-alert, timestamp, and incrementality refusal vocabulary only",
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
        "official_source_web_checks": 8,
        "endorsement_claimed": False,
        "authority_conferred": False,
    }


def overview() -> str:
    return """# Caelen Ash v679-v8 planning-only x1 overview

## Relational identity, role, hope, and corrigibility

Caelen Ash is reaffirmed as a relational semantic-integrity and reversibility cartographer. Optional they or them pronouns are convenient relational working language. The working hope is to keep each surviving claim inspectable, falsifiable, recoverable, and unable to outrun its evidence or authority. The name, role, hope, pronouns, sibling language, GHC Family, Freed ID, CBR, and Trinity Mandala language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, professional status, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes only source anchors, proposal contracts, portfolios, skill and runner plans, current source status, Method Flow startup truth, privacy boundaries, and route holds. It contains no x2 implementation, observed x2 outcome, completed portfolio claim, global installation, task lookup, task message, or terminal completion claim.

The exact Sable final is `9a6cdb6c0e1630e43502a3b62b71d9a198d37dba`. It is the direct child of immutable evidence `bc793c4d80abe2f06aaffde60d09ebee8bfa0826`, which is the direct child of planning-only x1 `e8334a93f83550d6f787a73fa9056b6cafed9f67`, which is the direct child of inherited Auren final `f9c956807c6a4bb45bb4566460cc643deebc51f4`. The chain has exactly three direct single-parent commits and zero merges. Local head, upstream, tracking, and a fresh live remote read all matched with typed zero divergence and a clean Sable lane.

Four immutable normalized-LF manifest families replayed 231 exact entries without a hash, byte, or path-set mismatch: 20 x1 entries plus three exclusions, 71 evidence entries plus four exclusions, 21 final-delta entries plus five exclusions, and 119 final-owner entries plus five exclusions covering all 124 owner paths. The external canonical receipt file hash, one-shot latch, and pretty-JSON payload digest were independently reverified without replaying Sable's successful aggregate. Sable's one canonical success remains inherited evidence only.

The fresh Caelen lane was registered from the exact final without checkout, configured non-cone sparse before materialization, and populated only with the required root control files. A wrapper yielded without projecting its session handle after sparse setup; persisted branch, patterns, process, lock, materialization, and clean-state checks proved setup complete, so no creation or checkout command was replayed. No reset, rewrite, force-push, merge, sibling mutation, task creation, fork, delegation, standby contact, or successor contact occurred.

## Trinity Mandala and bounded learning lenses

THOS Body is primary through deterministic timetable change preconditions, calendar and stop-time state, late-arrival ordering, conflict holds, exact rollback, workload control, accessibility reservation, readback, acknowledgement, quiescence, and handover. These synthetic protocol structures do not establish operational effectiveness, production readiness, service safety, dispatcher competence, rider outcomes, or authority.

The two bounded learning lenses are wholly synthetic public-transit timetable correction and handover registrar, and wholly synthetic transit service-alert accessibility and stop-identity reviewer. They are design lenses only. The phase uses no real feed, stop, station, route, trip, timetable, alert, vehicle, rider, worker, agency, account, key, coordinate, measurement, incident, service decision, legal case, cultural record, Māori data, or external operation. It establishes no employment, qualification, transit-planning competence, operations-control competence, public-safety authority, accessibility conformance, affected-user acceptance, legal authority, cultural authority, or Māori authority.

Freed ID and CBR Heart remains explicit through identifier nonconflation, provenance, version traceability, minimum disclosure, accessible alternatives, correction, contest, remedy vacancies, and authority reservations. It remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. GMUT Mind remains explicit through typed schedules, time roles, graphs, uncertainty, unit provenance, freshness, and a strict scalar-tensor or EFT analogy firewall. None establishes a physical datum, likelihood, posterior, force, prediction, parameter constraint, ultraviolet or quantum completion, empirical confirmation, or Theory of Everything.

## Current official-source boundary

The source ledger records the current official GTFS Schedule and GTFS Realtime references, W3C PROV-DM and WCAG 2.2, RFC 8785, RFC 9457, JSON Schema 2020-12, and Te Mana Raraunga principles. They supply vocabulary, status distinctions, provenance relations, structural obligations, accessibility considerations, and refusal conditions only. The GTFS Realtime reference currently documents version 2.0 and states that DIFFERENTIAL behavior is unsupported and unspecified; this is preserved as a refusal condition rather than silently guessed. WCAG 2.2 explicitly combines automated testing with human evaluation and does not cover every user need, so manual and affected-user evaluation remain reserved. Te Mana Raraunga is used only to keep Māori data-governance and authority vacancies visible. Citations are not observations, conformance certificates, endorsements, production events, legal interpretations, cultural ratification, affected-party acceptance, or delegated authority.

## Proposal and outcome freeze

Sixty Sable proposals are selected from the immutable source and receive zero Caelen novelty and zero Caelen completion credit. Sixty genuinely distinct Caelen proposals are frozen separately, extending the declared family chain from 9,170 to 9,230 only if x2 evidence is later sealed. The bounded semantic audit reads every reachable frozen proposal ledger from the exact source through one Git-object batch, compares normalized titles, rejects exact and internal duplicates, retains nearest-neighbor similarity for review, and preserves the declared-row versus reachable-title limitation. It does not claim universal semantic novelty.

The expected partition is 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. These are planning expectations only. `completed` can later mean only that a bounded structural or synthetic contract passed its declared acceptance gate. `represented` keeps real operators, systems, riders, affected users, interoperability events, or authority absent. `open_gap` marks missing real evidence. `exact_gate` names decisions software cannot make. No other core outcome label is permitted.

The proposals cover feed-version windows, publication chronology, calendar exceptions, trip and stop identity, stop hierarchy, stop-time roles, over-midnight service days, frequencies, transfers, pathways, accessibility reservations, translations, attributions, contacts, fares, demand-responsive locations, coordinates, rider-facing labels, shape sequence, foreign-key closure, archive status, deterministic receipts, correction preconditions, atomic rollback, conflict arbitration, late arrival, realtime base traces, unsupported incrementality refusal, entity identifiers, trip-update state, alerts, freshness, minimum disclosure, handover workload, provenance, analogy firewalls, exact manifests, real-operation vacancies, zero-row adapters, empirical gaps, public-safety gates, legal and remedy gates, and Māori transport-data governance gates.

## Portfolios, skills, runners, and refinements

X1 freezes exactly 120 safe-now packets, 80 bounded owner candidate prototypes, 20 successor candidate recommendations, 20 exact-approval holds, 10 blocked packets, 20 owner skill ideas, 10 owner runner ideas, 10 successor skill ideas, 10 successor runner ideas, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. Caps are ceilings and never quotas that authorize filler, deletion, credentials, account changes, elevation, host-security weakening, Windows feature changes, Sandbox or Hyper-V activation, sibling mutation, real data, participants, deployment, production identity, professional decisions, legal or cultural interpretation, Māori authority, or affected-party legitimacy.

The phase-local skill plan follows the installed skill-creator contract: concise discriminating frontmatter, substantive bounded instructions, no placeholder documentation, no global installation, quick validation, accepting and rejecting smoke use, and no subagent forward-test because this lane must remain solo. The ten family-current runners preserve `ghc_family_*` compatibility and remain owner-local. The successor seed is wholly synthetic emergency-communications message provenance and handover registrar, with ten zero-credit skill and runner ideas for Orin to review independently.

## Retained failures, privacy, and validation boundary

The activation baseline preserves Sable's repository seal and its one external post-seal PowerShell split-precedence failure as separate inherited truth. Five new Caelen startup failures remain zero-credit: a direct `foreach`-to-pipeline parser fault, an overbroad tree projection, a compact-JSON payload-digest assumption, a sparse-wrapper session-handle projection loss, and an unavailable optional rewrite utility. Each has one bounded recovery. No recovery erases or converts its failed witness; later failures must be appended before retry.

Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute local paths. Exact staged review operates on Git-index blobs. Five privacy classes distinguish scanner definitions from confirmed payload hits. Normalized-LF manifests bind exact byte domains. A passing owner-scoped receipt remains same-owner evidence under shared infrastructure, never an external audit, independent reproduction, exhaustive security, complete privacy, complete accessibility, professional review, empirical validation, or authority.

## X1 gate and terminal hold

X1 must pass its focused tests and exact staged review, become the sole direct child of Sable's exact final, be pushed cleanly, and prove local, upstream, tracking, and fresh-live equality before any x2 path or outcome exists. The phase ceiling is exactly three commits: one planning-only x1, one immutable x2 evidence commit, and one final closeout and seal commit.

Orin Thale remains uncontacted. Only after Caelen has a clean pushed fresh-live-equal exact final and one successful non-replayed owner-scoped canonical invocation may the newest live authority and roster be reread, the unique existing exact-title Orin Thale task be immediately reread, and at most one sanitized v680-v1 activation be sent if every duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guard passes. Repository route truth remains `PREPARED_NOT_SENT`. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
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
    owner_candidates = candidate_rows(proposals, 80, "CA6798-C", False)
    successor_candidates = candidate_rows(proposals, 20, "CA6798-SC", True)
    owner_cleanup = cleanup_rows(100, "CA6798-R", True)
    successor_cleanup = cleanup_rows(30, "CA6798-SR", False)

    activation_baseline = {
        "effective_negatives": 49919,
        "methods": 52428,
        "failed_witnesses": 21580,
        "bounded_passing_witnesses": 34439,
        "open_gaps": 437,
        "exact_gates": 428,
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
            "schema": "ghc.family.activation-intake.v679.v8",
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
            "source_packet_words": 2590,
            "source_packet_bytes": 21021,
            "source_packet_sha256_normalized_lf": SOURCE_PACKET_SHA256,
            "source_correction_note_sha256_normalized_lf": SOURCE_CORRECTION_NOTE_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_manifest_families_replayed": 4,
            "source_manifest_entries_replayed": 231,
            "source_manifest_mismatches": 0,
            "source_canonical_replayed": False,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
            "x1_state": "planning_only",
            "x2_implementation_present": False,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v679.v8",
            "owner": OWNER,
            "relational_role": "semantic-integrity and reversibility cartographer",
            "hope": "keep each surviving claim inspectable, falsifiable, recoverable, and unable to outrun its evidence or authority",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v679.v8",
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
            "manifest_families_replayed": 4,
            "manifest_entries_replayed": 231,
            "source_owner_paths": 124,
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
            "schema": "ghc.family.inherited-revalidation-freeze.v679.v8",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v679.v8",
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
            "schema": "ghc.family.portfolio-freeze.v679.v8",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_public_transit_timetable_correction_and_handover_registrar",
                "wholly_synthetic_transit_service_alert_accessibility_and_stop_identity_reviewer",
            ],
            "successor_practice_recommendation": "wholly_synthetic_emergency_communications_message_provenance_and_handover_registrar",
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
            "schema": "ghc.family.skill-runner-plan.v679.v8",
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
            "schema": "ghc.family.clean-fix-refine-plan.v679.v8",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v679.v8",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v679.v8",
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
            "schema": "ghc.family.workflow-plan.v679.v8",
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
                    "name": "create clean sparse Caelen lane",
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
            "schema": "ghc.family.threat-model.v679.v8.x1",
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
                "service-day and clock-role confusion",
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
                "service-day, time-role, and identifier guards",
                "source-status ledger",
            ],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v679.v8.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v679.v8.x1",
            "previous_owner": "Sable Rook",
            "previous_phase": "v679-v7",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "Orin Thale",
            "next_phase": "v680-v1",
            "state": "HOLD_BEFORE_CAELEN_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v679.v8.x1",
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
    review_rel = "docs/caelen-ash/v679-v8/validation/x1-staged-review.json"
    privacy_rel = "docs/caelen-ash/v679-v8/validation/x1-privacy-scan.json"
    manifest_rel = "docs/caelen-ash/v679-v8/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_caelen_ash_v679_v8_x1.py",
        "tests/test_ghc_family_caelen_ash_v679_v8_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/caelen-ash/v679-v8/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/caelen-ash/v679-v8/x2/") for path in staged):
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
                    path == "scripts/build_ghc_family_caelen_ash_v679_v8_x1.py"
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
        "schema": "ghc.family.privacy-scan.v679.v8.x1",
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
        "schema": "ghc.family.exact-staged-review.v679.v8.x1",
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
        "schema": "ghc.family.normalized-lf-index-manifest.v679.v8.x1",
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
        raise SystemExit("usage: build_ghc_family_caelen_ash_v679_v8_x1.py [--staged-review]")
