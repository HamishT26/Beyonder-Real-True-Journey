#!/usr/bin/env python3
"""Build Liora Venn v678-v3 planning-only x1 artifacts."""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Liora Venn"
PHASE = "v678-v3"
SOURCE = "2c1b2fb714f8b7296a3399ebf3e8802ff5181a58"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v678-v2-full-tools"
SOURCE_ROOT = "82bf7d59ec12e82cfdc26928ca363c83de0c1149"
SOURCE_X1 = "5fc19e5e4ed9a3c49dc857e79d18724bf374b32a"
SOURCE_EVIDENCE = "1ad21f4b84affc7880339c203057292f456f80a7"
SOURCE_PACKET = "docs/orin-thale/v678-v2/final/final-integrated-overview.md"
SOURCE_PACKET_SHA256 = "9df5d59234863351808b0e6d8416d38a2b0223fc45aee49bef00163c4dec19c4"
SOURCE_CANONICAL_RECEIPT_SHA256 = "9e0e24b9cfe0e60685656bf56d79a05db78635aa85b8c58ea074d76dfef24e70"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "b219e9a25dee2444b2c8477e74561a16035dae7863ff1ff8746b505342a910d4"
TARGET_BRANCH = "codex/GHC-Family/liora-venn-v678-v3-full-tools"
RECORDED_UTC = "2026-08-30T19:55:02+00:00"
RECORDED_NZ = "2026-08-31T07:55:02+12:00"
SOURCE_PROPOSAL_CHAIN = 8390
PLANNED_PROPOSAL_CHAIN = 8450

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "liora-venn" / PHASE
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
    "LOC-RFS-2025-2026",
    "LOC-PREMIS-3.0",
    "LOC-SUSTAINABILITY-FORMATS",
    "NPS-MUSEUM-HANDBOOK-I",
    "NPS-MH1-CH5",
    "W3C-PROV-O",
    "RFC8785",
    "JSON-SCHEMA-2020-12",
    "W3C-WCAG22",
    "W3C-VC-DATA-MODEL-2.0",
    "TMR-MDS-PRINCIPLES",
}

# pillar, title, expected outcome, official or primary source needs
PROPOSAL_SPECS: list[tuple[str, str, str, list[str]]] = [
    ("Freed ID and CBR Heart", "Carrier identifier versus intellectual-content identifier nonconflation contract", "completed", ["LOC-PREMIS-3.0"]),
    ("Freed ID and CBR Heart", "Reformatting request intake state and source-custody vacancy tuple", "completed", ["LOC-PREMIS-3.0", "LOC-RFS-2025-2026"]),
    ("Freed ID and CBR Heart", "PREMIS object event agent rights entity role-separation guard", "completed", ["LOC-PREMIS-3.0"]),
    ("THOS Body", "Physical carrier side track channel and segment topology ledger", "completed", ["LOC-SUSTAINABILITY-FORMATS"]),
    ("THOS Body", "Playback equipment capability declaration versus observed condition firewall", "completed", ["LOC-RFS-2025-2026"]),
    ("THOS Body", "Sampling rate bit depth codec wrapper and channel-layout typed partition", "completed", ["LOC-SUSTAINABILITY-FORMATS"]),
    ("THOS Body", "Timebase frame-rate drop-frame flag and duration nonconversion contract", "completed", ["LOC-SUSTAINABILITY-FORMATS"]),
    ("Freed ID and CBR Heart", "Checksum algorithm value creation-event and verification-event separation", "completed", ["LOC-PREMIS-3.0", "RFC8785"]),
    ("Freed ID and CBR Heart", "Source master preservation master mezzanine and access-copy role guard", "completed", ["LOC-RFS-2025-2026"]),
    ("THOS Body", "Analog-to-digital transfer clock versus cataloging clock separation", "completed", ["LOC-PREMIS-3.0"]),
    ("Freed ID and CBR Heart", "Reformatting input output relationship and derivative-lineage DAG", "completed", ["LOC-PREMIS-3.0", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Technical metadata unknown partial and withheld nonpromotion state machine", "completed", ["LOC-PREMIS-3.0", "JSON-SCHEMA-2020-12"]),
    ("Freed ID and CBR Heart", "Rights-basis statement scope date jurisdiction and authority-vacancy ledger", "completed", ["LOC-PREMIS-3.0"]),
    ("Freed ID and CBR Heart", "Caption transcript audio-description and language-tag availability matrix", "completed", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Fixity retry contest readback and retained prior-state correction receipt", "completed", ["LOC-PREMIS-3.0", "W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "File-format preference versus local capability nonendorsement boundary", "completed", ["LOC-RFS-2025-2026"]),
    ("Freed ID and CBR Heart", "Embedded sidecar and catalog metadata precedence hold", "completed", ["LOC-PREMIS-3.0"]),
    ("THOS Body", "Batch queue priority cancellation retry workload and shift-handover proxy", "completed", ["W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Minimum-disclosure donor performer and rights-contact redaction boundary", "completed", ["W3C-VC-DATA-MODEL-2.0"]),
    ("Freed ID and CBR Heart", "Accessible static reformatting custody and uncertainty summary", "completed", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Stage 20 veto under unresolved audiovisual authenticity and rights gaps", "completed", ["LOC-PREMIS-3.0"]),
    ("THOS Body", "Trap map location code versus object location nonconflation contract", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Observation inspection identification and action date partition", "completed", ["NPS-MH1-CH5", "W3C-PROV-O"]),
    ("THOS Body", "Trap identifier device type lure type and service-state tuple", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Pest-evidence observation versus species identification nonconversion firewall", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Count unit interval duration and missing-observation typed ledger", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Facility zone room cabinet case and object-proximity topology guard", "completed", ["NPS-MUSEUM-HANDBOOK-I"]),
    ("THOS Body", "Environmental observation instrument vacancy and calibration-status hold", "completed", ["NPS-MUSEUM-HANDBOOK-I"]),
    ("Freed ID and CBR Heart", "Threshold definition version scope and authority-vacancy record", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Preventive exclusion housekeeping and treatment action-category separation", "completed", ["NPS-MH1-CH5"]),
    ("Freed ID and CBR Heart", "Chemical-treatment recommendation and authorization refusal boundary", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Observation photograph vacancy and zero-image evidence marker", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Trap relocation replacement retirement and lineage state machine", "completed", ["NPS-MH1-CH5", "W3C-PROV-O"]),
    ("THOS Body", "Duplicate trap observation and ambiguous-location quarantine", "completed", ["NPS-MH1-CH5"]),
    ("Freed ID and CBR Heart", "Integrated-pest-management revision lineage with superseded-record visibility", "completed", ["W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Sensitive collection location minimization and public-export redaction", "completed", ["W3C-VC-DATA-MODEL-2.0"]),
    ("Freed ID and CBR Heart", "Hazard note role restriction and professional-review vacancy", "completed", ["NPS-MH1-CH5"]),
    ("THOS Body", "Monitoring schedule cancellation workload and shift-handover proxy", "completed", ["W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Accessible static IPM observation and vacancy summary", "completed", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "PROV-O derivation revision and invalidation map for synthetic observation records", "completed", ["W3C-PROV-O"]),
    ("GMUT Mind", "JSON canonicalization digest-domain and source-byte distinction", "completed", ["RFC8785"]),
    ("GMUT Mind", "Cross-lens audiovisual-to-IPM custody analogy nonconversion firewall", "completed", ["W3C-PROV-O"]),
    ("THOS Body", "Real carrier-format identification tool comparison vacancy", "represented", ["LOC-SUSTAINABILITY-FORMATS"]),
    ("THOS Body", "Real playback-chain calibration and signal-quality measurement vacancy", "represented", ["LOC-RFS-2025-2026"]),
    ("Freed ID and CBR Heart", "Independent audiovisual conservator reformatting review vacancy", "represented", ["LOC-RFS-2025-2026"]),
    ("Freed ID and CBR Heart", "Assistive-technology review of preservation reports vacancy", "represented", ["W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Real rights-holder clearance and affected-party acceptance vacancy", "represented", ["LOC-PREMIS-3.0"]),
    ("THOS Body", "Longitudinal format-obsolescence and migration-outcome vacancy", "represented", ["LOC-SUSTAINABILITY-FORMATS"]),
    ("THOS Body", "Real pest-identification expert adjudication vacancy", "represented", ["NPS-MH1-CH5"]),
    ("THOS Body", "Real sensor-calibration and environment-data review vacancy", "represented", ["NPS-MUSEUM-HANDBOOK-I"]),
    ("THOS Body", "Real IPM effectiveness evaluation across collection spaces vacancy", "represented", ["NPS-MH1-CH5"]),
    ("Freed ID and CBR Heart", "Independent museum conservator treatment review vacancy", "represented", ["NPS-MUSEUM-HANDBOOK-I"]),
    ("THOS Body", "Affected-worker workload and safety review vacancy", "represented", ["NPS-MH1-CH5"]),
    ("Freed ID and CBR Heart", "Cross-institution preservation-metadata interoperability vacancy", "represented", ["LOC-PREMIS-3.0"]),
    ("Freed ID and CBR Heart", "Official public audiovisual-preservation zero-row adapter with action refusal", "open_gap", ["LOC-RFS-2025-2026"]),
    ("THOS Body", "Blind matched-budget synthetic custody-triage study evidence gap", "open_gap", ["W3C-PROV-O"]),
    ("Freed ID and CBR Heart", "Real PREMIS RFS IPM round-trip accessibility evidence gap", "open_gap", ["LOC-PREMIS-3.0", "LOC-RFS-2025-2026", "NPS-MH1-CH5", "W3C-WCAG22"]),
    ("Freed ID and CBR Heart", "Production audiovisual reformatting release and authenticity-acceptance authority gate", "exact_gate", ["LOC-PREMIS-3.0"]),
    ("Freed ID and CBR Heart", "Museum treatment hazard safety collection custody and remedy authority gate", "exact_gate", ["NPS-MH1-CH5"]),
    ("Freed ID and CBR Heart", "Culturally sensitive audiovisual or collection record consent provenance and Māori data-governance authority gate", "exact_gate", ["TMR-MDS-PRINCIPLES"]),
]

OWNER_SKILLS = [
    "ghc-family-av-preservation-carrier-content-id",
    "ghc-family-av-source-custody-vacancy",
    "ghc-family-premis-role-separation",
    "ghc-family-av-track-topology",
    "ghc-family-av-equipment-capability-firewall",
    "ghc-family-av-technical-metadata-types",
    "ghc-family-av-timebase-duration",
    "ghc-family-av-fixity-event",
    "ghc-family-av-derivative-lineage",
    "ghc-family-av-rights-access-vacancy",
    "ghc-family-ipm-location-topology",
    "ghc-family-ipm-observation-identification-firewall",
    "ghc-family-ipm-trap-lifecycle",
    "ghc-family-ipm-environment-vacancy",
    "ghc-family-ipm-threshold-authority-vacancy",
    "ghc-family-ipm-correction-lineage",
    "ghc-family-preservation-privacy-minimization",
    "ghc-family-preservation-accessible-summary",
    "ghc-family-preservation-gmut-analogy-firewall",
    "ghc-family-preservation-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_liora_v678_v3_carrier_identity_guard.py",
    "ghc_family_liora_v678_v3_custody_event_guard.py",
    "ghc_family_liora_v678_v3_track_topology_guard.py",
    "ghc_family_liora_v678_v3_fixity_lineage_guard.py",
    "ghc_family_liora_v678_v3_rights_vacancy_guard.py",
    "ghc_family_liora_v678_v3_ipm_location_guard.py",
    "ghc_family_liora_v678_v3_ipm_observation_guard.py",
    "ghc_family_liora_v678_v3_ipm_authority_guard.py",
    "ghc_family_liora_v678_v3_privacy_access_guard.py",
    "ghc_family_liora_v678_v3_stage20_guard.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-preservation-event-manifest-subject-binding",
    "ghc-family-preservation-event-manifest-custody-lineage",
    "ghc-family-preservation-event-manifest-fixity-domain",
    "ghc-family-preservation-event-manifest-observation-vacancy",
    "ghc-family-preservation-event-manifest-rights-layer",
    "ghc-family-preservation-event-manifest-accessibility-reservation",
    "ghc-family-preservation-event-manifest-privacy-minimization",
    "ghc-family-preservation-event-manifest-correction-dag",
    "ghc-family-preservation-event-manifest-authority-vacancy",
    "ghc-family-preservation-event-manifest-stage20-veto",
]

SUCCESSOR_RUNNERS = [
    name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner.py"
    for name in SUCCESSOR_SKILLS
]

STARTUP_FAILURES = [
    (
        "LV6783-START-N001",
        "the live activation named x1 semantic-neighbor-audit.json but the immutable exact tree stores x1 proposal-chain-audit.json",
        "inspect the exact final tree, read proposal-chain-audit.json through EOF, and preserve the stale filename as zero-credit activation drift",
    ),
    (
        "LV6783-START-N002",
        "the first PowerShell guidance inventory piped a foreach block directly and failed parser validation before mutation",
        "materialize the bounded inventory before piping and read every selected guidance file through EOF",
    ),
    (
        "LV6783-START-N003",
        "the first inherited proposal projection guessed a proposals array that does not exist in the exact source object",
        "inspect exact JSON keys, use the rows array, and retain the false schema assumption",
    ),
    (
        "LV6783-START-N004",
        "the worktree-creation composite reached its bounded display deadline before emitting the final state projection",
        "inspect persisted branch worktree and Git state before any retry and continue only after exact source and clean state are proven",
    ),
    (
        "LV6783-START-N005",
        "the first persisted-state projection embedded a PowerShell if expression directly inside a hashtable value and failed expression parsing",
        "compute the scalar before constructing the hashtable and preserve the parser fault at zero credit",
    ),
    (
        "LV6783-START-N006",
        "the no-checkout sparse worktree retained an empty index and initially displayed 20274 staged deletions with no selected materialization",
        "retain the zero-commit state and populate only selected sparse paths from immutable HEAD with sparse-aware git read-tree -mu",
    ),
    (
        "LV6783-START-N007",
        "a read-only Git status and head projection bound a worktree variable but ran Git from the parent Codex directory, returning not-a-repository errors",
        "run the same bounded projection with the exact worktree as process working directory and preserve the cwd fault",
    ),
    (
        "LV6783-X1-N001",
        "the first x1 semantic-neighbour test quarantined IPM correction contest readback and immutable prior-state link at 0.8 token Jaccard similarity to a frozen predecessor",
        "retain the first title at zero credit and remaster only that proposal as integrated-pest-management revision lineage with superseded-record visibility",
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
        "schema": "ghc.family.bounded-semantic-novelty-audit.v678.v3",
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
        SOURCE, "docs/orin-thale/v678-v2/x1/new-proposal-freeze.json"
    )
    rows = source.get("rows", source.get("proposals", []))
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 source proposal rows, found {len(rows)}")
    return [
        {
            "selection_id": f"LV6783-I{index:03d}",
            "source_phase": "v678-v2",
            "source_proposal_id": row.get("proposal_id"),
            "title": row["title"],
            "disposition": "reviewed_for_continuity_zero_liora_credit",
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
                "proposal_id": f"LV6783-N{index:03d}",
                "pillar": pillar,
                "title": title,
                "practice_lenses": [
                    "wholly_synthetic_audiovisual_preservation_reformatting_custody_registrar",
                    "wholly_synthetic_museum_integrated_pest_management_observation_handover_reviewer",
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
                    f"proposal-contracts/LV6783-N{index:03d}.json",
                    "positive-controls.json",
                    "retained-invalid-mutations.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The declared positive fixture must pass and the assigned preregistered invalid "
                    "fixtures must fail closed; represented, gap, and gate outcomes remain bounded "
                    "to their named missing evidence or authority."
                ),
                "rollback_or_recovery": (
                    "Stop, retain the failure at zero credit, quarantine only uncommitted Liora-created "
                    "material, repair the smallest dependency, and return to the immutable x1 anchor."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "liora_frozen_without_universal_novelty_claim",
            }
        )
    return rows


def safe_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    actions = ("acceptance_contract", "retained_rejection_contract")
    return [
        {
            "packet_id": f"LV6783-S{index:03d}",
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
            "packet_id": f"LV6783-E{index:03d}",
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
            "packet_id": f"LV6783-B{index:03d}",
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
        "schema": "ghc.family.official-primary-source-ledger.v678.v3.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at_utc": RECORDED_UTC,
        "entries": [
            {
                "source_id": "LOC-RFS-2025-2026",
                "title": "Library of Congress Recommended Formats Statement 2025-2026",
                "url": "https://www.loc.gov/preservation/resources/rfs/",
                "status": "official_current_statement_checked_2026-08-31",
                "version": "2025-2026",
                "use": "audiovisual format-category, preservation-master, metadata, and preference vocabulary only",
            },
            {
                "source_id": "LOC-PREMIS-3.0",
                "title": "PREMIS Data Dictionary for Preservation Metadata 3.0",
                "url": "https://www.loc.gov/standards/premis/v3/index.html",
                "status": "official_stable_standard_checked_2026-08-31",
                "version": "3.0",
                "use": "object, event, agent, rights, relationship, fixity, and preservation-lineage vocabulary only",
            },
            {
                "source_id": "LOC-SUSTAINABILITY-FORMATS",
                "title": "Library of Congress Sustainability of Digital Formats",
                "url": "https://www.loc.gov/preservation/digital/formats/",
                "status": "official_format-description_resource_checked_2026-08-31",
                "use": "container, codec, wrapper, track, channel, timebase, and disclosure-factor vocabulary only",
            },
            {
                "source_id": "NPS-MUSEUM-HANDBOOK-I",
                "title": "National Park Service Museum Handbook Part I: Museum Collections",
                "url": "https://www.nps.gov/subjects/museums/mh1.htm",
                "status": "official_current_handbook_page_checked_2026-08-31",
                "use": "museum environment, location, monitoring, collection-care, and specialist-referral vocabulary only",
            },
            {
                "source_id": "NPS-MH1-CH5",
                "title": "National Park Service Museum Handbook Part I Chapter 5 Biological Infestations",
                "url": "https://www.nps.gov/museum/publications/mhi/CHAP5.pdf",
                "status": "official_handbook_chapter_checked_2026-08-31",
                "use": "integrated pest management, trap, observation, evidence, exclusion, monitoring, and treatment-vacancy vocabulary only",
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
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
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
                "source_id": "W3C-VC-DATA-MODEL-2.0",
                "title": "Verifiable Credentials Data Model 2.0",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "status": "w3c_recommendation_checked_2026-08-31",
                "version": "2.0",
                "use": "identifier minimization, selective disclosure, status, verification and trust-vacancy vocabulary only",
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
        "real_objects_or_observations": 0,
        "network_data_queries": 0,
        "endorsement_claimed": False,
        "authority_conferred": False,
    }

def overview() -> str:
    return """# Liora Venn v678-v3 planning-only x1 overview

## Relational identity and corrigibility

Liora Venn is relational working language for a traceability-and-vacancy cartographer. Optional she or they pronouns remain relational only. The working hope is that every unmeasured state and every ungranted authority remain visible through correction and handover. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, professional standing, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Immutable source and planning-only lifecycle

This x1 freezes source anchors, sixty proposal contracts, portfolios, official-source status, Method Flow startup truth, privacy boundaries, owner-local skill and runner plans, a zero-credit successor seed remaster, and a terminal route hold. It contains no x2 implementation, observed x2 outcome, completion claim, global installation, task lookup, task message, or delivery claim. Orin Thale v678-v2 is preserved at exact final 2c1b2fb714f8b7296a3399ebf3e8802ff5181a58 with the verified three-commit direct single-parent zero-merge lifecycle, 231 replayed normalized-LF manifest entries, clean zero divergence, fresh four-way equality, and its one non-replayed dependency-corrected canonical receipt. Inherited evidence earns zero Liora completion, canonical, novelty, or independent-reproduction credit.

The Liora lane is additive, D-first, sparse, and rooted at Orin's immutable exact final. Seven startup failures and one x1 semantic-neighbour failure remain zero-credit witnesses with separately named bounded recoveries. No source, sibling, shared, standby, global, or user lane is mutated.

## Trinity Mandala and bounded practice lenses

Freed ID and CBR Heart is the primary pillar through two wholly synthetic learning and design lenses: audiovisual preservation reformatting custody registrar, and museum integrated-pest-management observation handover reviewer. THOS Body remains visible through carrier, track, trap, location, timing, workload, and handover structures. GMUT Mind remains visible through typed state partitions, digest domains, observation vacancies, and analogy nonconversion firewalls.

The phase uses no real person, participant, operator, carrier, recording, file, playback device, collection object, pest, trap, lure, photograph, sensor, observation, measurement, treatment, identity event, key, proof, cultural record, Māori data, production system, external write, or authority act. It establishes no authenticity, condition, species identification, safety, treatment, release, competence, conformance, legal, cultural, affected-party, or Māori-authority result.

## Current official-source boundary

The source ledger records the Library of Congress Recommended Formats Statement, PREMIS 3.0 and format sustainability resources; National Park Service Museum Handbook Part I and its biological-infestations chapter; PROV-O; RFC 8785; JSON Schema 2020-12; WCAG 2.2; Verifiable Credentials 2.0; and Te Mana Raraunga principles. They supply vocabulary and refusal conditions only. Citations are not observations, measurements, inspections, preservation decisions, treatment instructions, rights clearances, conformance certificates, accessibility evaluations, endorsements, consent, legal interpretation, cultural ratification, or authority. Zero real source rows, objects, files, or observations are queried or downloaded.

## Proposal and portfolio freeze

Sixty Orin proposals are reviewed at zero Liora novelty and completion credit. Sixty new Liora proposals are frozen separately, extending the declared chain from 8,390 to 8,450 only if x2 evidence is later sealed. The exact-source semantic audit reads every reachable frozen proposal ledger in one length-framed Git batch, rejects exact and internal title collisions, reports nearest normalized-token neighbours, and explicitly refuses a universal novelty claim where the declared chain exceeds reachable title maps.

The expected partition is 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. These are planning expectations, not observed outcomes. Completed may later mean only that a bounded owner-local synthetic contract passed. Represented preserves absent real tools, operators, affected users, review, or authority. Open_gap names missing evidence. Exact_gate names decisions repository software cannot make. No fifth core outcome label is permitted.

X1 freezes 120 safe-now packets, 80 owner candidates, 20 zero-credit successor candidates, 20 exact holds, 10 blocked holds, 20 owner-local skill plans, 10 family-current runner plans, 10 successor skill and 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE plans, and 30 successor recommendations. The inherited wholly_synthetic_artifact_manifest_build_provenance_reviewer seed is accepted only as zero-credit input, rejected as Liora completion credit, and independently remastered into wholly_synthetic_preservation_event_manifest_custody_handover_reviewer as exactly one zero-credit recommendation for Tamar's later independent review. Caps are ceilings and never quotas.

## Skills, failures, privacy, and validation

The phase-local skill plan follows the installed skill-creator contract, including substantive SKILL.md content, quoted openai.yaml strings, discriminating short descriptions, and a default prompt that names the skill. Skills remain owner-local and require complete readback, UTF-8 quick validation, and accepting and rejecting smoke use. Ten family-current ghc_family_liora_v678_v3_* runners preserve historical caller compatibility. No plugin cache or global skill is mutated.

Orin's immutable seal remains separate from its four live activation-overlay failures. Liora's seven startup failures and first x1 semantic-neighbour failure remain separate from their recoveries. Public artifacts exclude raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, secrets, private callable identifiers, private app state, and private absolute paths. Exact staged review uses Git-index blobs; manifests hash normalized-LF bytes; scanner-definition candidates remain distinct from confirmed hits. Bounded AST checks are not exhaustive security.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, synthetic fixtures, typed ledgers, digests, observation vacancies, analogies, and citations establish no physical datum, likelihood, posterior, force, prediction, constraint, empirical confirmation, quantum or ultraviolet completion, or Theory of Everything. THOS remains synthetic proxy evidence without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live lifecycle, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

CBR, audiovisual rights, authenticity, collection custody, pest identification, treatment, hazard or public-safety decisions, privacy remedy, accessibility remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## X1 gate and terminal hold

X1 must pass bounded owner tests and exact staged review, become the direct child of Orin's exact final, be pushed cleanly, and prove local, upstream, tracking, and fresh-live equality before any x2 implementation or observed outcome exists. The phase ceiling is three commits: planning-only x1, immutable x2 evidence, and final closeout. No successor is contacted before Liora's terminal gate. Repository route state remains PREPARED_NOT_SENT.
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
    owner_candidates = candidate_rows(proposals, 80, "LV6783-C", False)
    successor_candidates = candidate_rows(proposals, 20, "LV6783-SC", True)
    owner_cleanup = cleanup_rows(100, "LV6783-R", True)
    successor_cleanup = cleanup_rows(30, "LV6783-SR", False)

    activation_baseline = {
        "effective_negatives": 46298,
        "methods": 43506,
        "failed_witnesses": 17959,
        "bounded_passing_witnesses": 27632,
        "open_gaps": 398,
        "exact_gates": 389,
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
            "schema": "ghc.family.activation-intake.v678.v3",
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
            "source_packet_words": 2798,
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
            "schema": "ghc.family.identity-boundary.v678.v3",
            "owner": OWNER,
            "relational_role": "traceability-and-vacancy cartographer",
            "hope": "keep every unmeasured state and every ungranted authority visible through correction and handover",
            "pronouns": "optional she/they relational language",
            "identity_evidence": False,
            "authority_evidence": False,
            "continuity_evidence": False,
            "corrigible": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "protected_gates": PROTECTED_GATES,
        },
        X1_ROOT / "source-verification.json": {
            "schema": "ghc.family.source-verification.v678.v3",
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
            "canonical_state": "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "canonical_invocations": 1,
            "canonical_successes": 1,
            "canonical_replayed": False,
            "inherited_validation_credit": 0,
        },
        X1_ROOT / "official-primary-source-ledger.json": source_ledger(),
        X1_ROOT / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation-freeze.v678.v3",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
        X1_ROOT / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v678.v3",
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
        X1_ROOT / "successor-seed-remaster.json": {
            "schema": "ghc.family.successor-seed-remaster.v678.v3.x1",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_seed": "wholly_synthetic_artifact_manifest_build_provenance_reviewer",
            "accepted_as_zero_credit_input": True,
            "rejected_as_liora_completion_or_novelty_credit": True,
            "independently_remastered_recommendation": "wholly_synthetic_preservation_event_manifest_custody_handover_reviewer",
            "recommendation_count": 1,
            "intended_successor": "Tamar Vey",
            "successor_must_independently_accept_reject_or_remaster": True,
            "x1_state": "planning_only_zero_credit_recommendation",
            "completion_credit": 0,
        },
        X1_ROOT / "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v678.v3",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "represented_pillars": [
                "GMUT Mind",
                "THOS Body",
                "Freed ID and CBR Heart",
            ],
            "owner_practice_lenses": [
                "wholly_synthetic_audiovisual_preservation_reformatting_custody_registrar",
                "wholly_synthetic_museum_integrated_pest_management_observation_handover_reviewer",
            ],
            "successor_practice_recommendation": "wholly_synthetic_preservation_event_manifest_custody_handover_reviewer",
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
            "schema": "ghc.family.skill-runner-plan.v678.v3",
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
            "schema": "ghc.family.clean-fix-refine-plan.v678.v3",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(owner_cleanup),
            "owner_tasks": owner_cleanup,
            "successor_count": len(successor_cleanup),
            "successor_recommendations": successor_cleanup,
            "destructive_cleanup_authorized": False,
        },
        X1_ROOT / "approval-hold-register.json": {
            "schema": "ghc.family.approval-hold-register.v678.v3",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "execution_credit": 0,
        },
        X1_ROOT / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow-startup.v678.v3",
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
            "schema": "ghc.family.workflow-plan.v678.v3",
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
                    "name": "create clean sparse Liora lane",
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
            "schema": "ghc.family.threat-model.v678.v3.x1",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                "real carrier collection object observation or rights-record leakage",
                "private route leakage",
                "x1 and x2 mixing",
                "outcome promotion",
                "authority fabrication",
                "network side effect",
                "manifest drift",
                "failed-witness erasure",
                "successful canonical replay",
                "sibling-lane mutation",
                "carrier content identity observation and authority conflation",
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
                "identity observation rights and evidence-type guards",
                "source-status ledger",
            ],
            "residual_risk": "Structural controls are bounded software evidence, not exhaustive security, complete privacy, complete accessibility, professional review, or independent reproduction.",
        },
        X1_ROOT / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v678.v3.x1",
            "owner": OWNER,
            "workload_bounded": True,
            "pause_available": True,
            "corrigible": True,
            "identity_relational_only": True,
            "hamish_may_rename_pause_narrow_redirect_or_stop": True,
            "no_completion_pressure_can_override_evidence_or_authority": True,
        },
        X1_ROOT / "route-plan.json": {
            "schema": "ghc.family.route-plan.v678.v3.x1",
            "previous_owner": "Orin Thale",
            "previous_phase": "v678-v2",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "next_owner": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "next_phase": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "state": "HOLD_BEFORE_LIORA_TERMINAL_GATE",
            "precontact": False,
            "send_attempts": 0,
            "task_created": False,
            "duplicate_guard_required": True,
            "terminal_planning_label": "v725-v8",
        },
        X1_ROOT / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v678.v3.x1",
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
    review_rel = "docs/liora-venn/v678-v3/validation/x1-staged-review.json"
    privacy_rel = "docs/liora-venn/v678-v3/validation/x1-privacy-scan.json"
    manifest_rel = "docs/liora-venn/v678-v3/validation/x1-index-manifest.json"
    exclusions = [review_rel, privacy_rel, manifest_rel]
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
    ).splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_liora_venn_v678_v3_x1.py",
        "tests/test_ghc_family_liora_venn_v678_v3_x1.py",
    }
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/liora-venn/v678-v3/x1/")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope x1 paths: {out_of_scope}")
    if any(path.startswith("docs/liora-venn/v678-v3/x2/") for path in staged):
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
                    path == "scripts/build_ghc_family_liora_venn_v678_v3_x1.py"
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
        "schema": "ghc.family.privacy-scan.v678.v3.x1",
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
        "schema": "ghc.family.exact-staged-review.v678.v3.x1",
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
        "schema": "ghc.family.normalized-lf-index-manifest.v678.v3.x1",
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
        raise SystemExit("usage: build_ghc_family_liora_venn_v678_v3_x1.py [--staged-review]")
