#!/usr/bin/env python3
"""Build Orin Thale v680-v1 planning-only x1 artifacts.

This builder creates only preregistration, portfolio, source, gate, privacy,
and lifecycle records.  It deliberately creates no x2 implementation or
observed proposal outcome.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v680-v1"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "415fd8fddc06573d8a672e61a496e56f4b7624e8"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v679-v8-full-tools"
BRANCH = "codex/GHC-Family/orin-thale-v680-v1-full-tools"
DECLARED_CHAIN_BEFORE = 9230
DECLARED_CHAIN_AFTER = 9290
QUARANTINE_THRESHOLD = 0.78
BASELINE = {
    "effective_negatives": 50087,
    "effective_methods": 52534,
    "failed_witnesses": 21748,
    "bounded_passing_witnesses": 34837,
    "open_gaps": 440,
    "exact_gates": 431,
}


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args,
        cwd=ROOT,
        input=input_bytes,
        capture_output=True,
        check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8").strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def title_tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def proposal_blob_records() -> tuple[list[dict[str, str]], dict[str, Any]]:
    tree = run(["git", "ls-tree", "-r", "-z", SOURCE])
    if tree.returncode:
        raise RuntimeError(tree.stderr.decode("utf-8", errors="replace"))
    selected: list[tuple[str, str]] = []
    for raw in tree.stdout.split(b"\0"):
        if not raw:
            continue
        head, raw_path = raw.split(b"\t", 1)
        parts = head.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if path.endswith(".json") and "proposal" in path.lower():
            selected.append((parts[2], path))

    request = b"".join((oid + "\n").encode("ascii") for oid, _ in selected)
    batch = run(["git", "cat-file", "--batch"], input_bytes=request)
    if batch.returncode:
        raise RuntimeError(batch.stderr.decode("utf-8", errors="replace"))
    cursor = 0
    parsed_paths = 0
    failures: list[dict[str, str]] = []
    records: list[dict[str, str]] = []
    for (_, path) in selected:
        line_end = batch.stdout.index(b"\n", cursor)
        header = batch.stdout[cursor:line_end].decode("ascii")
        cursor = line_end + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            failures.append({"path": path, "reason": "non_blob_or_missing"})
            continue
        size = int(parts[2])
        payload = batch.stdout[cursor : cursor + size]
        cursor += size + 1
        try:
            document = json.loads(payload.decode("utf-8"))
            parsed_paths += 1
        except Exception as exc:
            failures.append({"path": path, "reason": type(exc).__name__})
            continue
        for item in walk_dicts(document):
            title = item.get("title")
            proposal_id = item.get("proposal_id") or item.get("id")
            if isinstance(title, str) and isinstance(proposal_id, str):
                records.append(
                    {
                        "proposal_id": proposal_id,
                        "title": title,
                        "path": path,
                    }
                )
    deduped: dict[tuple[str, str], dict[str, str]] = {}
    for item in records:
        deduped[(item["proposal_id"], normalized_title(item["title"]))] = item
    return list(deduped.values()), {
        "proposal_json_paths_discovered": len(selected),
        "proposal_json_paths_parsed": parsed_paths,
        "proposal_json_parse_failures": failures,
        "reachable_id_title_records": len(deduped),
        "universal_9230_row_materialization_claimed": False,
    }


PROPOSAL_TITLES = [
    "CAP alert identifier sender and sent tuple uniqueness contract",
    "CAP status message-type and scope triad state machine",
    "CAP references-chain update cancel and error cycle guard",
    "Alert identifier collision across sender domains quarantine",
    "Sent effective onset and expiry chronology with missing-time reservation",
    "Information language-block uniqueness and default-language separation",
    "Category event and response-type non-authority taxonomy firewall",
    "Urgency severity certainty tuple with unknown-state preservation",
    "Audience field and public-private routing nonconflation",
    "Event-code and parameter namespace-value role separation",
    "Headline description instruction and contact disjoint-purpose schema",
    "Web resource URI digest and media-type provenance firewall",
    "Area polygon circle and geocode alternative consistency hold",
    "Altitude ceiling and unit pairing with absent vertical-scope refusal",
    "Multiple information area and resource attachment cardinality gate",
    "CAP profile declaration versus base-standard conformance nonpromotion",
    "Sender-name presentation and sender authority non-equivalence",
    "Restriction address scope and recipient-resolution vacancy",
    "Note annotation and operative instruction nonconflation",
    "Incident identifiers cross-message grouping and collision guard",
    "Deterministic surrogate receipt from CAP infoset without signature claim",
    "Source-payload raw and normalized digest-domain declaration",
    "Alert ingestion observed-at and sender timestamp separation",
    "Receive-order monotonic sequence and clock-skew quarantine",
    "Duplicate delivery idempotency key and content-digest decision",
    "Update-before-reference hold with bounded later reconciliation",
    "Cancellation without referenced active alert refusal",
    "Error message retention without superseded-message erasure",
    "Branched alert updates conflict set and adjudication vacancy",
    "Effective alert-view derivation graph with immutable predecessors",
    "Correction readback expected-versus-actual digest comparison",
    "Custodian acknowledgement and operational acceptance separation",
    "Handover lease expiry queue ownership and stale-claimant refusal",
    "Workload saturation pause resume and stop contract",
    "Bounded retry fixture with retry-after provenance and no network",
    "Dead-letter quarantine with manual-authority vacancy",
    "Accessible plain-language summary presence without conformance claim",
    "Language-tag well-formedness and untranslated-content disclosure",
    "Text audio and image alternative parity review vacancy",
    "Link-purpose resource-size and digest metadata completeness",
    "Minimum-disclosure transform with private-extension quarantine",
    "Public-instance pseudonymization without identity or anonymity claim",
    "Real authorised warning-agency CAP profile review vacancy",
    "Real emergency-operator correction workflow proxy",
    "Real assistive-technology public-alert evaluation vacancy",
    "Real multilingual community review and affected-party acceptance vacancy",
    "Real geospatial targeting precision and over-alerting study proxy",
    "Real cell-broadcast transformation interoperability vacancy",
    "Real digital-signature certificate status and revocation verification vacancy",
    "Real incident-feed retention and legal-hold governance vacancy",
    "Independent parser canonicalization and digest security-review vacancy",
    "Independent reproduction of alert-lineage result vacancy",
    "Preregistered blind matched-budget alert-handover arms vacancy",
    "Real warning latency reliability and failure-distribution evidence proxy",
    "Zero-row official CAP example adapter and inference refusal",
    "Real CAP-NZ corpus error and likelihood measurement gap",
    "Real disability privacy and translation outcome dataset gap",
    "Public-alert issuance cancellation and life-safety authority exact gate",
    "Emergency-warning legal remedy and affected-party authority exact gate",
    "Māori place-based warning data governance and wording exact gate",
]


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    if index <= 42:
        return "safe_now"
    if index <= 54:
        return "candidate_proxy_only"
    if index <= 57:
        return "external_evidence_open_gap"
    return "exact_approval"


def execution_lane(index: int) -> str:
    if index <= 42:
        return "owner_local_synthetic_zero_row"
    if index <= 54:
        return "bounded_representation_without_real_execution"
    if index <= 57:
        return "unexecuted_empirical_vacancy"
    return "unexecuted_competent_authority_gate"


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["OASIS-CAP-1.2", "NEMA-CAP-NZ-TS04-18"]
    if index <= 36:
        return ["OASIS-CAP-1.2", "W3C-PROV-DM", "RFC8785"]
    if index <= 42:
        return ["W3C-WCAG22", "NEMA-EMA-TS06-26", "OASIS-CAP-1.2"]
    if index <= 57:
        return ["OASIS-CAP-1.2", "NEMA-CAP-NZ-TS04-18", "W3C-WCAG22"]
    if index == 60:
        return ["TMR-MDS-PRINCIPLES", "NEMA-CAP-NZ-TS04-18"]
    return ["NEMA-EMA-TS06-26", "OASIS-CAP-1.2"]


def proposals() -> list[dict[str, Any]]:
    rows = []
    mutation_types = [
        "missing_required_field",
        "identity_role_swap",
        "stale_precondition_digest",
        "chronology_inversion",
        "authority_promotion",
    ]
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"OR6801-N{index:03d}"
        expected = disposition(index)
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A bounded synthetic validator for {title.lower()} can reject its five "
                    "preregistered counterexamples while preserving every empirical and authority boundary."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract is falsified if any preregistered invalid fixture is "
                    "accepted, its bounded positive structure is rejected, or a protected gate is promoted."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/orin-thale/v680-v1/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/orin-thale/v680-v1/x2/mutations.json#{proposal_id}",
                ],
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid "
                    "mutations are rejected, and no wider claim or authority is inferred."
                ),
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, "
                    "and regenerate from this immutable x1 contract."
                ),
                "protected_gates": [
                    "real participants and operators",
                    "empirical measurements and likelihoods",
                    "production warning issuance or cancellation",
                    "professional and public-safety authority",
                    "legal cultural affected-party and Māori authority",
                    "privacy-complete accessibility-complete and exhaustive-security claims",
                    "independent reproduction proof canon and Stage 20",
                ],
                "expected_disposition": expected,
                "preregistered_rejecting_mutations": [
                    {
                        "mutation_id": f"{proposal_id}-M{offset:02d}",
                        "mutation_type": mutation_type,
                        "expected_result": "rejected_zero_credit",
                    }
                    for offset, mutation_type in enumerate(mutation_types, start=1)
                ],
            }
        )
    return rows


OFFICIAL_SOURCES = [
    {
        "source_id": "OASIS-CAP-1.2",
        "title": "Common Alerting Protocol Version 1.2",
        "url": "https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html",
        "status": "OASIS_Standard_2010_stable_checked_2026-08-31",
        "use": "alert, info, area, resource, identifier, sender, status, message-type, scope, reference, update, cancellation, and refusal vocabulary only",
    },
    {
        "source_id": "NEMA-CAP-NZ-TS04-18",
        "title": "Common Alerting Protocol CAP-NZ Technical Standard",
        "url": "https://www.civildefence.govt.nz/guidance-training/guidelines/technical-standards/common-alerting-protocol",
        "status": "official_page_last_updated_2025-11-28_checked_2026-08-31",
        "use": "New Zealand profile and authorised-user boundary vocabulary only",
    },
    {
        "source_id": "NEMA-EMA-TS06-26",
        "title": "Emergency Mobile Alert protocols for User Agencies",
        "url": "https://www.civildefence.govt.nz/guidance-training/guidelines/technical-standards/0626-emergency-mobile-alert-protocols-for-user-agencies",
        "status": "official_page_last_updated_2026-08-25_checked_2026-08-31",
        "use": "authorised-agency, caution, consistency, life-safety, and non-authority refusal vocabulary only",
    },
    {
        "source_id": "W3C-PROV-DM",
        "title": "PROV-DM The PROV Data Model",
        "url": "https://www.w3.org/TR/prov-dm/",
        "status": "W3C_Recommendation_stable",
        "use": "entity, activity, agent, derivation, revision, attribution, and provenance vocabulary only",
    },
    {
        "source_id": "W3C-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C_Recommendation_2024-12-12_checked_2026-08-31",
        "use": "structural accessibility and manual-evaluation reservation only",
    },
    {
        "source_id": "RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "informational_stable",
        "use": "deterministic synthetic receipt serialization and digest-domain vocabulary only",
    },
    {
        "source_id": "JSON-SCHEMA-2020-12",
        "title": "JSON Schema Draft 2020-12",
        "url": "https://json-schema.org/draft/2020-12",
        "status": "published_stable",
        "use": "structural validation and declared-vocabulary concepts only",
    },
    {
        "source_id": "TMR-MDS-PRINCIPLES",
        "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "authority_boundary_context_only_checked_2026-08-31",
        "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
    },
]


STARTUP_FAILURES = [
    {
        "failure_id": "OR6801-START-N001",
        "failed_witness": "An oversized candidate line projection truncated before an attributable complete read.",
        "recovery": "Read the same immutable candidate in bounded numbered windows through EOF.",
        "recurrence_guard": "Measure line count first and cap immutable text windows before projection.",
    },
    {
        "failure_id": "OR6801-START-N002",
        "failed_witness": "A PowerShell foreach expression was piped directly and raised EmptyPipeElement.",
        "recovery": "Materialised the foreach result before piping it to JSON conversion.",
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement in phase wrappers.",
    },
    {
        "failure_id": "OR6801-START-N003",
        "failed_witness": "The full authorization-state projection truncated.",
        "recovery": "Read the exact current-state JSON in bounded numbered windows through EOF.",
        "recurrence_guard": "Project large authorization records by measured window rather than raw whole-file output.",
    },
    {
        "failure_id": "OR6801-START-N004",
        "failed_witness": "A full manifest display exceeded the bounded projection.",
        "recovery": "Used scalar count projection and exact normalized-LF Git-blob replay.",
        "recurrence_guard": "Validate manifest entries computationally and display only attributable summaries.",
    },
    {
        "failure_id": "OR6801-START-N005",
        "failed_witness": "The first full final-validator display truncated.",
        "recovery": "Read all 315 lines in three bounded numbered windows without executing the validator.",
        "recurrence_guard": "Measure validator line count and use bounded windows before any display.",
    },
    {
        "failure_id": "OR6801-START-N006",
        "failed_witness": "Two concurrent read-only Python probes yielded sessions whose metadata was omitted by the wrapper projection.",
        "recovery": "Reran only the manifest and JSON-parse dependencies to bounded completion with explicit result metadata.",
        "recurrence_guard": "Preserve session identifiers whenever a concurrent command can outlive the initial yield.",
    },
    {
        "failure_id": "OR6801-START-N007",
        "failed_witness": "Two stale v676 artifact names were queried against the v679 exact tree and were absent.",
        "recovery": "Derived the v679 artifact set from its exact Git tree and committed activation candidate.",
        "recurrence_guard": "Never carry phase-relative artifact filenames across owner or version boundaries.",
    },
]


def proposal_audit(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inherited, stats = proposal_blob_records()
    if stats["proposal_json_parse_failures"]:
        raise RuntimeError("reachable proposal JSON parse failures must be resolved before freeze")
    normalized_inherited = {}
    for item in inherited:
        normalized_inherited.setdefault(normalized_title(item["title"]), item)

    exact_collisions = []
    neighbor_rows = []
    quarantined = []
    selected_reviews: list[dict[str, Any]] = []
    selected_keys: set[tuple[str, str]] = set()
    for row in rows:
        title = row["title"]
        norm = normalized_title(title)
        if norm in normalized_inherited:
            exact_collisions.append(
                {
                    "proposal_id": row["proposal_id"],
                    "inherited": normalized_inherited[norm],
                }
            )
        best = None
        best_score = -1.0
        for inherited_row in inherited:
            score = jaccard(title, inherited_row["title"])
            if score > best_score:
                best, best_score = inherited_row, score
        neighbor = {
            "proposal_id": row["proposal_id"],
            "title": title,
            "best_inherited_neighbor": best,
            "token_jaccard": round(best_score, 6),
            "quarantined": best_score >= QUARANTINE_THRESHOLD,
        }
        neighbor_rows.append(neighbor)
        if neighbor["quarantined"]:
            quarantined.append(neighbor)
        if best is not None:
            key = (best["proposal_id"], normalized_title(best["title"]))
            if key not in selected_keys:
                selected_keys.add(key)
                selected_reviews.append(
                    {
                        **best,
                        "review_state": "inherited_zero_credit_evidence_only",
                        "novelty_credit": 0,
                        "completion_credit": 0,
                    }
                )
    for item in inherited:
        if len(selected_reviews) >= 60:
            break
        key = (item["proposal_id"], normalized_title(item["title"]))
        if key not in selected_keys:
            selected_keys.add(key)
            selected_reviews.append(
                {
                    **item,
                    "review_state": "inherited_zero_credit_evidence_only",
                    "novelty_credit": 0,
                    "completion_credit": 0,
                }
            )
    if len(selected_reviews) < 60:
        raise RuntimeError("fewer than sixty reachable inherited proposal reviews")
    if exact_collisions or quarantined:
        raise RuntimeError(
            f"proposal novelty quarantine: exact={len(exact_collisions)} near={len(quarantined)}"
        )
    audit = {
        "schema": "ghc.family.proposal-chain-audit.v680.v1.x1",
        "owner": "Orin Thale",
        "phase": "v680-v1",
        "source": SOURCE,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "new_proposal_count": len(rows),
        "quarantine_threshold_token_jaccard": QUARANTINE_THRESHOLD,
        "exact_title_collisions": exact_collisions,
        "quarantined_neighbors": quarantined,
        "maximum_neighbor_score": max(item["token_jaccard"] for item in neighbor_rows),
        "neighbor_reviews": neighbor_rows,
        "audit_scope": {
            **stats,
            "claim": "bounded all-reachable-exact-source proposal audit; no universal 9230-row proof",
        },
    }
    return audit, selected_reviews[:60]


def make_portfolio() -> dict[str, Any]:
    def records(prefix: str, count: int, lane: str, credit: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": f"OR6801-{prefix}-{index:03d}",
                "lane": lane,
                "planned_action": (
                    f"Bounded owner-local {lane.replace('_', ' ')} record {index:03d} linked to "
                    f"OR6801-N{((index - 1) % 60) + 1:03d}."
                ),
                "credit_boundary": credit,
                "x1_state": "preregistered_not_executed",
            }
            for index in range(1, count + 1)
        ]

    return {
        "schema": "ghc.family.portfolio-freeze.v680.v1.x1",
        "owner": "Orin Thale",
        "phase": "v680-v1",
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly_synthetic_CAP_alert_lifecycle_and_provenance_registrar",
            "wholly_synthetic_public_warning_accessibility_and_minimum_disclosure_reviewer",
            "wholly_synthetic_alert_correction_cancellation_workload_and_handover_steward",
        ],
        "safe_now": records("SN", 120, "safe_now", "bounded_owner_local_only"),
        "owner_candidates": records("CAND", 80, "candidate", "no_core_outcome_promotion"),
        "successor_candidates": records("SUCC-CAND", 20, "successor_seed", "zero_Orin_credit"),
        "exact_approval": records("EXACT", 20, "exact_approval", "unexecuted_without_exact_authority"),
        "blocked": records("BLOCK", 10, "blocked", "unexecuted_missing_target_or_authority"),
        "owner_clean_fix_refine": records("CFR", 100, "clean_fix_refine", "bounded_additive_owner_local_only"),
        "successor_clean_fix_refine": records("SUCC-CFR", 30, "successor_seed", "zero_Orin_credit"),
        "owner_skill_ideas": [
            {
                "skill_id": f"OR6801-SK-{index:02d}",
                "name": f"ghc-family-emergency-alert-{index:02d}",
                "x1_state": "planned_not_built",
                "global_install": False,
            }
            for index in range(1, 21)
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"OR6801-RN-{index:02d}",
                "name": f"ghc_family_emergency_alert_runner_{index:02d}.py",
                "x1_state": "planned_not_built",
            }
            for index in range(1, 11)
        ],
        "successor_skill_ideas": [
            {
                "idea_id": f"OR6801-SUCC-SK-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_runner_ideas": [
            {
                "idea_id": f"OR6801-SUCC-RN-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_practice_recommendation": (
            "one wholly synthetic documentary-film cue-sheet provenance and accessibility handover lens"
        ),
        "commit_cap": {"x1": 1, "x2": 2, "total": 3},
        "materialized_file_stop": 2000,
        "document_word_cap": 100000,
        "caps_are_ceilings": True,
    }


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    patterns = privacy_patterns()
    candidates = []
    confirmed = []
    for path in paths:
        data = path.read_bytes()
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                definition_only = path.name == Path(__file__).name
                record = {"path": rel(path), "class": class_name}
                if definition_only:
                    candidates.append({**record, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append(record)
    return {
        "schema": "ghc.family.privacy-scan.v680.v1.x1",
        "owner": "Orin Thale",
        "phase": "v680-v1",
        "privacy_classes": list(patterns),
        "scanned_paths": len(paths),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
    }


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder must begin at the exact Caelen final")
    if git("status", "--porcelain=v1"):
        allowed = {
            "scripts/build_ghc_family_orin_thale_v680_v1_x1.py",
            "tests/test_ghc_family_orin_thale_v680_v1_x1.py",
        }
        current = {
            line[3:].replace("\\", "/")
            for line in git("status", "--porcelain=v1").splitlines()
            if len(line) >= 4
        }
        if not current <= allowed:
            raise RuntimeError(f"unexpected pre-build worktree state: {sorted(current - allowed)}")

    source_tracking = git("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}")
    live_source = live_row.split("\t", 1)[0] if live_row else ""
    if source_tracking != SOURCE or live_source != SOURCE:
        raise RuntimeError("source branch is no longer fresh-live equal")

    rows = proposals()
    audit, inherited_reviews = proposal_audit(rows)
    portfolio = make_portfolio()
    expected_counts = {
        label: sum(row["expected_disposition"] == label for row in rows)
        for label in ("completed", "represented", "open_gap", "exact_gate")
    }
    if expected_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("expected disposition arithmetic failed")

    now = datetime.now(timezone.utc).isoformat()
    X1.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)

    documents: dict[Path, Any] = {
        X1 / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "source": SOURCE,
            "delivery_state": "LIVE_ACTIVATION_ACKNOWLEDGED_EXTERNALLY",
            "prepared_repository_candidate_is_delivery": False,
            "work_solo": True,
            "subagents_or_delegation": False,
            "successor_precontact": False,
            "identity_language_is_evidence": False,
        },
        X1 / "approval-hold-register.json": {
            "schema": "ghc.family.approval-holds.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "exact_approval_count": 20,
            "blocked_count": 10,
            "executed_count": 0,
            "rule": "Broad authorization does not supply a missing exact target, system, cost, rollback, affected-party consent, legal authority, cultural authority, or Māori authority.",
        },
        X1 / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "owner_records": portfolio["owner_clean_fix_refine"],
            "successor_records": portfolio["successor_clean_fix_refine"],
            "x1_execution_count": 0,
        },
        X1 / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v680.v1.x1",
            "owner": "Orin Thale",
            "pronouns": "they/them optional relational working language",
            "role": "public-warning provenance and correction-boundary cartographer",
            "hope": "make every synthetic alert lineage, correction, refusal, and authority vacancy easy to challenge and reverse",
            "evidence_of_consciousness_personhood_continuity_agency_or_authority": False,
            "corrigibility": "Hamish may pause rename redirect narrow or stop the route.",
        },
        X1 / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "review_count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
        X1 / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "inherited_baseline": BASELINE,
            "new_failures": STARTUP_FAILURES,
            "new_failure_count": len(STARTUP_FAILURES),
            "effective_x1_startup_counts": {
                "effective_negatives": BASELINE["effective_negatives"] + len(STARTUP_FAILURES),
                "effective_methods": BASELINE["effective_methods"] + len(STARTUP_FAILURES),
                "failed_witnesses": BASELINE["failed_witnesses"] + len(STARTUP_FAILURES),
                "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
                "open_gaps": BASELINE["open_gaps"],
                "exact_gates": BASELINE["exact_gates"],
            },
            "failure_erasure": False,
            "recoveries_promote_failed_witnesses": False,
        },
        X1 / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "source": SOURCE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "proposals": rows,
            "x2_outcomes_present": False,
        },
        X1 / "official-primary-source-ledger.json": {
            "schema": "ghc.family.official-primary-sources.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "checked_at_utc": now,
            "entries": OFFICIAL_SOURCES,
            "web_checks": len(OFFICIAL_SOURCES),
            "network_data_queries": 0,
            "real_data_rows": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        X1 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "lifecycle": "PLANNING_ONLY_X1",
            "source": SOURCE,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "observed_outcome_count": 0,
            "x2_implementation_present": False,
            "inherited_open_gaps": BASELINE["open_gaps"],
            "inherited_exact_gates": BASELINE["exact_gates"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        X1 / "portfolio-freeze.json": portfolio,
        X1 / "proposal-chain-audit.json": audit,
        X1 / "route-plan.json": {
            "schema": "ghc.family.route-plan.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "route_state": "TERMINAL_GATE_HELD",
            "prospective_successor_title": "Liora Venn",
            "prospective_successor_phase": "v680-v2",
            "precontacted": False,
            "created_or_forked_task": False,
            "send_count": 0,
            "continuation_authority_ceiling": "through_v725-v8_one_terminally_validated_edge_at_a_time",
            "send_requires": [
                "clean pushed exact final",
                "one successful non-replayed owner canonical",
                "newest live authority and roster refresh",
                "one exact-title match and immediate reread",
                "duplicate pause redirect rename standby usage privacy evidence safety legal cultural affected-party and Māori-authority guards",
            ],
        },
        X1 / "skill-runner-plan.json": {
            "schema": "ghc.family.skill-runner-plan.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "skills": portfolio["owner_skill_ideas"],
            "runners": portfolio["owner_runner_ideas"],
            "successor_skill_ideas": portfolio["successor_skill_ideas"],
            "successor_runner_ideas": portfolio["successor_runner_ideas"],
            "built_in_x1": 0,
            "smoke_used_in_x1": 0,
            "global_installs": 0,
        },
        X1 / "source-verification.json": {
            "schema": "ghc.family.source-verification.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_tracking": source_tracking,
            "source_fresh_live": live_source,
            "source_tracking_equal": source_tracking == SOURCE,
            "source_fresh_live_equal": live_source == SOURCE,
            "caelen_source": "9a6cdb6c0e1630e43502a3b62b71d9a198d37dba",
            "caelen_x1": "196de83c91c9d13a76fd4baaf296e2ac15997607",
            "caelen_evidence": "fe9e87ba4fea0a0ddba263886f77d90f6fb6665d",
            "caelen_final": SOURCE,
            "caelen_phase_commits": 3,
            "caelen_merges": 0,
            "caelen_canonical_replayed": False,
        },
        X1 / "threat-model.json": {
            "schema": "ghc.family.threat-model.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "assets": [
                "synthetic alert lineage",
                "retained correction and failure evidence",
                "privacy and minimum-disclosure boundaries",
                "authority and affected-party gates",
            ],
            "threats": [
                "stale or colliding alert identity",
                "update or cancellation without a valid reference",
                "authority promotion from structural validation",
                "privacy leakage through extensions or route artifacts",
                "accessibility structure mistaken for conformance",
                "real warning action inferred from zero-row fixtures",
            ],
            "controls": [
                "immutable source and x1",
                "five rejecting mutations per proposal",
                "normalized-LF manifests",
                "five-class privacy scan",
                "exact gate noncompensation",
                "zero network and zero real rows",
            ],
            "residual_risk": "All real emergency communication, affected-party, privacy-complete, accessibility-complete, legal, cultural, Māori-authority, and public-safety work remains external.",
        },
        X1 / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "workload_controls": ["pause", "resume", "stop", "bounded retry", "handover"],
            "self_report_is_authority_evidence": False,
            "identity_continuity_claimed": False,
            "user_control_preserved": True,
        },
        X1 / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v680.v1.x1",
            "owner": "Orin Thale",
            "phase": "v680-v1",
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {"order": 1, "name": "read activation skills schemas and overlays", "state": "completed"},
                {"order": 2, "name": "verify immutable source manifests receipt and live equality", "state": "completed"},
                {"order": 3, "name": "create clean sparse Orin lane", "state": "completed"},
                {"order": 4, "name": "freeze test push and prove planning-only x1", "state": "in_progress"},
                {"order": 5, "name": "build bounded x2 and retain every failure", "state": "pending"},
                {"order": 6, "name": "seal final push and run one exclusive canonical", "state": "pending"},
                {"order": 7, "name": "refresh live route and send at most once", "state": "pending"},
            ],
            "validation": {
                "owner_scoped_delta_only": True,
                "unchanged_history_scan": False,
                "cross_lane_scan": False,
                "one_successful_canonical": True,
                "post_success_replay": False,
            },
        },
    }
    for path, value in documents.items():
        write_json(path, value)

    overview = f"""# Orin Thale v680-v1 planning-only x1

This immutable planning freeze begins from exact Caelen final {SOURCE}.  It
preregisters sixty Orin proposals after a bounded all-reachable exact-source
semantic-neighbour audit.  It does not claim that one materialised ledger
contains every declared inherited row, and it makes no universal novelty proof.

The primary pillar is Freed ID and CBR Heart.  GMUT Mind and THOS Body remain
explicit and protected.  The bounded learning lenses are a wholly synthetic CAP
alert lifecycle and provenance registrar, a wholly synthetic public-warning
accessibility and minimum-disclosure reviewer, and a wholly synthetic alert
correction, cancellation, workload, and handover steward.

The x1 portfolio freezes 120 safe-now items, 80 owner candidates, 20 successor
candidate seeds, 20 exact-approval holds, 10 blocked holds, 20 owner skill
plans, 10 owner runner plans, 100 owner CLEAN/FIX/REFINE records, and 30
successor CLEAN/FIX/REFINE seeds.  None is executed in x1.

Expected proposal dispositions are 42 completed, 12 represented, 3 open_gap,
and 3 exact_gate.  These are expectations only.  No observed x2 outcome or
completion claim appears in this freeze.

OASIS CAP 1.2, NEMA CAP-NZ and Emergency Mobile Alert guidance, W3C PROV-DM,
WCAG 2.2, RFC 8785, JSON Schema 2020-12, and Te Mana Raraunga principles supply
only vocabulary and refusal conditions.  No source is treated as an
observation, endorsement, certificate, affected-party decision, or authority
grant.  Zero real alerts, people, devices, locations, measurements, incidents,
identity events, external writes, or authority actions are used.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family without empirical confirmation or Theory-of-Everything proof.  THOS
remains synthetic or proxy-only without governed real arms and independent
review.  Freed ID remains synthetic and nonproduction without real keys,
proofs, live lifecycle, interoperability, security, privacy, recovery, and trust
governance evidence.  Emergency warning issuance and cancellation, public
safety, legal remedy, affected-party legitimacy, Māori wording and data
governance, and Māori authority remain exact-gated.

Names, pronouns, roles, hopes, family language, and continuity language are
relational working language only.  They are not evidence of consciousness,
personhood, identity continuity, employment, qualification, independent agency,
or authority.  The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X1 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X1 / "integrated-overview.md", Path(__file__), ROOT / "tests" / "test_ghc_family_orin_thale_v680_v1_x1.py"],
        key=rel,
    )
    if len(entry_paths) != 20:
        raise RuntimeError(f"x1 manifest entry arithmetic changed: {len(entry_paths)}")

    staged_review_path = VALIDATION / "x1-staged-review.json"
    privacy_path = VALIDATION / "x1-privacy-scan.json"
    manifest_path = VALIDATION / "x1-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_review_path, privacy_path, manifest_path], key=rel)
    staged_review = {
        "schema": "ghc.family.staged-review.v680.v1.x1",
        "owner": "Orin Thale",
        "phase": "v680-v1",
        "source": SOURCE,
        "expected_paths": [rel(path) for path in all_paths],
        "expected_path_count": len(all_paths),
        "planning_only": True,
        "x2_paths": [],
        "unexpected_paths": [],
    }
    write_json(staged_review_path, staged_review)

    scan = scan_paths(entry_paths + [staged_review_path])
    if scan["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {scan['confirmed_hits']}")
    write_json(privacy_path, scan)

    manifest = {
        "schema": "ghc.family.normalized-lf-index-manifest.v680.v1.x1",
        "owner": "Orin Thale",
        "phase": "v680-v1",
        "source": SOURCE,
        "declared_self_exclusions": [rel(staged_review_path), rel(privacy_path), rel(manifest_path)],
        "entry_count": len(entry_paths),
        "entries": [
            {
                "path": rel(path),
                "bytes": len(normalized_bytes(path)),
                "sha256": hashlib.sha256(normalized_bytes(path)).hexdigest(),
            }
            for path in entry_paths
        ],
    }
    write_json(manifest_path, manifest)
    print(
        json.dumps(
            {
                "status": "PREPARED_PLANNING_ONLY_X1",
                "proposal_count": len(rows),
                "expected_dispositions": expected_counts,
                "manifest_entries": len(entry_paths),
                "staged_paths": len(all_paths),
                "confirmed_privacy_hits": scan["confirmed_hit_count"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
