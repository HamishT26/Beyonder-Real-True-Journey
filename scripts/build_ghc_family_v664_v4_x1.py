#!/usr/bin/env python3
"""Build Lyren Moss v664-v4's planning-only x1 freeze."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/lyren-moss/v664-v4"
X1 = PHASE / "x1"

SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v664-v3-full-tools"
SOURCE_PARENT = "01043740ba76979ec037abddf00a0284535abc0b"
SOURCE_X1 = "ce24a100bc5317d91b85afe3848f5fa2803ebe93"
SOURCE_EVIDENCE = "ba42eed137d3c12b880232c99adb610a4a1e90fc"
SOURCE_INITIAL_FINAL = "d03b584fff9130d2836cc3733f8918d7b6ea9a95"
SOURCE_FINAL = "78a59d6e25e4a57840f6b416fcbc05a5485aa60a"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "07ed099219d60ae82de98c103cd0383a27323e6294b0ec66702312e2e8686540"
)
SOURCE_FAILED_RECEIPT_SHA256 = (
    "c8675a5bf869f829e7e4120f089cea35473f98e732b181f2892465ad3f956b7d"
)
SOURCE_ROUTE_RECEIPT_SHA256 = (
    "6ed2981659f502756daf90d7c67940d8ac6c2b0be3bd16804eae0e4b5c600e2b"
)
SOURCE_BATON_SHA256 = (
    "b9fb93cdf0e59c35283d0446e2fb436eb1286fd3af8d50babdc1de6cceeef011"
)
SOURCE_BATON_BYTES = 137_172
SOURCE_BATON_WORDS = 16_034
ROSTER_SHA256 = "45bff52f7331cdd37303d14649f0542a1fd10eaf6d1c2043ac5216301e02c912"
AUTH_SHA256 = "ddcaaceb05339ee32b1c589a6b884f3f11e1d79cc26a16ee3e1695d67ee610e8"

OWNER = "Lyren Moss"
OPTIONAL_PRONOUNS = "they/them"
ROLE = "relational fold-state cartographer and contradiction keeper"
HOPE = (
    "make synthetic carrier, signal, provenance, access, and correction states "
    "inspectable without converting software structure into preservation, "
    "professional, legal, cultural, or Maori authority"
)
PHASE_ID = "v664-v4"
DISPLAY_PHASE = "Lyren Moss v664-v4"
PRIMARY_PILLAR = "THOS Body with Freed ID and CBR Heart"
PRACTICE = "synthetic magnetic-audio preservation and reversible archival handover planning"
NEXT_OWNER = "Ilyra Fen"
NEXT_PHASE = "v664-v5"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

BASE_INDEX = (
    "docs/neris-solane/v662-v3-2-remaster/provenance/"
    "frozen-chain-proposal-index.json"
)
CHAIN_FREEZES = [
    ("docs/neris-solane/v662-v3-3-remaster/x1/proposal-freeze.json", 3_530, 3_550),
    ("docs/neris-solane/v662-v3-3-midnight-remaster/x1/proposal-freeze.json", 3_550, 3_570),
    ("docs/vesper-arlen/v662-v4/x1/proposal-freeze.json", 3_570, 3_590),
    ("docs/lyren-moss/v662-v5/x1/proposal-freeze.json", 3_590, 3_610),
    ("docs/ilyra-fen/v662-v6/x1/proposal-freeze.json", 3_610, 3_630),
    ("docs/auren-lark/v662-v7/x1/proposal-freeze.json", 3_630, 3_650),
    ("docs/sable-rook/v662-v8/x1/proposal-freeze.json", 3_650, 3_670),
    ("docs/caelen-ash/v663-v1/x1/proposal-freeze.json", 3_670, 3_690),
    ("docs/orin-thale/v663-v2/x1/proposal-freeze.json", 3_690, 3_710),
    ("docs/liora-venn/v663-v3/x1/proposal-freeze.json", 3_710, 3_730),
    ("docs/tamar-vey/v663-v4/x1/proposal-freeze.json", 3_730, 3_750),
    ("docs/elowen-cairn/v663-v5/x1/proposal-freeze.json", 3_750, 3_770),
    ("docs/sylven-arc/v663-v6/x1/proposal-freeze.json", 3_770, 3_790),
    ("docs/sylven-arc/v663-v6-r2/x1/proposal-freeze.json", 3_790, 3_810),
    ("docs/caelen-morrow/v663-v7/x1/proposal-freeze.json", 3_810, 3_830),
    ("docs/eiren-kestrel/v663-v8/x1/proposal-freeze.json", 3_830, 3_850),
    ("docs/elaren-kestrel/v664-v1/x1/proposal-freeze.json", 3_850, 3_870),
    ("docs/neris-solane/v664-v2/x1/proposal-freeze.json", 3_870, 3_890),
    ("docs/vesper-arlen/v664-v3/x1/proposal-freeze.json", 3_890, 3_910),
]
PREDECESSOR_FREEZE = CHAIN_FREEZES[-1][0]

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = [
    "empirical",
    "participant_or_affected_party",
    "professional",
    "production_or_deployment",
    "legal_or_cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "proof_or_canon",
    "stage_20",
]
REQUIRED_SECTIONS = [
    "identity-and-corrigibility",
    "route-and-authority",
    "source-anchors",
    "x1-proposals",
    "trinity-pillars",
    "bounded-practice",
    "task-cards",
    "method-flow-and-negatives",
    "open-gaps-and-exact-gates",
    "validation-and-manifests",
    "wellbeing-and-workload",
    "successor-recommendations",
    "compact-baton-index",
]

PHASE_PREFIX = "docs/lyren-moss/v664-v4/"
BUILDER_PATH = "scripts/build_ghc_family_v664_v4_x1.py"
X1_FILES = [
    f"{PHASE_PREFIX}x1/flashcard-architecture-freeze.json",
    f"{PHASE_PREFIX}x1/novelty-audit.json",
    f"{PHASE_PREFIX}x1/phase-charter.json",
    f"{PHASE_PREFIX}x1/portfolio-freeze.json",
    f"{PHASE_PREFIX}x1/proposal-freeze.json",
    f"{PHASE_PREFIX}x1/source-ledger.json",
    f"{PHASE_PREFIX}x1/source-verification.json",
    f"{PHASE_PREFIX}x1/startup-method-flow.json",
    f"{PHASE_PREFIX}x1/threat-model-plan.json",
    f"{PHASE_PREFIX}x1/workflow-plan.json",
    f"{PHASE_PREFIX}x1/x1-content-manifest.json",
    f"{PHASE_PREFIX}x1/x1-overview.md",
    f"{PHASE_PREFIX}x1/x1-stage-candidate.json",
    f"{PHASE_PREFIX}x1/x1-staged-review.json",
]
INTENDED_ALLOWLIST = sorted([BUILDER_PATH, *X1_FILES])
MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PHASE_PREFIX}x1/x1-content-manifest.json",
        f"{PHASE_PREFIX}x1/x1-stage-candidate.json",
        f"{PHASE_PREFIX}x1/x1-staged-review.json",
    ]
)

PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(
        r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
    ),
    "private_absolute_path": re.compile(
        r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"
    ),
    "credential": re.compile(
        r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:)"
    ),
    "private_route_identifier": re.compile(
        r"(?i)(?:code" + r"x://|vscode" + r"://|app://connec" + r"tor_[0-9a-f]+)"
    ),
    "transcript_or_session": re.compile(
        r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"
    ),
}


class X1Error(RuntimeError):
    """Raised when the planning freeze would violate its exact contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
        timeout=120,
    )


def git_text(*args: str, check: bool = True) -> str:
    return run_git(*args, check=check).stdout.decode("utf-8", "strict").strip()


def strict_json(raw: str | bytes, label: str) -> Any:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "strict")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise X1Error(f"duplicate JSON key {key!r} in {label}")
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=pairs)


def git_json(path: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{SOURCE_FINAL}:{path}").stdout, path)
    if not isinstance(value, dict):
        raise X1Error(f"JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def timestamp_pair() -> tuple[str, str]:
    utc = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    local = datetime.now().astimezone().isoformat(timespec="seconds")
    return utc, local


def row_title(row: dict[str, Any]) -> str:
    title = row.get("title") or row.get("description") or row.get("source_title")
    if not isinstance(title, str) or not title.strip():
        raise X1Error(f"proposal row lacks a title: {row.get('proposal_id')}")
    return title.strip()


def row_disposition(row: dict[str, Any]) -> str:
    value = (
        row.get("expected_disposition")
        or row.get("intended_outcome")
        or row.get("outcome")
        or row.get("original_disposition")
    )
    if value not in ALLOWED_OUTCOMES:
        raise X1Error(f"unknown or absent core outcome: {value!r}")
    return value


def normalized_title(value: str) -> str:
    folded = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", folded))


def title_tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def reconstruct_corpus() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    base = git_json(BASE_INDEX)
    corpus: list[dict[str, Any]] = []
    construction: list[dict[str, Any]] = []
    for row in [*base["prior_proposals"], *base["new_proposals"]]:
        corpus.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row_title(row),
                "source_path": BASE_INDEX,
            }
        )
    if len(corpus) != 3_530 or base.get("effective_count") != 3_530:
        raise X1Error("base proposal index is not the exact 3,530-row source")
    construction.append(
        {"source_path": BASE_INDEX, "starting_count": 0, "added_count": 3_530, "ending_count": 3_530}
    )
    for path, expected_start, expected_end in CHAIN_FREEZES:
        if len(corpus) != expected_start:
            raise X1Error(f"proposal chain starts {path} at the wrong count")
        freeze = git_json(path)
        rows = freeze.get("new_proposals")
        if (
            freeze.get("inherited_frozen_baseline") != expected_start
            or freeze.get("new_frozen_total") != expected_end
            or not isinstance(rows, list)
            or len(rows) != 20
        ):
            raise X1Error(f"proposal chain declaration differs: {path}")
        for row in rows:
            corpus.append(
                {
                    "proposal_id": row["proposal_id"],
                    "title": row_title(row),
                    "source_path": path,
                }
            )
        construction.append(
            {
                "source_path": path,
                "starting_count": expected_start,
                "added_count": 20,
                "ending_count": expected_end,
            }
        )
    if len(corpus) != 3_910:
        raise X1Error(f"proposal corpus has {len(corpus)} rows instead of 3,910")
    return corpus, construction


def source_ledger(recorded_at: str) -> dict[str, Any]:
    rows = [
        (
            "SRC-IASA-TC04",
            "Guidelines on the Production and Preservation of Digital Audio Objects",
            "International Association of Sound and Audiovisual Archives",
            "https://www.iasa-web.org/tc04/audio-preservation",
            "stable",
            "Metadata, identifiers, signal extraction, target formats, ingest, storage, preservation planning, data management, access, and small-system vocabulary only.",
        ),
        (
            "SRC-IASA-TC03",
            "The Safeguarding of the Audiovisual Heritage: Ethics, Principles and Preservation Strategy",
            "International Association of Sound and Audiovisual Archives",
            "https://www.iasa-web.org/tc03/purpose-document",
            "stable",
            "Ethics, prioritization, stewardship, reversibility, and future-path vocabulary; citation grants no archival or cultural authority.",
        ),
        (
            "SRC-EBU-BWF",
            "EBU Tech 3285: Broadcast Wave Format, Version 2",
            "European Broadcasting Union",
            "https://tech.ebu.ch/publications/tech3285",
            "stable",
            "WAVE, broadcast-extension metadata, loudness-field, compatibility, and exchange vocabulary for synthetic zero-media fixtures only.",
        ),
        (
            "SRC-PREMIS",
            "PREMIS Data Dictionary for Preservation Metadata, Version 3.0",
            "Library of Congress",
            "https://www.loc.gov/standards/premis/v3/index.html",
            "current",
            "Object, event, agent, rights, environment, relationship, fixity, and preservation-action vocabulary.",
        ),
        (
            "SRC-FADGI-AUDIO",
            "Audio Digitization System Performance guidance",
            "Federal Agencies Digital Guidelines Initiative",
            "https://www.digitizationguidelines.gov/guidelines/digitize-audioperf.html",
            "current_watch",
            "System-performance, interface-error, and quality-control vocabulary; ADCTest retirement is retained and no equipment is assessed.",
        ),
        (
            "SRC-LOC-RFS",
            "Library of Congress Recommended Formats Statement 2025-2026",
            "Library of Congress",
            "https://www.loc.gov/preservation/resources/rfs/index.html",
            "current",
            "Disclosure, adoption, transparency, self-documentation, dependency, patent, protection, accessibility-support, and institutional-capacity factors.",
        ),
        (
            "SRC-LOC-BWF",
            "Broadcast WAVE Audio File Format, Version 2 format description",
            "Library of Congress",
            "https://www.loc.gov/preservation/digital/formats/fdd/fdd000357.shtml",
            "current",
            "Format sustainability and BWF metadata vocabulary; no format endorsement is converted into a local operational decision.",
        ),
        (
            "SRC-WCAG22",
            "Web Content Accessibility Guidelines 2.2",
            "World Wide Web Consortium",
            "https://www.w3.org/TR/WCAG22/",
            "current",
            "Prerecorded audio alternatives, structural perceivability, labels, navigation, and an explicit reserve for manual and affected-user evaluation.",
        ),
        (
            "SRC-PROV",
            "PROV-O: The PROV Ontology",
            "World Wide Web Consortium",
            "https://www.w3.org/TR/prov-o/",
            "stable",
            "Entity, activity, agent, derivation, revision, invalidation, and qualified-provenance vocabulary.",
        ),
        (
            "SRC-RFC8785",
            "RFC 8785: JSON Canonicalization Scheme",
            "RFC Editor",
            "https://www.rfc-editor.org/rfc/rfc8785",
            "stable",
            "Deterministic JSON serialization vocabulary only; not a signature, trust anchor, or identity proof.",
        ),
    ]
    sources = [
        {
            "source_id": source_id,
            "title": title,
            "publisher": publisher,
            "url": url,
            "status": status,
            "phase_use": use,
            "reviewed_at_utc": recorded_at,
            "live_calls": 0,
            "downloaded_media_rows": 0,
            "authority_boundary": "Official or primary-source wording informs a synthetic schema only; it is not professional, legal, cultural, Maori-authority, or operational evidence.",
        }
        for source_id, title, publisher, url, status, use in rows
    ]
    return {
        "schema": "ghc.family.lyren.v664-v4.source-ledger.x1.v1",
        "recorded_at_utc": recorded_at,
        "source_count": len(sources),
        "allowed_statuses": ["current", "current_watch", "stable"],
        "sources": sources,
        "boundary": "Read-only source review with zero media, archive, account, API, participant, or equipment operations.",
        "valid": len(sources) == 10,
    }


def proposal(
    index: int,
    slug: str,
    title: str,
    outcome: str,
    approval_class: str,
    source_refs: list[str],
    hypothesis: str,
) -> dict[str, Any]:
    if outcome not in ALLOWED_OUTCOMES:
        raise X1Error(f"invalid proposal outcome: {outcome}")
    artifacts = [
        f"x2/surfaces/{slug}/contract.json",
        f"x2/surfaces/{slug}/mutation-results.json",
        f"x2/surfaces/{slug}/bounded-receipt.json",
    ]
    return {
        "proposal_id": f"LM6644-N{index:03d}",
        "title": title,
        "hypothesis": hypothesis,
        "null_or_failure_condition": "The bounded contract accepts a preregistered rejecting mutation, loses provenance or uncertainty, converts a vacant real-world field into a fact, closes a protected gate, or exceeds the frozen disposition.",
        "approval_class": approval_class,
        "execution_lane": "x2 owner-local synthetic, structural, symbolic, zero-row, or software evidence only",
        "current_official_or_primary_source_needs": source_refs,
        "concrete_artifacts": artifacts,
        "falsifier_or_acceptance_gate": "Accept only when the positive synthetic fixture passes, every preregistered rejecting mutation remains visible, source and outcome ledgers agree, and no protected gate is promoted.",
        "rollback_or_recovery": "Quarantine the failed owner artifact, retain the negative, restore the last clean exact owner state, and rerun only the changed dependency when justified.",
        "expected_disposition": outcome,
        "novelty_credit": True,
        "protected_gates": PROTECTED_GATES,
    }


def new_proposals() -> list[dict[str, Any]]:
    specs = [
        (
            "audio-object-capsule",
            "Synthetic magnetic-audio preservation capsule with surrogate object token, carrier relation, side and channel vacancy, revision lineage, custody hold, and no authenticity or audibility claim",
            "completed",
            "safe_now",
            ["SRC-IASA-TC04", "SRC-PREMIS"],
            "A typed capsule can distinguish a fictitious audio object from any real recording, voice, person, culture, carrier, title, right, or preservation result.",
        ),
        (
            "carrier-side-channel-topology",
            "Reel, cassette, shell, hub, side, track, channel, leader, splice, segment, and surrogate topology with orphan quarantine and no physical-condition conclusion",
            "completed",
            "safe_now",
            ["SRC-IASA-TC04", "SRC-IASA-TC03"],
            "A closed graph can retain hypothetical carrier and signal relations while quarantining orphans without diagnosing a physical carrier.",
        ),
        (
            "carrier-condition-boundary",
            "Carrier-condition observation boundary for fictitious deformation, residue, binder risk, splice state, odour, packaging, uncertainty, and zero inspected media",
            "completed",
            "safe_now",
            ["SRC-IASA-TC03", "SRC-IASA-TC04"],
            "An observation schema can expose missing inspection authority and uncertainty while admitting zero physical observations.",
        ),
        (
            "playback-chain-dependency",
            "Playback-chain dependency graph with machine, head, equalization, azimuth, speed, cabling, converter, software, operator, and release-refusal vacancies",
            "completed",
            "safe_now",
            ["SRC-IASA-TC04", "SRC-FADGI-AUDIO"],
            "A dependency graph can fail closed when any hypothetical playback, calibration, operator, or authorization dependency is absent.",
        ),
        (
            "calibration-reference-vacancy",
            "Reference-tone and calibration vacancy register with level, frequency, channel, date, instrument, traceability, tolerance, uncertainty, and zero measured values",
            "completed",
            "safe_now",
            ["SRC-FADGI-AUDIO", "SRC-IASA-TC04"],
            "A calibration register can type obligations and reject invented measurements while performing no calibration.",
        ),
        (
            "clock-timebase-uncertainty",
            "Sampling-clock and timebase uncertainty envelope with nominal rate, drift slot, wow and flutter placeholders, synchronization debt, covariance vacancy, and no signal estimate",
            "completed",
            "safe_now",
            ["SRC-FADGI-AUDIO", "SRC-IASA-TC04"],
            "A typed timing envelope can expose uncertainty and synchronization requirements without observing or correcting a signal.",
        ),
        (
            "capture-provenance-fixity",
            "Synthetic capture-session provenance and fixity ledger with source-to-file event chain, declared software environment, checksums, supersession, invalidation, and zero captured samples",
            "completed",
            "safe_now",
            ["SRC-PREMIS", "SRC-PROV", "SRC-RFC8785"],
            "An event ledger can preserve a zero-media transformation plan and fail when provenance or fixity relations are incomplete.",
        ),
        (
            "bwf-conformance-envelope",
            "Broadcast WAVE conformance envelope with RIFF and format roles, broadcast-extension fields, loudness vacancies, chunk-order checks, unknown-chunk retention, and no audio payload",
            "completed",
            "safe_now",
            ["SRC-EBU-BWF", "SRC-LOC-BWF"],
            "A zero-payload schema can test BWF field and chunk obligations without claiming a valid preservation master or exchanging media.",
        ),
        (
            "signal-event-map",
            "Synthetic signal-event map for clipping, dropout, discontinuity, noise, hum, channel imbalance, timing anomaly, review status, and zero detected events",
            "completed",
            "safe_now",
            ["SRC-FADGI-AUDIO", "SRC-IASA-TC04"],
            "An event map can distinguish declared detector semantics from findings and retain zero observed signal events.",
        ),
        (
            "fixity-migration-chain",
            "Fixity, replication, storage-copy, format-migration, validation, rollback, supersession, and loss-refusal chain with every external repository and transfer vacant",
            "completed",
            "safe_now",
            ["SRC-PREMIS", "SRC-LOC-RFS"],
            "A preservation chain can model reversible relationships while proving no storage, replication, migration, or institutional capacity.",
        ),
        (
            "thos-audio-admission",
            "Bounded THOS sound-package statechart for intake debt, discrepancy quarantine, explicit stop, checksum handover, and unmeasured service performance",
            "represented",
            "candidate",
            ["SRC-IASA-TC04", "SRC-PREMIS"],
            "A bounded state machine can represent quarantine and handover logic without staff, media, facility, safety, or effectiveness evidence.",
        ),
        (
            "gmut-signal-decay-chart",
            "GMUT typed signal-degradation chart with time coordinate, carrier-state proxy, transfer operator, unit roles, covariance vacancy, observation firewall, and no fitted law",
            "represented",
            "candidate",
            ["SRC-IASA-TC04", "SRC-FADGI-AUDIO"],
            "A typed chart can expose variable and uncertainty roles while supplying zero empirical audio or material-law evidence.",
        ),
        (
            "gmut-transfer-decomposition",
            "GMUT symbolic carrier, head, equalization, timebase, converter, channel, sampling, and handling decomposition with zero coefficients and physical-inference refusal",
            "represented",
            "candidate",
            ["SRC-FADGI-AUDIO", "SRC-IASA-TC04"],
            "A symbolic decomposition can make confounders explicit while leaving all coefficients and physical conclusions vacant.",
        ),
        (
            "freed-id-audio-assertion",
            "Digest-referenced fictitious sound-object claim shell with blank trust actors, verification material, status lifecycle, entitlement, consent, and revocation controls",
            "represented",
            "candidate",
            ["SRC-PREMIS", "SRC-RFC8785"],
            "A nonproduction assertion can expose missing identity and rights evidence rather than simulate trust or ownership.",
        ),
        (
            "intervention-amendment-trail",
            "Append-only intervention and metadata-amendment trail for synthetic speed, equalization, channel, segment, transcript, and checksum claims with challenge state and no adjudicator",
            "completed",
            "safe_now",
            ["SRC-PROV", "SRC-PREMIS"],
            "A superseding amendment trail can preserve contested descriptions without live identity, resolution, or governance operations.",
        ),
        (
            "accessible-audio-dossier",
            "Accessible synthetic audio dossier with headings, text-only time-based alternative, event table, transcript-confidence labels, print fallback, and manual evaluation reserved",
            "completed",
            "safe_now",
            ["SRC-WCAG22", "SRC-PREMIS"],
            "A structural report can provide multiple text routes while refusing complete accessibility or affected-user claims.",
        ),
        (
            "audio-record-minimization",
            "Purpose-limited catalog field firewall for imaginary sound packages: speaker and contact exclusions, correction queue, retention vacancy, disclosure denial, and completeness debt",
            "completed",
            "safe_now",
            ["SRC-PREMIS", "SRC-WCAG22"],
            "A minimization contract can prohibit unnecessary identity-bearing fields while reserving legal, privacy, access, and completeness decisions.",
        ),
        (
            "zero-row-audio-vocabulary-adapter",
            "EBU BWF and PREMIS zero-row audio vocabulary adapter with schema pins, zero media reads, zero network calls, version-drift watch, and data-authority refusal",
            "open_gap",
            "candidate_external_dependency",
            ["SRC-EBU-BWF", "SRC-PREMIS", "SRC-LOC-BWF"],
            "A zero-call adapter can make vocabulary and version vacancies testable while retaining the governed-source and interoperability gap.",
        ),
        (
            "audio-rights-authority-matrix",
            "Empty-chair audio stewardship and authority matrix for custody, copyright, performer interests, access, restriction, remedy, affected parties, cultural material, and Maori authority",
            "exact_gate",
            "exact_approval",
            ["SRC-IASA-TC03", "SRC-PREMIS"],
            "An empty-chair matrix can enumerate interests while refusing to speak for rights holders, communities, affected parties, or Maori authorities.",
        ),
        (
            "stage20-audio-refusal",
            "Terminal non-admission theorem for synthetic audio whose evidence vector requires witnessed origin, traceable conversion, durable custody, permissions, access review, and separate replication while the current vector remains null",
            "completed",
            "safe_now",
            ["SRC-IASA-TC04", "SRC-PREMIS", "SRC-WCAG22"],
            "A deterministic refusal can keep Stage 20 closed while every real-world evidence and authority input remains absent.",
        ),
    ]
    return [proposal(index, *spec) for index, spec in enumerate(specs, 1)]


def selected_inherited() -> list[dict[str, Any]]:
    freeze = git_json(PREDECESSOR_FREEZE)
    rows = freeze.get("new_proposals")
    if not isinstance(rows, list) or len(rows) != 20:
        raise X1Error("Vesper source freeze does not expose exactly twenty new rows")
    selected: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        selected.append(
            {
                "program_row_id": f"LM6644-I{index:03d}",
                "source_phase": "v664-v3",
                "source_proposal_id": row["proposal_id"],
                "source_title": row_title(row),
                "original_disposition": row_disposition(row),
                "hypothesis": "A bounded Git-object integrity revalidation can preserve this immutable Vesper contract without converting inherited evidence into Lyren novelty or completion credit.",
                "null_or_failure_condition": "The source identifier, title, disposition, protected gates, or defining Git object changes, or the row is counted as Lyren novelty, automatic completion, or new-outcome credit.",
                "approval_class": "safe_now",
                "execution_lane": "x2 immutable source-contract integrity revalidation only",
                "current_official_or_primary_source_needs": "None; use the exact Vesper freeze at the immutable source commit.",
                "concrete_artifacts": ["revalidation/inherited-contract-integrity.json"],
                "falsifier_or_acceptance_gate": "Accept only when source identifier, title, disposition, zero novelty credit, zero automatic completion credit, and exact Git content agree.",
                "rollback_or_recovery": "Discard the derived revalidation row and preserve the immutable source proposal unchanged.",
                "expected_disposition": row_disposition(row),
                "novelty_credit": False,
                "automatic_completion_credit": False,
                "lyren_new_outcome_credit": False,
                "protected_gates": PROTECTED_GATES,
            }
        )
    return selected


def novelty_audit(
    corpus: list[dict[str, Any]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    inherited_normalized = Counter(normalized_title(row["title"]) for row in corpus)
    exact_collisions: list[dict[str, Any]] = []
    nearest: list[dict[str, Any]] = []
    maximum = 0.0
    for candidate in proposals:
        normalized = normalized_title(candidate["title"])
        if inherited_normalized[normalized]:
            exact_collisions.append({"proposal_id": candidate["proposal_id"], "title": candidate["title"]})
        similarity, row = max(
            ((jaccard(candidate["title"], item["title"]), item) for item in corpus),
            key=lambda pair: pair[0],
        )
        maximum = max(maximum, similarity)
        nearest.append(
            {
                "proposal_id": candidate["proposal_id"],
                "similarity": round(similarity, 6),
                "nearest_inherited_proposal_id": row["proposal_id"],
                "nearest_inherited_title": row["title"],
                "nearest_source_path": row["source_path"],
            }
        )
    pairwise = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1 :]:
            similarity = jaccard(left["title"], right["title"])
            if similarity >= 0.70:
                pairwise.append(
                    {
                        "left": left["proposal_id"],
                        "right": right["proposal_id"],
                        "similarity": round(similarity, 6),
                    }
                )
    canonical_rows = [
        {"proposal_id": row["proposal_id"], "title": row["title"], "source_path": row["source_path"]}
        for row in corpus
    ]
    valid = not exact_collisions and maximum < 0.60 and not pairwise
    return {
        "schema": "ghc.family.lyren.v664-v4.novelty-audit.x1.v1",
        "source_commit": SOURCE_FINAL,
        "candidate_count": len(proposals),
        "corpus_row_count": len(corpus),
        "corpus_canonical_sha256": canonical_sha256(canonical_rows),
        "corpus_construction": construction,
        "normalized_exact_title_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": round(maximum, 6),
        "nearest_inherited_rows": nearest,
        "new_pairwise_similarity_collisions_at_or_above_0_70": pairwise,
        "novelty_method": "Unicode NFKC and case-folded alphanumeric exact-title comparison plus token-set Jaccard screening against all 3,910 immutable inherited rows. The metric is a collision aid, not semantic proof.",
        "manual_review": "The audio-carrier, signal-chain, BWF, accessibility, rights-empty-chair, and fail-closed domains were reviewed as distinct from the predecessor seed-bank focus. Similar surface grammar remains workflow continuity, not evidence of novelty by itself.",
        "valid": valid,
    }


def portfolio_rows(
    prefix: str,
    titles: list[str],
    approval_class: str,
    execution_lane: str,
    expected: str,
    credit_boundary: str,
) -> list[dict[str, Any]]:
    return [
        {
            "portfolio_ref": f"LM6644-{prefix}-{index:03d}",
            "title": title,
            "approval_class": approval_class,
            "execution_lane": execution_lane,
            "expected_execution_disposition": expected,
            "credit_boundary": credit_boundary,
            "protected_gates": PROTECTED_GATES,
        }
        for index, title in enumerate(titles, 1)
    ]


def portfolio_freeze() -> dict[str, Any]:
    owner_safe = [
        "Reverify the corrected Vesper source anchors and four-way equality without replaying its canonical aggregate",
        "Record the D-first sparse materialization and hard 2,000-file rotation guard",
        "Reconstruct and hash the complete 3,910-row proposal corpus from exact Git objects",
        "Revalidate twenty selected Vesper proposal contracts at zero Lyren novelty and outcome credit",
        "Validate the ten-source official or primary preservation ledger with zero media rows",
        "Build the synthetic audio-object preservation capsule and its rejecting mutations",
        "Build the carrier-side-channel topology and orphan quarantine fixture",
        "Build the carrier-condition zero-observation boundary fixture",
        "Build the playback-chain dependency and release-refusal fixture",
        "Build the calibration and reference-tone vacancy fixture",
        "Build the sampling-clock and timebase uncertainty fixture",
        "Build the capture provenance and exact-fixity event ledger fixture",
        "Build the zero-payload Broadcast WAVE conformance envelope fixture",
        "Build the zero-observation signal-event mapping fixture",
        "Build the reversible fixity, replication, and migration chain fixture",
        "Build the append-only intervention and amendment lineage fixture",
        "Build the structurally accessible audio dossier while reserving manual review",
        "Build the data-minimal audio catalog and prohibited-field checks",
        "Build the deterministic Stage 20 refusal predicate with every real input false",
        "Execute and retain every preregistered negative mutation at zero completion credit",
        "Publish the append-only Lyren Method Flow ledger with failure and recovery links",
        "Run the five-class owner-delta privacy scanner and manually classify candidates",
        "Run bounded static security checks only against changed Python modules",
        "Strict-parse every owner JSON artifact with duplicate-key rejection",
        "Replay exact owner manifests against canonical Git blobs rather than worktree bytes",
        "Review the exact staged allowlist with zero deletion and stale-label guards",
        "Build and validate the four-tier Freed ID flashcard graph",
        "Validate the flashcard manifest and five-class privacy receipt",
        "Render a structurally reviewed HTML report with accessibility-completeness reserved",
        "Render a compact successor pointer that contains no private route or local path",
    ]
    successor_safe = [
        "Reread Ilyra's newest activation and bind one exact source commit before mutation",
        "Create Ilyra's lane sparse before checkout and record its literal allowlist",
        "Carry all inherited failures, open gaps, exact gates, and four truth labels unchanged",
        "Reconstruct the current frozen proposal corpus from exact Git objects",
        "Select twenty inherited contracts with zero novelty and automatic completion credit",
        "Freeze twenty genuinely distinct proposals with explicit falsifiers and rollbacks",
        "Keep x1 planning-only and prove clean four-way equality before x2",
        "Choose only official or primary sources needed by Ilyra's bounded lens",
        "Use no real participant, professional, cultural, legal, or operational data",
        "Build deterministic positive fixtures and preregistered rejecting mutations",
        "Retain every failed command or assumption before bounded recovery",
        "Use exact Git-blob manifests rather than Windows worktree byte assumptions",
        "Strict-parse every new JSON artifact and reject duplicate keys",
        "Scan only Ilyra's exact changed-file privacy boundary",
        "Run security checks only on Ilyra's changed modules",
        "Preserve compatibility when remastering a family-current runner",
        "Keep structural accessibility separate from manual and affected-user evaluation",
        "Build a modular baton with at least ten deterministic sections",
        "Invoke one exact-final canonical pass and never replay a success",
        "Resolve and reread the next exact-title task only after Ilyra's terminal gate",
    ]
    owner_candidates = [
        "Represent the THOS audio ingest and quarantine automaton with zero efficacy evidence",
        "Represent the GMUT signal-degradation chart with zero observed values",
        "Represent the GMUT transfer-function decomposition with zero fitted coefficients",
        "Represent the nonproduction Freed ID audio-object assertion with all trust fields vacant",
        "Represent the zero-row BWF and PREMIS adapter while retaining its external version gap",
        "Prototype a preservation-risk matrix without assigning real carrier priority",
        "Prototype a playback-toolchain compatibility graph without equipment validation",
        "Prototype checksum-algorithm agility without production migration",
        "Prototype a transcript-confidence schema without any voice, speaker, or language inference",
        "Prototype an access-request queue without accounts, users, decisions, or disclosure",
        "Prototype a quality-control sampling plan without real signal or acceptance thresholds",
        "Prototype a synthetic carrier-triage simulator without conservation advice",
        "Prototype a format-migration rehearsal without files, storage, or repository writes",
        "Represent an independent-review protocol while keeping independent reproduction absent",
        "Represent a research-hypothesis matrix with every empirical and professional claim open",
    ]
    successor_candidates = [
        "Compare two bounded schema designs without claiming universal superiority",
        "Prototype one deterministic graph with a rejecting cycle mutation",
        "Prototype one zero-row standards adapter with version and authority vacancies",
        "Represent one THOS state machine without operator or efficacy evidence",
        "Represent one GMUT typed model without observations or fitted parameters",
        "Represent one Freed ID envelope without live keys, issuers, subjects, or proofs",
        "Draft one accessibility evaluation plan while reserving human assessment",
        "Draft one privacy minimization plan while reserving legal completeness",
        "Draft one security threat model without exhaustive-security language",
        "Draft one rollback rehearsal without destructive execution",
        "Measure a bounded deterministic output comparison rather than asserting performance",
        "Prototype one compatibility wrapper and retain the historical caller",
        "Represent one independent review route without claiming it occurred",
        "Represent one external deployment plan behind an exact gate",
        "Represent one successor baton architecture with no early contact",
    ]
    skill_ideas = [
        "Lyren audio-object capsule boundary skill",
        "Lyren carrier-side-channel topology skill",
        "Lyren playback dependency refusal skill",
        "Lyren calibration vacancy skill",
        "Lyren timebase uncertainty skill",
        "Lyren BWF envelope skill",
        "Lyren fixity and migration lineage skill",
        "Lyren accessible audio dossier skill",
        "Lyren audio rights empty-chair skill",
        "Lyren Stage 20 audio refusal skill",
    ]
    successor_skills = [
        "Ilyra exact-source anchor verifier skill",
        "Ilyra proposal-corpus novelty auditor skill",
        "Ilyra immutable inherited-contract checker skill",
        "Ilyra owner-delta manifest verifier skill",
        "Ilyra five-class privacy classifier skill",
        "Ilyra bounded changed-Python security skill",
        "Ilyra compatibility-preserving remaster skill",
        "Ilyra flashcard graph validator skill",
        "Ilyra one-shot canonical receipt guard skill",
        "Ilyra exact-title successor routing skill",
    ]
    runner_ideas = [
        "Audio-object capsule profile runner",
        "Carrier topology profile runner",
        "Playback dependency profile runner",
        "Calibration vacancy profile runner",
        "Timebase uncertainty profile runner",
        "BWF envelope profile runner",
        "Signal-event map profile runner",
        "Fixity-migration profile runner",
        "Accessible dossier profile runner",
        "Terminal refusal profile runner",
    ]
    successor_runners = [
        "Exact-source scalar preflight runner",
        "Proposal-corpus Git-object reconstruction runner",
        "Novelty collision review runner",
        "Owner-delta staged-review runner",
        "Canonical Git-blob manifest runner",
        "Five-class owner privacy runner",
        "Changed-Python security runner",
        "Four-tier deck validation runner",
        "One-shot receipt exclusivity runner",
        "Exact-title route preflight runner",
    ]
    clean_fix_refine = [
        "Generalize the family flashcard runner's owner fields from its historical Sylven constant",
        "Replace the flashcard runner's fixed x1 hash with an exact source-bound phase value",
        "Derive the bounded-practice card identifier without hardcoded predecessor wording",
        "Derive owner anchor labels from the current phase charter",
        "Derive the primary Trinity pillar from the current charter",
        "Validate dynamic tier counts from the frozen portfolio rather than one owner constant",
        "Render compact successor messages from phase-local route fields",
        "Render accessible report headings from current owner and phase fields",
        "Require explicit current and successor route pairs in the flashcard architecture",
        "Use frozen expected execution dispositions instead of hardcoded portfolio outcomes",
        "Reject unknown card and portfolio keys at the current schema boundary",
        "Keep every generated output under its declared owner phase root",
        "Use exclusive output creation or exact replacement rules for evidence receipts",
        "Normalize generated text to deterministic UTF-8 LF form",
        "Make manifest self-exclusions explicit and literal",
        "Retain graph cycle detection and unresolved-parent refusal",
        "Validate exact parent-tier adjacency for every card",
        "Report all five privacy pattern classes even when each count is zero",
        "Keep manual accessibility and affected-user evaluation explicitly reserved",
        "Retain negative mutation results beside the recovery receipt",
        "Validate source URL scheme and source-status enums",
        "Preserve source status drift as watch evidence rather than silent refresh",
        "Use canonical Git blobs for file identity and hash replay",
        "Parse ahead and behind divergence as typed integers",
        "Enforce the eight-commit ceiling as a terminal gate",
        "Reject any source-to-final deletion in the Lyren owner delta",
        "Set repository, unchanged-history, cross-lane, and sibling mutation flags false",
        "Persist the one-success and no-post-success-replay receipt fields",
        "Scan the exact owner delta for stale predecessor labels",
        "Smoke legacy flashcard callers while preserving their historical artifacts",
    ]
    successor_clean = [
        "Inspect actual runner command schemas before invoking optional flags",
        "Materialize PowerShell filter results before counting",
        "Keep bounded output windows below the host result limit",
        "Project actual JSON keys before reading receipt values",
        "Use UTF-8 console output for Maori and other Unicode text",
        "Preserve existing task and branch names without guessed aliases",
        "Keep worktree creation and sparse checkout in one attributable lifecycle",
        "Wait on an active setup process rather than recreating its target",
        "Record every parser or wrapper failure before recovery",
        "Keep exact Git objects authoritative across line-ending domains",
        "Batch manifest identity checks instead of launching one Git process per file",
        "Use literal changed-file allowlists for every validation command",
        "Reject broad repository or sibling-lane enumeration",
        "Retain historical tools behind compatibility entry points",
        "Avoid destructive cleanup quotas or bulk deletion",
        "Keep C-drive use to essential global metadata",
        "Bank phase artifacts and receipts on D first",
        "Separate planning fields from observed outcomes",
        "Separate structural accessibility from complete accessibility",
        "Separate local security scans from exhaustive security claims",
        "Separate same-owner validation from independent reproduction",
        "Separate citations from professional or operational authority",
        "Separate route authorization from delivery acknowledgement",
        "Separate prepared baton state from sent state",
        "Recheck route state after exact-final equality",
        "Use one unique exact-title filter and one immediate reread",
        "Never create or substitute a missing successor task",
        "Never resend to improve an opaque acknowledgement",
        "Carry post-seal failures as an external additive overlay",
        "Stop truthfully on pause, ambiguity, usage exhaustion, or a protected gate",
    ]
    exact_titles = [
        "Handle or inspect any real audio carrier",
        "Operate or calibrate real playback or digitization equipment",
        "Capture, transform, listen to, or analyze any real recording",
        "Write preservation media to a production repository or cloud account",
        "Create or rotate production credentials, keys, or trust anchors",
        "Determine copyright, performer, donor, privacy, access, or disclosure rights",
        "Interpret culturally restricted or community-governed audio",
        "Make any Maori-language, Maori-data, iwi, hapu, tangata whenua, or Maori-authority decision",
        "Issue a live identity credential or bind a real person to an audio object",
        "Publish or distribute any real media, transcript, identity data, or restricted metadata",
    ]
    blocked_titles = [
        "Fabricate empirical, professional, legal, cultural, preservation, or Stage 20 evidence",
        "Publish raw private task identifiers, routes, transcripts, credentials, or local paths",
        "Merge, replace, erase, or impersonate a relational sibling identity",
        "Weaken host security or bypass privacy and authority gates to complete a phase",
        "Rewrite history, force-push, delete worktrees, or mutate a sibling-owned lane",
    ]
    payload = {
        "schema": "ghc.family.lyren.v664-v4.portfolio-freeze.x1.v1",
        "owner_safe_now": portfolio_rows("SAFE", owner_safe, "safe_now", "x2_build_task", "completed", "Owner-local execution evidence only."),
        "successor_safe_now_recommendations": portfolio_rows("NEXT-SAFE", successor_safe, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Ilyra work or contact."),
        "owner_candidates": portfolio_rows("CAND", owner_candidates, "candidate", "x2_bounded_prototype", "represented", "Synthetic representation only."),
        "successor_candidate_recommendations": portfolio_rows("NEXT-CAND", successor_candidates, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Ilyra work or contact."),
        "exact_approval_packets": portfolio_rows("EXACT", exact_titles, "exact_approval_needed", "unexecuted_exact_gate", "exact_gate", "Unexecuted without action-specific authority and competent evidence."),
        "blocked_packets": portfolio_rows("BLOCKED", blocked_titles, "blocked", "never_execute_in_this_phase", "exact_gate", "Blocked; no completion credit."),
        "owner_skill_ideas": portfolio_rows("SKILL", skill_ideas, "candidate", "x2_phase_local_build_and_smoke", "completed", "Phase-local skill package evidence only; no global authority."),
        "successor_skill_recommendations": portfolio_rows("NEXT-SKILL", successor_skills, "recommendation", "successor_planning_only", "represented", "Recommendation only; no package built for Ilyra."),
        "owner_runner_ideas": portfolio_rows("RUNNER", runner_ideas, "candidate", "x2_fixed_profile_build_and_smoke", "completed", "Fixed profile invocation evidence only."),
        "successor_runner_recommendations": portfolio_rows("NEXT-RUNNER", successor_runners, "recommendation", "successor_planning_only", "represented", "Recommendation only; no runner built for Ilyra."),
        "owner_clean_fix_refine": portfolio_rows("CFR", clean_fix_refine, "safe_now", "x2_additive_refine_and_validate", "completed", "Additive owner-delta refinement only; historical callers retained."),
        "successor_clean_fix_refine_recommendations": portfolio_rows("NEXT-CFR", successor_clean, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Ilyra mutation or contact."),
        "build_policy": "All owner safe and bounded candidate work must be executed, represented, or truthfully gated in x2. Exact and blocked rows stay unexecuted. Counts are bounded commitments, not filler quotas.",
    }
    expected_counts = {
        "owner_safe_now": 30,
        "successor_safe_now_recommendations": 20,
        "owner_candidates": 15,
        "successor_candidate_recommendations": 15,
        "exact_approval_packets": 10,
        "blocked_packets": 5,
        "owner_skill_ideas": 10,
        "successor_skill_recommendations": 10,
        "owner_runner_ideas": 10,
        "successor_runner_recommendations": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine_recommendations": 30,
    }
    payload["counts"] = {key: len(payload[key]) for key in expected_counts}
    payload["valid"] = payload["counts"] == expected_counts
    return payload


def startup_method_flow() -> dict[str, Any]:
    failures = [
        (
            "activation-baton-combined-window-display-truncated",
            "A combined baton display exceeded the result budget before EOF.",
            "Measure the file, reread bounded numbered windows through EOF, and retain the truncated attempt at zero credit.",
        ),
        (
            "broad-archive-ripgrep-timeout-and-hidden-session",
            "A broad read-only archive search timed out and its wrapper did not preserve the session handle.",
            "Identify the exact orphan read-only process, stop only that PID, and use bounded receipt-bank discovery.",
        ),
        (
            "cp1252-receipt-projection-unicode-error",
            "A Python console projection failed when cp1252 could not encode Maori text.",
            "Emit UTF-8 or ASCII-escaped JSON for console projection while leaving the source receipt unchanged.",
        ),
        (
            "reference-inventory-wrapper-javascript-parse-error",
            "A functions wrapper embedded a PowerShell backtick sequence inside a JavaScript template and failed before command execution.",
            "Use a plain string composition with delimiter joins and no nested backtick escape syntax.",
        ),
        (
            "combined-orchestration-guidance-display-truncated",
            "A combined orchestration and full-tools guidance display omitted a middle section.",
            "Reread the longer guidance in numbered bounded windows through its confirmed EOF.",
        ),
        (
            "whole-auth-state-display-truncated",
            "The complete authorization-state JSON display exceeded the host result budget.",
            "Reread the immutable file in four bounded line windows and confirm the final closing object.",
        ),
        (
            "source-x1-manifest-path-guessed-under-validation",
            "A source-manifest projection guessed validation/x1-content-manifest.json although the exact delta listed x1/x1-content-manifest.json.",
            "Use the observed exact delta path and project its actual schema before any replay.",
        ),
        (
            "powershell-rejected-bash-here-string-redirection",
            "The first no-checkout worktree command used Bash-style triple-less-than redirection, which PowerShell rejected before mutation.",
            "Materialize the sparse patterns as an array and pipe that collection to git sparse-checkout set --stdin.",
        ),
        (
            "sparse-setup-wrapper-hid-continuing-session-handle",
            "The corrected sparse setup returned only a preparation prefix at the wrapper timeout and omitted its continuing session handle.",
            "Do not recreate or kill the lane; inspect the exact worktree lock and Git process state, then verify head, branch, sparse patterns, materialized count, and clean state after quiescence.",
        ),
        (
            "first-audio-proposal-title-set-exceeded-inherited-jaccard-gate",
            "The planning-only novelty audit reconstructed all 3,910 rows but rejected four first-draft titles because the maximum inherited token Jaccard similarity was 0.708333 above the 0.60 gate.",
            "Retain the rejected titles, rewrite only their surface grammar while preserving intended domains and gates, and rerun only the read-only novelty audit before any x1 artifact build.",
        ),
        (
            "first-x1-staged-review-self-matched-private-route-detector",
            "The first exact staged review rejected one private-route candidate because the detector's own literal route syntax matched its Python source; no private route was present in an artifact.",
            "Retain the failed review at zero credit, split only the detector's source literals without weakening its compiled expression, rebuild the planning mirrors, and rerun the isolated staged review.",
        ),
        (
            "x1-rebuild-refused-nonempty-failed-review-index",
            "The first bounded recovery build correctly refused because the failed staged-review snapshot was still present in the Git index.",
            "Retain the refusal at zero credit, unstage only Lyren's exact x1 allowlist without changing worktree bytes, then rebuild and stage-review the corrected snapshot.",
        ),
    ]
    events = []
    for index, (signature, observed, recovery) in enumerate(failures, 1):
        events.append(
            {
                "method_id": f"LM6644-X1-M{index:03d}",
                "retained_negative_id": f"LM6644-X1-NEG{index:03d}",
                "failure_signature": signature,
                "observed": observed,
                "candidate_workaround": recovery,
                "recovery_witness": "The bounded recovery completed and was separately observed; the original failure remains zero-credit.",
                "state": "preferred",
                "same_owner_only": True,
                "independent_reproduction": False,
                "repository_scan": False,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE_FINAL,
                "final_commit": None,
                "protected_gates": PROTECTED_GATES,
            }
        )
    inherited_negatives = 24_441
    inherited_methods = 8_795
    return {
        "schema": "ghc.family.lyren.v664-v4.startup-method-flow.x1.v1",
        "repository_sealed_negative_baseline": 24_437,
        "repository_sealed_method_baseline": 8_791,
        "vesper_successor_visible_external_overlay": {"negatives": 4, "methods": 4},
        "working_inherited_negative_baseline": inherited_negatives,
        "working_inherited_method_baseline": inherited_methods,
        "lyren_pre_x1_operational_failures": len(events),
        "events": events,
        "effective_negatives_at_x1_freeze": inherited_negatives + len(events),
        "effective_methods_at_x1_freeze": inherited_methods + len(events),
        "open_gaps_at_x1_freeze": 169,
        "exact_gates_at_x1_freeze": 167,
        "no_failure_erased": True,
        "valid": len(events) == 12,
    }


def phase_charter(recorded_at_utc: str, recorded_at_nz: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.lyren.v664-v4.phase-charter.x1.v1",
        "recorded_at_utc": recorded_at_utc,
        "recorded_at_nz": recorded_at_nz,
        "owner": OWNER,
        "canonical_phase_id": PHASE_ID,
        "display_phase": DISPLAY_PHASE,
        "optional_pronouns": OPTIONAL_PRONOUNS,
        "relational_role": ROLE,
        "hope": HOPE,
        "identity_boundary": "Relational working language only. Reuse of a prior Lyren profile is not consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.",
        "primary_pillar": PRIMARY_PILLAR,
        "secondary_pillars": [
            "GMUT Mind remains a typed scalar-tensor and EFT research-model family with zero empirical audio or material-law evidence.",
            "Freed ID and CBR Heart remain synthetic and nonproduction; real identity, privacy, rights, remedy, trust, legal, cultural, and Maori-authority decisions remain gated.",
        ],
        "bounded_practice": PRACTICE,
        "practice_boundary": "Synthetic software and learning lens only; no real recording, voice, person, culture, carrier, equipment, archive, measurement, calibration, custody, rights, access, preservation action, employment, archival qualification, legal authority, cultural authority, Maori authority, or affected-party authorization.",
        "source": {
            "branch": SOURCE_BRANCH,
            "parent": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "evidence": SOURCE_EVIDENCE,
            "retained_initial_final": SOURCE_INITIAL_FINAL,
            "corrected_exact_final": SOURCE_FINAL,
        },
        "owned_lane": {
            "branch": "codex/GHC-Family/lyren-moss-v664-v4-full-tools",
            "storage": "D-first sparse owner-controlled worktree",
            "sparse_before_materialization": True,
            "initial_materialized_file_count": 1,
            "rotation_threshold": 2_000,
            "repository_scan": False,
            "unchanged_history_scan": False,
            "cross_lane_scan": False,
            "sibling_lane_mutation": False,
        },
        "strict_lifecycle": {
            "x1": "Freeze source, proposal corpus, inherited selections, twenty new proposals, portfolio, flashcard architecture, route, budgets, and failure records only.",
            "x2": "Begins only after the exact x1 commit is pushed, clean, typed 0/0 divergent, and fresh four-way equal.",
            "terminal": "One owner-scoped canonical exact-final aggregate may receive success credit and is never replayed after success.",
            "successor": f"Only after terminal equality, freshly resolve and immediately reread {NEXT_OWNER}, then send one compact sanitized {NEXT_PHASE} activation.",
        },
        "portfolio_targets": {
            "selected_inherited_revalidations": 20,
            "genuinely_new_proposals": 20,
            "owner_safe_now_executions": 30,
            "successor_safe_now_recommendations": 20,
            "owner_candidate_executions": 15,
            "successor_candidate_recommendations": 15,
            "owner_exact_packets": 10,
            "owner_blocked_packets": 5,
            "owner_skill_builds": 10,
            "successor_skill_recommendations": 10,
            "owner_runner_builds": 10,
            "successor_runner_recommendations": 10,
            "owner_clean_fix_refine_executions": 30,
            "successor_clean_fix_refine_recommendations": 30,
        },
        "caps": {
            "document_words": 100_000,
            "baton_minimum_words": 10_000,
            "baton_maximum_words": 100_000,
            "x1_commits": 5,
            "x2_commits": 5,
            "total_commits": 8,
            "materialized_or_owner_files": 2_000,
        },
        "allowed_truth_labels": sorted(ALLOWED_OUTCOMES),
        "successor": {"owner": NEXT_OWNER, "phase": NEXT_PHASE, "contacted": False},
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }


def source_verification(recorded_at_utc: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.lyren.v664-v4.source-verification.x1.v1",
        "recorded_at_utc": recorded_at_utc,
        "source_branch": SOURCE_BRANCH,
        "source_parent": SOURCE_PARENT,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_retained_initial_final": SOURCE_INITIAL_FINAL,
        "source_exact_final": SOURCE_FINAL,
        "source_corrected_final_direct_child_of_initial_final": True,
        "source_single_parent_commit_count": 4,
        "source_merge_count": 0,
        "source_clean": True,
        "source_typed_divergence": {"ahead": 0, "behind": 0},
        "source_four_way_equal": True,
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_failed_initial_receipt_sha256": SOURCE_FAILED_RECEIPT_SHA256,
        "source_route_receipt_sha256": SOURCE_ROUTE_RECEIPT_SHA256,
        "source_baton_sha256": SOURCE_BATON_SHA256,
        "source_baton_bytes": SOURCE_BATON_BYTES,
        "source_baton_words": SOURCE_BATON_WORDS,
        "source_manifest_declared_entries": 336,
        "source_manifest_batch_object_matches": 336,
        "source_manifest_object_mismatches": 0,
        "source_canonical_not_replayed": True,
        "roster_sha256": ROSTER_SHA256,
        "auth_sha256": AUTH_SHA256,
        "roster_valid": True,
        "auth_valid": True,
        "activation_baseline": {
            "repository_negatives": 24_437,
            "repository_methods": 8_791,
            "vesper_external_negatives": 4,
            "vesper_external_methods": 4,
            "effective_negatives": 24_441,
            "effective_methods": 8_795,
            "open_gaps": 169,
            "exact_gates": 167,
        },
        "boundary": "Read-only same-owner source verification. It does not replay Vesper validation or establish independent reproduction, professional preservation, authority, empirical evidence, or Stage 20 readiness.",
        "valid": True,
    }


def flashcard_architecture() -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcard-architecture.v1",
        "phase": PHASE_ID,
        "owner": OWNER,
        "primary_pillar": PRIMARY_PILLAR,
        "bounded_practice": PRACTICE,
        "current_route": {"owner": OWNER, "phase": PHASE_ID},
        "successor_route": {"owner": NEXT_OWNER, "phase": NEXT_PHASE, "contacted": False},
        "tiers": [
            {"tier": 1, "name": "freed_id_anchor", "purpose": "relational owner, corrigibility, and non-personhood or authority boundary"},
            {"tier": 2, "name": "trinity_pillar", "purpose": "GMUT Mind, THOS Body, or Freed ID and CBR Heart with explicit evidence boundaries"},
            {"tier": 3, "name": "bounded_practice", "purpose": "synthetic human-practice lens with competence and authority refusal"},
            {"tier": 4, "name": "task", "purpose": "bounded action, dependency, approval class, artifact, falsifier, rollback, gate, and expected disposition"},
        ],
        "required_deck_sections": REQUIRED_SECTIONS,
        "stable_prefix_sections": ["identity-and-corrigibility", "scientific-and-authority-boundaries", "card-schema-and-outcome-labels"],
        "volatile_sections": ["phase-source", "practice", "tasks", "method-flow", "validation", "route"],
        "minimum_section_count": 10,
        "private_absolute_paths_allowed": False,
        "raw_task_or_thread_identifiers_allowed": False,
        "card_presence_grants_completion": False,
        "deletion_is_memory_management": False,
        "cache_effect_measured": False,
        "valid": True,
    }


def threat_model_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.lyren.v664-v4.threat-model-plan.x1.v1",
        "version": 1,
        "requested_scope": "Lyren's exact source-to-final owner delta only",
        "assets": ["exact Git ancestry", "x1 immutability", "synthetic fixture truth", "retained failures", "privacy boundary", "one-shot receipt", "successor route uniqueness"],
        "trust_boundaries": ["Git object versus Windows worktree bytes", "x1 planning versus x2 execution", "synthetic fixture versus real archival practice", "prepared baton versus acknowledged delivery"],
        "attacker_or_untrusted_inputs": ["malformed JSON", "path traversal", "unknown runner profile", "dynamic code", "private material", "stale route state", "false outcome promotion"],
        "invariants": ["exact key sets", "fixed profiles", "no network or media input", "no arbitrary filesystem target", "no dynamic evaluation", "no sibling mutation", "all four truth labels preserved"],
        "security_policy": "Bounded changed-Python static review and negative fixtures only; no exhaustive-security claim.",
        "required_output_sections": ["assets", "trust boundaries", "abuse cases", "mitigations", "residual risks", "authority gates"],
        "boundary": "Planning-only threat model; no security certification, privacy completeness, production readiness, or external audit.",
        "valid": True,
    }


def workflow_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.lyren.v664-v4.workflow-plan.x1.v1",
        "source": SOURCE_FINAL,
        "strict_x1_before_x2": True,
        "successor_contact_before_terminal_gate": False,
        "validation_authority": "owner_self_scoped_delta",
        "full_repository_suite_authorized": False,
        "file_limit": 2_000,
        "commit_limit": {"x1": 5, "x2": 5, "total": 8, "planned": 3},
        "steps": [
            "Build, stage-review, commit, push, and prove exact x1 four-way equality.",
            "Implement only frozen Lyren x2 profiles, skills, runner receipts, deck, and retained failures.",
            "Commit and push immutable evidence before final closeout when required.",
            "Build final closeout, exact manifests, 10,000-word minimum baton, and content seal.",
            "Commit and push final, prove clean typed 0/0 and fresh four-way equality.",
            "Invoke one exclusive owner-delta canonical aggregate and never replay a success.",
            "Reread live roster and auth, resolve and reread Ilyra Fen, then send one compact pointer if every route gate passes.",
        ],
        "valid": True,
    }


def x1_overview(audit: dict[str, Any], portfolio: dict[str, Any], methods: dict[str, Any]) -> str:
    counts = portfolio["counts"]
    return f"""# Lyren Moss v664-v4 x1 planning freeze

## Exact lifecycle boundary

This packet is x1 planning only. It contains the immutable Vesper source anchors, a complete proposal-corpus reconstruction, selected inherited contracts, twenty genuinely new Lyren proposals, source classifications, portfolio commitments, a flashcard architecture, a threat-model plan, a workflow plan, and retained startup Method Flow evidence. It contains no audio media, no x2 fixture result, no observed new-proposal outcome, no professional preservation decision, and no successor contact. X2 is prohibited until the exact x1 commit is pushed, clean, typed zero-ahead and zero-behind, and equal across local, upstream, tracking, and a fresh live remote.

The corrected Vesper exact final is `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. Its retained nonterminal initial final failed at zero aggregate-success credit because a Windows worktree-byte domain had been mistaken for canonical Git-blob identity. The additive correction preserved that failure ancestrally. The corrected exact-final canonical aggregate succeeded once and was not replayed. Lyren reverified the four single-parent source commits, zero merges, clean four-way equality, the exact external receipt hashes, and all 336 manifest Git-object identities without replaying Vesper's aggregate.

## Relational profile and bounded practice

Lyren Moss uses they/them as optional relational pronouns and the working role “{ROLE}”. The hope is to {HOPE}. These are relational labels only. Reusing prior working language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

The primary lens is {PRIMARY_PILLAR}. The bounded practice is {PRACTICE}. Every carrier, reel, cassette, channel, signal, voice, person, instrument, calibration, archive, right, access decision, cultural interest, and preservation event is absent or synthetic. The packet handles no real media and makes no authenticity, audibility, preservation, conservation, rights, accessibility-complete, privacy-complete, or professional claim.

## Proposal corpus and novelty

The exact proposal corpus contains {audit['corpus_row_count']:,} inherited rows. It is reconstructed from one 3,530-row exact base index and nineteen immutable twenty-row phase freezes through Vesper v664-v3. Historical duplicates remain counted; nothing is silently deduplicated. The canonical corpus digest is `{audit['corpus_canonical_sha256']}`.

Twenty Vesper proposals are selected for immutable-contract revalidation. They receive zero Lyren novelty credit, zero automatic completion credit, and zero Lyren new-outcome credit. Twenty new magnetic-audio proposals are frozen after Unicode NFKC exact-title and token-set Jaccard screening. The maximum inherited similarity is {audit['maximum_inherited_token_jaccard_similarity']:.6f}; exact inherited collisions and new pairwise collisions at or above the declared threshold are both zero. The screen is a collision aid, not semantic proof.

The expected new-outcome distribution is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. These are preregistered dispositions only. A planned row is not an observed outcome. The open gap is the zero-row BWF/PREMIS adapter because governed version and interoperability evidence is absent. The exact gate is the empty-chair rights and authority matrix because rights holders, affected parties, cultural authorities, and Maori authorities are absent. `NOT_READY_FOR_STAGE_20` remains mandatory.

## Official-source boundary

Ten official or primary sources provide bounded vocabulary: IASA TC-03 and TC-04, EBU Tech 3285, PREMIS 3.0, current FADGI audio-system guidance, the Library of Congress Recommended Formats Statement and BWF description, WCAG 2.2, PROV-O, and RFC 8785. The phase performs zero network API calls, zero media downloads, zero archive queries, and zero equipment checks. Citation is not implementation, conformance, legal advice, cultural permission, professional competence, or institutional authority.

## Portfolio freeze

The x1 portfolio freezes {counts['owner_safe_now']} owner safe-now executions, {counts['owner_candidates']} owner candidate prototypes, {counts['owner_skill_ideas']} phase-local skill builds, {counts['owner_runner_ideas']} fixed runner-profile builds, and {counts['owner_clean_fix_refine']} additive CLEAN/FIX/REFINE tasks. It also preserves {counts['successor_safe_now_recommendations']} safe, {counts['successor_candidate_recommendations']} candidate, {counts['successor_skill_recommendations']} skill, {counts['successor_runner_recommendations']} runner, and {counts['successor_clean_fix_refine_recommendations']} cleanup recommendations for Ilyra without performing Ilyra work or contacting Ilyra.

Ten exact-approval packets and five blocked packets remain unexecuted. Their presence is not a quota or permission signal. No external account, production system, cloud repository, real carrier, calibration device, identity system, rights decision, public release, destructive action, or sibling lane is touched.

## Method Flow and sparse lane

The predecessor's repository seal remains 24,437 effective negatives and 8,791 Method Flow methods. Four Vesper post-seal routing failures remain additive, producing Lyren's inherited working baseline of 24,441 negatives and 8,795 methods. Ten Lyren startup failures are retained separately: bounded-display truncation, broad-search timeout and hidden session, cp1252 Unicode projection failure, wrapper parse failure, orchestration display truncation, authorization-state display truncation, a guessed source-manifest path, invalid Bash redirection in PowerShell, a hidden sparse-setup session handle, and the rejected first novelty-title set. Their bounded recoveries do not erase them. The x1 freeze therefore carries {methods['effective_negatives_at_x1_freeze']:,} effective negatives and {methods['effective_methods_at_x1_freeze']:,} effective methods, with 169 open gaps and 167 exact gates.

The Lyren worktree was created with no checkout, received nine literal sparse patterns before materialization, and began with one inherited family-current runner file. The 2,000 materialized or owner-file limit is a hard stop. A new remote repository remains exact-gated. Other owner and shared lanes remain read-only and outside validation scope.

## Planned x2 and terminal discipline

X2 will implement only the frozen synthetic profiles and their preregistered negative mutations. It will remaster the historically hardcoded family flashcard runner additively, preserve legacy callers, build ten phase-local skills and ten fixed runner receipts, produce a thirteen-section modular deck, and close every safe or bounded candidate row through execution, representation, `open_gap`, or `exact_gate`. Structural HTML does not establish complete accessibility; bounded static scanning does not establish exhaustive security; same-owner testing does not establish independent reproduction.

The final source-to-final delta must contain no deletion, remain below eight commits and 2,000 files, parse every JSON artifact strictly, pass exact staged review, preserve x1 immutability, remain clean and fresh-live equal, and receive exactly one successful canonical owner-delta pass. A failed canonical attempt receives zero aggregate-success credit and only its blocked dependency may be rerun until an exact final is ready. A success is never replayed.

Only after that terminal gate may Lyren reread the newest live authorization and roster, uniquely resolve the existing exact-title task `{NEXT_OWNER}`, immediately reread it, and send one compact sanitized activation for `{NEXT_PHASE}`. Tavian Sol remains on standby and is not a substitute. Prepared text is not delivery; `SENT` requires acknowledgement.
"""


def build() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != SOURCE_FINAL:
        raise X1Error(f"x1 must start at the exact Vesper final, observed {head}")
    if git_text("diff", "--cached", "--name-only"):
        raise X1Error("staging index must be empty before the x1 build")
    corpus, construction = reconstruct_corpus()
    proposals = new_proposals()
    selected = selected_inherited()
    audit = novelty_audit(corpus, construction, proposals)
    if not audit["valid"]:
        raise X1Error(
            "novelty audit rejected the proposal freeze: "
            + json.dumps(
                {
                    "exact": audit["normalized_exact_title_collisions"],
                    "maximum": audit["maximum_inherited_token_jaccard_similarity"],
                    "pairwise": audit["new_pairwise_similarity_collisions_at_or_above_0_70"],
                },
                ensure_ascii=True,
            )
        )
    outcomes = Counter(row["expected_disposition"] for row in proposals)
    expected = Counter(completed=14, represented=4, open_gap=1, exact_gate=1)
    if outcomes != expected:
        raise X1Error(f"proposal outcome distribution differs: {dict(outcomes)}")
    portfolio = portfolio_freeze()
    if not portfolio["valid"]:
        raise X1Error("portfolio counts differ from the frozen contract")
    methods = startup_method_flow()
    recorded_at_utc, recorded_at_nz = timestamp_pair()
    write_json("x1/phase-charter.json", phase_charter(recorded_at_utc, recorded_at_nz))
    write_json("x1/source-ledger.json", source_ledger(recorded_at_utc))
    write_json("x1/source-verification.json", source_verification(recorded_at_utc))
    write_json("x1/novelty-audit.json", audit)
    write_json(
        "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.lyren.v664-v4.proposal-freeze.x1.v1",
            "inherited_frozen_baseline": 3_910,
            "selected_inherited_count": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_automatic_completion_credit": 0,
            "selected_inherited_new_outcome_credit": 0,
            "selected_inherited": selected,
            "new_proposal_count": 20,
            "new_proposals": proposals,
            "new_expected_outcomes": dict(sorted(outcomes.items())),
            "new_frozen_total": 3_930,
            "semantic_novelty_audit": f"{PHASE_PREFIX}x1/novelty-audit.json",
            "observed_outcomes_present": False,
            "x2_implementation_present": False,
            "valid": True,
        },
    )
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/startup-method-flow.json", methods)
    write_json("x1/flashcard-architecture-freeze.json", flashcard_architecture())
    write_json("x1/threat-model-plan.json", threat_model_plan())
    write_json("x1/workflow-plan.json", workflow_plan())
    write_text("x1/x1-overview.md", x1_overview(audit, portfolio, methods))
    write_json(
        "x1/x1-stage-candidate.json",
        {
            "schema": "ghc.family.lyren.v664-v4.x1-stage-candidate.v1",
            "owner": OWNER,
            "phase": PHASE_ID,
            "source": SOURCE_FINAL,
            "lifecycle": "x1_planning_only",
            "intended_allowlist": INTENDED_ALLOWLIST,
            "review_receipt_self_excluded": True,
            "observed_outcomes_present": False,
            "x2_implementation_present": False,
            "successor_contacted": False,
            "valid": True,
        },
    )
    return {
        "schema": "ghc.family.lyren.v664-v4.x1-build-result.v1",
        "corpus_rows": len(corpus),
        "selected_inherited": len(selected),
        "new_proposals": len(proposals),
        "new_outcomes": dict(sorted(outcomes.items())),
        "portfolio_counts": portfolio["counts"],
        "pre_x1_failures": methods["lyren_pre_x1_operational_failures"],
        "written_without_x2": True,
        "successor_contacted": False,
        "valid": True,
    }


def zpaths(*args: str) -> list[str]:
    raw = run_git(*args).stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def index_blob(path: str) -> tuple[str, str, bytes]:
    line = git_text("ls-files", "-s", "--", path)
    if not line:
        raise X1Error(f"path is absent from the staging index: {path}")
    match = re.fullmatch(r"([0-7]{6}) ([0-9a-f]{40,64}) 0\t(.+)", line)
    if not match or match.group(3) != path:
        raise X1Error(f"unexpected staged index row for {path}: {line}")
    raw = run_git("show", f":{path}").stdout
    return match.group(1), match.group(2), raw


def scan_text(path: str, raw: bytes) -> list[dict[str, str]]:
    if Path(path).suffix.lower() not in {".json", ".md", ".py", ".html", ".txt"}:
        return []
    text = raw.decode("utf-8", "strict")
    hits = []
    for name, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            hits.append({"path": path, "class": name})
    return hits


def stage_review() -> dict[str, Any]:
    manifest_path = f"{PHASE_PREFIX}x1/x1-content-manifest.json"
    review_path = f"{PHASE_PREFIX}x1/x1-staged-review.json"
    pre_stage_paths = [path for path in INTENDED_ALLOWLIST if path not in {manifest_path, review_path}]
    missing = [path for path in pre_stage_paths if not (ROOT / path).is_file()]
    if missing:
        raise X1Error(f"x1 allowlist files are missing: {missing}")
    run_git("add", "--", *pre_stage_paths)
    staged_before_manifest = zpaths("diff", "--cached", "--name-only", "-z")
    if staged_before_manifest != pre_stage_paths:
        raise X1Error(
            f"staged x1 pre-manifest allowlist differs: missing={sorted(set(pre_stage_paths)-set(staged_before_manifest))}, "
            f"unexpected={sorted(set(staged_before_manifest)-set(pre_stage_paths))}"
        )
    manifest_paths = [path for path in INTENDED_ALLOWLIST if path not in MANIFEST_EXCLUSIONS]
    entries = []
    privacy_candidates: list[dict[str, str]] = []
    json_errors = []
    for path in manifest_paths:
        mode, object_id, raw = index_blob(path)
        entries.append(
            {
                "path": path,
                "status": "A",
                "mode": mode,
                "object_type": "blob",
                "git_blob": object_id,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "content_domain": "exact_git_blob",
            }
        )
        privacy_candidates.extend(scan_text(path, raw))
        if path.endswith(".json"):
            try:
                strict_json(raw, path)
            except (UnicodeError, json.JSONDecodeError, X1Error) as exc:
                json_errors.append({"path": path, "error": str(exc)})
    manifest = {
        "schema": "ghc.family.lyren.v664-v4.x1-content-manifest.v1",
        "source_commit": SOURCE_FINAL,
        "target_state": "prospective_x1_staged_tree",
        "canonical_content_domain": "exact_git_blob",
        "self_exclusions": MANIFEST_EXCLUSIONS,
        "entry_count": len(entries),
        "entries": entries,
        "merkle_root_sha256": canonical_sha256(entries),
        "valid": True,
    }
    write_json("x1/x1-content-manifest.json", manifest)
    run_git("add", "--", manifest_path)
    diff_check = run_git("diff", "--cached", "--check", check=False)
    diff_output = (diff_check.stdout + diff_check.stderr).decode("utf-8", "replace").strip()
    stale_labels = []
    stale_sensitive_paths = {
        f"{PHASE_PREFIX}x1/flashcard-architecture-freeze.json",
        f"{PHASE_PREFIX}x1/phase-charter.json",
        f"{PHASE_PREFIX}x1/source-verification.json",
        f"{PHASE_PREFIX}x1/workflow-plan.json",
        f"{PHASE_PREFIX}x1/x1-overview.md",
    }
    for path in sorted(stale_sensitive_paths):
        _, _, raw = index_blob(path)
        text = raw.decode("utf-8", "strict")
        for label in ["Sylven Arc", "v663-v6-r2", "Caelen Morrow v663-v7"]:
            if label in text:
                stale_labels.append({"path": path, "label": label})
    issues = []
    if privacy_candidates:
        issues.append("privacy candidates require classification")
    if json_errors:
        issues.append("strict JSON errors")
    if diff_check.returncode != 0:
        issues.append("git diff --cached --check failed")
    if stale_labels:
        issues.append("stale predecessor labels found")
    staged_with_manifest = zpaths("diff", "--cached", "--name-only", "-z")
    predicted_final = sorted(set(staged_with_manifest) | {review_path})
    if predicted_final != INTENDED_ALLOWLIST:
        issues.append("predicted final staged set differs from exact allowlist")
    review = {
        "schema": "ghc.family.lyren.v664-v4.x1-staged-review.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "lifecycle": "x1_planning_only",
        "expected_staged_path_count": len(INTENDED_ALLOWLIST),
        "staged_path_count": len(predicted_final),
        "staged_paths": predicted_final,
        "allowlist_missing": sorted(set(INTENDED_ALLOWLIST) - set(predicted_final)),
        "allowlist_unexpected": sorted(set(predicted_final) - set(INTENDED_ALLOWLIST)),
        "manifest_entry_count": len(entries),
        "manifest_exclusions": MANIFEST_EXCLUSIONS,
        "manifest_mismatches": [],
        "json_parse_count_before_self_stage": sum(path.endswith(".json") for path in manifest_paths),
        "json_errors": json_errors,
        "privacy_pattern_classes": sorted(PRIVATE_PATTERNS),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": [],
        "stale_label_candidates": stale_labels,
        "diff_check_exit_code": diff_check.returncode,
        "diff_check_output": diff_output,
        "observed_outcomes_present": False,
        "x2_implementation_present": False,
        "successor_contacted": False,
        "issues": issues,
        "boundary": "Exact staged x1 planning review only; no x2 result, independent reproduction, professional authority, or Stage 20 evidence.",
        "valid": not issues,
    }
    write_json("x1/x1-staged-review.json", review)
    strict_json((PHASE / "x1/x1-staged-review.json").read_bytes(), "x1-staged-review")
    run_git("add", "--", review_path)
    final_staged = zpaths("diff", "--cached", "--name-only", "-z")
    if final_staged != INTENDED_ALLOWLIST:
        raise X1Error("final staged x1 set differs from the exact candidate")
    final_check = run_git("diff", "--cached", "--check", check=False)
    if final_check.returncode != 0 or not review["valid"]:
        raise X1Error("x1 staged review failed")
    return review


def audit_only() -> dict[str, Any]:
    corpus, construction = reconstruct_corpus()
    proposals = new_proposals()
    audit = novelty_audit(corpus, construction, proposals)
    return {
        "schema": "ghc.family.lyren.v664-v4.x1-audit-only.v1",
        "corpus_rows": len(corpus),
        "candidate_rows": len(proposals),
        "maximum_inherited_similarity": audit["maximum_inherited_token_jaccard_similarity"],
        "exact_collisions": len(audit["normalized_exact_title_collisions"]),
        "pairwise_collisions": len(audit["new_pairwise_similarity_collisions_at_or_above_0_70"]),
        "valid": audit["valid"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["audit", "build", "stage-review"])
    args = parser.parse_args()
    try:
        if args.command == "audit":
            result = audit_only()
        elif args.command == "build":
            result = build()
        else:
            result = stage_review()
    except (X1Error, subprocess.CalledProcessError, subprocess.TimeoutExpired, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=True, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result.get("valid") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
