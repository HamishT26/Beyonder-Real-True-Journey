#!/usr/bin/env python3
"""Build Orin Thale v684-v7 planning-only x1 artifacts.

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
PHASE = ROOT / "docs" / "orin-thale" / "v684-v7"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "162b40162f1045c5ad91cfb454fad10973bf4914"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v684-v6-full-tools"
BRANCH = "codex/GHC-Family/orin-thale-v684-v7-full-tools"
DECLARED_CHAIN_BEFORE = 11030
DECLARED_CHAIN_AFTER = 11090
QUARANTINE_THRESHOLD = 0.78
BASELINE = {
    "effective_negatives": 59738,
    "effective_methods": 73698,
    "failed_witnesses": 30799,
    "bounded_passing_witnesses": 54233,
    "open_gaps": 531,
    "exact_gates": 521,
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
        "universal_11030_row_materialization_claimed": False,
    }


PROPOSAL_TITLES = [
    "Synthetic herbarium accession namespace with every institution and object absent",
    "Catalogue number occurrence identifier and material-entity identity role separation",
    "Specimen object label image and transcription referent firewall",
    "Herbarium sheet packet fragment and derivative relationship typing",
    "Collection code institution code and owner-institution code nonconflation",
    "Accession number catalogue number and collector number role split",
    "Original label line order and normalized transcription separation",
    "Verbatim scientific name and interpreted taxon identification nonconversion",
    "Determination-event revision lineage without taxonomic authority",
    "Type-status field and nomenclatural-act authority separation",
    "Recorded-by agent string and real-person identity nonlinkage",
    "Event-date verbatim text and normalized-date uncertainty separation",
    "Locality verbatim text and georeferenced-coordinate separation",
    "Coordinate uncertainty and georeference-protocol vacancy",
    "Sensitive-locality generalization without exact coordinate disclosure",
    "Habitat notes and inferred ecological claim nonconversion",
    "Collection event and specimen-preparation event separation",
    "Preparations vocabulary with treatment action refused",
    "Material entity occurrence and organism concept boundary contract",
    "Associated-media identifier and image-binary noningestion",
    "Image view scale colour target and calibration vacancy",
    "OCR suggestion and curator-approved transcription nonequivalence",
    "Illegible-text marker and missing-value distinction",
    "Bracketed editorial expansion and original-label text nonerasure",
    "Diacritic Unicode and transliteration provenance guard",
    "Controlled-vocabulary mapping with original term retention",
    "Duplicate catalogue-identifier quarantine without record deletion",
    "Split sheet and mixed-gathering reconciliation hold",
    "Barcode replacement and legacy-identifier alias lineage",
    "Container drawer cabinet and location-path role separation",
    "Collection-location move event and current-location state separation",
    "Loan gift exchange and custody vocabulary without transaction",
    "Restriction marker and access-decision authority vacancy",
    "Rights statement licence and reproduction-permission nonequivalence",
    "Donor collector determiner and digitizer role minimization",
    "Personal-name minimum disclosure and indirect-collection notice placeholder",
    "Correction request contest annotation and remedy-queue lineage",
    "Amendment rollback preserving prior transcription and failed witness",
    "Shift handover with unresolved specimen-identity exceptions",
    "Workload pause resume stop and transfer-of-custody nonclaim",
    "Deterministic JSON digest for a zero-row specimen record",
    "Accessible specimen-summary table structural contract",
    "Represented GMUT typed specimen-occurrence state analogy without physical inference",
    "Represented GMUT provenance-residual analogy without likelihood or posterior",
    "Represented GMUT georeference-uncertainty board without a physical datum",
    "Represented THOS digitization-queue proxy without an operator",
    "Represented THOS correction-readback handover proxy without a participant",
    "Represented THOS workload cancellation and quiescence proxy",
    "Represented Freed ID synthetic curator capability without person identity",
    "Represented Freed ID synthetic specimen-record attestation without keys or proofs",
    "Represented CBR minimum disclosure for collector and donor names",
    "Represented CBR contest correction access and remedy structure with authority vacant",
    "Represented Latimer Core collection-description crosswalk without conformance",
    "Represented Darwin Core term crosswalk without biodiversity-data conformance",
    "Open gap for real specimens labels images collections and practitioners",
    "Open gap for empirical transcription and georeferencing accuracy with independent review",
    "Open gap for participatory disability-access evaluation community consultation and Māori-authority review of collection interfaces",
    "Exact gate for custody access reproduction conservation and work-release authority",
    "Exact gate for taonga mātauranga sensitive-locality Māori data governance and Māori authority",
    "Stage 20 nonpromotion latch for participant-free synthetic herbarium metadata refusing empirical deployment identity AGI ASI personhood theorem canon and final-physics status",
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
        return ["TDWG-DWC-2026-05-26", "TDWG-LTC-1.0.0", "W3C-PROV-O"]
    if index <= 32:
        return ["TDWG-DWC-2026-05-26", "TDWG-AC", "W3C-PROV-O", "RFC8785"]
    if index <= 42:
        return ["NZ-PRIVACY-PRINCIPLES", "NZ-IPP3A", "W3C-WCAG22", "RFC8785"]
    if index <= 54:
        return ["TDWG-DWC-2026-05-26", "TDWG-LTC-1.0.0", "W3C-PROV-O"]
    if index <= 57:
        return ["TDWG-DWC-2026-05-26", "W3C-WCAG22", "TMR-MDS-PRINCIPLES"]
    if index == 59:
        return ["TMR-MDS-PRINCIPLES", "TDWG-DWC-2026-05-26"]
    return ["TDWG-LTC-1.0.0", "NZ-PRIVACY-PRINCIPLES"]


def proposals() -> list[dict[str, Any]]:
    rows = []
    mutation_types = [
        "missing_required_field",
        "identifier_role_swap",
        "stale_precondition_digest",
        "correction_order_inversion",
        "authority_promotion",
    ]
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"OR6847-N{index:03d}"
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
                    f"docs/orin-thale/v684-v7/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/orin-thale/v684-v7/x2/mutations.json#{proposal_id}",
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
                    "production collection cataloguing or custody use",
                    "professional collections conservation and work-release authority",
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
        "source_id": "TDWG-DWC-2026-05-26",
        "title": "Darwin Core List of Terms",
        "url": "https://dwc.tdwg.org/list/",
        "status": "official_TDWG_current_term_list_version_2026-05-26_checked_2026-09-03",
        "use": "material entity occurrence identification location provenance and usage-policy vocabulary only; no specimen record or conformance claim",
    },
    {
        "source_id": "TDWG-LTC-1.0.0",
        "title": "TDWG Latimer Core Standard",
        "url": "https://ltc.tdwg.org/",
        "status": "official_TDWG_Latimer_Core_v1.0.0_checked_2026-09-03",
        "use": "collection description grouping and discovery vocabulary only; no collection inventory or conformance claim",
    },
    {
        "source_id": "TDWG-AC",
        "title": "TDWG Audiovisual Core",
        "url": "https://ac.tdwg.org/",
        "status": "official_TDWG_maintained_standard_checked_2026-09-03",
        "use": "biodiversity multimedia metadata and fitness-description vocabulary only; no media ingestion or conformance claim",
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "title": "New Zealand Office of the Privacy Commissioner Privacy Principles",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "official_Privacy_Act_2020_principles_surface_checked_2026-09-03",
        "use": "collection storage access correction accuracy retention use disclosure and identifier refusal vocabulary only; no legal interpretation",
    },
    {
        "source_id": "NZ-IPP3A",
        "title": "Information Privacy Principle 3A",
        "url": "https://www.privacy.org.nz/privacy-principles/3a/",
        "status": "official_IPP3A_in_force_from_2026-05-01_checked_2026-09-03",
        "use": "indirect-collection notification access and correction vocabulary only; no legal conclusion or exception claim",
    },
    {
        "source_id": "TDWG-STANDARDS",
        "title": "Biodiversity Information Standards catalogue",
        "url": "https://www.tdwg.org/standards/",
        "status": "official_TDWG_current_standards_catalogue_checked_2026-09-03",
        "use": "maintenance-status and standard-family vocabulary only; no certification endorsement or implementation claim",
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C_Recommendation_stable_checked_2026-09-03",
        "use": "entity, activity, derivation, revision, attribution, and provenance vocabulary only; no conformance",
    },
    {
        "source_id": "W3C-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C_Recommendation_checked_2026-09-03",
        "use": "structural accessibility vocabulary with manual and affected-user evaluation reserved",
    },
    {
        "source_id": "RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "informational_stable_checked_2026-09-03",
        "use": "deterministic synthetic receipt serialization and digest-domain vocabulary only",
    },
    {
        "source_id": "RFC3339",
        "title": "RFC 3339 Date and Time on the Internet",
        "url": "https://www.rfc-editor.org/rfc/rfc3339.html",
        "status": "standards_track_stable_checked_2026-09-03",
        "use": "timestamp syntax vocabulary only; no collection event time or operational equivalence",
    },
    {
        "source_id": "JSON-SCHEMA-2020-12",
        "title": "JSON Schema Draft 2020-12",
        "url": "https://json-schema.org/draft/2020-12",
        "status": "published_stable_checked_2026-09-03",
        "use": "synthetic record validation and declared-vocabulary concepts only",
    },
    {
        "source_id": "TMR-MDS-PRINCIPLES",
        "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "authority_boundary_context_only_checked_2026-09-03",
        "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
    },
]


STARTUP_FAILURES = [
    {
        "failure_id": "OR6847-ST-N001",
        "failed_witness": "The first whole authorization-state projection truncated before EOF.",
        "recovery": "Reread the exact current authorization state in bounded numbered windows through EOF.",
        "recurrence_guard": "Measure dense mutable-state documents and use conservative windows before projection.",
    },
    {
        "failure_id": "OR6847-ST-N002",
        "failed_witness": "A combined exact owner-manifest display truncated before every entry was attributable.",
        "recovery": "Reread the missing deterministic windows and validate every entry computationally.",
        "recurrence_guard": "Use compact manifest arithmetic plus bounded entry windows for large immutable manifests.",
    },
    {
        "failure_id": "OR6847-ST-N003",
        "failed_witness": "A PowerShell foreach producer was piped directly and raised EmptyPipeElement before any Git mutation.",
        "recovery": "Materialized the foreach rows before JSON conversion.",
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement.",
    },
    {
        "failure_id": "OR6847-ST-N004",
        "failed_witness": "A JavaScript orchestration wrapper contained invalid nested quoting and failed before launching its Git probes.",
        "recovery": "Split the wrapper into short literal scalar commands.",
        "recurrence_guard": "Prefer small independently attributable commands when PowerShell and JavaScript quoting interact.",
    },
    {
        "failure_id": "OR6847-ST-N005",
        "failed_witness": "The first per-blob manifest replay yielded no attributable output within its wrapper window.",
        "recovery": "Used one communicate-style git cat-file batch and compact exact parity output.",
        "recurrence_guard": "Batch immutable Git blobs with input and output handled by one completed subprocess.",
    },
    {
        "failure_id": "OR6847-ST-N006",
        "failed_witness": "The first route-projection validator call guessed --projection instead of the installed --state argument.",
        "recovery": "Read the installed help and reran only the projection validator with --state.",
        "recurrence_guard": "Inspect exact installed subcommand help before composing mutable routing checks.",
    },
    {
        "failure_id": "OR6847-ST-N007",
        "failed_witness": "The first projected-assignment call repeated the unsupported --projection argument.",
        "recovery": "Applied the observed --state contract and reran only the bounded assignment lookup.",
        "recurrence_guard": "Reuse the validated installed argument contract across related subcommands.",
    },
    {
        "failure_id": "OR6847-ST-N008",
        "failed_witness": "A prior-Orin template tree lookup used a one-character-wrong commit and returned not-a-tree.",
        "recovery": "Read the exact prior Orin worktree head and used its literal owner-local template paths.",
        "recurrence_guard": "Resolve a template head from its clean literal worktree before querying the object database.",
    },
    {
        "failure_id": "OR6847-X1-N001",
        "failed_witness": "The first large title-block patch failed verification and changed no file.",
        "recovery": "Applied sixty exact one-line title replacements through the same patch surface.",
        "recurrence_guard": "Use small exact hunks for long independently replaceable list items.",
    },
    {
        "failure_id": "OR6847-X1-N002",
        "failed_witness": "The first official-source patch retained one stale checked-date context and failed verification without a write.",
        "recovery": "Inspected the exact materialized lines and changed only the corrected current source rows.",
        "recurrence_guard": "Re-read mechanically transformed context before applying a multi-entry semantic patch.",
    },
    {
        "failure_id": "OR6847-X1-N003",
        "failed_witness": "The first complete reachable-proposal audit found no exact collision but quarantined two titles at or above the 0.78 token-Jaccard threshold.",
        "recovery": "Projected only the two exact neighbour pairs and refined their semantic surfaces without changing hypotheses dispositions gates or threshold.",
        "recurrence_guard": "Run the complete reachable audit before freeze and preserve every quarantined first attempt.",
    },
    {
        "failure_id": "OR6847-X1-N004",
        "failed_witness": "The first bounded neighbour projection reached its result but the host console could not encode a Māori macron under cp1252.",
        "recovery": "Repeated only the projection with ASCII-safe JSON escaping.",
        "recurrence_guard": "Use explicit UTF-8 or ASCII-safe escaping for bounded Windows console projections.",
    },
    {
        "failure_id": "OR6847-X1-N005",
        "failed_witness": "The first post-build stale-label review found current schema identifiers still carrying the prior v684.v7 dotted version.",
        "recovery": "Changed only current owner schema identifiers to v684.v7 and rebuilt the planning packet.",
        "recurrence_guard": "Search hyphenated underscored and dotted phase labels before staging a derived template.",
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
        "schema": "ghc.family.proposal-chain-audit.v684.v7.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7",
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
            "claim": "bounded all-reachable-exact-source proposal audit; no universal 11030-row proof",
        },
    }
    return audit, selected_reviews[:60]


def make_portfolio() -> dict[str, Any]:
    def records(prefix: str, count: int, lane: str, credit: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": f"OR6847-{prefix}-{index:03d}",
                "lane": lane,
                "planned_action": (
                    f"Bounded owner-local {lane.replace('_', ' ')} record {index:03d} linked to "
                    f"OR6847-N{((index - 1) % 60) + 1:03d}."
                ),
                "credit_boundary": credit,
                "x1_state": "preregistered_not_executed",
            }
            for index in range(1, count + 1)
        ]

    return {
        "schema": "ghc.family.portfolio-freeze.v684.v7.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7",
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly_synthetic_herbarium_accession_and_object_label_referent_registrar",
            "wholly_synthetic_botanical_label_transcription_and_georeference_vacancy_reviewer",
            "wholly_synthetic_collection_location_accessibility_privacy_workload_and_handover_steward",
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
                "skill_id": f"OR6847-SK-{index:02d}",
                "name": f"ghc-family-herbarium-provenance-{index:02d}",
                "x1_state": "planned_not_built",
                "global_install": False,
            }
            for index in range(1, 21)
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"OR6847-RN-{index:02d}",
                "name": f"ghc_family_herbarium_record_runner_{index:02d}.py",
                "x1_state": "planned_not_built",
            }
            for index in range(1, 11)
        ],
        "successor_skill_ideas": [
            {
                "idea_id": f"OR6847-SUCC-SK-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_runner_ideas": [
            {
                "idea_id": f"OR6847-SUCC-RN-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_practice_recommendation": (
            "one wholly synthetic community-archive oral-history accession restriction and accessible handover lens"
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
        "schema": "ghc.family.privacy-scan.v684.v7.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7",
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
            "scripts/build_ghc_family_orin_thale_v684_v7_x1.py",
            "tests/test_ghc_family_orin_thale_v684_v7_x1.py",
        }
        current = {
            line[3:].replace("\\", "/")
            for line in git("status", "--porcelain=v1").splitlines()
            if len(line) >= 4
        }
        unexpected = {
            path
            for path in current
            if path not in allowed and not path.startswith("docs/orin-thale/v684-v7/")
        }
        if unexpected:
            raise RuntimeError(f"unexpected pre-build worktree state: {sorted(unexpected)}")

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
            "schema": "ghc.family.activation-intake.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "source": SOURCE,
            "delivery_state": "LIVE_ACTIVATION_ACKNOWLEDGED_EXTERNALLY",
            "prepared_repository_candidate_is_delivery": False,
            "work_solo": True,
            "subagents_or_delegation": False,
            "successor_precontact": False,
            "identity_language_is_evidence": False,
        },
        X1 / "approval-hold-register.json": {
            "schema": "ghc.family.approval-holds.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "exact_approval_count": 20,
            "blocked_count": 10,
            "executed_count": 0,
            "rule": "Broad authorization does not supply a missing exact target, system, cost, rollback, affected-party consent, legal authority, cultural authority, or Māori authority.",
        },
        X1 / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "owner_records": portfolio["owner_clean_fix_refine"],
            "successor_records": portfolio["successor_clean_fix_refine"],
            "x1_execution_count": 0,
        },
        X1 / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v684.v7.x1",
            "owner": "Orin Thale",
            "pronouns": "they/them optional relational working language",
            "role": "specimen-record minimum-disclosure and reversible-correction cartographer",
            "hope": "make every synthetic specimen referent, disclosure decision, correction, and authority vacancy easy to inspect, challenge, and reverse",
            "evidence_of_consciousness_personhood_continuity_agency_or_authority": False,
            "corrigibility": "Hamish may pause rename redirect narrow or stop the route.",
        },
        X1 / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "review_count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
        X1 / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
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
            "schema": "ghc.family.new-proposal-freeze.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "source": SOURCE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "proposals": rows,
            "x2_outcomes_present": False,
        },
        X1 / "official-primary-source-ledger.json": {
            "schema": "ghc.family.official-primary-sources.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "checked_at_utc": now,
            "entries": OFFICIAL_SOURCES,
            "web_checks": len(OFFICIAL_SOURCES),
            "network_data_queries": 0,
            "real_data_rows": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        X1 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
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
            "schema": "ghc.family.route-plan.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "route_state": "TERMINAL_GATE_HELD",
            "prospective_successor_title": "Liora Venn",
            "prospective_successor_phase": "v684-v8",
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
            "schema": "ghc.family.skill-runner-plan.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "skills": portfolio["owner_skill_ideas"],
            "runners": portfolio["owner_runner_ideas"],
            "successor_skill_ideas": portfolio["successor_skill_ideas"],
            "successor_runner_ideas": portfolio["successor_runner_ideas"],
            "built_in_x1": 0,
            "smoke_used_in_x1": 0,
            "global_installs": 0,
        },
        X1 / "source-verification.json": {
            "schema": "ghc.family.source-verification.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_tracking": source_tracking,
            "source_fresh_live": live_source,
            "source_tracking_equal": source_tracking == SOURCE,
            "source_fresh_live_equal": live_source == SOURCE,
            "caelen_source": "9a2fcdc6021dcc8226ff7150b990bfe429671680",
            "caelen_x1": "ab50360d737177ab1ebe4564b348a88b540c9ed4",
            "caelen_evidence": "ca4ac41d8984e8fcec58982bfd6507030dcd1480",
            "caelen_first_final": "af3cf6bdf1a5d890ccf417e6f6c9c203c0a7f563",
            "caelen_second_final": "93f1ead9b0d28baa93870c2b4fb67140055014c0",
            "caelen_final": SOURCE,
            "caelen_phase_commits": 5,
            "caelen_merges": 0,
            "caelen_canonical_replayed": False,
        },
        X1 / "threat-model.json": {
            "schema": "ghc.family.threat-model.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "assets": [
                "synthetic specimen-record and transcription lineage",
                "retained correction and failure evidence",
                "privacy and minimum-disclosure boundaries",
                "authority and affected-party gates",
            ],
            "threats": [
                "stale or colliding specimen label and catalogue identity",
                "transcription correction or location change without a valid referent",
                "authority promotion from structural validation",
                "sensitive location or private route leakage",
                "accessibility structure mistaken for conformance",
                "real collection custody access or conservation action inferred from zero-row fixtures",
            ],
            "controls": [
                "immutable source and x1",
                "five rejecting mutations per proposal",
                "normalized-LF manifests",
                "five-class privacy scan",
                "exact gate noncompensation",
                "zero network and zero real rows",
            ],
            "residual_risk": "All real collection, conservation, custody, access, affected-party, privacy-complete, accessibility-complete, legal, cultural, Māori-authority, and work-release activity remains external.",
        },
        X1 / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
            "workload_controls": ["pause", "resume", "stop", "bounded retry", "handover"],
            "self_report_is_authority_evidence": False,
            "identity_continuity_claimed": False,
            "user_control_preserved": True,
        },
        X1 / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v684.v7.x1",
            "owner": "Orin Thale",
            "phase": "v684-v7",
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

    overview = f"""# Orin Thale v684-v7 planning-only x1

This immutable planning freeze begins from exact Caelen privacy-corrected final {SOURCE}. It preregisters sixty genuinely new Orin proposals after a bounded all-reachable exact-source semantic-neighbour audit and preserves sixty inherited reviews at zero novelty and completion credit. The declared chain advances from 11,030 to 11,090 rows. No universal claim is made about future or unreachable wording.

The primary pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. The three wholly synthetic learning lenses are herbarium accession and object-label referent registration; botanical label transcription and georeference-vacancy review; and collection-location, accessibility, privacy, workload, and handover stewardship.

The x1 portfolio freezes 120 safe-now items, 80 owner candidates, 20 successor candidate seeds, 20 exact-approval holds, 10 blocked holds, 20 owner skill plans, 10 owner runner plans, 100 owner CLEAN/FIX/REFINE records, and 30 successor CLEAN/FIX/REFINE seeds. None is executed in x1.

Expected dispositions are 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. They are expectations only. No observed x2 outcome, skill build, runner build, real specimen record, external write, or completion claim appears in this freeze.

Current TDWG Darwin Core, Latimer Core, Audiovisual Core and standards pages, W3C PROV-O and WCAG 2.2, RFC 3339 and RFC 8785, JSON Schema 2020-12, the New Zealand Privacy Commissioner privacy-principles and IPP 3A pages, and Te Mana Raraunga principles supply vocabulary and refusal conditions only. Citations are not observations, endorsements, certificates, legal conclusions, affected-party decisions, cultural ratification, or authority grants.

Zero real people, participants, collectors, donors, determiners, institutions, collections, specimens, sheets, labels, images, coordinates, locations, measurements, treatments, custody events, identity events, keys, proofs, rights decisions, external writes, or authority acts are used.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains synthetic or proxy-only without governed real arms and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, live lifecycle, interoperability, security, privacy, recovery, and trust-governance evidence. Collection custody, access, reproduction, conservation, work release, privacy remedy, legal interpretation, affected-party legitimacy, Māori wording and data governance, taonga or mātauranga treatment, and Māori authority remain exact-gated.

Names, pronouns, roles, hopes, family language, and continuity language are relational working language only. They are not evidence of consciousness, personhood, identity continuity, employment, qualification, independent agency, or authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X1 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X1 / "integrated-overview.md", Path(__file__), ROOT / "tests" / "test_ghc_family_orin_thale_v684_v7_x1.py"],
        key=rel,
    )
    if len(entry_paths) != 20:
        raise RuntimeError(f"x1 manifest entry arithmetic changed: {len(entry_paths)}")

    staged_review_path = VALIDATION / "x1-staged-review.json"
    privacy_path = VALIDATION / "x1-privacy-scan.json"
    manifest_path = VALIDATION / "x1-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_review_path, privacy_path, manifest_path], key=rel)
    staged_review = {
        "schema": "ghc.family.staged-review.v684.v7.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7",
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
        "schema": "ghc.family.normalized-lf-index-manifest.v684.v7.x1",
        "owner": "Orin Thale",
        "phase": "v684-v7",
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
