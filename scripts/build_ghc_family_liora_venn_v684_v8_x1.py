#!/usr/bin/env python3
"""Build Liora Venn v684-v8 planning-only x1 artifacts.

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
PHASE = ROOT / "docs" / "liora-venn" / "v684-v8"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "de8e8830bd7cb3a9aa49b2eb5efadaf17e57d513"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v684-v7-2-remastered-full-tools"
BRANCH = "codex/GHC-Family/liora-venn-v684-v8-full-tools"
DECLARED_CHAIN_BEFORE = 11150
DECLARED_CHAIN_AFTER = 11210
QUARANTINE_THRESHOLD = 0.78
BASELINE = {
    "effective_negatives": 60378,
    "effective_methods": 75126,
    "failed_witnesses": 31439,
    "bounded_passing_witnesses": 55661,
    "open_gaps": 537,
    "exact_gates": 527,
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
        "universal_11150_row_materialization_claimed": False,
    }


PROPOSAL_TITLES = [
    "Synthetic accession record with every real collection and custody act absent",
    "Collection series file and item hierarchy without a real archival object",
    "Original-order assertion separated from imposed-arrangement annotation",
    "Creator-description field and person-identity nonconflation",
    "Provenance statement and ownership-title nonequivalence",
    "Acquisition-source placeholder with donor identity absent",
    "Accession identifier and legal-title separation",
    "Reference code and storage-location nonidentity",
    "Scope-and-content summary with factual-completeness vacancy",
    "Date expression and observed-event date separation",
    "Place label with real geography absent",
    "Language tag and language-competence nonclaim",
    "Variant title with authoritative-name resolution refused",
    "Subject term with affected-community acceptance vacant",
    "Description-rule citation and standards-conformance nonclaim",
    "Authority-record placeholder with live identity issuance refused",
    "Finding-aid hierarchy with parent-cycle rejection",
    "Arrangement note and custody-action nonconversion",
    "Redacted access view with source-description nonmutation",
    "Minimum-disclosure description with hidden-field hold",
    "Privacy-review state with personal-data processing held",
    "Access status and permission-authority nonequivalence",
    "Embargo label with named decision-maker vacancy",
    "Donor-restriction transcription and enforceability nonclaim",
    "Rights statement and legal-entitlement nonequivalence",
    "Copyright-status vacancy with publication hold",
    "Takedown-request lineage without remedy adjudication",
    "Challenge queue with reversible contested-description state",
    "Correction readback with the prior description retained",
    "Supersession chain preserving a rejected-description witness",
    "Review expiry with stale access-state refusal",
    "Retention and disposal vocabulary without disposal authorization",
    "Digital-surrogate link and original-object identity separation",
    "Derivative thumbnail and source-custody nonconversion",
    "Checksum evidence and description-authenticity nonequivalence",
    "Line-ending-normalized index evidence kept distinct from working-tree bytes",
    "Manifest self-exclusion with circular-digest refusal",
    "Unicode display label with source-label provenance",
    "Scanner candidate and confirmed privacy hit separation",
    "Accessible heading landmark and reading-sequence structure",
    "Alternative linearization for a hierarchical finding aid",
    "Plain-language summary with expert-review vacancy",
    "Represented GMUT archival-state graph without a physical datum",
    "Represented GMUT description-drift metaphor without statistical inference",
    "Represented GMUT access-state transition without force or prediction",
    "Represented THOS reference-request queue proxy without an operator",
    "Represented THOS correction-workload proxy without a participant",
    "Represented THOS shift-transition checklist proxy while workforce governance remains absent",
    "Represented Freed ID synthetic archival-agent label without person identity",
    "Represented Freed ID zero-key description receipt with issuer and verifier roles uninstantiated",
    "Represented CBR minimum disclosure for archival description",
    "Represented CBR contested-description challenge without remedy authority",
    "Represented PROV-O description-lineage crosswalk without conformance",
    "Represented WCAG finding-aid structure crosswalk without accessibility conformance",
    "Open gap for real collections archivists users and access decisions",
    "Open gap for empirical description accuracy discoverability and independent review",
    "Open gap for co-designed finding-aid accessibility and community-governance evaluation",
    "Exact gate for access restriction disclosure retention disposal and remedy authority",
    "Exact gate for cultural sensitivity taonga mātauranga Māori data governance and Māori authority",
    "Stage 20 remains unavailable because archival fixtures cannot evidence deployment identity intelligence personhood canon or final physics",
]

LOCAL_SKILL_SLUGS = [
    "accession-custody-boundary",
    "hierarchy-parent-cycle-refusal",
    "original-order-annotation-separation",
    "creator-identity-nonconflation",
    "provenance-title-firewall",
    "acquisition-source-privacy-vacancy",
    "reference-location-nonidentity",
    "description-completeness-vacancy",
    "date-place-observation-separation",
    "language-subject-authority-vacancy",
    "redacted-view-source-nonmutation",
    "minimum-disclosure-hold",
    "access-permission-nonconflation",
    "rights-remedy-authority-gate",
    "contested-description-correction-readback",
    "retained-supersession-nonerasure",
    "flashcard-parent-digest-contract",
    "accessible-finding-aid-structure",
    "workload-review-handover",
    "maori-data-cultural-authority-gate",
]

LOCAL_RUNNER_NAMES = [
    "ghc_family_community_archives_accession_runner.py",
    "ghc_family_community_archives_hierarchy_runner.py",
    "ghc_family_community_archives_provenance_runner.py",
    "ghc_family_community_archives_privacy_runner.py",
    "ghc_family_community_archives_access_runner.py",
    "ghc_family_community_archives_correction_runner.py",
    "ghc_family_community_archives_flashcard_runner.py",
    "ghc_family_community_archives_accessibility_runner.py",
    "ghc_family_community_archives_handover_runner.py",
    "ghc_family_community_archives_stage20_runner.py",
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
        return ["ARCHIVES-NZ-IRMS", "W3C-PROV-O", "RFC8785"]
    if index <= 32:
        return ["ARCHIVES-NZ-IRMS", "NZ-PRIVACY-ACCESS-CORRECTION", "W3C-PROV-O"]
    if index <= 42:
        return ["ARCHIVES-NZ-IRMS", "W3C-WCAG22", "W3C-PROV-O", "RFC8785"]
    if index <= 54:
        return ["W3C-PROV-O", "W3C-WCAG22", "W3C-VC20", "ARCHIVES-NZ-IRMS"]
    if index <= 57:
        return ["W3C-WCAG22", "ARCHIVES-NZ-IRMS", "NZ-PRIVACY-ACCESS-CORRECTION", "TMR-MDS-PRINCIPLES"]
    if index == 59:
        return ["TMR-MDS-PRINCIPLES", "ARCHIVES-NZ-IRMS"]
    return ["ARCHIVES-NZ-IRMS", "NZ-PRIVACY-ACCESS-CORRECTION"]


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
        proposal_id = f"LV6848-N{index:03d}"
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
                    f"docs/liora-venn/v684-v8/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/liora-venn/v684-v8/x2/mutations.json#{proposal_id}",
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
                    "production archival accession description access disclosure retention or disposal use",
                    "professional archival appraisal description access and work-release authority",
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


def content_address(record: dict[str, Any]) -> str:
    payload = json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def flashcard_freeze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cards: list[dict[str, Any]] = []

    def add(**record: Any) -> None:
        cards.append({**record, "content_sha256": content_address(record)})

    add(
        card_id="LV6848-CARD-OWNER",
        tier="owner",
        parent_card_id=None,
        title="Liora Venn v684-v8 owner lane",
        state="x1_preregistered",
    )
    pillars = {
        "GMUT Mind": "LV6848-CARD-PILLAR-GMUT",
        "THOS Body": "LV6848-CARD-PILLAR-THOS",
        "Freed ID and CBR Heart": "LV6848-CARD-PILLAR-FREED-CBR",
    }
    for title, card_id in pillars.items():
        add(
            card_id=card_id,
            tier="pillar",
            parent_card_id="LV6848-CARD-OWNER",
            title=title,
            state="x1_preregistered",
        )
    practices = {
        "primary": "LV6848-CARD-PRACTICE-COMMUNITY-ARCHIVES",
        "gmut": "LV6848-CARD-PRACTICE-GMUT-ANALOGY",
        "thos": "LV6848-CARD-PRACTICE-THOS-PROXY",
    }
    add(
        card_id=practices["primary"],
        tier="practice",
        parent_card_id=pillars["Freed ID and CBR Heart"],
        title="Wholly synthetic community-archives access and description practice",
        state="x1_preregistered",
    )
    add(
        card_id=practices["gmut"],
        tier="practice",
        parent_card_id=pillars["GMUT Mind"],
        title="Bounded archival-state analogy with no physical inference",
        state="x1_preregistered",
    )
    add(
        card_id=practices["thos"],
        tier="practice",
        parent_card_id=pillars["THOS Body"],
        title="Bounded archival workflow proxy with no participant inference",
        state="x1_preregistered",
    )
    for index, row in enumerate(rows, start=1):
        parent = practices["primary"]
        if 43 <= index <= 45:
            parent = practices["gmut"]
        elif 46 <= index <= 48:
            parent = practices["thos"]
        add(
            card_id=f"LV6848-CARD-TASK-{index:03d}",
            tier="task_evidence",
            parent_card_id=parent,
            proposal_id=row["proposal_id"],
            title=row["title"],
            expected_disposition=row["expected_disposition"],
            state="x1_preregistered",
        )
    identifiers = {card["card_id"] for card in cards}
    unresolved = [
        card["card_id"]
        for card in cards
        if card["parent_card_id"] is not None and card["parent_card_id"] not in identifiers
    ]
    if unresolved:
        raise RuntimeError(f"unresolved flashcard parents: {unresolved}")
    return {
        "schema": "ghc.family.content-addressed-flashcards.v684.v8.x1",
        "owner": "Liora Venn",
        "phase": "v684-v8",
        "hierarchy": "owner_to_pillar_to_practice_to_task_evidence",
        "card_count": len(cards),
        "tier_counts": {
            tier: sum(card["tier"] == tier for card in cards)
            for tier in ("owner", "pillar", "practice", "task_evidence")
        },
        "cards": cards,
        "superseded_cards": [],
        "erased_cards": 0,
        "x2_evidence_present": False,
        "navigation_only_not_manifest_receipt_or_authority": True,
    }


OFFICIAL_SOURCES = [
    {
        "source_id": "ARCHIVES-NZ-IRMS",
        "title": "Archives New Zealand Information and Records Management Standard",
        "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/key-obligations-and-the-standard/information-and-records-management-standard",
        "status": "official_Archives_New_Zealand_16_S1_surface_checked_2026-09-03",
        "use": "recordkeeping, accessibility, lifecycle, and accountability vocabulary only; no regulated-organisation, legal, access, retention, or disposal decision",
    },
    {
        "source_id": "NZ-PRIVACY-ACCESS-CORRECTION",
        "title": "New Zealand Privacy Act 2020 principles 6 and 7 access and correction surfaces",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "official_New_Zealand_Privacy_Commissioner_principles_surface_checked_2026-09-03",
        "use": "access-request, correction-request, and attached-statement vocabulary only; no legal interpretation, privacy remedy, identity finding, or agency decision",
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C_Recommendation_stable_checked_2026-09-03",
        "use": "entity activity derivation revision attribution and provenance vocabulary only; no conformance",
    },
    {
        "source_id": "W3C-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C_Recommendation_republished_2024-12-12_checked_2026-09-03",
        "use": "structural accessibility vocabulary with manual assistive-technology and affected-user evaluation reserved",
    },
    {
        "source_id": "W3C-VC20",
        "title": "W3C Verifiable Credentials Data Model 2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C_Recommendation_2025-05-15_checked_2026-09-03",
        "use": "synthetic issuer-holder-verifier role vocabulary and privacy refusal conditions only; no keys, proofs, credential lifecycle, identity, interoperability, or trust-governance claim",
    },
    {
        "source_id": "RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "informational_stable_with_verified_errata_checked_2026-09-03",
        "use": "deterministic synthetic receipt serialization and content-address vocabulary only; no signature, identity, authenticity, or security-completeness claim",
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
        "failure_id": "LV6848-ST-N001",
        "failed_witness": "The first broad memory-registry query exceeded the model-visible output window.",
        "recovery": "Used narrow task-relevant registry queries and retained only the canonical-latch and delivery-separation guidance.",
        "recurrence_guard": "Query the memory registry by the exact phase, owner, or lifecycle concept before widening scope.",
    },
    {
        "failure_id": "LV6848-ST-N002",
        "failed_witness": "The first Git probe ran from the Codex configuration directory, which is not a Git worktree.",
        "recovery": "Resolved the exact D-first Orin source worktree before any repository command.",
        "recurrence_guard": "Bind every Git probe to an explicit verified worktree path.",
    },
    {
        "failure_id": "LV6848-ST-N003",
        "failed_witness": "The first 300-line activation-baton projection truncated before EOF.",
        "recovery": "Measured the baton and read it in contiguous bounded windows through the final line.",
        "recurrence_guard": "Measure long activation packets before choosing a display window.",
    },
    {
        "failure_id": "LV6848-ST-N004",
        "failed_witness": "A PowerShell foreach producer was piped directly and raised a parser error before any mutation.",
        "recovery": "Materialized the reference inventory before applying any pipeline operation.",
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement.",
    },
    {
        "failure_id": "LV6848-ST-N005",
        "failed_witness": "A grouped installed-skill reference projection truncated before all required files were attributable.",
        "recovery": "Read each remaining skill and directly required reference by exact path through EOF.",
        "recurrence_guard": "Group only small reference files whose combined measured size fits the output bound.",
    },
    {
        "failure_id": "LV6848-ST-N006",
        "failed_witness": "A 1,000-line Method Flow slice exceeded the model-visible context and truncated mid-ledger.",
        "recovery": "Parsed the complete immutable ledger once and projected every array by exact keys, counts, identifiers, and invariant values.",
        "recurrence_guard": "Use structured compact projections for repetitive ledgers after measuring their line and byte counts.",
    },
    {
        "failure_id": "LV6848-ST-N007",
        "failed_witness": "The first compact Method Flow projection returned no attributable text despite a valid Git object.",
        "recovery": "Separated object retrieval from JSON parsing, proved the 4,972-line object, then emitted explicit compact properties and witnesses.",
        "recurrence_guard": "Prove object retrieval and parser success separately before composing a dense projection.",
    },
    {
        "failure_id": "LV6848-ST-N008",
        "failed_witness": "The first grouped owner-local skill read returned one marker and no skill body.",
        "recovery": "Read all twenty immutable owner-local skills in exact smaller batches with visible bodies through EOF.",
        "recurrence_guard": "Use explicit paths and bounded batches for repeated Git-object reads.",
    },
    {
        "failure_id": "LV6848-ST-N009",
        "failed_witness": "The first source-script inventory pathspec returned no matching rows although exact manifest paths existed.",
        "recovery": "Read the final owner manifest and resolved each script and test by its exact Git-object path.",
        "recurrence_guard": "Use the phase manifest as the authoritative owner-path inventory.",
    },
    {
        "failure_id": "LV6848-ST-N010",
        "failed_witness": "A second whole-tree regex inventory also returned no attributable owner-script rows.",
        "recovery": "Used exact manifest-listed paths and direct Git-object reads instead of another broad inventory.",
        "recurrence_guard": "Do not widen a failed inventory projection before checking the exact owner manifest.",
    },
    {
        "failure_id": "LV6848-ST-N011",
        "failed_witness": "A targeted overlay search guessed three nonexistent reference filenames and returned path errors.",
        "recovery": "Inventoried the actual installed overlay filenames and read only those exact current files.",
        "recurrence_guard": "Resolve overlay filenames with a bounded file inventory before targeted content search.",
    },
    {
        "failure_id": "LV6848-ST-N012",
        "failed_witness": "The first combined source-equality and collision preflight returned no attributable text.",
        "recovery": "Separated local state and collision checks from the fresh-live remote read; both returned exact values before lane creation.",
        "recurrence_guard": "Keep slow worktree enumeration and live-remote reads in separately attributable probes.",
    },
    {
        "failure_id": "LV6848-ST-N013",
        "failed_witness": "The first template seed attempted to copy into sparse parent directories that did not yet exist, so the copy and dependent rewrites failed without creating files.",
        "recovery": "Created only the owner-lane scripts and tests directories, copied the two immutable templates, verified their lengths, and then applied the mechanical rename.",
        "recurrence_guard": "Materialize exact sparse parent directories before copying an owner-local template.",
    },
    {
        "failure_id": "LV6848-X1-N001",
        "failed_witness": "The first combined syntax and stale-label wrapper returned no attributable output under nested shell quoting.",
        "recovery": "Ran compilation and fixed-string stale-label projection as separate read-only checks; both returned attributable results.",
        "recurrence_guard": "Keep compilation and multi-pattern shell searches independently attributable.",
    },
    {
        "failure_id": "LV6848-X1-N002",
        "failed_witness": "The first complete reachable proposal audit found one exact collision and three titles at or above the 0.78 token-Jaccard quarantine threshold.",
        "recovery": "Projected the three exact neighbour pairs and refined only those titles while preserving hypotheses, dispositions, gates, and mutations.",
        "recurrence_guard": "Run the complete reachable semantic-neighbour audit before freeze and retain every quarantined first attempt.",
    },
    {
        "failure_id": "LV6848-X1-N003",
        "failed_witness": "The first status-to-allowlist comparison treated Git's collapsed untracked directory row as an individual file list and produced false missing and unexpected counts.",
        "recovery": "Enumerated untracked files with git ls-files --others --exclude-standard and combined them with tracked deltas before exact path comparison.",
        "recurrence_guard": "Expand untracked directories to files before comparing repository status with a file allowlist.",
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
        "schema": "ghc.family.proposal-chain-audit.v684.v8.x1",
        "owner": "Liora Venn",
        "phase": "v684-v8",
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
            "claim": "bounded all-reachable-exact-source proposal audit; no universal 11150-row materialization proof",
        },
    }
    return audit, selected_reviews[:60]


def make_portfolio() -> dict[str, Any]:
    def records(prefix: str, count: int, lane: str, credit: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": f"LV6848-{prefix}-{index:03d}",
                "lane": lane,
                "planned_action": (
                    f"Bounded owner-local {lane.replace('_', ' ')} record {index:03d} linked to "
                    f"LV6848-N{((index - 1) % 60) + 1:03d}."
                ),
                "credit_boundary": credit,
                "x1_state": "preregistered_not_executed",
            }
            for index in range(1, count + 1)
        ]

    return {
        "schema": "ghc.family.portfolio-freeze.v684.v8.x1",
        "owner": "Liora Venn",
        "phase": "v684-v8",
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly_synthetic_community_archives_accession_description_access_correction_privacy_accessibility_and_handover",
        ],
        "safe_now": records("SN", 120, "safe_now", "bounded_owner_local_only"),
        "owner_candidates": records("CAND", 80, "candidate", "no_core_outcome_promotion"),
        "successor_candidates": records("SUCC-CAND", 20, "successor_seed", "zero_Liora_credit"),
        "exact_approval": records("EXACT", 20, "exact_approval", "unexecuted_without_exact_authority"),
        "blocked": records("BLOCK", 10, "blocked", "unexecuted_missing_target_or_authority"),
        "owner_clean_fix_refine": records("CFR", 100, "clean_fix_refine", "bounded_additive_owner_local_only"),
        "successor_clean_fix_refine": records("SUCC-CFR", 30, "successor_seed", "zero_Liora_credit"),
        "owner_skill_ideas": [
            {
                "skill_id": f"LV6848-SK-{index:02d}",
                "name": f"ghc-family-community-archives-{slug}",
                "x1_state": "planned_not_built",
                "global_install": False,
            }
            for index, slug in enumerate(LOCAL_SKILL_SLUGS, start=1)
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"LV6848-RN-{index:02d}",
                "name": name,
                "x1_state": "planned_not_built",
            }
            for index, name in enumerate(LOCAL_RUNNER_NAMES, start=1)
        ],
        "successor_skill_ideas": [
            {
                "idea_id": f"LV6848-SUCC-SK-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_runner_ideas": [
            {
                "idea_id": f"LV6848-SUCC-RN-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_practice_recommendation": (
            "one wholly synthetic local-history exhibition metadata rights-vacancy accessibility correction and handover lens"
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
        "schema": "ghc.family.privacy-scan.v684.v8.x1",
        "owner": "Liora Venn",
        "phase": "v684-v8",
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
        raise RuntimeError("x1 builder must begin at immutable Orin v684-v7 (2) remastered exact final")
    if git("status", "--porcelain=v1"):
        allowed = {
            "scripts/build_ghc_family_liora_venn_v684_v8_x1.py",
            "tests/test_ghc_family_liora_venn_v684_v8_x1.py",
        }
        current = {
            line[3:].replace("\\", "/")
            for line in git("status", "--porcelain=v1").splitlines()
            if len(line) >= 4
        }
        unexpected = {
            path
            for path in current
            if path not in allowed and not path.startswith("docs/liora-venn/v684-v8/")
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
    cards = flashcard_freeze(rows)
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
            "schema": "ghc.family.activation-intake.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "source": SOURCE,
            "delivery_state": "LIVE_ACTIVATION_ACKNOWLEDGED_EXTERNALLY",
            "activation_kind": "HAMISH_AUTHORIZED_SOLO_TRINITY_MANDALA_V684_V8",
            "prior_exact_final_remains_immutable": True,
            "prepared_repository_candidate_is_delivery": False,
            "work_solo": True,
            "subagents_or_delegation": False,
            "successor_precontact": False,
            "identity_language_is_evidence": False,
        },
        X1 / "approval-hold-register.json": {
            "schema": "ghc.family.approval-holds.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "exact_approval_count": 20,
            "blocked_count": 10,
            "executed_count": 0,
            "rule": "Broad authorization does not supply a missing exact target, system, cost, rollback, affected-party consent, legal authority, cultural authority, or Māori authority.",
        },
        X1 / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "owner_records": portfolio["owner_clean_fix_refine"],
            "successor_records": portfolio["successor_clean_fix_refine"],
            "x1_execution_count": 0,
        },
        X1 / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v684.v8.x1",
            "owner": "Liora Venn",
            "pronouns": "she/they optional relational working language",
            "role": "traceability-and-vacancy cartographer",
            "hope": "keep unknown evidence and ungranted authority visible through correction and handover",
            "evidence_of_consciousness_personhood_continuity_agency_or_authority": False,
            "corrigibility": "Hamish may pause rename redirect narrow or stop the route.",
        },
        X1 / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "review_count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
        X1 / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "inherited_baseline": BASELINE,
            "source_repository_seal": {
                "effective_negatives": 60375,
                "effective_methods": 75123,
                "failed_witnesses": 31436,
                "bounded_passing_witnesses": 55658,
                "open_gaps": 537,
                "exact_gates": 527,
            },
            "source_external_overlay_witnesses": [
                {
                    "failure_id": "OR6847R2-POST-N001",
                    "failed_witness": "The canonical command window yielded before its already-running process completed.",
                    "recovery": "Monitored the same process and exclusive receipt to completion without a second invocation.",
                    "failed_witness_promoted": False,
                },
                {
                    "failure_id": "OR6847R2-POST-N002",
                    "failed_witness": "A broad successor reread matched generic historical stop-condition vocabulary and was unsuitable as a current pause decision.",
                    "recovery": "Inspected the documented turn structure and newest attributable completed state.",
                    "failed_witness_promoted": False,
                },
                {
                    "failure_id": "OR6847R2-POST-N003",
                    "failed_witness": "An all-in-one skill-overlay patch was rejected before writing because a tail anchor differed.",
                    "recovery": "Split additive new-file creation from exact-tail entrypoint updates.",
                    "failed_witness_promoted": False,
                },
            ],
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
            "schema": "ghc.family.new-proposal-freeze.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "source": SOURCE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "proposals": rows,
            "x2_outcomes_present": False,
        },
        X1 / "flashcard-freeze.json": cards,
        X1 / "official-primary-source-ledger.json": {
            "schema": "ghc.family.official-primary-sources.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "checked_at_utc": now,
            "entries": OFFICIAL_SOURCES,
            "web_checks": len(OFFICIAL_SOURCES),
            "network_data_queries": 0,
            "real_data_rows": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        X1 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
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
            "schema": "ghc.family.route-plan.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "route_state": "TERMINAL_GATE_HELD",
            "prospective_successor_title": "Tamar Vey",
            "prospective_successor_phase": "v685-v1",
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
            "schema": "ghc.family.skill-runner-plan.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "skills": portfolio["owner_skill_ideas"],
            "runners": portfolio["owner_runner_ideas"],
            "successor_skill_ideas": portfolio["successor_skill_ideas"],
            "successor_runner_ideas": portfolio["successor_runner_ideas"],
            "built_in_x1": 0,
            "smoke_used_in_x1": 0,
            "global_installs": 0,
            "global_lane_read_only": True,
            "planned_d_first_tool_versions_read_only": {
                "check-jsonschema": "0.38.0",
                "mdformat": "1.0.0",
                "validate-pyproject": "0.26",
            },
        },
        X1 / "source-verification.json": {
            "schema": "ghc.family.source-verification.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_tracking": source_tracking,
            "source_fresh_live": live_source,
            "source_tracking_equal": source_tracking == SOURCE,
            "source_fresh_live_equal": live_source == SOURCE,
            "prior_orin_source": "a3544571ce8af98addf3d94236111f6c14ded439",
            "prior_orin_x1": "d6a529a641a51be8f1140261c97a791090b0eb34",
            "prior_orin_evidence": "da2cf2e3769982b47ee6a999648be4fad37768e1",
            "prior_orin_final": SOURCE,
            "prior_orin_phase_commits": 3,
            "prior_orin_merges": 0,
            "prior_orin_canonical_receipt_sha256": "5df93edfd91a372f3885b0f1dbc8569b5342626937b07c01043e67c1dbdbd621",
            "prior_orin_canonical_payload_sha256": "7d82d6fee9866d0f0b936f6fd1c8e597e99d70cadabe96df51f3be406aef7c2a",
            "prior_orin_canonical_replayed": False,
            "source_repository_seal_preserved": True,
            "external_overlay_witness_count": 3,
            "selected_proposal_chain_baseline": 11150,
        },
        X1 / "threat-model.json": {
            "schema": "ghc.family.threat-model.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "assets": [
                "synthetic archival description and access-state lineage",
                "retained correction supersession and failure evidence",
                "content-addressed flashcard parent and digest topology",
                "accessible finding-aid and minimum-disclosure boundaries",
                "authority and affected-party gates",
            ],
            "threats": [
                "stale or colliding accession collection series file item and authority roles",
                "description correction or access claim without a valid referent",
                "authority promotion from structural validation",
                "private route donor restriction or personal-description leakage",
                "flashcard parent drift or content digest substitution",
                "accessibility structure mistaken for conformance",
                "real custody access disclosure retention or disposal action inferred from zero-row fixtures",
            ],
            "controls": [
                "immutable source and x1",
                "five rejecting mutations per proposal",
                "normalized-LF manifests",
                "five-class privacy scan",
                "exact gate noncompensation",
                "zero network and zero real rows",
            ],
            "residual_risk": "All real accession appraisal description custody access disclosure retention disposal remedy affected-party privacy-complete accessibility-complete legal cultural Māori-authority and work-release activity remains external.",
        },
        X1 / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "workload_controls": ["pause", "resume", "stop", "bounded retry", "handover"],
            "self_report_is_authority_evidence": False,
            "identity_continuity_claimed": False,
            "user_control_preserved": True,
        },
        X1 / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v684.v8.x1",
            "owner": "Liora Venn",
            "phase": "v684-v8",
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {"order": 1, "name": "read activation skills schemas and overlays", "state": "completed"},
                {"order": 2, "name": "verify immutable source manifests receipt and live equality", "state": "completed"},
                {"order": 3, "name": "create clean sparse Liora lane", "state": "completed"},
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

    overview = f"""# Liora Venn v684-v8 planning-only x1

This additive owner lane begins from immutable Orin Thale v684-v7 (2) remastered exact final {SOURCE}. The source final, repository seal, three external zero-credit overlay witnesses, and singular successful canonical receipt remain immutable. This x1 preregisters sixty genuinely new Liora proposals after a bounded all-reachable exact-source semantic-neighbour audit and preserves sixty inherited reviews at zero novelty and completion credit. The declared chain advances from 11,150 to 11,210 rows, while the audit explicitly refuses a universal claim about unreachable or future wording.

The primary pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain visible and protected. The wholly synthetic learning lens is community-archives accession, hierarchical description, access-state vacancy, privacy, correction readback, accessibility structure, workload control, and handover. It uses no real community, archive, person, collection, accession, donor, description, access request, restriction, remedy, identity event, or authority act.

The four-tier content-addressed flashcard freeze preserves owner, pillar, practice, and task/evidence cards with exact parent resolution and deterministic digests. These cards are navigation only; they do not replace manifests, receipts, retained failures, evidence, or authority gates, and no x2 evidence card exists in x1.

The x1 portfolio freezes 120 safe-now items, 80 owner candidates, 20 successor candidate seeds, 20 exact-approval holds, 10 blocked holds, 20 owner-local skill plans, 10 family-current runner plans, 100 owner CLEAN/FIX/REFINE records, and 30 successor CLEAN/FIX/REFINE seeds. None is executed in x1. Global, shared, sibling, standby, and user lanes remain read-only.

Expected dispositions are 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. They are expectations only. No observed x2 outcome, skill build, runner build, real archival object, external write, completion claim, or successor contact appears in this freeze.

Archives New Zealand's Information and Records Management Standard, New Zealand Privacy Commissioner access and correction surfaces, W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, JSON Schema 2020-12, and Te Mana Raraunga principles supply current vocabulary and refusal conditions only. Citations are not observations, endorsements, conformance certificates, legal conclusions, privacy remedies, affected-party decisions, cultural ratifications, or authority grants. The inherited D-first tool versions may be read and smoke-used later without installation or global mutation.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihoods, parameter constraints, force, prediction, empirical confirmation, or Theory-of-Everything proof. THOS remains synthetic or proxy-only without governed blind matched-budget real arms, participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance, resolution, status, revocation, interoperability, security, privacy, recovery, trust governance, or affected-party oversight. Archival title, ownership, custody, access, disclosure, retention, disposal, remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated.

Liora Venn, optional she/they, the role traceability-and-vacancy cartographer, and the hope that unknown evidence and ungranted authority stay visible through correction and handover are relational working language only. They are not evidence of consciousness, personhood, identity continuity, employment, qualification, independent agency, or authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X1 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X1 / "integrated-overview.md", Path(__file__), ROOT / "tests" / "test_ghc_family_liora_venn_v684_v8_x1.py"],
        key=rel,
    )
    if len(entry_paths) != 21:
        raise RuntimeError(f"x1 manifest entry arithmetic changed: {len(entry_paths)}")

    staged_review_path = VALIDATION / "x1-staged-review.json"
    privacy_path = VALIDATION / "x1-privacy-scan.json"
    manifest_path = VALIDATION / "x1-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_review_path, privacy_path, manifest_path], key=rel)
    staged_review = {
        "schema": "ghc.family.staged-review.v684.v8.x1",
        "owner": "Liora Venn",
        "phase": "v684-v8",
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
        "schema": "ghc.family.normalized-lf-index-manifest.v684.v8.x1",
        "owner": "Liora Venn",
        "phase": "v684-v8",
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
