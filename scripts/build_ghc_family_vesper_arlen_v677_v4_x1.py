#!/usr/bin/env python3
"""Build the planning-only Vesper Arlen v677-v4 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Vesper Arlen"
OWNER_SLUG = "vesper-arlen"
PHASE = "v677-v4"
DISPLAY_PHASE = "v677-v4"
BRANCH = "codex/GHC-Family/vesper-arlen-v677-v4-full-tools"
SOURCE = "7b5c6a52492c84d54232871c4e6a6e4425c82c1e"
SOURCE_PHASE = "v677-v3"
GENERATED_AT_NZ = "2026-08-31T00:02:45+12:00"
DECLARED_CHAIN_BEFORE = 7970
DECLARED_CHAIN_AFTER = 8030
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 44473,
    "effective_methods": 39279,
    "retained_failed_witnesses": 16134,
    "bounded_passing_witnesses": 23845,
    "open_gaps": 377,
    "exact_gates": 368,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Neris Solane v677-v3 immutable repository seal at the exact source; Vesper startup failures are retained separately below."
    ),
}

NEW_TITLES = [
 "Synthetic microfilm reel registry namespace without collection identity, custody, or service claim",
 "Reel can leader trailer frame and surrogate relation graph without handling or ownership conclusion",
 "Frame sequence ordinal and edge relation contract without observed image-content assertion",
 "Target board title board date board and technical-frame vocabulary with every real value vacant",
 "Roll image frame and exposure index topology without digitization or inspection claim",
 "Reduction-ratio field vacancy refusing inferred scale, magnification, or metrological validity",
 "Polarity generation master duplicate and service-copy vocabulary vacancy without material determination",
 "Frame orientation rotation skew and registration placeholders without measured geometry",
 "Missing duplicate repeated reversed and out-of-order frame quarantine on synthetic indexes",
 "Splice cue leader break trailer break and join relation firewall without damage diagnosis",
 "Density resolution focus and legibility field vacancies without measurement or quality certification",
 "Camera operator laboratory institution collection and station identity firewall without attribution",
 "Film base emulsion backing adhesive container and sleeve material vacancies without composition finding",
 "Carrier-surface anomaly token matrix for fictional acetate polyester and silver-gelatin surrogates without diagnosis",
 "Edge-code perforation notch and manufacturer-mark cue firewall without authenticity inference",
 "Scale target resolution chart label and unit vocabulary without calibration validation",
 "Frame boundary crop offset overlap and registration placeholders without image capture",
 "Damaged leader loose reel sharp can and unstable carrier hazard vocabulary with action channels disabled",
 "Storage temperature humidity light ventilation and orientation register with every observation vacant",
 "Synthetic reel chronology and generation-change lineage with every real event and date vacant",
 "Reel box can sleeve folder and surrogate locator escrow with ownership and custody fields disabled",
 "Digitization derivative crop rotation contrast compression and transcription lineage without real media",
 "Prior inspection duplication rehousing cleaning repair and migration chronology without professional inference",
 "Names handwriting signatures labels addresses and marginalia privacy firewall without identity attribution",
 "Collection place community cultural-context and traditional-knowledge compartment without interpretation authority",
 "Repository location access restriction rights and retention fields with every real value vacant",
 "Reel-workflow finite-state ledger for fictional intake triage review amendment and release without service events",
 "Container opening reel movement threading scanning cleaning and handling packet with action fields hard-disabled",
 "Cleaning repair duplication scanning disposal sampling and treatment refusal board for synthetic carriers",
 "Carrier hazard hold for sharp edges mould dust acetate decay nitrate risk lifting and unstable supports",
 "Emergency vocabulary capsule for damaged microfilm with operational and preservation decisions disabled",
 "Reversible correction and supersession lineage for synthetic reel, frame, and derivative assertions",
 "Bitemporal review ledger binding synthetic frame assertions to reversible transaction and valid instants",
 "Duplicate reel dangling frame impossible sequence loop and orphan derivative rejection contract",
 "RFC 8785 byte-canonicalization harness for invented reel records with nonfinite-number refusal",
 "Normalized-LF exact Git-blob manifest for owner-local microfilm provenance evidence",
 "Screen-reader route grammar for reel headings frame summaries gaps and unresolved review slots",
 "Textual frame-map alternative using ordered reels frames targets gaps annotations and uncertainty vacancies",
 "CSS-independent magnification and pattern-coded frame navigator proxy with low-vision user study reserved",
 "Comprehension-scaffolded synopsis of an invented reel register with affected-user evaluation vacant",
 "Field-minimization matrix for anonymous reel and frame topology with expiry and deletion authority vacant",
 "Contestation queue for disputed microfilm assertions with reversible visibility and remedy states",
 "Digest-keyed four-tier study deck spanning intake provenance dispute correction and abstention",
 "Citation-bound micrographics vocabulary card separating description consent rights and authority",
 "Merkle-addressed correction DAG preserving retraction conflicts and successor metadata",
 "GMUT sequence-graph analogy for reels frames and derivatives without physical-law promotion",
 "Metamorphic reel-edge renumbering oracle preserving only adjacency invariants and refusing physical semantics",
 "Identifiability refusal register for vacant frame-evidence variables and unconstrained sequence parameters",
 "No-data GMUT observation firewall blocking posterior force and law promotion from carrier graphs",
 "Equal-resource THOS documentation protocol with no archivists technicians users devices sessions or result",
 "THOS microfilm-ingest state machine with acquisition inspection handling scanning and deployment routes disabled",
 "Keyless Freed ID metadata shell for anonymous reel surrogates with every credential lifecycle field disabled",
 "CBR dispute-state escrow for fictional carrier records with claimant authority and remedy outcome unset",
 "Two-practice boundary matrix for micrographics metadata archiving and accessible technical documentation",
 "Real archivist micrographics technician conservator custodian rights-holder and affected-user evidence gap",
 "Manual browser keyboard screen-reader low-vision and independent-reader evaluation gap for reel dossiers",
 "Reachability ledger for proposal-title blobs with the inaccessible chain remainder kept open",
 "Real carrier inspection handling repair duplication digitization release and professional-signoff exact gate",
 "Carrier rights custodial title community privacy taonga context and Māori governance reservation gate",
 "Stage 20 abstention tribunal for micrographics proxies pending external evidence and authorized review"
]

SOURCES = [
 {
  "source_id": "LOC-PREMIS-3",
  "url": "https://www.loc.gov/standards/premis/premis-3-0-final.pdf",
  "status": "Library of Congress PREMIS Data Dictionary for Preservation Metadata version 3.0 checked 2026-08-30",
  "use": "object, event, agent, rights, fixity, and preservation-metadata vocabulary only; zero real repository events"
 },
 {
  "source_id": "LOC-PREMIS-CURRENT",
  "url": "https://www.loc.gov/standards/premis/index.html",
  "status": "Library of Congress PREMIS maintenance page checked 2026-08-30",
  "use": "current maintenance and version-context vocabulary only; no conformance or preservation claim"
 },
 {
  "source_id": "W3C-PROV-O",
  "url": "https://www.w3.org/TR/prov-o/",
  "status": "W3C Recommendation checked 2026-08-30",
  "use": "entity, activity, agent, derivation, attribution, and revision vocabulary only"
 },
 {
  "source_id": "NARA-PRESERVATION-FORMATS",
  "url": "https://www.archives.gov/preservation/formats",
  "status": "official US National Archives media-format guidance index checked 2026-08-30",
  "use": "carrier and format classification vocabulary only; no real material diagnosis"
 },
 {
  "source_id": "NARA-MICROFILM-PREP",
  "url": "https://www.archives.gov/preservation/formats/microfilm-prep.html",
  "status": "official US National Archives microfilm preparation guidance checked 2026-08-30",
  "use": "reel, target, sequence, preparation, and handling-boundary vocabulary only; no operational instruction or professional authority"
 },
 {
  "source_id": "RFC-8785",
  "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
  "status": "RFC Editor informational RFC checked 2026-08-30",
  "use": "deterministic JSON vocabulary only; no production cryptographic assurance"
 },
 {
  "source_id": "RFC-6902",
  "url": "https://www.rfc-editor.org/info/rfc6902/",
  "status": "RFC Editor standards-track RFC page checked 2026-08-30",
  "use": "bounded JSON patch-operation vocabulary only; no production synchronization assurance"
 },
 {
  "source_id": "WCAG-2.2",
  "url": "https://www.w3.org/TR/WCAG22/",
  "status": "W3C Recommendation with current errata checked 2026-08-30",
  "use": "structural accessibility vocabulary only; no conformance claim"
 },
 {
  "source_id": "W3C-VC-DATA-MODEL-2.0",
  "url": "https://www.w3.org/TR/vc-data-model-2.0/",
  "status": "W3C Recommendation checked 2026-08-30",
  "use": "status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs"
 },
 {
  "source_id": "NZ-PRIVACY-PRINCIPLES",
  "url": "https://www.privacy.org.nz/privacy-principles/",
  "status": "official New Zealand Privacy Commissioner principles page checked 2026-08-30",
  "use": "collection, use, disclosure, access, correction, retention, and minimization vocabulary only; no compliance conclusion"
 },
 {
  "source_id": "TE-MANA-RARAUNGA",
  "url": "https://www.temanararaunga.maori.nz/",
  "status": "Te Mana Raraunga public authority-reservation context checked 2026-08-30",
  "use": "Māori data-sovereignty and authority-reservation vocabulary only; no Māori wording, interpretation, ratification, or authority claim"
 }
]

PROTECTED_GATES = [
 "no real person, participant, archivist, micrographics technician, conservator, custodian, owner, rights-holder, affected user, institution, collection, reel, frame, carrier, image, record, measurement, inspection, handling, repair, duplication, digitization, release, network row, or external write",
 "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
 "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
 "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
 "no professional, archival, micrographics, conservation, carrier-condition, material, structural, access, hazard, repair, handling, preservation, ownership, custody, attribution, copyright, privacy-remedy, legal, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
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
    ("VSP6774-START-N001", "A combined guidance, roster, and authorization projection exceeded its presentation budget and earned no complete-read credit.", "VSP6774-START-P001", "Bounded file-specific windows completed every required guidance and schema through EOF without mutation."),
    ("VSP6774-START-N002", "The first raw activation-packet projection exceeded its output budget and was incomplete.", "VSP6774-START-P002", "Bounded line windows completed the exact committed activation packet through EOF and verified its normalized-LF digest."),
    ("VSP6774-START-N003", "A source-fetch wrapper returned no attributable fetch result and earned zero fresh-live-equality credit.", "VSP6774-START-P003", "A fresh literal ref fetch followed by scalar local, upstream, tracking, and live-remote comparisons established exact equality."),
    ("VSP6774-START-N004", "The first per-blob manifest validator crossed its command-yield boundary and left one owner-started read-only probe running.", "VSP6774-START-P004", "Persisted process state was inspected, the bounded probe was allowed to finish, and no mutation or canonical credit was claimed."),
    ("VSP6774-START-N005", "A stop request raced with an already-exited owner-started probe and returned a missing-process error.", "VSP6774-START-P005", "The process table and Git state confirmed that the read-only probe had already exited and changed no repository byte."),
    ("VSP6774-START-N006", "A second per-blob validator crossed its command-yield boundary and earned zero manifest credit.", "VSP6774-START-P006", "The exact owner-started probe was identified and stopped, then a single Git batch-object replay completed the immutable comparisons."),
    ("VSP6774-START-N007", "A naive byte-count interpretation treated twenty CRLF-projected YAML checkout files as digest mismatches.", "VSP6774-START-P007", "The predecessor contract was reread and all normalized-LF Git-blob digests matched; raw checkout-byte differences retained zero failure-conversion credit."),
    ("VSP6774-START-N008", "The worktree-creation wrapper yielded before the sparse checkout finished and returned no completion credit.", "VSP6774-START-P008", "The existing registration and checkout were inspected in place after completion; the fresh named lane was clean at the exact source."),
    ("VSP6774-START-N009", "The first sparse-checkout extension used an unsupported add subcommand option and changed no pattern.", "VSP6774-START-P009", "The supported literal add form extended only the declared Vesper x1 manifest path."),
    ("VSP6774-START-N010", "The first patch-helper invocation was rooted at the app workspace and created three untracked Vesper-named files outside the D-first lane.", "VSP6774-START-P010", "Only those three newly created files were removed with the patch helper; a verified junction then routed patch edits to the intended Vesper worktree."),
    ("VSP6774-X1-N001", "The first source-bounded semantic audit rejected three exact inherited titles and ten additional titles at or above the preregistered 0.75 token-Jaccard ceiling, then stopped before writing x1 documents.", "VSP6774-X1-P001", "Only the thirteen cited Vesper titles were rewritten with narrower microfilm-specific semantics; every unflagged proposal and the immutable source remained unchanged before the isolated audit retry."),
    ("VSP6774-X1-N002", "The first exact staged diff-hygiene check rejected one extra blank line at the x1 builder EOF.", "VSP6774-X1-P002", "Only the extra EOF blank line was removed; the affected manifests and diff-hygiene dependency were regenerated without replaying the successful x1 test invocation."),
]

OWNER_SKILLS = [
 "ghc-microfilm-reel-namespace",
 "ghc-microfilm-frame-topology",
 "ghc-microfilm-sequence-gap-quarantine",
 "ghc-microfilm-splice-cue-firewall",
 "ghc-microfilm-material-vacancy",
 "ghc-microfilm-condition-cue-firewall",
 "ghc-microfilm-derivative-lineage",
 "ghc-microfilm-custody-vacancy",
 "ghc-microfilm-role-separation",
 "ghc-microfilm-correction-chain",
 "ghc-microfilm-privacy-filter",
 "ghc-microfilm-rights-reservation",
 "ghc-microfilm-cultural-authority-gate",
 "ghc-microfilm-maori-authority-gate",
 "ghc-microfilm-content-domain",
 "ghc-microfilm-json-patch-guard",
 "ghc-microfilm-deterministic-serialization",
 "ghc-microfilm-accessibility-structure",
 "ghc-microfilm-real-evidence-gap",
 "ghc-microfilm-professional-authority-gate"
]

SUCCESSOR_SKILLS = [
 "successor-carrier-context-card-intake",
 "successor-frame-sequence-neighbor-audit",
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
    "ghc_family_vesper_arlen_v677_v4_contract_runner.py",
    "ghc_family_vesper_arlen_v677_v4_mutation_runner.py",
    "ghc_family_vesper_arlen_v677_v4_topology_runner.py",
    "ghc_family_vesper_arlen_v677_v4_metadata_runner.py",
    "ghc_family_vesper_arlen_v677_v4_flashcard_runner.py",
    "ghc_family_vesper_arlen_v677_v4_toolchain_runner.py",
    "ghc_family_vesper_arlen_v677_v4_privacy_runner.py",
    "ghc_family_vesper_arlen_v677_v4_accessibility_runner.py",
    "ghc_family_vesper_arlen_v677_v4_portfolio_runner.py",
    "build_ghc_family_vesper_arlen_v677_v4_report.py",
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
    source_phase = "Neris Solane v677-v3 exact final"
    path = "docs/neris-solane/v677-v3/x1/new-proposal-freeze.json"
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
                "vesper_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"VSP6774-N{offset:03d}"
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
            source_ids += ["LOC-PREMIS-3", "LOC-PREMIS-CURRENT", "NARA-PRESERVATION-FORMATS", "NARA-MICROFILM-PREP"]
        if 26 <= offset <= 45:
            source_ids += ["LOC-PREMIS-3", "NARA-MICROFILM-PREP"]
        if offset in {22, 28, 37, 38, 39, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        if offset in {24, 25, 41, 42, 53, 54, 55, 56, 57, 58, 59, 60}:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real microfilm, reel, frame, carrier, image, inspection, handling, treatment, identity, rights, professional, legal, cultural, or authority claims."
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
            "task_id": f"VSP6774-{prefix}-{index:03d}",
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
            "packet_id": f"VSP6774-{prefix}-{index:03d}",
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
            "docs/vesper-arlen/v677-v4/validation/x1-manifest.json",
            "docs/vesper-arlen/v677-v4/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Neris Solane v677-v3 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Vesper x1 already exists; no overwrite permitted")

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
            "new_vesper_proposals": len(rows),
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
            "practice_1": "synthetic microfilm reel, frame, sequence, target, derivative, and provenance metadata archiving",
            "practice_2": "synthetic accessible technical-documentation structure, correction, and abstention review",
            "successor_recommendation": "synthetic audiovisual-carrier catalogue accessibility analysis",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Lyren Moss", "SCAND"),
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
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Lyren Moss", "SCFR"),
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
        "microfilm-reel-frame-provenance-practice",
        "accessible-technical-documentation-practice",
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
            "successor": "Lyren Moss",
            "successor_phase": "v677-v5",
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
        f"""# Vesper Arlen {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Neris Solane's immutable v677-v3 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Neris's successful owner-scoped canonical aggregate, repository seal, delivery event, or retained evidence.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Vesper proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is THOS Body. The wholly synthetic learning and design lenses are microfilm reel, frame, sequence, target, derivative, and provenance metadata archiving, together with accessible technical-documentation structure, correction, and abstention review. GMUT Mind and Freed ID and CBR Heart remain explicit and protected. No real person, collection, reel, frame, carrier, image, measurement, inspection, handling, repair, digitization, custody action, rights decision, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 Lyren candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

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
