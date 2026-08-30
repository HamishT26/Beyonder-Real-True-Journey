#!/usr/bin/env python3
"""Build the planning-only Lyren Moss v677-v5 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Lyren Moss"
OWNER_SLUG = "lyren-moss"
PHASE = "v677-v5"
DISPLAY_PHASE = "v677-v5"
BRANCH = "codex/GHC-Family/lyren-moss-v677-v5-full-tools"
SOURCE = "aca9fbd51662312c49850c773d99dab3cc55be04"
SOURCE_PHASE = "v677-v4"
GENERATED_AT_NZ = "2026-08-31T00:52:44+12:00"
DECLARED_CHAIN_BEFORE = 8030
DECLARED_CHAIN_AFTER = 8090
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 44785,
    "effective_methods": 40222,
    "retained_failed_witnesses": 16446,
    "bounded_passing_witnesses": 24476,
    "open_gaps": 380,
    "exact_gates": 371,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Vesper Arlen v677-v4 immutable repository seal at the exact source; Lyren startup failures are retained separately below."
    ),
}

NEW_TITLES = [
    "Synthetic audiovisual asset catalogue namespace without collection identity custody or service claim",
    "PBCore-style asset and instantiation separation table with every real identifier vacant",
    "Physical and digital instantiation relation graph without media ownership or availability conclusion",
    "Title subject description genre and audience field contract with fictional values only",
    "Creator contributor publisher and affiliation identity firewall without attribution",
    "Rights summary link and embedded-statement reservation without permission conclusion",
    "Media type physical format digital format and standard vocabulary vacancy without conformance claim",
    "Time start duration and end-time contradiction quarantine for invented programmes",
    "Audio essence-track channel sample-rate and bit-depth placeholders without signal measurement",
    "Video essence-track frame-rate aspect-ratio and frame-size placeholders without image inspection",
    "Caption sign-language and audio-description alternative-mode register without accessibility-complete claim",
    "Asset-level and track-level language role uncertainty ledger with no speaker inference",
    "Master mezzanine preservation and access-copy generation vocabulary without authenticity decision",
    "Shell hub reel cassette disc cylinder and file-container relation graph without handling advice",
    "Playback device machine calibration compatibility and maintenance firewall with every action disabled",
    "Drop-frame non-drop-frame timecode and frame-count disagreement quarantine without timing certification",
    "Segment part sequence ordinal and duration topology for a wholly invented programme",
    "Side programme track chapter and clip relation map with orphan and cycle rejection",
    "Mono stereo and multichannel configuration vocabulary without listening or channel verification",
    "Analog-to-digital transition lineage with every capture event operator and device vacant",
    "Checksum fixity packaging and storage vocabulary without real bytes or preservation assurance",
    "Migration transcode remux resample and caption-edit lineage without real media transformation",
    "Born-digital source and digitized-surrogate distinction without provenance or authenticity conclusion",
    "Cue-sheet log transcript shot-list and annotation privacy firewall without content attribution",
    "Names voices performances labels addresses and credits firewall without identity inference",
    "Fictional broadcast-region context compartment exposing jurisdiction and community fields only as null tokens",
    "Anonymous shelf-token and access-window schema with retention controller and deletion authority unset",
    "Catalogue intake triage review amendment and release finite-state ledger without service events",
    "Playback rewind cleaning repair digitization and disposal packet with action fields hard-disabled",
    "Mould sticky-shed vinegar warping delamination and unstable-carrier vocabulary without diagnosis",
    "Incident-language lexicon for fictional audiovisual carriers that refuses triage instruction and preservation response",
    "Reversible correction and supersession lineage for synthetic asset instantiation and track assertions",
    "Bitemporal review ledger binding fictional catalogue assertions to transaction and valid instants",
    "Duplicate asset orphan instantiation impossible track loop and dangling segment rejection contract",
    "RFC 8785 byte-canonicalization harness for invented audiovisual catalogue records",
    "Git-object newline-domain receipt binding synthetic AV metadata hashes while labeling checkout bytes noncanonical",
    "Screen-reader route grammar for asset instantiation track gap and unresolved-review headings",
    "Textual timeline waveform and spectrogram alternative with every signal observation vacant",
    "Caption transcript and audio-description status table with synchronization evaluation reserved",
    "CSS-independent magnification contrast and focus-order proxy with low-vision study reserved",
    "Comprehension-scaffolded synopsis of an invented audiovisual catalogue with evaluation vacant",
    "Field-minimization matrix for anonymous asset instantiation and track topology",
    "Contestation queue for disputed audiovisual catalogue assertions with reversible visibility states",
    "Four-tier learning-card namespace keyed by canonical payload digests for AV catalogue abstention",
    "Standards vocabulary provenance card for PBCore asset and instantiation terms with rights and authority separation",
    "Merkle-addressed catalogue correction DAG preserving retractions conflicts and replacements",
    "GMUT asset-instantiation graph analogy without physical-law or empirical promotion",
    "Metamorphic instantiation-identifier permutation oracle preserving only graph invariants",
    "Identifiability refusal register for vacant track variables and unconstrained timing parameters",
    "Catalogue-only GMUT graph sandbox with every likelihood posterior force prediction and law field uninhabited",
    "Matched-budget THOS catalogue-document protocol blueprint reserving every human arm device session and outcome",
    "THOS audiovisual-catalogue state machine with ingest playback migration and deployment routes disabled",
    "Keyless Freed ID metadata shell for anonymous audiovisual surrogates with credential fields disabled",
    "CBR appeal-and-remedy state machine for invented AV metadata with every claimant reviewer decision and authority vacant",
    "Real audiovisual archivist cataloguer engineer conservator rights-holder and affected-user evidence gap",
    "Manual browser keyboard screen-reader caption low-vision and independent-reader evaluation gap",
    "Declared-chain coverage exception register for unreachable historical proposal titles without universal novelty",
    "Real carrier inspection playback repair migration digitization release and professional-signoff exact gate",
    "Indigenous-data and taonga-record authority reservation for invented broadcast descriptions with every decision unpopulated",
    "Final-state denylist barring readiness promotion until named external validators and governing bodies supply evidence",
]

SOURCES = [
    {
        "source_id": "PBCORE-XSD-2.1",
        "url": "https://pbcore.org/xsd",
        "status": "PBCore official current-release schema page checked 2026-08-31; page identifies PBCore 2.1 as the current release",
        "use": "asset, instantiation, element-order, and audiovisual metadata vocabulary only; no conformance claim"
    },
    {
        "source_id": "PBCORE-INSTANTIATION",
        "url": "https://pbcore.org/elements/instantiation",
        "status": "PBCore official instantiation-elements page checked 2026-08-31",
        "use": "physical and digital representation, essence-track, timing, and relation vocabulary only; zero real media rows"
    },
    {
        "source_id": "LOC-AV-CARE",
        "url": "https://www.loc.gov/preservation/care/record.html",
        "status": "Library of Congress audiovisual care page checked 2026-08-31",
        "use": "carrier and handling-boundary vocabulary only; no operational instruction, diagnosis, treatment, or professional authority"
    },
    {
        "source_id": "W3C-MAUR",
        "url": "https://www.w3.org/TR/media-accessibility-reqs/",
        "status": "W3C Media Accessibility User Requirements Note checked 2026-08-31",
        "use": "captions, descriptions, transcripts, navigation, and user-needs vocabulary only; no conformance or affected-user evaluation claim"
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
 "no real person, participant, audiovisual archivist, cataloguer, engineer, conservator, custodian, owner, rights-holder, affected user, institution, collection, asset, instantiation, carrier, track, signal, image, sound, record, measurement, inspection, playback, handling, repair, migration, digitization, release, network row, or external write",
 "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
 "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
 "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
 "no professional, archival, audiovisual-cataloguing, engineering, conservation, carrier-condition, material, structural, access, hazard, repair, playback, handling, preservation, ownership, custody, attribution, copyright, privacy-remedy, legal, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
    ("LYR6775-START-N001", "The live activation message declared a baton SHA-256 that did not match the exact committed Git blob.", "LYR6775-START-P001", "The committed baton, baton-integrity record, content seal, owner manifest, and final-delta manifest independently agreed on the exact Git-blob digest; the live mismatch remains retained at zero credit and Vesper history was not rewritten."),
    ("LYR6775-START-N002", "A naive x2 manifest replay treated twenty CRLF-projected YAML checkout-byte counts as canonical mismatches.", "LYR6775-START-P002", "The predecessor contract and retained Vesper failure were reread; all 208 normalized-LF Git-blob SHA-256 values matched, while the legacy checkout-byte metadata differences retain zero conversion credit."),
    ("LYR6775-START-N003", "The first target-lane uniqueness wrapper contained an invalid nested PowerShell expression and stopped at parse time before running Git.", "LYR6775-START-P003", "A simple scalar uniqueness probe established that the Lyren target lane and branch were absent and changed no repository state."),
    ("LYR6775-START-N004", "The second combined target-lane probe exited without attributable scalar output and earned zero setup credit.", "LYR6775-START-P004", "A bounded line-oriented probe established target absence, branch absence, exact source head, clean source state, and sufficient D-drive capacity."),
    ("LYR6775-START-N005", "The first broad x1 patch failed its exact-context verification because one predecessor-phase label had already changed during namespace adaptation.", "LYR6775-START-P005", "Narrow exact-context patches and dynamically bounded marker replacements updated only the untracked Lyren x1 scaffolding."),
    ("LYR6775-START-N006", "The first manifest-contract search named a nonexistent build-prefixed x2 manifest script and returned a path error.", "LYR6775-START-P006", "A bounded filename listing identified the exact family-current manifest script, whose code and retained CRLF failure contract were then read completely."),
    ("LYR6775-START-N007", "The first recursive cleanup request for newly generated Python bytecode was rejected by command safety before execution.", "LYR6775-START-P007", "No repository byte changed; bytecode remained ignored and all later Python invocations disable bytecode writes."),
    ("LYR6775-START-N008", "A second nonrecursive bytecode cleanup request was also rejected by command safety before execution.", "LYR6775-START-P008", "Cleanup retries stopped; Git status, owner manifests, and materialization accounting exclude the ignored generated cache."),
    ("LYR6775-X1-N001", "The first source-bounded semantic audit rejected one exact historical title and ten additional titles at or above the preregistered 0.75 token-Jaccard ceiling, then stopped before writing x1 documents.", "LYR6775-X1-P001", "Only the eleven cited Lyren titles were rewritten with narrower audiovisual-catalogue semantics; every unflagged proposal and the immutable source remained unchanged before the isolated audit retry."),
    ("LYR6775-X1-N002", "The first eleven-title patch failed exact-context verification on the final trailing-comma line and changed no file.", "LYR6775-X1-P002", "A narrower exact-context patch changed only the eleven quarantined Lyren titles before the isolated audit retry."),
    ("LYR6775-X1-N003", "The second source-bounded audit cleared ten rewritten collisions but retained the terminal-gate title exactly at the 0.75 quarantine threshold.", "LYR6775-X1-P003", "Only that terminal-gate title was rewritten as a distinct readiness denylist before one further isolated audit retry."),
    ("LYR6775-X1-N004", "The third audit exposed an unintended sixty-first title, which shifted the rights gate into proposal 060 and left it exactly at the 0.75 quarantine threshold.", "LYR6775-X1-P004", "The extra planning-only practice-boundary row was removed, restoring exactly sixty titles with rows 055 through 057 open and rows 058 through 060 exact-gated."),
    ("LYR6775-X1-N005", "The fourth audit confirmed the sixty-row partition but retained the audiovisual rights and taonga authority gate exactly at the 0.75 semantic threshold.", "LYR6775-X1-P005", "Only proposal 059 was rewritten as an unpopulated broadcast-description authority reservation before the next isolated audit retry."),
]

OWNER_SKILLS = [
 "ghc-audiovisual-asset-instantiation-split",
 "ghc-audiovisual-track-topology",
 "ghc-audiovisual-timecode-gap-quarantine",
 "ghc-audiovisual-alternative-mode-firewall",
 "ghc-audiovisual-format-vacancy",
 "ghc-audiovisual-condition-cue-firewall",
 "ghc-audiovisual-derivative-lineage",
 "ghc-audiovisual-location-vacancy",
 "ghc-audiovisual-role-separation",
 "ghc-audiovisual-correction-chain",
 "ghc-audiovisual-privacy-filter",
 "ghc-audiovisual-rights-reservation",
 "ghc-audiovisual-cultural-authority-gate",
 "ghc-audiovisual-maori-authority-gate",
 "ghc-audiovisual-content-domain",
 "ghc-audiovisual-json-patch-guard",
 "ghc-audiovisual-deterministic-serialization",
 "ghc-audiovisual-accessibility-structure",
 "ghc-audiovisual-real-evidence-gap",
 "ghc-audiovisual-professional-authority-gate"
]

SUCCESSOR_SKILLS = [
 "successor-audiovisual-context-card-intake",
 "successor-asset-instantiation-neighbor-audit",
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
    "ghc_family_lyren_moss_v677_v5_contract_runner.py",
    "ghc_family_lyren_moss_v677_v5_mutation_runner.py",
    "ghc_family_lyren_moss_v677_v5_topology_runner.py",
    "ghc_family_lyren_moss_v677_v5_metadata_runner.py",
    "ghc_family_lyren_moss_v677_v5_flashcard_runner.py",
    "ghc_family_lyren_moss_v677_v5_toolchain_runner.py",
    "ghc_family_lyren_moss_v677_v5_privacy_runner.py",
    "ghc_family_lyren_moss_v677_v5_accessibility_runner.py",
    "ghc_family_lyren_moss_v677_v5_portfolio_runner.py",
    "build_ghc_family_lyren_moss_v677_v5_report.py",
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
    source_phase = "Vesper Arlen v677-v4 exact final"
    path = "docs/vesper-arlen/v677-v4/x1/new-proposal-freeze.json"
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
                "lyren_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"LYR6775-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785", "RFC-6902"]
        if offset <= 25:
            source_ids += ["PBCORE-XSD-2.1", "PBCORE-INSTANTIATION", "LOC-PREMIS-3", "LOC-AV-CARE"]
        if 26 <= offset <= 45:
            source_ids += ["PBCORE-XSD-2.1", "PBCORE-INSTANTIATION", "LOC-PREMIS-3", "W3C-MAUR"]
        if offset in {22, 28, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-MAUR"]
        if offset in {24, 25, 41, 42, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real audiovisual assets, instantiations, carriers, tracks, signals, images, sound, playback, inspection, handling, treatment, identity, rights, professional, legal, cultural, or authority claims."
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
            "task_id": f"LYR6775-{prefix}-{index:03d}",
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
            "packet_id": f"LYR6775-{prefix}-{index:03d}",
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
            "docs/lyren-moss/v677-v5/validation/x1-manifest.json",
            "docs/lyren-moss/v677-v5/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Vesper Arlen v677-v4 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Lyren x1 already exists; no overwrite permitted")

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
            "new_lyren_proposals": len(rows),
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
            "primary_pillar": "Freed ID and CBR Heart",
            "practice_1": "synthetic audiovisual asset, instantiation, track, timing, derivative, and provenance catalogue metadata",
            "practice_2": "synthetic captions, transcript, description, navigation, correction, and abstention documentation",
            "successor_recommendation": "synthetic community-radio programme catalogue accessibility analysis",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Ilyra Fen", "SCAND"),
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Ilyra Fen", "SCFR"),
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
        "audiovisual-asset-instantiation-provenance-practice",
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
            "successor": "Ilyra Fen",
            "successor_phase": "v677-v6",
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
        f"""# Lyren Moss {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Vesper Arlen's immutable v677-v4 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Vesper's successful owner-scoped canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Lyren proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is Freed ID and CBR Heart. The wholly synthetic learning and design lenses are audiovisual asset, instantiation, track, timing, derivative, and provenance catalogue metadata, together with captions, transcript, description, navigation, correction, and abstention documentation. GMUT Mind and THOS Body remain explicit and protected. No real person, collection, asset, instantiation, carrier, track, signal, image, sound, measurement, inspection, playback, handling, repair, migration, digitization, custody action, rights decision, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 Ilyra candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

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
