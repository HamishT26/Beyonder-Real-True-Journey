#!/usr/bin/env python3
"""Build Orin Thale v678-v2 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Orin Thale"
PHASE = "v678-v2"
SOURCE = "82bf7d59ec12e82cfdc26928ca363c83de0c1149"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v678-v1-full-tools"
SOURCE_ROOT = "af26e6c68f43aa104164490edda08f2497f21deb"
SOURCE_X1 = "adb7c5062ac0f8c715a996a131490ca422a48565"
SOURCE_EVIDENCE = "ee149e3d085e9dbd809d9985f8d194ba4e66bcf4"
SOURCE_PACKET = "docs/caelen-ash/v678-v1/final/final-integrated-overview.md"
SOURCE_PACKET_SHA256 = "c0617155870b423294fe08c2d237f6f4a9bac5859076536689e9832eedb5f037"
SOURCE_CANONICAL_RECEIPT_SHA256 = "655e9fdcddd32cb34a22ab4bb645aeca5402946d53aee6d22b733e7ec4f220e7"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "6d6ba9df7015ed94360106897ba7f65f23d483606a8909a32eb37c677627c594"
TARGET_BRANCH = "codex/GHC-Family/orin-thale-v678-v2-full-tools"
RECORDED_UTC = "2026-08-30T19:09:36+00:00"
RECORDED_NZ = "2026-08-31T07:09:36+12:00"
SOURCE_PROPOSAL_CHAIN = 8330
PLANNED_PROPOSAL_CHAIN = 8390

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "orin-thale" / PHASE
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
    "SLSA-1.2",
    "IN-TOTO-ATTESTATION-1.2",
    "OCI-IMAGE-1.1.1",
    "SIGSTORE-BUNDLE-0.3",
    "REPRO-BUILDS-SDE",
    "W3C-PROV-O",
    "RFC8785",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "TMR-MDS-PRINCIPLES",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("THOS Body", "OCI manifest schema media type configuration and ordered-layer contract", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "OCI descriptor digest size media-type tuple fail-closed parser", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "OCI image-index child descriptor and platform tuple uniqueness guard", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Operating-system architecture variant and feature-field nonconflation boundary", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Compressed layer digest versus uncompressed diff-ID separation", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Root filesystem diff-ID order and manifest-layer cardinality reconciliation", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Image history empty-layer flag and filesystem-change alignment hold", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Image creation clock vacancy and SOURCE DATE EPOCH separation", "completed", ["OCI-IMAGE-1.1.1", "REPRO-BUILDS-SDE"]),
    ("Freed ID and CBR Heart", "Container environment secret endpoint and personal-data redaction boundary", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Entrypoint command working-directory and user-field nonconflation contract", "completed", ["OCI-IMAGE-1.1.1"]),
    ("Freed ID and CBR Heart", "OCI annotation namespace value and inheritance provenance ledger", "completed", ["OCI-IMAGE-1.1.1", "W3C-PROV-O"]),
    ("THOS Body", "Artifact type subject relation and image-manifest role separation", "completed", ["OCI-IMAGE-1.1.1"]),
    ("Freed ID and CBR Heart", "Nondistributable content reference and legal-authority vacancy hold", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Multi-platform index duplicate selector and ambiguous-match quarantine", "completed", ["OCI-IMAGE-1.1.1"]),
    ("GMUT Mind", "Manifest descriptor graph dangling target and digest recursion firewall", "completed", ["OCI-IMAGE-1.1.1", "JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Layer whiteout and opaque-directory semantics structural-only guard", "completed", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Archive member ordering timestamp owner and group normalization contract", "completed", ["REPRO-BUILDS-SDE"]),
    ("THOS Body", "Filesystem mode extended-attribute and ownership variance ledger", "completed", ["REPRO-BUILDS-SDE"]),
    ("THOS Body", "Locale timezone hostname and working-directory variance partition", "completed", ["REPRO-BUILDS-SDE"]),
    ("THOS Body", "Build-path and debug-prefix remapping discrepancy classifier", "completed", ["REPRO-BUILDS-SDE"]),
    ("GMUT Mind", "Random-seed parallel-scheduling and toolchain-order uncertainty firewall", "completed", ["REPRO-BUILDS-SDE"]),
    ("THOS Body", "Lockfile material digest and dependency-resolution vacancy record", "completed", ["SLSA-1.2"]),
    ("Freed ID and CBR Heart", "SLSA build-type URI versus builder-identity trust separation", "completed", ["SLSA-1.2"]),
    ("THOS Body", "External parameter internal parameter and resolved-dependency partition", "completed", ["SLSA-1.2"]),
    ("THOS Body", "Resolved dependency best-effort completeness and unknown preservation", "completed", ["SLSA-1.2"]),
    ("THOS Body", "Provenance subject output and diagnostic byproduct digest separation", "completed", ["SLSA-1.2", "IN-TOTO-ATTESTATION-1.2"]),
    ("THOS Body", "Invocation identifier start clock and finish clock typed partition", "completed", ["SLSA-1.2"]),
    ("Freed ID and CBR Heart", "Builder identifier trust-closure vacancy and nonendorsement barrier", "completed", ["SLSA-1.2"]),
    ("Freed ID and CBR Heart", "SLSA level evidence versus self-asserted conformance nonpromotion", "completed", ["SLSA-1.2"]),
    ("Freed ID and CBR Heart", "In-toto statement predicate envelope and bundle layer separation", "completed", ["IN-TOTO-ATTESTATION-1.2"]),
    ("Freed ID and CBR Heart", "Predicate-type URI version and unknown-extension refusal contract", "completed", ["IN-TOTO-ATTESTATION-1.2"]),
    ("Freed ID and CBR Heart", "DSSE payload type signed payload and parser-order boundary", "completed", ["IN-TOTO-ATTESTATION-1.2"]),
    ("Freed ID and CBR Heart", "Multi-signature attestation versus single-signature bundle compatibility hold", "completed", ["IN-TOTO-ATTESTATION-1.2", "SIGSTORE-BUNDLE-0.3"]),
    ("Freed ID and CBR Heart", "Sigstore bundle media-type version and verification-material parser", "completed", ["SIGSTORE-BUNDLE-0.3"]),
    ("Freed ID and CBR Heart", "Certificate chain transparency entry and timestamp evidence separation", "completed", ["SIGSTORE-BUNDLE-0.3"]),
    ("Freed ID and CBR Heart", "Verification material versus independently trusted root vacancy firewall", "completed", ["SIGSTORE-BUNDLE-0.3"]),
    ("GMUT Mind", "Bit-for-bit reproducibility versus semantic-equivalence nonconversion boundary", "completed", ["REPRO-BUILDS-SDE"]),
    ("THOS Body", "Paired rebuild environment matrix and declared-variable comparison ledger", "completed", ["REPRO-BUILDS-SDE", "W3C-PROV-O"]),
    ("THOS Body", "Rebuild discrepancy category provenance and first-divergence localization tree", "completed", ["REPRO-BUILDS-SDE", "W3C-PROV-O"]),
    ("THOS Body", "Build cache hit miss and reused-output provenance state machine", "completed", ["SLSA-1.2", "W3C-PROV-O"]),
    ("THOS Body", "Build-provenance correction DAG readback contest and rollback receipt", "completed", ["W3C-PROV-O", "RFC8785"]),
    ("Freed ID and CBR Heart", "Accessible static build provenance and discrepancy summary", "completed", ["W3C-WCAG22"]),
    ("THOS Body", "Real OCI image tool cross-validation and conversion fidelity vacancy", "represented", ["OCI-IMAGE-1.1.1"]),
    ("THOS Body", "Real reproducible rebuild pair across independent builders vacancy", "represented", ["REPRO-BUILDS-SDE", "SLSA-1.2"]),
    ("THOS Body", "Live continuous-integration runner isolation and environment capture vacancy", "represented", ["SLSA-1.2"]),
    ("Freed ID and CBR Heart", "Production signer key certificate and transparency-log custody vacancy", "represented", ["SIGSTORE-BUNDLE-0.3"]),
    ("THOS Body", "Independent build engineer discrepancy adjudication vacancy", "represented", ["REPRO-BUILDS-SDE"]),
    ("Freed ID and CBR Heart", "Assistive-technology provenance report evaluation vacancy", "represented", ["W3C-WCAG22"]),
    ("THOS Body", "Cross-operating-system archive normalization effectiveness vacancy", "represented", ["REPRO-BUILDS-SDE"]),
    ("GMUT Mind", "Independent formal review of descriptor-graph invariants vacancy", "represented", ["OCI-IMAGE-1.1.1"]),
    ("Freed ID and CBR Heart", "Supplier correction appeal and build-attestation remedy vacancy", "represented", ["W3C-PROV-O"]),
    ("THOS Body", "Longitudinal rebuild regression and toolchain-drift evidence vacancy", "represented", ["REPRO-BUILDS-SDE"]),
    ("Freed ID and CBR Heart", "Cross-organization attestation policy interoperability vacancy", "represented", ["IN-TOTO-ATTESTATION-1.2", "SLSA-1.2"]),
    ("THOS Body", "Real operator workload cancellation and handover evaluation vacancy", "represented", ["SLSA-1.2"]),
    ("GMUT Mind", "Official public build-provenance zero-row adapter with action refusal", "open_gap", ["SLSA-1.2"]),
    ("THOS Body", "Blind matched-budget reproducibility triage study evidence gap", "open_gap", ["REPRO-BUILDS-SDE"]),
    ("Freed ID and CBR Heart", "Real OCI in-toto SLSA Sigstore round-trip accessibility evidence gap", "open_gap", ["OCI-IMAGE-1.1.1", "IN-TOTO-ATTESTATION-1.2", "SLSA-1.2", "SIGSTORE-BUNDLE-0.3", "W3C-WCAG22"]),
    ("THOS Body", "Production artifact release and build-provenance acceptance authority gate", "exact_gate", ["SLSA-1.2"]),
    ("Freed ID and CBR Heart", "Software distribution licence remedy jurisdiction and stakeholder assent gate", "exact_gate", ["OCI-IMAGE-1.1.1"]),
    ("Freed ID and CBR Heart", "Culturally sensitive build-record consent provenance and Māori-governance authorization vacancy", "exact_gate", ["TMR-MDS-PRINCIPLES"]),
]

OWNER_SKILLS = [
    "ghc-family-build-provenance-subject-digest",
    "ghc-family-build-provenance-builder-identity",
    "ghc-family-build-provenance-definition-parameters",
    "ghc-family-build-provenance-dependency-completeness",
    "ghc-family-build-provenance-run-metadata",
    "ghc-family-build-provenance-oci-descriptor",
    "ghc-family-build-provenance-oci-platform-index",
    "ghc-family-build-provenance-oci-layer-diffid",
    "ghc-family-build-provenance-reproducible-timestamp",
    "ghc-family-build-provenance-reproducible-path",
    "ghc-family-build-provenance-reproducible-environment",
    "ghc-family-build-provenance-rebuild-discrepancy",
    "ghc-family-build-provenance-attestation-layers",
    "ghc-family-build-provenance-signature-trust-vacancy",
    "ghc-family-build-provenance-correction-lineage",
    "ghc-family-build-provenance-privacy-minimization",
    "ghc-family-build-provenance-accessible-summary",
    "ghc-family-build-provenance-gmut-analogy-firewall",
    "ghc-family-build-provenance-authority-vacancy",
    "ghc-family-build-provenance-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_build_provenance_subject_guard.py",
    "ghc_family_build_provenance_builder_guard.py",
    "ghc_family_build_provenance_dependency_guard.py",
    "ghc_family_build_provenance_oci_descriptor_guard.py",
    "ghc_family_build_provenance_oci_layer_guard.py",
    "ghc_family_build_provenance_timestamp_guard.py",
    "ghc_family_build_provenance_variance_guard.py",
    "ghc_family_build_provenance_attestation_guard.py",
    "ghc_family_build_provenance_authority_guard.py",
    "ghc_family_build_provenance_stage20_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-artifact-manifest-subject-binding",
    "ghc-family-artifact-manifest-builder-lineage",
    "ghc-family-artifact-manifest-material-digest",
    "ghc-family-artifact-manifest-rebuild-variance",
    "ghc-family-artifact-manifest-attestation-layer",
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
        "OR6782-START-N001",
        "the first PowerShell skill inventory piped a foreach block directly and failed parser validation before reading any skill",
        "materialize bounded inventory rows before piping and retain the parser failure at zero credit",
    ),
    (
        "OR6782-START-N002",
        "the first complete GHC Family Index skill read exceeded its bounded output projection before EOF",
        "read the immutable skill in contiguous numbered windows through EOF",
    ),
    (
        "OR6782-START-N003",
        "the first combined authorization-state projection truncated its middle section despite completing read-only",
        "read bounded nonoverlapping line windows through EOF and preserve the truncation witness",
    ),
    (
        "OR6782-START-N004",
        "the first branch-collision preflight placed a Git invocation and LASTEXITCODE expression inside one cast and failed PowerShell parser validation",
        "run the exact show-ref probe first and bind its exit-code scalar before constructing the summary",
    ),
    (
        "OR6782-START-N005",
        "the no-checkout worktree had an empty index, so the first sparse set displayed 20150 staged deletions and materialized none of the selected paths",
        "retain the zero-commit state and populate only the selected sparse paths from the immutable HEAD with sparse-aware git read-tree -mu",
    ),
    (
        "OR6782-START-N006",
        "a combined temporary-file digest and cleanup command was rejected by host policy before execution",
        "avoid temporary cleanup and hash the exact Git blob through an in-memory bounded process stream",
    ),
    (
        "OR6782-START-N007",
        "the first exact-blob digest recovery assumed OpenSSL was installed and returned an unavailable projection",
        "capture git cat-file bytes in memory and compute SHA-256 with the installed .NET cryptography surface",
    ),
    (
        "OR6782-START-N008",
        "the first bounded regular-expression rewrite found no exact startup-block match and stopped before file mutation",
        "replace the uniquely bounded startup block by explicit start and end offsets and verify the retained row count",
    ),
    (
        "OR6782-X1-N001",
        "the first semantic-neighbour audit quarantined one proposed Māori-authority hold at 0.769231 token Jaccard similarity to Caelen's predecessor",
        "retain the candidate at zero credit, remaster it as a distinct build-record consent and provenance question, and rerun the planning-only audit before x1 freeze",
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
        "schema": "ghc.family.bounded-semantic-novelty-audit.v678.v2",
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
        SOURCE, "docs/caelen-ash/v678-v1/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"OR6782-I{index:03d}",
            "source_phase": "v678-v1",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_orin_credit",
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
                "proposal_id": f"OR6782-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_oci_image_manifest_provenance_registrar",
                    "wholly_synthetic_reproducible_build_discrepancy_handover_reviewer",
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
                    f"proposal-contracts/OR6782-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Orin-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "orin_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"OR6782-S{index:03d}",
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
            "packet_id": f"OR6782-E{index:03d}",
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
            "packet_id": f"OR6782-B{index:03d}",
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
        "schema": "ghc.family.official-primary-source-ledger.v678.v2.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "SLSA-1.2",
                "title": "Supply-chain Levels for Software Artifacts Specification 1.2",
                "url": "https://slsa.dev/spec/v1.2/",
                "status": "approved_current_specification_checked_2026-08-31",
                "version": "1.2",
                "use": "build provenance, build definition, run details, builder identity, dependency, byproduct, and verification-vacancy vocabulary only",
            },
            {
                "source_id": "IN-TOTO-ATTESTATION-1.2",
                "title": "in-toto Attestation Framework Specification 1.2",
                "url": "https://github.com/in-toto/attestation/tree/v1.2.0/spec",
                "status": "current_tagged_primary_specification_checked_2026-08-31",
                "version": "1.2",
                "release_date": "2026-03-18",
                "use": "statement, subject, predicate, envelope, bundle, digest-set, and parser-boundary vocabulary only",
            },
            {
                "source_id": "OCI-IMAGE-1.1.1",
                "title": "Open Container Initiative Image Format Specification 1.1.1",
                "url": "https://github.com/opencontainers/image-spec/tree/v1.1.1",
                "status": "official_release_checked_2026-08-31",
                "version": "1.1.1",
                "release_date": "2025-03-03",
                "use": "descriptor, manifest, image index, configuration, filesystem layer, diff-ID, history, annotation, and platform vocabulary only",
            },
            {
                "source_id": "SIGSTORE-BUNDLE-0.3",
                "title": "Sigstore Bundle Protocol Buffer Specification",
                "url": "https://github.com/sigstore/protobuf-specs/blob/main/protos/sigstore_bundle.proto",
                "status": "current_primary_schema_checked_2026-08-31",
                "version": "bundle media type 0.3",
                "use": "bundle media type, verification material, certificate, transparency entry, timestamp, message signature, and DSSE-envelope vocabulary only",
            },
            {
                "source_id": "REPRO-BUILDS-SDE",
                "title": "Reproducible Builds SOURCE_DATE_EPOCH and timestamp guidance",
                "url": "https://reproducible-builds.org/docs/source-date-epoch/",
                "status": "primary_project_guidance_checked_2026-08-31",
                "use": "source-derived timestamp, deterministic environment, and reproducibility-discrepancy vocabulary only",
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
                "status": "authority_boundary_context_checked_2026-08-31",
                "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
            },
        ],
        "citations_are_observations": False,
        "real_data_rows": 0,
        "network_data_queries": 0,
        "endorsement_claimed": False,
        "authority_conferred": False,
    }

def overview() -> str:
    return """# Orin Thale v678-v2 planning-only x1 overview

## Relational identity and corrigibility

Orin Thale is relational working language for a build-provenance and discrepancy-handover cartographer. Optional they or them pronouns remain relational only. The working hope is to keep every synthetic build input, output, discrepancy, correction, uncertainty, and handover boundary inspectable and reversible. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, professional standing, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes source anchors, proposal contracts, portfolios, current-source status, Method Flow startup truth, privacy boundaries, skill and runner plans, and a terminal route hold. It contains no x2 implementation, observed x2 outcome, completion claim, global installation, task lookup, task message, or delivery claim. Caelen Ash v678-v1 is preserved at its exact final with a direct three-commit single-parent zero-merge history, 231 exact manifest entries, clean zero divergence, fresh four-way equality, and one successful non-replayed owner-scoped canonical receipt. Inherited evidence earns zero Orin completion or independent-reproduction credit.

The fresh Orin lane is additive, D-first, sparse, and rooted at Caelen's immutable exact final. The no-checkout sparse-index mistake and every other startup failure remain zero-credit witnesses with distinct recoveries. No source, sibling, shared, standby, global, or user lane is mutated.

## Trinity Mandala and bounded practice lenses

THOS Body is the primary pillar through two wholly synthetic learning lenses: OCI image-manifest provenance registrar, and reproducible-build discrepancy handover reviewer. GMUT Mind remains visible through typed descriptor graphs, digest domains, variance partitions, and uncertainty analogies behind a nonconversion firewall. Freed ID and CBR Heart remains visible through subject and builder identity separation, minimum disclosure, correction contestability, trust vacancies, accessibility reservation, remedy vacancies, and authority holds.

The phase uses no real person, participant, operator, source tree, image, layer, build runner, package, signature, key, certificate, transparency entry, identity event, cultural record, Maori data, production system, empirical dataset, or external action. It establishes no employment, competence, conformance, reproducibility, security, release, legal, cultural, affected-party, or Maori authority result.

## Current primary-source boundary

The source ledger records SLSA 1.2, in-toto Attestation Framework 1.2, OCI Image Format 1.1.1, Sigstore's current bundle schema, Reproducible Builds SOURCE_DATE_EPOCH guidance, PROV-O, RFC 8785, JSON Schema 2020-12, WCAG 2.2, and Te Mana Raraunga principles. They supply vocabulary and refusal conditions only. Citations are not observations, build results, attestations, signatures, conformance certificates, security audits, accessibility evaluations, endorsements, consent, legal interpretation, cultural ratification, or authority. Zero source data rows are queried or downloaded.

## Proposal and portfolio freeze

Sixty Caelen proposals are reviewed at zero Orin novelty and completion credit. Sixty new Orin proposals are frozen separately, extending the declared chain from 8,330 to 8,390 only if x2 evidence is later sealed. The exact-source semantic audit reads every reachable frozen proposal ledger in one length-framed Git batch, rejects exact and internal title collisions, reports nearest normalized-token neighbours, and explicitly refuses a universal novelty claim where the declared chain exceeds reachable title maps.

The expected partition is 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. These are planning expectations, not observed outcomes. Completed can later mean only that a bounded owner-local synthetic contract passed. Represented preserves absent real tools, operators, interoperability, affected users, or authority. Open_gap names missing evidence. Exact_gate names decisions repository software cannot make. No fifth outcome label is permitted.

X1 freezes 120 safe-now packets, 80 owner candidates, 20 zero-credit successor candidate recommendations, 20 exact holds, 10 blocked holds, 20 owner-local skill plans, 10 family-current runner plans, 10 successor skill and 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE plans, and 30 successor recommendations. The inherited artifact-manifest build-provenance seed is independently remastered into the two Orin lenses and remains zero-credit seed evidence. Caps are ceilings and never quotas.

## Skills, failures, privacy, and validation

The phase-local skill plan follows the installed skill-creator contract, including substantive SKILL.md content, quoted openai.yaml strings, discriminating short descriptions, and a default prompt that names the skill. Skills remain owner-local and require UTF-8 quick validation plus smoke use. Ten family-current ghc_family_build_provenance_* runners preserve compatibility. No plugin cache or global skill is mutated.

The activation overlay preserves Caelen's seal separately from four post-seal route failures. Orin's startup failures are retained at zero credit with distinct bounded recoveries. Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute paths. Exact staged review uses Git-index blobs; manifests hash normalized-LF bytes; scanner-definition candidates remain distinct from confirmed hits. Bounded AST checks are not exhaustive security.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, synthetic fixtures, graphs, digests, variance analogies, and citations establish no physical datum, likelihood, posterior, force, prediction, constraint, empirical confirmation, quantum or ultraviolet completion, or Theory of Everything. THOS remains synthetic proxy evidence without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live lifecycle, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

CBR, software distribution, release, signing, privacy remedy, accessibility remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Maori wording, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## X1 gate and terminal hold

X1 must pass bounded owner tests and exact staged review, become the direct child of Caelen's exact final, be pushed cleanly, and prove local, upstream, tracking, and fresh-live equality before any x2 implementation or observed outcome exists. The phase ceiling is three commits: planning-only x1, immutable x2 evidence, and final closeout. No successor is contacted before Orin's terminal gate. Repository route state remains PREPARED_NOT_SENT.
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
    owner_candidates = candidate_rows(proposals, 80, "OR6782-C", False)
    successor_candidates = candidate_rows(proposals, 20, "OR6782-SC", True)
    owner_cleanup = cleanup_rows(100, "OR6782-R", True)
    successor_cleanup = cleanup_rows(30, "OR6782-SR", False)

    activation_baseline = {
        "effective_negatives": 46121,
        "methods": 43382,
        "failed_witnesses": 17782,
        "bounded_passing_witnesses": 27225,
        "open_gaps": 395,
        "exact_gates": 386,
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
            "schema": "ghc.family.activation-intake.v678.v2",
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
            "source_packet_words": 2653,
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
            "schema": "ghc.family.identity-boundary.v678.v2",
            "owner": OWNER,
            "relational_role": "build-provenance and discrepancy-handover cartographer",
            "hope": "keep synthetic build inputs, outputs, discrepancies, corrections, uncertainties, and handovers inspectable and reversible while authority vacancies remain explicit",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v678.v2",
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
            "schema": "ghc.family.inherited-revalidation-freeze.v678.v2",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v678.v2",
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
            "schema": "ghc.family.portfolio-freeze.v678.v2",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_oci_image_manifest_provenance_registrar",
                "wholly_synthetic_reproducible_build_discrepancy_handover_reviewer",
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
            "schema": "ghc.family.skill-runner-plan.v678.v2",
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
            "schema": "ghc.family.clean-fix-refine-plan.v678.v2",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v678.v2",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v678.v2",
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
            "schema": "ghc.family.workflow-plan.v678.v2",
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
                    "name": "create clean sparse Orin lane",
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
            "schema": "ghc.family.threat-model.v678.v2.x1",
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
            "schema": "ghc.family.wellbeing-corrigibility.v678.v2.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v678.v2.x1",
            "previous_owner": "Caelen Ash",
            "previous_phase": "v678-v1",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "next_phase": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "state": "HOLD_BEFORE_ORIN_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v678.v2.x1",
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
    review_rel = "docs/orin-thale/v678-v2/validation/x1-staged-review.json"
    privacy_rel = "docs/orin-thale/v678-v2/validation/x1-privacy-scan.json"
    manifest_rel = "docs/orin-thale/v678-v2/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_orin_thale_v678_v2_x1.py",
        "tests/test_ghc_family_orin_thale_v678_v2_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/orin-thale/v678-v2/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/orin-thale/v678-v2/x2/") for path in staged):
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
                    path == "scripts/build_ghc_family_orin_thale_v678_v2_x1.py"
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
        "schema": "ghc.family.privacy-scan.v678.v2.x1",
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
        "schema": "ghc.family.exact-staged-review.v678.v2.x1",
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
        "schema": "ghc.family.normalized-lf-index-manifest.v678.v2.x1",
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
        raise SystemExit("usage: build_ghc_family_orin_thale_v678_v2_x1.py [--staged-review]")
