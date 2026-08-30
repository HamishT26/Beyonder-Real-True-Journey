#!/usr/bin/env python3
"""Build the planning-only Eiren Kestrel v677-v1 x1 packet."""

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
PHASE = "v677-v1"
DISPLAY_PHASE = "v677-v1"
BRANCH = "codex/GHC-Family/eiren-kestrel-v677-v1-full-tools"
SOURCE = "c768916e41b6ecccef21658c81cab7fce0c5a06d"
SOURCE_PHASE = "v676-v8"
GENERATED_AT_NZ = "2026-08-30T21:40:00+12:00"
DECLARED_CHAIN_BEFORE = 7790
DECLARED_CHAIN_AFTER = 7850
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 43513,
    "effective_methods": 36411,
    "retained_failed_witnesses": 15174,
    "bounded_passing_witnesses": 21928,
    "open_gaps": 368,
    "exact_gates": 359,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Caelen Morrow v676-v8 immutable repository seal and acknowledged activation truth, kept separate from Eiren startup failures."
    ),
}

NEW_TITLES = [
    "Synthetic stained-glass panel namespace without object identity ownership or treatment claim",
    "Quatrefoil lancet medallion border and tracery relation graph without architectural survey",
    "Glass-piece lead-came solder-junction topology without material identification",
    "Panel-bar saddle-bar tie-wire and frame relation without structural safety conclusion",
    "Painted flashed opalescent and pot-metal glass vocabulary firewall without composition claim",
    "Lead zinc copper and brass came-material vacancy without alloy determination",
    "Copper-foil seam and solder-joint relation without fabrication or repair instruction",
    "Putty cement and waterproofing field vacancy without material selection or application",
    "Frame masonry ferramenta and setting-bed relation without installation permission",
    "Protective-glazing cavity vent and exterior-layer proxy without design recommendation",
    "Panel bay light and window-opening hierarchy without building access or survey claim",
    "Cartoon cutline pattern and glass-piece relation without authorship or design attribution",
    "Lead-line trace and junction-degree graph without load or stability theorem",
    "Foil-width came-profile and joint-geometry fields with all measurements vacant",
    "Glass fracture crack loss and edge-chip cue register without condition diagnosis",
    "Bowing bulging deflection and displacement placeholders without measurement",
    "Paint-layer flaking firing and corrosion cues without material or treatment conclusion",
    "Biological deposit soiling condensation and weathering cue registry without cause attribution",
    "Ferramenta corrosion tie failure and support vacancy without safety assessment",
    "Light transmission color and opacity placeholders without optical measurement",
    "Rubbing calque and digital-trace surrogate lineage with rights and scale vacancy",
    "Panel photograph recto oblique transmitted-light and detail-view index without image capture",
    "Piece-number and lead-line coordinate map with no real window association",
    "Detached fragment and temporary-location record without custody or handling claim",
    "Loss-fill insert and replacement-piece assertion vacancy without originality decision",
    "Previous intervention and releading event chronology without authenticity inference",
    "Maker studio donor date inscription and signature claim firewall without attribution",
    "Iconography subject sacred narrative and cultural-context compartment without interpretation authority",
    "Architectural location orientation elevation and access fields with every real value vacant",
    "Environmental exposure and microclimate context register without observed readings",
    "Work-order intake and return-status vacancy without possession or service claim",
    "Panel-removal decision packet with action fields hard-disabled and competence evidence absent",
    "Disassembly releading soldering cleaning and installation action refusal board",
    "Hazard hold for lead solder flux acids sharp glass heights and electrical exposure",
    "Emergency stabilization triage representation without operational recommendation",
    "Reversible correction and supersession lineage for panel assertions",
    "Bitemporal provenance ledger for synthetic survey and intervention statements",
    "Duplicate piece dangling junction impossible loop and orphan panel rejection contract",
    "Byte-stable panel dossier serialization with locale and property-order refusal",
    "Normalized-LF exact Git-blob manifest for owner-local stained-glass evidence",
    "Keyboard-navigable panel dossier headings with screen-reader evaluation reserved",
    "Textual panel-map alternative using ordered piece and junction descriptions without conformance claim",
    "Low-vision contrast and zoom companion proxy with manual evaluation reserved",
    "Plain-language geometric tour of a synthetic panel with comprehension review held open",
    "Field-by-field minimization matrix for anonymous panel topology records with expiry vacancies",
    "Contestation queue for disputed panel assertions with reversible visibility states and no adjudication",
    "Four-level Eiren learning index linking role pillar glazing lens and falsifier without identity continuity",
    "Content-addressed learning-card atlas ordered by stained-glass documentation lifecycle",
    "Citation-bound vocabulary card with separate observation consent and authority columns",
    "Append-only card supersession DAG retaining withdrawn and contradicted nodes",
    "GMUT graph analogy for lead-line and glass-piece topology without physical promotion",
    "Component-renaming permutation test for panel graphs with invariant adjacency and no gauge analogy claim",
    "GMUT identifiability board separating symbolic parameters from absent observations",
    "THOS participant-free comparator for monolithic and modular conservation handovers",
    "Real conservator glazier architect custodian and affected-user evaluation gap",
    "External laboratory browser assistive-technology and affected-reader replication vacancy",
    "Canonical row-to-title mapping and complete reachable history gap",
    "Real survey handling repair releading installation and professional-release exact gate",
    "Contested ownership access sacred imagery cultural heritage and Māori-authority exact gate",
    "Stage20 closure docket requiring independent empirical physics production identity and competent governance evidence",
]

SOURCES = [
    {
        "source_id": "NPS-STAINED-GLASS",
        "url": "https://home.nps.gov/articles/000/stained-glass.htm",
        "status": "official National Park Service stained-glass preservation page checked 2026-08-30",
        "use": "panel, glass, came, support, deterioration, documentation, and preservation-reservation vocabulary only",
    },
    {
        "source_id": "NPS-PRESERVATION-BRIEF-33",
        "url": "https://www.nps.gov/orgs/1739/upload/preservation-brief-33-stained-leaded-glass.pdf",
        "status": "official National Park Service Preservation Brief 33 checked 2026-08-30",
        "use": "historic stained and leaded-glass documentation, deterioration, repair-reservation, and professional-boundary vocabulary only",
    },
    {
        "source_id": "HISTORIC-ENGLAND-STAINED-GLASS",
        "url": "https://historicengland.org.uk/advice/technical-advice/buildings/stained-glass-windows/",
        "status": "official Historic England stained-glass guidance page checked 2026-08-30",
        "use": "window, panel, environmental deterioration, conservation, protective-glazing, and competence-reservation vocabulary only",
    },
    {
        "source_id": "HISTORIC-ENGLAND-ENVIRONMENTAL-GUIDANCE",
        "url": "https://historicengland.org.uk/images-books/publications/stained-glass-windows-managing-environmental-deterioration/heag195-stained-glass-windows-jul24/",
        "status": "official Historic England guidance publication page checked 2026-08-30",
        "use": "environment, condensation, protective-glazing, monitoring-reservation, and professional-review vocabulary only",
    },
    {
        "source_id": "W3C-PROV-OVERVIEW",
        "url": "https://www.w3.org/TR/prov-overview/",
        "status": "W3C Working Group Note",
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
        "status": "W3C Recommendation checked 2026-08-30",
        "use": "status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "official New Zealand Privacy Commissioner principles page checked 2026-08-30",
        "use": "collection, use, disclosure, access, correction, retention, and minimization vocabulary only; no compliance or legal conclusion",
    },
    {
        "source_id": "TE-MANA-RARAUNGA",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "status": "Te Mana Raraunga principles publication checked 2026-08-30",
        "use": "Māori data-sovereignty and authority-reservation vocabulary only; no Māori wording, ratification, interpretation, or authority claim",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, glazier, stained-glass conservator, architect, custodian, owner, affected user, panel, window, glass, came, solder, ferramenta, frame, building, observation, measurement, image, handling, removal, disassembly, repair, releading, cleaning, treatment, installation, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
    "no professional, survey, condition, material, structural, access, working-at-height, chemical, lead, sharp-glass, electrical, fire, repair, handling, conservation, ownership, custody, sacred-imagery, heritage, copyright, legal, privacy-remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
        "EK6771-START-N001",
        "A PowerShell foreach projection was piped without materialization and raised EmptyPipeElement.",
        "EK6771-START-P001",
        "The rows were materialized before conversion and only the missing read-only projection was rerun.",
    ),
    (
        "EK6771-START-N002",
        "The complete activation packet exceeded one visible display envelope.",
        "EK6771-START-P002",
        "Bounded numbered windows completed the exact committed packet through EOF without changing it.",
    ),
    (
        "EK6771-START-N003",
        "A combined small-document read truncated before every source document reached EOF.",
        "EK6771-START-P003",
        "The incomplete files were read separately through EOF and no source was mutated.",
    ),
    (
        "EK6771-START-N004",
        "The complete final-owner manifest listing exceeded the available context window.",
        "EK6771-START-P004",
        "Bounded manifest windows and structured count projections completed the exact same file.",
    ),
    (
        "EK6771-START-N005",
        "A source-manifest projection guessed the digest key sha256 although the schema uses sha256_normalized_lf.",
        "EK6771-START-P005",
        "The real manifest keys were inspected before the corrected read-only projection.",
    ),
    (
        "EK6771-START-N006",
        "A large mandatory-skill display overflowed before every selected SKILL.md reached EOF.",
        "EK6771-START-P006",
        "Each selected skill and required reference was read in bounded numbered windows through EOF.",
    ),
    (
        "EK6771-START-N007",
        "Two rg probes passed Windows wildcard path operands that rg rejected.",
        "EK6771-START-P007",
        "The probes were repeated only with explicit paths and include globs.",
    ),
    (
        "EK6771-START-N008",
        "The first combined current-state beacon displays truncated the historical payloads.",
        "EK6771-START-P008",
        "Full JSON parsing, exact hashes, and bounded field projections classified all three beacons as historical v557 evidence rather than live route authority.",
    ),
    (
        "EK6771-START-N009",
        "The first worktree preflight placed command separators inside a parenthesized projection and raised a missing-closing-parenthesis parser error.",
        "EK6771-START-P009",
        "Separate scalar commands recovered exact source, branch, path, and remote truth without mutation.",
    ),
    (
        "EK6771-START-N010",
        "The corrected worktree preflight exceeded its first presentation window while the read-only process continued.",
        "EK6771-START-P010",
        "The original session was awaited to completion and no duplicate preflight was launched.",
    ),
    (
        "EK6771-START-N011",
        "A normalized-LF baton probe joined git-show lines without restoring the final newline and produced an incorrect byte count and digest presentation.",
        "EK6771-START-P011",
        "The exact Git blob and Caelen canonical receipt established the authoritative byte count and SHA-256 without replaying validation.",
    ),
    (
        "EK6771-START-N012",
        "Worktree creation reported an inherited non-cone sparse-pattern warning while materialization continued.",
        "EK6771-START-P012",
        "The original session completed once and the intended sparse list, exact source head, Eiren branch, and clean lane were verified.",
    ),
    (
        "EK6771-START-N013",
        "A manifest read guessed a nested final-validation directory that does not exist in the Caelen packet.",
        "EK6771-START-P013",
        "The bounded phase tree revealed the exact validation/final-owner-manifest.json path before further schema reads.",
    ),
    (
        "EK6771-START-N014",
        "The first x1 constants patch used one stale inherited context sentence and failed without changing the file.",
        "EK6771-START-P014",
        "The exact current context was reread and the narrowly corrected patch applied once.",
    ),
    (
        "EK6771-X1-N001",
        "The first source-bounded Eiren title slate failed closed with ten inherited semantic collisions or quarantined neighbors.",
        "EK6771-X1-P001",
        "Only those ten titles were rewritten; the isolated audit then found zero exact collisions, zero quarantined rows, zero parse failures, and maximum Jaccard 0.666667 below 0.75.",
    ),
    (
        "EK6771-X1-N002",
        "A combined substantive x1 patch contained an inherited overview sentence that no longer matched and applied no changes.",
        "EK6771-X1-P002",
        "The exact current fields and overview were reread, then patched in two bounded reviewable changes.",
    ),
    (
        "EK6771-X1-N003",
        "One rg inspection pattern lost its quoted successor token and failed with an unclosed-group regex error.",
        "EK6771-X1-P003",
        "Independent literal expressions replaced the compound regex and recovered only the requested locations.",
    ),
    (
        "EK6771-X1-N004",
        "The first mechanical template copy placed untracked future x2 and final Eiren surfaces in the planning-only worktree before x1 freeze.",
        "EK6771-X1-P004",
        "Those owner-new files were never staged or executed and were removed after exact parent-scope checks; only the core, x1 builder, x1 manifest, and x1 test remained for the freeze.",
    ),
    (
        "EK6771-X1-N005",
        "The first exact path-bounded PowerShell cleanup was rejected by host command policy before deleting any file.",
        "EK6771-X1-P005",
        "Patch-based deletion removed only the seventeen newly copied untracked Eiren future-lifecycle files.",
    ),
    (
        "EK6771-X1-N006",
        "The first semantic-audit summary projection guessed four non-existent count field names and returned null presentations.",
        "EK6771-X1-P006",
        "The exact audit schema keys were inspected and the source-bounded counts were recovered without rerunning the audit.",
    ),
]

OWNER_SKILLS = [
    "stained-glass-panel-namespace",
    "panel-component-topology",
    "came-junction-relation-firewall",
    "material-claim-vacancy",
    "hazardous-work-action-hold",
    "panel-image-lineage",
    "conservation-intake-nonpromotion",
    "custody-status-vacancy",
    "panel-provenance-ledger",
    "panel-topology-validator",
    "accessibility-panel-summary-proxy",
    "rights-challenge-escrow",
    "freed-id-four-tier-deck",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-panel-analogy-firewall",
    "gmut-identifiability-boundary",
    "thos-conservation-handover-proxy",
    "cbr-affected-party-gate",
    "stage20-stained-glass-refusal",
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
    "ghc_family_eiren_kestrel_v677_v1_contract_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_mutation_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_panel_topology_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_metadata_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_flashcard_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_toolchain_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_privacy_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_accessibility_runner.py",
    "ghc_family_eiren_kestrel_v677_v1_portfolio_runner.py",
    "build_ghc_family_eiren_kestrel_v677_v1_report.py",
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
    source_phase = "Caelen Morrow v676-v8 exact final"
    path = "docs/caelen-morrow/v676-v8/x1/new-proposal-freeze.json"
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
        proposal_id = f"EK6771-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-OVERVIEW", "RFC-8785"]
        if offset <= 25:
            source_ids += ["NPS-STAINED-GLASS", "NPS-PRESERVATION-BRIEF-33"]
        if 26 <= offset <= 45:
            source_ids += ["HISTORIC-ENGLAND-STAINED-GLASS", "HISTORIC-ENGLAND-ENVIRONMENTAL-GUIDANCE"]
        if offset in {22, 28, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 55, 56, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        if offset in {45, 46, 55, 56, 59, 60}:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real panel, window, component, record, measurement, survey, treatment, identity, rights, professional, legal, cultural, or authority claims."
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
            "task_id": f"EK6771-{prefix}-{index:03d}",
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
            "packet_id": f"EK6771-{prefix}-{index:03d}",
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
            "docs/eiren-kestrel/v677-v1/validation/x1-manifest.json",
            "docs/eiren-kestrel/v677-v1/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Caelen v676-v8 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Eiren x1 already exists; no overwrite permitted")

    rows = new_rows()
    inherited = inherited_selection(repo)
    audit = semantic_audit(repo, rows)
    if audit["exact_title_collisions"] or audit["selected_rows_quarantined"] or audit["json_parse_failures"]:
        raise SystemExit(
            "semantic audit failed closed: "
            + json.dumps(
                {
                    "exact": audit["exact_title_collisions"],
                    "quarantined": audit["selected_rows_quarantined"],
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
            "practice_1": "synthetic stained-glass panel survey and component-topology documentation",
            "practice_2": "synthetic conservation-intake, provenance, accessibility, and handover documentation",
            "successor_recommendation": "synthetic conservation-record continuity and refusal-boundary documentation",
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
        "stained-glass-panel-practice",
        "intake-provenance-and-handover-practice",
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
            "successor_phase": "v677-v2",
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
    write_text(
        x1 / "x1-overview.md",
        f"""# Eiren Kestrel {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Caelen Morrow's immutable v676-v8 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Caelen's canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Eiren proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is THOS Body. The wholly synthetic learning/design lens is stained-glass panel survey, component topology, provenance, accessibility, conservation intake, and handover documentation. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. No real person, panel, window, glass, came, measurement, survey, repair, handling, custody action, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, global promotion, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action.

## Boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Professional, inspection, calibration, repair, safety, ownership, legal, cultural, affected-party, Māori-data, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

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
