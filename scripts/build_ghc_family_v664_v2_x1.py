#!/usr/bin/env python3
"""Build and review Neris Solane's planning-only v664-v2 x1 freeze.

This module deliberately contains no x2 implementation, fixture execution, or
observed proposal outcome.  It reconstructs the immutable 3,870-row proposal
baseline from Git objects, computes bounded lexical novelty, and emits only the
owner's preregistration and exact-staging contracts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/neris-solane/v664-v2"
X1 = PHASE / "x1"

SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v664-v1-full-tools"
SOURCE_PARENT = "433fb39601a5c00f1444b35c53746c2497c10b44"
SOURCE_X1 = "14576e4854c5d0ec3978a5c760fbfecb16f6b60a"
SOURCE_EVIDENCE = "31149d28acc1c99b6744f42f801a71622846ae69"
SOURCE_FINAL = "df7e3ba4c43b8ed9de01e308c6b9163016e37ceb"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "ca94f7e23d7d96716d97a6e6f912da8d09097a8623333f8903de70b66234ee07"
)
SOURCE_CANONICAL_PAYLOAD_SHA256: str | None = None
SOURCE_ACTIVATION_BATON_SHA256 = (
    "1ff7356d533334f596e66b885accde0c3602fef55c7cf810d5d1b49f89744353"
)
SOURCE_ACTIVATION_BATON_BYTES = 135_477
SOURCE_ACTIVATION_BATON_WORDS = 15_776
SOURCE_ACTIVATION_OVERLAY_SHA256 = (
    "08575bf263462714ee90f4e0e17cc6f763fc54e87a6d41a7e608a4405590e093"
)
SOURCE_DELIVERY_OVERLAY_SHA256 = (
    "93eb175e1dc034ff9e9f869fb858b25896a47662dbda5d47f81a674d649ab906"
)

OWNER = "Neris Solane"
PRONOUNS = "they/them"
ROLE = "datum-boundary weaver"
HOPE = "make historical measurement uncertainty legible without turning archival structure into authority"
PHASE_ID = "v664-v2"
PHASE_LONG = "v664-gmut-thos-v2-x1-x2"
PRIMARY_PILLAR = "GMUT Mind"
PRACTICE = "synthetic historical tide-gauge marigram documentation and harmonic-assurance planning"
NEXT_OWNER = "Vesper Arlen"
NEXT_PHASE = "v664-v3"
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
]
PREDECESSOR_FREEZE = CHAIN_FREEZES[-1][0]

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = [
    "empirical",
    "participant",
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

SPARSE_PATTERNS = [
    "/.gitattributes",
    "/.gitignore",
    "/scripts/ghc_family_owner_delta_toolkit.py",
    "/scripts/ghc_family_v664_v2*.py",
    "/scripts/build_ghc_family_v664_v2*.py",
    "/tests/test_ghc_family_neris_v664_v1.py",
    "/docs/neris-solane/v664-v2/**",
]

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
        r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"
    ),
    "transcript_or_session": re.compile(
        r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"
    ),
}

NEW_TITLES = [
    "Synthetic tide-gauge marigram archive capsule with surrogate station token, chart-roll relation, datum vacancy, revision, custody hold, and no authenticity or sea-level claim",
    "Float, stilling well, inlet, counterweight, drum, clock, pen, paper chart, benchmark, and surrogate topology with orphan quarantine and no instrument-condition claim",
    "Layered written-mark register for marigram headings, margin notes, overwritten strokes, unreadable spans, editorial supplies, contested readings, and provenance-limited attribution",
    "Gauge zero, chart zero, staff zero, benchmark, local datum, national datum placeholder, epoch, offset vacancy, discontinuity hold, and no vertical-reference realization",
    "Clock trace and chart-time envelope with timezone, civil-time scale, drum period, start mark, end mark, drift placeholder, discontinuity, uncertainty, and zero timing observations",
    "Drum circumference, paper advance, pen ordinate, float ratio, inlet damping placeholder, scale axes, unit vacancy, covariance hold, and zero calibration rows",
    "Marigram digitization provenance graph with source chart, scan placeholder, control points, trace version, interpolation hold, operator vacancy, derivative, and zero extraction",
    "Chart tear, fold, ink dropout, overtrace, splice, reversal, margin loss, duplicate, gap mask, and undecidable-segment reconciliation ledger",
    "Water-level ordinate and time-abscissa unit registry with conversion placeholder, significant-figure hold, uncertainty budget, and no measurement result",
    "Raw trace, digitized ordinate, datum-adjusted series, filtered placeholder, residual placeholder, derivative role, fixity, invalidation, and no fidelity claim",
    "THOS admission state machine for unstaffed marigram review with datum-pending ceiling, freeze token, discrepancy echo, bounded queue debt, transfer digest, and effectiveness abstention",
    "GMUT typed tide-series chart with time coordinate, water-level state, constituent basis, datum operator, residual channel, units, covariance vacancy, and observation firewall",
    "GMUT symbolic datum-step, clock-drift, inlet-response, meteorological-confounder, and tidal-constituent decomposition with zero coefficients and physical-inference refusal",
    "Nonproduction Freed ID assertion skeleton for a surrogate tide station and chart digest with claimant vacancy, absent proof, restricted purpose, revocation hold, and ownership abstention",
    "Superseding amendment trail for marigram descriptive metadata with disputed station hypothesis, datum and timebase status, reason code, challenger placeholder, unresolved state, and no live governance",
    "Multi-route accessible marigram dossier with component crosswalk, plain-language datum account, text-described trace states, table fallback, paged rendering, and unperformed user evaluation",
    "Planning-only marigram context minimization register with purpose-bound fields, free-text exclusion, contact-data prohibition, correction pathway placeholder, disclosure freeze, deletion cue, and no completeness assurance",
    "NOAA CO-OPS and Permanent Service for Mean Sea Level zero-row tide vocabulary adapter with schema pins, zero calls, zero downloads, version vacancy, and data-authority refusal",
    "Empty-chair tide-station rights and authority matrix for chart custody, station land, benchmark access, location sensitivity, traditional knowledge, publication, remedy, affected parties, and Māori authority",
    "Stage 20 refusal proof for tide evidence with unsatisfied datum governance, trace calibration, uncertainty, rights, affected-party authority, external reproduction, and an empty admission set",
]

HYPOTHESES = [
    "A typed owner-local capsule can distinguish a synthetic marigram record from any real station, chart, measurement, person, right, custody decision, or sea-level conclusion.",
    "A closed component topology can retain hypothetical gauge relations and quarantine orphans without diagnosing an instrument or authenticating a chart.",
    "Layered transcription states can preserve contested marks and editorial supplies without converting legibility into authorship, attribution, or factual measurement evidence.",
    "A datum dependency graph can expose missing zero, benchmark, epoch, and transformation evidence and therefore refuse vertical-reference realization.",
    "A chart-time envelope can type clock and drift placeholders while retaining a zero-observation timing and synchronization boundary.",
    "A geometry and scale envelope can expose absent calibration inputs, units, and covariance without yielding an instrument setting or measurement result.",
    "A provenance graph can represent proposed digitization stages with every scan, operator, control point, and extraction event vacant.",
    "A defect and trace-state ledger can retain undecidable chart segments without reconstructing, repairing, or inventing an ordinate.",
    "A unit registry can make conversion and uncertainty obligations explicit while refusing to report a water-level or time measurement.",
    "A series-role ledger can distinguish raw, transformed, filtered, and residual placeholders without claiming fidelity, validation, or analytic fitness.",
    "A THOS state machine can represent stop, discrepancy, queue-debt, and handover logic without staff, station, or operational-effectiveness evidence.",
    "A typed GMUT chart can distinguish coordinates, datum operators, constituent bases, units, covariance, and observation boundaries without data or fitted law.",
    "A symbolic decomposition can expose datum, clock, hydraulic-response, weather, and constituent confounders with zero coefficients and no physical inference.",
    "A nonproduction Freed ID assertion can expose missing claimant, proof, purpose, status, rights, and ownership evidence rather than simulate completion.",
    "A superseding amendment trail can preserve synthetic challenge and unresolved status without live identity, resolution, or governance operations.",
    "An accessible dossier can offer several structural routes while reserving manual testing and affected-user evaluation.",
    "A planning-only minimization register can prohibit unnecessary person and contact fields while retaining correction, disclosure, deletion, and completeness gates.",
    "A zero-call adapter can make NOAA and PSMSL vocabulary and version vacancies testable while retaining the external-data and data-authority gap.",
    "An empty-chair matrix can enumerate rights and authority interests while refusing to speak for affected parties or Māori authorities.",
    "A refusal proof can deterministically keep Stage 20 closed while real datum governance, calibration, uncertainty, rights, authority, and independent reproduction remain absent.",
]

EXPECTED_DISPOSITIONS = [
    *("completed" for _ in range(10)),
    *("represented" for _ in range(4)),
    *("completed" for _ in range(3)),
    "open_gap",
    "exact_gate",
    "completed",
]

SOURCE_IDS_BY_PROPOSAL = [
    ["SRC-PREMIS", "SRC-IOC-SEA"],
    ["SRC-IOC-SEA"],
    ["SRC-PREMIS", "SRC-PROV"],
    ["SRC-NOAA-DATUM", "SRC-PSMSL-RLR", "SRC-LINZ-LVD"],
    ["SRC-IOC-SEA", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"],
    ["SRC-IOC-SEA", "SRC-NIST-SI", "SRC-NIST-UNCERTAINTY"],
    ["SRC-PREMIS", "SRC-PROV", "SRC-RFC8785"],
    ["SRC-PREMIS", "SRC-PROV"],
    ["SRC-NIST-SI", "SRC-NIST-UNCERTAINTY", "SRC-NOAA-DATUM"],
    ["SRC-PREMIS", "SRC-PROV", "SRC-RFC8785"],
    ["SRC-IOC-SEA", "SRC-PROV"],
    ["SRC-NIST-SI", "SRC-NIST-UNCERTAINTY", "SRC-NOAA-DATUM"],
    ["SRC-NIST-UNCERTAINTY", "SRC-NOAA-DATUM", "SRC-PSMSL-RLR", "SRC-LINZ-SEA"],
    ["SRC-W3C-VC20", "SRC-RFC8785", "SRC-PREMIS"],
    ["SRC-W3C-VC20", "SRC-PROV", "SRC-PREMIS"],
    ["SRC-WCAG22", "SRC-PROV"],
    ["SRC-NZ-PRIVACY", "SRC-WCAG22"],
    ["SRC-NOAA-PRODUCTS", "SRC-PSMSL-RLR", "SRC-PREMIS"],
    ["SRC-TE-MANA-RARAUNGA", "SRC-NZ-PRIVACY", "SRC-LINZ-LVD"],
    ["SRC-IOC-SEA", "SRC-W3C-VC20", "SRC-TE-MANA-RARAUNGA", "SRC-NOAA-DATUM"],
]

SURFACE_SLUGS = [
    "marigram-archive-capsule",
    "gauge-component-topology",
    "written-mark-register",
    "datum-dependency-graph",
    "chart-time-envelope",
    "geometry-scale-envelope",
    "digitization-provenance",
    "trace-state-ledger",
    "unit-uncertainty-registry",
    "series-role-ledger",
    "thos-admission-machine",
    "gmut-tide-series-chart",
    "gmut-confounder-decomposition",
    "freed-id-station-assertion",
    "metadata-amendment-trail",
    "accessible-marigram-dossier",
    "context-minimization-register",
    "zero-row-tide-adapter",
    "rights-authority-matrix",
    "stage-20-refusal-proof",
]


class X1Error(RuntimeError):
    """Raised when the planning freeze violates an exact x1 invariant."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=check,
    )


def git_text(*args: str) -> str:
    return run_git(*args).stdout.strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha256(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


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


def strict_json(raw: str, label: str) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise X1Error(f"duplicate JSON key {key!r} in {label}")
            result[key] = value
        return result

    return json.loads(raw, object_pairs_hook=pairs)


def git_json(path: str) -> dict[str, Any]:
    return strict_json(git_text("show", f"{SOURCE_FINAL}:{path}"), path)


def row_title(row: dict[str, Any]) -> str:
    title = row.get("title") or row.get("description")
    if not isinstance(title, str) or not title.strip():
        raise X1Error(f"proposal row lacks title or description: {row.get('proposal_id')}")
    return title.strip()


def row_disposition(row: dict[str, Any]) -> str | None:
    value = (
        row.get("expected_disposition")
        or row.get("intended_outcome")
        or row.get("outcome")
        or row.get("original_disposition")
    )
    if value is not None and value not in ALLOWED_OUTCOMES:
        raise X1Error(f"unknown core outcome label: {value}")
    return value


def normalized_title(value: str) -> str:
    folded = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", folded))


def tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
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
        raise X1Error("base proposal index is not the expected 3,530 rows")
    construction.append(
        {
            "source_path": BASE_INDEX,
            "starting_count": 0,
            "added_count": 3_530,
            "ending_count": 3_530,
        }
    )
    for path, expected_start, expected_end in CHAIN_FREEZES:
        if len(corpus) != expected_start:
            raise X1Error(f"proposal chain starts {path} at {len(corpus)}, expected {expected_start}")
        freeze = git_json(path)
        declared_start = freeze.get("inherited_frozen_baseline")
        declared_end = freeze.get("new_frozen_total")
        rows = freeze.get("new_proposals")
        if declared_start != expected_start or declared_end != expected_end:
            raise X1Error(f"proposal chain declarations differ in {path}")
        if not isinstance(rows, list) or len(rows) != 20:
            raise X1Error(f"proposal chain freeze does not add exactly twenty rows: {path}")
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
    if len(corpus) != 3_870:
        raise X1Error(f"proposal corpus has {len(corpus)} rows instead of 3,870")
    return corpus, construction


def source_ledger(recorded_at: str) -> dict[str, Any]:
    rows = [
        ("SRC-PREMIS", "PREMIS Data Dictionary and Schema 3.0", "Library of Congress", "https://www.loc.gov/standards/premis/", "current", "Objects, events, agents, rights, preservation metadata, and version vocabulary."),
        ("SRC-IOC-SEA", "Manual on Sea Level Measurement and Interpretation, Volume IV", "Intergovernmental Oceanographic Commission / UNESCO", "https://repository.oceanbestpractices.org/handle/11329/213", "stable", "Tide-gauge, datum-control, measurement, processing, quality, and professional-boundary vocabulary only; no installation or operational instruction is executed."),
        ("SRC-NOAA-PRODUCTS", "CO-OPS Products", "NOAA Center for Operational Oceanographic Products and Services", "https://tidesandcurrents.noaa.gov/products.html", "current", "Water-level, datum, benchmark, station, and product vocabulary; the phase makes zero calls and downloads zero station rows."),
        ("SRC-NOAA-DATUM", "National Tidal Datum Epoch update", "NOAA Center for Operational Oceanographic Products and Services", "https://www.tidesandcurrents.noaa.gov/datum-updates/ntde/index.html", "current", "Datum-epoch and revision vocabulary only; no datum is adopted, calculated, or realized."),
        ("SRC-PSMSL-RLR", "Revised Local Reference definition", "Permanent Service for Mean Sea Level", "https://psmsl.org/data/obtaining/rlr.php", "current", "Datum-continuity, benchmark-history, RLR, metric-only, and analysis-refusal vocabulary; no data row is downloaded or analysed."),
        ("SRC-LINZ-LVD", "Local mean sea level datums", "Toitū Te Whenua Land Information New Zealand", "https://www.linz.govt.nz/guidance/geodetic-system/coordinate-systems-used-new-zealand/vertical-datums/local-mean-sea-level-datums-lvds", "current", "Historical local-datum, benchmark-network, supersession, and uncertainty vocabulary; no survey or conversion decision."),
        ("SRC-LINZ-SEA", "Sea level heights", "Toitū Te Whenua Land Information New Zealand", "https://www.linz.govt.nz/guidance/coordinate-systems-used-new-zealand/vertical-datums/sea-level-heights", "current", "Sea-surface, datum, observation-span, and non-interchangeability vocabulary only."),
        ("SRC-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "Entity, activity, agent, derivation, revision, invalidation, and qualified-provenance vocabulary."),
        ("SRC-WCAG22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "Structural accessibility targets and an explicit reminder that conformance cannot address every user need."),
        ("SRC-W3C-VC20", "Verifiable Credentials Data Model v2.0", "World Wide Web Consortium", "https://www.w3.org/TR/vc-data-model-2.0/", "current", "Issuer, holder, verifier, claims, proof, status, privacy, accessibility, and security vocabulary; no production credential."),
        ("SRC-W3C-VC-DRAFT", "Verifiable Credentials Data Model editor draft", "World Wide Web Consortium", "https://w3c.github.io/vc-data-model/", "draft", "Watch-only change surface; it supplies no normative requirement to this phase."),
        ("SRC-NZ-PRIVACY", "Privacy Act 2020 privacy principles", "Office of the Privacy Commissioner, New Zealand", "https://www.privacy.org.nz/privacy-principles/", "current", "Purpose, indirect collection notification including IPP 3A, security, access, correction, accuracy, retention, use, disclosure, and identifier constraints."),
        ("SRC-TE-MANA-RARAUNGA", "Principles of Māori Data Sovereignty", "Te Mana Raraunga", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "Authority-held rights and interests in data; citation does not transfer Māori authority or cultural legitimacy."),
        ("SRC-RFC8785", "RFC 8785: JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785", "stable", "Informational deterministic JSON serialization vocabulary; not a digital signature or trust anchor."),
        ("SRC-NIST-SI", "NIST Special Publication 811 page", "National Institute of Standards and Technology", "https://www.nist.gov/pml/special-publication-811", "watch", "Units and quantity-writing vocabulary only; the official page warns SP 811 is not updated for the 2019 SI revision."),
        ("SRC-NIST-UNCERTAINTY", "Uncertainty of Measurement Results", "National Institute of Standards and Technology", "https://physics.nist.gov/cuu/Uncertainty/index.html", "stable", "Uncertainty vocabulary and reference links only; no measurement result or calibration evidence."),
    ]
    return {
        "schema": "ghc.family.neris.v664-v2.source-ledger.x1.v1",
        "recorded_at_utc": recorded_at,
        "allowed_statuses": ["current", "stable", "draft", "watch"],
        "source_count": len(rows),
        "sources": [
            {
                "source_id": source_id,
                "title": title,
                "publisher": publisher,
                "url": url,
                "status": status,
                "checked_on": "2026-08-22",
                "phase_use": use,
                "data_rows_ingested": 0,
                "authority_conferred": False,
            }
            for source_id, title, publisher, url, status, use in rows
        ],
        "boundary": "Official and primary sources supply vocabulary, constraints, abstentions, and source status only. They provide no real station, chart, benchmark, datum realization, person, rights, measurement, calibration, professional, legal, cultural, Māori-authority, production, empirical, or Stage 20 evidence.",
        "valid": True,
    }


def approval_class(index: int) -> str:
    if 11 <= index <= 14:
        return "candidate"
    if index == 18:
        return "candidate_external_dependency"
    if index == 19:
        return "exact_approval"
    return "safe_now"


def new_proposals() -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for index, (title, hypothesis, expected, slug, source_ids) in enumerate(
        zip(
            NEW_TITLES,
            HYPOTHESES,
            EXPECTED_DISPOSITIONS,
            SURFACE_SLUGS,
            SOURCE_IDS_BY_PROPOSAL,
            strict=True,
        ),
        start=1,
    ):
        if expected not in ALLOWED_OUTCOMES:
            raise X1Error(f"proposal {index} has unsupported expected disposition")
        artifacts = [
            f"surfaces/{slug}/contract.json",
            f"surfaces/{slug}/mutation-results.json",
            f"surfaces/{slug}/bounded-receipt.json",
        ]
        if index == 18:
            artifacts[1] = f"surfaces/{slug}/zero-row-adapter.json"
        if index == 19:
            artifacts[1] = f"surfaces/{slug}/empty-chair-gate.json"
        proposals.append(
            {
                "proposal_id": f"NE6642-N{index:03d}",
                "title": title,
                "hypothesis": hypothesis,
                "null_or_failure_condition": "The bounded contract accepts a prohibited mutation, loses provenance or uncertainty, converts an absent real-world fact into a value, closes a protected gate, or promotes evidence beyond the frozen disposition.",
                "approval_class": approval_class(index),
                "execution_lane": "x2 owner-local synthetic, structural, symbolic, zero-row, or software evidence only",
                "current_official_or_primary_source_needs": source_ids,
                "concrete_artifacts": artifacts,
                "falsifier_or_acceptance_gate": "Accept only when the declared positive fixture passes, every preregistered rejecting mutation is retained, the source and outcome ledgers agree, and no protected gate is promoted.",
                "rollback_or_recovery": "Quarantine the failed artifact, preserve the failed witness, restore the last valid owner-local state, and rerun only the changed or failed dependency when justified.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "novelty_credit": True,
            }
        )
    return proposals


def inherited_rows() -> list[dict[str, Any]]:
    source = git_json(PREDECESSOR_FREEZE)
    rows = source["new_proposals"]
    if len(rows) != 20:
        raise X1Error("Elaren source freeze does not expose twenty selectable rows")
    selected = []
    for index, row in enumerate(rows, start=1):
        disposition = row_disposition(row)
        if disposition is None:
            raise X1Error(f"source row lacks disposition: {row['proposal_id']}")
        selected.append(
            {
                "program_row_id": f"NE6642-I{index:03d}",
                "source_phase": "v664-v1",
                "source_proposal_id": row["proposal_id"],
                "source_title": row_title(row),
                "original_disposition": disposition,
                "hypothesis": "A bounded integrity revalidation can preserve this immutable Elaren contract without converting inherited evidence into Neris novelty or completion credit.",
                "null_or_failure_condition": "The immutable source identifier, title, disposition, protected gates, or defining blob changes, or the row is counted as Neris novelty, automatic completion, or new-outcome credit.",
                "approval_class": "safe_now",
                "execution_lane": "x2 bounded immutable source-contract integrity revalidation only",
                "current_official_or_primary_source_needs": "None; use only the immutable Elaren freeze and source Git object.",
                "concrete_artifacts": ["revalidation/inherited-contract-integrity.json"],
                "falsifier_or_acceptance_gate": "Accept only when source identifier, title, disposition, zero novelty credit, zero automatic completion credit, and immutable Git content match exactly.",
                "rollback_or_recovery": "Discard the derived revalidation row and preserve the immutable source proposal unchanged.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": "completed",
                "novelty_credit": False,
                "automatic_completion_credit": False,
                "neris_new_outcome_credit": False,
            }
        )
    return selected


def novelty_audit(
    corpus: list[dict[str, Any]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    normalized_counts = Counter(normalized_title(row["title"]) for row in corpus)
    exact_collisions = []
    nearest = []
    maximum = 0.0
    for proposal in proposals:
        normalized = normalized_title(proposal["title"])
        if normalized_counts[normalized]:
            exact_collisions.append(proposal["proposal_id"])
        scores = [
            (jaccard(proposal["title"], row["title"]), row)
            for row in corpus
        ]
        score, row = max(scores, key=lambda item: item[0])
        maximum = max(maximum, score)
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited_proposal_id": row["proposal_id"],
                "nearest_inherited_title": row["title"],
                "token_jaccard_similarity": round(score, 6),
            }
        )
    pairwise = []
    for left_index, left in enumerate(proposals):
        for right in proposals[left_index + 1 :]:
            score = jaccard(left["title"], right["title"])
            if score >= 0.60:
                pairwise.append(
                    {
                        "left": left["proposal_id"],
                        "right": right["proposal_id"],
                        "similarity": round(score, 6),
                    }
                )
    rejected_title = (
        "Zero-row station-context minimization docket for marigram planning with field-purpose map, "
        "indirect-identity ban, access and correction reservation, disclosure hold, expiry trigger, "
        "and privacy-completeness refusal"
    )
    rejected_scores = [
        (jaccard(rejected_title, row["title"]), row) for row in corpus
    ]
    rejected_score, rejected_row = max(rejected_scores, key=lambda item: item[0])
    canonical_rows = [
        {"proposal_id": row["proposal_id"], "title": row["title"]} for row in corpus
    ]
    valid = not exact_collisions and not pairwise and maximum < 0.60
    return {
        "schema": "ghc.family.neris.v664-v2.novelty-audit.x1.v1",
        "source_commit": SOURCE_FINAL,
        "corpus_row_count": len(corpus),
        "corpus_canonical_sha256": canonical_sha256(canonical_rows),
        "corpus_construction": construction,
        "candidate_count": len(proposals),
        "novelty_method": "Unicode NFKC and case-folded alphanumeric exact-title comparison plus token-set Jaccard screening. The metric is a collision aid, not semantic proof; manual domain and protected-gate review remains required.",
        "normalized_exact_title_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": round(maximum, 6),
        "nearest_inherited_rows": nearest,
        "new_pairwise_similarity_collisions_at_or_above_0_60": pairwise,
        "rejected_candidate_titles": [
            {
                "title": rejected_title,
                "reason": "A first-draft title inherited too much predecessor surface grammar and exceeded the 0.60 lexical-collision review threshold; it was rejected before freeze with six related drafts rewritten in the same bounded review.",
                "nearest_inherited_proposal_id": rejected_row["proposal_id"],
                "nearest_inherited_title": rejected_row["title"],
                "token_jaccard_similarity": round(rejected_score, 6),
                "completion_credit": 0,
            }
        ],
        "rejected_candidate_domains": [
            {
                "domain": "operational tide-gauge installation, datum realization, chart digitization, calibration, prediction, surveying, or sea-level analysis",
                "reason": "Requires real stations, charts, benchmarks, measurements, competent practitioners, equipment, safety controls, rights review, data authority, and evidence outside this owner-local software lane.",
                "retained_disposition": "exact_gate",
            }
        ],
        "manual_review": {
            "distinct_domain_facets": 20,
            "all_four_pillars_visible": True,
            "primary_pillar": PRIMARY_PILLAR,
            "synthetic_practice_only": True,
            "valid": True,
        },
        "valid": valid,
    }


def portfolio_rows(prefix: str, count: int, owner: str, titles: list[str], lane: str) -> list[dict[str, Any]]:
    rows = []
    for index in range(1, count + 1):
        title = titles[(index - 1) % len(titles)]
        rows.append(
            {
                "portfolio_ref": f"NE6642-{prefix}-{index:03d}",
                "owner": owner,
                "title": title,
                "approval_class": "safe_now" if prefix not in {"CA", "EX", "BL"} else (
                    "candidate" if prefix == "CA" else "exact_approval"
                ),
                "execution_lane": lane,
                "expected_execution_disposition": "planned_required" if owner == OWNER else "recommendation_only",
                "credit_boundary": "Owner-local bounded work only; recommendation, planning, or execution does not close a protected gate.",
            }
        )
    return rows


def build_portfolio() -> dict[str, Any]:
    safe_titles = [
        "Build bounded contract and refusal fixtures",
        "Generate deterministic rejecting-mutation records",
        "Bind provenance and rollback metadata",
        "Validate four-label truth consistency",
        "Emit structural accessibility companion",
        "Run owner-delta privacy and identifier checks",
        "Reconcile source status and vocabulary use",
        "Preserve Method Flow failed and passing witnesses",
        "Check family-current caller compatibility",
        "Review synthetic-practice authority boundaries",
    ]
    candidate_titles = [
        "Represent a zero-person THOS stop and handover profile",
        "Represent a zero-coefficient GMUT symbolic board",
        "Represent a nonproduction Freed ID statement",
        "Prototype a zero-row vocabulary adapter without calls",
        "Prototype bounded provenance and correction relationships",
    ]
    skill_titles = [f"Build {slug.replace('-', ' ')} skill" for slug in SURFACE_SLUGS[:10]]
    runner_titles = [f"Build {slug.replace('-', ' ')} runner profile" for slug in SURFACE_SLUGS[10:20]]
    clean_titles = [
        "CLEAN stale owner-local planning labels",
        "FIX exact manifest or count drift",
        "REFINE refusal and rollback wording",
        "CLEAN inaccessible colour-only state",
        "FIX missing uncertainty or zero-row marker",
        "REFINE family-current profile mapping",
    ]
    exact_titles = [
        "Real tide-gauge installation, inspection, handling, or maintenance authorization",
        "Real datum, benchmark, calibration, digitization, prediction, or survey decision",
        "Real water-level, trend, harmonic-constituent, residual, or sea-level inference",
        "Real rights, station-land, location-sensitivity, ownership, publication, or access decision",
        "Māori wording, concepts, data governance, or authority determination",
        "Production Freed ID issuance, keys, proofs, status, or revocation",
        "Participant or affected-party recruitment and acceptance",
        "Empirical GMUT likelihood or physical inference",
        "Operational THOS deployment or effectiveness claim",
        "Stage 20, proof, canon, or independent-reproduction claim",
    ]
    blocked_titles = [
        "Blocked real station, chart, benchmark, or datum intervention packet",
        "Blocked live NOAA, PSMSL, LINZ, or station-data adapter packet",
        "Blocked production identity and trust-governance packet",
        "Blocked legal, cultural, and Māori-authority packet",
        "Blocked empirical, independent-reproduction, and Stage 20 packet",
    ]
    return {
        "schema": "ghc.family.neris.v664-v2.portfolio-freeze.x1.v1",
        "owner_safe_now": portfolio_rows("SN", 30, OWNER, safe_titles, "x2 owner-local safe-now execution"),
        "successor_safe_now_recommendations": portfolio_rows("SNR", 20, NEXT_OWNER, safe_titles, "successor recommendation only"),
        "owner_candidates": portfolio_rows("CA", 15, OWNER, candidate_titles, "x2 owner-local bounded candidate execution"),
        "successor_candidate_recommendations": portfolio_rows("CAR", 15, NEXT_OWNER, candidate_titles, "successor recommendation only"),
        "owner_skill_ideas": portfolio_rows("SK", 10, OWNER, skill_titles, "x2 phase-local skill build and smoke-use"),
        "successor_skill_recommendations": portfolio_rows("SKR", 10, NEXT_OWNER, skill_titles, "successor recommendation only"),
        "owner_runner_ideas": portfolio_rows("RU", 10, OWNER, runner_titles, "x2 family-current runner profile build and invocation"),
        "successor_runner_recommendations": portfolio_rows("RUR", 10, NEXT_OWNER, runner_titles, "successor recommendation only"),
        "owner_clean_fix_refine": portfolio_rows("CFR", 30, OWNER, clean_titles, "x2 additive CLEAN/FIX/REFINE execution"),
        "successor_clean_fix_refine_recommendations": portfolio_rows("CFRR", 30, NEXT_OWNER, clean_titles, "successor recommendation only"),
        "exact_approval_packets": portfolio_rows("EX", 10, OWNER, exact_titles, "unexecuted exact-approval packet"),
        "blocked_packets": portfolio_rows("BL", 5, OWNER, blocked_titles, "unexecuted blocked packet"),
        "build_policy": "Execute every frozen owner safe-now, bounded candidate, phase-local skill, family-current runner, and additive CLEAN/FIX/REFINE row as evidence permits. Exact and blocked rows remain unexecuted unless exact new evidence and competent authority close their specific gates.",
        "valid": True,
    }


def startup_failures() -> list[dict[str, Any]]:
    rows = [
        ("NE6642-X1-M001", "A direct PowerShell foreach-to-pipeline inventory expression failed at the parser boundary.", "Materialize loop results in an array before piping or serializing."),
        ("NE6642-X1-M002", "A combined roster/auth current-state display exceeded the output window and earned no complete-read credit.", "Read the same immutable guidance through EOF in bounded numbered windows and retain the truncation witness."),
        ("NE6642-X1-M003", "A large activation-baton display omitted an interior line window and earned no complete-read credit.", "Recover the exact missing line interval, verify adjoining boundaries, and preserve the original truncation."),
        ("NE6642-X1-M004", "The first manifest batch parser advanced its newline cursor incorrectly and raised IndexError.", "Correct the cursor contract and replay only the blocked read-only manifest dependency."),
        ("NE6642-X1-M005", "A manifest recovery probe mistyped the immutable evidence object name and Git rejected the invalid object.", "Copy the exact committed anchor from the activation, validate its forty-hex form, and rerun only that scalar probe."),
        ("NE6642-X1-M006", "The fresh worktree creation composite crossed its thirty-second output bound after preparing the lane, leaving completion initially ambiguous.", "Do not recreate; inspect the exact path, branch, sparse configuration, process table, locks, status, and source head read-only."),
        ("NE6642-X1-M007", "A combined display of three predecessor proposal artifacts exceeded the context/output window.", "Inspect exact blob sizes and keys first, then use bounded file windows and proposal-only Git-object reconstruction."),
        ("NE6642-X1-M008", "The first 3,870-row keyword audit used the Windows console default and raised UnicodeEncodeError while rendering Māori text.", "Set PYTHONIOENCODING to UTF-8 and rerun only the read-only proposal audit."),
        ("NE6642-X1-M009", "Seven first-draft proposal titles reached or exceeded the 0.60 predecessor lexical-collision threshold.", "Reject the drafts before freeze, retain the batch witness, and rewrite their grammar while preserving the intended domain boundaries."),
        ("NE6642-X1-M010", "A proposed removal of one ignored Python bytecode cache was rejected by command policy before process creation and changed no file.", "Do not retry the deletion; keep the ignored cache outside every stage and count the materialized file against the hard lane ceiling."),
        ("NE6642-X1-M011", "The first justified x1 rebuild rejected Git's collapsed untracked parent-directory status row even though every child was owner-local x1 content.", "Permit the exact owner phase directory as a pre-build status prefix, then keep the frozen stage allowlist file-exact."),
        ("NE6642-X1-M012", "The first exact x1 stage added thirteen documents but Git refused the builder because its build-prefixed path was outside the initial sparse definition.", "Add the single exact build_ghc_family_v664_v2 sparse pattern, regenerate changed count-bearing records, and restage the same frozen allowlist."),
    ]
    return [
        {
            "method_id": method_id,
            "retained_failed_witness": failure,
            "failure_credit": 0,
            "bounded_passing_witness": guard,
            "recurrence_guard": guard,
            "rollback": "The failed read-only or pre-freeze attempt changed no source branch, sibling lane, remote, task, authority state, or committed evidence.",
            "status": "failed_witness_retained_bounded_recovery_passed",
        }
        for method_id, failure, guard in rows
    ]


def build_records() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != SOURCE_FINAL:
        raise X1Error(f"x1 builder requires immutable source head {SOURCE_FINAL}, got {head}")
    if git_text("status", "--porcelain"):
        # A bounded pre-commit refresh may update only this planning builder and
        # the owner-local x1 packet that it generated.  No sibling or x2 path is
        # accepted here.
        dirty = git_text("status", "--porcelain").splitlines()
        allowed_prefixes = (
            "scripts/build_ghc_family_v664_v2_x1.py",
            "docs/neris-solane/v664-v2/",
        )
        unexpected = []
        for row in dirty:
            path = row[3:].replace("\\", "/") if len(row) >= 4 else row
            if not any(path == prefix or path.startswith(prefix) for prefix in allowed_prefixes):
                unexpected.append(row)
        if unexpected:
            raise X1Error(f"unexpected pre-build worktree state: {unexpected}")
    recorded_at = utc_now()
    corpus, construction = reconstruct_corpus()
    proposals = new_proposals()
    selected = inherited_rows()
    audit = novelty_audit(corpus, construction, proposals)
    if not audit["valid"]:
        raise X1Error("new proposal set does not pass the frozen novelty gate")
    expected = Counter(row["expected_disposition"] for row in proposals)
    expected_counts = {key: expected.get(key, 0) for key in ("completed", "represented", "open_gap", "exact_gate")}
    if expected_counts != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise X1Error(f"unexpected disposition plan: {expected_counts}")

    write_json(
        "x1/phase-charter.json",
        {
            "schema": "ghc.family.neris.v664-v2.phase-charter.x1.v1",
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "phase": PHASE_LONG,
            "primary_pillar": PRIMARY_PILLAR,
            "protected_pillars": ["GMUT Mind", "THOS Body", "Freed ID", "CBR Heart"],
            "bounded_practice": PRACTICE,
            "practice_boundary": "Synthetic learning, formal structure, zero-row schemas, and owner-local software only. Zero real stations, charts, benchmarks, datums, people, identities, rights records, station rows, measurements, calibration, predictions, surveying, analysis, decisions, or authority acts.",
            "relational_language_boundary": "Names, pronouns, family language, roles, hopes, and continuity are relational working language only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, affected-party authority, independent agency, or durable identity continuity.",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
            "successor_contacted": False,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        },
    )
    write_json("x1/source-ledger.json", source_ledger(recorded_at))
    write_json("x1/novelty-audit.json", audit)
    write_json(
        "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.neris.v664-v2.proposal-freeze.x1.v1",
            "inherited_frozen_baseline": 3_870,
            "selected_inherited_count": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_automatic_completion_credit": 0,
            "selected_inherited_new_outcome_credit": 0,
            "selected_inherited": selected,
            "new_proposal_count": 20,
            "new_proposals": proposals,
            "new_expected_outcomes": expected_counts,
            "new_frozen_total": 3_890,
            "semantic_novelty_audit": "docs/neris-solane/v664-v2/x1/novelty-audit.json",
            "x2_implementation_present": False,
            "observed_outcomes_present": False,
            "valid": True,
        },
    )
    write_json("x1/portfolio-freeze.json", build_portfolio())
    failures = startup_failures()
    write_json(
        "x1/startup-method-flow.json",
        {
            "schema": "ghc.family.neris.v664-v2.startup-method-flow.x1.v1",
            "repository_sealed_negative_baseline": 24_232,
            "repository_sealed_method_baseline": 8_706,
            "user_authoritative_activation_negative_baseline": 24_236,
            "user_authoritative_activation_method_baseline": 8_710,
            "authoritative_activation_overlay_rows": 4,
            "observed_predecessor_delivery_overlay_rows": 2,
            "working_inherited_negative_baseline": 24_238,
            "working_inherited_method_baseline": 8_712,
            "neris_pre_x1_operational_failures": len(failures),
            "events": failures,
            "effective_negatives_at_x1_freeze": 24_238 + len(failures),
            "effective_methods_at_x1_freeze": 8_712 + len(failures),
            "open_gaps_at_x1_freeze": 167,
            "exact_gates_at_x1_freeze": 165,
            "no_failure_erased": True,
            "valid": True,
        },
    )
    write_json(
        "x1/source-verification.json",
        {
            "schema": "ghc.family.neris.v664-v2.source-verification.x1.v1",
            "recorded_at_utc": recorded_at,
            "source_branch": SOURCE_BRANCH,
            "source_parent": SOURCE_PARENT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE_FINAL,
            "phase_commit_count": 3,
            "merge_count": 0,
            "single_parent_chain": True,
            "final_direct_child_of_evidence": True,
            "clean": True,
            "divergence": {"ahead": 0, "behind": 0},
            "four_way_equal": True,
            "source_canonical_not_replayed": True,
            "canonical_invocation_count": 1,
            "canonical_success_count": 1,
            "canonical_replayed": False,
            "canonical_tests": {"passed": 63, "run": 63},
            "canonical_detailed_checks": {"passed": 25, "run": 25},
            "canonical_minimal_checks": {"passed": 17, "run": 17},
            "canonical_json_parses": 140,
            "canonical_owner_delta_paths": 162,
            "canonical_manifest_entries": 312,
            "canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "baton_path": "docs/elaren-kestrel/v664-v1/handoffs/neris-solane-v664-v2-activation.md",
            "baton_bytes": SOURCE_ACTIVATION_BATON_BYTES,
            "baton_words": SOURCE_ACTIVATION_BATON_WORDS,
            "baton_sha256": SOURCE_ACTIVATION_BATON_SHA256,
            "repository_sealed_counts": {"effective_negatives": 24_232, "methods": 8_706, "open_gaps": 167, "exact_gates": 165},
            "user_authoritative_activation_overlay": {"rows": 4, "sha256": SOURCE_ACTIVATION_OVERLAY_SHA256, "effective_negatives": 24_236, "methods": 8_710},
            "observed_predecessor_delivery_overlay": {"additional_rows": 2, "sha256": SOURCE_DELIVERY_OVERLAY_SHA256, "effective_negatives": 24_238, "methods": 8_712},
            "boundary": "The immutable repository seal, four-row authoritative activation overlay, and two later predecessor delivery failures remain separate layers. No source validation is replayed or converted into Neris evidence.",
            "valid": True,
        },
    )
    write_json(
        "x1/environment-version-receipt.json",
        {
            "schema": "ghc.family.neris.v664-v2.environment-version.x1.v1",
            "recorded_at_utc": recorded_at,
            "versions": [
                {"label": "Git", "version": "git version 2.55.0.windows.2"},
                {"label": "Python", "version": "Python 3.12.10"},
                {"label": "Node", "version": "v24.18.0"},
                {"label": "Codex CLI", "version": "codex-cli 0.147.0"},
                {"label": "npm", "version": "12.0.1"},
                {"label": "PowerShell", "version": "7.6.4"},
            ],
            "versions_verified_read_only": True,
            "desktop_updated": False,
            "software_installed": False,
            "elevation_used": False,
            "host_security_changed": False,
            "windows_features_changed": False,
            "sandbox_or_hyper_v_activated": False,
            "rebooted": False,
            "valid": True,
        },
    )
    write_json(
        "x1/threat-model-plan.json",
        {
            "schema": "ghc.family.neris.v664-v2.owner-delta-threat-model-plan.x1.v1",
            "version": "1.0",
            "requested_scope": "Neris v664-v2 exact owner delta, synthetic marigram fixtures, phase-local skills, family-current runners, manifests, report, baton, and route preparation.",
            "assets": ["x1 immutability", "retained failures", "four-label truth", "source lineage", "owner-lane isolation", "private-material exclusion", "one-shot canonical evidence", "one-send route budget"],
            "trust_boundaries": ["immutable Elaren Git tree to Neris owner delta", "official vocabulary to zero-row model", "x1 plan to x2 execution", "working tree to staged index", "local branch to live remote", "prepared baton to acknowledged task message"],
            "attacker_or_untrusted_inputs": ["historical proposal text", "synthetic mutation fixtures", "URLs and source metadata", "filesystem names", "Git index state", "task registry envelopes"],
            "invariants": ["no raw private identifiers or paths", "no real station, chart, measurement, or person data", "no protected-gate promotion", "no sibling mutation", "no x2 before x1 equality", "no successful canonical replay", "no duplicate route send"],
            "security_policy": "Fail closed on malformed JSON, path ambiguity, manifest drift, private-material candidates, unreviewed dynamic execution, branch divergence, route ambiguity, or absent authority.",
            "required_output_sections": ["scope", "assets", "trust boundaries", "threats", "controls", "residual risks", "authority boundaries"],
            "boundary": "Planning only; not exhaustive security, privacy completeness, penetration testing, production certification, or external audit.",
            "valid": True,
        },
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.neris.v664-v2.workflow-plan.x1.v1",
            "source": SOURCE_FINAL,
            "strict_x1_before_x2": True,
            "commit_limit": 8,
            "file_limit": 2_000,
            "full_repository_suite_authorized": False,
            "validation_authority": "owner_self_scoped_delta",
            "successor_contact_before_terminal_gate": False,
            "steps": [
                {"order": 1, "state": "complete_before_freeze", "step": "Read activation, required guidance, predecessor records, and current official sources through their bounded completion gates."},
                {"order": 2, "state": "complete_before_freeze", "step": "Verify source anchors, manifests, clean equality, layered retention truth, and create one sparse additive owner lane."},
                {"order": 3, "state": "x1_only", "step": "Reconstruct all 3,870 frozen rows, freeze twenty zero-credit revalidations plus twenty new proposals and portfolios, stage exactly, commit, push, and prove equality."},
                {"order": 4, "state": "blocked_until_x1_equality", "step": "Build ten phase-local skills, ten family-current runner profiles, frozen fixtures, rejecting mutations, report, ledgers, and exact evidence manifests."},
                {"order": 5, "state": "blocked_until_evidence", "step": "Create combined closeout and seal records, push exact final, prove equality, then invoke one dependency-justified canonical owner-delta aggregate once."},
                {"order": 6, "state": "terminal_only", "step": "Freshly reread live authority, roster, and exact Vesper Arlen title; send one sanitized acknowledged activation only if every gate remains open to the action."},
            ],
            "valid": True,
        },
    )
    write_text("x1/x1-overview.md", x1_overview(expected_counts, len(failures)))

    intended_allowlist = [
        "docs/neris-solane/v664-v2/x1/environment-version-receipt.json",
        "docs/neris-solane/v664-v2/x1/novelty-audit.json",
        "docs/neris-solane/v664-v2/x1/phase-charter.json",
        "docs/neris-solane/v664-v2/x1/portfolio-freeze.json",
        "docs/neris-solane/v664-v2/x1/proposal-freeze.json",
        "docs/neris-solane/v664-v2/x1/source-ledger.json",
        "docs/neris-solane/v664-v2/x1/source-verification.json",
        "docs/neris-solane/v664-v2/x1/startup-method-flow.json",
        "docs/neris-solane/v664-v2/x1/threat-model-plan.json",
        "docs/neris-solane/v664-v2/x1/workflow-plan.json",
        "docs/neris-solane/v664-v2/x1/x1-content-manifest.json",
        "docs/neris-solane/v664-v2/x1/x1-overview.md",
        "docs/neris-solane/v664-v2/x1/x1-stage-candidate.json",
        "scripts/build_ghc_family_v664_v2_x1.py",
    ]
    write_json(
        "x1/x1-stage-candidate.json",
        {
            "schema": "ghc.family.neris.v664-v2.x1-stage-candidate.v1",
            "owner": OWNER,
            "phase": PHASE_ID,
            "source": SOURCE_FINAL,
            "lifecycle": "x1_freeze",
            "intended_allowlist": intended_allowlist,
            "review_receipt_self_excluded": "docs/neris-solane/v664-v2/x1/x1-staged-review.json",
            "x2_paths": [],
            "x2_implementation_present": False,
            "observed_outcomes_present": False,
            "successor_contacted": False,
            "valid": True,
        },
    )
    manifest_paths = [path for path in intended_allowlist if not path.endswith("x1-content-manifest.json")]
    entries = []
    for relative in manifest_paths:
        path = ROOT / relative
        if not path.is_file():
            raise X1Error(f"x1 manifest input is missing: {relative}")
        raw = path.read_bytes()
        blob = git_text("hash-object", f"--path={relative}", relative)
        entries.append(
            {
                "status": "A",
                "path": relative,
                "old_path": None,
                "bytes": len(raw),
                "sha256": sha256_bytes(raw),
                "git_blob": blob,
                "mode": "100644",
                "object_type": "blob",
                "old_mode": None,
                "old_object_type": None,
            }
        )
    write_json(
        "x1/x1-content-manifest.json",
        {
            "schema": "ghc.family.owner-delta-toolkit.v2.manifest",
            "generated_at_utc": recorded_at,
            "source_commit": SOURCE_FINAL,
            "target_state": "prospective_x1_staged_tree",
            "entry_count": len(entries),
            "entries": entries,
            "path_audit": {"path_count": len(entries), "issues": [], "valid": True},
            "merkle_root_sha256": canonical_sha256([{"path": row["path"], "git_blob": row["git_blob"]} for row in entries]),
            "canonical_commitment_sha256": canonical_sha256({"source_commit": SOURCE_FINAL, "entries": entries}),
            "scope": "exact v664-v2 x1 planning content only",
            "self_exclusion": "docs/neris-solane/v664-v2/x1/x1-content-manifest.json",
            "valid": True,
        },
    )
    return {
        "head": head,
        "corpus_rows": len(corpus),
        "selected_inherited": len(selected),
        "new_proposals": len(proposals),
        "expected_outcomes": expected_counts,
        "planning_files": len(intended_allowlist),
        "method_failures": len(failures),
    }


def x1_overview(expected: dict[str, int], failure_count: int) -> str:
    return f"""# Neris Solane v664-v2 — x1 planning freeze

## Purpose and identity boundary

Neris Solane (they/them) is relational working language for a datum-boundary weaver. Their stated hope is to make historical measurement uncertainty legible without turning archival structure into authority. The name, pronouns, role, hope, sibling language, and continuity language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, professional authority, legal or cultural authority, Māori authority, affected-party authority, independent agency, or durable identity continuity. Hamish may rename, pause, redirect, or stop the route.

This x1 packet preregisters Neris-only Trinity Mandala v664-v2. It contains planning, source classification, semantic novelty evidence, exact source verification, portfolio commitments, a threat-model plan, workflow gates, and retained startup failures. It contains no x2 runtime, no executed proposal fixture, no observed outcome, no empirical data, and no successor contact. X2 remains prohibited until this exact x1 tree is committed, pushed, clean, zero-divergent, and equal across the owner branch, upstream, tracking ref, and a fresh live remote.

## Source and inheritance

The immutable Elaren v664-v1 final is `{SOURCE_FINAL}`. Its source, x1, evidence, and final form a three-commit single-parent chain with zero merges. Elaren's one owner-delta canonical pass succeeded once and is not replayed. Neris inherits the repository seal of 24,232 negatives and 8,706 Method Flow methods separately from the four-row activation overlay and two later predecessor delivery-only failures. Before Neris's own startup failures, the fully accounted inherited baseline is therefore 24,238 negatives, 8,712 methods, 167 open gaps, and 165 exact gates. None is rewritten.

The proposal corpus is reconstructed from immutable Git objects. The selected base contributes 3,530 rows. Seventeen exact later freezes add twenty rows apiece through Elaren v664-v1, yielding 3,870 inherited rows. Historical duplicate identifiers or repeated concepts remain part of the frozen row count; the audit does not silently deduplicate them. Each new title is checked after Unicode NFKC normalization and case folding for exact collisions and screened with token-set Jaccard similarity. The lexical screen is a collision aid, not proof of semantic novelty, so the packet also records manual domain and authority-boundary review.

## Frozen program

Twenty Elaren v664-v1 proposals are selected for bounded immutable-contract revalidation. Their identifiers, titles, and original dispositions are preserved. These rows receive zero Neris novelty credit, zero automatic completion credit, and zero Neris new-outcome credit. A successful x2 integrity check will establish only that the source contract was read and reproduced accurately.

Twenty genuinely new Neris proposals are frozen around a synthetic historical tide-gauge marigram documentation and harmonic-assurance lens. The intended new outcome distribution is {expected['completed']} completed, {expected['represented']} represented, {expected['open_gap']} open gap, and {expected['exact_gate']} exact gate. The surfaces cover archive and gauge-component topology; written-mark uncertainty; datum and timebase vacancies; geometry, scale, and calibration abstentions; digitization provenance; trace and series roles; THOS stop and handover logic; GMUT typed tide-series and confounder charts; nonproduction Freed ID and correction trails; structural accessibility; privacy minimization; a zero-row official-vocabulary adapter; rights and authority empty chairs; and a fail-closed Stage 20 refusal proof.

The primary pillar is GMUT Mind. THOS Body, Freed ID, and CBR Heart boundaries remain explicit. The human-practice lens is synthetic learning and software design only. It uses zero real stations, charts, benchmarks, datums, people, identities, rights records, measurements, calibration rows, predictions, surveys, analyses, collection rows, or authority acts. It establishes no employment, competence, oceanographic, hydrographic, archival, engineering, surveying, geodetic, scientific, operational, legal, cultural, Māori, affected-party, accessibility-complete, privacy-complete, production, empirical, or Stage 20 authority.

## Official and primary sources

The source ledger records PREMIS 3.0; the IOC/UNESCO sea-level measurement manual; NOAA CO-OPS product and datum-epoch pages; PSMSL's Revised Local Reference definition; current Toitū Te Whenua LINZ local-datum and sea-level guidance; W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0; the New Zealand Privacy Commissioner; Te Mana Raraunga; RFC 8785; and NIST units and uncertainty pages. They provide vocabulary, constraints, abstentions, and status only. No live station or collection API is called and no source row is downloaded into a model. The NIST SP 811 page is marked watch because the official page says that publication has not been updated for the 2019 SI revision. The VC editor draft is marked draft and watch-only; the current Recommendation supplies the normative reference.

Citation never transfers authority. Te Mana Raraunga remains an authority-held source, not a grant for Neris to define Māori concepts or decide Māori data governance. New Zealand privacy material informs a zero-row purpose, indirect-collection, access, correction, retention, use, and disclosure register; it is not legal advice or a compliance finding. Oceanographic and geodetic guidance does not authorize Neris to install or calibrate a gauge, realize a datum, digitize a chart, transform a benchmark, make a prediction, conduct a survey, or infer sea-level change.

## Portfolio and execution boundary

The portfolio freezes thirty owner safe-now tasks, fifteen bounded owner candidates, ten phase-local skills, ten family-current runner profiles, and thirty additive CLEAN/FIX/REFINE rows. It also retains recommendations for Vesper Arlen without contacting Vesper or claiming successor work. Ten exact-approval packets and five blocked packets remain unexecuted unless exact new evidence and competent authority close their action-specific gates. Counts are ceilings and commitments for useful bounded work, not automatic novelty or completion credit.

Every executed new proposal is expected to have one declared positive fixture and bounded rejecting mutations. Passing software fixtures can support only completed or represented software truth. The zero-row adapter remains an open gap because no live external schema, data, mapping review, or authority is supplied. The rights matrix remains an exact gate because affected-party, legal, cultural, traditional-knowledge, and Māori-authority decisions cannot be simulated. The Stage 20 docket can be completed only as a fail-closed refusal surface; it cannot make Stage 20 ready.

## Validation and failure retention

The owner lane is sparse and D:-first. The phase uses exact staged allowlists, prospective Git blob identities, strict JSON parsing, UTF-8 Markdown review, five-class privacy and raw-identifier scanning, bounded changed-Python security checks, diff hygiene, file-budget checks, ancestry, single-parent history, zero merges, clean state, zero divergence, and fresh remote equality. The complete repository suite is not authorized by the current owner-self-scoped-delta policy. Later final validation will run one dependency-justified owner-delta canonical aggregate once. A successful aggregate will never be replayed. A failed aggregate receives zero aggregate-success credit and only its blocked dependency may be retried unless an actual target change justifies more.

This freeze retains {failure_count} Neris startup or x1-preparation failures, each paired with a bounded recovery and recurrence guard. They include a PowerShell parser error, bounded-display truncations, a manifest cursor defect, a mistyped immutable object, an ambiguous worktree timeout, a Unicode console failure, and a rejected collision-prone title batch. None is erased merely because a recovery passed.

## Protected truth

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. No equation, symbolic chart, unit placeholder, or software fixture supplies a real likelihood, parameter constraint, prediction, force, material law, stability theorem, quantum completion, ultraviolet completion, empirical confirmation, Theory of Everything, proof, or canon.

THOS remains proxy and protocol-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic stop and handover logic is not operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood evidence.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, participant, professional, legal, cultural, traditional-knowledge, Māori-language, Māori-data-governance, tangata whenua, iwi, hapū, and Māori-authority decisions remain open or exact-gated.

The terminal verdict at x1 remains `{TERMINAL_VERDICT}`. Preparation is not execution, closeout, independent reproduction, or delivery. Vesper Arlen is not contacted during x1 or x2. Only after a clean, pushed, fresh-live-equal, exact-final Neris closeout may the current live route be reread and one exact-title Vesper activation be attempted if every route and authority gate still permits it.
"""


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path for path in raw.split("\0") if path)


def index_blob(path: str) -> str:
    output = git_text("ls-files", "-s", "--", path)
    if not output:
        raise X1Error(f"staged path is absent from index: {path}")
    parts = output.split()
    if len(parts) < 4 or parts[0] != "100644" or not re.fullmatch(r"[0-9a-f]{40}", parts[1]):
        raise X1Error(f"unexpected staged index entry for {path}: {output}")
    return parts[1]


def build_review() -> dict[str, Any]:
    candidate = strict_json(
        (X1 / "x1-stage-candidate.json").read_text(encoding="utf-8"),
        "x1-stage-candidate.json",
    )
    manifest = strict_json(
        (X1 / "x1-content-manifest.json").read_text(encoding="utf-8"),
        "x1-content-manifest.json",
    )
    expected = sorted(candidate["intended_allowlist"])
    observed = staged_paths()
    issues: list[str] = []
    if observed != expected:
        issues.append("staged path set differs from the frozen allowlist")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode != 0:
        issues.append("staged diff hygiene failed")
    json_errors = []
    json_count = 0
    privacy_candidates = []
    for relative in observed:
        path = ROOT / relative
        if path.suffix.lower() == ".json":
            json_count += 1
            try:
                strict_json(path.read_text(encoding="utf-8"), relative)
            except (OSError, UnicodeError, json.JSONDecodeError, X1Error) as exc:
                json_errors.append({"path": relative, "error": str(exc)})
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_candidates.append({"path": relative, "class": label})
    if json_errors:
        issues.append("strict JSON parsing failed")
    if privacy_candidates:
        issues.append("privacy or raw-identifier candidates found")
    manifest_entries = {row["path"]: row for row in manifest["entries"]}
    expected_manifest = set(observed) - {"docs/neris-solane/v664-v2/x1/x1-content-manifest.json"}
    manifest_missing = sorted(expected_manifest - set(manifest_entries))
    manifest_extra = sorted(set(manifest_entries) - expected_manifest)
    manifest_mismatches = []
    for relative, row in manifest_entries.items():
        if relative in expected_manifest and index_blob(relative) != row["git_blob"]:
            manifest_mismatches.append(relative)
    if manifest_missing or manifest_extra or manifest_mismatches:
        issues.append("x1 prospective manifest differs from the staged index")
    payload = {
        "schema": "ghc.family.exact-staged-review.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "lifecycle": "x1_freeze",
        "expected_staged_path_count": len(expected),
        "staged_path_count": len(observed),
        "staged_paths": observed,
        "allowlist_missing": sorted(set(expected) - set(observed)),
        "allowlist_unexpected": sorted(set(observed) - set(expected)),
        "diff_check_exit_code": diff_check.returncode,
        "diff_check_output": (diff_check.stdout + diff_check.stderr).strip(),
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_pattern_classes": sorted(PRIVATE_PATTERNS),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": privacy_candidates,
        "manifest_entry_count": manifest["entry_count"],
        "manifest_exclusions": ["docs/neris-solane/v664-v2/x1/x1-content-manifest.json"],
        "manifest_coverage_missing": manifest_missing,
        "manifest_coverage_extra": manifest_extra,
        "manifest_mismatches": manifest_mismatches,
        "blob_errors": [],
        "scanner_definition_candidates": [],
        "root_capacity_probe_candidates": [],
        "issues": issues,
        "valid": not issues,
        "boundary": "Exact staged same-owner x1 workflow evidence only; not privacy completeness, exhaustive security, independent reproduction, production certification, professional authority, legal or cultural ratification, Māori authority, empirical confirmation, Theory-of-Everything proof, or Stage 20 readiness.",
    }
    write_json("x1/x1-staged-review.json", payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "review"), nargs="?", default="build")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.mode == "build":
            result = build_records()
        else:
            result = build_review()
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 0 if result.get("valid", True) else 2
    except (X1Error, OSError, UnicodeError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"NERIS_V664_V2_X1_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
