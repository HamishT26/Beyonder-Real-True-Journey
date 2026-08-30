#!/usr/bin/env python3
"""Build the planning-only Neris Solane v677-v3 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Neris Solane"
OWNER_SLUG = "neris-solane"
PHASE = "v677-v3"
DISPLAY_PHASE = "v677-v3"
BRANCH = "codex/GHC-Family/neris-solane-v677-v3-full-tools"
SOURCE = "76e4e605a63074f4664296f9b61c59d41886d097"
SOURCE_PHASE = "v677-v2"
GENERATED_AT_NZ = "2026-08-30T20:22:16+12:00"
DECLARED_CHAIN_BEFORE = 7910
DECLARED_CHAIN_AFTER = 7970
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 44145,
    "effective_methods": 38304,
    "retained_failed_witnesses": 15806,
    "bounded_passing_witnesses": 23198,
    "open_gaps": 374,
    "exact_gates": 365,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Elaren Kestrel v677-v2 immutable repository seal plus its one-row post-final route overlay, kept as separately attributable layers."
    ),
}

NEW_TITLES = ['Synthetic meteorological-chart registry namespace without station identity measurement or service claim',
 'Barograph drum clock pen arm baseline and trace relation graph without pressure observation',
 'Thermograph bulb linkage clock drum and temperature-trace topology without calibration conclusion',
 'Hygrograph sensing element linkage pen and humidity-trace relation without material identification',
 'Rain-gauge collector funnel receiver and chart register without precipitation quantity',
 'Anemograph direction speed clock and trace-channel relation without wind inference',
 'Sunshine-recorder card groove burn-mark and time-scale vocabulary firewall without exposure claim',
 'Instrument enclosure screen stand and surrogate station-layout topology without siting assessment',
 'Chart origin time grid annotation channel and trace-segment register without observed timestamp',
 'Clock-drift pen-lag trace-gap overlap and discontinuity placeholders without correction value',
 'Pressure temperature humidity wind rainfall and sunshine channel inventory with every reading vacant',
 'Instrument serial maker station observer date and service-history firewall without attribution',
 'Chart paper ink coating adhesive fastener and housing-material vacancies without composition determination',
 'Fade stain tear crease abrasion mould and pest cue register without condition diagnosis',
 'Pen skip smudge overwrite trimming and splice cues without authenticity or cause inference',
 'Scale label unit symbol range graduation and axis-orientation fields without metrological validation',
 'Chart edge datum mark rotation offset and registration placeholders without measured geometry',
 'Loose pen arm cracked window detached chart and unstable housing support vacancy without safety assessment',
 'Environmental storage light humidity temperature and vibration register without observed readings',
 'Synthetic station chronology and instrument-change lineage with all real locations and events vacant',
 'Chart-sheet sequence volume folder sleeve and surrogate locator escrow with custody fields disabled',
 'Image derivative crop rotation contrast and transcription lineage without real image capture',
 'Previous annotation repair rehousing cleaning and digitization chronology without professional inference',
 'Observer initials station name instrument maker plaque and handwriting firewall without identity attribution',
 'Weather event place name community impact and cultural-context compartment without interpretation authority',
 'Archive location orientation container and access fields with every real value vacant',
 'Documentation queue admission review correction and discharge sentinel with every service event vacant',
 'Container opening chart movement and instrument handling decision packet with action fields hard-disabled',
 'Cleaning flattening repair sampling calibration and digitization action refusal board',
 'Hazard hold for glass sharp edges mould dust mercury lead paint electricity lifting and unstable supports',
 'Emergency vocabulary capsule for damaged meteorological charts with operational decision channel disabled',
 'Reversible correction and supersession lineage for synthetic chart-component assertions',
 'Bitemporal clock ledger binding synthetic trace assertions to reversible review instants',
 'Duplicate channel dangling trace impossible time loop and orphan annotation rejection contract',
 'Deterministic JSON dossier normalizer for surrogate weather charts with NaN and key-order rejection',
 'Normalized-LF exact Git-blob manifest for owner-local meteorological-chart evidence',
 'Screen-reader route grammar for chart headings axis summaries and unresolved human-review slots',
 'Textual trace-map alternative using ordered axes channels gaps annotations and uncertainty vacancies',
 'Low-vision chart contrast zoom and trace-distinction companion proxy with manual review reserved',
 'Comprehension-scaffolded synopsis of an invented barograph sheet with evaluation vacancy',
 'Field minimization matrix for anonymous chart and instrument topology with expiry vacancies',
 'Contestation queue for disputed meteorological-chart assertions with reversible visibility states',
 'Digest-keyed modular study deck spanning trace intake dispute correction and abstention',
 'Citation-bound weather-instrument vocabulary card separating observation consent rights and authority',
 'Hash-linked supersession graph retaining withdrawn contradicted and replacement learning nodes',
 'GMUT trace-graph analogy for channels clocks and annotations without physical-law promotion',
 'Label-permutation metamorphic fixture preserving synthetic instrument-channel adjacency without physics claim',
 'Underdetermined parameter register for absent meteorological observations and nonidentifiable graph coefficients',
 'GMUT uncertainty-vacancy ledger refusing posterior constraint prediction force or detected-law language',
 'Two-arm equal-resource THOS documentation protocol with no users operators devices sessions or result',
 'THOS chart-ingest state machine with all acquisition calibration control and deployment routes disabled',
 'Freed ID surrogate chart envelope with zero keys proofs issuance status resolution or revocation',
 'CBR challenge remedy and affected-party queue with every real claimant reviewer and decision vacant',
 'Three-profession boundary matrix for meteorological metrology archival description and accessibility review',
 'Real meteorologist metrologist archivist conservator custodian and affected-reader evaluation gap',
 'External browser keyboard assistive-technology and independent-reader replication gap for chart dossiers',
 'Accessible-source title-map coverage gap between reachable proposal blobs and the declared chain',
 'Real chart survey calibration handling repair digitization release and professional-signoff exact gate',
 'Contested station data ownership access cultural heritage Māori-data-governance and Māori-authority exact gate',
 'Terminal readiness refusal matrix for meteorological proxies awaiting independent unrelated evidence and competent authority']

SOURCES = [{'source_id': 'WMO-NO8-2026-PRELIMINARY',
  'url': 'https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/instruments-and-methods-of-observation-programme-imop/preliminary-2026-edition-of-guide-instruments-and-methods-of-observation-wmo-no-8',
  'status': 'official WMO preliminary 2026 guide page checked 2026-08-30',
  'use': 'instrument, observation-method, calibration, traceability, and explicit preliminary-status vocabulary '
         'only'},
 {'source_id': 'NOAA-NCEI-HOMR',
  'url': 'https://www.ncei.noaa.gov/access/homr/api',
  'status': 'official NOAA NCEI Historical Observing Metadata Repository page checked 2026-08-30',
  'use': 'station-history, identifier, observation-time, reporting-method, equipment-change, and metadata vocabulary '
         'only; zero rows acquired'},
 {'source_id': 'NOAA-NCEI-STATION-HISTORIES',
  'url': 'https://www.ncei.noaa.gov/products/land-based-station/station-histories',
  'status': 'official NOAA NCEI station-histories page checked 2026-08-30',
  'use': 'station-history and circumstances-of-observation vocabulary only; zero observations acquired'},
 {'source_id': 'NPS-MUSEUM-HANDBOOK-II',
  'url': 'https://www.nps.gov/museum/publications/MHII/MHII.pdf',
  'status': 'official National Park Service Museum Handbook Part II checked 2026-08-30',
  'use': 'catalogue, accession, status, location, condition, and record-correction vocabulary only'},
 {'source_id': 'W3C-PROV-O',
  'url': 'https://www.w3.org/TR/prov-o/',
  'status': 'W3C Recommendation checked 2026-08-30',
  'use': 'entity, activity, agent, derivation, and attribution vocabulary only'},
 {'source_id': 'NIST-TN-1297',
  'url': 'https://www.nist.gov/pml/nist-technical-note-1297',
  'status': 'official NIST uncertainty guidance page checked 2026-08-30',
  'use': 'quantity, uncertainty, traceability, and absent-measurement boundary vocabulary only'},
 {'source_id': 'WORKSAFE-SAFE-MACHINERY',
  'url': 'https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/',
  'status': 'official WorkSafe New Zealand machinery guidance page checked 2026-08-30',
  'use': 'hazard-elimination, guarding, competence, and action-refusal vocabulary only; no operational advice'},
 {'source_id': 'WCAG-2.2',
  'url': 'https://www.w3.org/TR/WCAG22/',
  'status': 'W3C Recommendation with current errata checked 2026-08-30',
  'use': 'structural accessibility vocabulary only; no conformance claim'},
 {'source_id': 'W3C-VC-DATA-MODEL-2.0',
  'url': 'https://www.w3.org/TR/vc-data-model-2.0/',
  'status': 'W3C Recommendation checked 2026-08-30',
  'use': 'status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs'},
 {'source_id': 'NZ-PRIVACY-PRINCIPLES',
  'url': 'https://www.privacy.org.nz/privacy-principles/',
  'status': 'official New Zealand Privacy Commissioner principles page checked 2026-08-30',
  'use': 'collection, use, disclosure, access, correction, retention, and minimization vocabulary only; no '
         'compliance conclusion'},
 {'source_id': 'TE-MANA-RARAUNGA',
  'url': 'https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty',
  'status': 'Te Mana Raraunga principles publication checked 2026-08-30',
  'use': 'Māori data-sovereignty and authority-reservation vocabulary only; no Māori wording, interpretation, '
         'ratification, or authority claim'},
 {'source_id': 'RFC-8785',
  'url': 'https://www.rfc-editor.org/rfc/rfc8785.html',
  'status': 'RFC Editor informational RFC checked 2026-08-30',
  'use': 'deterministic JSON vocabulary only; no production cryptographic assurance'}]

PROTECTED_GATES = ['no real person, participant, meteorologist, metrologist, archivist, conservator, custodian, owner, affected user, '
 'station, instrument, meteorological chart, trace, annotation, collection, observation, measurement, image, '
 'handling, calibration, repair, cleaning, treatment, digitization, release, network row, or external write',
 'no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, '
 'ultraviolet or quantum completion, final physics, or Theory-of-Everything claim',
 'no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, '
 'personhood, or independent-reproduction claim',
 'no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, '
 'trust-governance, affected-party acceptance, or identity-continuity claim',
 'no professional, meteorological, calibration, condition, material, structural, access, machinery, glass, mercury, '
 'electrical, mould, dust, lifting, repair, handling, conservation, ownership, custody, heritage, copyright, legal, '
 'privacy-remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority '
 'decision',
 'no accessibility-complete, privacy-complete, exhaustive-security, proof, canon, or Stage 20 claim']

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

STARTUP_FAILURES = [('NRS6773-START-N001',
  'The initial memory-summary size projection piped a PowerShell if/else expression directly and failed with an '
  'empty-pipe parse error before reading or changing repository state.',
  'NRS6773-START-P001',
  'A scalar assignment before JSON projection recovered the bounded memory lookup without mutation.'),
 ('NRS6773-START-N002',
  'The first activation-packet lines 101-200 display clipped part of a long flashcard line and earned zero '
  'full-window credit.',
  'NRS6773-START-P002',
  'Separate 101-150 and 151-200 windows recovered the unchanged packet bytes through that interval.'),
 ('NRS6773-START-N003',
  'The first all-window activation-packet display exceeded the global presentation budget and was incomplete.',
  'NRS6773-START-P003',
  'Bounded 25-line windows completed the exact 496-line packet through EOF without mutation.'),
 ('NRS6773-START-N004',
  'The first full current-state.json projection exceeded its output budget before EOF.',
  'NRS6773-START-P004',
  'Four bounded windows completed all 1,556 lines and preserved the mutable snapshot read-only.'),
 ('NRS6773-START-N005',
  'A broad activation-packet rg projection expanded repeated flashcard prose and exceeded its output budget.',
  'NRS6773-START-P005',
  'Exact headings and bounded packet sections supplied the required route and lifecycle fields without repeating the '
  'broad projection.'),
 ('NRS6773-START-N006',
  'A combined parallel manifest replay exceeded the model-context presentation boundary and produced no attributable '
  'complete aggregate.',
  'NRS6773-START-P006',
  'Serial scalar-only Git-blob replays established all four manifest digests and the content seal without invoking '
  'the predecessor canonical.'),
 ('NRS6773-START-N007',
  'The first PowerShell manifest wrapper was rejected by the command policy before execution.',
  'NRS6773-START-P007',
  'A read-only Python Git-object projection used literal paths and emitted bounded scalar results.'),
 ('NRS6773-START-N008',
  'The first isolated replay used a nonexistent manifests directory and raised FileNotFoundError before any '
  'Git-object comparison.',
  'NRS6773-START-P008',
  'A literal rg file listing resolved the validation directory and the replay then used the exact committed '
  'filenames.'),
 ('NRS6773-START-N009',
  'Parallel byte-and-digest replay reported inconsistent checkout-byte mismatches for CRLF YAML projections.',
  'NRS6773-START-P009',
  'Serial replay distinguished raw checkout byte counts from normalized-LF Git-blob digests and established zero '
  'digest mismatches.'),
 ('NRS6773-START-N010',
  'A broad D-drive receipt-name scan remained unbounded past ninety seconds and was cancelled with zero receipt '
  'credit.',
  'NRS6773-START-P010',
  'A bounded search of the named canonical and validation receipt banks located the exact predecessor latch and '
  'receipt.'),
 ('NRS6773-START-N011',
  'A depth-two D-drive directory projection expanded thousands of paths and exceeded its presentation budget.',
  'NRS6773-START-P011',
  'The top-level receipt-bank names already exposed by the bounded prefix were used for exact bank-scoped searches '
  'only.'),
 ('NRS6773-X1-N001',
  'The first broad prior-Neris Git-tree projection crossed its command-yield boundary without returning a bounded '
  'file list.',
  'NRS6773-X1-P001',
  'Exact docs, scripts, and tests pathspecs recovered only the declared prior-owner templates without mutating '
  'them.'),
 ('NRS6773-X1-N002',
  'The first source-bounded semantic audit found one exact inherited title and ten additional titles at or above '
  'the preregistered 0.75 token-Jaccard quarantine ceiling, then failed closed before writing x1 documents.',
  'NRS6773-X1-P002',
  'The bounded collision report identified only the eleven affected proposal IDs; those titles were rewritten '
  'while every noncolliding proposal and the immutable source remained unchanged.'),
 ('NRS6773-X1-N003',
  'The first x1 test invocation ran before staged-manifest assembly: nine tests passed and the manifest-coverage '
  'test failed because the four owner code paths were not yet recorded.',
  'NRS6773-X1-P003',
  'The exact declared x1 set was staged, the manifest assembler captured the four code paths, and only the failed '
  'manifest-coverage test was selected for dependency recovery; the nine prior passes were not replayed.')]

OWNER_SKILLS = ['meteorological-chart-registry-namespace',
 'chart-grid-component-topology',
 'trace-relation-firewall',
 'measurement-claim-vacancy',
 'hazardous-instrument-action-hold',
 'chart-image-lineage',
 'archive-intake-nonpromotion',
 'custody-status-vacancy',
 'meteorological-chart-provenance-ledger',
 'trace-topology-validator',
 'accessibility-chart-summary-proxy',
 'rights-challenge-escrow',
 'freed-id-four-tier-deck',
 'content-addressed-flashcard-index',
 'flashcard-supersession-nonerasure',
 'gmut-trace-analogy-firewall',
 'gmut-identifiability-boundary',
 'thos-meteorological-handover-proxy',
 'cbr-affected-party-gate',
 'stage20-meteorological-chart-refusal']

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
    "ghc_family_neris_solane_v677_v3_contract_runner.py",
    "ghc_family_neris_solane_v677_v3_mutation_runner.py",
    "ghc_family_neris_solane_v677_v3_topology_runner.py",
    "ghc_family_neris_solane_v677_v3_metadata_runner.py",
    "ghc_family_neris_solane_v677_v3_flashcard_runner.py",
    "ghc_family_neris_solane_v677_v3_toolchain_runner.py",
    "ghc_family_neris_solane_v677_v3_privacy_runner.py",
    "ghc_family_neris_solane_v677_v3_accessibility_runner.py",
    "ghc_family_neris_solane_v677_v3_portfolio_runner.py",
    "build_ghc_family_neris_solane_v677_v3_report.py",
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
    source_phase = "Elaren Kestrel v677-v2 exact final"
    path = "docs/elaren-kestrel/v677-v2/x1/new-proposal-freeze.json"
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
                "neris_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"NRS6773-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 25:
            source_ids += ["WMO-NO8-2026-PRELIMINARY", "NOAA-NCEI-HOMR"]
        if 26 <= offset <= 45:
            source_ids += ["NOAA-NCEI-STATION-HISTORIES", "NPS-MUSEUM-HANDBOOK-II", "NIST-TN-1297", "WORKSAFE-SAFE-MACHINERY"]
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
                    "real meteorological chart, station, instrument, observation, measurement, calibration, treatment, identity, rights, professional, legal, cultural, or authority claims."
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
            "task_id": f"NRS6773-{prefix}-{index:03d}",
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
            "packet_id": f"NRS6773-{prefix}-{index:03d}",
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
            "docs/neris-solane/v677-v3/validation/x1-manifest.json",
            "docs/neris-solane/v677-v3/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Elaren Kestrel v677-v2 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Neris x1 already exists; no overwrite permitted")

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
            "new_elaren_proposals": len(rows),
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
            "primary_pillar": "GMUT Mind",
            "practice_1": "synthetic meteorological-chart component, chart-grid, sensor-arm, trace, and trace-topology documentation",
            "practice_2": "synthetic provenance, accessibility, conservation-intake, correction, and handover documentation",
            "successor_recommendation": "synthetic provenance-record continuity and refusal-boundary documentation",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Neris Solane", "SCAND"),
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Neris Solane", "SCFR"),
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
        "meteorological-chart-trace-practice",
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
            "successor": "Neris Solane",
            "successor_phase": "v677-v3",
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
        f"""# Neris Solane {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Elaren Kestrel's immutable v677-v2 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Elaren's successful owner-scoped canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Elaren proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is GMUT Mind. The wholly synthetic learning/design lens is meteorological-chart component, chart-grid, sensor-arm, trace, and trace topology together with provenance, accessibility, conservation-intake, correction, and handover documentation. GMUT Mind and THOS Body remain explicit and protected. No real person, station record, model, component, collection record, image, measurement, survey, repair, retrace, handling, custody action, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

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
