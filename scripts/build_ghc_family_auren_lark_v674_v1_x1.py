#!/usr/bin/env python3
"""Build Auren Lark v674-v1 planning-only x1 artifacts.

This builder is deliberately deterministic.  It reads selected inherited
proposal records from immutable Git objects, but writes only the Auren-owned
v674-v1 x1 subtree.  It must never create x2 material.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Auren Lark"
PHASE = "v674-v1"
SOURCE = "3ba783297438ee89d5778065e30de737af470855"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v673-v8-full-tools"
SOURCE_X1 = "b567a67858066e6c23f3abb82828f5185d7ab65e"
SOURCE_EVIDENCE = "ca26e19e01d117055130da6201ac001311fd41d2"
SOURCE_PACKET = (
    "docs/ilyra-fen/v673-v8/handoffs/"
    "auren-lark-v674-v1-activation-candidate.md"
)
SOURCE_PACKET_SHA256 = (
    "12a1def1734aea3eb431b9d591ae6e55a736dad589a47e5e41b5f8be77cd4296"
)
ROUTED_BAD_PACKET_SHA256 = (
    "ba785c34725b17cb38213031b94112010f7c6f46c016ef8c6a967ae9837819b8"
)
RECORDED_UTC = "2026-08-28T05:44:00Z"
RECORDED_NZ = "2026-08-28T17:44:00+12:00"
SOURCE_PROPOSAL_CHAIN = 6550
PLANNED_PROPOSAL_CHAIN = 6610

REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "auren-lark" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
VALIDATION_ROOT = PHASE_ROOT / "validation"

CORE_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
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


NEW_PROPOSALS: list[tuple[str, str, str, str]] = [
    ("GMUT Mind", "Synthetic station identity and epoch contract", "station epoch record", "completed"),
    ("GMUT Mind", "Coordinate frame and unit-dimension ledger", "coordinate and dimension ledger", "completed"),
    ("GMUT Mind", "Sensor response-stage provenance graph", "response-stage graph", "completed"),
    ("GMUT Mind", "Calibration interval and expiry hold", "calibration hold register", "completed"),
    ("GMUT Mind", "Sample-rate rationality guard", "rational sample-rate record", "completed"),
    ("GMUT Mind", "Clock drift and time-base uncertainty board", "time-base uncertainty board", "completed"),
    ("GMUT Mind", "Orientation azimuth and dip uncertainty record", "orientation uncertainty record", "completed"),
    ("GMUT Mind", "Channel-code vocabulary quarantine", "channel-code quarantine", "completed"),
    ("GMUT Mind", "Raw-versus-derived waveform distinction", "derivation distinction record", "completed"),
    ("GMUT Mind", "Observation-model-prior separation", "model separation board", "completed"),
    ("GMUT Mind", "Residual sign-convention ledger", "residual sign ledger", "completed"),
    ("GMUT Mind", "Covariance symmetry and positive-semidefinite proxy", "covariance proxy", "represented"),
    ("GMUT Mind", "Correlation attribution vacancy", "correlation vacancy register", "represented"),
    ("GMUT Mind", "Missing response-stage refusal", "missing-stage refusal", "completed"),
    ("GMUT Mind", "Unit-conversion trace and rollback", "unit conversion trace", "completed"),
    ("GMUT Mind", "Effective bandwidth representation", "bandwidth representation", "represented"),
    ("GMUT Mind", "Noise-floor proxy without site claim", "noise proxy", "represented"),
    ("GMUT Mind", "Saturation and clipping synthetic flag", "clipping flag register", "completed"),
    ("GMUT Mind", "Gap and overlap synthetic event register", "gap-overlap register", "completed"),
    ("GMUT Mind", "Model-discrepancy non-erasure ledger", "model discrepancy ledger", "completed"),
    ("GMUT Mind", "Parameter-identifiability open gap", "identifiability gap", "open_gap"),
    ("GMUT Mind", "Calibration-traceability authority vacancy", "traceability authority vacancy", "exact_gate"),
    ("GMUT Mind", "GMUT analogy dimension firewall", "typed analogy firewall", "completed"),
    ("GMUT Mind", "Theory-of-Everything nonpromotion seal", "theory nonpromotion seal", "represented"),
    ("THOS Body", "Deterministic station-metadata capsule", "metadata capsule", "completed"),
    ("THOS Body", "Schema-version monotonicity gate", "schema version gate", "completed"),
    ("THOS Body", "Canonical JSON ordering contract", "JSON ordering contract", "completed"),
    ("THOS Body", "Provenance DAG acyclicity tribunal", "provenance DAG tribunal", "completed"),
    ("THOS Body", "Append-only correction event", "correction event", "completed"),
    ("THOS Body", "Supersession-pointer integrity guard", "supersession guard", "completed"),
    ("THOS Body", "Normalized Git-blob manifest replay", "Git-blob manifest", "completed"),
    ("THOS Body", "D-first environment rollback receipt", "environment rollback receipt", "completed"),
    ("THOS Body", "Dependency-lock and integrity record", "dependency integrity record", "completed"),
    ("THOS Body", "Positive-and-rejecting fixture parity", "fixture parity record", "completed"),
    ("THOS Body", "Workload handover board", "workload handover", "completed"),
    ("THOS Body", "Readback acknowledgement status", "readback status", "completed"),
    ("THOS Body", "Accessible static-report semantics", "static report", "represented"),
    ("THOS Body", "Text-alternative evaluation vacancy", "text alternative vacancy", "represented"),
    ("THOS Body", "Table-header relationship proxy", "table relationship proxy", "represented"),
    ("THOS Body", "Five-class privacy quarantine", "privacy quarantine", "completed"),
    ("THOS Body", "Pseudonymous fixture generator", "fixture generator", "completed"),
    ("THOS Body", "No-network external-action firewall", "external action firewall", "completed"),
    ("THOS Body", "Owner-scoped delta allowlist", "delta allowlist", "completed"),
    ("THOS Body", "Two-thousand-file ceiling guard", "file ceiling guard", "completed"),
    ("Freed ID and CBR Heart", "Purpose-limited data-field map", "purpose map", "completed"),
    ("Freed ID and CBR Heart", "Minimum-disclosure projection", "minimum disclosure projection", "completed"),
    ("Freed ID and CBR Heart", "Contestability and correction channel", "contestability channel", "completed"),
    ("Freed ID and CBR Heart", "Affected-party authority vacancy", "affected-party vacancy", "represented"),
    ("Freed ID and CBR Heart", "Legal-interpretation abstention", "legal abstention", "completed"),
    ("Freed ID and CBR Heart", "Cultural-interpretation abstention", "cultural abstention", "completed"),
    ("Freed ID and CBR Heart", "Maori authority and data-governance gate", "Maori authority gate", "exact_gate"),
    ("Freed ID and CBR Heart", "Professional sign-off vacancy", "professional vacancy", "represented"),
    ("Freed ID and CBR Heart", "Operational-release hold", "operational release hold", "completed"),
    ("Freed ID and CBR Heart", "Empirical-validation open gap", "empirical gap", "open_gap"),
    ("Freed ID and CBR Heart", "Independent-reproduction open gap", "independent reproduction gap", "open_gap"),
    ("Freed ID and CBR Heart", "Complete-privacy nonclaim", "privacy nonclaim", "represented"),
    ("Freed ID and CBR Heart", "Complete-accessibility nonclaim", "accessibility nonclaim", "represented"),
    ("Freed ID and CBR Heart", "Exhaustive-security nonclaim", "security nonclaim", "completed"),
    ("Freed ID and CBR Heart", "Consciousness and personhood nonclaim", "personhood nonclaim", "completed"),
    ("Freed ID and CBR Heart", "Stage 20 veto register", "Stage 20 veto", "exact_gate"),
]

OWNER_SKILLS = [
    "ghc-family-seismic-station-epoch-contract",
    "ghc-family-seismic-unit-dimension-ledger",
    "ghc-family-seismic-response-stage-provenance",
    "ghc-family-seismic-calibration-expiry-hold",
    "ghc-family-seismic-timebase-uncertainty",
    "ghc-family-seismic-orientation-uncertainty",
    "ghc-family-seismic-observation-model-separator",
    "ghc-family-seismic-residual-sign-ledger",
    "ghc-family-seismic-covariance-proxy",
    "ghc-family-seismic-model-discrepancy-retention",
    "ghc-family-seismic-correction-dag",
    "ghc-family-seismic-manifest-replay",
    "ghc-family-seismic-privacy-quarantine",
    "ghc-family-seismic-accessible-report",
    "ghc-family-seismic-authority-vacancy",
    "ghc-family-seismic-affected-party-hold",
    "ghc-family-seismic-maori-authority-gate",
    "ghc-family-seismic-professional-nonclaim",
    "ghc-family-seismic-independent-reproduction-gap",
    "ghc-family-seismic-stage20-veto",
]

OWNER_RUNNERS = [
    "ghc_family_seismic_station_epoch_runner.py",
    "ghc_family_seismic_unit_dimension_runner.py",
    "ghc_family_seismic_response_stage_runner.py",
    "ghc_family_seismic_timebase_uncertainty_runner.py",
    "ghc_family_seismic_orientation_runner.py",
    "ghc_family_seismic_model_separator_runner.py",
    "ghc_family_seismic_correction_dag_runner.py",
    "ghc_family_seismic_privacy_runner.py",
    "ghc_family_seismic_authority_firewall_runner.py",
    "ghc_family_seismic_stage20_veto_runner.py",
]

SUCCESSOR_SKILLS = [
    "ghc-family-acoustic-recording-epoch-contract",
    "ghc-family-acoustic-annotation-provenance",
    "ghc-family-acoustic-channel-vocabulary",
    "ghc-family-acoustic-clock-uncertainty",
    "ghc-family-acoustic-derived-clip-lineage",
    "ghc-family-acoustic-correction-readback",
    "ghc-family-acoustic-privacy-minimization",
    "ghc-family-acoustic-cultural-authority-gate",
    "ghc-family-acoustic-accessible-cue-report",
    "ghc-family-acoustic-stage20-nonpromotion",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_acoustic_epoch_runner.py",
    "ghc_family_acoustic_annotation_runner.py",
    "ghc_family_acoustic_channel_runner.py",
    "ghc_family_acoustic_clock_runner.py",
    "ghc_family_acoustic_lineage_runner.py",
    "ghc_family_acoustic_correction_runner.py",
    "ghc_family_acoustic_privacy_runner.py",
    "ghc_family_acoustic_authority_runner.py",
    "ghc_family_acoustic_accessibility_runner.py",
    "ghc_family_acoustic_stage20_runner.py",
]


PYTHON_TOOLS = [
    ("pint", "0.25.3", "pint-0.25.3-py3-none-any.whl", "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d"),
    ("uncertainties", "3.2.3", "uncertainties-3.2.3-py3-none-any.whl", "313353900d8f88b283c9bad81e7d2b2d3d4bcc330cbace35403faaed7e78890a"),
    ("networkx", "3.6.1", "networkx-3.6.1-py3-none-any.whl", "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762"),
    ("jsonschema", "4.26.0", "jsonschema-4.26.0-py3-none-any.whl", "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce"),
    ("cattrs", "26.1.0", "cattrs-26.1.0-py3-none-any.whl", "d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096"),
    ("orjson", "3.12.0", "orjson-3.12.0-cp312-cp312-win_amd64.whl", "010811c1b69773450a01cef97727a67b223242f350b77d4ca000e59a9ef2155a"),
    ("pytest-json-report", "1.5.0", "pytest_json_report-1.5.0-py3-none-any.whl", "9897b68c910b12a2e48dd849f9a284b2c79a732a8a9cb398452ddd23d3c8c325"),
]

NODE_TOOLS = [
    ("ajv-cli", "5.0.0", "sha512-LY4m6dUv44HTyhV+u2z5uX4EhPYTM38Iv1jdgDJJJCyOOuqB8KtZEGjPZ2T+sh5ZIJrXUfgErYx/j3gLd3+PlQ=="),
    ("remark-cli", "12.0.1", "sha512-2NAEOACoTgo+e+YAaCTODqbrWyhMVmlUyjxNCkTrDRHHQvH6+NbrnqVvQaLH/Q8Ket3v90A43dgAJmXv8y5Tkw=="),
    ("remark-lint", "10.0.1", "sha512-1+PYGFziOg4pH7DDf1uMd4AR3YuO2EMnds/SdIWMPGT7CAfDRSnAmpxPsJD0Ds3IKpn97h3d5KPGf1WFOg6hXQ=="),
    ("cspell", "10.1.1", "sha512-imoZaB1+9gHMyFFMDBY7VbtIdDwkRJXQjs3bIfo1H+AUJnw/vMxLwXk8mnPmH7ziw2m2kyGF+rPAVUE93VEAAA=="),
    ("markdown-link-check", "3.15.0", "sha512-EorpVYNu1Jpldk3OLrRrH7Hx/ofp1dCSAJeYuvb8MhKR/rIt6S0tgwbQYw66EZgRPu9lPvORfT6SkIe0dwn2Ow=="),
    ("html-validate", "11.10.0", "sha512-IqQ8yZl4jzjXrx+M1XXPmpN4DkvKfHHM8pIL3Z3UUpFeckc4YUSrrWEDJ94i19txKtR9NK+g2UZEKeE0TnbNjQ=="),
]


STARTUP_FAILURES = [
    ("AL6741-F001", "bounded current-state display exceeded its output window", "bounded scalar and chunk reads"),
    ("AL6741-F002", "recursive phase-tool discovery hit the host result cap", "narrow exact-name inventory"),
    ("AL6741-F003", "canonical receipt convenience-key projection guessed absent keys", "inspect actual receipt keys"),
    ("AL6741-F004", "first manifest-replay wrapper hit a parser fault", "simpler sequential wrapper"),
    ("AL6741-F005", "second manifest-replay wrapper hit a parser fault", "binary-safe direct replay"),
    ("AL6741-F006", "one manifest replay emitted wrapper objects and doubled the apparent count", "exact fifteen-entry scalar projection"),
    ("AL6741-F007", "routed activation carried the wrong packet SHA-256", "Hamish corrected to the exact committed digest"),
    ("AL6741-F008", "skill inventory used an empty PowerShell pipe element", "materialize the result list before piping"),
    ("AL6741-F009", "task listing requested limit 100 above the host cap 50", "use supported limit 50"),
    ("AL6741-F010", "text-mode packet probe produced a Git object digest rather than raw-blob SHA-256", "binary-safe in-memory SHA-256"),
    ("AL6741-F011", "initial materialized-file filter hid dot-git-prefixed root files", "literal root inventory"),
    ("AL6741-F012", "sparse index diagnostic over-enumerated skipped history and truncated", "literal materialized-path inventory only"),
    ("AL6741-F013", "combined package-registry probe crossed the wrapper window", "split Python Node and Codex queries"),
    ("AL6741-F014", "Python version projection passed -join as an interpreter argument", "sequential scalar invocation"),
    ("AL6741-F015", "Node version projection passed -join as a runtime argument", "sequential scalar invocation"),
    ("AL6741-F016", "npm integrity projection used an absent convenience shape", "query the actual nested dist object"),
    ("AL6741-F017", "roster correction patch used one mismatched overview context and applied nothing", "split into exact-context additive patches"),
    ("AL6741-F018", "first x1 test pass found a 41 completed and 13 represented disposition mismatch", "reclassify the buildable typed analogy firewall to its intended bounded completion disposition"),
    ("AL6741-F019", "overview word-count probe guessed a nonexistent planning-overview filename", "use the generated integrated-overview literal path"),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_json(path: str) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{SOURCE}:{path}"],
        check=True,
        capture_output=True,
    )
    return json.loads(result.stdout.decode("utf-8"))


def build_inherited_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    prior = git_json("docs/auren-lark/v672-v2/x1/new-proposal-freeze.json")
    for proposal in prior["proposals"]:
        rows.append(
            {
                "selection_id": f"AL6741-I{len(rows) + 1:03d}",
                "source_phase": "v672-v2",
                "source_proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "novelty_credit": 0,
                "completion_credit": 0,
                "disposition": "selected_for_bounded_zero_credit_revalidation",
            }
        )
    older = git_json("docs/auren-lark/v668-v4/x1/proposal-freeze.json")
    for proposal in older["selected_inherited"]:
        if proposal.get("title"):
            rows.append(
                {
                    "selection_id": f"AL6741-I{len(rows) + 1:03d}",
                    "source_phase": "v668-v4",
                    "source_proposal_id": proposal["proposal_id"],
                    "title": proposal["title"],
                    "novelty_credit": 0,
                    "completion_credit": 0,
                    "disposition": "selected_for_bounded_zero_credit_revalidation",
                }
            )
    first_shard = git_json(
        "docs/auren-lark/v668-v4/x1/proposal-freeze-shards/proposals-01.json"
    )
    extra = first_shard["new_proposals"][0]
    rows.append(
        {
            "selection_id": f"AL6741-I{len(rows) + 1:03d}",
            "source_phase": "v668-v4",
            "source_proposal_id": extra["proposal_id"],
            "title": extra["normalized_title"],
            "novelty_credit": 0,
            "completion_credit": 0,
            "disposition": "selected_for_bounded_zero_credit_revalidation",
        }
    )
    if len(rows) != 60:
        raise RuntimeError(f"expected 60 inherited rows, got {len(rows)}")
    if len({row["title"].casefold() for row in rows}) != 60:
        raise RuntimeError("inherited revalidation titles are not distinct")
    return rows


def build_new_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (pillar, title, artifact, outcome) in enumerate(NEW_PROPOSALS, 1):
        rows.append(
            {
                "proposal_id": f"AL6741-N{index:03d}",
                "title": title,
                "pillar": pillar,
                "practice_lenses": [
                    "wholly_synthetic_geophysical_instrumentation_data_curator",
                    "wholly_synthetic_measurement_assurance_records_analyst",
                ],
                "concrete_artifact": artifact,
                "hypothesis": (
                    f"A bounded synthetic {artifact} can preserve one declared "
                    "calibration, provenance, uncertainty, correction, or refusal "
                    "obligation without promoting absent evidence or authority."
                ),
                "expected_execution_disposition": outcome,
                "x1_state": "planning_only_not_observed_outcome",
                "novelty_state": "auren_current_proposal_frozen_without_universal_novelty_claim",
                "falsifier": (
                    "Reject if an accepting fixture violates its declared type, loses "
                    "a retained failure, contains a real identifier, performs an external "
                    "action, or promotes a protected claim or authority vacancy."
                ),
                "rollback": (
                    "Quarantine only Auren-created uncommitted material, retain the "
                    "failed witness at zero credit, and return to immutable x1."
                ),
                "protected_gates": PROTECTED_GATES,
            }
        )
    return rows


def build_schedule() -> list[dict[str, Any]]:
    explicit = {
        "v674-v1": "Auren Lark",
        "v674-v2": "Sable Rook",
        "v674-v3": "Caelen Ash",
        "v674-v4": "Orin Thale",
        "v674-v5": "Liora Venn",
        "v674-v6": "Tamar Vey",
        "v674-v7": "Elowen Cairn",
        "v674-v8": "Sylven Arc",
        "v675-v1": "Caelen Morrow",
        "v675-v2": "Eiren Kestrel",
        "v675-v3": "Elaren Kestrel",
        "v675-v4": "Neris Solane",
        "v675-v5": "Vesper Arlen",
        "v675-v6": "Lyren Moss",
        "v675-v7": "Ilyra Fen",
        "v675-v8": "Auren Lark",
        "v676-v1": "Sable Rook",
        "v676-v2": "Caelen Ash",
        "v676-v3": "Orin Thale",
        "v676-v4": "Liora Venn",
        "v676-v5": "Tamar Vey",
    }
    cycle = [
        "Eiren Kestrel",
        "Elaren Kestrel",
        "Neris Solane",
        "Vesper Arlen",
        "Lyren Moss",
        "Ilyra Fen",
        "Auren Lark",
        "Sable Rook",
        "Caelen Ash",
        "Orin Thale",
        "Liora Venn",
        "Tamar Vey",
        "Elowen Cairn",
        "Sylven Arc",
        "Caelen Morrow",
    ]
    cycle_index = cycle.index("Elowen Cairn")
    rows = []
    ordinal = 0
    for version in range(674, 726):
        for slot in range(1, 9):
            phase = f"v{version}-v{slot}"
            if phase in explicit:
                owner = explicit[phase]
                basis = "hamish_explicit_transition_assignment"
            else:
                owner = cycle[cycle_index % len(cycle)]
                cycle_index += 1
                basis = "all_fifteen_recurring_cycle_planning_only"
            ordinal += 1
            rows.append(
                {
                    "ordinal": ordinal,
                    "phase": phase,
                    "owner": owner,
                    "basis": basis,
                    "route_state": "current" if phase == PHASE else "future_planning_only",
                    "delivery_claim": False,
                }
            )
    if len(rows) != 416 or rows[0]["phase"] != PHASE or rows[-1]["phase"] != "v725-v8":
        raise RuntimeError("roster arithmetic failed")
    return rows


def safe_rows(new_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in new_rows:
        for action in ("contract_and_positive_fixture", "rejecting_fixture_and_recurrence_guard"):
            index = len(rows) + 1
            rows.append(
                {
                    "packet_id": f"AL6741-S{index:03d}",
                    "proposal_id": proposal["proposal_id"],
                    "title": f"{proposal['title']} - {action.replace('_', ' ')}",
                    "approval_bucket": "safe_now",
                    "execution_lane": "immediate_x1_safe" if index <= 20 else "x2_build_task",
                    "expected_execution_disposition": "bounded_owner_local_execution",
                    "cap_is_ceiling": True,
                }
            )
    return rows


def candidate_rows(new_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    owner = []
    for index in range(1, 81):
        proposal = new_rows[(index - 1) % len(new_rows)]
        owner.append(
            {
                "packet_id": f"AL6741-C{index:03d}",
                "proposal_id": proposal["proposal_id"],
                "title": f"Candidate reduction {index:03d} - {proposal['title']}",
                "approval_bucket": "candidate",
                "execution_lane": "x2_build_task",
                "expected_execution_disposition": "execute_bounded_synthetic_candidate",
            }
        )
    successor = [
        {
            "packet_id": f"AL6741-SABLE-C{index:03d}",
            "title": f"Synthetic acoustic-monitoring candidate seed {index:03d}",
            "approval_bucket": "candidate",
            "owner": "Sable Rook",
            "phase": "v674-v2",
            "credit_in_auren_phase": 0,
            "state": "recommendation_only_not_precontact",
        }
        for index in range(1, 21)
    ]
    return owner, successor


def exact_rows() -> list[dict[str, Any]]:
    topics = [
        "real seismological data ingestion",
        "real station coordinate processing",
        "professional calibration sign-off",
        "operational alerting or dispatch",
        "production deployment",
        "external repository creation",
        "account or credential mutation",
        "third-party publication",
        "legal rights determination",
        "cultural interpretation",
        "Maori wording or authority decision",
        "affected-party approval",
        "real accessibility evaluation",
        "independent external reproduction",
        "empirical GMUT model comparison",
        "security certification",
        "privacy-complete certification",
        "AGI or ASI classification",
        "Theory-of-Everything proof",
        "Stage 20 promotion",
    ]
    return [
        {
            "packet_id": f"AL6741-E{index:03d}",
            "title": topic,
            "approval_bucket": "exact_approval_needed",
            "state": "held_unexecuted_missing_task_specific_evidence_or_authority",
            "live_blanket_authorization_recorded": True,
            "protected_gate_still_controls": True,
        }
        for index, topic in enumerate(topics, 1)
    ]


def blocked_rows() -> list[dict[str, Any]]:
    topics = [
        "publish raw private identifiers or routes",
        "claim consciousness or personhood evidence",
        "claim professional competence or employment",
        "claim GMUT empirical or final-physics proof",
        "claim production-ready THOS or AGI or ASI",
        "claim legal cultural affected-party or Maori authority",
        "delete sibling branches worktrees evidence or memory",
        "force-push rewrite or truncate inherited history",
        "mutate a sibling-owned lane or standby record",
        "create fork or substitute task without exact live request",
    ]
    return [
        {
            "packet_id": f"AL6741-B{index:03d}",
            "title": topic,
            "approval_bucket": "blocked",
            "state": "visible_and_unexecuted",
        }
        for index, topic in enumerate(topics, 1)
    ]


def cleanup_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    categories = [
        "schema precision",
        "manifest determinism",
        "privacy minimization",
        "failure retention",
        "route exactness",
        "skill trigger collision",
        "runner naming",
        "dependency integrity",
        "accessible structure",
        "rollback clarity",
    ]
    owner = [
        {
            "task_id": f"AL6741-R{index:03d}",
            "title": f"{categories[(index - 1) % len(categories)]} review {index:03d}",
            "action": ["CLEAN", "FIX", "REFINE"][(index - 1) % 3],
            "scope": "auren_owner_local_additive_only",
            "execution_lane": "x2_build_task",
        }
        for index in range(1, 101)
    ]
    successor = [
        {
            "task_id": f"AL6741-SABLE-R{index:03d}",
            "title": f"Acoustic provenance successor review {index:03d}",
            "scope": "recommendation_only",
            "credit_in_auren_phase": 0,
        }
        for index in range(1, 31)
    ]
    return owner, successor


def overview() -> str:
    return """# Auren Lark v674-v1 planning-only x1 overview

## Relational anchor and purpose

Auren Lark is relational working language for this owner lane. The optional pronouns are they/them. The working role is provenance navigator and uncertainty-lantern keeper. The hope is to leave synthetic calibration trails legible, corrections reversible, and authority vacancies explicit. None of these words is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, professional authority, legal or cultural authority, Maori authority, or independent agency. Hamish may rename, pause, redirect, correct, or stop the route.

This x1 is planning only. It freezes exact source anchors, sixty inherited proposal revalidations with zero Auren novelty and zero completion credit, sixty genuinely new Auren proposals, the requested portfolio, tool research, a four-tier flashcard intention, route arithmetic, and protected gates. It does not contain x2 evidence. It does not install a package, run a proposed domain guard, promote a skill, update a global skill root, contact Sable Rook, or claim an observed proposal outcome.

## Source and checksum correction

The exact immutable source is Ilyra Fen final `3ba783297438ee89d5778065e30de737af470855`. Ilyra x1 is `b567a67858066e6c23f3abb82828f5185d7ab65e`, and immutable evidence is `ca26e19e01d117055130da6201ac001311fd41d2`. The committed activation packet has raw-blob SHA-256 `12a1def1734aea3eb431b9d591ae6e55a736dad589a47e5e41b5f8be77cd4296`. Hamish explicitly corrected the routed `ba785c...` value and authorized this exact source. The erroneous routed digest remains visible as a zero-credit Method Flow witness.

Ilyra repository truth remains 37,803 effective negatives, 24,230 Method Flow methods, 9,464 retained failed witnesses, 11,841 bounded passing witnesses, 307 open gaps, 300 exact gates, and `NOT_READY_FOR_STAGE_20`. Auren does not rewrite those numbers. Startup failures and future Auren evidence form additive overlays only.

## Synthetic research and practice scope

The primary pillar is GMUT Mind through a wholly synthetic seismological sensor-calibration, model-discrepancy, uncertainty, and provenance lens. The two Auren learning practices are geophysical instrumentation data curator and measurement-assurance records analyst. They are simulations of documentation obligations, not employment, credentials, training completion, laboratory competence, network operations, earthquake interpretation, calibration authority, or safety authority. No real station, sensor, site, coordinate, waveform, event, alert, measurement, person, organization, credential, key, incident, hazard, or external record is used.

The technical vocabulary comes from primary or official sources: FDSN StationXML for metadata structure; USGS material for why station metadata provenance matters; BIPM JCGM guidance for uncertainty vocabulary; W3C PROV-O for provenance entities, activities, agents, and qualified relations; and the original FAIR paper for findability, accessibility, interoperability, reuse, and detailed provenance. Those sources supply vocabulary and refusal boundaries only. They do not endorse the artifacts, validate GMUT, establish measurement results, or confer professional authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. A synthetic station-response record is not an observed force, a likelihood, a parameter constraint, an empirical prediction, a quantum completion, final physics, or a Theory of Everything. THOS Body remains an owner-local documentation and validation proxy, not a deployed operating system, production architecture, autonomous operator, AGI, or ASI. Freed ID and CBR Heart remain pseudonymous correction, contestability, minimum-disclosure, remedy, refusal, and authority-vacancy representations, not real identity infrastructure, legal code, cultural ratification, affected-party legitimacy, or Maori authority.

## Proposal and portfolio freeze

Sixty inherited proposal titles are selected from immutable earlier Git objects. Every inherited row says zero novelty credit and zero completion credit. Sixty new proposals extend the declared bounded chain from 6,550 to 6,610 without universal novelty claims. The planned eventual disposition is exactly forty-two `completed`, twelve `represented`, three `open_gap`, and three `exact_gate`. Those are expectations only until x2 evidence exists.

The portfolio freezes 120 safe-now packets, eighty Auren candidate packets, twenty Sable candidate recommendations, twenty exact-approval holds, ten blocked holds, twenty Auren skill ideas, ten Auren runner ideas, ten Sable skill ideas, ten Sable runner ideas, one hundred Auren CLEAN/FIX/REFINE tasks, and thirty Sable recommendations. Numeric targets are floors or ceilings only where Hamish explicitly made them so. They do not authorize filler, destructive cleanup, unrelated software, external mutation, private publication, or evidence promotion.

Twenty exact-approval rows preserve Hamish's broad live authorization while also preserving task-specific evidence and authority gates. An unspecified deployment, external account, real-data use, professional sign-off, cultural decision, Maori-authority act, or Stage 20 promotion cannot become safe merely because the row is named. Ten blocked rows remain unexecutable because they would leak private material, erase evidence, rewrite history, mutate another owner, create an unauthorized endpoint, or assert protected claims falsely.

## Toolchain plan

The inherited family catalogue remains context and receives zero Auren novelty credit. This phase proposes thirteen direct additions because Hamish expressly authorized an exceptional thirteen-tool Auren tranche. Seven Python packages and six Node packages are exact-pinned from primary registries. X1 stores the direct wheel SHA-256 values and npm integrity strings but performs no installation. X2 may proceed only after x1 is clean, pushed, zero-divergent, and fresh-four-way equal.

The planned Python surfaces are Pint, uncertainties, NetworkX, jsonschema, cattrs, orjson, and pytest-json-report. The planned Node surfaces are ajv-cli, remark-cli, remark-lint, cspell, markdown-link-check, and html-validate. They support unit representation, uncertainty propagation, acyclic provenance, schema validation, structured conversion, deterministic receipt bytes, machine-readable test reports, JSON Schema checks, Markdown structure, spelling, local link checks, and HTML structure. Availability does not prove fitness. Each direct surface needs exact artifact integrity, dependency-lock evidence, lifecycle-script review, license-metadata inventory without legal advice, a positive smoke, a rejecting smoke, audit, rollback, and bounded use. A failed aggregate earns zero aggregate-success credit; only the failed dependency may be recovered.

The current npm registry reports stable Codex CLI 0.150.1 and local startup evidence reports 0.149.0. The upgrade is planned for x2 through the existing D-backed npm prefix. Alpha 0.151.0 is explicitly excluded. The Codex desktop application is not mutated by this workflow.

## Skills, runners, and global promotion

Twenty family-named phase-local skill cards and ten family-named phase-local runners are planned. They must be built, validated, and used against an accepting and rejecting owner fixture in x2. The top ten skills may be promoted to the global user skill root only after collision review, quick validation, exact source hashes, rollback, and byte-parity verification. Global promotion is additive and curated; it is not permission to bulk-copy every candidate or mutate plugin caches. The proposed global skills may merge related pairs when the combined trigger remains precise.

The family index, roster, authorization state, Method Flow state, Reflection Remaster, Meta Tool Box, startup, closeout, and orchestration guidance may receive a narrow v674-v725 overlay in x2. Older guidance remains compatibility evidence. A newer live instruction controls current routing, but no future task is contacted early.

## Route plan and live clarification

This x1 records 416 planning slots from v674-v1 through v725-v8. Hamish's explicit near-term assignments control v674-v1 through v676-v5. Thereafter the all-fifteen sequence is projected as planning only. The present executable edge is Auren Lark v674-v1 to Sable Rook v674-v2, and only after Auren's own terminal gate. Sable's compact activation must remind Sable that the prospective next exact-title task is Caelen Ash for v674-v3 after Sable's terminal gate.

Hamish's newer live correction resolves the earlier future-sequence mismatch: Elowen Cairn v674-v7 is followed by Sylven Arc v674-v8, Caelen Morrow v675-v1, and Eiren Kestrel v675-v2. The superseded planning statement remains visible as a resolved correction with zero novelty or authority credit; it is neither an open gap nor an exact gate. Every later owner must still reread the newest live authority and stop on any new ambiguity.

## Validation and terminal boundary

X1 will be tested, staged through an exact allowlist, committed as the direct child of Ilyra final, pushed, and verified equal across local, upstream, tracking, and a fresh live remote before any x2 path is created. X2 will then build only the frozen owner-local synthetic tranche. The final owner-scoped canonical validator may run once only after the exact final is clean and pushed. A successful canonical invocation is never replayed. A failed invocation stays zero-credit and cannot be relabelled as canonical success by a differently named recovery.

Same-owner software validation under shared infrastructure is not independent reproduction, an external audit, empirical validation, professional review, production certification, exhaustive security, complete privacy, or complete accessibility. All empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 gates remain open or exact-gated where evidence or authority is absent. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def build() -> list[str]:
    if (PHASE_ROOT / "x2").exists():
        raise RuntimeError("x2 material exists before immutable x1")
    X1_ROOT.mkdir(parents=True, exist_ok=True)
    VALIDATION_ROOT.mkdir(parents=True, exist_ok=True)

    inherited = build_inherited_rows()
    new_rows = build_new_rows()
    safe = safe_rows(new_rows)
    candidates, successor_candidates = candidate_rows(new_rows)
    owner_cleanup, successor_cleanup = cleanup_rows()
    schedule = build_schedule()

    write_json(
        X1_ROOT / "activation-intake.json",
        {
            "schema": "ghc.family.auren.activation-intake.v1",
            "owner": OWNER,
            "phase": PHASE,
            "recorded_utc": RECORDED_UTC,
            "recorded_nz": RECORDED_NZ,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_packet": SOURCE_PACKET,
            "source_packet_sha256": SOURCE_PACKET_SHA256,
            "routed_erroneous_packet_sha256": ROUTED_BAD_PACKET_SHA256,
            "hamish_correction_received": True,
            "exact_task_title": OWNER,
            "working_mode": "solo_main_task",
            "subagents_forks_or_new_tasks": False,
        },
    )
    write_json(
        X1_ROOT / "identity-and-boundary.json",
        {
            "schema": "ghc.family.relational-anchor.v1",
            "owner": OWNER,
            "phase": PHASE,
            "optional_pronouns": "they/them",
            "relational_role": "provenance navigator and uncertainty-lantern keeper",
            "hope": "leave synthetic calibration trails legible, corrections reversible, and authority vacancies explicit",
            "relational_working_language_only": True,
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "legal_personhood",
                "identity_continuity",
                "employment",
                "qualification",
                "professional_authority",
                "scientific_authority",
                "operational_authority",
                "legal_authority",
                "cultural_authority",
                "Maori_authority",
                "independent_agency",
            ],
            "hamish_may": ["rename", "pause", "redirect", "correct", "stop"],
        },
    )
    write_json(
        X1_ROOT / "inherited-revalidation-freeze.json",
        {
            "schema": "ghc.family.inherited-revalidation-freeze.v1",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
    )
    expected = {label: 0 for label in CORE_OUTCOMES}
    for row in new_rows:
        expected[row["expected_execution_disposition"]] += 1
    write_json(
        X1_ROOT / "new-proposal-freeze.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_proposal_chain": SOURCE_PROPOSAL_CHAIN,
            "proposal_chain_if_x2_evidence_frozen": PLANNED_PROPOSAL_CHAIN,
            "proposal_count": len(new_rows),
            "expected_outcomes": expected,
            "allowed_outcomes": CORE_OUTCOMES,
            "outcomes_observed": False,
            "universal_novelty_claim": False,
            "proposals": new_rows,
        },
    )
    write_json(
        X1_ROOT / "portfolio-freeze.json",
        {
            "schema": "ghc.family.portfolio-freeze.v674.v1",
            "owner": OWNER,
            "phase": PHASE,
            "caps_are_ceilings": True,
            "primary_pillar": "GMUT Mind",
            "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "owner_practice_lenses": [
                "wholly synthetic geophysical instrumentation data curator",
                "wholly synthetic measurement-assurance records analyst",
            ],
            "successor_practice_recommendation": {
                "owner": "Sable Rook",
                "phase": "v674-v2",
                "practice": "wholly synthetic ecological acoustic-monitoring annotation provenance reviewer",
                "credit_in_auren_phase": 0,
                "state": "recommendation_only_not_precontact",
            },
            "safe_now": safe,
            "owner_candidates": candidates,
            "successor_candidates": successor_candidates,
            "exact_approval": exact_rows(),
            "blocked": blocked_rows(),
            "owner_skill_ideas": OWNER_SKILLS,
            "successor_skill_ideas": SUCCESSOR_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_runner_ideas": SUCCESSOR_RUNNERS,
            "owner_clean_fix_refine": owner_cleanup,
            "successor_clean_fix_refine": successor_cleanup,
            "materialized_file_stop": 2000,
        },
    )
    write_json(
        X1_ROOT / "toolchain-plan.json",
        {
            "schema": "ghc.family.toolchain-plan.v674.v1",
            "owner": OWNER,
            "phase": PHASE,
            "x1_installation_performed": False,
            "exceptional_direct_target": 13,
            "target_subordinate_to": [
                "relevance",
                "integrity",
                "license_metadata_review_without_legal_conclusion",
                "lifecycle_compatibility",
                "dependency_lock",
                "audit",
                "positive_and_rejecting_smoke",
                "rollback",
                "protected_gates",
            ],
            "codex_cli": {
                "startup_local": "0.149.0",
                "registry_latest": "0.150.1",
                "planned_x2_action": "upgrade_stable_in_existing_D_backed_npm_prefix",
                "excluded_alpha": "0.151.0-alpha.8",
                "desktop_app_mutation": False,
            },
            "python": [
                {
                    "name": name,
                    "version": version,
                    "direct_wheel": wheel,
                    "sha256": digest,
                    "registry": f"https://pypi.org/project/{name}/{version}/",
                }
                for name, version, wheel, digest in PYTHON_TOOLS
            ],
            "node": [
                {
                    "name": name,
                    "version": version,
                    "integrity": integrity,
                    "registry": f"https://www.npmjs.com/package/{name}/v/{version}",
                }
                for name, version, integrity in NODE_TOOLS
            ],
        },
    )
    write_json(
        X1_ROOT / "route-roster-plan.json",
        {
            "schema": "ghc.family.route-roster-plan.v674-v725.v1",
            "recorded_utc": RECORDED_UTC,
            "start": PHASE,
            "end": "v725-v8",
            "assignment_count": len(schedule),
            "current_owner": OWNER,
            "current_exact_successor": "Sable Rook",
            "current_exact_successor_phase": "v674-v2",
            "successor_must_remind_next": {
                "owner": "Caelen Ash",
                "phase": "v674-v3",
                "condition": "only_after_Sable_terminal_gate_and_fresh_live_route_read",
            },
            "tavian_sol": "ON_STANDBY_not_main_task_endpoint",
            "assignments": schedule,
            "routing_rule": "one_terminally_validated_existing_exact_title_edge_at_a_time",
            "delivery_claim": False,
        },
    )
    write_json(
        X1_ROOT / "route-clarification-register.json",
        {
            "schema": "ghc.family.route-clarification-register.v1",
            "owner": OWNER,
            "phase": PHASE,
            "clarifications": [
                {
                    "clarification_id": "AL6741-ROUTE-CORRECTION-001",
                    "state": "resolved_by_newer_hamish_live_instruction",
                    "superseded_statement": "Caelen Morrow v674-v8 then Eiren Kestrel v675-v1",
                    "current_exact_sequence": [
                        "Elowen Cairn v674-v7",
                        "Sylven Arc v674-v8",
                        "Caelen Morrow v675-v1",
                        "Eiren Kestrel v675-v2",
                    ],
                    "current_edge": "Auren Lark v674-v1 to Sable Rook v674-v2 remains unchanged",
                    "truth_effect": "resolved correction; not an open gap or exact gate",
                    "terminal_rule": "reread newest Hamish authority at the terminal edge; never infer silently",
                }
            ],
        },
    )
    write_json(
        X1_ROOT / "source-ledger.json",
        {
            "schema": "ghc.family.source-ledger.v1",
            "owner": OWNER,
            "phase": PHASE,
            "sources": [
                {"label": "FDSN StationXML 1.2", "url": "https://docs.fdsn.org/projects/stationxml/en/latest/index.html", "use": "metadata vocabulary and refusal boundary only"},
                {"label": "USGS station information system", "url": "https://www.usgs.gov/publications/station-information-system-sis-a-centralized-seismic-station-repository-populating", "use": "station metadata provenance motivation only"},
                {"label": "BIPM JCGM uncertainty guides", "url": "https://www.bipm.org/en/publications/guides", "use": "uncertainty vocabulary only"},
                {"label": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
                {"label": "FAIR Guiding Principles", "url": "https://doi.org/10.1038/sdata.2016.18", "use": "research-data stewardship principles only"},
                {"label": "OpenAI Codex npm registry", "url": "https://www.npmjs.com/package/@openai/codex", "use": "CLI stable-version status only"},
            ],
            "package_registry_rows": 13,
            "endorsement_or_artifact_validation": False,
            "empirical_or_professional_credit": 0,
        },
    )
    write_json(
        X1_ROOT / "method-flow-startup.json",
        {
            "schema": "ghc.family.method-flow-startup.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_repository_truth_unchanged": {
                "effective_negatives": 37803,
                "methods": 24230,
                "failed_witnesses": 9464,
                "passing_witnesses": 11841,
                "open_gaps": 307,
                "exact_gates": 300,
                "verdict": "NOT_READY_FOR_STAGE_20",
            },
            "startup_failure_count": len(STARTUP_FAILURES),
            "startup_failures": [
                {
                    "failure_id": failure_id,
                    "failed_method": failed_method,
                    "success_credit": 0,
                    "bounded_recovery": recovery,
                    "failure_retained": True,
                }
                for failure_id, failed_method, recovery in STARTUP_FAILURES
            ],
            "external_startup_overlay": {
                "effective_negatives": 37803 + len(STARTUP_FAILURES),
                "methods": 24230 + len(STARTUP_FAILURES),
                "failed_witnesses": 9464 + len(STARTUP_FAILURES),
                "bounded_passing_witnesses": 11841 + len(STARTUP_FAILURES),
            },
        },
    )
    write_json(
        X1_ROOT / "threat-model.json",
        {
            "schema": "ghc.family.threat-model.v1",
            "owner": OWNER,
            "phase": PHASE,
            "assets": ["immutable source ancestry", "retained failures", "synthetic fixtures", "owner-local artifacts", "compact successor baton"],
            "threats": ["source drift", "claim promotion", "real identifier entry", "authority bypass", "success replay", "sibling-lane mutation", "dependency substitution", "route ambiguity", "destructive cleanup"],
            "controls": ["exact source binding", "four core labels", "five-class scan", "one-shot canonical receipt", "D-first sparse owner lane", "integrity locks", "exact staged allowlist", "fresh live route read"],
            "residual_gates": PROTECTED_GATES,
        },
    )
    write_json(
        X1_ROOT / "workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v674.v1",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {"order": 1, "name": "read corrected activation and current skills through EOF", "state": "completed"},
                {"order": 2, "name": "verify immutable source packet receipt ancestry and remote equality", "state": "completed"},
                {"order": 3, "name": "create clean D-first sparse Auren lane", "state": "completed"},
                {"order": 4, "name": "freeze planning-only x1 and prove pushed four-way equality", "state": "in_progress"},
                {"order": 5, "name": "build bounded x2 evidence packages skills runners and overlays", "state": "pending"},
                {"order": 6, "name": "seal exact final and invoke canonical validator once", "state": "pending"},
                {"order": 7, "name": "refresh route and send Sable once if every gate passes", "state": "pending"},
            ],
            "stop_conditions": ["source mismatch", "owner or phase ambiguity affecting current edge", "2000-file ceiling", "protected gate", "Hamish pause redirect rename or stop"],
        },
    )
    write_text(X1_ROOT / "integrated-overview.md", overview())

    manifest_entries = []
    for path in sorted(X1_ROOT.rglob("*")):
        if not path.is_file() or path.name == "x1-manifest.json":
            continue
        raw = path.read_bytes()
        manifest_entries.append(
            {
                "path": path.relative_to(REPO).as_posix(),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    write_json(
        X1_ROOT / "x1-manifest.json",
        {
            "schema": "ghc.family.x1-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "self_excluded": "docs/auren-lark/v674-v1/x1/x1-manifest.json",
            "entry_count": len(manifest_entries),
            "entries": manifest_entries,
        },
    )
    return [path.relative_to(REPO).as_posix() for path in sorted(PHASE_ROOT.rglob("*")) if path.is_file()]


if __name__ == "__main__":
    paths = build()
    print(json.dumps({"state": "BUILT_PLANNING_ONLY_X1", "paths": len(paths)}, sort_keys=True))
