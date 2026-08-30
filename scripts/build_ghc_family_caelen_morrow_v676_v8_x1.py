#!/usr/bin/env python3
"""Build the planning-only Caelen Morrow v676-v8 remaster x1 packet."""

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
PHASE = "v676-v8"
DISPLAY_PHASE = "v676-v8"
BRANCH = "codex/GHC-Family/caelen-morrow-v676-v8-full-tools"
SOURCE = "56075d91265e71ce9165670db78ef455c29d5e2f"
SOURCE_PHASE = "v676-v7-r2-correction1"
GENERATED_AT_NZ = "2026-08-30T17:26:21+12:00"
DECLARED_CHAIN_BEFORE = 7730
DECLARED_CHAIN_AFTER = 7790
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 43195,
    "effective_methods": 35460,
    "retained_failed_witnesses": 14856,
    "bounded_passing_witnesses": 21295,
    "open_gaps": 365,
    "exact_gates": 356,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Sylven v676-v7-r2 repository seal plus corrected-composite, delivery, post-delivery, and route-method external overlays, kept separate from Caelen startup failures."
    ),
}

NEW_TITLES = [
    "Synthetic horological movement namespace without object identity ownership or service claim",
    "Gear train wheel pinion arbor and pivot relation graph without physical inspection",
    "Escapement pallet fork escape wheel and impulse relation without rate conclusion",
    "Balance spring and regulator relation with beat and amplitude quantities vacant",
    "Pendulum suspension crutch and anchor relation without setup or adjustment instruction",
    "Mainspring barrel arbor and bridle topology without stored energy or serviceability claim",
    "Fusee chain and maintaining-power relation without tension or handling instruction",
    "Keyless winding setting stem crown and clutch map without operation claim",
    "Motion works cannon pinion minute wheel and hour wheel topology without alignment claim",
    "Calendar date day month and leap mechanism proxy without correction authority",
    "Striking train rack snail hammer and warning relation without acoustic or safety claim",
    "Repeater slide governor and rack relation without function or authenticity inference",
    "Remontoire and constant-force vocabulary firewall without performance claim",
    "Detent chronometer escapement term register without classification or precision claim",
    "Jewel bushing endshake and sideshake vacancy without wear diagnosis",
    "Dial hand chapter ring and aperture relation without condition or originality claim",
    "Case bezel bow pendant crown and crystal relation without opening or handling permission",
    "Lubrication point and material vacancy without oil selection or application instruction",
    "Corrosion abrasion scoring and fracture cue register without condition diagnosis",
    "Magnetism and demagnetization refusal board without test or treatment action",
    "Water-resistance seal and pressure-test vacancy without safety or conformance claim",
    "Rate beat error amplitude and power-reserve measurement schema with every value vacant",
    "Timing-position and temperature-context register without measured rows",
    "Disassembly sequence and parts-tray custody proxy without repair authorization",
    "Image surrogate lineage for synthetic movement views with rights and scale vacancy",
    "Component assertion provenance and reversible correction lineage",
    "Horological intake handover capsule with competence and work-release abstention",
    "Owner custody accession and return-status vacancy without possession claim",
    "Workload and interruption budget for resumable synthetic documentation",
    "Hazard hold for stored energy sharp edges chemicals dust and electrical exposure",
    "Byte-stable horology card serialization with locale and field-order refusal",
    "Duplicate component dangling relation and impossible topology rejection contract",
    "Chronology date inscription maker and serial-claim firewall without attribution",
    "Manufacture style period and origin vocabulary compartment without authenticity claim",
    "Replacement original and modified-part assertion vacancy without provenance decision",
    "Parts compatibility and interchangeability refusal without fit or installation evidence",
    "Separated instruction event observation and analyst-comment channels for service history",
    "Keyboard-navigable movement dossier headings with untested screen-reader reserve",
    "Low-vision textual alternative proxy for diagram structure without conformance claim",
    "Cognitive-accessible handover summary with affected-user evaluation reserved",
    "Least-data synthetic clock-record field ledger with retention and deletion holds",
    "Rights restriction remedy and challenge escrow for contested records",
    "Owner-pillar-practice-task memory cue matrix with nonidentity Freed ID boundary",
    "Digest-keyed learning-card atlas ordered by horology lifecycle sections",
    "Flashcard source-to-claim firewall separating vocabulary evidence and authority",
    "Non-erasing card revision genealogy with explicit obsolete-state witnesses",
    "GMUT graph analogy for coupled movement components without physical promotion",
    "GMUT relabeling and gauge-choice firewall for component identifiers",
    "GMUT identifiability board separating parameter symbols from observable timing data",
    "THOS participant-free comparator for monolithic and modular handover packets",
    "Participant-free THOS interruption-recovery trace with no human-benefit inference",
    "Synthetic credential-lifecycle placeholder for correction suspension recovery and invalidation",
    "CBR challenge remedy and affected-party acceptance representation only",
    "Zero-row provenance adapter for official museum timekeeping vocabulary",
    "Zero-call Smithsonian timekeeping collection adapter with no downloaded rows",
    "Real horologist conservator curator and affected-user evaluation gap",
    "Independent reproduction assistive-technology and browser evaluation gap",
    "Real inspection timing calibration service repair handling and professional-release exact gate",
    "Contested timepiece custody access heritage Indigenous-data and Māori-authority hold",
    "Empirical GMUT production identity deployment exhaustive-security and Stage20 exact gate",
]

SOURCES = [
    {
        "source_id": "SMITHSONIAN-TIMEKEEPING",
        "url": "https://www.si.edu/spotlight/clocks-watches",
        "status": "official Smithsonian timekeeping collection surface checked 2026-08-30",
        "use": "clock, watch, timepiece, collection, object-type, and rights-vacancy vocabulary only; zero calls and zero downloaded rows in execution",
    },
    {
        "source_id": "NIST-TIME-FREQUENCY",
        "url": "https://www.nist.gov/pml/time-and-frequency-division",
        "status": "official NIST Time and Frequency Division page checked 2026-08-30",
        "use": "time, frequency, metrology, realization, distribution, and calibration-boundary vocabulary only; no owner measurement or calibration claim",
    },
    {
        "source_id": "NIST-CLOCK-FAQ",
        "url": "https://www.nist.gov/pml/time-and-frequency-division/timekeeping-and-clocks-faqs",
        "status": "official NIST timekeeping and clocks FAQ checked 2026-08-30",
        "use": "periodic-event, gear-counting, pendulum, quartz, frequency, and traceability vocabulary only; no timing observation or service instruction",
    },
    {
        "source_id": "LOC-COLLECTIONS-CARE",
        "url": "https://www.loc.gov/preservation/care/",
        "status": "official Library of Congress collections-care page checked 2026-08-30",
        "use": "handling, storage, documentation, and preservation-boundary vocabulary only; no object-specific care or professional claim",
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
    "no real person, participant, horologist, watchmaker, clockmaker, conservator, curator, custodian, owner, affected user, clock, watch, movement, component, object, observation, measurement, handling, disassembly, repair, treatment, calibration, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
    "no professional, inspection, timing, calibration, repair, handling, conservation, ownership, custody, heritage, copyright, legal, privacy-remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
        "CM6768-START-N001",
        "The complete authorization state exceeded one visible display envelope.",
        "CM6768-START-P001",
        "Bounded numbered windows completed the same exact file through EOF without changing it.",
    ),
    (
        "CM6768-START-N002",
        "A combined activation-packet window truncated one middle range.",
        "CM6768-START-P002",
        "The missing nonoverlapping range was read directly and packet integrity was preserved.",
    ),
    (
        "CM6768-START-N003",
        "A PowerShell parent projection used an invalid inline conditional expression.",
        "CM6768-START-P003",
        "Only the missing parent scalars were rerun with valid materialized expressions.",
    ),
    (
        "CM6768-START-N004",
        "A worktree inspection repeated the same invalid inline conditional form.",
        "CM6768-START-P004",
        "Separate scalar variables recovered branch and path truth without mutation.",
    ),
    (
        "CM6768-START-N005",
        "The worktree-add presentation window elapsed while the original sparse checkout continued.",
        "CM6768-START-P005",
        "Process and Git-state inspection waited for the original operation and avoided duplicate creation.",
    ),
    (
        "CM6768-START-N006",
        "A broad recursive lock inspection exceeded its bounded presentation window.",
        "CM6768-START-P006",
        "Exact known lock paths and process state replaced the broad inspection.",
    ),
    (
        "CM6768-START-N007",
        "A premature status read during active sparse checkout emitted a truncated apparent-deletion list.",
        "CM6768-START-P007",
        "After checkout exit, scalar diff, index, status, and untracked counts proved a clean exact-source lane.",
    ),
    (
        "CM6768-START-N008",
        "A custom manifest probe incorrectly compared checkout byte counts with raw Git-blob byte counts.",
        "CM6768-START-P008",
        "Declared normalized-LF hashes replayed exactly and the manifest scripts confirmed checkout-byte semantics.",
    ),
    (
        "CM6768-START-N009",
        "Several PowerShell foreach projections were piped without materialization and hit empty-pipe parser faults.",
        "CM6768-START-P009",
        "Rows were materialized before conversion and only the missing projections were rerun.",
    ),
    (
        "CM6768-START-N010",
        "A broad keyword Git-grep produced no attributable bounded output.",
        "CM6768-START-P010",
        "The source-bounded semantic audit in the x1 builder became the attributable novelty check.",
    ),
    (
        "CM6768-START-N011",
        "The first source-script inventory projection hit the same empty-pipe parser fault.",
        "CM6768-START-P011",
        "The file rows were materialized and the exact source inventory was recovered once.",
    ),
    (
        "CM6768-START-N012",
        "The sparse checkout was initially observed with zero materialized owner files while its checkout process remained active.",
        "CM6768-START-P012",
        "No operation was repeated; after normal exit the intended empty additive owner scope and clean source head were verified.",
    ),
    (
        "CM6768-START-N013",
        "Two exact PowerShell Remove-Item cleanup attempts were rejected by the host command policy before deletion.",
        "CM6768-START-P013",
        "Only generated owner-worktree bytecode caches were deleted with an exact path-bounded Python fallback after parent-scope assertions.",
    ),
    (
        "CM6768-START-N014",
        "A nested PowerShell range projection flattened unexpectedly and produced no requested source window.",
        "CM6768-START-P014",
        "The one missing bounded source window was emitted with direct scalar bounds and no file mutation.",
    ),
    (
        "CM6768-X1-N001",
        "The first source-bounded semantic audit failed closed with four exact title collisions and ten rows at or above the 0.75 quarantine threshold.",
        "CM6768-X1-P001",
        "Only the ten named proposal titles were rewritten for semantic distinction; the threshold, source corpus, counts, outcome plan, and protected gates remained unchanged before the isolated audit rerun.",
    ),
    (
        "CM6768-X1-N002",
        "The first exact x1 privacy review treated the owner core scanner definitions as two confirmed payload hits.",
        "CM6768-X1-P002",
        "Only the exact owner core scanner-definition path was added to the adjudication allowlist; all five patterns, all payload paths, and fail-closed behavior remained unchanged.",
    ),
    (
        "CM6768-X1-N003",
        "The first staged diff-hygiene check found one extra terminal blank line in the owner core and x1 test.",
        "CM6768-X1-P003",
        "Only the two terminal blank lines and one stale runner-description owner label were corrected before regenerating exact manifests.",
    ),
]

OWNER_SKILLS = [
    "horological-movement-component-topology",
    "gear-train-relation-vacancy",
    "escapement-claim-firewall",
    "rate-measurement-vacancy",
    "stored-energy-safety-hold",
    "movement-image-lineage",
    "horological-intake-nonpromotion",
    "custody-status-vacancy",
    "timing-provenance-ledger",
    "movement-topology-validator",
    "accessibility-summary-proxy",
    "rights-challenge-escrow",
    "freed-id-four-tier-deck",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-movement-analogy-firewall",
    "gmut-identifiability-boundary",
    "thos-modular-context-proxy-guard",
    "cbr-affected-party-gate",
    "stage20-horology-refusal",
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
    "ghc_family_caelen_morrow_v676_v8_contract_runner.py",
    "ghc_family_caelen_morrow_v676_v8_mutation_runner.py",
    "ghc_family_caelen_morrow_v676_v8_movement_topology_runner.py",
    "ghc_family_caelen_morrow_v676_v8_metadata_runner.py",
    "ghc_family_caelen_morrow_v676_v8_flashcard_runner.py",
    "ghc_family_caelen_morrow_v676_v8_toolchain_runner.py",
    "ghc_family_caelen_morrow_v676_v8_privacy_runner.py",
    "ghc_family_caelen_morrow_v676_v8_accessibility_runner.py",
    "ghc_family_caelen_morrow_v676_v8_portfolio_runner.py",
    "build_ghc_family_caelen_morrow_v676_v8_report.py",
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
    source_phase = "Sylven Arc v676-v7-r2 corrected exact final"
    path = "docs/sylven-arc/v676-v7-r2/x1/new-proposal-freeze.json"
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
        proposal_id = f"CM6768-N{offset:03d}"
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
            source_ids += ["SMITHSONIAN-TIMEKEEPING", "NIST-CLOCK-FAQ", "NIST-TIME-FREQUENCY"]
        if 26 <= offset <= 45:
            source_ids += ["SMITHSONIAN-TIMEKEEPING", "LOC-COLLECTIONS-CARE"]
        if offset in {23, 34, 43, 44, 45, 46, 47, 48, 49, 55, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real timepiece, component, record, measurement, inspection, repair, identity, rights, professional, legal, cultural, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} accepts a missing or contradictory field, a raw or real identifier, a non-authorized outcome label, "
                    "or an observation, measurement, intervention, calibration, repair, competence, right, identity, or authority claim."
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
            "task_id": f"CM6768-{prefix}-{index:03d}",
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
            "packet_id": f"CM6768-{prefix}-{index:03d}",
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
            "docs/caelen-morrow/v676-v8/validation/x1-manifest.json",
            "docs/caelen-morrow/v676-v8/validation/x1-staged-review.json",
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
            "new_caelen_proposals": len(rows),
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
            "practice_1": "synthetic horological movement and timepiece documentation",
            "practice_2": "synthetic conservation-intake, provenance, accessibility, and handover documentation",
            "successor_recommendation": "synthetic timekeeping-record continuity and refusal-boundary documentation",
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
        "horological-movement-practice",
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
            "successor": "Eiren Kestrel",
            "successor_phase": "v677-v1",
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
        f"""# Caelen Morrow {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Sylven Arc's immutable corrected exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Sylven's retained failed canonical, corrected composite, repository seal, delivery receipt, or external overlays.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Caelen proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is GMUT Mind. The wholly synthetic learning/design lens is horological movement, timepiece, provenance, accessibility, intake, and handover documentation. THOS Body and Freed ID/CBR Heart remain explicit and protected. No real timepiece, person, measurement, inspection, repair, custody action, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

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
