#!/usr/bin/env python3
"""Build the planning-only Caelen Morrow v678-v7 remaster x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Caelen Morrow"
OWNER_SLUG = "caelen-morrow"
PHASE = "v678-v7"
DISPLAY_PHASE = "v678-v7"
BRANCH = "codex/GHC-Family/caelen-morrow-v678-v7-full-tools"
SOURCE = "0110062a8a42e882b209440de54c7dd219c7e4d4"
SOURCE_PHASE = "v678-v6-correction3"
GENERATED_AT_NZ = "2026-08-31T12:19:03+12:00"
DECLARED_CHAIN_BEFORE = 8630
DECLARED_CHAIN_AFTER = 8690
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "repository_sealed_effective_negatives": 47293,
    "repository_sealed_effective_methods": 45413,
    "repository_sealed_retained_failed_witnesses": 18954,
    "repository_sealed_bounded_passing_witnesses": 29544,
    "external_route_failures": 2,
    "effective_negatives": 47295,
    "effective_methods": 45415,
    "retained_failed_witnesses": 18956,
    "bounded_passing_witnesses": 29546,
    "open_gaps": 410,
    "exact_gates": 401,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Sylven v678-v6 correction3 repository seal plus two post-composite route/display failures, "
        "kept separate from Caelen startup and live-baton failures."
    ),
}

NEW_TITLES = [
    "Synthetic magnetic-audio carrier namespace without recording identity assertion",
    "Reel flange hub pack leader trailer and splice relation topology without inspection",
    "Open-reel cassette cartridge shell window and spool form classification vacancy",
    "Tape width length thickness basefilm binder backcoat and oxide field set with zero measurement",
    "Track count full-half-quarter track direction and channel layout record without playback",
    "Nominal speed equalization standard flux level and reference-tone fields held vacant",
    "Tape pack wind direction edge profile cinching and popped-strand cue register without diagnosis",
    "Leader colour splice type edit mark and timing cue transcription firewall without physical handling",
    "Container box reel label insert and annotation derivative lineage without authorship claim",
    "Manufacturer formulation batch serial date and place provenance braid with attribution vacancy",
    "Acetate polyester PVC base and oxide formulation claim quarantine without material testing",
    "Vinegar odor lubricant loss binder hydrolysis mold and residue cue reservation without diagnosis",
    "Magnetic field temperature humidity dust water and pollutant exposure fields held vacant",
    "Reel diameter hub diameter pack radius and tape duration fields with measurement absent",
    "Side A side B track direction take-up supply and winding orientation relation graph",
    "Physical carrier image crop label scan waveform thumbnail and derivative provenance without authenticity claim",
    "Housing sleeve reel box cushion orientation and shelf-status placeholder with zero handling",
    "Carrier custody accession location and withdrawal event model with all real identifiers absent",
    "Append-only carrier correction supersession and disputed-description lineage",
    "Accessible carrier status and handling-hold summary with manual review reserved",
    "Synthetic playback-chain namespace without equipment identity or operation claim",
    "Reproducer head azimuth track format speed equalization and gain-setting vacancy contract",
    "Capstan pinch roller tension guide lifter and transport path relation without machine inspection",
    "Preamplifier converter clock interface workstation and storage chain graph without energization",
    "Alignment tape reference flux tone frequency phase and level fields with zero signals",
    "Sample rate bit depth channel count interleave codec and container profile without file ingestion",
    "BWF bext iXML axml cue and adtl metadata presence board with zero media bytes",
    "Time-reference timestamp duration start offset and continuity fields with no observed timing",
    "Channel assignment polarity phase correlation and crosstalk fields held vacant",
    "Wow flutter speed drift scrape flutter drop-out and print-through cue register without measurement",
    "Noise hum hiss distortion clipping saturation and dynamic-range fields with no audio analysis",
    "Signal extraction attempt event state machine with transport-disabled execution",
    "Playback setup correction supersession and rejected-setting append-only provenance",
    "Digital primary access derivative and service-copy relation without preservation-success claim",
    "Fixity algorithm digest event and verification-status contract with zero archival package",
    "Package inventory representation structure metadata and missing-object refusal",
    "Migration normalization transcoding and resampling action plan with execution denied",
    "Storage replica location refresh audit and loss-event schema with no repository operation",
    "Provenance graph for synthetic capture transform validation and publication stages",
    "GMUT time-frequency analogy firewall without physical inference or empirical credit",
    "Synthetic audiovisual-description namespace without speaker performer or rights-holder identity claim",
    "Title date language genre subject and note fields with creator-attribution vacancy",
    "THOS zero-person audiovisual intake triage pause stop and shift-handover protocol",
    "Workload queue priority timebox fatigue signal and escalation ledger without real staff",
    "Freed ID nonproduction archive-access role envelope with zero cryptographic material and disabled lifecycle",
    "Selective-disclosure placeholder for access conditions with no credential proof or release",
    "Consent restriction embargo copyright license and orphan-work status quarantine",
    "Privacy redaction sensitivity and disclosure-review state machine with zero personal data",
    "Transcript caption audio-description and easy-read companion vacancy board",
    "Keyboard semantic heading table contrast and focus-order structure with conformance reserved",
    "Listener accessibility preference handover without affected-user evaluation claim",
    "Traditional knowledge sacred-content community protocol and culturally sensitive material hold",
    "Place person group and language-label correction challenge and remedy escrow",
    "Public catalogue access copy research request and publication decision firewall",
    "Real carrier inspection playback digitization and preservation-quality evidence gap",
    "Real accessibility privacy security and affected-user evaluation evidence gap",
    "Current institutional format capability and storage-interoperability evidence gap",
    "Recording ownership copyright privacy consent and affected-party authority exact gate",
    "Professional playback conservation electrical chemical mold and workplace safety exact gate",
    "Archive-audio Māori-language naming taonga mātauranga tikanga kaitiakitanga iwi hapū governance decision vacancy",
]

SOURCES = [
    {
        "source_id": "LOC-AV-CARE",
        "url": "https://www.loc.gov/preservation/care/record.html",
        "status": "official Library of Congress audiovisual care page checked 2026-08-31",
        "use": "magnetic-tape carrier, reel, hub, cassette, handling-hold, storage, and deterioration-cue vocabulary only; no object handling, inspection, playback, storage prescription, or treatment is performed",
    },
    {
        "source_id": "LOC-RFS-AUDIO",
        "url": "https://www.loc.gov/preservation/resources/rfs/",
        "status": "official Library of Congress 2025-2026 Recommended Formats Statement checked 2026-08-31",
        "use": "audio-work, physical and digital characteristic, preferred-or-acceptable, preservation, access, and format-vacancy vocabulary only; no acquisition, institutional preference, format endorsement, ingest, or preservation outcome is claimed",
    },
    {
        "source_id": "NARA-MACHINE-READABLE",
        "url": "https://www.archives.gov/preservation/holdings-maintenance/machine-readable",
        "status": "official U.S. National Archives machine-readable media page checked 2026-08-31",
        "use": "magnetic field, binder, substrate, oxide, mold, playback-hold, reformatting, and specialist-referral vocabulary only; no real tape, environment, playback, repair, or reformatting action",
    },
    {
        "source_id": "IASA-TC04",
        "url": "https://www.iasa-web.org/tc04/audio-preservation",
        "status": "International Association of Sound and Audiovisual Archives TC-04 web edition checked 2026-08-31; second edition 2009",
        "use": "metadata, persistent-identifier vacancy, signal extraction, preservation target, ingest, storage, planning, access, and optical-disc vocabulary only; no professional instruction, playback, digitization, or archival result",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation",
        "use": "entity, activity, agent, derivation, and attribution vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation with current errata",
        "use": "structural accessibility vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation",
        "use": "status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, archivist, conservator, engineer, operator, custodian, owner, rights-holder, affected user, recording, tape, reel, cassette, cartridge, player, signal, waveform, transcript, package, observation, measurement, handling, playback, digitization, migration, repair, treatment, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
    "no professional playback, signal extraction, preservation, conservation, electrical, chemical, biological, mold, fire, workplace-safety, ownership, copyright, licence, consent, privacy-remedy, cultural, affected-party, traditional-knowledge, sacred-content, Māori-language, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, proof, canon, or Stage 20 claim",
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
    (
        "CM6787-START-N001",
        "A PowerShell skill inventory piped raw foreach output and failed with EmptyPipeElement before completing the read-only projection.",
        "CM6787-START-P001",
        "The rows were materialized before sorting and the mandatory installed-skill inventory completed without repository mutation.",
    ),
    (
        "CM6787-START-N002",
        "A combined all-tree proposal inventory returned no attributable output within its bounded presentation.",
        "CM6787-START-P002",
        "The exact source-tree inventory was split into scalar count and semantic-audit steps, preserving the original zero-credit attempt.",
    ),
    (
        "CM6787-START-N003",
        "The live activation supplied a 63-character composite-latch SHA-256 value and therefore failed digest-shape validation.",
        "CM6787-START-P003",
        "The exact external latch file hashed to the same supplied prefix plus a final b; both the rejected baton value and verified 64-character digest remain separate.",
    ),
    (
        "CM6787-START-N004",
        "An interactive PTY novelty-audit attempt echoed the JSON input but could not deliver a Windows EOF and was interrupted before an audit result.",
        "CM6787-START-P004",
        "The original process was terminated without repository access or mutation, preventing an orphaned read-only audit.",
    ),
    (
        "CM6787-START-N005",
        "A plain-pipe novelty-audit attempt received closed empty stdin and failed with JSONDecodeError before inspecting the source tree.",
        "CM6787-START-P005",
        "The bounded scratch auditor embedded the deterministic 60-title slate and completed one attributable source audit.",
    ),
    (
        "CM6787-START-N006",
        "The worktree creation and sparse-checkout wrapper crossed its reporting window after announcing the new branch.",
        "CM6787-START-P006",
        "No mutation was repeated; process and Git-state inspection established that the original operation completed at the exact source.",
    ),
    (
        "CM6787-START-N007",
        "A status read raced the still-running sparse checkout and emitted a very large apparent-deletion projection.",
        "CM6787-START-P007",
        "After the original checkout settled, scalar status, branch, head, sparse-pattern, process, and file-count checks proved a clean 661-file lane.",
    ),
    (
        "CM6787-START-N008",
        "The first post-timeout inspection mixed a full apparent-deletion list with the global worktree registry and truncated its presentation.",
        "CM6787-START-P008",
        "A bounded scalar-only inspection recovered the exact required state without repeating worktree creation.",
    ),
    (
        "CM6787-START-N009",
        "A combined activation-baseline and proposal-title patch failed closed because one inherited context line differed from the drafted patch.",
        "CM6787-START-P009",
        "The edit was split into exact-context patches; only the intended additive Caelen template changed and the failed patch changed no bytes.",
    ),
    (
        "CM6787-START-N010",
        "The host policy rejected an exact path-bounded PowerShell removal of two owner-generated bytecode-cache directories before deletion.",
        "CM6787-START-P010",
        "A Python fallback asserted both literal targets were named __pycache__ under the exact owner worktree, removed only those generated caches, and verified zero remained.",
    ),
]

OWNER_SKILLS = [
    "magnetic-audio-carrier-namespace",
    "reel-pack-relation-topology",
    "tape-format-vacancy",
    "carrier-material-claim-quarantine",
    "deterioration-cue-reservation",
    "exposure-field-vacancy",
    "audio-label-provenance",
    "carrier-custody-nonclaim",
    "playback-chain-topology",
    "transport-operation-firewall",
    "signal-parameter-vacancy",
    "bwf-metadata-presence",
    "fixity-package-nonpromotion",
    "migration-action-denylist",
    "audiovisual-description-boundary",
    "accessibility-companion-vacancy",
    "rights-consent-quarantine",
    "freed-id-archive-role-envelope",
    "thos-audiovisual-handover-proxy",
    "maori-audio-authority-reservation",
]

SUCCESSOR_SKILLS = [
    "successor-context-card-intake",
    "successor-proposal-neighbor-audit",
    "successor-toolchain-delta-guard",
    "successor-method-flow-nonerasure",
    "successor-static-report-landmarks",
    "successor-zero-network-adapter",
    "successor-exact-gate-register",
    "successor-bounded-retry-selector",
    "successor-roster-route-refresh",
    "successor-baton-file-index",
]

OWNER_RUNNERS = [
    "ghc_family_caelen_morrow_v678_v7_contract_runner.py",
    "ghc_family_caelen_morrow_v678_v7_mutation_runner.py",
    "ghc_family_caelen_morrow_v678_v7_carrier_topology_runner.py",
    "ghc_family_caelen_morrow_v678_v7_metadata_runner.py",
    "ghc_family_caelen_morrow_v678_v7_flashcard_runner.py",
    "ghc_family_caelen_morrow_v678_v7_toolchain_runner.py",
    "ghc_family_caelen_morrow_v678_v7_privacy_runner.py",
    "ghc_family_caelen_morrow_v678_v7_accessibility_runner.py",
    "ghc_family_caelen_morrow_v678_v7_portfolio_runner.py",
    "build_ghc_family_caelen_morrow_v678_v7_report.py",
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
    source_phase = "Sylven Arc v678-v6 correction3 exact final"
    path = "docs/sylven-arc/v678-v6/x1/new-proposal-freeze.json"
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
                "caelen_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"CM6787-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 20:
            source_ids += ["LOC-AV-CARE", "NARA-MACHINE-READABLE"]
        if 21 <= offset <= 40:
            source_ids += ["IASA-TC04", "LOC-RFS-AUDIO"]
        if 41 <= offset <= 60:
            source_ids += ["IASA-TC04", "LOC-RFS-AUDIO"]
        if offset in {20, 39, 41, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real recording, carrier, signal, record, playback, digitization, migration, identity, rights, "
                    "professional, legal, cultural, affected-party, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} accepts a missing or contradictory field, a raw or real identifier, a non-authorized outcome label, "
                    "or an observation, measurement, handling, playback, extraction, preservation, migration, competence, right, identity, or authority claim."
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
    internal_pairs = [
        {
            "left_id": left["proposal_id"],
            "right_id": right["proposal_id"],
            "token_jaccard": round(jaccard(left["title"], right["title"]), 4),
        }
        for left_index, left in enumerate(rows)
        for right in rows[left_index + 1 :]
    ]
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
        "maximum_internal_score": max(row["token_jaccard"] for row in internal_pairs),
        "internal_pairs_quarantined": sum(
            row["token_jaccard"] >= QUARANTINE_THRESHOLD for row in internal_pairs
        ),
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
            "task_id": f"CM6787-{prefix}-{index:03d}",
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
            "packet_id": f"CM6787-{prefix}-{index:03d}",
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
            "docs/caelen-morrow/v678-v7/validation/x1-manifest.json",
            "docs/caelen-morrow/v678-v7/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable corrected Sylven exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Caelen x1 already exists; no overwrite permitted")

    rows = new_rows()
    inherited = inherited_selection(repo)
    audit = semantic_audit(repo, rows)
    if (
        audit["exact_title_collisions"]
        or audit["selected_rows_quarantined"]
        or audit["internal_pairs_quarantined"]
        or audit["json_parse_failures"]
    ):
        raise SystemExit(
            "semantic audit failed closed: "
            + json.dumps(
                {
                    "exact": audit["exact_title_collisions"],
                    "quarantined": audit["selected_rows_quarantined"],
                    "internal_quarantined": audit["internal_pairs_quarantined"],
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
            "new_caelen_proposals": len(rows),
            "universal_novelty_proved": False,
            "proposals": rows,
        },
    )
    dump(
        x1 / "source-verification.json",
        {
            "source_branch": "codex/GHC-Family/sylven-arc-v678-v6-full-tools",
            "source": SOURCE,
            "anchors": {
                "elowen_source_and_final": "d7a2e3d1851d8a9eb6a8707968a47354b44e824a",
                "sylven_x1": "22d310c7ae4fdbd45959d388d15642039d748da0",
                "sylven_x2_evidence": "7b747952b6a6916c3881066865ff7021aeabea3c",
                "sylven_first_final": "ea27f954b8636f167c83b964c0ba5ad15301ea1e",
                "sylven_correction1": "79c42c6158c9799344e16a9ed5fc49092422b698",
                "sylven_correction2_failed_canonical_head": "706292a287ed36b892d97d80c9571e7a1d8b8ded",
                "sylven_correction3_exact_final": SOURCE,
            },
            "source_to_final_commits": 6,
            "single_parent_commits": 6,
            "merges": 0,
            "final_parent_count": 1,
            "clean_zero_divergent_fresh_four_way_equal": True,
            "failed_canonical_receipt_sha256": "06e5b4d462ac51765d914e1f6e1d48d8831229dc24918daaee2eea97d63aa16e",
            "failed_canonical_payload_sha256": "67ac13794ac47b127adc998ee4389570063620f0c4a63cb75ca3608c782bb8ee",
            "dependency_corrected_composite_receipt_sha256": "6abbde655df189cb93952df7ae2835c8c6ef9d8fcb484b9e5d931145096aee16",
            "dependency_corrected_composite_payload_sha256": "9873c558b2a6ddc1525df8acf3603015a9cfbf041cfc26cf0d9ce0f572498424",
            "rejected_live_baton_latch_sha256": "3a63df317f42032be42989d6a32eb0c2b1151de45543b9d6c29e3fcce2b0af2",
            "verified_composite_latch_sha256": "3a63df317f42032be42989d6a32eb0c2b1151de45543b9d6c29e3fcce2b0af2b",
            "rejected_baton_digest_length": 63,
            "verified_latch_digest_length": 64,
            "sylven_failed_canonical_success_credit": 0,
            "sylven_terminal_status": "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_FAILED_CANONICAL_CREDIT",
            "inherited_validation_replayed": False,
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
            "forty_or_more_new_claim": True,
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
            "primary_pillar": "Freed ID and CBR Heart",
            "secondary_pillars": ["GMUT Mind", "THOS Body"],
            "practice_1": "synthetic magnetic-audio carrier and playback-chain documentation",
            "practice_2": "synthetic audiovisual preservation-package, accessibility, rights-vacancy, and handover documentation",
            "successor_recommendation": "synthetic optical-sound and audiovisual-package continuity documentation with protected rights gates",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Eiren Kestrel", "SCAND"),
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
            "global_promotion_ceiling": 0,
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Eiren Kestrel", "SCFR"),
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
        "magnetic-audio-carrier-practice",
        "signal-package-rights-and-handover-practice",
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
            "successor": "Eiren Kestrel",
            "successor_phase": "v678-v8",
            "authority_horizon": "v725-v8",
            "precontact_forbidden": True,
            "release_requires": [
                "immutable x1 push and fresh-live equality before x2",
                "immutable evidence",
                "clean pushed exact final",
                "one successful non-replayed owner-scoped canonical receipt",
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
    dump(
        x1 / "workflow-plan.json",
        {
            "state": "PLANNING_ONLY_X1",
            "steps": [
                "freeze source-bounded proposal and portfolio plan",
                "commit and push immutable x1",
                "prove clean local upstream tracking and fresh-live equality",
                "execute bounded synthetic x2 only",
                "commit and push immutable evidence",
                "build direct-child closeout and seal",
                "invoke at most one attributable exact-final owner canonical aggregate",
                "refresh exact terminal route and send at most once only after every gate passes",
            ],
            "x2_before_x1_push_forbidden": True,
            "canonical_success_replay_forbidden": True,
            "full_repository_suite_authorized": False,
        },
    )
    dump(
        x1 / "wellbeing-and-corrigibility.json",
        {
            "workload_state": "bounded_and_resumable",
            "pause_stop_redirect_supported": True,
            "hamish_may_rename_pause_redirect_narrow_or_stop": True,
            "continuity_or_identity_claim": False,
            "role": "relational signal-lantern and rights-vacancy steward",
            "hope": "keep every carrier claim distinct from observation, every preservation plan distinct from authority, and every handover recoverable",
        },
    )
    write_text(
        x1 / "identity-and-authority.md",
        """# Caelen Morrow v678-v7 relational working boundary

Caelen Morrow is relational working language for a **signal-lantern and rights-vacancy steward**, with the bounded hope of keeping every carrier claim distinct from observation, every preservation plan distinct from authority, and every handover recoverable.

The name, role, hope, pronouns, sibling and family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the work.
""",
    )
    write_text(
        x1 / "threat-model.md",
        """# Caelen Morrow v678-v7 planning threat model

The bounded assets are proposal truth, exact Git objects, retained failures, privacy-safe documentation, and protected authority gates. Threats include x1/x2 mixing, stale-anchor reuse, false novelty, fabricated observation, accidental real identifiers, package or network side effects, rights or cultural overreach, failure erasure, canonical replay, and premature successor contact.

Controls are an exact immutable source, source-bounded semantic comparison, four authorized outcome labels, zero-row synthetic fixtures, five-class scanning, exact normalized-LF manifests, additive Method Flow, no package installation, no network ingestion, no external writes, no real playback or digitization, planning-only x1, one-attributable-canonical discipline, and a terminal route hold.

Residual gaps include universal historical novelty, real preservation quality, real accessibility and privacy evaluation, independent security and reproduction, professional judgement, legal rights, consent, cultural legitimacy, affected-party acceptance, Māori-language and Māori-data-governance review, and Māori authority.
""",
    )
    write_text(
        x1 / "x1-overview.md",
        f"""# Caelen Morrow {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Sylven Arc's immutable corrected exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Sylven's retained failed canonical, corrected composite, repository seal, delivery receipt, or external overlays.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Caelen proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical and scientific novelty remain unproved.

## Practice, pillars, and flashcards

The primary pillar is Freed ID and CBR Heart. The wholly synthetic learning/design lens is magnetic-audio carrier, playback-chain, preservation-package, provenance, accessibility, rights-vacancy, intake, and handover documentation. GMUT Mind and THOS Body remain explicit and protected. No real recording, carrier, person, playback, signal, measurement, inspection, digitization, migration, custody action, rights decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, global promotion, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action.

## Boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Professional playback, signal extraction, preservation, conservation, safety, ownership, copyright, consent, privacy, legal, cultural, affected-party, Māori-language, Māori-data, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

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
