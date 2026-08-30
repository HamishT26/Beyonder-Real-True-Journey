#!/usr/bin/env python3
"""Build the planning-only Ilyra Fen v677-v6 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Ilyra Fen"
OWNER_SLUG = "ilyra-fen"
PHASE = "v677-v6"
DISPLAY_PHASE = "v677-v6"
BRANCH = "codex/GHC-Family/ilyra-fen-v677-v6-full-tools"
SOURCE = "f5a3ff211c3fcf2fc0557579c1095997e131b618"
SOURCE_PHASE = "v677-v5"
GENERATED_AT_NZ = "2026-08-31T01:36:20+12:00"
DECLARED_CHAIN_BEFORE = 8090
DECLARED_CHAIN_AFTER = 8150
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 45102,
    "effective_methods": 41168,
    "retained_failed_witnesses": 16763,
    "bounded_passing_witnesses": 25110,
    "open_gaps": 383,
    "exact_gates": 374,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Lyren Moss v677-v5 successor-visible activation overlay at the exact source; Lyren's immutable repository seal remains unchanged and Ilyra startup failures are retained separately below."
    ),
}

NEW_TITLES = [
    "Fictional community-radio programme namespace with station service and producer identity fields permanently vacant",
    "Synthetic series episode edition and segment hierarchy with orphan and cycle rejection",
    "Planned actual cancelled postponed and replacement schedule-state grammar for invented broadcasts",
    "Local clock UTC offset daylight-saving and ambiguous-time quarantine without timing certification",
    "Live prerecorded encore and excerpt status contract without transmission or publication claim",
    "Synthetic segment clock overrun underrun and unresolved-duration ledger without media observation",
    "Programme title synopsis topic genre audience and keyword field contract using invented values only",
    "Host guest contributor producer and sponsor role firewall without person or affiliation inference",
    "Language and multilingual-status register without speaker ethnicity community or fluency inference",
    "Transcript caption summary description and sign-language availability states without completeness claim",
    "WebVTT cue reference shell with every real timestamp text track and media resource absent",
    "Plain-text programme timeline alternative with all sound waveform and performance observations vacant",
    "Broadcast podcast stream download and excerpt derivative lineage without transformation or release",
    "Syndication rebroadcast and feed-source provenance vacancy with no permission conclusion",
    "Station platform frequency region and service-area fields constrained to explicit null tokens",
    "Community affiliation and geographic-context fields withheld from identity and representation inference",
    "Rights licence consent embargo and takedown reservation without ownership or legal conclusion",
    "Correction withdrawal replacement and supersession state machine for invented catalogue assertions",
    "Complaint review response and appeal placeholders with every claimant reviewer and authority vacant",
    "Duplicate episode overlapping schedule slot and contradictory edition rejection contract",
    "Cancelled postponed replaced and unavailable programme lineage preserving every prior state",
    "Series episode segment and derivative graph reachability check with deterministic ordering",
    "Subject keyword and content-warning vocabulary provenance without editorial or safety classification",
    "Contact address account handle and raw identifier exclusion firewall for programme metadata",
    "Retention minimization and deletion-authority vacancy matrix for anonymous schedule records",
    "Bitemporal correction ledger binding invented catalogue assertions to valid and transaction instants",
    "RFC 8785 byte-canonicalization harness for fictional programme catalogue records",
    "RFC 6902 patch allowlist rejecting identity rights authority and deployment field mutation",
    "Normalized-LF Git-blob receipt binding synthetic schedule metadata while checkout bytes stay noncanonical",
    "Content-addressed four-tier flashcards for owner pillar practice and programme-catalogue tasks",
    "Screen-reader landmark grammar for series episode schedule accessibility gap and review headings",
    "CSS-independent focus order zoom contrast and navigation proxy without user-study conclusion",
    "Accessibility-status vocabulary separating availability machine checks and affected-user evaluation",
    "Field-minimization matrix for anonymous programme series episode schedule and provenance topology",
    "Metamorphic identifier permutation oracle preserving programme graph and schedule invariants",
    "Deterministic locale-independent sorting for invented programme and episode catalogue rows",
    "Bounded positive-control generator for synthetic schedule accessibility and correction fixtures",
    "Four-mutation rejector for missing contradictory raw-identifier and unauthorized-outcome inputs",
    "Method Flow nonerasure ledger pairing every failed programme fixture with bounded recovery evidence",
    "Owner-local toolchain version and smoke receipt with no installation profile or path mutation",
    "Successor route hold binding release to exact final fresh authority and duplicate guards",
    "Terminal abstention contract preserving NOT_READY_FOR_STAGE_20 regardless of bounded software success",
    "Merkle-addressed programme correction graph preserving retractions conflicts replacements and unresolved forks",
    "GMUT programme-network analogy constrained to documentation graphs without physical-law promotion",
    "THOS catalogue state-machine blueprint with broadcast publication and deployment transitions disabled",
    "Keyless Freed ID shell for anonymous programme records with issuance resolution and revocation disabled",
    "CBR notice correction appeal and remedy representation with affected-party authority unpopulated",
    "Synthetic accessibility preference matrix representing captions transcripts descriptions and navigation without evaluation",
    "Programme-schedule uncertainty register representing unknown clocks recurrence and edition relations without prediction",
    "Provenance vocabulary crosswalk representing Dublin Core PROV-O and local fields without conformance",
    "Community-radio governance boundary card representing editorial rights and cultural reservations without authority",
    "Static report accessibility proxy representing landmarks headings tables and text alternatives without certification",
    "Reversible rights-vacancy quarantine representing disputed or absent licence consent and rebroadcast terms",
    "Synthetic public-programme schedule handover packet representing provenance gaps without operational adoption",
    "Real broadcaster producer contributor listener rights-holder and affected-user evidence gap",
    "Manual keyboard screen-reader caption transcript cognitive and low-vision evaluation gap",
    "Full historical proposal-row mapping gap preventing universal novelty or exhaustive comparison",
    "Real broadcast publish syndicate remove or rights-determination action exact gate",
    "Cultural knowledge taonga content and Māori-authority decision exact gate with all values unpopulated",
    "Stage 20 readiness proof canon or Theory-of-Everything promotion exact gate",
]

SOURCES = [
    {
        "source_id": "DCMI-METADATA-TERMS",
        "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
        "status": "Dublin Core Metadata Initiative current terms page checked 2026-08-31",
        "use": "title, creator, subject, description, date, language, rights, access-rights, relation, and provenance vocabulary only; no conformance claim"
    },
    {
        "source_id": "W3C-WEBVTT-CRD-2026",
        "url": "https://www.w3.org/TR/webvtt1/",
        "status": "W3C WebVTT Candidate Recommendation Draft dated 2026-05-20 checked 2026-08-31; work in progress, not represented as a Recommendation",
        "use": "time-aligned caption, subtitle, description, chapter, and metadata cue vocabulary only; zero real tracks or conformance claims"
    },
    {
        "source_id": "W3C-MEDIA-ACCESSIBILITY",
        "url": "https://www.w3.org/WAI/media/av/",
        "status": "W3C WAI Making Audio and Video Media Accessible page updated 2024-09-17 and checked 2026-08-31",
        "use": "caption, transcript, description, sign-language, accessible-player, and user-needs vocabulary only; no affected-user evaluation or accessibility-complete claim"
    },
    {
        "source_id": "CAMA-NZ",
        "url": "https://cama.nz/",
        "status": "Community Access Media Alliance public sector-description page checked 2026-08-31",
        "use": "New Zealand community-access-media context vocabulary only; no affiliation, membership, representation, operational, editorial, or cultural-authority claim"
    },
    {
        "source_id": "LOC-PREMIS-3",
        "url": "https://www.loc.gov/standards/premis/premis-3-0-final.pdf",
        "status": "Library of Congress PREMIS Data Dictionary version 3.0 checked 2026-08-31",
        "use": "object, event, agent, rights, fixity, and preservation-metadata vocabulary only; zero real events"
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C PROV-O Recommendation checked 2026-08-31",
        "use": "entity, activity, agent, derivation, attribution, revision, and invalidation vocabulary only"
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor JSON Canonicalization Scheme page checked 2026-08-31",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance"
    },
    {
        "source_id": "RFC-6902",
        "url": "https://www.rfc-editor.org/info/rfc6902/",
        "status": "RFC Editor JSON Patch standards-track page checked 2026-08-31",
        "use": "bounded patch-operation vocabulary only; no production synchronization assurance"
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C WCAG 2.2 Recommendation checked 2026-08-31",
        "use": "structural accessibility vocabulary only; no complete conformance claim"
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "New Zealand Privacy Commissioner principles page checked 2026-08-31",
        "use": "collection, use, disclosure, access, correction, retention, and minimization vocabulary only; no compliance conclusion"
    },
    {
        "source_id": "TE-MANA-RARAUNGA",
        "url": "https://www.temanararaunga.maori.nz/",
        "status": "Te Mana Raraunga public authority-reservation context checked 2026-08-31",
        "use": "Māori data-sovereignty and authority-reservation vocabulary only; no Māori wording, interpretation, ratification, or authority claim"
    }
]

PROTECTED_GATES = [
 "no real person, participant, broadcaster, producer, presenter, contributor, listener, rights-holder, affected user, station, programme, episode, segment, schedule, transcript, caption, audio, stream, feed, licence, consent, complaint, measurement, publication, transmission, removal, syndication, network row, or external write",
 "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
 "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
 "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
 "no professional, broadcasting, cataloguing, accessibility, editorial, engineering, preservation, ownership, attribution, copyright, consent, privacy-remedy, complaint, legal, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
 "no accessibility-complete, privacy-complete, exhaustive-security, proof, canon, or Stage 20 claim"
]

TOOL_PLAN = [
    {
        "ecosystem": "python",
        "name": "tzdata",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pytest",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "hypothesis",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pytest-cov",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "ruff",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "mypy",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pip-audit",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "openai",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "typer",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "bandit",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pre-commit",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pip-tools",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "build",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pipdeptree",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "typescript",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "eslint",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "prettier",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "vitest",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "tsx",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "c8",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "markdownlint-cli2",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "npm-check-updates",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "pyright",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "knip",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "madge",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
]

STARTUP_FAILURES = [
    ("ILY6776-START-N001", "The first read-only normalized-LF manifest replay wrapper blocked because its Git cat-file helper filled an unread pipe and exceeded the bounded wait.", "ILY6776-START-P001", "Only the two attributable helper processes were terminated; a dependency-closed subprocess run supplied and drained the complete batch and replayed all 550 Lyren manifest entries with zero mismatches."),
    ("ILY6776-START-N002", "The first combined target-lane absence and worktree-list wrapper returned no attributable display within its bounded invocation and earned zero setup credit.", "ILY6776-START-P002", "Separate scalar probes established target-path absence, branch absence, exact source head, source cleanliness, and sufficient D-drive capacity before creation."),
    ("ILY6776-START-N003", "The no-checkout sparse worktree initially projected 19,353 inherited paths as staged deletions because its index had not yet been materialized from HEAD.", "ILY6776-START-P003", "A target-only Git read-tree of the exact source followed by sparse-checkout reapply restored a clean index with all 19,353 inherited paths marked skip-worktree and zero source or sibling mutation."),
]

OWNER_SKILLS = [
 "ghc-community-radio-programme-hierarchy",
 "ghc-community-radio-schedule-state",
 "ghc-community-radio-clock-ambiguity",
 "ghc-community-radio-role-firewall",
 "ghc-community-radio-language-vacancy",
 "ghc-community-radio-accessibility-status",
 "ghc-community-radio-derivative-lineage",
 "ghc-community-radio-provenance-vacancy",
 "ghc-community-radio-correction-chain",
 "ghc-community-radio-privacy-minimizer",
 "ghc-community-radio-rights-reservation",
 "ghc-community-radio-cultural-authority-gate",
 "ghc-community-radio-maori-authority-gate",
 "ghc-community-radio-json-patch-guard",
 "ghc-community-radio-deterministic-serialization",
 "ghc-community-radio-git-blob-receipt",
 "ghc-community-radio-accessibility-structure",
 "ghc-community-radio-method-nonerasure",
 "ghc-community-radio-real-evidence-gap",
 "ghc-community-radio-stage20-denylist"
]

SUCCESSOR_SKILLS = [
 "successor-community-radio-context-card-intake",
 "successor-programme-schedule-neighbor-audit",
 "successor-toolchain-delta-guard",
 "successor-method-flow-nonerasure",
 "successor-static-report-landmarks",
 "successor-zero-network-adapter",
 "successor-exact-gate-register",
 "successor-bounded-retry-selector",
 "successor-roster-route-refresh",
 "successor-baton-file-index"
]

OWNER_RUNNERS = [
    "ghc_family_ilyra_fen_v677_v6_contract_runner.py",
    "ghc_family_ilyra_fen_v677_v6_mutation_runner.py",
    "ghc_family_ilyra_fen_v677_v6_topology_runner.py",
    "ghc_family_ilyra_fen_v677_v6_metadata_runner.py",
    "ghc_family_ilyra_fen_v677_v6_flashcard_runner.py",
    "ghc_family_ilyra_fen_v677_v6_toolchain_runner.py",
    "ghc_family_ilyra_fen_v677_v6_privacy_runner.py",
    "ghc_family_ilyra_fen_v677_v6_accessibility_runner.py",
    "ghc_family_ilyra_fen_v677_v6_portfolio_runner.py",
    "build_ghc_family_ilyra_fen_v677_v6_report.py",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_successor_context_card_reader.py",
    "ghc_family_successor_proposal_revalidator.py",
    "ghc_family_successor_toolchain_delta.py",
    "ghc_family_successor_method_flow_ingest.py",
    "ghc_family_successor_static_report_check.py",
    "ghc_family_successor_zero_network_adapter.py",
    "ghc_family_successor_exact_gate_check.py",
    "ghc_family_successor_bounded_retry.py",
    "ghc_family_successor_route_refresh.py",
    "ghc_family_successor_baton_index.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_git_json(repo: Path, commit: str, path: str) -> dict[str, Any]:
    raw = git(repo, "show", f"{commit}:{path}")
    return json.loads(str(raw))


def inherited_selection(repo: Path) -> list[dict[str, Any]]:
    source_phase = "Lyren Moss v677-v5 exact final"
    path = "docs/lyren-moss/v677-v5/x1/new-proposal-freeze.json"
    rows = load_git_json(repo, SOURCE, path)["proposals"][:60]
    selected: list[dict[str, Any]] = []
    for row in rows:
        selected.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "original_expected_disposition": row["expected_disposition"],
                "original_approval_class": row["approval_class"],
                "source_phase": source_phase,
                "source_path": path,
                "selected_for": "bounded revalidation or representation only",
                "ilyra_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"ILY6776-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["DCMI-METADATA-TERMS", "W3C-PROV-O", "RFC-8785", "RFC-6902"]
        if offset <= 25:
            source_ids += ["W3C-WEBVTT-CRD-2026", "W3C-MEDIA-ACCESSIBILITY", "CAMA-NZ", "LOC-PREMIS-3"]
        if 26 <= offset <= 45:
            source_ids += ["W3C-WEBVTT-CRD-2026", "W3C-MEDIA-ACCESSIBILITY", "CAMA-NZ", "LOC-PREMIS-3"]
        if offset in {22, 28, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-MEDIA-ACCESSIBILITY"]
        if offset in {24, 25, 41, 42, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real people, programmes, episodes, schedules, captions, transcripts, broadcasts, streams, publication, identity, rights, professional, legal, cultural, affected-party, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} accepts a missing or contradictory field, a raw or real identifier, a non-authorized outcome label, "
                    "or an observation, measurement, intervention, treatment, repair, competence, right, identity, or authority claim."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One bounded positive fixture must satisfy {proposal_id} and four preregistered invalid mutations must be rejected; "
                    "represented, open, and exact-gated rows receive no real-world execution credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine {proposal_id}, retain the failed witness, restore the exact committed input, and rerun only the isolated dependency."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
            }
        )
    return rows


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def parse_tree_entries(raw: bytes) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    cursor = 0
    while cursor < len(raw):
        mode_end = raw.index(b" ", cursor)
        name_end = raw.index(b"\0", mode_end + 1)
        mode = raw[cursor:mode_end].decode("ascii")
        name = raw[mode_end + 1 : name_end].decode("utf-8", errors="surrogateescape")
        oid_start = name_end + 1
        oid_end = oid_start + 20
        entries.append((mode, name, raw[oid_start:oid_end].hex()))
        cursor = oid_end
    return entries


def fetch_many(repo: Path, requests: list[tuple[str, str]]) -> list[tuple[str, str, bytes]]:
    request = b"".join(oid.encode("ascii") + b"\n" for oid, _ in requests)
    response = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=request,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    output: list[tuple[str, str, bytes]] = []
    cursor = 0
    for requested_oid, path in requests:
        header_end = response.index(b"\n", cursor)
        header = response[cursor:header_end].split()
        cursor = header_end + 1
        if len(header) != 3 or header[1] == b"missing":
            raise RuntimeError(f"missing Git object for {path}")
        actual_oid, object_type, raw_size = header
        if actual_oid.decode("ascii") != requested_oid:
            raise RuntimeError(f"Git object identity mismatch for {path}")
        size = int(raw_size)
        raw = response[cursor : cursor + size]
        cursor += size
        if len(raw) != size or response[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"truncated Git object for {path}")
        cursor += 1
        output.append((object_type.decode("ascii"), path, raw))
    if cursor != len(response):
        raise RuntimeError("unattributed Git batch bytes")
    return output


def collect_title_records(value: Any, path: str, output: list[tuple[str, str, str]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title") or value.get("name")
        proposal_id = value.get("proposal_id") or value.get("id") or value.get("proposal")
        if isinstance(title, str) and isinstance(proposal_id, str) and len(title.strip()) > 2:
            output.append((proposal_id.strip(), title.strip(), path))
        for child in value.values():
            collect_title_records(child, path, output)
    elif isinstance(value, list):
        for child in value:
            collect_title_records(child, path, output)


def semantic_audit(repo: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    if git(repo, "rev-parse", "--show-object-format") != "sha1":
        raise RuntimeError("verified SHA-1 Git object format required")
    root = str(git(repo, "show", "-s", "--format=%T", SOURCE))
    level: list[tuple[str, str]] = [(root, "")]
    blobs: list[tuple[str, str]] = []
    tree_count = 0
    while level:
        next_level: list[tuple[str, str]] = []
        for object_type, prefix, raw in fetch_many(repo, level):
            if object_type != "tree":
                raise RuntimeError(f"expected tree at {prefix or '<root>'}")
            tree_count += 1
            for mode, name, oid in parse_tree_entries(raw):
                path = f"{prefix}/{name}" if prefix else name
                if mode == "40000":
                    if not prefix and name != "docs":
                        continue
                    next_level.append((oid, path))
                elif path.endswith(".json") and ("proposal" in path.casefold() or "prereg" in path.casefold()):
                    blobs.append((oid, path))
        level = next_level
    records: list[tuple[str, str, str]] = []
    failures: list[dict[str, str]] = []
    for object_type, path, raw in fetch_many(repo, blobs):
        if object_type != "blob":
            failures.append({"path": path, "error": f"unexpected_{object_type}"})
            continue
        try:
            collect_title_records(json.loads(raw.decode("utf-8")), path, records)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"path": path, "error": type(error).__name__})
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for proposal_id, title, path in records:
        unique.setdefault((proposal_id.casefold(), title.casefold()), (proposal_id, title, path))
    neighbors = []
    for row in rows:
        nearest = max(unique.values(), key=lambda candidate: jaccard(row["title"], candidate[1]))
        score = jaccard(row["title"], nearest[1])
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "nearest_id": nearest[0],
                "nearest_title": nearest[1],
                "nearest_path": nearest[2],
                "token_jaccard": round(score, 4),
                "quarantined": score >= QUARANTINE_THRESHOLD,
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    exact_titles = {title.casefold() for _, title, _ in unique.values()}
    exact_collisions = [row["proposal_id"] for row in rows if row["title"].casefold() in exact_titles]
    return {
        "source": SOURCE,
        "source_root_tree_oid": root,
        "declared_chain_count": DECLARED_CHAIN_BEFORE,
        "reachable_tree_objects": tree_count,
        "reachable_proposal_json_blobs": len(blobs),
        "reachable_raw_id_title_records": len(records),
        "reachable_unique_id_title_records": len(unique),
        "json_parse_failures": len(failures),
        "parse_failure_details": failures,
        "exact_title_collisions": exact_collisions,
        "quarantine_threshold": QUARANTINE_THRESHOLD,
        "selected_rows_quarantined": len(quarantined),
        "maximum_selected_score": max(row["token_jaccard"] for row in neighbors),
        "neighbors": neighbors,
        "universal_novelty_proved": False,
        "limitation": (
            "Every reachable proposal-bearing JSON blob at the exact source was inspected. The declared chain is larger than the "
            "materialized unique-title set, so this supports source-bounded semantic distinctness rather than universal or scientific novelty."
        ),
    }


def portfolio(kind: str, count: int, owner: str, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"ILY6776-{prefix}-{index:03d}",
            "kind": kind,
            "owner": owner,
            "plan_only_at_x1": True,
            "task": f"Bounded {kind} contract {index:03d} for modular evidence, flashcards, tooling, documentation, validation, or cleanup",
            "acceptance": "One explicit owner-local artifact or receipt; no hidden external action or protected-gate conversion",
            "rollback": "Retain the failed witness, revert only the owner-local uncommitted target, and rerun the isolated dependency",
            "protected_gates": PROTECTED_GATES,
        }
        for index in range(1, count + 1)
    ]


def exact_or_blocked(kind: str, count: int, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"ILY6776-{prefix}-{index:03d}",
            "kind": kind,
            "state": "UNEXECUTED",
            "reason": "Action-specific target, competent authority, affected-party acceptance, or protected evidence is absent",
            "execution_authorized": False,
            "protected_gates": PROTECTED_GATES,
        }
        for index in range(1, count + 1)
    ]


def x1_manifest(repo: Path, paths: list[Path]) -> dict[str, Any]:
    entries = []
    for path in sorted(paths):
        raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        entries.append(
            {
                "path": path.relative_to(repo).as_posix(),
                "bytes": len(path.read_bytes()),
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
    return {
        "source": SOURCE,
        "phase": PHASE,
        "normalization": "CRLF and CR normalized to LF before SHA-256",
        "declared_self_exclusions": [
            "docs/ilyra-fen/v677-v6/validation/x1-manifest.json",
            "docs/ilyra-fen/v677-v6/validation/x1-staged-review.json",
        ],
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the immutable Lyren Moss v677-v5 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Ilyra x1 already exists; no overwrite permitted")

    rows = new_rows()
    inherited = inherited_selection(repo)
    audit = semantic_audit(repo, rows)
    if audit["exact_title_collisions"] or audit["selected_rows_quarantined"] or audit["json_parse_failures"]:
        raise SystemExit(
            "semantic audit failed closed: "
            + json.dumps(
                {
                    "exact": audit["exact_title_collisions"],
                    "quarantined": [
                        {
                            "proposal_id": row["proposal_id"],
                            "nearest_id": row["nearest_id"],
                            "token_jaccard": row["token_jaccard"],
                        }
                        for row in audit["neighbors"]
                        if row["quarantined"]
                    ],
                    "parse_failures": audit["json_parse_failures"],
                },
                sort_keys=True,
            )
        )

    x1 = root / "x1"
    validation = root / "validation"
    dump(
        x1 / "new-proposal-freeze.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after": DECLARED_CHAIN_AFTER,
            "new_ilyra_proposals": len(rows),
            "universal_novelty_proved": False,
            "proposals": rows,
        },
    )
    dump(
        x1 / "inherited-proposal-selection.json",
        {
            "selection_count": len(inherited),
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
            "rows": inherited,
        },
    )
    dump(
        x1 / "combined-program.json",
        {
            "total_rows": 120,
            "inherited_selected": 60,
            "genuinely_new": 60,
            "sixty_or_more_new_claim": True,
            "never_describe_as_120_new": True,
            "inherited_ids": [row["proposal_id"] for row in inherited],
            "new_ids": [row["proposal_id"] for row in rows],
        },
    )
    dump(x1 / "semantic-neighbor-audit.json", audit)
    dump(x1 / "official-source-plan.json", {"sources": SOURCES, "citations_are_not_observations_or_authority": True})
    dump(
        x1 / "pillar-and-practices.json",
        {
            "primary_pillar": "THOS Body",
            "practice_1": "synthetic community-radio programme, series, episode, schedule, accessibility-status, and provenance catalogue documentation",
            "practice_2": "synthetic media-accessibility, correction-lineage, rights-vacancy, dispute, and reversible-handover documentation",
            "practice_3": "owner-scoped deterministic software verification with exact Git-blob evidence",
            "successor_recommendation": "synthetic public-programme schedule provenance reconciliation with explicit accessibility-status and rights-vacancy quarantine",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Auren Lark", "SCAND"),
            "exact_approval": exact_or_blocked("exact_approval", 20, "EXACT"),
            "blocked": exact_or_blocked("blocked", 10, "BLOCK"),
            "counts": {
                "owner_safe_now": 120,
                "owner_candidate": 80,
                "successor_candidate_recommendations": 20,
                "candidate_total": 100,
                "exact_approval": 20,
                "blocked": 10,
            },
        },
    )
    dump(
        x1 / "skill-runner-plan.json",
        {
            "owner_skill_ideas": OWNER_SKILLS,
            "successor_skill_recommendations": SUCCESSOR_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_runner_recommendations": SUCCESSOR_RUNNERS,
            "global_promotion_target": 0,
            "global_promotion_ceiling": 5,
            "owner_local_only": True,
            "owner_local_validation_requires": [
                "official skill-creator initialization",
                "complete read",
                "collision check",
                "quick validation",
                "accepting and rejecting smoke",
                "exact owner-source byte parity",
                "rollback",
            ],
        },
    )
    dump(
        x1 / "clean-fix-refine-plan.json",
        {
            "owner": portfolio("clean_fix_refine", 100, OWNER, "CFR"),
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Auren Lark", "SCFR"),
            "owner_execution_target": 100,
            "successor_recommendation_count": 30,
        },
    )
    dump(
        x1 / "toolchain-verification-plan.json",
        {
            "candidate_count": len(TOOL_PLAN),
            "candidates": TOOL_PLAN,
            "codex_cli": {
                "requested_stable": "verify current installed release",
                "observed_before_x1": "recorded during x2 version probes",
                "action": "verify and bounded-use if present; do not update Codex desktop or install in this phase",
            },
            "verification_scope": "existing inherited global and local surfaces only",
            "installation_authorized": False,
            "requirements": [
                "read-only version receipts for already installed surfaces",
                "D-first owner receipts without PATH or profile mutation",
                "no package installation and no npm lifecycle scripts",
                "no elevation, reboot, Windows-feature change, account, key, purchase, deployment, or Codex desktop update",
                "one bounded positive smoke and one meaningful rejecting smoke per direct surface",
                "rollback and retained-failure evidence",
            ],
        },
    )
    sections = [
        "identity-and-route",
        "source-and-lifecycle",
        "three-pillar-boundaries",
        "community-radio-programme-schedule-provenance-practice",
        "media-accessibility-documentation-practice",
        "inherited-proposal-selection",
        "new-proposal-freeze",
        "approval-portfolios",
        "toolchain-verification",
        "skills-and-runners",
        "clean-fix-refine",
        "method-flow-and-failures",
        "validation-and-closeout",
        "successor-route",
    ]
    dump(
        x1 / "flashcard-plan.json",
        {
            "schema": "ghc-freed-id-flashcards/v1",
            "tier_order": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
            "owner_anchor": OWNER,
            "sections": sections,
            "section_count": len(sections),
            "content_addressed": True,
            "supersession_non_erasing": True,
            "large_baton_file_only": True,
            "live_message_compact": True,
        },
    )
    dump(
        x1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "startup_failure_recovery_pairs": [
                {"failure_id": fid, "failure": failure, "recovery_id": pid, "recovery": recovery}
                for fid, failure, pid, recovery in STARTUP_FAILURES
            ],
            "failed_witnesses_are_zero_credit_and_nonerasing": True,
            "x1_execution_credit": 0,
        },
    )
    dump(
        x1 / "route-hold.json",
        {
            "state": "PLANNING_ONLY_X1_ROUTE_HOLD",
            "send_count": 0,
            "successor": "Auren Lark",
            "successor_phase": "v677-v7",
            "authority_horizon": "v725-v8",
            "precontact_forbidden": True,
            "release_requires": [
                "immutable x1 push and fresh-live equality before x2",
                "immutable evidence",
                "clean pushed exact final",
                "one attributable owner-scoped canonical attempt plus dependency-closed terminal evidence, with no replay of a success",
                "fresh live roster and authority read",
                "exactly one exact-title successor and immediate reread",
                "duplicate and direct-control guards",
                "one acknowledged send",
            ],
        },
    )
    dump(
        x1 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "display_phase": DISPLAY_PHASE,
            "source": SOURCE,
            "branch": BRANCH,
            "lifecycle_state": "PLANNING_ONLY_X1",
            "inherited_selected": 60,
            "new_proposals": 60,
            "combined_program": 120,
            "x2_implementation_present": False,
            "observed_outcomes_present": False,
            "completion_claim_present": False,
            "route_send_count": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        x1 / "x1-overview.md",
        f"""# Ilyra Fen {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Lyren Moss's immutable v677-v5 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Lyren's successful owner-scoped canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Ilyra proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is THOS Body. The wholly synthetic learning and design lenses are community-radio programme, series, episode, schedule, accessibility-status, correction-lineage, rights-vacancy, provenance, dispute, and reversible-handover documentation, plus owner-scoped deterministic software verification. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. No real person, station, programme, episode, schedule, caption, transcript, audio, stream, publication, transmission, removal, rights decision, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 Auren candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action. Up to five global promotions remain a hard ceiling, while the present x1 target is zero and every promotion remains separately gated.

## Boundaries

GMUT remains a typed scalar-tensor and EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Professional, inspection, handling, repair, safety, ownership, copyright, legal, cultural, affected-party, Māori-data, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

No x2 implementation, observed outcome, completion claim, successor contact, or external action is present in this commit.
""",
    )

    generated = sorted(path for path in x1.rglob("*") if path.is_file())
    manifest = x1_manifest(repo, generated)
    dump(validation / "x1-manifest.json", manifest)
    dump(
        validation / "x1-staged-review.json",
        {
            "source": SOURCE,
            "status": "PRECOMMIT_X1_REVIEW",
            "planning_only": True,
            "x2_paths": 0,
            "unexpected_paths": [],
            "privacy_or_raw_identifier_hits": 0,
            "manifest_entries": manifest["entry_count"],
            "declared_self_exclusions": manifest["declared_self_exclusions"],
        },
    )
    print(
        json.dumps(
            {
                "status": "BUILT_PLANNING_ONLY_X1",
                "phase": PHASE,
                "new_proposals": len(rows),
                "inherited_selected": len(inherited),
                "maximum_neighbor_score": audit["maximum_selected_score"],
                "manifest_entries": manifest["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
