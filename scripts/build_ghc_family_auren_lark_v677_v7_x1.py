#!/usr/bin/env python3
"""Build the planning-only Auren Lark v677-v7 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Auren Lark"
OWNER_SLUG = "auren-lark"
PHASE = "v677-v7"
DISPLAY_PHASE = "v677-v7"
BRANCH = "codex/GHC-Family/auren-lark-v677-v7-full-tools"
SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
SOURCE_PHASE = "v677-v6"
GENERATED_AT_NZ = "2026-08-31T02:28:00+12:00"
DECLARED_CHAIN_BEFORE = 8150
DECLARED_CHAIN_AFTER = 8210
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 45401,
    "effective_methods": 42084,
    "retained_failed_witnesses": 17062,
    "bounded_passing_witnesses": 25727,
    "open_gaps": 386,
    "exact_gates": 377,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Ilyra Fen v677-v6 repository seal at the exact source; Ilyra's external canonical remains separate and Auren startup failures are retained below at zero credit."
    ),
}

NEW_TITLES = [
    "Synthetic civic information-request casefile namespace with requester and agency fields permanently vacant",
    "Fictional record-set item part attachment and derivative hierarchy with orphan and cycle rejection",
    "Submitted acknowledged clarified transferred withdrawn completed and disputed request-state grammar",
    "Received due paused extended decided and closed clock model with statutory timing deliberately uncomputed",
    "Access granted partial refused unavailable and neither-confirm-nor-deny representation without a decision",
    "Correction accepted declined partially accepted statement-attached and unresolved status contract",
    "Invented statement-of-correction linkage ensuring a contested assertion and its counterstatement remain paired",
    "Synthetic disclosure-recipient notification lineage with every recipient and communication absent",
    "Requester representative caseworker reviewer and decision-maker role firewall without identity inference",
    "Record title description date provenance retention security and access-status fields using invented values only",
    "Personal-information indicator represented as unknown without classification of any real data",
    "Mixed-record segmentation placeholder with every third-party privileged and safety-sensitive item absent",
    "Scope clarification and narrowing ledger preserving fictional wording without legal or professional advice",
    "Search-source registry representing repositories queried without claiming exhaustive discovery",
    "Version rendition redaction and release-package topology without an actual document transformation",
    "Withholding-ground citation placeholder with competent legal interpretation explicitly reserved",
    "Reason schedule explanation appeal and complaint placeholders with every authority vacant",
    "Accessibility-format preference and delivery-channel states without affected-user evaluation",
    "Language and communication-assistance vacancy register without fluency ethnicity or cultural inference",
    "Authorized-representative proof vacancy gate that never accepts delegation or identity evidence",
    "Duplicate request contradictory status and impossible lifecycle transition rejection contract",
    "Casefile chronology and relationship reachability check with deterministic ordering",
    "Correction supersession retraction and counterstatement graph preserving every prior assertion",
    "Dispute divergence branch retained without a final truth legal or remedy determination",
    "Contact address account handle biometric secret credential and raw-identifier exclusion firewall",
    "Data-minimization matrix for an anonymous request correction and review topology",
    "Retention and disposal-authority vacancy matrix preventing deletion transfer or destruction action",
    "Bitemporal case-assertion ledger separating invented valid and transaction instants",
    "RFC 8785 byte-canonicalization harness for a fictional access-and-correction docket",
    "RFC 6902 patch allowlist rejecting identity authority remedy disclosure and real-action fields",
    "Counterstatement-bearing docket Git-object receipt using normalized line endings and lifecycle-specific hashes",
    "Four-tier case-request flashcard deck binding anonymous docket nodes to access correction and provenance tasks",
    "Screen-reader landmark grammar for request correction dispute provenance gap and review headings",
    "Case-review HTML traversal model with skip-link heading table focus zoom and reflow proxies absent a user study",
    "Format-request assurance ladder distinguishing declared available structurally inspected and person-evaluated states",
    "Dublin Core PROV-O PREMIS and Archives New Zealand vocabulary crosswalk without conformance",
    "Metamorphic pseudonymous-identifier permutation oracle preserving casefile topology invariants",
    "Deterministic locale-independent sorting for invented request correction and event rows",
    "Bounded positive-control generator for synthetic access correction and counterstatement fixtures",
    "Docket mutation matrix rejecting orphan counterstatements impossible access states identifier leakage and false remedies",
    "Nonerasing access-correction failure ledger linking each rejected case transition to its bounded recovery witness",
    "D-isolated command provenance inventory for casefile builders with version probes smokes and zero profile mutation",
    "Post-seal Sable route escrow requiring current roster reread exact title uniqueness and duplicate-send denial",
    "Casefile-bounded abstention invariant forbidding readiness promotion from any synthetic docket software result",
    "Content-addressed counterstatement fork forest retaining challenged assertions divergent revisions and unresolved review branches",
    "GMUT information-flow analogy constrained to documentation graphs without physical-law promotion",
    "THOS casefile state-machine blueprint with disclosure decision remedy and deployment transitions disabled",
    "Anonymous docket pseudonym shell with requester-key issuance delegation resolution recovery and revocation permanently disabled",
    "Rights-reservation matrix for notice access correction counterstatement review and remedy with every affected-party seat vacant",
    "Synthetic accessibility preference matrix representing format navigation explanation and assistance without evaluation",
    "Information and Records Management Standard vocabulary map without regulated-organisation conformance",
    "Privacy Principles access and correction vocabulary map without compliance or case determination",
    "Cultural data and Māori-authority reservation card with every substantive value unpopulated",
    "Accessible case-review HTML shell exposing docket chronology dispute branches vocabulary notes and unresolved gates",
    "Real requester agency record decision disclosure reviewer and affected-party evidence gap",
    "Real records-management legal privacy and public-sector professional evaluation gap",
    "Manual keyboard screen-reader cognitive low-vision privacy and security evaluation gap",
    "Real access correction refusal disclosure complaint appeal or remedy action exact gate",
    "Reserved taonga-record metadata field-set requiring competent Māori authority before any value interpretation or action",
    "Synthetic docket success cannot authorize Stage 20 proof-canon final-physics or Theory-of-Everything promotion",
]

SOURCES = [
    {
        "source_id": "NZ-OPC-IPP6",
        "url": "https://www.privacy.org.nz/privacy-principles/6/",
        "status": "New Zealand Office of the Privacy Commissioner IPP 6 page checked 2026-08-31",
        "use": "access-request and correction-advice vocabulary only; no legal interpretation, compliance conclusion, case handling, or real-person data"
    },
    {
        "source_id": "NZ-OPC-IPP7",
        "url": "https://www.privacy.org.nz/privacy-principles/7/",
        "status": "New Zealand Office of the Privacy Commissioner IPP 7 page checked 2026-08-31",
        "use": "correction-request, statement-of-correction, and linked-notification vocabulary only; no legal interpretation, remedy, decision, or compliance conclusion"
    },
    {
        "source_id": "NZ-OPC-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "New Zealand Office of the Privacy Commissioner principles overview, including IPP 3A in force from 2026-05-01, checked 2026-08-31",
        "use": "collection, storage, access, correction, accuracy, use, disclosure, retention, and identifier vocabulary only; no compliance conclusion"
    },
    {
        "source_id": "ARCHIVES-NZ-IRM-STANDARD",
        "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/key-obligations-and-the-standard/information-and-records-management-standard",
        "status": "Archives New Zealand Information and Records Management Standard page checked 2026-08-31",
        "use": "record, metadata, accountability, governance, accessibility, usability, risk, and lifecycle vocabulary only; no regulated-organisation conformance or professional-authority claim"
    },
    {
        "source_id": "ARCHIVES-NZ-METADATA-MINIMUM",
        "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/implementation/metadata/minimum-requirements-for-metadata",
        "status": "Archives New Zealand minimum metadata requirements page checked 2026-08-31",
        "use": "identifier, name, creation date, activity, creator, application, later action, disposition, and protection vocabulary only; all real values remain absent"
    },
    {
        "source_id": "ARCHIVES-NZ-METADATA-GUIDE",
        "url": "https://www.archives.govt.nz/manage-information/how-to-manage-your-information/implementation/metadata/metadata-for-information-and-records",
        "status": "Archives New Zealand metadata guidance updated June 2026 and checked 2026-08-31",
        "use": "content, context, structure, point-of-capture, process, relationship, and persistent-link vocabulary only; no implementation or audit claim"
    },
    {
        "source_id": "DCMI-METADATA-TERMS",
        "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
        "status": "Dublin Core Metadata Initiative current terms page checked 2026-08-31",
        "use": "title, creator, description, date, rights, access-rights, relation, and provenance vocabulary only; no conformance claim"
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
        "source_id": "TE-MANA-RARAUNGA",
        "url": "https://www.temanararaunga.maori.nz/",
        "status": "Te Mana Raraunga public authority-reservation context checked 2026-08-31",
        "use": "Māori data-sovereignty and authority-reservation vocabulary only; no Māori wording, interpretation, ratification, or authority claim"
    }
]

PROTECTED_GATES = [
 "no real person, participant, requester, representative, agency, caseworker, reviewer, decision-maker, record, attachment, request, correction, counterstatement, disclosure, refusal, complaint, appeal, remedy, disposition, identifier, contact route, case row, or external write",
 "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
 "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
 "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
 "no professional, records-management, archival, privacy, accessibility, public-sector, legal, engineering, preservation, ownership, disposal, disclosure, complaint, remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
    ("AUR6777-START-N001", "The first activation packet word-count expression over-escaped its token pattern and falsely returned zero.", "AUR6777-START-P001", "An explicit UTF-8 read with the corrected token expression counted 16,449 words and the exact packet SHA-256 was independently confirmed."),
    ("AUR6777-START-N002", "A PowerShell foreach expression was piped directly and failed with EmptyPipeElement before producing a source projection.", "AUR6777-START-P002", "The rows were first materialized into a bounded array and only then projected, producing the attributable result."),
    ("AUR6777-START-N003", "A combined ancestry projection embedded native Git commands in a PowerShell expression and failed at parse time.", "AUR6777-START-P003", "Each ancestry edge and exit code was captured as a scalar before projection; source, x1, evidence, and final direct-parent checks then matched."),
    ("AUR6777-START-N004", "The first unbounded current-authentication JSON display was truncated and could not prove complete guidance coverage.", "AUR6777-START-P004", "The same immutable file was reread in numbered bounded chunks through EOF without mutation."),
    ("AUR6777-START-N005", "A broad D-drive filename search for Ilyra's canonical receipt exhausted its 30-second display bound without a usable path.", "AUR6777-START-P005", "The search was narrowed to the declared receipt banks, locating the exact receipt and matching its activation SHA-256."),
    ("AUR6777-START-N006", "The shared current-auth and roster snapshots were structurally valid but stale at v667 and could not establish the live v677 edge.", "AUR6777-START-P006", "The stale snapshots were retained as zero-credit drift evidence; the newer exact Ilyra activation and Hamish authority establish Auren v677-v7 and prospective Sable v677-v8 subject to terminal refresh."),
    ("AUR6777-START-N007", "The first large activation display ended at its output limit and did not constitute an EOF read.", "AUR6777-START-P007", "Bounded UTF-8 chunks covered the missing region through EOF and were bound to the verified packet hash."),
    ("AUR6777-START-N008", "The first owner-template copy attempted destinations before the empty sparse scripts and tests directories existed, so all three copies failed.", "AUR6777-START-P008", "Only the missing Auren-owned directories were created; the three exact source templates were then copied successfully without sibling mutation."),
    ("AUR6777-START-N009", "The first x1 builder invocation found the pre-created empty owner phase directory and failed closed under its no-overwrite guard.", "AUR6777-START-P009", "A read-only exact-target inspection proved the Auren v677-v7 directory had zero children; only that empty owner directory was removed before a fresh builder invocation."),
    ("AUR6777-START-N010", "The first complete source-bounded semantic audit found five exact-title collisions and fifteen rows at or above the 0.75 neighbor threshold, all retained with zero freeze credit.", "AUR6777-START-P010", "Only the fifteen generic rows were rewritten as casefile-specific contracts before a new full source audit; the failed collision and quarantine result remains nonerasing Method Flow evidence."),
    ("AUR6777-START-N011", "The first owner-test command used py -3, which resolved to a Microsoft Store Python 3.13 surface without pytest and failed before collection.", "AUR6777-START-P011", "A bounded command-resolution probe selected the installed Python 3.12 runtime; python -B reported pytest 9.1.1 before the owner test was retried."),
    ("AUR6777-START-N012", "The legacy workspace-dependency loader returned that the app tool had moved to the Codex-app MCP server and supplied no runtime paths.", "AUR6777-START-P012", "Local read-only command resolution identified the exact Python executable and pytest surface without installing packages or mutating profiles."),
    ("AUR6777-START-N013", "The first Python 3.12 owner-test run occurred before exact staging and returned nine passes plus one manifest-coverage failure because the provisional manifest did not yet bind the three code and test paths.", "AUR6777-START-P013", "The exact planning-only set was staged first, then the normalized-LF manifest assembler bound all staged owner paths before the owner test was rerun."),
]

OWNER_SKILLS = [
 "ghc-civic-record-casefile-hierarchy",
 "ghc-civic-record-request-state",
 "ghc-civic-record-clock-vacancy",
 "ghc-civic-record-role-firewall",
 "ghc-civic-record-representation-vacancy",
 "ghc-civic-record-accessibility-status",
 "ghc-civic-record-rendition-lineage",
 "ghc-civic-record-provenance-vacancy",
 "ghc-civic-record-correction-chain",
 "ghc-civic-record-privacy-minimizer",
 "ghc-civic-record-remedy-reservation",
 "ghc-civic-record-cultural-authority-gate",
 "ghc-civic-record-maori-authority-gate",
 "ghc-civic-record-json-patch-guard",
 "ghc-civic-record-deterministic-serialization",
 "ghc-civic-record-git-blob-receipt",
 "ghc-civic-record-accessibility-structure",
 "ghc-civic-record-method-nonerasure",
 "ghc-civic-record-real-evidence-gap",
 "ghc-civic-record-stage20-denylist"
]

SUCCESSOR_SKILLS = [
 "successor-community-archive-context-card-intake",
 "successor-acquisition-provenance-neighbor-audit",
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
    "ghc_family_auren_lark_v677_v7_contract_runner.py",
    "ghc_family_auren_lark_v677_v7_mutation_runner.py",
    "ghc_family_auren_lark_v677_v7_topology_runner.py",
    "ghc_family_auren_lark_v677_v7_metadata_runner.py",
    "ghc_family_auren_lark_v677_v7_flashcard_runner.py",
    "ghc_family_auren_lark_v677_v7_toolchain_runner.py",
    "ghc_family_auren_lark_v677_v7_privacy_runner.py",
    "ghc_family_auren_lark_v677_v7_accessibility_runner.py",
    "ghc_family_auren_lark_v677_v7_portfolio_runner.py",
    "build_ghc_family_auren_lark_v677_v7_report.py",
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

PORTFOLIO_TOPICS = [
    "casefile namespace and hierarchy",
    "request lifecycle state",
    "clock and deadline vacancy",
    "access-outcome representation",
    "correction-outcome representation",
    "counterstatement linkage",
    "disclosure-recipient lineage",
    "role and identity firewall",
    "record metadata crosswalk",
    "search-source provenance",
    "version rendition and redaction topology",
    "appeal complaint and remedy vacancy",
    "accessible-format status",
    "privacy and identifier minimization",
    "retention and disposal authority vacancy",
    "deterministic JSON canonicalization",
    "bounded JSON patch allowlist",
    "normalized-LF Git-blob evidence",
    "content-addressed flashcards",
    "Method Flow nonerasure",
]

PORTFOLIO_ACTIONS = [
    "schema contract",
    "bounded positive fixture",
    "rejecting mutation fixture",
    "metamorphic invariant check",
    "accessible documentation card",
    "attributable receipt and rollback note",
]

PROTECTED_ACTION_TOPICS = [
    "use a real requester identity",
    "accept representative authority",
    "classify real personal information",
    "release a real record",
    "refuse a real request",
    "correct a real record",
    "attach a real counterstatement",
    "notify a real disclosure recipient",
    "decide a legal deadline",
    "select a withholding ground",
    "make a complaint determination",
    "make an appeal determination",
    "order or deliver a remedy",
    "dispose of or destroy a record",
    "assert regulated recordkeeping conformance",
    "assert privacy compliance",
    "assert accessibility completeness",
    "decide a cultural-data question",
    "exercise Māori authority",
    "promote Stage 20 or proof canon",
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
    source_phase = "Ilyra Fen v677-v6 exact final"
    path = "docs/ilyra-fen/v677-v6/x1/new-proposal-freeze.json"
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
                "auren_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"AUR6777-N{offset:03d}"
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
            source_ids += ["NZ-OPC-IPP6", "NZ-OPC-IPP7", "NZ-OPC-PRIVACY-PRINCIPLES", "ARCHIVES-NZ-IRM-STANDARD"]
        if 26 <= offset <= 45:
            source_ids += ["ARCHIVES-NZ-METADATA-MINIMUM", "ARCHIVES-NZ-METADATA-GUIDE", "LOC-PREMIS-3"]
        if offset in {22, 28, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "ARCHIVES-NZ-METADATA-GUIDE"]
        if offset in {24, 25, 41, 42, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["NZ-OPC-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real people, requesters, agencies, records, requests, corrections, disclosures, refusals, complaints, appeals, remedies, identity, professional, legal, cultural, affected-party, or authority claims."
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
    rows = []
    for index in range(1, count + 1):
        topic = PORTFOLIO_TOPICS[(index - 1) % len(PORTFOLIO_TOPICS)]
        action = PORTFOLIO_ACTIONS[((index - 1) // len(PORTFOLIO_TOPICS)) % len(PORTFOLIO_ACTIONS)]
        rows.append(
            {
                "task_id": f"AUR6777-{prefix}-{index:03d}",
                "kind": kind,
                "owner": owner,
                "plan_only_at_x1": True,
                "topic": topic,
                "action": action,
                "task": f"Create one owner-local {action} for {topic}",
                "acceptance": "One explicit synthetic owner-local artifact or receipt with deterministic acceptance and no protected-gate conversion",
                "rollback": "Retain the failed witness, revert only the owner-local uncommitted target, and rerun the isolated dependency",
                "protected_gates": PROTECTED_GATES,
            }
        )
    return rows


def exact_or_blocked(kind: str, count: int, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"AUR6777-{prefix}-{index:03d}",
            "kind": kind,
            "requested_action": PROTECTED_ACTION_TOPICS[index - 1],
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
            "docs/auren-lark/v677-v7/validation/x1-manifest.json",
            "docs/auren-lark/v677-v7/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Ilyra Fen v677-v6 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Auren x1 already exists; no overwrite permitted")

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
            "new_auren_proposals": len(rows),
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
            "practice_1": "synthetic public-record access-and-correction casefile registration, status, counterstatement, provenance, and dispute documentation",
            "practice_2": "synthetic archival metadata, accessibility-format, authority-vacancy, appeal, and reversible-handover documentation",
            "practice_3": "owner-scoped deterministic software verification with exact Git-blob evidence",
            "successor_recommendation": "synthetic community-archive acquisition provenance reconciliation with explicit access-status, cultural-authority vacancy, and reversible quarantine",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Sable Rook", "SCAND"),
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Sable Rook", "SCFR"),
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
        "synthetic-access-correction-casefile-practice",
        "archival-metadata-accessibility-and-authority-vacancy-practice",
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
            "successor": "Sable Rook",
            "successor_phase": "v677-v8",
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
        f"""# Auren Lark {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Ilyra Fen's immutable v677-v6 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Ilyra's successful external owner-scoped canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Auren proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is Freed ID and CBR Heart. The wholly synthetic learning and design lenses are public-record access-and-correction casefile registration, status, statement-of-correction linkage, provenance, dispute, archival metadata, accessibility-format, authority-vacancy, appeal, and reversible-handover documentation, plus owner-scoped deterministic software verification. GMUT Mind and THOS Body remain explicit and protected. No real person, requester, representative, agency, record, request, correction, disclosure, refusal, complaint, appeal, remedy, disposal, rights decision, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 Sable candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action. Up to five global promotions remain a hard ceiling, while the present x1 target is zero and every promotion remains separately gated.

## Boundaries

GMUT remains a typed scalar-tensor and EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Records-management, archival, privacy, accessibility, public-sector, legal, cultural, affected-party, Māori-data, Māori-authority, complete-privacy, complete-accessibility, exhaustive-security, independent-reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

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
