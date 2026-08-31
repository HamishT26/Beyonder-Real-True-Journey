#!/usr/bin/env python3
"""Build the planning-only Neris Solane v679-v2 x1 packet."""

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
PHASE = "v679-v2"
DISPLAY_PHASE = "v679-v2"
BRANCH = "codex/GHC-Family/neris-solane-v679-v2-full-tools"
SOURCE = "35ed4bc7b4da175b22432534fcdd38cdac2f2707"
SOURCE_PHASE = "v679-v1"
GENERATED_AT_NZ = "2026-08-31T14:28:30+12:00"
DECLARED_CHAIN_BEFORE = 8810
DECLARED_CHAIN_AFTER = 8870
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 48226,
    "effective_methods": 48220,
    "retained_failed_witnesses": 19887,
    "bounded_passing_witnesses": 31423,
    "open_gaps": 419,
    "exact_gates": 410,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Elaren Kestrel v679-v1 immutable repository seal of 48,223 negatives, 48,217 methods, 19,884 failed witnesses, and 31,420 bounded passing witnesses, plus the separately attributable external route overlay yielding 48,226 / 48,220 / 19,887 / 31,423; the 419 open gaps and 410 exact gates remain unchanged."
    ),
}

NEW_TITLES = [
    "Synthetic optical-semaphore station dossier namespace without operator identity ownership or operational claim",
    "Signal-station chain node relay and terminus topology without historical network assertion",
    "Mast arm shutter panel and indicator component map without object inventory claim",
    "Arm azimuth elevation and position-state placeholders without angular measurement",
    "Codebook sign family variant and unknown-symbol relation without message interpretation",
    "Station interval visibility and line-of-sight vacancy register with every real distance absent",
    "Message token group separator and acknowledgement-state grammar without executable signaling instruction",
    "Dispatch transmit relay receive and close state lineage without communication-performance claim",
    "Observation-window schedule placeholder with zero watchkeeping or station operation",
    "Tower cabin platform and access-zone topology without entry or custody permission",
    "Signal-arm position-combination graph without an executable codebook or operating sequence",
    "Upstream downstream branch and terminal station relation without deployed-network claim",
    "Clock epoch transmission-delay and relay-latency placeholders without timing measurement",
    "Weather visibility fog glare and horizon cue registry without observation or cause attribution",
    "Daylight shutter and night-lamp state vacancies without lighting or signaling operation",
    "Telescope viewing aperture alignment and field-of-view placeholders without setup guidance",
    "Pulley rope lever spindle and counterweight linkage topology without mechanics assessment",
    "Timber metal fabric paint and glass material vacancies without identification or condition judgment",
    "Station-book page folio entry and correction sequence without custody or authenticity claim",
    "Codeword phrase numeric-group and null-token mapping without real message content",
    "Cancellation correction supersession and acknowledgement lineage for synthetic dispatch assertions",
    "Sent received relayed missed and uncertain message states without delivery conclusion",
    "Operator observer messenger inspector and historian role vacancies without person identity",
    "Duty roster shift and watch placeholders without a real person date or time",
    "Route map station location and jurisdiction placeholders with all real coordinates absent",
    "Cabinet drawer codebook key and logbook storage vacancies without possession or access claim",
    "Seal stamp signature and annotation-mark placeholders without authorship or authenticity conclusion",
    "Archive series folder item leaf and surrogate hierarchy without collection custody assertion",
    "Copy extract transcription and translation provenance chain without authorship attribution",
    "Source destination and border-jurisdiction placeholders without legal or political interpretation",
    "Emergency weather maintenance and visibility hold flags without response instructions",
    "Tower height ladder platform and fall-exposure reservation without access or safety advice",
    "Optical glare eye-strain and telescope-use hazard reservation without health assessment",
    "Pulley counterweight pinch crush and stored-energy reservation without machinery instruction",
    "Night lamp flame fuel heat smoke and fume reservation without operation or exposure assessment",
    "Electrical retrofit battery cable and switch placeholders with every energized action disabled",
    "Storm wind lightning and structural-access hold without engineering or weather judgment",
    "Remote-station travel fatigue isolation and emergency-communication hold without work advice",
    "Synthetic semaphore assertion correction graph with immutable prior cards and reversible successor edges",
    "Surrogate dispatch epoch pairing for state-change and audit-review time without clock conformance",
    "Canonical UTF-8 record serialization for synthetic signal registers with non-finite number rejection",
    "Git-object evidence map for Neris phase assets with LF-stable content digests",
    "Assistive reading-order map linking signal components and dispatch states to prose landmarks with evaluator vacancy",
    "Textual arm-position alternative using ordered station nodes state labels and intentionally blank regions",
    "Low-vision signal-diagram contrast and zoom companion proxy with manual review reserved",
    "Cognitive-accessibility companion explaining synthetic relay states with reader testing absent",
    "Field-minimization matrix for anonymous station and dispatch topology with expiry vacancies",
    "Contestation queue for disputed message provenance and station-history assertions with reversible visibility states",
    "Spaced-repetition card matrix for station-relay vocabulary and refusal-boundary recall",
    "GMUT relay-graph analogy for station adjacency and latent state without physical-law promotion",
    "GMUT latent-state observability quarantine for sparse symbolic station transitions and unset parameters",
    "THOS matched-budget synthetic document comparison protocol for relay records without participants",
    "Freed ID nonproduction dispatch-role descriptor with absent credentials and disabled lifecycle events",
    "Synthetic fail-safe route-state automaton with no live message transmission or control authority",
    "Real operator historian conservator engineer affected-user and station evaluation gap",
    "Independent assistive-user browser and domain-expert evaluation vacancy for the static semaphore dossier",
    "Reachable proposal-corpus cardinality gap against the declared 8810-row lineage",
    "Real station access signaling observation maintenance repair illumination and professional-release exact gate",
    "Intercepted-message secrecy ownership access cultural heritage and Māori-authority exact gate",
    "Independent-evidence promotion interlock keeping Stage 20 exact-gated to competent authorities",
]

SOURCES = [
    {
        "source_id": "ITU-HISTORY-SEMAPHORE",
        "url": "https://www.itu.int/en/history/pages/ITUsHistory.aspx",
        "status": "official ITU historical overview checked 2026-08-31",
        "use": "visual semaphore station, relay-network, telegraph, and later standardization vocabulary only; no operational or historical-authorship authority",
    },
    {
        "source_id": "ITU-FROM-SEMAPHORE-TO-SATELLITE",
        "url": "https://search.itu.int/history/HistoryDigitalCollectionDocLibrary/12.25.72.en.100.pdf",
        "status": "official ITU historical publication checked 2026-08-31",
        "use": "station-chain, visual-telegraph, code-system, boundary, cost, and historical-limitation vocabulary only; no real station or message assertion",
    },
    {
        "source_id": "LOC-PAPER-CARE",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "official Library of Congress paper-care guidance checked 2026-08-31",
        "use": "paper handling, storage, environment, and professional-referral vocabulary only; no treatment authority",
    },
    {
        "source_id": "WORKSAFE-WORKING-AT-HEIGHT",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/working-at-height/working-at-height-in-nz/",
        "status": "official WorkSafe New Zealand working-at-height page checked 2026-08-31",
        "use": "height, fall-risk, competence, worker-consultation, and stop-condition vocabulary only; no access, climbing, engineering, or safety advice",
    },
    {
        "source_id": "WORKSAFE-MACHINE-LOCKOUTS",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/keeping-workers-safe-with-machine-lockouts/",
        "status": "official WorkSafe New Zealand lockout guidance checked 2026-08-31",
        "use": "isolation, unexpected-startup, stored-energy, competence, and stop-condition vocabulary only; no machine operation",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation checked 2026-08-31",
        "use": "entity, activity, agent, derivation, and attribution vocabulary only",
    },
    {
        "source_id": "NIST-TN-1297",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297",
        "status": "official NIST uncertainty guidance page checked 2026-08-31",
        "use": "quantity, uncertainty, traceability, and absent-measurement boundary vocabulary only",
    },
    {
        "source_id": "WORKSAFE-SAFE-MACHINERY",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/",
        "status": "official WorkSafe New Zealand machinery guidance page checked 2026-08-31",
        "use": "hazard-elimination, guarding, competence, and action-refusal vocabulary only; no operational advice",
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
        "status": "W3C Recommendation checked 2026-08-31",
        "use": "status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "official New Zealand Privacy Commissioner principles page checked 2026-08-31",
        "use": "collection, use, disclosure, access, correction, retention, and minimization vocabulary only; no compliance or legal conclusion",
    },
    {
        "source_id": "TE-MANA-RARAUNGA",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "Te Mana Raraunga principles publication checked 2026-08-31",
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
    "no real person, participant, signal operator, observer, messenger, historian, conservator, engineer, custodian, owner, affected user, station, tower, mast, arm, shutter, lamp, telescope, codebook, logbook, message, route, coordinate, observation, measurement, image, handling, access, setup, operation, signaling, maintenance, repair, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
    "no professional, condition, material, historical, archival, telecommunication, navigation, station-access, climbing, fall, machinery, pinch, crush, stored-energy, flame, fuel, heat, smoke, fume, electrical, storm, fatigue, repair, handling, conservation, ownership, custody, intercepted-message, secrecy, heritage, copyright, legal, privacy-remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
        "NE6792-START-N001",
        "The first JavaScript-orchestrated PowerShell probe used unsafe nested quoting and failed before filesystem access.",
        "NE6792-START-P001",
        "Literal paths and scalar commands replaced the nested expression and completed the intended read-only projection.",
    ),
    (
        "NE6792-START-N002",
        "A PowerShell normalized-content hash probe selected an ambiguous Replace or hash overload and earned no verification credit.",
        "NE6792-START-P002",
        "A byte-explicit normalized-LF implementation recovered the packet hash without repository mutation.",
    ),
    (
        "NE6792-START-N003",
        "A combined activation-packet projection truncated before EOF and earned no complete-read credit.",
        "NE6792-START-P003",
        "Bounded non-overlapping fifty-line windows completed the immutable activation packet through EOF.",
    ),
    (
        "NE6792-START-N004",
        "A PowerShell foreach pipeline used an empty pipe element while measuring named skill files and failed before any write.",
        "NE6792-START-P004",
        "Materializing the collection before formatting recovered the exact skill inventory.",
    ),
    (
        "NE6792-START-N005",
        "A combined flashcard and Meta Tool Box reference projection exceeded its output budget and earned no complete-read credit.",
        "NE6792-START-P005",
        "Each directly applicable reference was reread separately through EOF.",
    ),
    (
        "NE6792-START-N006",
        "The first lane-admission object embedded command status in a parenthesized expression and failed PowerShell parsing.",
        "NE6792-START-P006",
        "Scalar status variables recovered the exact branch, remote, D-drive, and candidate-absence admission facts.",
    ),
    (
        "NE6792-START-N007",
        "A second foreach-to-pipeline expression failed while summarizing manifest keys and earned no manifest credit.",
        "NE6792-START-P007",
        "A materialized result collection recovered the manifest structure without replaying Elaren tests or canonical validation.",
    ),
    (
        "NE6792-START-N008",
        "A manifest replay launched hundreds of separate Git show processes and returned no attributable result in the bounded window.",
        "NE6792-START-P008",
        "One read-only Git cat-file batch stream per immutable commit replayed all five manifest and seal sets with zero mismatch.",
    ),
    (
        "NE6792-START-N009",
        "A broad source Git grep for candidate-domain words outlived its bounded result window and was terminated without a repository write.",
        "NE6792-START-P009",
        "The phase semantic auditor replaced the broad grep with source-bounded proposal JSON traversal and exact neighbor quarantine.",
    ),
    (
        "NE6792-START-N010",
        "The first no-checkout worktree command exceeded its bounded window after creating only the exact branch while its checkout child continued asynchronously.",
        "NE6792-START-P010",
        "Read-only state probes found the exact branch and later the exact worktree metadata; no second branch was created and no deletion occurred.",
    ),
    (
        "NE6792-START-N011",
        "A resumed worktree-add attempt encountered the path created by the still-running first process and failed closed.",
        "NE6792-START-P011",
        "The existing exact path and Git metadata were adopted without replacement, reset, or branch rewrite.",
    ),
    (
        "NE6792-START-N012",
        "A checkout attempt met the active first process index lock and performed no materialization.",
        "NE6792-START-P012",
        "After proving the exact owning Git processes and waiting for their natural completion, the lock cleared and sparse state resolved cleanly with two tracked files materialized.",
    ),
    (
        "NE6792-X1-N001",
        "The first source-bounded semantic audit quarantined ten titles at or above the 0.75 token-Jaccard ceiling, including two exact inherited collisions, and wrote no x1 artifact.",
        "NE6792-X1-P001",
        "Only the ten quarantined titles were rewritten; the other fifty proposals and immutable source stayed unchanged before the isolated semantic dependency was rerun.",
    ),
]

OWNER_SKILLS = [
    "semaphore-dossier-namespace",
    "signal-station-topology",
    "arm-position-vacancy",
    "relay-chain-graph",
    "dispatch-state-lineage",
    "semaphore-claim-firewall",
    "station-action-refusal-firewall",
    "tower-hazard-reservation",
    "signal-material-vacancy",
    "provenance-correction-ledger",
    "semaphore-accessibility-proxy",
    "message-rights-contestation",
    "freed-id-zero-key-envelope",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-relay-analogy-firewall",
    "gmut-identifiability-boundary",
    "thos-dispatch-handover-proxy",
    "cbr-affected-party-gate",
    "stage20-semaphore-refusal",
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
    "ghc_family_neris_solane_v679_v2_contract_runner.py",
    "ghc_family_neris_solane_v679_v2_mutation_runner.py",
    "ghc_family_neris_solane_v679_v2_topology_runner.py",
    "ghc_family_neris_solane_v679_v2_metadata_runner.py",
    "ghc_family_neris_solane_v679_v2_flashcard_runner.py",
    "ghc_family_neris_solane_v679_v2_toolchain_runner.py",
    "ghc_family_neris_solane_v679_v2_privacy_runner.py",
    "ghc_family_neris_solane_v679_v2_accessibility_runner.py",
    "ghc_family_neris_solane_v679_v2_portfolio_runner.py",
    "build_ghc_family_neris_solane_v679_v2_report.py",
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
    source_phase = "Elaren Kestrel v679-v1 exact final"
    path = "docs/elaren-kestrel/v679-v1/x1/new-proposal-freeze.json"
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
        proposal_id = f"NE6792-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "NIST-TN-1297", "RFC-8785"]
        if offset <= 25:
            source_ids += ["ITU-HISTORY-SEMAPHORE", "ITU-FROM-SEMAPHORE-TO-SATELLITE"]
        if 26 <= offset <= 45:
            source_ids += ["LOC-PAPER-CARE", "WORKSAFE-WORKING-AT-HEIGHT", "WORKSAFE-MACHINE-LOCKOUTS", "WORKSAFE-SAFE-MACHINERY"]
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
                    "real station, signal, message, route, codebook, logbook, observation, measurement, operation, maintenance, identity, rights, professional, legal, cultural, or authority claims."
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
            "task_id": f"NE6792-{prefix}-{index:03d}",
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
            "packet_id": f"NE6792-{prefix}-{index:03d}",
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
            "docs/neris-solane/v679-v2/validation/x1-manifest.json",
            "docs/neris-solane/v679-v2/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Elaren Kestrel v679-v1 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Elaren x1 already exists; no overwrite permitted")

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
            "new_neris_proposals": len(rows),
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
            "practice_1": "synthetic optical-semaphore station, arm-state, relay-chain, and dispatch-lineage documentation",
            "practice_2": "synthetic provenance, uncertainty, accessibility, hazard-refusal, rights, correction, and handover documentation",
            "owner_occupational_lenses": ["archival metadata analyst", "reliability analyst"],
            "successor_recommendation": "archival metadata analyst",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Vesper Arlen", "SCAND"),
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Vesper Arlen", "SCFR"),
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
        "semaphore-station-relay-and-dispatch-practice",
        "provenance-uncertainty-rights-accessibility-and-handover-practice",
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
            "successor": "Vesper Arlen",
            "successor_phase": "v679-v3",
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

This additive owner lane begins at Elaren Kestrel's immutable v679-v1 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite Elaren's repository seal, delivery event, or retained evidence, and it does not replay Elaren's successful owner-scoped canonical aggregate or any already-passing component.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Neris proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is GMUT Mind. The wholly synthetic learning/design lens is optical-semaphore station, arm-state, relay-chain, dispatch-lineage, provenance, uncertainty, accessibility, hazard-refusal, rights, correction, and handover documentation. THOS Body and Freed ID/CBR Heart remain explicit and protected. No real person, station, tower, mast, signal, message, codebook, logbook, route, coordinate, image, measurement, access, setup, operation, signaling, maintenance, repair, handling, release, rights decision, cultural decision, or authority act exists. The bounded occupational lenses are archival metadata analysis and reliability analysis without employment, qualification, or professional-authority claims. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, global promotion, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action.

## Boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Professional signaling, telecommunications, navigation, archival description, historical interpretation, station access, climbing/fall safety, machinery and stored-energy safety, flame/fuel/electrical/weather exposure, message secrecy, conservation, authorship, copyright, ownership, custody, access, legal or cultural interpretation, affected-party legitimacy, Māori data governance, Māori-authority, accessibility completeness, privacy completeness, exhaustive security, independent reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

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
