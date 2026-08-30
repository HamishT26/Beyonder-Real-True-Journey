#!/usr/bin/env python3
"""Build Caelen Ash v678-v1 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Caelen Ash"
PHASE = "v678-v1"
SOURCE = "af26e6c68f43aa104164490edda08f2497f21deb"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v677-v8-full-tools"
SOURCE_ROOT = "668abe7b09dbdde9da5d1d806920938abcb1cca8"
SOURCE_X1 = "24eadfbbdbd057dddb136bb43b731ea1433b2098"
SOURCE_EVIDENCE = "a9dadf0312582aa1528781bb65ea9c9f5cbd6685"
SOURCE_PACKET = "docs/sable-rook/v677-v8/final/final-integrated-overview.md"
SOURCE_PACKET_SHA256 = "1ebdc6939f99bd93021daf713cce24cefcaec4552aa4fb177233f4dff8163796"
SOURCE_CANONICAL_RECEIPT_SHA256 = "57495b7c38b6ec891b8369d647738e523524ff9f2b019a40d4e99d732a6aeb22"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "836d8a35723a477ff4487c58dfbd3bb5f78751f8f5fcba6fd805197eba211612"
TARGET_BRANCH = "codex/GHC-Family/caelen-ash-v678-v1-full-tools"
RECORDED_UTC = "2026-08-30T17:56:00+00:00"
RECORDED_NZ = "2026-08-31T05:56:00+12:00"
SOURCE_PROPOSAL_CHAIN = 8270
PLANNED_PROPOSAL_CHAIN = 8330

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "caelen-ash" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
VALIDATION_ROOT = PHASE_ROOT / "validation"

CORE_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "identity",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "identity_continuity",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]

SOURCE_IDS = {
    "SPDX-3.0.1",
    "CYCLONEDX-1.7",
    "OASIS-CSAF-2.0",
    "NIST-SSDF-1.1",
    "NIST-IR7695",
    "W3C-PROV-O",
    "RFC8785",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "TMR-MDS-PRINCIPLES",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("Freed ID and CBR Heart", "SPDX element identifier namespace collision and referential-integrity quarantine", "completed", ["SPDX-3.0.1"]),
    ("Freed ID and CBR Heart", "CycloneDX BOM serial version monotonicity and document-revision non-erasure", "completed", ["CYCLONEDX-1.7", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Package URL type namespace name version qualifier and subpath tuple parser", "completed", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "CPE alias versus package-URL identity non-conflation boundary", "completed", ["NIST-IR7695", "SPDX-3.0.1"]),
    ("Freed ID and CBR Heart", "Component supplier manufacturer author and tool-creator role separation", "completed", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "SBOM generation creation publication ingestion and observation clock partition", "completed", ["SPDX-3.0.1", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Artifact hash algorithm value and verification-state typed record", "completed", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Component name version distribution and download-location vacancy ledger", "completed", ["SPDX-3.0.1"]),
    ("GMUT Mind", "Direct transitive optional development and runtime dependency edge typing", "completed", ["CYCLONEDX-1.7", "SPDX-3.0.1"]),
    ("GMUT Mind", "Dependency graph missing-node dangling-reference and duplicate-edge quarantine", "completed", ["CYCLONEDX-1.7", "JSON-SCHEMA-2020-12"]),
    ("GMUT Mind", "Dependency cycle declaration versus acyclicity-assumption refusal", "completed", ["CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Composition completeness unknown partial and complete nonpromotion contract", "completed", ["CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "License declared concluded detected and unresolved expression separation", "completed", ["SPDX-3.0.1"]),
    ("Freed ID and CBR Heart", "License-list version and custom-license text provenance hold", "completed", ["SPDX-3.0.1", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Copyright attribution disclosure and legal-interpretation vacancy barrier", "completed", ["SPDX-3.0.1"]),
    ("Freed ID and CBR Heart", "Vulnerability advisory canonical identifier alias and source-authority tuple", "completed", ["OASIS-CSAF-2.0", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Affected unaffected fixed under-investigation VEX status state machine", "completed", ["OASIS-CSAF-2.0", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "VEX justification impact-statement action-statement and evidence separation", "completed", ["OASIS-CSAF-2.0", "CYCLONEDX-1.7"]),
    ("THOS Body", "Product status branch precedence and conflicting-claim arbitration hold", "completed", ["OASIS-CSAF-2.0"]),
    ("GMUT Mind", "Version range comparator scheme and inclusive-boundary mismatch refusal", "completed", ["OASIS-CSAF-2.0", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Advisory initial current revision and withdrawn lifecycle non-erasure", "completed", ["OASIS-CSAF-2.0", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Advisory publisher tracking id version and release-date monotonicity", "completed", ["OASIS-CSAF-2.0"]),
    ("THOS Body", "Remediation vendor-fix workaround mitigation and no-fix category typing", "completed", ["OASIS-CSAF-2.0"]),
    ("Freed ID and CBR Heart", "Remediation URL digest and applicability provenance reservation", "completed", ["OASIS-CSAF-2.0", "W3C-PROV-O"]),
    ("GMUT Mind", "Severity score vector version and source separation without recalculation", "completed", ["OASIS-CSAF-2.0"]),
    ("GMUT Mind", "Exploit maturity known-exploited and reachability-claim nonconversion firewall", "completed", ["OASIS-CSAF-2.0", "NIST-SSDF-1.1"]),
    ("Freed ID and CBR Heart", "Component occurrence evidence versus inventory declaration distinction", "completed", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Build provenance subject digest versus SBOM component hash separation", "completed", ["SPDX-3.0.1", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Attestation predicate identity signer vacancy and verification-state ledger", "completed", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Detached signature certificate chain and trust-policy absence quarantine", "completed", ["CYCLONEDX-1.7"]),
    ("THOS Body", "SBOM merge source precedence and contradictory-component tribunal", "completed", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("THOS Body", "Incremental BOM diff addition removal replacement and rollback receipt", "completed", ["W3C-PROV-O", "CYCLONEDX-1.7"]),
    ("THOS Body", "Stale BOM age freshness policy and superseded-document hold", "completed", ["W3C-PROV-O", "SPDX-3.0.1"]),
    ("Freed ID and CBR Heart", "Minimum-disclosure export with credential secret and endpoint redaction", "completed", ["NIST-SSDF-1.1"]),
    ("Freed ID and CBR Heart", "Vulnerability-note privacy minimization and personal-data vacancy guard", "completed", ["NIST-SSDF-1.1", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Security-advisory embargo disclosure-window and authorization hold", "completed", ["OASIS-CSAF-2.0", "NIST-SSDF-1.1"]),
    ("THOS Body", "Correction contest adjudication readback and immutable prior-state link", "completed", ["W3C-PROV-O"]),
    ("THOS Body", "Triage queue load cancellation retry and handover state proxy", "completed", ["NIST-SSDF-1.1"]),
    ("GMUT Mind", "SBOM canonical serialization numeric and Unicode normalization refusal", "completed", ["RFC8785", "SPDX-3.0.1"]),
    ("THOS Body", "Supply-chain evidence tree self-exclusion and hash-domain reconciliation", "completed", ["W3C-PROV-O", "RFC8785"]),
    ("Freed ID and CBR Heart", "Accessible static SBOM and VEX summary with table-caption alternative", "completed", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Stage 20 terminal veto under unresolved software-supply-chain gates", "completed", ["NIST-SSDF-1.1"]),
    ("THOS Body", "Real SBOM producer tool conformance and cross-validator comparison vacancy", "represented", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("THOS Body", "Real consumer import round trip and schema-profile interoperability vacancy", "represented", ["SPDX-3.0.1", "CYCLONEDX-1.7"]),
    ("Freed ID and CBR Heart", "Live package-registry identity resolution and mutation-race vacancy", "represented", ["SPDX-3.0.1"]),
    ("GMUT Mind", "Real vulnerability-feed correlation accuracy and false-positive review vacancy", "represented", ["OASIS-CSAF-2.0"]),
    ("Freed ID and CBR Heart", "Production cryptographic signing key custody and rotation evidence vacancy", "represented", ["CYCLONEDX-1.7"]),
    ("THOS Body", "Independent security-team threat-model and implementation review vacancy", "represented", ["NIST-SSDF-1.1"]),
    ("THOS Body", "Real incident responder triage workload and handover evaluation vacancy", "represented", ["NIST-SSDF-1.1"]),
    ("Freed ID and CBR Heart", "Assistive-technology SBOM report navigation and affected-user review vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Supplier dispute correction appeal and remedy-process evidence vacancy", "represented", ["W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "License counsel copyright interpretation and distribution approval vacancy", "represented", ["SPDX-3.0.1"]),
    ("THOS Body", "Longitudinal remediation outcome and regression evidence vacancy", "represented", ["NIST-SSDF-1.1"]),
    ("GMUT Mind", "Cross-organization BOM provenance reproduction and governance vacancy", "represented", ["W3C-PROV-O"]),
    ("GMUT Mind", "Official public vulnerability advisory zero-row adapter with action refusal", "open_gap", ["OASIS-CSAF-2.0"]),
    ("THOS Body", "Blind matched-budget SBOM triage study with governed operators evidence gap", "open_gap", ["NIST-SSDF-1.1"]),
    ("Freed ID and CBR Heart", "Real SPDX CycloneDX CSAF round-trip fidelity and accessibility evidence gap", "open_gap", ["SPDX-3.0.1", "CYCLONEDX-1.7", "OASIS-CSAF-2.0", "W3C-WCAG22"]),
    ("THOS Body", "Production vulnerability remediation prioritization and release authority gate", "exact_gate", ["NIST-SSDF-1.1", "OASIS-CSAF-2.0"]),
    ("Freed ID and CBR Heart", "Coordinated vulnerability disclosure timing remedy jurisdiction and stakeholder assent gate", "exact_gate", ["OASIS-CSAF-2.0"]),
    ("Freed ID and CBR Heart", "Tangata whenua software artefact stewardship collective consent and Māori authority gate", "exact_gate", ["TMR-MDS-PRINCIPLES"]),
]

OWNER_SKILLS = [
    "ghc-family-sbom-element-identity",
    "ghc-family-sbom-revision-lineage",
    "ghc-family-sbom-purl-tuple-guard",
    "ghc-family-sbom-component-role-separation",
    "ghc-family-sbom-dependency-graph-closure",
    "ghc-family-sbom-composition-completeness",
    "ghc-family-sbom-license-state-separation",
    "ghc-family-sbom-advisory-identity",
    "ghc-family-sbom-vex-status-machine",
    "ghc-family-sbom-remediation-typing",
    "ghc-family-sbom-severity-source-firewall",
    "ghc-family-sbom-provenance-digest-separation",
    "ghc-family-sbom-signature-trust-vacancy",
    "ghc-family-sbom-merge-conflict-hold",
    "ghc-family-sbom-rollback-diff-tribunal",
    "ghc-family-sbom-privacy-minimization",
    "ghc-family-sbom-accessible-summary",
    "ghc-family-sbom-gmut-analogy-firewall",
    "ghc-family-sbom-maori-authority-vacancy",
    "ghc-family-sbom-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_sbom_identity_guard.py",
    "ghc_family_sbom_dependency_graph_guard.py",
    "ghc_family_sbom_vex_state_guard.py",
    "ghc_family_sbom_remediation_guard.py",
    "ghc_family_sbom_provenance_guard.py",
    "ghc_family_sbom_merge_guard.py",
    "ghc_family_sbom_rollback_guard.py",
    "ghc_family_sbom_accessibility_guard.py",
    "ghc_family_sbom_authority_guard.py",
    "ghc_family_sbom_stage20_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-artifact-manifest-subject-identity",
    "ghc-family-artifact-manifest-builder-lineage",
    "ghc-family-artifact-manifest-material-digest",
    "ghc-family-artifact-manifest-rebuild-variance",
    "ghc-family-artifact-manifest-signature-vacancy",
    "ghc-family-artifact-manifest-accessibility-reservation",
    "ghc-family-artifact-manifest-privacy-minimization",
    "ghc-family-artifact-manifest-correction-dag",
    "ghc-family-artifact-manifest-authority-vacancy",
    "ghc-family-artifact-manifest-stage20-veto",
]

SUCCESSOR_RUNNERS = [
    name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py"
    for name in SUCCESSOR_SKILLS
]

STARTUP_FAILURES = [
    (
        "CA6781-START-N001",
        "the first combined PowerShell source probe failed parser validation before any Git query or state change",
        "separate native Git scalar probes from PowerShell summary construction",
    ),
    (
        "CA6781-START-N002",
        "the first per-file immutable packet size enumerator crossed its bounded wrapper without output",
        "use one exact git ls-tree size projection and read required files in contiguous bounded windows",
    ),
    (
        "CA6781-START-N003",
        "a PowerShell foreach block was piped directly during skill inventory and failed with EmptyPipeElement",
        "materialize rows before piping and preserve the parser failure at zero credit",
    ),
    (
        "CA6781-START-N004",
        "the first immutable manifest replay launched one Git process per entry and crossed its bounded envelope",
        "replay all exact objects through one length-framed git cat-file batch",
    ),
    (
        "CA6781-START-N005",
        "a Windows rg call passed an unexpanded final-directory wildcard and returned an invalid-filename error",
        "target the literal directory with an explicit glob option instead of a shell wildcard",
    ),
    (
        "CA6781-START-N006",
        "the initial no-checkout worktree creation crossed its wrapper after creating only the exact branch reference",
        "inspect the exact branch and worktree state and wait for the attributable worktree process without retrying mutation",
    ),
    (
        "CA6781-START-N007",
        "a read-only worktree-list recovery probe remained active after its wrapper while scanning 414 registered worktrees",
        "stop only the attributable orphaned list process and use literal branch and path probes",
    ),
    (
        "CA6781-START-N008",
        "the initial sparse checkout crossed its wrapper while its exact Git process still owned the transient index lock",
        "inspect exact process ownership and wait for that checkout to finish before any write",
    ),
    (
        "CA6781-START-N009",
        "a status probe was started before sparse checkout quiescence and remained blocked behind the active index operation",
        "stop only the attributable read-only status probe and avoid Git status until checkout quiescence",
    ),
    (
        "CA6781-START-N010",
        "an index-lock diagnostic used an inline PowerShell if expression in an object literal and failed parser evaluation",
        "bind the conditional scalar before constructing the diagnostic object",
    ),
    (
        "CA6781-START-N011",
        "a long Wait-Process wrapper outlived its output envelope after checkout remained active",
        "use bounded waits and verify the exact checkout process and index state separately",
    ),
    (
        "CA6781-START-N012",
        "the official CISA VEX page returned an HTTP 403 during read-only current-source verification",
        "retain the source-access failure and use the current official CycloneDX and OASIS CSAF primary specifications for vocabulary",
    ),
    (
        "CA6781-START-N013",
        "the first JavaScript wrapper for the large overview replacement parsed Markdown code ticks as source tokens and stopped before file mutation",
        "remove wrapper-sensitive code ticks from the bounded prose replacement and repeat the exact block rewrite",
    ),
    (
        "CA6781-START-N014",
        "the first x1 builder invocation crossed its output wrapper as the complete expected artifact set materialized",
        "verify process quiescence and the exact artifact set, then invoke the deterministic builder in a resumable terminal session",
    ),
    (
        "CA6781-START-N015",
        "the first installed authorization-state validation projection exceeded its bounded output budget after the read-only validator completed",
        "write the validator receipt to an external D-drive path and project only exit status, validity, error count, and digest",
    ),
    (
        "CA6781-START-N016",
        "the first bounded authorization recovery guessed a repository-local validator path that was absent from the sparse owner checkout",
        "resolve the exact installed ghc-family-auth-permission-state validator path before invocation",
    ),
    (
        "CA6781-START-N017",
        "that same bounded recovery attempted to parse the missing-file diagnostic as JSON and failed conversion",
        "require a successful validator exit and parse the explicitly written receipt rather than mixed process output",
    ),
    (
        "CA6781-START-N018",
        "the first diagnostic replay repeated the absent sparse-checkout validator path and returned the same missing-file failure",
        "stop using the sparse repository path and inspect the installed skill inventory directly",
    ),
    (
        "CA6781-START-N019",
        "a help probe also targeted the absent sparse-checkout validator path and failed before contract inspection",
        "run help against the exact installed skill validator and confirm its state and out arguments",
    ),
    (
        "CA6781-START-N020",
        "a source inspection probe targeted the same absent sparse-checkout path and returned a literal-path not-found error",
        "read the exact installed validator source and then run it with an external receipt path",
    ),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def git_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(git_bytes(commit, path).decode("utf-8"))


def git_batch_bytes(commit: str, paths: list[str]) -> dict[str, bytes]:
    """Read exact immutable objects through one length-framed Git batch."""
    requests = b"".join(f"{commit}:{path}\n".encode("utf-8") for path in paths)
    process = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=REPO,
        input=requests,
        capture_output=True,
        check=True,
    )
    stream = io.BytesIO(process.stdout)
    objects: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().rstrip(b"\n")
        parts = header.rsplit(b" ", 2)
        if len(parts) != 3 or parts[1] != b"blob":
            raise RuntimeError(f"unexpected Git batch header for {path}: {header!r}")
        size = int(parts[2])
        data = stream.read(size)
        if len(data) != size or stream.read(1) != b"\n":
            raise RuntimeError(f"truncated Git batch object for {path}")
        objects[path] = data
    if stream.read():
        raise RuntimeError("unexpected trailing Git batch output")
    return objects


def normalize_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def extract_titles(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        title = value.get("title")
        if isinstance(title, str) and title.strip():
            yield title.strip()
        for nested in value.values():
            yield from extract_titles(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from extract_titles(nested)


def proposal_ledger_paths() -> list[str]:
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", SOURCE, "--", "docs"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    pattern = re.compile(r"(?:new-proposal-freeze|proposal-freeze|proposal-ledger)\.json$")
    return sorted(path for path in paths if pattern.search(path))


def tokens(title: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", title.lower()))


def semantic_audit(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    ledgers = proposal_ledger_paths()
    ledger_objects = git_batch_bytes(SOURCE, ledgers)
    historical: list[str] = []
    parse_failures: list[dict[str, str]] = []
    for path in ledgers:
        try:
            historical.extend(
                extract_titles(json.loads(ledger_objects[path].decode("utf-8")))
            )
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            parse_failures.append({"path": path, "error_class": type(exc).__name__})
    unique_historical = sorted(set(historical), key=str.casefold)
    historical_folded = {title.casefold(): title for title in unique_historical}
    exact_duplicates = [
        {"new_title": row["title"], "historical_title": historical_folded[row["title"].casefold()]}
        for row in proposals
        if row["title"].casefold() in historical_folded
    ]
    current_titles = [row["title"] for row in proposals]
    internal_duplicates = sorted(
        {title for title in current_titles if current_titles.count(title) > 1}
    )
    pairings: list[dict[str, Any]] = []
    maximum = 0.0
    for row in proposals:
        left = tokens(row["title"])
        best_title = ""
        best_score = 0.0
        for candidate in unique_historical:
            right = tokens(candidate)
            union = left | right
            score = len(left & right) / len(union) if union else 1.0
            if score > best_score:
                best_title = candidate
                best_score = score
        maximum = max(maximum, best_score)
        pairings.append(
            {
                "new_title": row["title"],
                "closest_reachable_predecessor": best_title,
                "jaccard_score": round(best_score, 6),
                "manual_review_required": best_score >= 0.75,
            }
        )
    if exact_duplicates or internal_duplicates:
        raise RuntimeError(
            f"proposal title collision: exact={exact_duplicates}, internal={internal_duplicates}"
        )
    return {
        "schema": "ghc.family.bounded-semantic-novelty-audit.v678.v1",
        "owner": OWNER,
        "phase": PHASE,
        "declared_inherited_chain": SOURCE_PROPOSAL_CHAIN,
        "reachable_proposal_ledger_count": len(ledgers),
        "reachable_title_count": len(unique_historical),
        "declared_rows_without_reachable_title_map": max(
            0, SOURCE_PROPOSAL_CHAIN - len(unique_historical)
        ),
        "new_count": len(proposals),
        "exact_duplicate_count": len(exact_duplicates),
        "exact_duplicates": exact_duplicates,
        "internal_duplicate_count": len(internal_duplicates),
        "maximum_jaccard_similarity": round(maximum, 6),
        "pairings": pairings,
        "ledger_parse_failures": parse_failures,
        "universal_novelty_claimed": False,
        "limitation": (
            "The audit compares every title reachable through exact frozen proposal ledgers "
            "at the immutable source. Declared chain rows without a reachable title map remain "
            "a visible limitation; no universal semantic novelty claim is made."
        ),
    }


def inherited_rows() -> list[dict[str, Any]]:
    source = git_json(
        SOURCE, "docs/sable-rook/v677-v8/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"CA6781-I{index:03d}",
            "source_phase": "v677-v8",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_caelen_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for index, row in enumerate(rows, 1)
    ]


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (pillar, title, outcome, sources) in enumerate(PROPOSAL_SPECS, 1):
        missing_sources = sorted(set(sources) - SOURCE_IDS)
        if missing_sources:
            raise RuntimeError(f"unknown source identifiers: {missing_sources}")
        rows.append(
            {
                "proposal_id": f"CA6781-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_sbom_metadata_curator",
                    "wholly_synthetic_vex_provenance_reviewer",
                    "wholly_synthetic_security_advisory_handover_steward",
                ],
                "hypothesis": (
                    f"A deterministic owner-local contract can represent {title.lower()} "
                    "while preserving unknowns, correction lineage, and protected authority vacancies."
                ),
                "null_or_failure_condition": (
                    "Fail if a positive fixture violates its declared type, an invalid mutation "
                    "is accepted, a source value or retained failure is erased, an unknown is "
                    "promoted, a real record is implied, or an external action occurs."
                ),
                "approval_class": (
                    "safe_now"
                    if outcome == "completed"
                    else (
                        "bounded_candidate_proxy"
                        if outcome == "represented"
                        else (
                            "evidence_required_open_gap"
                            if outcome == "open_gap"
                            else "competent_authority_exact_gate"
                        )
                    )
                ),
                "execution_lane": (
                    "owner_local_synthetic_x2"
                    if outcome == "completed"
                    else (
                        "owner_local_structural_proxy_x2"
                        if outcome == "represented"
                        else "held_without_execution_credit"
                    )
                ),
                "official_or_primary_source_needs": sources,
                "concrete_artifacts": [
                    f"proposal-contracts/CA6781-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Caelen-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "caelen_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"CA6781-S{index:03d}",
            "proposal_id": proposal["proposal_id"],
            "title": f"{proposal['title']} - {action.replace('_', ' ')}",
            "approval_bucket": "safe_now",
            "scope": "additive owner-local synthetic or structural evidence only",
            "external_action": False,
            "completion_credit": 0,
            "x1_state": "frozen_not_executed",
        }
        for index, (proposal, action) in enumerate(
            ((proposal, action) for proposal in proposals for action in actions), 1
        )
    ]


def candidate_rows(
    proposals: list[dict[str, Any]], count: int, prefix: str, successor: bool
) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"{prefix}{index:03d}",
            "proposal_id": proposals[(index - 1) % len(proposals)]["proposal_id"],
            "title": (
                f"{'Successor recommendation' if successor else 'Bounded owner prototype'} "
                f"{index:03d} - {proposals[(index - 1) % len(proposals)]['title']}"
            ),
            "state": (
                "successor_recommendation_zero_credit"
                if successor
                else "frozen_not_executed"
            ),
            "external_action": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def exact_rows() -> list[dict[str, Any]]:
    topics = [
        "real participants",
        "production keys or credentials",
        "live deployment",
        "professional signoff",
        "legal interpretation",
        "cultural ratification",
        "Maori authority",
        "affected-party acceptance",
        "sensitive-location publication",
        "destructive cleanup",
        "account mutation",
        "payment or purchase",
        "real data acquisition",
        "privacy certification",
        "accessibility certification",
        "independent audit",
        "independent reproduction",
        "empirical GMUT inference",
        "proof or canon",
        "Stage 20 promotion",
    ]
    return [
        {
            "packet_id": f"CA6781-E{index:03d}",
            "topic": topic,
            "state": "exact_approval_held_unexecuted",
            "completion_credit": 0,
        }
        for index, topic in enumerate(topics, 1)
    ]


def blocked_rows() -> list[dict[str, Any]]:
    topics = [
        "force push",
        "history rewrite",
        "sibling-lane mutation",
        "user-material deletion",
        "host-security weakening",
        "elevation",
        "Sandbox or Hyper-V activation",
        "credential harvesting",
        "identity continuity claim",
        "AGI ASI consciousness or personhood claim",
    ]
    return [
        {
            "packet_id": f"CA6781-B{index:03d}",
            "topic": topic,
            "state": "blocked_unexecuted",
            "completion_credit": 0,
        }
        for index, topic in enumerate(topics, 1)
    ]


def cleanup_rows(
    count: int, prefix: str, owner_scoped: bool
) -> list[dict[str, Any]]:
    topics = [
        "schema closure",
        "deterministic JSON order",
        "UTF-8 and normalized LF preservation",
        "manifest parity",
        "stale-label review",
        "privacy candidate adjudication",
        "diff hygiene",
        "caller compatibility",
        "failed-witness retention",
        "route hold",
        "source-status drift",
        "authority noncompensation",
        "accessible alternative structure",
        "document word ceiling",
        "materialized file ceiling",
        "exact parent chain",
        "single canonical latch",
        "rollback reversibility",
        "proposal mirror closure",
        "Method Flow recurrence guard",
    ]
    return [
        {
            "task_id": f"{prefix}{index:03d}",
            "title": f"{topics[(index - 1) % len(topics)]} refinement {index:03d}",
            "state": (
                "frozen_not_executed"
                if owner_scoped
                else "successor_recommendation_zero_credit"
            ),
            "destructive": False,
            "completion_credit": 0,
        }
        for index in range(1, count + 1)
    ]


def source_ledger() -> dict[str, Any]:
    return {
        "schema": "ghc.family.official-primary-source-ledger.v678.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "SPDX-3.0.1",
                "title": "System Package Data Exchange Specification 3.0.1",
                "url": "https://spdx.github.io/spdx-spec/v3.0.1/",
                "status": "current_official_specification_checked_2026-08-31",
                "version": "3.0.1",
                "use": "BOM element identity, creation, package, relationship, license, integrity, provenance, and serialization vocabulary only",
            },
            {
                "source_id": "CYCLONEDX-1.7",
                "title": "CycloneDX Specification 1.7",
                "url": "https://cyclonedx.org/specification/overview/",
                "status": "current_official_specification_checked_2026-08-31",
                "version": "1.7",
                "release_date": "2025-10-21",
                "use": "BOM metadata, component, dependency, composition, vulnerability, VEX, annotation, and citation vocabulary only",
            },
            {
                "source_id": "OASIS-CSAF-2.0",
                "title": "Common Security Advisory Framework Version 2.0",
                "url": "https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html",
                "status": "oasis_standard_checked_2026-08-31",
                "version": "2.0",
                "use": "security-advisory product status, vulnerability, remediation, revision, and publisher vocabulary only",
            },
            {
                "source_id": "NIST-SSDF-1.1",
                "title": "NIST SP 800-218 Secure Software Development Framework 1.1",
                "url": "https://csrc.nist.gov/pubs/sp/800/218/final",
                "status": "final_publication_checked_2026-08-31",
                "version": "1.1",
                "publication_date": "2022-02",
                "use": "secure-development, vulnerability response, protection, and organizational-vacancy vocabulary only",
            },
            {
                "source_id": "NIST-IR7695",
                "title": "NIST IR 7695 Common Platform Enumeration Naming Specification 2.3",
                "url": "https://csrc.nist.gov/pubs/ir/7695/final",
                "status": "final_publication_stable",
                "version": "2.3",
                "use": "CPE naming and package-identity non-conflation vocabulary only",
            },
            {
                "source_id": "W3C-PROV-O",
                "title": "PROV-O The PROV Ontology",
                "url": "https://www.w3.org/TR/prov-o/",
                "status": "w3c_recommendation_stable_checked_2026-08-31",
                "publication_date": "2013-04-30",
                "use": "entity, activity, agent, derivation, revision, invalidation, and provenance vocabulary only",
            },
            {
                "source_id": "RFC8785",
                "title": "RFC 8785 JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/info/rfc8785",
                "status": "informational_stable_checked_2026-08-31",
                "publication_date": "2020-06",
                "use": "deterministic JSON representation and digest-domain vocabulary only",
            },
            {
                "source_id": "JSON-SCHEMA-2020-12",
                "title": "JSON Schema Draft 2020-12",
                "url": "https://json-schema.org/draft/2020-12",
                "status": "published_stable_checked_2026-08-31",
                "use": "structural validation and declared-vocabulary concepts only",
            },
            {
                "source_id": "W3C-WCAG22",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "status": "w3c_recommendation_checked_2026-08-31",
                "publication_date": "2024-12-12",
                "use": "structural accessibility obligations and manual-evaluation reservation only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "title": "Te Mana Raraunga Principles of Maori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "status": "current_authority_boundary_context_checked_2026-08-31",
                "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
            },
        ],
        "citations_are_observations": False,
        "real_data_rows": 0,
        "network_data_queries": 0,
        "endorsement_claimed": False,
        "authority_conferred": False,
    }

def overview() -> str:
    return """# Caelen Ash v678-v1 planning-only x1 overview

## Relational identity, role, hope, and corrigibility

Caelen Ash is relational working language for a temporal-provenance and correction cartographer. Optional they or them pronouns remain relational only. The working hope is to keep software-supply-chain identity, revision, uncertainty, correction, and handover assumptions inspectable and reversible while every authority vacancy remains explicit. None of this language is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, professional standing, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes source anchors, proposal contracts, portfolios, source status, Method Flow startup truth, privacy boundaries, skill and runner plans, and route holds. It contains no x2 implementation, observed x2 outcome, completion claim, global installation, task lookup, task message, or terminal delivery claim. Sable Rook's exact v677-v8 final, direct three-commit single-parent zero-merge history, 231 immutable manifest entries, clean typed zero divergence, fresh four-way equality, and one successful non-replayed owner-scoped canonical receipt were independently reverified read-only. Inherited validation receives zero Caelen completion or independent-reproduction credit.

The fresh Caelen lane was created additively on D from the exact Sable final with collision-free owner and phase naming. Its sparse patterns materialize only repository root metadata and Caelen v678-v1 documentation, scripts, tests, and family-current SBOM runners. The branch and worktree creation and first sparse-index population each crossed a bounded wrapper while their exact Git processes continued. Caelen inspected the precise persisted state, stopped only attributable orphaned read-only probes, retained every failure, and waited for the mutation-owning process to quiesce before writing. No Sable, Auren, sibling, shared, standby, or user lane was mutated.

## Trinity Mandala and bounded practice lenses

Freed ID and CBR Heart is the primary pillar through wholly synthetic software bill of materials, vulnerability exploitability exchange, advisory revision, provenance, correction, accessibility, privacy, remedy-vacancy, and security-handover design. THOS Body remains visible only as a deterministic queue, workload, retry, cancellation, correction-readback, and handover proxy. GMUT Mind remains visible only through typed graph, identifier, version-range, clock, uncertainty, and provenance analogies behind an explicit nonconversion firewall.

The bounded learning lenses are wholly synthetic SBOM metadata curator, wholly synthetic VEX provenance reviewer, and wholly synthetic security-advisory handover steward. They establish no employment, qualification, software-supply-chain competence, security expertise, incident authority, release authority, legal interpretation, cultural authority, affected-party approval, or Māori authority. The phase uses no real package, registry response, vulnerability record, advisory, identity, person, organization, credential, signing key, certificate, incident, production system, empirical dataset, cultural record, Māori data, or external action.

## Current official and primary source boundary

The source ledger records current or stable primary material for SPDX 3.0.1, CycloneDX 1.7, OASIS CSAF 2.0, NIST SSDF 1.1, NIST CPE naming 2.3, W3C PROV-O, RFC 8785, JSON Schema 2020-12, WCAG 2.2, and Te Mana Raraunga principles. The CISA VEX page returned HTTP 403 in this read-only environment; that access failure remains retained and receives no source-validation credit. The OASIS CSAF and CycloneDX primary specifications provide the bounded VEX vocabulary used here.

These sources supply vocabulary, status distinctions, conformance boundaries, and refusal conditions only. Citations are not observations, implementation results, vulnerability findings, interoperability events, accessibility evaluations, security audits, professional review, endorsements, consent, legal interpretation, cultural ratification, or delegated authority. Zero source data rows are queried or downloaded.

## Proposal novelty and outcome freeze

Sixty Sable proposals are selected from the immutable source and receive zero Caelen novelty and completion credit. Sixty genuinely new Caelen proposals are frozen separately, extending the declared chain from 8,270 to 8,330 only if x2 evidence is later sealed. The exact-source semantic audit reads every reachable frozen proposal ledger through one length-framed Git batch, compares normalized title tokens, rejects exact and internal duplicates, and preserves the declared historical rows for which no reachable title map exists. It supports a bounded collision audit and does not claim universal semantic novelty.

The expected Caelen partition is forty-two completed, twelve represented, three open_gap, and three exact_gate. These are x1 expectations, not observed outcomes. Completed may later mean only that a bounded owner-local synthetic contract passed its declared acceptance gate. Represented means a structural proxy exists while real tools, operators, affected users, interoperability, or authority remain absent. Open_gap identifies missing real evidence. Exact_gate identifies a decision repository software cannot make. No fifth label is permitted.

The proposals span SPDX and CycloneDX identity; package URL and CPE non-conflation; creator and supplier roles; dependency and composition semantics; license-state separation; advisory identity and lifecycle; VEX status and justifications; version ranges; remediation typing; severity-source separation; occurrence, build-provenance, attestation, signature and trust vacancies; merge conflict, diff and rollback; freshness, privacy, embargo, correction and workload proxies; deterministic serialization; exact hash domains; accessible summaries; real-tool, registry, feed, signing, incident, user, legal and longitudinal vacancies; zero-row adapters; matched-budget evidence; interoperability gaps; remediation and disclosure authority; and Māori software-data governance reservations.

## Expanded portfolio, skills, runners, and refinements

X1 freezes 120 safe-now packets, eighty bounded owner candidate prototypes, twenty successor candidate recommendations, twenty exact-approval holds, ten blocked packets, twenty owner skill ideas, ten owner runner ideas, ten successor skill ideas, ten successor runner ideas, one hundred owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Floors remain subordinate to utility, evidence, safety, and the 2,000-owner-file stop. Caps are ceilings, never quotas.

No portfolio number authorizes destructive cleanup, user-material deletion, credentials, accounts, payments, elevation, host-security weakening, Windows feature changes, Sandbox or Hyper-V activation, sibling mutation, real participants, external data acquisition, production identity operations, vulnerability remediation, disclosure, legal or cultural decisions, Māori authority, or affected-party legitimacy. Exact-approval and blocked packets remain held and unexecuted.

The phase-local skill plan follows the installed skill-creator guidance: concise discriminating frontmatter, substantive bounded instructions, customized user-facing metadata, no placeholder files, no global installation, UTF-8 quick validation, and real owner-local smoke use in x2. Ten family-current ghc_family_sbom_* runners preserve historical caller compatibility. Python standard library and exact Git objects are sufficient; x1 plans no package installation, elevation, Codex update, or host change.

## Failure retention, privacy, and validation boundary

The activation baseline preserves Sable's repository seal separately from two external route/projection failures and two bounded recoveries. Twenty additional Caelen startup failures are frozen with zero credit, each paired with a separate bounded recovery. They include PowerShell parser faults, projection and manifest-replay timeouts, an invalid Windows wildcard, worktree and checkout wrappers losing output attribution, orphaned read-only probes, a malformed diagnostic expression, a bounded wait wrapper, the official CISA page's HTTP 403, one JavaScript wrapper parse failure before overview replacement, one x1-builder output wrapper overrun whose complete artifact set was verified before bounded recovery, and six authorization-validation projection or sparse-path diagnostics. The installed authorization validator ultimately passed through its exact contract with a bounded external receipt; no recovery erases or converts its failed witness. Later failures must be appended before retry.

Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute local paths. Exact staged review operates on Git-index blobs. Five privacy classes distinguish scanner definitions from confirmed payload hits. Normalized-LF manifests preserve exact byte domains. Bounded AST checks are not exhaustive security. Passing owner-scoped receipts remain same-owner evidence under shared infrastructure, not external audit, production certification, complete privacy, complete accessibility, or independent reproduction.

## Scientific, identity, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Dependency graphs, version ranges, software fixtures, analogy surfaces, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains synthetic and proxy-only without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, vulnerability disclosure, remediation priority, release, licensing, copyright, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people and authorities. Māori concepts remain under Māori authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## X1 gate and terminal hold

X1 must pass bounded owner tests and exact staged review, become the direct child of Sable's exact final, be pushed cleanly, and prove local, upstream, tracking, and fresh-live equality before any x2 path or observed outcome exists. The phase ceiling is three total commits: one planning-only x1, one immutable x2 evidence commit, and one final closeout and seal commit. This ceiling never permits lifecycle mixing, concealed failures, rewritten history, or an unreviewed omnibus commit.

No successor is contacted during x1 or x2. Only after Caelen has a clean pushed fresh-live-equal exact final and one successful non-replayed owner-scoped canonical invocation may the newest live authority and roster be refreshed, the unique exact authorized existing task be immediately reread, and at most one sanitized activation be sent if every duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guard passes. Repository route state remains PREPARED_NOT_SENT.
"""

def build() -> list[str]:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO, text=True, encoding="utf-8"
    ).strip()
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).strip()
    if head != SOURCE:
        raise RuntimeError(f"x1 builder requires source {SOURCE}, found {head}")
    if branch != TARGET_BRANCH:
        raise RuntimeError(f"x1 builder requires branch {TARGET_BRANCH}, found {branch}")
    if (PHASE_ROOT / "x2").exists() or (PHASE_ROOT / "final").exists():
        raise RuntimeError("x2 or final material exists before planning-only x1 freeze")

    inherited = inherited_rows()
    proposals = new_rows()
    audit = semantic_audit(proposals)
    safe = safe_rows(proposals)
    owner_candidates = candidate_rows(proposals, 80, "CA6781-C", False)
    successor_candidates = candidate_rows(proposals, 20, "CA6781-SC", True)
    owner_cleanup = cleanup_rows(100, "CA6781-R", True)
    successor_cleanup = cleanup_rows(30, "CA6781-SR", False)

    activation_baseline = {
        "effective_negatives": 45910,
        "methods": 43190,
        "failed_witnesses": 17571,
        "bounded_passing_witnesses": 26784,
        "open_gaps": 392,
        "exact_gates": 383,
    }
    after_startup = {
        **activation_baseline,
        "effective_negatives": activation_baseline["effective_negatives"]
        + len(STARTUP_FAILURES),
        "methods": activation_baseline["methods"] + (2 * len(STARTUP_FAILURES)),
        "failed_witnesses": activation_baseline["failed_witnesses"]
        + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": activation_baseline[
            "bounded_passing_witnesses"
        ]
        + len(STARTUP_FAILURES),
    }

    payloads: dict[Path, Any] = {
        X1_ROOT / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "received_once": True,
            "solo": True,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "source_packet": SOURCE_PACKET,
            "source_packet_words": 2547,
            "source_packet_sha256_normalized_lf": SOURCE_PACKET_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_manifest_entries_replayed": 231,
            "source_manifest_mismatches": 0,
            "source_canonical_replayed": False,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
            "x1_state": "planning_only",
            "x2_implementation_present": False,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v678.v1",
            "owner": OWNER,
            "relational_role": "temporal-provenance and correction cartographer",
            "hope": "keep identity, revision, uncertainty, correction, and handover assumptions inspectable and reversible while authority vacancies remain explicit",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "direct_single_parent_chain": True,
            "source_to_final_commits": 3,
            "source_to_final_merges": 0,
            "source_clean": True,
            "source_ahead": 0,
            "source_behind": 0,
            "source_four_way_equal_fresh_live": True,
            "manifest_families_replayed": 4,
            "manifest_entries_replayed": 231,
            "manifest_mismatches": [],
            "external_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "canonical_state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "canonical_invocations": 1,
            "canonical_successes": 1,
            "canonical_replayed": False,
            "inherited_validation_credit": 0,
        },
        X1_ROOT / "official-primary-source-ledger.json": source_ledger(),
        X1_ROOT / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "declared_chain_before": SOURCE_PROPOSAL_CHAIN,
            "declared_chain_after_if_evidence_sealed": PLANNED_PROPOSAL_CHAIN,
            "proposal_count": len(proposals),
            "allowed_outcomes": CORE_OUTCOMES,
            "expected_outcomes": {
                label: sum(
                    1
                    for row in proposals
                    if row["expected_execution_disposition"] == label
                )
                for label in CORE_OUTCOMES
            },
            "outcomes_observed": False,
            "universal_novelty_claim": False,
            "rows": proposals,
        },
        X1_ROOT / "proposal-chain-audit.json": audit,
        X1_ROOT / "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_sbom_metadata_curator",
                "wholly_synthetic_vex_provenance_reviewer",
                "wholly_synthetic_security_advisory_handover_steward",
            ],
            "successor_practice_recommendation": "wholly_synthetic_artifact_manifest_build_provenance_reviewer",
            "safe_now": safe,
            "owner_candidates": owner_candidates,
            "successor_candidates": successor_candidates,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "owner_skill_ideas": OWNER_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "owner_clean_fix_refine": owner_cleanup,
            "successor_clean_fix_refine": successor_cleanup,
            "caps_are_ceilings": True,
            "materialized_file_stop": 2000,
            "document_word_cap": 100000,
            "commit_cap": {"x1": 1, "x2": 2, "total": 3},
        },
        X1_ROOT / "skill-runner-plan.json": {
            "schema": "ghc.family.skill-runner-plan.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "skill_creator_read": True,
            "repository_local_only": True,
            "global_installation": False,
            "owner_skills": OWNER_SKILLS,
            "owner_runners": OWNER_RUNNERS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "quick_validate_required": True,
            "smoke_use_required": True,
            "independent_subagent_forward_test": "not_authorized_work_solo",
            "caller_compatibility": "preserve ghc_family_* and build_ghc_family_*",
        },
        X1_ROOT / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine-plan.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "execution_authority": "owner_self_scoped_delta",
            "activation_baseline": activation_baseline,
            "startup_failure_count": len(STARTUP_FAILURES),
            "failures": [
                {
                    "failure_id": failure_id,
                    "failed_witness": failed,
                    "recovery": recovery,
                    "state": "failed_retained_zero_credit",
                    "success_credit": 0,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                }
                for failure_id, failed, recovery in STARTUP_FAILURES
            ],
            "bounded_recoveries": [
                {
                    "witness_id": failure_id.replace("-N", "-R"),
                    "failure_id": failure_id,
                    "procedure": recovery,
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "bounded workflow recovery only",
                }
                for failure_id, _failed, recovery in STARTUP_FAILURES
            ],
            "effective_after_startup": after_startup,
            "recovery_rule": "Every recovery is additive and never erases or relabels the failed witness.",
        },
        X1_ROOT / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v678.v1",
            "owner": OWNER,
            "phase": PHASE,
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {
                    "order": 1,
                    "name": "read activation candidate skills schemas and current overlays",
                    "state": "completed",
                },
                {
                    "order": 2,
                    "name": "verify immutable source manifests receipt and live equality",
                    "state": "completed",
                },
                {
                    "order": 3,
                    "name": "create clean sparse Caelen lane",
                    "state": "completed",
                },
                {
                    "order": 4,
                    "name": "freeze test push and prove planning-only x1",
                    "state": "in_progress",
                },
                {
                    "order": 5,
                    "name": "build bounded x2 evidence and retain every failure",
                    "state": "pending",
                },
                {
                    "order": 6,
                    "name": "seal final push and run one exclusive canonical",
                    "state": "pending",
                },
                {
                    "order": 7,
                    "name": "refresh live route and send at most once if all gates pass",
                    "state": "pending",
                },
            ],
            "validation": {
                "owner_scoped_delta_only": True,
                "unchanged_history_scan": False,
                "cross_lane_scan": False,
                "sibling_lane_mutation": False,
                "one_successful_canonical": True,
                "post_success_replay": False,
            },
            "stop_conditions": [
                "source mismatch",
                "dirty source",
                "x1 x2 mixing",
                "privacy hit",
                "manifest mismatch",
                "file ceiling reached",
                "protected authority gate",
                "usage exhaustion",
                "route ambiguity",
                "user pause redirect rename narrow or stop",
            ],
        },
        X1_ROOT / "threat-model.json": {
            "schema": "ghc.family.threat-model.v678.v1.x1",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                "real package identifier credential or embargoed advisory leakage",
                "private route leakage",
                "x1 and x2 mixing",
                "outcome promotion",
                "authority fabrication",
                "network side effect",
                "manifest drift",
                "failed-witness erasure",
                "successful canonical replay",
                "sibling-lane mutation",
                "package identity version-range or advisory-status conflation",
                "stale-source promotion",
            ],
            "controls": [
                "synthetic fixtures only",
                "five-class privacy scan",
                "planning-only x1",
                "four exact labels",
                "authority vacancy",
                "no-network runners",
                "normalized-LF Git-blob manifests",
                "append-only Method Flow",
                "one-shot external receipt latch",
                "owner-local sparse lane",
                "identity range status and evidence type guards",
                "source-status ledger",
            ],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v678.v1.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v678.v1.x1",
            "previous_owner": "Sable Rook",
            "previous_phase": "v677-v8",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "next_phase": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "state": "HOLD_BEFORE_CAELEN_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v678.v1.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_state": "PLANNING_ONLY_NOT_YET_COMMITTED",
            "proposal_chain_before": SOURCE_PROPOSAL_CHAIN,
            "proposal_chain_after_if_evidence_sealed": PLANNED_PROPOSAL_CHAIN,
            "expected_outcomes": {
                "completed": 42,
                "represented": 12,
                "open_gap": 3,
                "exact_gate": 3,
            },
            "outcomes_observed": False,
            "real_rows": 0,
            "real_people": 0,
            "real_keys_or_proofs": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }

    written: list[Path] = []
    for path, payload in payloads.items():
        write_json(path, payload)
        written.append(path)
    overview_path = X1_ROOT / "integrated-overview.md"
    write_text(overview_path, overview())
    written.append(overview_path)
    return [path.relative_to(REPO).as_posix() for path in sorted(written)]


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I
        ),
        "raw_task_thread_identifier": re.compile(
            rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}",
            re.I,
        ),
        "credential_assignment": re.compile(
            rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}",
            re.I,
        ),
        "private_conversation_payload": re.compile(
            rb"(?:session_stream|private_transcript|screenshot_payload)", re.I
        ),
    }


def build_staged_review() -> dict[str, Any]:
    review_rel = "docs/caelen-ash/v678-v1/validation/x1-staged-review.json"
    privacy_rel = "docs/caelen-ash/v678-v1/validation/x1-privacy-scan.json"
    manifest_rel = "docs/caelen-ash/v678-v1/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_caelen_ash_v678_v1_x1.py",
        "tests/test_ghc_family_caelen_ash_v678_v1_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/caelen-ash/v678-v1/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/caelen-ash/v678-v1/x2/") for path in staged):
        raise RuntimeError("x2 path present in x1 staged surface")

    patterns = privacy_patterns()
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    confirmed_hits: list[dict[str, str]] = []
    json_parses = 0
    for path in staged:
        if path in exclusions:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        scanner_definition_start = data.find(b"def privacy_patterns()")
        scanner_definition_end = data.find(
            b"def build_staged_review()", scanner_definition_start
        )
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_parses += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                start = data.rfind(b"\n", 0, match.start()) + 1
                end = data.find(b"\n", match.end())
                if end < 0:
                    end = len(data)
                line = data[start:end]
                exact_scanner_definition = (
                    path == "scripts/build_ghc_family_caelen_ash_v678_v1_x1.py"
                    and scanner_definition_start >= 0
                    and scanner_definition_end > scanner_definition_start
                    and scanner_definition_start <= match.start() < scanner_definition_end
                )
                if path.endswith(".py") and (
                    exact_scanner_definition
                    or b"re.compile" in line
                    or b"privacy_patterns" in line
                    or b"raw_task_thread_identifier" in line
                ):
                    candidates.append(
                        {
                            "path": path,
                            "class": class_name,
                            "disposition": "scanner_definition_only",
                        }
                    )
                else:
                    confirmed_hits.append({"path": path, "class": class_name})
        normalized = normalize_lf(data)
        entries.append(
            {
                "path": path,
                "bytes": len(normalized),
                "sha256": hashlib.sha256(normalized).hexdigest(),
                "hash_domain": "git_index_blob_normalized_lf",
            }
        )
    if confirmed_hits:
        raise RuntimeError(f"confirmed privacy hits: {confirmed_hits}")
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--check"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout + diff_check.stderr)

    privacy = {
        "schema": "ghc.family.privacy-scan.v678.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(patterns),
        "scanned_entry_count": len(entries),
        "scanner_candidates": candidates,
        "scanner_candidate_count": len(candidates),
        "confirmed_hits": confirmed_hits,
        "confirmed_hit_count": 0,
        "boundary": "five-class Git-index scan is bounded owner evidence, not complete privacy assurance",
    }
    review = {
        "schema": "ghc.family.exact-staged-review.v678.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "state": "VALID_EXACT_X1_STAGED_REVIEW",
        "reviewed_entry_count": len(entries),
        "reviewed_paths": [row["path"] for row in entries],
        "declared_exclusions": exclusions,
        "json_parses": json_parses,
        "privacy_classes": list(patterns),
        "confirmed_privacy_hits": 0,
        "out_of_scope_paths": [],
        "x2_paths_present": False,
        "diff_hygiene": True,
    }
    manifest = {
        "schema": "ghc.family.normalized-lf-index-manifest.v678.v1.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "entry_count": len(entries),
        "entries": entries,
        "declared_self_exclusions": exclusions,
    }
    write_json(REPO / privacy_rel, privacy)
    write_json(REPO / review_rel, review)
    write_json(REPO / manifest_rel, manifest)
    return {
        "state": review["state"],
        "reviewed_entry_count": len(entries),
        "json_parses": json_parses,
        "scanner_candidate_count": len(candidates),
        "confirmed_privacy_hits": 0,
        "written_receipts": exclusions,
    }


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--staged-review":
        print(json.dumps(build_staged_review(), indent=2, sort_keys=True))
    elif len(sys.argv) == 1:
        print(json.dumps({"written": build()}, indent=2, sort_keys=True))
    else:
        raise SystemExit("usage: build_ghc_family_caelen_ash_v678_v1_x1.py [--staged-review]")
