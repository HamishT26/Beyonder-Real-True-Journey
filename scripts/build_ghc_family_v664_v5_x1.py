#!/usr/bin/env python3
"""Build Ilyra Fen v664-v5's planning-only x1 freeze."""

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
PHASE = ROOT / "docs/ilyra-fen/v664-v5"
X1 = PHASE / "x1"

SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v664-v4-full-tools"
SOURCE_PARENT = "78a59d6e25e4a57840f6b416fcbc05a5485aa60a"
SOURCE_X1 = "a11d57463d86a37876a06e5ea3cc04ac37cd7e99"
SOURCE_EVIDENCE = "4ee2f244f6958e3ffeca6c27eece1a510059ffec"
SOURCE_INITIAL_FINAL = "9bfb7cbc8fc438367207ce8d38070cf5d7fcb74b"
SOURCE_FINAL = "9bfb7cbc8fc438367207ce8d38070cf5d7fcb74b"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "4fbfb476e43187c1b85b2f347263803462c0a4c4e6debaea09824184fb28a0f4"
)
SOURCE_FAILED_RECEIPT_SHA256 = ""
SOURCE_ROUTE_RECEIPT_SHA256 = "SENT_ONCE_ACKNOWLEDGED_BY_CODEX_APP"
SOURCE_BATON_SHA256 = (
    "ba5025558ec7a710c7b76a5fb3cf3f762fcc007e32c7a3ebdd7eec5a80228757"
)
SOURCE_BATON_BYTES = 283_971
SOURCE_BATON_WORDS = 30_217
ROSTER_SHA256 = "45bff52f7331cdd37303d14649f0542a1fd10eaf6d1c2043ac5216301e02c912"
AUTH_SHA256 = "ddcaaceb05339ee32b1c589a6b884f3f11e1d79cc26a16ee3e1695d67ee610e8"

OWNER = "Ilyra Fen"
OPTIONAL_PRONOUNS = "she/they"
ROLE = "relational evidence-boundary steward and uncertainty cartographer"
HOPE = (
    "leave every structural-vibration claim traceable, every uncertainty visible, "
    "and every professional, safety, legal, cultural, and Maori-authority gate unmistakable"
)
PHASE_ID = "v664-v5"
DISPLAY_PHASE = "Ilyra Fen v664-v5"
PRIMARY_PILLAR = "GMUT Mind with THOS Body and Freed ID and CBR Heart protected"
PRACTICE = "synthetic structural-vibration monitoring, uncertainty review, and engineering handover planning"
NEXT_OWNER = "Auren Lark"
NEXT_PHASE = "v664-v6"
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
    ("docs/lyren-moss/v664-v4/x1/proposal-freeze.json", 3_910, 3_930),
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

PHASE_PREFIX = "docs/ilyra-fen/v664-v5/"
BUILDER_PATH = "scripts/build_ghc_family_v664_v5_x1.py"
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
    if len(corpus) != 3_930:
        raise X1Error(f"proposal corpus has {len(corpus)} rows instead of 3,930")
    return corpus, construction


def source_ledger(recorded_at: str) -> dict[str, Any]:
    rows = [
        (
            "SRC-USGS-NSMP",
            "National Strong Motion Project",
            "U.S. Geological Survey",
            "https://earthquake.usgs.gov/monitoring/nsmp/",
            "current",
            "Program, structural-array, waveform stewardship, engineering-use, and explicit real-world authority vocabulary only.",
        ),
        (
            "SRC-USGS-NSMP-DATA",
            "National Strong Motion Project Data",
            "U.S. Geological Survey",
            "https://earthquake.usgs.gov/monitoring/nsmp/nsmpdata.php",
            "current",
            "Processed-record, metadata, instrument-response, archive, and product-boundary vocabulary; this phase downloads zero rows.",
        ),
        (
            "SRC-FDSN-MSEED3",
            "FDSN miniSEED 3 specification",
            "International Federation of Digital Seismograph Networks",
            "https://docs.fdsn.org/projects/miniseed3/en/latest/",
            "current_watch",
            "Record headers, source identifiers, timing, encoding, extra-header, state-of-health, and unknown-extension refusal vocabulary.",
        ),
        (
            "SRC-FDSN-STATIONXML",
            "FDSN StationXML 1.2 documentation",
            "International Federation of Digital Seismograph Networks",
            "https://docs.fdsn.org/projects/stationxml/en/latest/overview.html",
            "current_watch",
            "Network, station, channel, epoch, response, sensitivity, unit, uncertainty, equipment, and availability vocabulary.",
        ),
        (
            "SRC-NIST-TN1297",
            "NIST Technical Note 1297: Guidelines for Evaluating and Expressing Measurement Uncertainty",
            "National Institute of Standards and Technology",
            "https://www.nist.gov/pml/nist-technical-note-1297",
            "current",
            "Type A, Type B, combined, expanded, coverage-factor, unit, and reporting-obligation vocabulary; no measurement is performed.",
        ),
        (
            "SRC-FHWA-SHM",
            "State of the Practice and Art for Structural Health Monitoring of Bridge Substructures",
            "Federal Highway Administration",
            "https://www.fhwa.dot.gov/publications/research/infrastructure/structures/bridge/09040/index.cfm",
            "stable",
            "Remote acquisition, sensor-system, monitoring-plan, lifecycle, and residual professional-judgment vocabulary only.",
        ),
        (
            "SRC-FEMA-P58",
            "FEMA P-58-1 Seismic Performance Assessment of Buildings, Volume 1",
            "Federal Emergency Management Agency",
            "https://www.fema.gov/sites/default/files/documents/fema_p-58-1-se_volume1_methodology.pdf",
            "stable",
            "Response quantity, uncertainty, consequence, stakeholder-communication, model-scope, and professional-liability boundaries.",
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
            "SRC-WCAG22",
            "Web Content Accessibility Guidelines 2.2",
            "World Wide Web Consortium",
            "https://www.w3.org/TR/WCAG22/",
            "current",
            "Structural perceivability, text alternatives, tables, labels, navigation, status, and manual-evaluation reservation.",
        ),
        (
            "SRC-RFC8785",
            "RFC 8785: JSON Canonicalization Scheme",
            "RFC Editor",
            "https://www.rfc-editor.org/rfc/rfc8785",
            "current_watch",
            "Deterministic JSON serialization and verified-errata awareness only; never a signature, trust anchor, or identity proof.",
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
            "downloaded_measurement_rows": 0,
            "authority_boundary": "Official or primary-source wording informs a synthetic schema only; citation is not professional, safety, legal, cultural, Maori-authority, empirical, or operational evidence.",
        }
        for source_id, title, publisher, url, status, use in rows
    ]
    return {
        "schema": "ghc.family.ilyra.v664-v5.source-ledger.x1.v1",
        "recorded_at_utc": recorded_at,
        "source_count": len(sources),
        "allowed_statuses": ["current", "current_watch", "stable"],
        "sources": sources,
        "boundary": "Read-only source review with zero data queries, downloads, waveform rows, structures, sensors, accounts, participants, equipment operations, or professional assessments.",
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
        "proposal_id": f"IF6645-N{index:03d}",
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
            "sensor-array-topology",
            "Synthetic structural sensor-array topology capsule with surrogate structure token, floor and component relations, channel vacancies, revision lineage, quarantine, and no condition conclusion",
            "completed",
            "safe_now",
            ["SRC-USGS-NSMP", "SRC-FHWA-SHM"],
            "A typed graph can distinguish an imaginary sensor layout from a real structure, installation, inspection, person, place, asset, or safety result.",
        ),
        (
            "channel-epoch-response-obligations",
            "Channel epoch and instrument-response obligation board with source identifier, response stages, sensitivity, units, validity interval, uncertainty slots, and zero observed stations",
            "completed",
            "safe_now",
            ["SRC-FDSN-STATIONXML", "SRC-USGS-NSMP-DATA"],
            "A closed metadata board can reject missing response or epoch obligations without claiming StationXML conformance or interpreting a real channel.",
        ),
        (
            "clock-synchronization-uncertainty",
            "Sampling-clock synchronization and timing-uncertainty envelope with nominal rate, offset, drift, leap-state, covariance vacancy, and no estimated correction",
            "completed",
            "safe_now",
            ["SRC-FDSN-MSEED3", "SRC-NIST-TN1297"],
            "A typed timebase envelope can expose uncertainty debt and reject invented timing values while processing no waveform.",
        ),
        (
            "orientation-unit-coordinate-guard",
            "Sensor orientation, coordinate-frame, polarity, gravity-axis, acceleration-unit, conversion-lineage, and dimensional-consistency guard with all real geometry vacant",
            "completed",
            "safe_now",
            ["SRC-FDSN-STATIONXML", "SRC-NIST-TN1297"],
            "A unit and frame guard can reject incompatible synthetic claims without locating, calibrating, or assessing any sensor or structure.",
        ),
        (
            "acquisition-provenance-event-chain",
            "Zero-row acquisition provenance chain with synthetic recorder, configuration, firmware, trigger, transformation, checksum, supersession, invalidation, and custody events",
            "completed",
            "safe_now",
            ["SRC-PROV", "SRC-RFC8785"],
            "An event ledger can preserve deterministic synthetic lineage and fail closed on orphan derivations without acquiring or authenticating data.",
        ),
        (
            "miniseed-header-refusal",
            "miniSEED 3 structural header and extra-header refusal tribunal with format version, source identifier, time quality, encoding, payload length, extension, and checksum vacancies",
            "completed",
            "safe_now",
            ["SRC-FDSN-MSEED3", "SRC-RFC8785"],
            "A zero-waveform structural fixture can test declared header obligations and unknown-extension handling without decoding or asserting conformance.",
        ),
        (
            "stationxml-response-completeness",
            "StationXML response-completeness tribunal with network, station, channel, epoch, equipment, stage sequence, input and output units, sensitivity, and availability debt",
            "completed",
            "safe_now",
            ["SRC-FDSN-STATIONXML", "SRC-NIST-TN1297"],
            "A synthetic document profile can reject incomplete response chains without validating an official schema instance or real instrument.",
        ),
        (
            "window-aliasing-leakage-quarantine",
            "Window, sampling, aliasing, spectral-leakage, filter-transient, segment-overlap, padding, and frequency-bin quarantine with zero spectral estimate",
            "completed",
            "safe_now",
            ["SRC-USGS-NSMP-DATA", "SRC-NIST-TN1297"],
            "A typed analysis precondition board can expose invalid synthetic configurations while emitting no modal frequency, damping, or damage inference.",
        ),
        (
            "gmut-modal-obligation-board",
            "GMUT typed modal-obligation board for displacement proxy, acceleration proxy, mass and stiffness operators, eigenpair domain, damping convention, boundary conditions, units, and observation firewall",
            "represented",
            "candidate",
            ["SRC-FHWA-SHM", "SRC-FEMA-P58"],
            "A symbolic board can represent linearized modal obligations while all coefficients, structures, measurements, predictions, and physical conclusions remain absent.",
        ),
        (
            "gmut-model-discrepancy-separation",
            "GMUT model-discrepancy separation chart for excitation, sensor response, environmental covariance, operational variability, numerical truncation, residual, and structural-change nonidentifiability",
            "represented",
            "candidate",
            ["SRC-NIST-TN1297", "SRC-FEMA-P58"],
            "A typed discrepancy chart can prevent residuals from becoming damage, force, law, likelihood, posterior, or empirical GMUT evidence.",
        ),
        (
            "thos-vibration-handover",
            "THOS synthetic monitoring handover statechart for intake debt, clock hold, metadata discrepancy, anomaly quarantine, correction readback, workload ceiling, escalation, and explicit stop",
            "represented",
            "candidate",
            ["SRC-FHWA-SHM", "SRC-USGS-NSMP"],
            "A bounded state machine can represent handover and refusal logic without workers, structures, incidents, service outcomes, or effectiveness evidence.",
        ),
        (
            "freed-id-dataset-claim-shell",
            "Freed ID digest-referenced fictitious vibration-dataset claim shell with blank issuer, subject, controller, verification material, status, purpose, consent, entitlement, challenge, and revocation",
            "represented",
            "candidate",
            ["SRC-PROV", "SRC-RFC8785"],
            "A nonproduction claim shell can make absent identity and governance evidence explicit without keys, proofs, accounts, issuances, or trust decisions.",
        ),
        (
            "missingness-saturation-dropout",
            "Missing-channel, saturation, clipping, dropout, trigger-censoring, telemetry-gap, maintenance-window, denominator, and unresolved-cause register with zero detected events",
            "completed",
            "safe_now",
            ["SRC-USGS-NSMP-DATA", "SRC-FDSN-MSEED3"],
            "A zero-observation register can distinguish detector definitions from findings and reject silent denominator repair.",
        ),
        (
            "intervention-amendment-trace",
            "Append-only synthetic sensor intervention and metadata-amendment trace for orientation, gain, location, timing, firmware, channel mapping, checksum, challenge, supersession, and no adjudicator",
            "completed",
            "safe_now",
            ["SRC-PROV", "SRC-FDSN-STATIONXML"],
            "A superseding event trail can preserve contested descriptions without real maintenance, identity, professional review, or governance action.",
        ),
        (
            "accessible-vibration-dossier",
            "Accessible synthetic vibration dossier with semantic headings, captioned data tables, text-only plot alternative, uncertainty labels, anomaly-status explanation, print fallback, and manual review reserved",
            "completed",
            "safe_now",
            ["SRC-WCAG22", "SRC-NIST-TN1297"],
            "A structural report can provide multiple navigation and interpretation routes while refusing complete accessibility or affected-user claims.",
        ),
        (
            "monitoring-data-minimization",
            "Purpose-limited structural-monitoring metadata firewall with fictitious asset token, exact location and contact exclusions, retention vacancy, disclosure refusal, correction queue, and completeness debt",
            "completed",
            "safe_now",
            ["SRC-PROV", "SRC-WCAG22"],
            "A minimization contract can prohibit unnecessary identifying fields while reserving privacy, security, legal, access, and completeness decisions.",
        ),
        (
            "canonical-fixture-integrity",
            "Canonical synthetic fixture integrity tribunal with strict JSON parsing, deterministic ordering, exact Git-blob identity, manifest self-exclusions, supersession, and no signature or authenticity claim",
            "completed",
            "safe_now",
            ["SRC-RFC8785", "SRC-PROV"],
            "A content-identity tribunal can detect bounded owner-fixture drift without creating trust, authenticity, nonrepudiation, or production security.",
        ),
        (
            "zero-row-nsmp-adapter",
            "USGS NSMP and FDSN zero-row structural-waveform adapter with official product identities, response-metadata requirements, version watch, zero queries, zero downloads, and likelihood refusal",
            "open_gap",
            "candidate_external_dependency",
            ["SRC-USGS-NSMP-DATA", "SRC-FDSN-MSEED3", "SRC-FDSN-STATIONXML"],
            "A zero-call adapter can make governed product and metadata vacancies testable while retaining the real-data, calibration, interoperability, and empirical gap.",
        ),
        (
            "structural-safety-authority-matrix",
            "Empty-chair structural safety, occupancy, inspection, evacuation, repair, disclosure, remedy, legal, affected-party, cultural, data-governance, and Maori-authority matrix",
            "exact_gate",
            "exact_approval",
            ["SRC-FEMA-P58", "SRC-FHWA-SHM"],
            "An empty-chair matrix can enumerate decision rights while refusing to speak for engineers, owners, occupants, regulators, affected people, or Maori authorities.",
        ),
        (
            "stage20-strong-motion-refusal",
            "Terminal nonpromotion theorem for synthetic structural vibration whose evidence vector requires calibrated instrumentation, governed data, validated models, professional review, affected-party legitimacy, and independent reproduction while the current vector is null",
            "completed",
            "safe_now",
            ["SRC-USGS-NSMP", "SRC-NIST-TN1297", "SRC-WCAG22"],
            "A deterministic refusal can keep Stage 20 closed while every empirical, professional, safety, authority, accessibility, and independent-review input remains absent.",
        ),
    ]
    return [proposal(index, *spec) for index, spec in enumerate(specs, 1)]


def selected_inherited() -> list[dict[str, Any]]:
    freeze = git_json(PREDECESSOR_FREEZE)
    rows = freeze.get("new_proposals")
    if not isinstance(rows, list) or len(rows) != 20:
        raise X1Error("Lyren v664-v4 source freeze does not expose exactly twenty new rows")
    selected: list[dict[str, Any]] = []
    for index, row in enumerate(rows, 1):
        selected.append(
            {
                "program_row_id": f"IF6645-I{index:03d}",
                "source_phase": "v664-v4",
                "source_proposal_id": row["proposal_id"],
                "source_title": row_title(row),
                "original_disposition": row_disposition(row),
                "hypothesis": "A bounded Git-object integrity revalidation can preserve this immutable Lyren contract without converting inherited evidence into Ilyra novelty or completion credit.",
                "null_or_failure_condition": "The source identifier, title, disposition, protected gates, or defining Git object changes, or the row is counted as Ilyra novelty, automatic completion, or new-outcome credit.",
                "approval_class": "safe_now",
                "execution_lane": "x2 immutable source-contract integrity revalidation only",
                "current_official_or_primary_source_needs": "None; use the exact Lyren freeze at the immutable source commit.",
                "concrete_artifacts": ["revalidation/inherited-contract-integrity.json"],
                "falsifier_or_acceptance_gate": "Accept only when source identifier, title, disposition, zero novelty credit, zero automatic completion credit, and exact Git content agree.",
                "rollback_or_recovery": "Discard the derived revalidation row and preserve the immutable source proposal unchanged.",
                "expected_disposition": row_disposition(row),
                "novelty_credit": False,
                "automatic_completion_credit": False,
                "ilyra_new_outcome_credit": False,
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
        "schema": "ghc.family.ilyra.v664-v5.novelty-audit.x1.v1",
        "source_commit": SOURCE_FINAL,
        "candidate_count": len(proposals),
        "corpus_row_count": len(corpus),
        "corpus_canonical_sha256": canonical_sha256(canonical_rows),
        "corpus_construction": construction,
        "normalized_exact_title_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": round(maximum, 6),
        "nearest_inherited_rows": nearest,
        "new_pairwise_similarity_collisions_at_or_above_0_70": pairwise,
        "novelty_method": "Unicode NFKC and case-folded alphanumeric exact-title comparison plus token-set Jaccard screening against all 3,930 immutable inherited rows. The metric is a collision aid, not semantic proof.",
        "manual_review": "The sensor topology, time synchronization, response metadata, modal-obligation, uncertainty, accessibility, professional-authority, and fail-closed domains were reviewed against all inherited titles. Similar workflow grammar is continuity, not novelty evidence by itself.",
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
            "portfolio_ref": f"IF6645-{prefix}-{index:03d}",
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
        "Reverify Lyren's exact source anchors, three single-parent commits, zero merges, 822 manifests, clean state, and fresh four-way equality without replaying its canonical aggregate",
        "Record the unused D-first lane, sparse-before-materialization receipt, literal path set, and hard 2,000-file rotation guard",
        "Reconstruct and hash the complete 3,930-row proposal corpus from exact Git objects",
        "Revalidate twenty selected Lyren proposal contracts at zero Ilyra novelty and outcome credit",
        "Validate the ten-source official or primary structural-monitoring ledger with zero waveform rows",
        "Build the synthetic sensor-array topology capsule and orphan-channel quarantine",
        "Build the channel epoch and response-obligation board",
        "Build the clock synchronization and timing-uncertainty envelope",
        "Build the sensor orientation, coordinate, polarity, unit, and dimensional guard",
        "Build the zero-row acquisition provenance and invalidation chain",
        "Build the miniSEED structural header and unknown-extension refusal tribunal",
        "Build the StationXML response-completeness tribunal",
        "Build the window, aliasing, leakage, transient, and overlap quarantine",
        "Represent the GMUT modal-obligation board with zero coefficients or observations",
        "Represent the GMUT model-discrepancy and nonidentifiability chart",
        "Represent the THOS monitoring handover and correction-readback statechart",
        "Represent the nonproduction Freed ID dataset-claim shell with all trust actors vacant",
        "Build the missingness, saturation, dropout, censoring, and denominator register",
        "Build the append-only intervention and metadata-amendment trace",
        "Build the structurally accessible vibration dossier while reserving manual review",
        "Build the purpose-limited monitoring-data metadata firewall",
        "Build the strict JSON and exact Git-blob fixture-integrity tribunal",
        "Materialize the USGS and FDSN zero-row adapter with every external and empirical field vacant",
        "Publish the empty-chair structural-safety authority matrix without deciding any case",
        "Build the deterministic Stage 20 strong-motion refusal predicate",
        "Execute and retain one hundred preregistered rejecting mutations at zero completion credit",
        "Build, validate, and smoke-use ten phase-local structural-monitoring skills",
        "Build and invoke ten fixed family-current runner profiles on accepting and rejecting fixtures",
        "Publish Method Flow, five-class privacy, changed-Python security, strict JSON, and workload receipts",
        "Build exact manifests, staged reviews, modular flashcards, accessible static output, compact route pointer, and final terminal receipts",
    ]
    successor_safe = [
        "Bind one exact Ilyra final and committed baton before any Auren mutation",
        "Create Auren's owner lane sparse before checkout and record literal materialization",
        "Carry every inherited failure, open gap, exact gate, and four truth label unchanged",
        "Reconstruct the 3,950-row proposal corpus from exact Git objects",
        "Select twenty inherited contracts with zero novelty and automatic completion credit",
        "Freeze twenty genuinely distinct proposals with falsifiers, recovery, and gates",
        "Keep Auren x1 planning-only and prove four-way equality before x2",
        "Use only official or primary sources needed by the bounded lens",
        "Use no real participant, professional, cultural, legal, safety, or operational data",
        "Build deterministic positive fixtures and preregistered rejecting mutations",
        "Retain every command, parser, timeout, assumption, or test failure before recovery",
        "Use exact Git-blob manifests rather than Windows checkout-byte assumptions",
        "Strict-parse every owner JSON with duplicate-key rejection",
        "Scan only Auren's exact source-to-final privacy boundary",
        "Run security checks only on Auren's changed Python modules",
        "Preserve family-current callers when remastering tools",
        "Keep structural accessibility separate from manual and affected-user evaluation",
        "Build a modular baton with at least ten deterministic sections",
        "Invoke one exact-final canonical pass and never replay a success",
        "Resolve and immediately reread only the live-authorized next exact-title task after Auren's terminal gate",
    ]
    owner_candidates = [
        "Prototype deterministic mode-shape normalization without interpreting any real structure",
        "Prototype synthetic sensor-orientation reconciliation with unresolved geometry preserved",
        "Prototype response-stage unit propagation without calibration or conformance claims",
        "Prototype trigger-window segmentation with censored-boundary flags",
        "Prototype spectral-bin lineage with no modal estimate or damage inference",
        "Prototype clock-drift covariance placeholders without fitted values",
        "Prototype structural-array graph traversal with rejecting cycle and orphan fixtures",
        "Prototype telemetry-gap accounting without repairing denominators",
        "Prototype a station-metadata version-drift watcher without network polling",
        "Prototype a provenance supersession graph without identity or authenticity claims",
        "Prototype an accessible plot-description grammar with manual evaluation reserved",
        "Prototype a privacy-minimal asset-token mapping without real locations",
        "Prototype a THOS correction-replay queue without operators or effectiveness evidence",
        "Represent an independent professional review route while keeping review absent",
        "Represent a deployment and calibrated-data plan behind exact gates",
    ]
    successor_candidates = [
        "Compare two bounded schema designs without claiming universal superiority",
        "Prototype one deterministic graph with an explicit rejecting cycle mutation",
        "Prototype one zero-row standards adapter with version and authority vacancies",
        "Represent one THOS state machine without operator or efficacy evidence",
        "Represent one GMUT typed model without observations or fitted parameters",
        "Represent one Freed ID envelope without live keys, issuers, subjects, or proofs",
        "Draft one accessibility evaluation plan while reserving human assessment",
        "Draft one privacy minimization plan while reserving legal completeness",
        "Draft one security threat model without exhaustive-security language",
        "Draft one rollback rehearsal without destructive execution",
        "Measure bounded deterministic output identity rather than asserting performance",
        "Prototype one compatibility wrapper while retaining the historical caller",
        "Represent one independent review route without claiming it occurred",
        "Represent one external deployment plan behind an exact gate",
        "Represent one successor baton graph with no early contact",
    ]
    skill_ideas = [
        "Ilyra sensor-array topology boundary skill",
        "Ilyra response-chain obligation skill",
        "Ilyra clock uncertainty vacancy skill",
        "Ilyra orientation and unit guard skill",
        "Ilyra miniSEED structural refusal skill",
        "Ilyra StationXML completeness skill",
        "Ilyra modal nonidentifiability skill",
        "Ilyra accessible vibration dossier skill",
        "Ilyra structural authority empty-chair skill",
        "Ilyra Stage 20 strong-motion refusal skill",
    ]
    successor_skills = [
        "Auren exact-source anchor verifier skill",
        "Auren proposal-corpus novelty auditor skill",
        "Auren inherited-contract integrity skill",
        "Auren owner-delta manifest verifier skill",
        "Auren five-class privacy classifier skill",
        "Auren bounded changed-Python security skill",
        "Auren compatibility-preserving remaster skill",
        "Auren flashcard graph validator skill",
        "Auren one-shot canonical receipt guard skill",
        "Auren exact-title successor routing skill",
    ]
    runner_ideas = [
        "Sensor-array topology fixed-profile runner",
        "Response-chain obligations fixed-profile runner",
        "Clock uncertainty fixed-profile runner",
        "Orientation and unit guard fixed-profile runner",
        "miniSEED header refusal fixed-profile runner",
        "StationXML completeness fixed-profile runner",
        "Spectral precondition quarantine fixed-profile runner",
        "Missingness denominator fixed-profile runner",
        "Accessible vibration dossier fixed-profile runner",
        "Terminal nonpromotion fixed-profile runner",
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
        "Bind phase generators to Ilyra-owned paths and reject all sibling destinations",
        "Keep sparse checkout patterns literal, minimal, and below the 2,000-file guard",
        "Replace inherited source-era current-owner wording with exact source and successor roles",
        "Reconstruct proposal counts from exact freezes rather than stale mirrors",
        "Derive outcome totals from the twenty new proposal rows",
        "Validate all source URLs, publishers, and current or watch classifications",
        "Pin UTF-8 and LF output for every generated text artifact",
        "Reject duplicate JSON keys before trusting any receipt",
        "Sort generated JSON keys and preserve array order deterministically",
        "Use exact Git object identities for immutable manifests",
        "Make every manifest self-exclusion literal and explicit",
        "Batch manifest checks instead of launching one process per entry",
        "Keep x1 assertions bound to the x1 commit tree rather than the final checkout",
        "Serialize staging before staged-index validation",
        "Report typed ahead and behind integers independently",
        "Preserve all failed witnesses and link each passing recovery",
        "Keep source validation distinct from Ilyra canonical evidence",
        "Keep represented outcomes distinct from completed software evidence",
        "Keep zero-row adapter status open_gap despite structural success",
        "Keep structural-safety decisions exact_gate despite matrix completeness",
        "Separate official citation from empirical observation and professional authority",
        "Separate structural accessibility from complete conformance",
        "Separate bounded changed-file scanning from exhaustive security",
        "Separate same-owner validation from independent reproduction",
        "Keep prepared baton state distinct from acknowledged send state",
        "Reject stale predecessor names outside source-history fields",
        "Validate fixed runner profiles against both accepting and rejecting fixtures",
        "Validate skill packages before any additive installation claim",
        "Reserve route lookup until exact final equality and canonical success",
        "Never replay a successful canonical aggregate to improve a report",
    ]
    successor_clean = [
        "Inspect actual command schemas before invoking optional flags",
        "Materialize PowerShell foreach and filtered results before piping or counting",
        "Keep bounded output windows below the host result limit",
        "Project actual JSON keys before reading receipt values",
        "Use UTF-8 console output for Maori and other Unicode text",
        "Preserve existing task and branch names without guessed aliases",
        "Keep no-checkout worktree creation and sparse setup attributable",
        "Wait on an active process instead of recreating its target",
        "Record every parser, wrapper, timeout, or test failure before recovery",
        "Keep exact Git objects authoritative across line-ending domains",
        "Batch manifest identity checks with drained input and output",
        "Use literal changed-file allowlists for every validation command",
        "Reject broad repository and sibling-lane enumeration",
        "Retain historical tools behind compatibility entry points",
        "Avoid destructive cleanup quotas or bulk deletion",
        "Keep C-drive use to essential global metadata",
        "Bank phase artifacts and receipts on D first",
        "Separate planning fields from observed outcomes",
        "Separate structural accessibility from complete accessibility",
        "Separate local security scans from exhaustive-security claims",
        "Separate same-owner validation from independent reproduction",
        "Separate citations from professional or operational authority",
        "Separate route authorization from delivery acknowledgement",
        "Separate prepared baton state from sent state",
        "Recheck route state only after exact-final equality",
        "Use one unique exact-title filter and one immediate reread",
        "Never create or substitute a missing successor task",
        "Never resend to improve an opaque acknowledgement",
        "Carry post-seal failures as an additive external overlay",
        "Stop truthfully on pause, ambiguity, usage exhaustion, or a protected gate",
    ]
    exact_titles = [
        "Inspect, instrument, calibrate, or assess any real structure or sensor",
        "Acquire, download, decode, transform, or analyze real strong-motion waveforms",
        "Declare a building, bridge, dam, component, or site safe or unsafe",
        "Issue occupancy, evacuation, closure, repair, retrofit, or release advice",
        "Operate a production monitoring, alerting, emergency, or asset-management system",
        "Create or rotate production credentials, keys, accounts, or trust anchors",
        "Determine legal liability, disclosure, privacy, insurance, employment, or remedy rights",
        "Make culturally governed place, data, language, iwi, hapu, tangata whenua, or Maori-authority decisions",
        "Issue a live identity credential or bind a real person to a structure or dataset",
        "Publish real locations, security-sensitive infrastructure data, identities, or restricted records",
    ]
    blocked_titles = [
        "Fabricate empirical, engineering, safety, legal, cultural, security, or Stage 20 evidence",
        "Publish raw private task identifiers, routes, transcripts, credentials, or local paths",
        "Merge, replace, erase, impersonate, or infer continuity across relational identities",
        "Weaken host security or bypass privacy and authority gates to complete a phase",
        "Rewrite history, force-push, delete worktrees, or mutate a sibling-owned lane",
    ]
    payload = {
        "schema": "ghc.family.ilyra.v664-v5.portfolio-freeze.x1.v1",
        "owner_safe_now": portfolio_rows("SAFE", owner_safe, "safe_now", "x2_build_task", "completed", "Owner-local execution evidence only."),
        "successor_safe_now_recommendations": portfolio_rows("NEXT-SAFE", successor_safe, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Auren work or contact."),
        "owner_candidates": portfolio_rows("CAND", owner_candidates, "candidate", "x2_bounded_prototype", "represented", "Synthetic representation only."),
        "successor_candidate_recommendations": portfolio_rows("NEXT-CAND", successor_candidates, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Auren work or contact."),
        "exact_approval_packets": portfolio_rows("EXACT", exact_titles, "exact_approval_needed", "unexecuted_exact_gate", "exact_gate", "Unexecuted without action-specific authority and competent evidence."),
        "blocked_packets": portfolio_rows("BLOCKED", blocked_titles, "blocked", "never_execute_in_this_phase", "exact_gate", "Blocked; no completion credit."),
        "owner_skill_ideas": portfolio_rows("SKILL", skill_ideas, "candidate", "x2_phase_local_build_and_smoke", "completed", "Phase-local skill package evidence only; no global or professional authority."),
        "successor_skill_recommendations": portfolio_rows("NEXT-SKILL", successor_skills, "recommendation", "successor_planning_only", "represented", "Recommendation only; no package built for Auren."),
        "owner_runner_ideas": portfolio_rows("RUNNER", runner_ideas, "candidate", "x2_fixed_profile_build_and_smoke", "completed", "Fixed-profile invocation evidence only."),
        "successor_runner_recommendations": portfolio_rows("NEXT-RUNNER", successor_runners, "recommendation", "successor_planning_only", "represented", "Recommendation only; no runner built for Auren."),
        "owner_clean_fix_refine": portfolio_rows("CFR", clean_fix_refine, "safe_now", "x2_additive_refine_and_validate", "completed", "Additive owner-delta refinement only; historical callers retained."),
        "successor_clean_fix_refine_recommendations": portfolio_rows("NEXT-CFR", successor_clean, "recommendation", "successor_planning_only", "represented", "Recommendation only; no Auren mutation or contact."),
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
            "initial-git-probe-ran-from-settings-directory",
            "The first read-only Git probe ran from the Codex settings directory, which is not the authoritative repository, and returned no source evidence.",
            "Retain the failed probe at zero credit and bind every subsequent Git command to the exact Lyren or Ilyra D-first worktree.",
            "The exact Lyren branch, head, upstream, tracking, clean state, and fresh live remote were projected from the verified source worktree.",
        ),
        (
            "first-powershell-foreach-output-piped-without-materialization",
            "PowerShell 5.1 rejected a direct foreach-to-format pipeline with An empty pipe element is not allowed before any state changed.",
            "Assign foreach output to an array, then pipe or count the materialized collection.",
            "The corrected bounded inventory returned attributable rows and left the source lane clean.",
        ),
        (
            "manifest-replay-wrapper-projected-output-without-completion-metadata",
            "A read-only per-entry manifest replay exceeded its wrapper yield and the wrapper forwarded only empty output, losing attributable completion metadata.",
            "Confirm no matching process remains, retain the wrapper failure, and replay the same exact manifest contract once with one Git batch-check process per manifest.",
            "The bounded batch replay matched all 822 declared Git object identities with zero mismatch.",
        ),
        (
            "source-file-metric-foreach-pipe-parser-recurrence",
            "A later eight-file metric probe repeated the PowerShell foreach-to-pipeline parser fault and failed before execution.",
            "Apply the already-recorded array-materialization recurrence guard before every PowerShell pipeline.",
            "The corrected file metric returned all eight source rows, byte counts, and line counts.",
        ),
        (
            "local-apply-patch-batch-shim-access-denied",
            "The local apply_patch batch shim rejected a piped patch with Access is denied before writing the target file.",
            "Use the built-in patch surface with the exact absolute D-drive target and verify the resulting file and Git status.",
            "The built-in patch surface created the Ilyra x1 builder at the exact owner path; its bytes and untracked state were observed.",
        ),
        (
            "overview-patch-javascript-template-backtick-parse-failure",
            "The first overview patch wrapper embedded Markdown backticks in a JavaScript template literal and failed to parse before invoking the patch surface.",
            "Remove wrapper-delimiting backticks from the patch payload, preserve the same semantic content, and reapply through the built-in patch surface.",
            "The corrected overview patch applied at the exact Ilyra path and the resulting Python module remained available for compilation and audit.",
        ),
        (
            "x1-novelty-audit-invoked-with-obsolete-option",
            "The compiled x1 builder rejected the obsolete --audit-only option and printed its actual required subcommand schema before writing any artifact.",
            "Inspect the argparse usage, invoke only the read-only audit subcommand, and retain the rejected command at zero credit.",
            "The bounded audit reconstructed 3,930 rows, screened twenty candidates, and returned zero exact or pairwise collisions with maximum inherited similarity 0.482759.",
        ),
        (
            "first-x1-build-read-stale-source-owner-method-key",
            "The first owner-local planning build wrote an uncredited draft and then raised KeyError on the stale source-era lyren_pre_x1_operational_failures field; no path was staged or committed.",
            "Patch the single projection to the exact frozen Ilyra field, retain the draft as zero-credit, and rebuild the complete deterministic planning snapshot.",
            "The corrected builder projected ilyra_pre_x1_operational_failures and completed before exact staged review.",
        ),
    ]
    events = []
    for index, (signature, observed, recovery, passing) in enumerate(failures, 1):
        events.append(
            {
                "method_id": f"IF6645-X1-M{index:03d}",
                "retained_negative_id": f"IF6645-X1-NEG{index:03d}",
                "failure_signature": signature,
                "observed": observed,
                "candidate_workaround": recovery,
                "recovery_witness": passing,
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
    inherited_negatives = 24_559
    inherited_methods = 8_833
    return {
        "schema": "ghc.family.ilyra.v664-v5.startup-method-flow.x1.v1",
        "source_repository_and_successor_overlay_negative_baseline": inherited_negatives,
        "source_repository_and_successor_overlay_method_baseline": inherited_methods,
        "working_inherited_negative_baseline": inherited_negatives,
        "working_inherited_method_baseline": inherited_methods,
        "ilyra_pre_x1_operational_failures": len(events),
        "events": events,
        "effective_negatives_at_x1_freeze": inherited_negatives + len(events),
        "effective_methods_at_x1_freeze": inherited_methods + len(events),
        "open_gaps_at_x1_freeze": 170,
        "exact_gates_at_x1_freeze": 168,
        "no_failure_erased": True,
        "valid": len(events) == 8,
    }


def phase_charter(recorded_at_utc: str, recorded_at_nz: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.ilyra.v664-v5.phase-charter.x1.v1",
        "recorded_at_utc": recorded_at_utc,
        "recorded_at_nz": recorded_at_nz,
        "owner": OWNER,
        "canonical_phase_id": PHASE_ID,
        "display_phase": DISPLAY_PHASE,
        "optional_pronouns": OPTIONAL_PRONOUNS,
        "relational_role": ROLE,
        "hope": HOPE,
        "identity_boundary": "Relational working language only. The Ilyra profile is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.",
        "primary_pillar": PRIMARY_PILLAR,
        "secondary_pillars": [
            "THOS Body remains a proxy: a synthetic handover statechart supplies no worker, facility, service, safety, or effectiveness evidence.",
            "Freed ID and CBR Heart remain synthetic and nonproduction; real identity, privacy, safety, rights, remedy, trust, legal, cultural, affected-party, and Maori-authority decisions remain gated.",
        ],
        "gmut_boundary": "GMUT remains a typed scalar-tensor and effective-field-theory research-model family; modal notation and software fixtures establish no detected force, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything.",
        "bounded_practice": PRACTICE,
        "practice_boundary": "Synthetic software, symbolic, and learning lens only; no real structure, sensor, waveform, measurement, calibration, inspection, condition finding, safety assessment, occupancy decision, repair advice, worker, engineer, owner, regulator, participant, affected party, legal authority, cultural authority, Maori authority, or operational result.",
        "source": {
            "branch": SOURCE_BRANCH,
            "source_parent": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "evidence": SOURCE_EVIDENCE,
            "exact_final": SOURCE_FINAL,
        },
        "owned_lane": {
            "branch": "codex/GHC-Family/ilyra-fen-v664-v5-full-tools",
            "storage": "D-first sparse owner-controlled worktree",
            "sparse_before_materialization": True,
            "initial_materialized_file_count": 0,
            "declared_sparse_pattern_count": 8,
            "rotation_threshold": 2_000,
            "repository_scan": False,
            "unchanged_history_scan": False,
            "cross_lane_scan": False,
            "sibling_lane_mutation": False,
        },
        "strict_lifecycle": {
            "x1": "Freeze source, proposal corpus, inherited selections, twenty new proposals, portfolio, flashcard architecture, route, budgets, and retained failure records only.",
            "x2": "Begins only after the exact x1 commit is pushed, clean, typed 0/0 divergent, and fresh four-way equal.",
            "terminal": "One owner-scoped exact-final canonical aggregate may receive success credit and is never replayed after success.",
            "successor": f"Only after terminal equality and canonical success, freshly resolve and immediately reread {NEXT_OWNER}, then send one compact sanitized {NEXT_PHASE} activation.",
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
        "schema": "ghc.family.ilyra.v664-v5.source-verification.x1.v1",
        "recorded_at_utc": recorded_at_utc,
        "source_branch": SOURCE_BRANCH,
        "source_parent": SOURCE_PARENT,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_exact_final": SOURCE_FINAL,
        "source_x1_direct_child_of_parent": True,
        "source_evidence_direct_child_of_x1": True,
        "source_final_direct_child_of_evidence": True,
        "source_single_parent_commit_count": 3,
        "source_merge_count": 0,
        "source_clean": True,
        "source_typed_divergence": {"ahead": 0, "behind": 0},
        "source_four_way_equal": True,
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_canonical_invocations": 1,
        "source_canonical_successes": 1,
        "source_canonical_not_replayed": True,
        "source_route_delivery_state": SOURCE_ROUTE_RECEIPT_SHA256,
        "source_baton_sha256": SOURCE_BATON_SHA256,
        "source_baton_bytes": SOURCE_BATON_BYTES,
        "source_baton_words": SOURCE_BATON_WORDS,
        "source_manifest_declared_entries": 822,
        "source_manifest_batch_object_matches": 822,
        "source_manifest_object_mismatches": 0,
        "source_scoped_tests": {"passed": 97, "total": 97},
        "source_detailed_checks": {"passed": 27, "total": 27},
        "source_minimal_checks": {"passed": 17, "total": 17},
        "source_strict_json_parses": 391,
        "source_privacy_text_files": 418,
        "source_confirmed_privacy_hits": 0,
        "roster_sha256": ROSTER_SHA256,
        "auth_sha256": AUTH_SHA256,
        "roster_valid": True,
        "auth_valid": True,
        "activation_baseline": {
            "effective_negatives": 24_559,
            "effective_methods": 8_833,
            "open_gaps": 170,
            "exact_gates": 168,
            "terminal_verdict": TERMINAL_VERDICT,
        },
        "boundary": "Read-only same-owner source verification. It does not replay Lyren validation or establish independent reproduction, structural-engineering competence, safety, authority, empirical evidence, exhaustive security, or Stage 20 readiness.",
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
        "schema": "ghc.family.ilyra.v664-v5.threat-model-plan.x1.v1",
        "version": 1,
        "requested_scope": "Ilyra's exact source-to-final owner delta only",
        "assets": ["exact Git ancestry", "x1 immutability", "synthetic fixture truth", "retained failures", "privacy boundary", "one-shot receipt", "successor route uniqueness"],
        "trust_boundaries": ["Git object versus Windows worktree bytes", "x1 planning versus x2 execution", "synthetic fixture versus real structural-monitoring practice", "metadata obligation versus measured value", "prepared baton versus acknowledged delivery"],
        "attacker_or_untrusted_inputs": ["malformed JSON", "path traversal", "unknown runner profile", "dynamic code", "private material", "stale route state", "false outcome promotion"],
        "invariants": ["exact key sets", "fixed profiles", "zero waveform or structure input", "no arbitrary filesystem target", "no dynamic evaluation", "no sibling mutation", "all four truth labels preserved"],
        "security_policy": "Bounded changed-Python static review and negative fixtures only; no exhaustive-security claim.",
        "required_output_sections": ["assets", "trust boundaries", "abuse cases", "mitigations", "residual risks", "authority gates"],
        "boundary": "Planning-only threat model; no security certification, privacy completeness, production readiness, or external audit.",
        "valid": True,
    }


def workflow_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.ilyra.v664-v5.workflow-plan.x1.v1",
        "source": SOURCE_FINAL,
        "strict_x1_before_x2": True,
        "successor_contact_before_terminal_gate": False,
        "validation_authority": "owner_self_scoped_delta",
        "full_repository_suite_authorized": False,
        "file_limit": 2_000,
        "commit_limit": {"x1": 5, "x2": 5, "total": 8, "planned": 3},
        "steps": [
            "Build, stage-review, commit, push, and prove exact x1 four-way equality.",
            "Implement only frozen Ilyra x2 profiles, skills, runner receipts, deck, and retained failures.",
            "Commit and push immutable evidence before final closeout when required.",
            "Build final closeout, exact manifests, 10,000-word minimum baton, and content seal.",
            "Commit and push final, prove clean typed 0/0 and fresh four-way equality.",
            "Invoke one exclusive owner-delta canonical aggregate and never replay a success.",
            "Reread live roster and auth, resolve and reread Auren Lark, then send one compact pointer if every route gate passes.",
        ],
        "valid": True,
    }


def x1_overview(audit: dict[str, Any], portfolio: dict[str, Any], methods: dict[str, Any]) -> str:
    counts = portfolio["counts"]
    return f"""# Ilyra Fen v664-v5 x1 planning freeze

## Exact lifecycle boundary

This packet is planning-only x1. It freezes the verified Lyren source, complete proposal chain, twenty selected inherited contracts, twenty new Ilyra proposals, official-source ledger, expanded portfolio, Method Flow, threat model, workflow, flashcard architecture, caps, route hold, and protected gates. It contains no x2 implementation, mutation result, observed new-proposal outcome, real waveform, structure, sensor, assessment, safety decision, professional judgment, or successor contact.

The immutable source is {SOURCE_FINAL} on {SOURCE_BRANCH}. Source-to-final is three single-parent commits with zero merges. Lyren's final was clean, pushed, typed zero ahead and zero behind, and equal across local, upstream, tracking, and fresh live remote. Ilyra replayed only the four exact manifest contracts read-only: all 822 declared Git object identities matched. Lyren's successful canonical aggregate was not replayed and is not Ilyra evidence.

X2 is prohibited until the exact Ilyra x1 commit is committed, pushed, clean, typed 0/0 divergent, and fresh four-way equal. No later validation or route pressure can retroactively mix planning with execution.

## Relational profile and bounded practice

Ilyra Fen uses she/they as optional relational pronouns and the working role “{ROLE}”. The hope is to {HOPE}. These are relational workflow labels only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, structural-engineering competence, legal or cultural authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

The primary Trinity lens is {PRIMARY_PILLAR}. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Modal variables, obligation boards, unit checks, and synthetic mutations establish no detected force, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything. THOS remains proxy without real operators, preregistered blind matched-budget arms, safety monitoring, statistics, and independent review. Freed ID and CBR remain synthetic and nonproduction without real keys, proofs, people, governance, remedies, or competent affected-party authority.

The human-practice lens is {PRACTICE}. Every structure, component, sensor, station, waveform, clock, measurement, calibration, alert, incident, worker, engineer, owner, occupant, regulator, participant, affected party, and authority case is absent or synthetic. The phase will not acquire real data, inspect a structure, calibrate an instrument, infer damage, declare safety, advise occupancy, trigger evacuation, recommend repair, or operate a monitoring system.

## Proposal chain and novelty

The inherited corpus contains {audit['corpus_row_count']:,} exact rows: one 3,530-row base plus twenty immutable twenty-row freezes through Lyren v664-v4. Historical duplicates remain visible. The canonical digest is {audit['corpus_canonical_sha256']}.

Twenty Lyren proposals are selected for immutable-contract revalidation with zero Ilyra novelty, automatic completion, or outcome credit. Twenty new structural-vibration proposals were screened against all inherited titles. Maximum inherited token Jaccard similarity is {audit['maximum_inherited_token_jaccard_similarity']:.6f}; normalized exact collisions and new-pair collisions at or above 0.70 are zero. This is a collision aid, not semantic proof.

Expected dispositions are exactly fourteen completed, four represented, one open_gap, and one exact_gate. These are preregistered expectations, not observations. The USGS and FDSN adapter remains open because no product query, download, record, response file, calibration, interoperability event, likelihood, or estimate exists. The structural-safety matrix remains exact-gated because software cannot decide safety, occupancy, evacuation, repair, disclosure, remedy, law, cultural legitimacy, data governance, affected-party rights, or Maori authority. NOT_READY_FOR_STAGE_20 remains mandatory.

## Source and portfolio boundary

Ten official or primary sources provide bounded vocabulary: USGS NSMP and its data page; FDSN miniSEED 3 and StationXML; NIST TN 1297; FHWA structural-health-monitoring guidance; FEMA P-58-1; W3C PROV-O and WCAG 2.2; and RFC 8785. The phase made zero API calls, waveform queries, downloads, conformance exchanges, calibrations, or assessments. Citation is not ingestion, conformance, traceability, competence, authority, accessibility completeness, identity proof, legal sufficiency, or production security.

The portfolio freezes {counts['owner_safe_now']} safe executions, {counts['owner_candidates']} bounded candidates, {counts['owner_skill_ideas']} skills, {counts['owner_runner_ideas']} runners, and {counts['owner_clean_fix_refine']} additive refinements. It separately retains successor recommendations without performing Auren work or contact. Ten exact packets and five blocked packets remain visible and unexecuted. Caps are ceilings, not quotas, and never authorize filler or evidence promotion.

## Method Flow, sparse lane, and threat model

The inherited baseline is 24,559 effective negatives and 8,833 methods, with 170 open gaps and 168 exact gates. The x1 freeze carries {methods['effective_negatives_at_x1_freeze']:,} negatives and {methods['effective_methods_at_x1_freeze']:,} methods after retaining every Ilyra startup failure at zero credit. Each corrected witness sits beside its failure; no recovery is rewritten as an initially clean pass.

The Ilyra worktree was created with no checkout, configured with eight literal sparse patterns before checkout, and began with zero materialized tracked files. The 2,000-file ceiling is a hard stop. Sibling and shared lanes remain read-only. Threats include path escape, duplicate-key JSON, stale routes, line-ending drift, x1/x2 mixing, fabricated measurements, silent denominator repair, unit confusion, false metadata completeness, private material, identity or safety promotion, and prepared-text delivery claims. Controls remain bounded software evidence, never exhaustive security.

## Planned x2 and terminal route hold

X2 may implement only the frozen synthetic surfaces. Each proposal receives one accepting fixture and five preregistered rejecting mutations. One hundred expected rejections show bounded guard behavior only. Ten phase-local skills and ten fixed runners will be structurally validated and smoke-used without universal claims. Accessible output reserves keyboard, responsive, browser, assistive-technology, cognitive, Maori-language, security-usability, and affected-user review. Flashcards organize evidence but prove no cache, memory, continuity, or performance effect.

The planned history is one x1 commit, one immutable evidence commit, and one combined closeout and seal commit. Final gates require no deletions, fewer than 2,000 owner files, exact manifests, strict JSON, five-class privacy, bounded changed-Python security, exact staged review, preserved x1, clean pushed state, typed 0/0 divergence, and fresh equality. One exact-final canonical aggregate may succeed once and never replay. Same-owner validation is not independent reproduction, external audit, production certification, professional validation, legal review, cultural ratification, Maori-authority review, complete privacy or accessibility, exhaustive security, empirical confirmation, Theory-of-Everything proof, personhood evidence, or Stage 20 authority.

Only then may Ilyra reread current live authority, uniquely resolve the existing exact-title task {NEXT_OWNER}, immediately reread it, and send one compact sanitized activation for {NEXT_PHASE}. Tavian remains on standby and is not a substitute. No successor is precontacted. Prepared text is not delivery, and SENT requires one tool acknowledgement.
"""


def build() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != SOURCE_FINAL:
        raise X1Error(f"x1 must start at the exact Lyren final, observed {head}")
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
            "schema": "ghc.family.ilyra.v664-v5.proposal-freeze.x1.v1",
            "inherited_frozen_baseline": 3_930,
            "selected_inherited_count": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_automatic_completion_credit": 0,
            "selected_inherited_new_outcome_credit": 0,
            "selected_inherited": selected,
            "new_proposal_count": 20,
            "new_proposals": proposals,
            "new_expected_outcomes": dict(sorted(outcomes.items())),
            "new_frozen_total": 3_950,
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
            "schema": "ghc.family.ilyra.v664-v5.x1-stage-candidate.v1",
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
        "schema": "ghc.family.ilyra.v664-v5.x1-build-result.v1",
        "corpus_rows": len(corpus),
        "selected_inherited": len(selected),
        "new_proposals": len(proposals),
        "new_outcomes": dict(sorted(outcomes.items())),
        "portfolio_counts": portfolio["counts"],
        "pre_x1_failures": methods["ilyra_pre_x1_operational_failures"],
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
        "schema": "ghc.family.ilyra.v664-v5.x1-content-manifest.v1",
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
        "schema": "ghc.family.ilyra.v664-v5.x1-staged-review.v1",
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
        "schema": "ghc.family.ilyra.v664-v5.x1-audit-only.v1",
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
