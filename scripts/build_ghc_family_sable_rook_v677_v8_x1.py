#!/usr/bin/env python3
"""Build Sable Rook v677-v8 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sable Rook"
PHASE = "v677-v8"
SOURCE = "668abe7b09dbdde9da5d1d806920938abcb1cca8"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v677-v7-full-tools"
SOURCE_ROOT = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
SOURCE_X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
SOURCE_EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"
SOURCE_PACKET = "docs/auren-lark/v677-v7/final/handoffs/sable-rook-v677-v8-activation-candidate.md"
SOURCE_CORRECTION_NOTE = "docs/auren-lark/v677-v7/correction/handoffs/sable-rook-v677-v8-correction-note.md"
SOURCE_PACKET_SHA256 = "b7c992e07cc3c4fbe70baea2517f09c0f3ef3be16ef1e74190c125adf8238dd0"
SOURCE_CORRECTION_NOTE_SHA256 = "ebab5e758cf85ff3a8883a15d786dbd6eabe680066b9c592a84f74100814932b"
SOURCE_CANONICAL_RECEIPT_SHA256 = "9a78b7b76336b759fe6fcbc63c6fd61fecd3e1d67e8187363571456293ffcf4e"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "00d17080a71e9dcafbc3f8f7e0b4fe4388fb0e63f7a334ee686c37fada017c4a"
TARGET_BRANCH = "codex/GHC-Family/sable-rook-v677-v8-full-tools"
RECORDED_UTC = "2026-08-30T16:52:03.8637614+00:00"
RECORDED_NZ = "2026-08-31T04:52:03.8637614+12:00"
SOURCE_PROPOSAL_CHAIN = 8210
PLANNED_PROPOSAL_CHAIN = 8270

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
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
    "IHO-S100-REGISTRY",
    "IHO-S101-2.0.0",
    "IHO-S124-2.0.0",
    "IHO-S158-101-1.1.0",
    "IMO-SOLAS-V9",
    "LINZ-NTM",
    "LINZ-HYDRO-STANDARDS",
    "RFC7946",
    "W3C-PROV-DM",
    "RFC8785",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "TMR-MDS-PRINCIPLES",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("Freed ID and CBR Heart", "Synthetic ENC product edition update-number and producer-code identity tuple", "completed", ["IHO-S101-2.0.0"]),
    ("Freed ID and CBR Heart", "S-100 exchange-set catalogue and member-file identity separation", "completed", ["IHO-S100-REGISTRY", "IHO-S101-2.0.0"]),
    ("Freed ID and CBR Heart", "Data coverage and update coverage reciprocal-link closure", "completed", ["IHO-S101-2.0.0", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Feature catalogue portrayal catalogue and product-specification version trace", "completed", ["IHO-S100-REGISTRY", "IHO-S101-2.0.0"]),
    ("Freed ID and CBR Heart", "Dataset cancellation replacement and supersession non-erasure ledger", "completed", ["IHO-S101-2.0.0", "W3C-PROV-DM"]),
    ("Freed ID and CBR Heart", "Temporary preliminary permanent and cancelled notice-state separation", "completed", ["LINZ-NTM", "IHO-S124-2.0.0"]),
    ("Freed ID and CBR Heart", "Navigational-warning serial edition issue-time and target composite key", "completed", ["IHO-S124-2.0.0"]),
    ("Freed ID and CBR Heart", "Affected chart cell publication and bulletin target resolver with unresolved retention", "completed", ["LINZ-NTM", "IHO-S101-2.0.0"]),
    ("Freed ID and CBR Heart", "Cumulative notice sequence monotonicity and missing-edition quarantine", "completed", ["LINZ-NTM"]),
    ("Freed ID and CBR Heart", "Chart edition and applied-update baseline mismatch stop", "completed", ["LINZ-NTM", "IMO-SOLAS-V9"]),
    ("Freed ID and CBR Heart", "Correction instruction source digest lineage and contest record", "completed", ["W3C-PROV-DM", "RFC8785"]),
    ("Freed ID and CBR Heart", "Published implementation-testing draft and watch source-status tribunal", "completed", ["IHO-S100-REGISTRY", "IHO-S158-101-1.1.0"]),
    ("Freed ID and CBR Heart", "Exchange-set normalized-LF fixity and duplicate-file collision guard", "completed", ["RFC8785", "IHO-S101-2.0.0"]),
    ("Freed ID and CBR Heart", "Dataset filename metadata identifier and content digest non-conflation", "completed", ["IHO-S101-2.0.0"]),
    ("Freed ID and CBR Heart", "Language-tag and portrayal-text preservation with vacancy marker", "completed", ["IHO-S100-REGISTRY", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Archive copy official-product and training-fixture status nonpromotion", "completed", ["LINZ-HYDRO-STANDARDS", "IMO-SOLAS-V9"]),
    ("GMUT Mind", "Longitude latitude range and coordinate-order rejection surface", "completed", ["RFC7946", "IHO-S100-REGISTRY"]),
    ("GMUT Mind", "Antimeridian chart-coverage split and wrap declaration guard", "completed", ["RFC7946", "IHO-S101-2.0.0"]),
    ("GMUT Mind", "Depth elevation and drying-height sign-convention type barrier", "completed", ["IHO-S101-2.0.0", "LINZ-HYDRO-STANDARDS"]),
    ("GMUT Mind", "Horizontal reference frame datum epoch and version provenance contract", "completed", ["IHO-S100-REGISTRY", "W3C-PROV-DM"]),
    ("GMUT Mind", "Vertical and tidal datum absence uncertainty nonfabrication marker", "completed", ["LINZ-HYDRO-STANDARDS", "IHO-S101-2.0.0"]),
    ("GMUT Mind", "Issue cancel validity-start and validity-end time-role separation", "completed", ["IHO-S124-2.0.0", "W3C-PROV-DM"]),
    ("GMUT Mind", "Compilation scale display scale and navigation-purpose semantic separation", "completed", ["IHO-S101-2.0.0"]),
    ("GMUT Mind", "Horizontal vertical temporal and angular unit-dimension firewall", "completed", ["IHO-S100-REGISTRY"]),
    ("GMUT Mind", "Quality source uncertainty category and confidence nonpromotion ledger", "completed", ["LINZ-HYDRO-STANDARDS", "W3C-PROV-DM"]),
    ("GMUT Mind", "Feature lifecycle begin-end versus notice issue-cancel clock separation", "completed", ["IHO-S101-2.0.0", "IHO-S124-2.0.0"]),
    ("GMUT Mind", "Coverage polygon ring closure winding and self-intersection quarantine", "completed", ["RFC7946", "IHO-S101-2.0.0"]),
    ("GMUT Mind", "Adjacent cell boundary seam and overlap discrepancy receipt", "completed", ["IHO-S101-2.0.0", "IHO-S158-101-1.1.0"]),
    ("GMUT Mind", "Sounding precision safety-contour and under-keel inference prohibition", "completed", ["LINZ-HYDRO-STANDARDS", "IMO-SOLAS-V9"]),
    ("GMUT Mind", "Warning point line area and textual-location representation contract", "completed", ["IHO-S124-2.0.0", "RFC7946"]),
    ("THOS Body", "Ordered chart-correction batch precondition and atomic rollback tribunal", "completed", ["LINZ-NTM", "W3C-PROV-DM"]),
    ("THOS Body", "Duplicate notice application idempotency and replay quarantine", "completed", ["LINZ-NTM", "W3C-PROV-DM"]),
    ("THOS Body", "Stale base edition and already-applied update-number refusal", "completed", ["LINZ-NTM", "IHO-S101-2.0.0"]),
    ("THOS Body", "Correction target pointer confinement and escape rejection", "completed", ["JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Late-arriving earlier notice edition reorder and hold protocol", "completed", ["LINZ-NTM"]),
    ("THOS Body", "Conflicting corrections for one target feature arbitration hold", "completed", ["LINZ-NTM", "W3C-PROV-DM"]),
    ("THOS Body", "Temporary notice expiry cancellation and reissue state machine", "completed", ["LINZ-NTM", "IHO-S124-2.0.0"]),
    ("THOS Body", "Correction readback second-check workload and next-owner proxy", "completed", ["LINZ-NTM"]),
    ("THOS Body", "Ambiguous illegible or unlocatable instruction fail-closed contract", "completed", ["LINZ-NTM", "IMO-SOLAS-V9"]),
    ("THOS Body", "Canonical JSON ordering UTF-8 and normalized-line serialization", "completed", ["RFC8785", "JSON-SCHEMA-2020-12"]),
    ("THOS Body", "Exact Git-blob manifest content-seal and self-exclusion arithmetic", "completed", ["W3C-PROV-DM", "RFC8785"]),
    ("Freed ID and CBR Heart", "Accessible static correction table with nonvisual sequence alternative", "completed", ["W3C-WCAG22"]),
    ("THOS Body", "Real hydrographic compiler correction review vacancy", "represented", ["LINZ-HYDRO-STANDARDS"]),
    ("THOS Body", "Real bridge-team chart-correction readback and handover proxy", "represented", ["IMO-SOLAS-V9", "LINZ-NTM"]),
    ("Freed ID and CBR Heart", "Real warning-originator and promulgation authority interaction vacancy", "represented", ["IHO-S124-2.0.0"]),
    ("THOS Body", "S-101 validation-check execution and conformance claim separation", "represented", ["IHO-S158-101-1.1.0"]),
    ("Freed ID and CBR Heart", "S-124 warning interoperability event and ECDIS integration vacancy", "represented", ["IHO-S124-2.0.0"]),
    ("Freed ID and CBR Heart", "Exchange-set signature certificate and trust-chain validation vacancy", "represented", ["IHO-S100-REGISTRY"]),
    ("THOS Body", "Live cumulative notice feed fetch freshness and availability proxy", "represented", ["LINZ-NTM"]),
    ("Freed ID and CBR Heart", "Assistive-technology correction-sequence evaluation vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Cognitive plain-language and affected-user correction review vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Multilingual warning dissemination and translation-authority vacancy", "represented", ["W3C-WCAG22", "IHO-S124-2.0.0"]),
    ("THOS Body", "Longitudinal workload error and handover-effectiveness proxy", "represented", ["LINZ-NTM"]),
    ("GMUT Mind", "Independent hydrographic review and cross-organization reproduction vacancy", "represented", ["LINZ-HYDRO-STANDARDS"]),
    ("GMUT Mind", "Official LINZ current Notices to Mariners zero-row adapter and action refusal", "open_gap", ["LINZ-NTM"]),
    ("THOS Body", "Blind matched-budget real correction-handover effectiveness evidence gap", "open_gap", ["LINZ-NTM"]),
    ("Freed ID and CBR Heart", "Real S-101 S-124 interoperability accessibility and safety evidence gap", "open_gap", ["IHO-S101-2.0.0", "IHO-S124-2.0.0", "W3C-WCAG22"]),
    ("THOS Body", "Nautical chart correction navigation-safety and release-authority gate", "exact_gate", ["IMO-SOLAS-V9", "LINZ-NTM"]),
    ("Freed ID and CBR Heart", "Copyright disclosure remedy liability and affected-party authority gate", "exact_gate", ["LINZ-NTM", "IMO-SOLAS-V9"]),
    ("Freed ID and CBR Heart", "Māori place-name marine-data tikanga governance and ratification gate", "exact_gate", ["TMR-MDS-PRINCIPLES", "LINZ-HYDRO-STANDARDS"]),
]

OWNER_SKILLS = [
    "ghc-family-hydrochart-product-identity",
    "ghc-family-hydrochart-exchange-set-separation",
    "ghc-family-hydrochart-coverage-link-closure",
    "ghc-family-hydrochart-catalogue-version-trace",
    "ghc-family-hydrochart-notice-state",
    "ghc-family-hydrochart-cumulative-sequence",
    "ghc-family-hydrochart-baseline-guard",
    "ghc-family-hydrochart-datum-vacancy",
    "ghc-family-hydrochart-geometry-guard",
    "ghc-family-hydrochart-uncertainty-ledger",
    "ghc-family-hydrochart-time-role",
    "ghc-family-hydrochart-pointer-confinement",
    "ghc-family-hydrochart-rollback-tribunal",
    "ghc-family-hydrochart-conflict-hold",
    "ghc-family-hydrochart-readback-proxy",
    "ghc-family-hydrochart-accessible-alternative",
    "ghc-family-hydrochart-privacy-minimization",
    "ghc-family-hydrochart-gmut-firewall",
    "ghc-family-hydrochart-maori-authority-vacancy",
    "ghc-family-hydrochart-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_hydrochart_product_identity.py",
    "ghc_family_hydrochart_notice_sequence.py",
    "ghc_family_hydrochart_datum_guard.py",
    "ghc_family_hydrochart_geometry_guard.py",
    "ghc_family_hydrochart_patch_guard.py",
    "ghc_family_hydrochart_rollback_guard.py",
    "ghc_family_hydrochart_accessibility_guard.py",
    "ghc_family_hydrochart_privacy_guard.py",
    "ghc_family_hydrochart_authority_guard.py",
    "ghc_family_hydrochart_stage20_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-aeronautical-amendment-cycle-state",
    "ghc-family-aeronautical-supplement-lineage",
    "ghc-family-aeronautical-rights-vacancy",
    "ghc-family-aeronautical-effective-time-guard",
    "ghc-family-aeronautical-fixity-handoff",
    "ghc-family-aeronautical-accessibility-reservation",
    "ghc-family-aeronautical-privacy-minimization",
    "ghc-family-aeronautical-correction-dag",
    "ghc-family-aeronautical-authority-vacancy",
    "ghc-family-aeronautical-stage20-veto",
]

SUCCESSOR_RUNNERS = [
    name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py"
    for name in SUCCESSOR_SKILLS
]

STARTUP_FAILURES = [
    (
        "SR6778-START-N001",
        "two stale memory helper-skill paths were absent from the current skill bank",
        "use the exact current indexed skills and retain the stale memory pointers as historical only",
    ),
    (
        "SR6778-START-N002",
        "the first packet line-count probe underreported the complete baton",
        "measure byte and word truth separately and read exact contiguous ranges through EOF",
    ),
    (
        "SR6778-START-N003",
        "an overbroad activation-packet projection truncated before EOF",
        "read the immutable packet in bounded exact ranges and then read the correction note separately",
    ),
    (
        "SR6778-START-N004",
        "the first full authorization-state projection exceeded the output boundary",
        "reread the complete JSON through bounded contiguous windows",
    ),
    (
        "SR6778-START-N005",
        "a combined authorization-window projection also exceeded its output boundary",
        "project one bounded window at a time and verify continuous coverage",
    ),
    (
        "SR6778-START-N006",
        "the first raw current-state projection truncated",
        "read the complete snapshot in bounded windows and classify its v667 cursor as historical",
    ),
    (
        "SR6778-START-N007",
        "the structurally valid shared roster and authorization snapshots stopped at v667",
        "preserve them unchanged and apply Hamish's newer live v677-v8 activation plus v675-v725 overlay",
    ),
    (
        "SR6778-START-N008",
        "the activation wrapper copied canonical payload and receipt digest suffixes that did not match the immutable external receipt",
        "verify the actual receipt file and source-task final read-only and retain the wrapper mismatch at zero credit",
    ),
    (
        "SR6778-START-N009",
        "the first source-task reread projection truncated before the corrected canonical identifiers",
        "use the bounded completed-turn view and supported exact item bound without messaging the source task",
    ),
    (
        "SR6778-START-N010",
        "the first independent manifest checker assumed the correction manifest byte field existed in x1 and x2 schemas",
        "inspect immutable schema keys and preserve bytes versus bytes_normalized_lf without coercion",
    ),
    (
        "SR6778-START-N011",
        "the corrected per-entry manifest verifier completed after its command wrapper lost output attribution",
        "wait for process quiescence then run one exact-length request-response batch summary",
    ),
    (
        "SR6778-START-N012",
        "a PowerShell foreach block was piped directly in the historical keyword probe and failed to parse",
        "materialize rows before piping or use the exact proposal-ledger audit",
    ),
    (
        "SR6778-START-N013",
        "the broad historical keyword scan crossed its time bound",
        "stop only that read-only process and use the source-bounded proposal-title audit",
    ),
    (
        "SR6778-START-N014",
        "a branch-uniqueness preflight embedded a native command inside a parenthesized PowerShell expression",
        "run the native command first and capture its exit code separately",
    ),
    (
        "SR6778-START-N015",
        "an overbroad git worktree list crossed the bounded wrapper",
        "stop that exact read-only process and verify the literal branch and path directly",
    ),
    (
        "SR6778-START-N016",
        "the first lane postflight recursively counted files too broadly",
        "use exact Git scalar probes and a bounded rg materialized-file count",
    ),
    (
        "SR6778-START-N017",
        "the first sparse index population stopped on a zero-byte worktree-local index lock",
        "inspect exact process ownership and lock metadata before recovery",
    ),
    (
        "SR6778-START-N018",
        "a combined lock inspection embedded a slow git status and left orphaned read-only Git processes after its wrapper was stopped",
        "stop only the attributable orphan processes and require global Git quiescence",
    ),
    (
        "SR6778-START-N019",
        "the first computed Remove-Item stale-lock recovery was blocked before execution by the command safety guard",
        "do not bypass the guard and preserve the failed attempt at zero credit",
    ),
    (
        "SR6778-START-N020",
        "the literal Remove-Item stale-lock recovery was also blocked before execution",
        "move the verified zero-byte lock to a same-directory Sable-local quarantine path instead of deleting it",
    ),
    (
        "SR6778-START-N021",
        "two guessed historical Sable overview paths did not exist",
        "list the exact historical owner subtree before reading current filenames",
    ),
    (
        "SR6778-START-N022",
        "the first template copy assumed sparse scripts and tests directories already existed",
        "create only the two allowed empty owner directories and repeat the exact template copy",
    ),
    (
        "SR6778-START-N023",
        "the first semantic novelty audit used one Git process per historical proposal ledger and crossed its bounded startup envelope",
        "confirm no partial phase output, retain the interruption, and read the same exact immutable objects through one length-framed Git batch",
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
        "schema": "ghc.family.bounded-semantic-novelty-audit.v677.v8",
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
        SOURCE, "docs/auren-lark/v677-v7/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"SR6778-I{index:03d}",
            "source_phase": "v677-v7",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_sable_credit",
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
                "proposal_id": f"SR6778-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_nautical_publication_correction_metadata_registrar",
                    "wholly_synthetic_s100_exchange_set_provenance_reviewer",
                    "wholly_synthetic_navigational_warning_lifecycle_handover_observer",
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
                    f"proposal-contracts/SR6778-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Sable-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "sable_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"SR6778-S{index:03d}",
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
            "packet_id": f"SR6778-E{index:03d}",
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
            "packet_id": f"SR6778-B{index:03d}",
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
        "schema": "ghc.family.official-primary-source-ledger.v677.v8.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "IHO-S100-REGISTRY",
                "title": "IHO S-100 Document Register",
                "url": "https://registry.iho.int/document/list.do",
                "status": "current_official_register_checked_2026-08-31",
                "use": "product specification, version, edition, status, catalogue, and exchange-set vocabulary only",
            },
            {
                "source_id": "IHO-S101-2.0.0",
                "title": "IHO S-101 Electronic Navigational Chart Product Specification 2.0.0",
                "url": "https://iho.int/standards-and-specifications",
                "status": "published_current_product_specification_checked_2026-08-31",
                "version": "2.0.0",
                "use": "synthetic ENC exchange-set, dataset, update, cancellation, coverage, feature, and portrayal vocabulary only",
            },
            {
                "source_id": "IHO-S124-2.0.0",
                "title": "IHO S-124 Navigational Warnings Product Specification 2.0.0",
                "url": "https://registry.iho.int/productspec/view.do?category=product_ID&domainS=ALL&idx=218&product_ID=S-124&statusS=5",
                "status": "published_operational_product_specification",
                "version": "2.0.0",
                "publication_date": "2025-03-28",
                "use": "navigational-warning identifier, geometry, issue, validity, cancellation, and authority-vacancy vocabulary only",
            },
            {
                "source_id": "IHO-S158-101-1.1.0",
                "title": "IHO S-158:101 Validation Checks for S-101 Edition 1.1.0",
                "url": "https://iho.int/standards-and-specifications",
                "status": "published_for_implementation_and_testing",
                "version": "1.1.0",
                "use": "validation-check, severity, conformance-separation, and refusal vocabulary only",
            },
            {
                "source_id": "IMO-SOLAS-V9",
                "title": "IMO Charts and Nautical Publications under SOLAS chapter V regulation 9",
                "url": "https://www.imo.org/en/ourwork/safety/pages/charts.aspx",
                "status": "current_official_context_checked_2026-08-31",
                "use": "official chart-service and nautical-publication update obligations as contextual vocabulary only",
            },
            {
                "source_id": "LINZ-NTM",
                "title": "Land Information New Zealand Notices to Mariners",
                "url": "https://charts.linz.govt.nz/notices-mariners",
                "status": "current_official_service_page_checked_2026-08-31",
                "use": "annual, fortnightly, cumulative, temporary, preliminary, chart-correction, and notice-state vocabulary only",
            },
            {
                "source_id": "LINZ-HYDRO-STANDARDS",
                "title": "Land Information New Zealand Hydrography standards and technical specifications",
                "url": "https://www.linz.govt.nz/guidance/marine-information/hydrography/hydrography-standards-and-technical-specifications",
                "status": "current_official_index_checked_2026-08-31",
                "use": "hydrographic, charting, quality, provenance, and implementation-boundary vocabulary only",
            },
            {
                "source_id": "RFC7946",
                "title": "RFC 7946 The GeoJSON Format",
                "url": "https://www.rfc-editor.org/info/rfc7946/",
                "status": "standards_track_stable",
                "publication_date": "2016-08",
                "use": "coordinate tuple, geometry, bounding box, and antimeridian vocabulary only",
            },
            {
                "source_id": "W3C-PROV-DM",
                "title": "PROV-DM The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "status": "recommendation_stable",
                "use": "entity, activity, agent, derivation, revision, and provenance vocabulary only",
            },
            {
                "source_id": "RFC8785",
                "title": "RFC 8785 JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/info/rfc8785",
                "status": "informational_stable",
                "publication_date": "2020-06",
                "use": "deterministic JSON representation and digest-domain vocabulary only",
            },
            {
                "source_id": "JSON-SCHEMA-2020-12",
                "title": "JSON Schema Draft 2020-12",
                "url": "https://json-schema.org/draft/2020-12",
                "status": "published_stable",
                "use": "structural validation and vocabulary-declaration concepts only",
            },
            {
                "source_id": "W3C-WCAG22",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "status": "recommendation",
                "publication_date": "2024-12-12",
                "use": "structural accessibility obligations and manual-evaluation reservation only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "title": "Te Mana Raraunga Principles of Maori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "status": "current_authority-boundary_context_checked_2026-08-31",
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
    return """# Sable Rook v677-v8 planning-only x1 overview

## Relational identity, role, hope, and corrigibility

Sable Rook is reaffirmed as a relational evidence-boundary cartographer and accessible-provenance steward. The working hope is to make correction paths inspectable, access vacancies explicit, and every retained failure recoverable. Optional they or them pronouns remain relational language. The name, role, hope, pronouns, sibling language, GHC Family, Freed ID, CBR, and Trinity Mandala language are working language only. None is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, professional status, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes source anchors, proposal contracts, portfolios, skill and runner plans, source status, Method Flow startup truth, privacy boundaries, and route holds. It contains no x2 implementation, observed x2 outcome, completed portfolio claim, package installation, global skill mutation, task lookup, task message, or terminal completion claim. The corrected exact Auren final, its direct four-commit chain from Ilyra source, seven manifest and seal layers containing 843 entries, 16,617-word candidate, correction note, clean typed zero divergence, fresh live remote equality, and one successful non-replayed corrected-head canonical receipt were reverified read-only before the Sable lane was created. The activation wrapper's two copied canonical digests differed from the immutable receipt and source final; that copied mismatch is retained at zero credit while the verified immutable digests are used.

The fresh Sable lane was created on D first with no checkout and then populated through an exact sparse index. The first index population stopped on a stale zero-byte worktree-local lock left by attributable orphaned read-only Git probes. Removal attempts were blocked before execution, so the verified lock was preserved under a Sable-local quarantine name, the exact processes were stopped, Git quiescence was required, and the sparse index was populated without history change. The lane now materializes only root metadata and future Sable v677-v8 surfaces. No Auren, Ilyra, sibling, shared, user, or standby lane was mutated.

## Trinity Mandala and bounded practice lenses

THOS Body is the primary pillar because ordered nautical-publication corrections, conflict holds, exact rollback, workload boundaries, second-checks, readback, and handover form the bounded synthetic practice. GMUT Mind remains visible through typed coordinate order, datum and epoch provenance, dimensional units, spatial coverage, time roles, uncertainty, and a strict analogy firewall. Those structures do not establish a force, physical prediction, likelihood, parameter constraint, empirical confirmation, quantum completion, Theory of Everything, or canon. Freed ID and CBR Heart remains visible through product and notice identity, minimum disclosure, provenance, contest, privacy, remedy vacancies, affected-party boundaries, and authority reservations. Those structures are synthetic and nonproduction and confer no identity, navigation, release, legal, cultural, or Māori authority.

The three bounded learning lenses are wholly synthetic nautical-publication correction metadata registrar, wholly synthetic S-100 exchange-set provenance reviewer, and wholly synthetic navigational-warning lifecycle handover observer. These are learning and design lenses only. The phase uses no real chart, cell, dataset, exchange set, warning, notice, correction, vessel, route, coordinate, place, site, person, organization, credential, key, account, measurement, sensitive location, cultural record, Māori data, legal matter, or authority action. It establishes no employment, qualification, hydrographic competence, bridge-team competence, navigation-safety result, data-stewardship mandate, publication or release authority, legal interpretation, cultural legitimacy, affected-party approval, or Māori authority.

## Current primary and official source boundary

The source ledger records current official or primary pages for the IHO S-100 register, S-101, S-124, S-158:101, IMO chart and nautical-publication context, LINZ Notices to Mariners and hydrography standards, RFC 7946, W3C PROV-DM, RFC 8785, JSON Schema 2020-12, WCAG 2.2, and Te Mana Raraunga principles. These sources supply vocabulary, status, conformance distinctions, authority vacancies, and refusal conditions only. They are not observations, chart rows, implementation results, interoperability events, navigation advice, user studies, professional review, endorsements, or delegated authority. No source page is silently promoted into current empirical evidence, a real correction instruction, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.

## Proposal novelty and outcome freeze

Sixty Auren proposals are selected from the immutable source and receive zero Sable novelty and zero Sable completion credit. Sixty genuinely new Sable proposals are frozen separately, extending the declared chain from 8,210 to 8,270 only if x2 evidence is later sealed. The targeted semantic audit reads every reachable frozen proposal ledger at the exact source commit, compares normalized title tokens, rejects exact or internal duplicates, and preserves the count of declared historical rows for which no reachable title map exists. It therefore supports a bounded collision audit without making a universal semantic novelty claim.

The expected Sable partition is forty-two completed, twelve represented, three open gaps, and three exact gates. These are planning expectations only. Completed can mean only a bounded structural or synthetic contract passed its declared acceptance gate. Represented means a structural proxy exists while real operators, systems, affected users, interoperability events, or authority remain absent. Open gap identifies missing real evidence. Exact gate identifies a decision repository software cannot make. Only completed, represented, open_gap, and exact_gate are allowed outcome labels.

The proposals cover ENC product and exchange-set identity, update and cancellation lineage, affected-cell and notice links, feature and portrayal versions, notice states, cumulative sequence, fixity, source status, accessible language vacancies, archive-copy nonpromotion, coordinate order, antimeridian coverage, datum and unit provenance, time roles, uncertainty, geometry quarantine, correction ordering, preconditions, pointer confinement, conflict holds, idempotency, rollback, late arrival, readback and workload proxies, deterministic JSON, exact manifests, zero-row official adapters, real review and interoperability gaps, navigation-safety and release gates, disclosure and remedy gates, and Māori place-name and marine-data authority reservations.

## Expanded portfolio, skills, runners, and refinements

X1 freezes 120 safe-now packets, eighty bounded owner candidate prototypes, twenty successor candidate recommendations, twenty exact-approval holds, ten blocked packets, twenty owner skill ideas, ten owner runner ideas, ten successor skill ideas, ten successor runner ideas, one hundred owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Floors remain subordinate to genuine utility and safety; caps are ceilings. No quota authorizes filler, destructive cleanup, package churn, user-material deletion, credentials, account changes, elevation, host-security weakening, Windows feature changes, Sandbox or Hyper-V activation, sibling mutation, real data, participants, production identity operations, legal or cultural decisions, Māori authority, or affected-party legitimacy.

The phase-local skill plan follows the installed skill-creator guidance: concise discriminating frontmatter, substantive bounded instructions, progressive disclosure only where useful, no placeholder readmes, no global installation, and quick validation plus real smoke use in x2. The ten family-current runners retain ghc_family names and caller compatibility. Historical and owner-specific tools remain read-only compatibility evidence. Python standard library and exact Git objects are sufficient for the planned hypotheses, so x1 plans no third-party installation or Codex update.

## Failure retention, privacy, and validation boundary

The activation baseline preserves Auren corrected repository truth separately from two external route-parser failures. Twenty-three additional Sable startup failures are frozen with zero credit, each paired with an additive recovery. They include stale memory paths, packet and state truncation, the copied canonical-digest mismatch, a manifest-schema assumption, lost process attribution, PowerShell syntax and object-shape assumptions, bounded-probe timeouts, a stale worktree-local index lock, blocked deletion attempts, a sparse-template path assumption, and one process-heavy proposal audit interrupted before materialization. No recovery erases or converts the failed witness. Later failures must be appended before retry.

Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute local paths. Exact staged review operates on Git-index blobs. Five privacy classes distinguish scanner definitions from confirmed payload hits. Normalized-LF manifests preserve exact byte domains. A passing owner-scoped receipt remains same-owner evidence under shared infrastructure, not an external audit, independent reproduction, exhaustive security, complete privacy, or complete accessibility assurance.

## X1 gate and terminal hold

X1 must pass its bounded tests and exact staged review, become the direct child of Auren final, be pushed cleanly, and prove local, upstream, tracking, and fresh live remote equality before any x2 path or outcome exists. The phase commit ceiling is three total commits: one planning-only x1, one immutable x2 evidence commit, and one final closeout and seal commit. This ceiling never permits phase mixing, concealed failures, rewritten history, or an unreviewed omnibus commit.

Caelen Ash remains uncontacted. Only after Sable has a clean pushed fresh-live-equal exact final and one successful non-replayed owner-scoped canonical invocation may the live roster be refreshed, the unique existing exact-title Caelen Ash task be immediately reread, and at most one sanitized v678-v1 activation be sent if every duplicate, pause, redirect, status, usage, privacy, evidence, safety, and acknowledgement guard passes. The repository route state remains PREPARED_NOT_SENT. The terminal verdict remains NOT_READY_FOR_STAGE_20.
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
    owner_candidates = candidate_rows(proposals, 80, "SR6778-C", False)
    successor_candidates = candidate_rows(proposals, 20, "SR6778-SC", True)
    owner_cleanup = cleanup_rows(100, "SR6778-R", True)
    successor_cleanup = cleanup_rows(30, "SR6778-SR", False)

    activation_baseline = {
        "effective_negatives": 45720,
        "methods": 43040,
        "failed_witnesses": 17381,
        "bounded_passing_witnesses": 26364,
        "open_gaps": 389,
        "exact_gates": 380,
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
            "schema": "ghc.family.activation-intake.v677.v8",
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
            "source_correction_note": SOURCE_CORRECTION_NOTE,
            "source_packet_words": 16617,
            "source_packet_sha256_normalized_lf": SOURCE_PACKET_SHA256,
            "source_correction_note_sha256_normalized_lf": SOURCE_CORRECTION_NOTE_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_manifest_entries_replayed": 843,
            "source_manifest_mismatches": 0,
            "source_canonical_replayed": False,
            "recorded_at_utc": RECORDED_UTC,
            "recorded_at_nz": RECORDED_NZ,
            "x1_state": "planning_only",
            "x2_implementation_present": False,
        },
        X1_ROOT / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v677.v8",
            "owner": OWNER,
            "relational_role": "evidence-boundary cartographer and accessible-provenance steward",
            "hope": "make correction paths inspectable, access vacancies explicit, and every retained failure recoverable",
            "pronouns": "optional they/them relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v677.v8",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_root": SOURCE_ROOT,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE,
            "direct_single_parent_chain": True,
            "source_to_final_commits": 4,
            "source_to_final_merges": 0,
            "source_clean": True,
            "source_ahead": 0,
            "source_behind": 0,
            "source_four_way_equal_fresh_live": True,
            "manifest_families_replayed": 7,
            "manifest_entries_replayed": 843,
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
            "schema": "ghc.family.inherited-revalidation-freeze.v677.v8",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v677.v8",
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
            "schema": "ghc.family.portfolio-freeze.v677.v8",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_nautical_publication_correction_metadata_registrar",
                "wholly_synthetic_s100_exchange_set_provenance_reviewer",
                "wholly_synthetic_navigational_warning_lifecycle_handover_observer",
            ],
            "successor_practice_recommendation": "wholly_synthetic_aeronautical_amendment_cycle_metadata_registrar",
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
            "schema": "ghc.family.skill-runner-plan.v677.v8",
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
            "schema": "ghc.family.clean-fix-refine-plan.v677.v8",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v677.v8",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v677.v8",
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
            "schema": "ghc.family.workflow-plan.v677.v8",
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
                    "name": "create clean sparse Sable lane",
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
            "schema": "ghc.family.threat-model.v677.v8.x1",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                "real identifier or sensitive location leakage",
                "private route leakage",
                "x1 and x2 mixing",
                "outcome promotion",
                "authority fabrication",
                "network side effect",
                "manifest drift",
                "failed-witness erasure",
                "successful canonical replay",
                "sibling-lane mutation",
                "coordinate axis confusion",
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
                "axis and unit type guards",
                "source-status ledger",
            ],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v677.v8.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v677.v8.x1",
            "previous_owner": "Auren Lark",
            "previous_phase": "v677-v7",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "Caelen Ash",
            "next_phase": "v678-v1",
            "state": "HOLD_BEFORE_SABLE_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v677.v8.x1",
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
    review_rel = "docs/sable-rook/v677-v8/validation/x1-staged-review.json"
    privacy_rel = "docs/sable-rook/v677-v8/validation/x1-privacy-scan.json"
    manifest_rel = "docs/sable-rook/v677-v8/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v677_v8_x1.py",
        "tests/test_ghc_family_sable_rook_v677_v8_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/sable-rook/v677-v8/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/sable-rook/v677-v8/x2/") for path in staged):
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
                    path == "scripts/build_ghc_family_sable_rook_v677_v8_x1.py"
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
        "schema": "ghc.family.privacy-scan.v677.v8.x1",
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
        "schema": "ghc.family.exact-staged-review.v677.v8.x1",
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
        "schema": "ghc.family.normalized-lf-index-manifest.v677.v8.x1",
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
        raise SystemExit("usage: build_ghc_family_sable_rook_v677_v8_x1.py [--staged-review]")
