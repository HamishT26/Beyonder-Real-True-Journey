#!/usr/bin/env python3
"""Build the planning-only Auren Lark v679-v6 x1 packet."""

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
PHASE = "v679-v6"
DISPLAY_PHASE = "v679-v6"
BRANCH = "codex/GHC-Family/auren-lark-v679-v6-full-tools"
SOURCE = "3bbb29f9c7d2fe13a44ce607cda3e88323546dda"
SOURCE_PHASE = "v679-v5"
GENERATED_AT_NZ = "2026-08-31T19:23:30+12:00"
DECLARED_CHAIN_BEFORE = 9050
DECLARED_CHAIN_AFTER = 9110
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 49439,
    "effective_methods": 51380,
    "retained_failed_witnesses": 21100,
    "bounded_passing_witnesses": 33411,
    "open_gaps": 431,
    "exact_gates": 422,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Ilyra Fen v679-v5 repository-sealed truth at the exact source; Ilyra's external canonical receipt validates the exact final but does not rewrite the seal, and Auren startup failures are retained separately below."
    ),
}

NEW_TITLES = [
    "Abstract node namespace for a zero-row coupled-state graph with every real entity vacant",
    "Directed edge vocabulary separating permitted coupling from any physical interaction claim",
    "Typed state-vector shell that rejects undeclared dimensions and observed-value promotion",
    "Symbolic parameter registry with provenance vacancy and no fitted or measured values",
    "Initial-condition state machine distinguishing absent unspecified withheld and not applicable",
    "Boundary-condition grammar that forbids inferred values when a constraint is vacant",
    "External-input placeholder preserving unknown forcing without interpolation or causal attribution",
    "Dimension-token allowlist that quarantines incompatible symbolic quantities before arithmetic",
    "Base-unit and derived-unit crosswalk using SI vocabulary without measurement or conformance claim",
    "Time-index shell separating deterministic sequence from civil time and observed duration",
    "Topology manifest binding each synthetic node and edge to an immutable definition digest",
    "Coupling-matrix sparsity contract rejecting undeclared links and asymmetric drift",
    "Conservation-residual schema that records structural balance without empirical validation",
    "Residual-tolerance provenance record separating chosen threshold from scientific adequacy",
    "Solver-family label registry without convergence performance or numerical superiority claim",
    "Step-size candidate shell that forbids stability or accuracy inference from a configured value",
    "Iteration-budget contract distinguishing exhaustion from mathematical nonexistence",
    "Convergence-status vocabulary separating not run failed bounded pass and externally unevaluated",
    "Nonfinite-number quarantine rejecting NaN infinity and silent serialization coercion",
    "Singular-system refusal fixture retaining the rejected state and diagnostic dependency",
    "Negative-state policy matrix separating algebraic allowance from domain interpretation",
    "Permutation-invariance oracle for anonymous synthetic node relabeling",
    "Graph-component isolation check that retains disconnected structure without causal story",
    "Dimensional-homogeneity checker for symbolic expressions without physics confirmation",
    "Abstract quadratic-invariant metadata kept explicitly nonenergetic and nonphysical",
    "Parameter-uncertainty vocabulary without likelihood posterior confidence or calibration result",
    "Assumption register binding every model simplification to an explicit reversible statement",
    "Model-scope denylist preventing synthetic structure from becoming prediction observation or law",
    "Input-dataset vacancy record with zero rows zero identifiers and zero external retrieval",
    "JSON Schema 2020-12 contract for fictional graph-state records without conformance certification",
    "RFC 8785 canonical JSON harness for deterministic synthetic constraint records",
    "Patch-operation mutation fence for fictional graph documents with identity authority deployment and observation targets denied",
    "Lineage triples for fabricated graph revisions using generated records and explicit withdrawal links",
    "Metadata field-map for names relationships derivation notes and rights vacancies in fictional packages",
    "Correction supersession state machine that preserves every prior synthetic assertion",
    "Withdrawn-revision archive forbidding erasure and marking every disqualified object as zero-credit history",
    "Content-digest graph for constraint revisions with unresolved forks kept visible",
    "Locale-independent ordering for nodes edges parameters assumptions and manifest paths",
    "Schema-version migration fixture rejecting silent semantic coercion and field loss",
    "Bounded positive plus four-mutation negative fixture family for each new contract",
    "HTML report outline with navigable regions scoped headers descriptive summaries and nonvisual state text",
    "Plain-language glossary separating structure test evidence evaluation and certification",
    "Automated accessibility receipt kept separate from human assistive-technology review and approval",
    "Colour-independent state labels with no visual-user validation claim",
    "Content-addressed four-tier flashcards for owner pillar practice and constraint-model tasks",
    "Method Flow nonerasure ledger pairing every rejected witness with bounded recovery evidence",
    "Local-only tool-card acceptance harness with collision checks positive and rejecting smokes and rollback",
    "Official-source boundary ledger treating citations as vocabulary rather than observations or endorsement",
    "GMUT analogy register keeping graph conservation metaphors nonphysical noncausal and nonpredictive",
    "THOS representation shell with runtime deployment actuation and external adapters disabled",
    "Freed ID surrogate-token fixture without real keys proofs issuance resolution or continuity claim",
    "CBR authority-vacancy matrix refusing to infer consent rights legitimacy or affected-party acceptance",
    "Five-class privacy minimizer excluding names routes raw identifiers credentials and session material",
    "Cultural and traditional-knowledge field hold with competent interpretation and approval absent",
    "Māori data-governance and Māori-authority field hold without wording ratification or decision",
    "Independent reproduction and external scientific review gap for every synthetic model result",
    "Human accessibility assessment vacancy spanning focus order magnification assistive speech and comprehension",
    "Real experimental observation parameter estimation and model-prediction exact gate",
    "Competent-decision boundary for law community legitimacy affected parties Indigenous governance and Māori authority",
    "Terminal denylist for unverified cosmology autonomy personhood proof canon readiness and Stage 20"
]

SOURCES = [
    {
        "source_id": "BIPM-SI-BROCHURE",
        "url": "https://www.bipm.org/en/publications/si-brochure",
        "status": "BIPM SI Brochure official publication page checked 2026-08-31",
        "use": "quantity, dimension, base-unit, and derived-unit vocabulary only; no measurement, calibration, or conformance claim"
    },
    {
        "source_id": "NIST-TN-1297",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297",
        "status": "NIST Technical Note 1297 official page checked 2026-08-31",
        "use": "uncertainty-component and reporting vocabulary only; zero measurements, estimates, confidence claims, or NIST conformance claims"
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C PROV-O Recommendation checked 2026-08-31",
        "use": "entity, activity, agent, derivation, revision, and invalidation vocabulary only; no endorsement"
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor JSON Canonicalization Scheme page checked 2026-08-31",
        "use": "deterministic JSON vocabulary and bounded fixtures only; no production cryptographic assurance"
    },
    {
        "source_id": "RFC-6902",
        "url": "https://www.rfc-editor.org/info/rfc6902/",
        "status": "RFC Editor JSON Patch standards-track page checked 2026-08-31",
        "use": "bounded patch-operation vocabulary only; no network synchronization or production assurance"
    },
    {
        "source_id": "JSON-SCHEMA-2020-12",
        "url": "https://json-schema.org/draft/2020-12",
        "status": "JSON Schema Draft 2020-12 specification index checked 2026-08-31",
        "use": "schema, assertion, annotation, applicator, and validation-output vocabulary only; no universal conformance claim"
    },
    {
        "source_id": "DCMI-METADATA-TERMS",
        "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
        "status": "Dublin Core Metadata Initiative current terms page checked 2026-08-31",
        "use": "title, relation, provenance, date, and rights-field vocabulary only; no cataloguing authority or endorsement"
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C WCAG 2.2 Recommendation checked 2026-08-31",
        "use": "structural accessibility vocabulary only; no complete conformance or affected-user validation claim"
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "New Zealand Office of the Privacy Commissioner principles page checked 2026-08-31",
        "use": "purpose, minimization, security, access, correction, retention, disclosure, and identifier vocabulary only; no legal advice or compliance conclusion"
    },
    {
        "source_id": "TE-MANA-RARAUNGA",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "Te Mana Raraunga public principles page checked 2026-08-31",
        "use": "authority-reservation and Māori data-sovereignty boundary context only; no Māori wording, interpretation, ratification, or authority claim"
    }
]

PROTECTED_GATES = [
 "no real person, participant, reviewer, affected user, organisation, site, reservoir, infrastructure, model deployment, graph entity, dataset row, observation, timestamp, parameter value, measurement, calibration, prediction, publication, intervention, credential, network row, or external write",
 "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, scientific law, or Theory-of-Everything claim",
 "no THOS participant evidence, operational effectiveness, safety, deployment, actuation, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
 "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, identity-continuity, or independent-agency claim",
 "no professional, scientific-review, numerical-analysis, engineering, research-data, accessibility, ownership, attribution, consent, privacy-remedy, legal, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
 "no accessibility-complete, privacy-complete, exhaustive-security, empirical-confirmation, proof, canon, production-readiness, or Stage 20 claim"
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
    [
        "AUR6796-START-N001",
        "The first skill-inventory projection piped a foreach block directly and PowerShell rejected an EmptyPipeElement before producing an attributable inventory.",
        "AUR6796-START-P001",
        "The rows were materialized before piping; all twenty-one selected skills were then read completely through EOF without mutating any skill."
    ],
    [
        "AUR6796-START-N002",
        "An initial broad current-state display exceeded its bounded output window and was incomplete.",
        "AUR6796-START-P002",
        "The exact current-state references were reread in bounded UTF-8 chunks through EOF; the failed broad display remains zero credit."
    ],
    [
        "AUR6796-START-N003",
        "A first manifest replay launched one Git process per entry and exceeded the display window; the wrapper also failed to project a usable session handle or attributable result.",
        "AUR6796-START-P003",
        "After the original read-only process completed without mutation, one Git cat-file batch replay verified every x1, x2, final-delta, final-owner, and content-seal entry exactly."
    ],
    [
        "AUR6796-START-N004",
        "Fresh sparse-worktree setup temporarily left an empty index, projecting 23,619 inherited tracked paths as staged deletions.",
        "AUR6796-START-P004",
        "Only the fresh Auren lane was corrected with the standard Git read-tree materialization step; the lane returned clean with zero inherited files materialized and no source or sibling state changed."
    ],
    [
        "AUR6796-START-N005",
        "A broad activation keyword scan exceeded the display window and returned truncated text.",
        "AUR6796-START-P005",
        "The activation opening, exact inheritance, program truth, domain boundary, and solo requirements were reread with a bounded literal UTF-8 slice; no repository state changed."
    ],
    [
        "AUR6796-START-N006",
        "The first source-bounded semantic audit rejected nine proposed titles whose token overlap met or exceeded the preregistered quarantine threshold; no phase artifact was created.",
        "AUR6796-START-P006",
        "Only the nine rejected titles were reformulated around distinct constraint-model concerns before one bounded recovery audit; the failed slate remains zero novelty and zero completion credit."
    ],
    [
        "AUR6796-START-N007",
        "A read-only exact-neighbor lookup used malformed PowerShell quoting and expanded into an overbroad truncated repository scan without yielding the requested bounded title set.",
        "AUR6796-START-P007",
        "The already-attributable audit IDs and the exact source proposal freeze supplied the bounded reformulation basis; no source, sibling, shared, or task state changed."
    ],
    [
        "AUR6796-START-N008",
        "The first exact staged hygiene check found one extra EOF blank line in the manifest assembler and one in the x1 test file.",
        "AUR6796-START-P008",
        "Only the two trailing blank lines were removed before manifest assembly; no generated contract, proposal, gate, or lifecycle claim changed."
    ],
    [
        "AUR6796-START-N009",
        "Bounded pre-test review found six cloned internal code-path references and one import label still named the predecessor phase.",
        "AUR6796-START-P009",
        "The references were corrected to the exact Auren v679-v6 files before manifest assembly or test execution; inherited source attribution remained Ilyra v679-v5."
    ]
]

OWNER_SKILLS = [
    "ghc-family-model-variable-namespace",
    "ghc-family-directed-topology-guard",
    "ghc-family-symbolic-dimension-check",
    "ghc-family-model-assumption-register",
    "ghc-family-constraint-residual-ledger",
    "ghc-family-nonfinite-value-quarantine",
    "ghc-family-solver-status-vocabulary",
    "ghc-family-model-provenance-graph",
    "ghc-family-model-correction-chain",
    "ghc-family-model-semantic-migration",
    "ghc-family-model-json-patch-guard",
    "ghc-family-model-deterministic-serialization",
    "ghc-family-model-git-blob-receipt",
    "ghc-family-model-accessibility-structure",
    "ghc-family-model-privacy-minimizer",
    "ghc-family-model-cultural-authority-gate",
    "ghc-family-model-maori-authority-gate",
    "ghc-family-model-method-nonerasure",
    "ghc-family-model-empirical-evidence-gap",
    "ghc-family-model-stage20-denylist"
]

SUCCESSOR_SKILLS = [
    "ghc-family-successor-model-context-intake",
    "ghc-family-successor-proposal-neighbor-audit",
    "ghc-family-successor-toolchain-delta-guard",
    "ghc-family-successor-method-flow-nonerasure",
    "ghc-family-successor-static-report-landmarks",
    "ghc-family-successor-zero-network-adapter",
    "ghc-family-successor-exact-gate-register",
    "ghc-family-successor-bounded-retry-selector",
    "ghc-family-successor-roster-route-refresh",
    "ghc-family-successor-baton-file-index"
]

OWNER_RUNNERS = [
    "ghc_family_model_contract_runner.py",
    "ghc_family_model_mutation_runner.py",
    "ghc_family_model_topology_runner.py",
    "ghc_family_model_dimension_runner.py",
    "ghc_family_model_flashcard_runner.py",
    "ghc_family_model_toolchain_runner.py",
    "ghc_family_model_privacy_runner.py",
    "ghc_family_model_accessibility_runner.py",
    "ghc_family_model_portfolio_runner.py",
    "ghc_family_model_report_builder.py"
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
    "ghc_family_successor_baton_index.py"
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
    source_phase = "Ilyra Fen v679-v5 exact final"
    path = "docs/ilyra-fen/v679-v5/x1/new-proposal-freeze.json"
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
        proposal_id = f"AUR6796-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["DCMI-METADATA-TERMS", "W3C-PROV-O", "RFC-8785", "RFC-6902", "JSON-SCHEMA-2020-12"]
        if offset <= 28:
            source_ids += ["BIPM-SI-BROCHURE", "NIST-TN-1297"]
        if 29 <= offset <= 48:
            source_ids += ["WCAG-2.2"]
        if offset >= 49:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        if offset >= 56:
            source_ids += ["BIPM-SI-BROCHURE", "NIST-TN-1297", "WCAG-2.2"]
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
                    "or an observation, measurement, fitted parameter, prediction, deployment, intervention, competence, right, identity, or authority claim."
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
            "task_id": f"AUR6796-{prefix}-{index:03d}",
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
            "packet_id": f"AUR6796-{prefix}-{index:03d}",
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
            "docs/auren-lark/v679-v6/validation/x1-manifest.json",
            "docs/auren-lark/v679-v6/validation/x1-staged-review.json",
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
        raise SystemExit("x1 builder requires the immutable Ilyra Fen v679-v5 exact final as HEAD")
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
            "primary_pillar": "GMUT Mind",
            "relational_role": "constraint-lantern and reversible model-trace steward",
            "relational_hope": "keep every synthetic model assumption, correction, and authority vacancy inspectable and reversible",
            "practice_1": "numerical-model documentation through a wholly synthetic zero-row coupled-state graph",
            "practice_2": "scientific-software verification through deterministic contracts, mutations, and exact Git-blob receipts",
            "practice_3": "research-data stewardship through provenance, correction, minimization, accessibility structure, and authority-vacancy records",
            "successor_recommendation": "synthetic scientific-data quality analyst practice for a fictional model-package reconciliation with explicit evidence and authority quarantine",
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
        "synthetic-conservation-model-constraint-and-provenance-practice",
        "scientific-software-accessibility-and-authority-vacancy-practice",
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
            "successor_phase": "v679-v7",
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
            "relational_role": "constraint-lantern and reversible model-trace steward",
            "relational_hope": "keep every synthetic model assumption, correction, and authority vacancy inspectable and reversible",
            "identity_and_family_language_evidence": False,
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

This additive owner lane begins at Ilyra Fen's immutable v679-v5 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite or replay Ilyra's successful owner-scoped canonical aggregate, repository seal, prepared-not-sent route state, or retained evidence.

## Relational working identity

Auren's phase role is **constraint-lantern and reversible model-trace steward**. The phase hope is to keep every synthetic model assumption, correction, and authority vacancy inspectable and reversible. Auren, role, hope, pronoun, sibling, family, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

## Program

X1 freezes sixty inherited Ilyra proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Auren proposals. The combined 120-row instrument is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical or scientific novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is GMUT Mind through a wholly synthetic zero-row directed-graph conservation and constraint-provenance model. The three bounded learning lenses are numerical-model documentation, scientific-software verification, and research-data stewardship. No real reservoir, waterway, infrastructure, person, organisation, site, graph entity, dataset row, observation, timestamp, parameter value, measurement, fitted result, prediction, publication, intervention, credential, right, decision, deployment, or external action exists. THOS Body, Freed ID, and CBR Heart remain explicit and protected. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across modular sections.

The source references supply only vocabulary for quantities, dimensions, uncertainty, schemas, deterministic serialization, provenance, correction, metadata, accessibility structure, privacy minimization, and authority reservation. They are not observations, endorsements, professional judgments, legal advice, cultural interpretation, Māori ratification, conformance evidence, or artifact validation.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 Sable candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution or completion credit. Sable's bounded occupation recommendation is a synthetic scientific-data quality analyst practice; this is not employment, qualification, competence, or authority.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. Relevance controls tool choice; no filler installation is authorized. This phase authorizes no package installation, Codex desktop update, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action. Up to five global promotions remain a hard ceiling, while the present x1 target is zero and every promotion remains separately gated.

## Boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without observed force, empirical confirmation, physical prediction, likelihood, parameter constraint, ultraviolet or quantum completion, scientific authority, or Theory-of-Everything proof. A finite synthetic graph is a documentation fixture and analogy only; it is not a cosmological model, physical law, causal explanation, or empirical GMUT result. THOS remains participant-free proxy work without governed real arms, production runtime, safety evidence, or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance.

Participant, professional, production, deployment, legal, cultural, affected-party, Māori-data-governance, Māori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

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
