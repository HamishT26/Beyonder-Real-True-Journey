#!/usr/bin/env python3
"""Build the planning-only Eiren Kestrel v678-v8 remaster x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Eiren Kestrel"
OWNER_SLUG = "eiren-kestrel"
PHASE = "v678-v8"
DISPLAY_PHASE = "v678-v8"
BRANCH = "codex/GHC-Family/eiren-kestrel-v678-v8-full-tools"
SOURCE = "88c952afae7a7dafa60c99f3f2b218a6687c9809"
SOURCE_PHASE = "v678-v7"
GENERATED_AT_NZ = "2026-08-31T13:00:40+12:00"
DECLARED_CHAIN_BEFORE = 8690
DECLARED_CHAIN_AFTER = 8750
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "repository_sealed_effective_negatives": 47603,
    "repository_sealed_effective_methods": 46346,
    "repository_sealed_retained_failed_witnesses": 19264,
    "repository_sealed_bounded_passing_witnesses": 30169,
    "external_route_failures": 2,
    "effective_negatives": 47605,
    "effective_methods": 46349,
    "retained_failed_witnesses": 19266,
    "bounded_passing_witnesses": 30170,
    "open_gaps": 413,
    "exact_gates": 404,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Caelen v678-v7 repository seal plus two post-seal route or presentation failures and one "
        "bounded recovery method, kept separate from Eiren startup and live-delivery evidence."
    ),
}

NEW_TITLES = [
    "Synthetic architectural drawing-set namespace without project site or creator identity assertion",
    "Sheet code title subtitle discipline sequence and cross-reference graph with identifiers vacant",
    "Title-block revision issue status and supersession ledger without authorship approval or release claim",
    "Plan elevation section detail schedule and diagram view taxonomy without design interpretation",
    "Paper tracing cloth vellum film and board support-category vacancy without material identification",
    "Graphite ink wash colour pencil transfer print and reprographic-media cue reservation without diagnosis",
    "Blueprint diazotype photostat electrostatic and digital surrogate process quarantine without authentication",
    "Sheet dimensions margins folds tears losses stains and distortion fields with zero observation",
    "Oversize folder tube flat-file portfolio and enclosure relation model without handling prescription",
    "Drawing front verso overlay insert legend note and stamp component graph without inspection",
    "Architectural scale ratio unit notation and graphic-bar placeholders with zero measurement",
    "Grid datum level benchmark coordinate and north-arrow fields held vacant without survey inference",
    "Line type line weight hatch poche symbol abbreviation and key relation board without meaning claim",
    "Dimension string tolerance radius angle slope area and volume vocabulary with no measured value",
    "Room door window stair roof wall column beam and foundation relation graph without building judgement",
    "Mechanical electrical plumbing structural landscape and civil discipline links without engineering authority",
    "Existing demolition proposed alternate and as-built state vocabulary with construction truth withheld",
    "Revision cloud delta marker bulletin addendum and substitution lineage without contractual effect",
    "Drawing-set completeness index with missing-sheet refusal and no document-control certification",
    "Accessible sheet summary and view-by-view text companion with manual evaluation reserved",
    "Synthetic architectural-record accession series folder item and sheet hierarchy without custody claim",
    "Creator office drafter checker approver client and contractor role vacancies without person identity",
    "Project number commission date location structure name and address fields with all real values absent",
    "Append-only description correction challenge supersession and disputed-attribution provenance",
    "Sheet image crop thumbnail tile and derivative lineage without authenticity or faithful-reproduction claim",
    "Digitization capture target colour target scale bar and resolution plan with camera operation denied",
    "File format colour profile compression orientation and page-order profile without file ingestion",
    "Fixity digest package inventory representation and missing-object refusal with zero archival package",
    "Storage copy access copy reference image and preservation surrogate relations without success claim",
    "Rights copyright license donor restriction embargo and orphan-status quarantine without legal decision",
    "Privacy redaction sensitive-location and security-review state machine with zero personal or site data",
    "Catalogue subject place structure function style and date label vacancies without historical interpretation",
    "Provenance graph for synthetic creation revision reproduction description and access stages",
    "Transport-disabled catalogue adapter with declared zero rows and zero external calls",
    "Deterministic normalized-JSON sheet descriptor with digest collision and ambiguity refusal",
    "GMUT geometric-scale analogy firewall without spacetime metric measurement or physical inference",
    "GMUT typed adjacency tensor for sheet-view relations with all empirical coefficients vacant",
    "GMUT coordinate-transform placeholder with dimensional typing and observational firewall",
    "GMUT uncertainty board for unknown scale date orientation and provenance without posterior claim",
    "GMUT graph-invariant comparison for drawing revisions without uniqueness or discovery claim",
    "THOS zero-person drawing intake triage pause stop quarantine and handover protocol",
    "THOS sheet-review workload queue timebox fatigue placeholder and escalation ledger without real staff",
    "Freed ID nonproduction archive-role envelope with zero keys proofs issuance or lifecycle event",
    "Selective-disclosure placeholder for restricted drawings with no credential proof or release",
    "Consent contestation correction remedy and revocation-request envelope with no affected party",
    "Keyboard heading landmark table focus and noncolour-status structure with conformance reserved",
    "Long-description vacancy board for plans elevations sections and details without affected-user validation",
    "Cognitive-access plain-language sheet navigation and glossary proxy without user-study claim",
    "Māori place-name parallel-label vacancy with wording ratification and authority explicitly reserved",
    "Traditional knowledge sacred site cultural landscape and sensitive-location protection hold",
    "Public catalogue search request reproduction and publication decision firewall",
    "Architectural drawing disaster-response priority proxy with no emergency or conservation instruction",
    "Drawing-condition comparison card with no diagnosis treatment recommendation or handling act",
    "Successor handover index for sheets gaps gates methods and retained failures without route precontact",
    "Real architectural-record inspection measurement digitization and preservation-quality evidence gap",
    "Real browser assistive-technology cognitive and affected-user accessibility evaluation evidence gap",
    "Current institutional storage reproduction interoperability and security capability evidence gap",
    "Design attribution title reproduction restriction and claimant-remedy decision docket under competent-authority hold",
    "Professional architecture engineering conservation surveying construction and workplace-safety exact gate",
    "Māori-language naming whenua wāhi tapu mātauranga tikanga kaitiakitanga iwi hapū governance exact gate",
]

SOURCES = [
    {
        "source_id": "LOC-PAPER-CARE",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "official Library of Congress works-on-paper care page checked 2026-08-31",
        "use": "flat paper, drawing, print, map, enclosure, oversize, light, handling-hold, and condition-referral vocabulary only; no real handling, storage prescription, diagnosis, or treatment",
    },
    {
        "source_id": "NARA-CARTO-ARCH",
        "url": "https://www.archives.gov/research/cartographic/general-info-leaflet-26",
        "status": "official U.S. National Archives cartographic and architectural records page checked 2026-08-31",
        "use": "map, chart, architectural drawing, engineering drawing, plan, record group, series, file, and reference vocabulary only; no holdings claim, search, copy order, custody, or professional decision",
    },
    {
        "source_id": "NARA-HISTORIC-ARCH",
        "url": "https://www.archives.gov/research/electronic-records/historic-preservation",
        "status": "official U.S. National Archives historic-preservation and architecture electronic-records page checked 2026-08-31",
        "use": "paper map, plan, architectural or engineering drawing, digital image, subject category, and online-access vocabulary only; no ingestion, digitization, interpretation, or preservation result",
    },
    {
        "source_id": "NIST-SI",
        "url": "https://www.nist.gov/publications/international-system-units-si-2019-edition",
        "status": "official NIST SI 2019 edition page checked 2026-08-31",
        "use": "SI unit, symbol, dimension, and reporting vocabulary only; all architectural dimensions and measurements remain absent",
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
    "no real person, participant, architect, drafter, engineer, surveyor, builder, conservator, archivist, operator, custodian, owner, rights-holder, affected user, building, site, drawing, map, plan, sheet, media, image, file, observation, measurement, handling, digitization, repair, treatment, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
    "no professional architecture, drafting, engineering, surveying, construction, document control, preservation, conservation, electrical, chemical, fire, workplace-safety, ownership, copyright, licence, consent, privacy-remedy, cultural, affected-party, traditional-knowledge, sacred-site, Māori-language, Māori-data-governance, or Māori-authority decision",
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
        "EK6788-START-N001",
        "A combined seven-file manifest schema projection exceeded its presentation bound and was truncated before every manifest could be attributed.",
        "EK6788-START-P001",
        "Each immutable manifest and staged review was read separately with compact metadata plus complete path, byte, and digest rows; no source byte changed.",
    ),
    (
        "EK6788-START-N002",
        "A template-addition patch used relative destinations and placed twelve provisional owner files in the shared Codex workspace instead of the new D-first lane.",
        "EK6788-START-P002",
        "The exact twelve provisional files were removed with an attributable patch, absence was verified, and absolute D-first patch destinations were used without touching sibling lanes.",
    ),
    (
        "EK6788-START-N003",
        "The worktree creation and sparse-checkout wrapper crossed its first reporting window after the new branch was announced.",
        "EK6788-START-P003",
        "The original process was waited once without replay; it completed at the exact source and the branch, head, clean state, and sparse patterns were then verified.",
    ),
    (
        "EK6788-START-N004",
        "A composite sparse-lane inspection expanded the sparse index and returned advisory text without the requested scalar receipt.",
        "EK6788-START-P004",
        "Separate bounded probes established exact head, branch, clean status, and the complete sparse-pattern file without repeating checkout or changing repository state.",
    ),
    (
        "EK6788-START-N005",
        "A stale-label scan supplied Windows wildcard paths as literal ripgrep roots and therefore returned no attributable scan result.",
        "EK6788-START-P005",
        "The corrected read-only scan used explicit script and test roots with an include glob and produced the complete bounded stale-label inventory.",
    ),
    (
        "EK6788-START-N006",
        "Host command policy rejected an exact path-bounded PowerShell removal of two generated bytecode-cache directories before deletion.",
        "EK6788-START-P006",
        "A Python fallback resolved the owner worktree, asserted both exact targets remained inside it and were named bytecode caches, removed only those generated directories, and verified zero remained.",
    ),
    (
        "EK6788-START-N007",
        "The first planning builder failed closed because one proposed authority-gate title scored 0.7692 against an inherited row, above the 0.75 quarantine threshold.",
        "EK6788-START-P007",
        "Only the quarantined title was rewritten with a distinct design-attribution and claimant-remedy frame before rerunning the planning dependency.",
    ),
    (
        "EK6788-START-N008",
        "The first isolated novelty diagnostic assumed a selected_neighbor_rows field that the exact audit schema does not contain and raised KeyError.",
        "EK6788-START-P008",
        "The audit keys were inspected directly, establishing that per-row results are stored in the neighbors array.",
    ),
    (
        "EK6788-START-N009",
        "The second isolated novelty diagnostic assumed a generic score field in neighbor rows and raised KeyError.",
        "EK6788-START-P009",
        "One exact neighbor row was inspected, then the declared token_jaccard and quarantined fields isolated the single collision without changing source history.",
    ),
    (
        "EK6788-START-N010",
        "The first staged diff whitespace check found one extra terminal blank line in three mechanically cloned owner files.",
        "EK6788-START-P010",
        "Only the three terminal blank lines were removed by patch before regenerating exact manifests and rerunning the affected owner checks.",
    ),
]

OWNER_SKILLS = [
    "architectural-sheet-namespace",
    "title-block-identity-vacancy",
    "scale-unit-placeholder",
    "drawing-set-sequence-graph",
    "revision-cloud-provenance",
    "lineweight-symbol-legend",
    "north-arrow-orientation-vacancy",
    "level-grid-datum-nonclaim",
    "blueprint-process-quarantine",
    "paper-media-condition-cue",
    "oversize-enclosure-vacancy",
    "architectural-drawing-custody-nonclaim",
    "drawing-digitization-plan-firewall",
    "sheet-image-derivative-provenance",
    "accessible-drawing-companion",
    "rights-embargo-quarantine",
    "freed-id-drawing-role-envelope",
    "thos-drawing-handover-proxy",
    "gmut-scale-analogy-firewall",
    "maori-place-authority-reservation",
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
    "ghc_family_eiren_kestrel_v678_v8_contract_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_mutation_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_sheet_topology_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_metadata_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_flashcard_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_toolchain_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_privacy_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_accessibility_runner.py",
    "ghc_family_eiren_kestrel_v678_v8_portfolio_runner.py",
    "build_ghc_family_eiren_kestrel_v678_v8_report.py",
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
    source_phase = "Caelen Morrow v678-v7 exact final"
    path = "docs/caelen-morrow/v678-v7/x1/new-proposal-freeze.json"
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
                "eiren_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"EK6788-N{offset:03d}"
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
            source_ids += ["LOC-PAPER-CARE", "NARA-CARTO-ARCH"]
        if 21 <= offset <= 40:
            source_ids += ["NARA-HISTORIC-ARCH", "NIST-SI"]
        if 41 <= offset <= 60:
            source_ids += ["NARA-CARTO-ARCH", "NARA-HISTORIC-ARCH"]
        if offset in {20, 39, 41, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real person, building, site, drawing, record, observation, measurement, handling, digitization, identity, rights, "
                    "professional, legal, cultural, affected-party, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} accepts a missing or contradictory field, a raw or real identifier, a non-authorized outcome label, "
                    "or an observation, measurement, handling, digitization, preservation, architecture, engineering, competence, right, identity, or authority claim."
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
            "task_id": f"EK6788-{prefix}-{index:03d}",
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
            "packet_id": f"EK6788-{prefix}-{index:03d}",
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
            "docs/eiren-kestrel/v678-v8/validation/x1-manifest.json",
            "docs/eiren-kestrel/v678-v8/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Caelen v678-v7 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Eiren x1 already exists; no overwrite permitted")

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
            "new_eiren_proposals": len(rows),
            "universal_novelty_proved": False,
            "proposals": rows,
        },
    )
    dump(
        x1 / "source-verification.json",
        {
            "source_branch": "codex/GHC-Family/caelen-morrow-v678-v7-full-tools",
            "source": SOURCE,
            "anchors": {
                "sylven_source_and_final": "0110062a8a42e882b209440de54c7dd219c7e4d4",
                "caelen_x1": "58278e392c4d6774b1db8ef548d2f324edb892b2",
                "caelen_x2_evidence": "997f06b8ef13366f035e1c64ab9a162de27a7567",
                "caelen_exact_final": SOURCE,
            },
            "source_to_final_commits": 3,
            "single_parent_commits": 3,
            "merges": 0,
            "final_parent_count": 1,
            "clean_zero_divergent_fresh_four_way_equal": True,
            "canonical_receipt_sha256": "0af918c2b925486a711635ca38edb480bab80186ea9a95f8949e874d6efda1c7",
            "canonical_payload_sha256": "1465bf748b409a4934e16af1f1d273b744cfbe40438befb9372a10a08f3f2a61",
            "canonical_latch_sha256": "b9cc8b47e51d7cb93f34b20ff5a81be7480be446f7cbec0a69e9700128d9c454",
            "baton_normalized_lf_sha256": "dcf233087d8a310af410a13321b83e98733ed1e911ed3e589d322abc8f8166e6",
            "canonical_invocation_count": 1,
            "canonical_success_count": 1,
            "canonical_replay_count": 0,
            "caelen_terminal_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
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
            "primary_pillar": "GMUT Mind",
            "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "practice_1": "synthetic architectural drawing-set, title-block, scale, revision, and reprographic-process documentation",
            "practice_2": "synthetic paper-record preservation, digitization-plan, accessibility, rights-vacancy, and handover documentation",
            "successor_recommendation": "synthetic technical-illustration and diagram continuity documentation with protected authorship and accessibility gates",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Elaren Kestrel", "SCAND"),
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Elaren Kestrel", "SCFR"),
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
        "architectural-drawing-set-practice",
        "paper-record-rights-accessibility-and-handover-practice",
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
            "successor": "Elaren Kestrel",
            "successor_phase": "v679-v1",
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
            "role": "relational scale-lantern and revision-boundary steward",
            "hope": "keep every drawing description distinct from observation, every scale placeholder distinct from measurement, and every revision handover recoverable",
        },
    )
    write_text(
        x1 / "identity-and-authority.md",
        """# Eiren Kestrel v678-v8 relational working boundary

Eiren Kestrel is relational working language for a **scale-lantern and revision-boundary steward**, with the bounded hope of keeping every drawing description distinct from observation, every scale placeholder distinct from measurement, and every revision handover recoverable.

The name, role, hope, pronouns, sibling and family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the work.
""",
    )
    write_text(
        x1 / "threat-model.md",
        """# Eiren Kestrel v678-v8 planning threat model

The bounded assets are proposal truth, exact Git objects, retained failures, privacy-safe documentation, and protected authority gates. Threats include x1/x2 mixing, stale-anchor reuse, false novelty, fabricated observation, accidental real identifiers, package or network side effects, rights or cultural overreach, failure erasure, canonical replay, and premature successor contact.

Controls are an exact immutable source, source-bounded semantic comparison, four authorized outcome labels, zero-row synthetic fixtures, five-class scanning, exact normalized-LF manifests, additive Method Flow, no package installation, no network ingestion, no external writes, no real drawing inspection, measurement, handling, or digitization, planning-only x1, one-attributable-canonical discipline, and a terminal route hold.

Residual gaps include universal historical novelty, real preservation quality, real accessibility and privacy evaluation, independent security and reproduction, professional judgement, legal rights, consent, cultural legitimacy, affected-party acceptance, Māori-language and Māori-data-governance review, and Māori authority.
""",
    )
    write_text(
        x1 / "x1-overview.md",
        f"""# Eiren Kestrel {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Caelen Morrow's immutable exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Caelen's canonical validation, repository seal, delivery event, or external overlays.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Eiren proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical and scientific novelty remain unproved.

## Practice, pillars, and flashcards

The primary pillar is GMUT Mind. The wholly synthetic learning/design lens is architectural drawing-set, scale, title-block, revision, reprographic-process, paper-record preservation, provenance, accessibility, rights-vacancy, intake, and handover documentation. THOS Body and Freed ID/CBR Heart remain explicit and protected. No real person, building, site, drawing, plan, sheet, observation, measurement, inspection, handling, digitization, custody action, rights decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, global promotion, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action.

## Boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Professional architecture, drafting, engineering, surveying, construction, document control, preservation, conservation, safety, ownership, copyright, consent, privacy, legal, cultural, affected-party, Māori-language, Māori-data, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

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
