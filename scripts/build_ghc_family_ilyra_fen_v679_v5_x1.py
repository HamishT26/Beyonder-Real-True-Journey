#!/usr/bin/env python3
"""Build the planning-only Ilyra Fen v679-v5 x1 packet."""

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
PHASE = "v679-v5"
DISPLAY_PHASE = "v679-v5"
BRANCH = "codex/GHC-Family/ilyra-fen-v679-v5-full-tools"
SOURCE = "9cce202db223bec1aa7c81dd98dcbd3b83c6cd29"
SOURCE_PHASE = "v679-v4"
GENERATED_AT_NZ = "2026-08-31T18:24:00+12:00"
DECLARED_CHAIN_BEFORE = 8990
DECLARED_CHAIN_AFTER = 9050
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 49130,
    "effective_methods": 50444,
    "retained_failed_witnesses": 20791,
    "bounded_passing_witnesses": 32784,
    "open_gaps": 428,
    "exact_gates": 419,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Lyren Moss v679-v4 successor-visible activation overlay at the exact source; Lyren's immutable repository seal remains unchanged and Ilyra startup failures are retained separately below."
    ),
}

NEW_TITLES = [
    "Synthetic community-observatory log namespace with every real site instrument and operator identity vacant",
    "Invented instrument-class and surrogate-device hierarchy with duplicate and orphan rejection",
    "Environmental channel vocabulary with temperature humidity pressure light and particulate values unobserved",
    "Observation-time shell preserving absent timestamps and explicit temporal uncertainty",
    "Monotonic sequence tokens separating acquisition order from civil-time interpretation under unresolved offset metadata",
    "Unit-token allowlist with unknown and incompatible unit quarantine before any conversion",
    "Calibration-placeholder grammar separating not evaluated expired unknown and externally gated states",
    "Maintenance-status lineage for invented instruments without work-order or service claim",
    "Firmware and configuration vacancy record with no device access or operational inference",
    "Sampling-interval placeholder that forbids inferred cadence when source observations are absent",
    "Sensor-response and transfer-function vacancy register without metrological conclusion",
    "Location-granularity minimizer preserving an invented zone label while withholding exact place",
    "Coordinate and elevation fields constrained to explicit null values with no geolocation inference",
    "Operator and reviewer role firewall forbidding person affiliation qualification and authority inference",
    "Environmental-context label shell without hazard conservation or collection-care conclusion",
    "Missing-reading sentinel that distinguishes absent unavailable withheld and not-applicable from numeric zero",
    "Missingness-reason vocabulary with deterministic order and no causal interpretation",
    "Out-of-range flag placeholder that cannot become risk incident alarm or intervention evidence",
    "Duplicate log-entry quarantine keyed only by synthetic digest and deterministic sequence",
    "Sequence-gap register preserving vacancy without inventing lost observations",
    "Clock-rollback detector fixture using invented counters and no real temporal claim",
    "Clock-drift uncertainty placeholder without calibration or correction authority",
    "Observation-procedure vocabulary shell separating planned described and actually performed states",
    "OGC Observations Measurements and Samples terminology crosswalk without conformance claim",
    "OGC SensorML process-component shell with every sensor actuator and process instance absent",
    "PROV-O entity activity derivation and revision graph using invented nodes only",
    "PREMIS object event rights and agent shell with events agents and rights determinations vacant",
    "DCMI title date relation provenance and access-rights crosswalk without cataloguing authority",
    "Correction supersession state machine preserving every prior synthetic assertion",
    "Retraction and invalidation nonerasure ledger retaining rejected entries at zero credit",
    "Quarantine release-state grammar requiring an absent competent-authority decision",
    "Chain-of-custody vacancy record with no custodian transfer possession or receipt claim",
    "Access disposition matrix that refuses to infer stewardship consent reuse permission or statutory status from empty fields",
    "Privacy-minimization matrix excluding names contacts coordinates device identifiers and free text",
    "Synthetic log identifier permutation oracle proving invariance under anonymous surrogate renaming",
    "RFC 8785 canonical JSON harness for fictional observatory log records",
    "RFC 6902 patch allowlist rejecting identity authority deployment and measurement promotion",
    "Normalized-LF Git-blob manifest binding owner artifacts independently of checkout newline form",
    "Content-digest graph for synthetic log correction provenance with unresolved forks retained",
    "Locale-independent deterministic ordering for channels states references and manifest paths",
    "Schema-version migration fixture preserving old fields and rejecting silent semantic coercion",
    "Bounded positive and four-mutation negative fixture family for every new proposal contract",
    "Accessible landmark heading caption and table structure for the synthetic observatory report",
    "Plain-language status glossary separating structural check availability evaluation and certification",
    "Machine-check accessibility state separated from manual and affected-user evaluation",
    "Colour-independent status token and text-label representation without visual-user validation",
    "Keyboard focus navigation and zoom behaviour represented as unverified accessibility requirements",
    "Content-addressed four-tier flashcards for owner pillar practice and instrument-log tasks",
    "Method Flow nonerasure ledger pairing each rejecting witness with bounded recovery evidence",
    "Owner-local family skill and runner validation with no global installation or production claim",
    "Verify-only twenty-five-tool receipt without package installation profile or prefix mutation",
    "Terminal handoff release interlock requiring sealed lifecycle evidence current-route confirmation and one-recipient acknowledgement",
    "Graph-shape metaphor for traceability records kept explicitly nonphysical and noncausal",
    "THOS instrument-log state-machine representation with observation publication and deployment disabled",
    "Real community-observatory participant instrument and governance evidence gap",
    "Manual keyboard screen-reader low-vision cognitive and affected-user evaluation gap",
    "Unreachable historical title inventory recorded as a bounded comparison limitation and novelty-credit stop",
    "Real measurement publication calibration release or external-action exact gate",
    "Community cultural knowledge Māori-data-governance and Māori-authority decision exact gate",
    "Terminal promotion denylist for unverified cosmology autonomy personhood and readiness assertions",
]

SOURCES = [
    {
        "source_id": "DCMI-METADATA-TERMS",
        "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
        "status": "Dublin Core Metadata Initiative current terms page checked 2026-08-31",
        "use": "title, creator, subject, description, date, language, rights, access-rights, relation, and provenance vocabulary only; no conformance claim"
    },
    {
        "source_id": "OGC-OMS-3",
        "url": "https://www.ogc.org/standards/om/",
        "status": "OGC Observations, Measurements, and Samples version 3.0 standards page checked 2026-08-31",
        "use": "observation, feature, procedure, sample, result, and metadata vocabulary only; no real observation or conformance claim"
    },
    {
        "source_id": "OGC-SENSORML",
        "url": "https://www.ogc.org/standards/sensorml/",
        "status": "OGC SensorML standards page, including versions 3.0, 2.1, and 2.0, checked 2026-08-31",
        "use": "process, component, sensor, actuator, input, output, parameter, and lineage vocabulary only; every real process instance remains absent"
    },
    {
        "source_id": "NIST-TN-1297",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297/nist-guidelines-evaluating-and-expressing-uncertainty-nist-measurement",
        "status": "NIST Technical Note 1297 official page checked 2026-08-31",
        "use": "uncertainty-component and reporting vocabulary only; zero measurements, uncertainty values, calibration conclusions, or NIST conformance claims"
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
 "no real person, participant, operator, reviewer, rights-holder, affected user, observatory, site, instrument, sensor, device, channel, log, reading, timestamp, coordinate, calibration, certificate, measurement, result, publication, release, intervention, network row, or external write",
 "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
 "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
 "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
 "no professional, observational, metrological, calibration, accessibility, engineering, preservation, ownership, attribution, consent, privacy-remedy, legal, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
    ("ILY6795-START-N001", "The first worktree-list probe incorrectly treated the Codex home as a Git repository and failed before reading any branch state.", "ILY6795-START-P001", "The exact Lyren source worktree was used for every later read-only Git probe and no repository state changed."),
    ("ILY6795-START-N002", "The first authorization-state chunk read guessed a nonexistent current-auth-permission-state filename.", "ILY6795-START-P002", "The exact skill reference inventory was enumerated and current-state.json was read in bounded chunks through EOF."),
    ("ILY6795-START-N003", "A broad external canonical-receipt search exceeded its display window without yielding an attributable exact result.", "ILY6795-START-P003", "The committed canonical implementation supplied the exact D-isolated receipt location, whose file and payload digests were then verified directly."),
    ("ILY6795-START-N004", "A read-only prior-Ilyra delta probe used an unverified historical source revision and Git rejected the invalid range.", "ILY6795-START-P004", "The prior Ilyra lifecycle was read from its exact commit log before its source-to-final delta was inspected."),
    ("ILY6795-START-N005", "The sparse worktree creation wrapper outlived its thirty-second display window after Git began preparing the new lane.", "ILY6795-START-P005", "No mutation was replayed; the exact worktree registration, branch, index lock, sparse patterns, process quiescence, clean state, and source head were observed until completion."),
    ("ILY6795-START-N006", "The first post-timeout state wrapper spent its display budget counting a transient full-index deletion projection and did not reach its process summary.", "ILY6795-START-P006", "A bounded exact gitdir and index-lock probe waited for the original sparse operation to finish, after which the lane was clean with zero inherited files materialized."),
    ("ILY6795-START-N007", "The first substantive x1 patch expected a mutually exclusive source-mapping branch where the inspected template used two independent conditions, so the patch rejected without writing.", "ILY6795-START-P007", "The exact source and reference blocks were reread and patched separately; the failed zero-write attempt remains retained at zero completion credit."),
    ("ILY6795-START-N008", "The first x1 builder invocation outlived its display window and its unretained session handle later exited without creating phase artifacts or yielding an attributable result.", "ILY6795-START-P008", "After proving the original process had exited, the phase directory remained absent, and the source head remained unchanged, one deterministic recovery invocation retained its session handle for exact outcome capture."),
    ("ILY6795-START-N009", "The retained recovery builder correctly failed closed because six proposed titles exceeded the source-bounded semantic-neighbor threshold, including one exact historical duplicate.", "ILY6795-START-P009", "Only the six rejected titles were reformulated around distinct instrument-log concerns and the semantic audit was run again; the failed proposal slate remains retained at zero novelty and completion credit."),
    ("ILY6795-START-N010", "A read-only historical-neighbor extractor assumed a rows key that the inspected proposal-freeze schemas did not contain.", "ILY6795-START-P010", "The exact JSON keys were enumerated first and the proposals array was then read without mutating any source artifact."),
    ("ILY6795-START-N011", "The first x1 test selection ran before exact staged-manifest assembly, so nine checks passed but the manifest-coverage check correctly rejected the preliminary fifteen-entry builder manifest.", "ILY6795-START-P011", "The exact x1 set was staged, the dedicated manifest assembler added the three code entries, and only the failed coverage test was selected for recovery; the nine earlier successes were not replayed."),
    ("ILY6795-START-N012", "A proposed regeneration after the test-order failure reached the x1 non-overwrite guard and was correctly refused before writing.", "ILY6795-START-P012", "The already-generated planning packet was preserved and only its retained startup ledger was extended additively before exact staged-manifest binding."),
]

OWNER_SKILLS = [
 "ghc-community-observatory-instrument-hierarchy",
 "ghc-community-observatory-log-state",
 "ghc-community-observatory-clock-ambiguity",
 "ghc-community-observatory-role-firewall",
 "ghc-community-observatory-reading-vacancy",
 "ghc-community-observatory-accessibility-status",
 "ghc-community-observatory-channel-lineage",
 "ghc-community-observatory-provenance-vacancy",
 "ghc-community-observatory-correction-chain",
 "ghc-community-observatory-privacy-minimizer",
 "ghc-community-observatory-calibration-reservation",
 "ghc-community-observatory-cultural-authority-gate",
 "ghc-community-observatory-maori-authority-gate",
 "ghc-community-observatory-json-patch-guard",
 "ghc-community-observatory-deterministic-serialization",
 "ghc-community-observatory-git-blob-receipt",
 "ghc-community-observatory-accessibility-structure",
 "ghc-community-observatory-method-nonerasure",
 "ghc-community-observatory-real-evidence-gap",
 "ghc-community-observatory-stage20-denylist"
]

SUCCESSOR_SKILLS = [
 "successor-community-observatory-context-card-intake",
 "successor-instrument-log-neighbor-audit",
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
    "ghc_family_ilyra_fen_v679_v5_contract_runner.py",
    "ghc_family_ilyra_fen_v679_v5_mutation_runner.py",
    "ghc_family_ilyra_fen_v679_v5_topology_runner.py",
    "ghc_family_ilyra_fen_v679_v5_metadata_runner.py",
    "ghc_family_ilyra_fen_v679_v5_flashcard_runner.py",
    "ghc_family_ilyra_fen_v679_v5_toolchain_runner.py",
    "ghc_family_ilyra_fen_v679_v5_privacy_runner.py",
    "ghc_family_ilyra_fen_v679_v5_accessibility_runner.py",
    "ghc_family_ilyra_fen_v679_v5_portfolio_runner.py",
    "build_ghc_family_ilyra_fen_v679_v5_report.py",
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
    source_phase = "Lyren Moss v679-v4 exact final"
    path = "docs/lyren-moss/v679-v4/x1/new-proposal-freeze.json"
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
        proposal_id = f"ILY6795-N{offset:03d}"
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
            source_ids += ["OGC-OMS-3", "OGC-SENSORML", "NIST-TN-1297", "LOC-PREMIS-3"]
        if 26 <= offset <= 45:
            source_ids += ["OGC-OMS-3", "OGC-SENSORML", "NIST-TN-1297", "LOC-PREMIS-3"]
        if offset in {22, 28, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "OGC-OMS-3"]
        if offset in {24, 25, 41, 42, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real people, sites, instruments, sensors, channels, logs, readings, timestamps, coordinates, calibrations, measurements, interventions, identity, professional, legal, cultural, affected-party, or authority claims."
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
            "task_id": f"ILY6795-{prefix}-{index:03d}",
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
            "packet_id": f"ILY6795-{prefix}-{index:03d}",
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
            "docs/ilyra-fen/v679-v5/validation/x1-manifest.json",
            "docs/ilyra-fen/v679-v5/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Lyren Moss v679-v4 exact final as HEAD")
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
            "practice_1": "synthetic community-observatory site, instrument, channel, log, reading-vacancy, clock, calibration-reservation, and provenance documentation",
            "practice_2": "synthetic structural-accessibility, correction-lineage, rights-and-authority vacancy, dispute, and reversible-handover documentation",
            "practice_3": "owner-scoped deterministic software verification with exact Git-blob evidence",
            "successor_recommendation": "synthetic community-observatory observation-package provenance reconciliation with explicit calibration, accessibility, and authority quarantine",
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
        "community-observatory-instrument-log-calibration-and-provenance-practice",
        "structural-accessibility-and-authority-vacancy-documentation-practice",
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
            "successor_phase": "v679-v6",
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

This additive owner lane begins at Lyren Moss's immutable v679-v4 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Lyren's successful owner-scoped canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Ilyra proposals. The combined 120-row instrument is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is THOS Body. The wholly synthetic learning and design lenses are community-observatory site, instrument, channel, log, reading-vacancy, clock, calibration-reservation, structural-accessibility, correction-lineage, rights-and-authority vacancy, provenance, dispute, and reversible-handover documentation, plus owner-scoped deterministic software verification. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. No real person, observatory, site, instrument, sensor, channel, log, reading, timestamp, coordinate, calibration, certificate, measurement, result, publication, intervention, rights decision, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

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
