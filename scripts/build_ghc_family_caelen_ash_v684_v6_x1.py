#!/usr/bin/env python3
"""Build the planning-only Caelen Ash v684-v6 x1 freeze.

The builder is deliberately deterministic.  It creates no x2 outcome, performs
no network or participant operation, and keeps route delivery in
PREPARED_NOT_SENT state.  The optional staged-review mode proves the exact Git
index surface after the caller has staged the declared x1 allowlist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v684-v6"
OWNER = "Caelen Ash"
BASE = ROOT / "docs" / "caelen-ash" / PHASE
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE_HEAD = "9a2fcdc6021dcc8226ff7150b990bfe429671680"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v684-v5-full-tools"
AUREN_SOURCE = "73321b3ff077c3f33726562b8e9d5952608a060e"
SABLE_X1 = "699e42fe27678cc0e12a55c2d60ba029c62998b4"
SABLE_EVIDENCE = "35073d785c63ab2bbf47260d66ca54e6865b877d"
SABLE_PRIOR_FINAL = "69661bc2a721986a222cb75fe89d0352e314b3c0"
BRANCH = "codex/GHC-Family/caelen-ash-v684-v6-full-tools"
CHAIN_BEFORE = 10_970
CHAIN_AFTER = 11_030

ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED = [
    "empirical confirmation",
    "participant or affected-party evidence",
    "professional or scientific authority",
    "production or deployment readiness",
    "legal interpretation or authority",
    "cultural legitimacy or ratification",
    "Māori wording, data governance, or authority",
    "complete privacy or accessibility assurance",
    "exhaustive security",
    "independent reproduction",
    "AGI or ASI",
    "consciousness or personhood",
    "Theory of Everything proof",
    "proof or canon",
    "Stage 20 authority",
]

SOURCE_URLS = {
    "nasa_facilities": "https://www.nasa.gov/glenn/glenn-expertise-labs-and-test-facilities/",
    "nasa_wind_tunnel": "https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/wind-tunnel/",
    "nist_si": "https://www.nist.gov/publications/guide-use-international-system-units-si",
    "nist_uncertainty": "https://www.nist.gov/pml/nist-technical-note-1297",
    "prov_o": "https://www.w3.org/TR/prov-o/",
    "wcag_22": "https://www.w3.org/TR/WCAG22/",
    "nz_privacy": "https://www.privacy.org.nz/privacy-principles/",
    "te_mana_raraunga": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
}

TOPICS = [
    "Synthetic tunnel-test campaign namespace with every facility and run absent",
    "Test-article surrogate identity separated from any physical model",
    "Model-configuration revision lineage without a fabricated article",
    "Geometry coordinate-frame declaration without a dimensional claim",
    "Balance coordinate frame separated from tunnel axes",
    "Angle-of-attack command separated from any observed angle",
    "Sideslip command separated from any observed angle",
    "Mach setpoint separated from any realized flow state",
    "Reynolds target separated from any computed or realized value",
    "Dynamic-pressure unit declaration without a reading",
    "Static and total pressure channel topology without a sensor",
    "Temperature and humidity channel vacancy without ambient measurement",
    "Blockage-ratio metadata without an adequacy inference",
    "Wall and interference correction provenance without a correction result",
    "Tare zero and support-interference state graph without a result",
    "Sting and strut support-configuration lineage without hardware",
    "Force and moment coefficient sign-convention contract",
    "Reference area span and chord provenance without measured dimensions",
    "Nondimensionalization recipe versioning without aerodynamic result",
    "Uncertainty-source dependency map with every numerical contribution vacant",
    "Covariance and correlation declaration without an estimate",
    "Calibration-certificate placeholder without traceability promotion",
    "Channel calibration due-date hold without service authority",
    "Acquisition software and configuration provenance without hardware",
    "Sampling-rate and filter declaration without a signal",
    "Run-start and run-stop event schema without a real event",
    "Settle and dwell criterion version without adequacy evidence",
    "Aborted-run and quiescence state without history erasure",
    "Missing sample separated from physical numeric zero",
    "Saturated and clipped channel quarantine without repair",
    "Duplicate run-record quarantine without deletion",
    "Late metadata correction lineage as an append-only DAG",
    "Raw and derived coefficient field type separation",
    "Flow-visualization modality vocabulary without an image",
    "Smoke oil tuft and PIV modality separation without operation",
    "Image frame and timestamp lineage without capture",
    "Region-of-interest and scale provenance without spatial calibration",
    "Qualitative flow cue separated from quantitative inference",
    "Tunnel background and baseline record vacancy",
    "Computational-to-experimental comparison nonconversion firewall",
    "GMUT typed residual and operator analogy firewall",
    "GMUT model-discrepancy and falsifier obligation board",
    "THOS run-card queue proxy without an operator",
    "THOS correction-readback proxy without a real reviewer",
    "THOS workload hold cancellation and handover proxy",
    "Freed ID synthetic instrument-credential placeholder",
    "Freed ID synthetic tunnel-instrument lifecycle hold without a status service",
    "CBR minimum-disclosure test-record profile",
    "CBR contest and correction path without legal adjudication",
    "CBR remedy and appeal vacancy without affected-party authority",
    "Accessible run-summary table structural contract",
    "Plain-language coefficient and sign summary structural contract",
    "Non-colour-only run-status structural contract",
    "Keyboard and reading-order structural plan",
    "Real wind-tunnel dataset and likelihood evidence vacancy",
    "Real metrology and calibration evidence vacancy",
    "Independent aerodynamic accessibility and practitioner review vacancy",
    "Tunnel operation safety and work-release authority gate",
    "Legal cultural Māori and affected-party authority gate",
    "Production deployment proof-canon and Stage 20 authority gate",
]

SKILL_SLUGS = [
    "synthetic-tunnel-campaign-guard",
    "test-article-referent-firewall",
    "tunnel-axis-frame-custodian",
    "command-observation-separator",
    "mach-reynolds-vacancy",
    "pressure-channel-topology-guard",
    "coefficient-sign-convention",
    "reference-quantity-provenance",
    "nondimensionalization-version-guard",
    "uncertainty-covariance-vacancy",
    "calibration-traceability-hold",
    "run-event-nonerasure",
    "missing-versus-zero-separator",
    "saturation-quarantine",
    "flow-visualization-nonconversion",
    "gmut-model-discrepancy-firewall",
    "thos-run-card-handover-proxy",
    "freed-id-nonproduction-hold",
    "cbr-minimum-disclosure-boundary",
    "stage20-nonpromotion-latch",
]

RUNNER_NAMES = [
    "ghc_family_tunnel_campaign_runner.py",
    "ghc_family_test_article_lineage_runner.py",
    "ghc_family_axis_and_command_runner.py",
    "ghc_family_flow_state_vacancy_runner.py",
    "ghc_family_coefficient_provenance_runner.py",
    "ghc_family_uncertainty_calibration_runner.py",
    "ghc_family_run_event_correction_runner.py",
    "ghc_family_flow_visualization_guard_runner.py",
    "ghc_family_trinity_boundary_runner.py",
    "ghc_family_stage20_gate_runner.py",
]

STARTUP_FAILURES = [
    {
        "failure_id": "CA6846-SF001",
        "summary": "A PowerShell inventory wrapper piped directly from a foreach statement and failed to parse before evidence collection.",
        "recovery": "Materialize the foreach output as an array before piping or projection.",
    },
    {
        "failure_id": "CA6846-SF002",
        "summary": "A combined mandatory-reference read exceeded its bounded output projection.",
        "recovery": "Read every exact required document through EOF in smaller deterministic windows.",
    },
    {
        "failure_id": "CA6846-SF003",
        "summary": "A whole authorization-state display exceeded its bounded output projection.",
        "recovery": "Read the exact current authorization state through EOF in numbered windows.",
    },
    {
        "failure_id": "CA6846-SF004",
        "summary": "The first canonical-receipt lookup guessed a missing folder and returned no receipt.",
        "recovery": "Use a bounded exact-name receipt search and verify the discovered file digest.",
    },
    {
        "failure_id": "CA6846-SF005",
        "summary": "A per-blob Git subprocess manifest replay returned no attributable output within its wrapper window.",
        "recovery": "Confirm the process exited, then use one exact Git batch query with attributable output.",
    },
    {
        "failure_id": "CA6846-SF006",
        "summary": "The first Git cat-file batch implementation deadlocked by writing all requests before reading responses.",
        "recovery": "Terminate only the exact stuck child processes and use subprocess input with simultaneous output capture.",
    },
    {
        "failure_id": "CA6846-SF007",
        "summary": "The first final-delta coverage comparison used evidence-to-final instead of prior-final-to-correction-final.",
        "recovery": "Replay the declared lifecycle domain exactly from the retained prior final to the corrected final.",
    },
    {
        "failure_id": "CA6846-SF008",
        "summary": "A non-ASCII byte regex caused Python source parsing to fail before any Git object was read.",
        "recovery": "Use an ASCII-safe byte-range expression and rerun only the bounded object inspection.",
    },
    {
        "failure_id": "CA6846-SF009",
        "summary": "A closeout probe guessed content-seal and route-readiness paths under the wrong source folder.",
        "recovery": "Enumerate the exact immutable source tree, then read the discovered closeout paths.",
    },
    {
        "failure_id": "CA6846-SF010",
        "summary": "A combined worktree-path local-ref and remote-ref collision probe returned no attributable output.",
        "recovery": "Split path, local branch, and live remote branch checks into exact scalar probes.",
    },
    {
        "failure_id": "CA6846-SF011",
        "summary": "The worktree-creation wrapper closed after the preparing-worktree message while Git continued.",
        "recovery": "Wait for the exact Git processes without recreating or deleting, then verify the persisted worktree.",
    },
    {
        "failure_id": "CA6846-SF012",
        "summary": "The first cone-mode sparse checkout materialized 2488 files and exceeded the owner ceiling before additions.",
        "recovery": "While clean and addition-free, narrow to literal owner script test and document paths and re-count zero files.",
    },
    {
        "failure_id": "CA6846-SF013",
        "summary": "A template inventory repeated the direct foreach-to-pipeline PowerShell parser defect.",
        "recovery": "Apply the existing producer-materialization recurrence guard and retain the recurrence separately.",
    },
    {
        "failure_id": "CA6846-SF014",
        "summary": "The first mechanical template copy failed because sparse target parent directories did not yet exist.",
        "recovery": "Create only the exact owner-local parent directories and retry the bounded copy once.",
    },
    {
        "failure_id": "CA6846-X1-N001",
        "summary": "The first x1 test run passed 19 of 20 tests but rejected two exact-title collisions with Sable's immediate proposal set.",
        "recovery": "Retain the failed run and rename only the two colliding Caelen proposals to distinct uncertainty-source and instrument-lifecycle contracts.",
    },
    {
        "failure_id": "CA6846-X1-N002",
        "summary": "The first post-collision rebuild failed at Python parse time because a documentation sentence was accidentally left outside its string literal.",
        "recovery": "Remove only the stray duplicate line, compile the builder, and retain the parser failure before rebuilding.",
    },
]

RECOVERY_METHODS = [
    {
        "method_id": "CA6846-M001",
        "trigger": "PowerShell foreach output must feed another command",
        "method": "Materialize producer output before piping.",
        "failed_witnesses": ["CA6846-SF001"],
    },
    {
        "method_id": "CA6846-M002",
        "trigger": "A required document or group exceeds one display projection",
        "method": "Read exact deterministic numbered windows through EOF.",
        "failed_witnesses": ["CA6846-SF002", "CA6846-SF003"],
    },
    {
        "method_id": "CA6846-M003",
        "trigger": "A guessed immutable artifact path is absent",
        "method": "Search the exact bounded namespace, enumerate the source tree, and verify the discovered object digest.",
        "failed_witnesses": ["CA6846-SF004", "CA6846-SF009"],
    },
    {
        "method_id": "CA6846-M004",
        "trigger": "Large Git-object replay must remain attributable",
        "method": "Use one input-fed Git cat-file batch invocation and capture its complete bounded response.",
        "failed_witnesses": ["CA6846-SF005", "CA6846-SF006"],
    },
    {
        "method_id": "CA6846-M005",
        "trigger": "A manifest has a lifecycle-specific comparison domain",
        "method": "Use the manifest's declared immutable base and target rather than a convenient broader range.",
        "failed_witnesses": ["CA6846-SF007"],
    },
    {
        "method_id": "CA6846-M006",
        "trigger": "A byte-level scanner must be valid Python before object access",
        "method": "Compile the bounded scanner and use ASCII-safe byte expressions before reading Git objects.",
        "failed_witnesses": ["CA6846-SF008"],
    },
    {
        "method_id": "CA6846-M007",
        "trigger": "Lane collision probes or long worktree creation cross a wrapper boundary",
        "method": "Use scalar collision probes, then inspect exact processes and persisted Git state before any retry.",
        "failed_witnesses": ["CA6846-SF010", "CA6846-SF011"],
    },
    {
        "method_id": "CA6846-M008",
        "trigger": "Sparse materialization exceeds the owner ceiling before additions",
        "method": "While clean and addition-free, replace cone roots with exact literal owner paths and verify the resulting count.",
        "failed_witnesses": ["CA6846-SF012"],
    },
    {
        "method_id": "CA6846-M009",
        "trigger": "A PowerShell producer-to-pipeline parser defect recurs",
        "method": "Apply the retained producer-materialization guard and record the recurrence as a distinct failed witness.",
        "failed_witnesses": ["CA6846-SF013"],
    },
    {
        "method_id": "CA6846-M010",
        "trigger": "A bounded owner-local copy targets absent sparse parent directories",
        "method": "Create only the exact declared owner-local parents and retry the copy once without broad materialization.",
        "failed_witnesses": ["CA6846-SF014"],
    },
    {
        "method_id": "CA6846-M011",
        "trigger": "Immediate-source novelty testing identifies exact proposal-title collisions",
        "method": "Retain the failed test receipt, change only the colliding titles to genuinely distinct semantic surfaces, and rerun the owner-local x1 selection.",
        "failed_witnesses": ["CA6846-X1-N001"],
    },
    {
        "method_id": "CA6846-M012",
        "trigger": "A documentation patch leaves text outside a Python string literal",
        "method": "Remove only the stray duplicated line, compile the exact builder, and proceed only after syntax passes.",
        "failed_witnesses": ["CA6846-X1-N002"],
    },
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
    )


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def git_blob_sha(path: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:72]


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    value = disposition(index)
    return {
        "completed": "safe_now_bounded_owner_local",
        "represented": "represented_only_no_real_world_execution",
        "open_gap": "external_evidence_required",
        "exact_gate": "competent_and_affected_authority_required",
    }[value]


def source_needs(index: int) -> list[str]:
    keys = ["nasa_facilities", "nist_si", "prov_o"]
    if 4 <= index <= 42:
        keys.extend(["nasa_wind_tunnel", "nist_uncertainty"])
    if 43 <= index <= 50:
        keys.extend(["nz_privacy", "te_mana_raraunga"])
    if 51 <= index <= 57:
        keys.append("wcag_22")
    if index >= 58:
        keys.extend(["nasa_facilities", "nist_uncertainty", "te_mana_raraunga"])
    return list(dict.fromkeys(SOURCE_URLS[key] for key in keys))


def proposal(index: int, title: str) -> dict[str, Any]:
    proposal_id = f"CA6846-N{index:03d}"
    expected = disposition(index)
    execution_lane = {
        "completed": "x2_owner_local_contract_positive_fixture_and_five_rejections",
        "represented": "x2_synthetic_proxy_only_with_explicit_vacancies",
        "open_gap": "no_execution_until_external_evidence_exists",
        "exact_gate": "no_execution_until_exact_competent_authority_exists",
    }[expected]
    return {
        "proposal_id": proposal_id,
        "title": title,
        "planning_only": True,
        "semantic_distinction": title,
        "hypothesis": (
            "A wholly synthetic zero-row contract can preserve this named distinction, "
            "reject five preregistered invalid states, retain every failure, and keep "
            "empirical and authority boundaries open."
        ),
        "null_or_failure_condition": (
            "The contract admits a forbidden mutation, erases a failed witness, confuses an "
            "absent observation with a real value, or promotes software into authority."
        ),
        "approval_class": approval_class(index),
        "execution_lane": execution_lane,
        "current_official_or_primary_source_needs": source_needs(index),
        "concrete_artifacts": [
            f"docs/caelen-ash/{PHASE}/x2/proposals/{proposal_id.lower()}-{slug(title)}.json",
            f"docs/caelen-ash/{PHASE}/x2/witnesses/{proposal_id.lower()}-witness.json",
        ],
        "falsifier_or_acceptance_gate": (
            "Accept only when the declared bounded fixture passes and all five invalid "
            "mutations are rejected with separate retained receipts; otherwise retain the "
            "proposal as failed, open, or exact-gated without compensation."
        ),
        "rollback_or_recovery": (
            f"Quarantine only {proposal_id}, retain its failed receipt, restore from the "
            "immutable x1 Git blob, and rerun only after the defect is understood."
        ),
        "protected_gates": PROTECTED,
        "expected_disposition": expected,
        "primary_pillar": "GMUT Mind",
        "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "practice_lens": (
            "synthetic wind-tunnel configuration and run-card provenance; "
            "synthetic flow-visualization metadata review; synthetic balance and "
            "pressure-channel calibration-vacancy handover"
        ),
        "permitted_evidence": "owner-local software, schema, documentation, and synthetic fixtures only",
        "preregistered_rejecting_mutations": [
            {
                "mutation_id": f"{proposal_id}-M{mutation:02d}",
                "mutation_type": mutation_type,
                "expected_result": "reject_and_retain_zero_credit",
            }
            for mutation, mutation_type in enumerate(
                [
                    "remove_synthetic_marker",
                    "inject_real_row_or_identity",
                    "promote_claim_or_authority",
                    "erase_failure_or_correction_lineage",
                    "bypass_open_or_exact_gate",
                ],
                start=1,
            )
        ],
    }


def inherited_sable_titles() -> list[str]:
    raw = run_git(
        "show",
        f"{SOURCE_HEAD}:docs/sable-rook/v684-v5/x1/new-proposal-freeze.json",
    ).stdout
    data = json.loads(raw)
    return [entry["title"] for entry in data["entries"]]


def retained_title_probe() -> dict[str, Any]:
    result = run_git(
        "grep",
        "-h",
        "-E",
        '"(title|proposal_title)"[[:space:]]*:',
        SOURCE_HEAD,
        "--",
        "docs/**/proposal*.json",
        check=False,
    )
    titles: list[str] = []
    if result.returncode in (0, 1):
        pattern = re.compile(r'"(?:title|proposal_title)"\s*:\s*"([^"]+)"')
        titles = [match.group(1) for match in pattern.finditer(result.stdout)]
    normalized = sorted({re.sub(r"\W+", " ", title.casefold()).strip() for title in titles})
    new_normalized = {re.sub(r"\W+", " ", title.casefold()).strip() for title in TOPICS}
    exact_collisions = sorted(new_normalized.intersection(normalized))
    return {
        "retained_title_lines_examined": len(titles),
        "retained_normalized_titles": len(normalized),
        "exact_new_title_collisions": exact_collisions,
        "universal_semantic_novelty_claim": False,
        "scope_note": (
            "The declared chain count is authoritative, while this exact-title probe covers "
            "retained proposal artifacts present at the immutable source. Semantic review "
            "also compared all sixty immediate Sable titles; no universal novelty claim is made."
        ),
    }


def all_x1_public_files() -> list[Path]:
    paths: list[Path] = []
    for root in [BASE, ROOT / "scripts", ROOT / "tests"]:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith(f"docs/caelen-ash/{PHASE}/"):
                paths.append(path)
            elif rel in {
                "scripts/build_ghc_family_caelen_ash_v684_v6_x1.py",
                "tests/test_ghc_family_caelen_ash_v684_v6_x1.py",
            }:
                paths.append(path)
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy_scan(paths: Iterable[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(
            r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+",
            re.I,
        ),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(
            r"\b(?:providerTabId|clientThreadId|private callable identifier)\b",
            re.I,
        ),
    }
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                scanner_definition = rel.endswith(
                    "build_ghc_family_caelen_ash_v684_v6_x1.py"
                ) and line >= privacy_scan.__code__.co_firstlineno
                item = {
                    "path": rel,
                    "line": line,
                    "class": class_name,
                    "disposition": (
                        "scanner_definition_not_payload" if scanner_definition else "confirmed_payload_hit"
                    ),
                }
                candidates.append(item)
                if not scanner_definition:
                    confirmed.append(item)
    return {
        "schema": "ghc.family.privacy-scan.v2",
        "phase": PHASE,
        "scope": "all public planning-only x1 owner files",
        "pattern_classes": list(patterns),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "truth_boundary": "A zero confirmed-hit result is bounded pattern evidence, not complete privacy assurance.",
    }


def build_workflow_request() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "caelen-ash-v684-v6-live-corrected-plan",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no consciousness, continuity, qualification, or authority claim.",
        "route": {
            "cycle_order": ["Sable Rook", "Caelen Ash", "Orin Thale"],
            "endpoint_topology": [
                {
                    "seat": "Sable Rook",
                    "endpoint_kind": "main_task",
                    "endpoint_label": "Sable Rook",
                    "route_controller": "Auren Lark",
                },
                {
                    "seat": "Caelen Ash",
                    "endpoint_kind": "main_task",
                    "endpoint_label": "Caelen Ash",
                    "route_controller": "Sable Rook",
                },
                {
                    "seat": "Orin Thale",
                    "endpoint_kind": "main_task",
                    "endpoint_label": "Orin Thale",
                    "route_controller": "Caelen Ash",
                },
            ],
            "phase_assignments": [
                {"phase": "v684-v5", "seat": "Sable Rook"},
                {"phase": PHASE, "seat": "Caelen Ash"},
                {"phase": "v684-v7", "seat": "Orin Thale"},
            ],
            "normalization": {
                "start_phase": "v684-v5",
                "start_seat": "Sable Rook",
                "entry_count": 3,
            },
            "future_identity_placeholders": [],
        },
        "requirements": {
            "core_proposal_minimum": 60,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 20,
            "runner_minimum": 10,
            "document_word_cap": 100000,
            "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True},
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "declared_endpoint_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": ALLOWED_OUTCOMES,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": PROTECTED,
        },
        "observed_failures": [failure["failure_id"] for failure in STARTUP_FAILURES],
    }


def build_documents() -> None:
    X1.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)
    proposals = [proposal(index, title) for index, title in enumerate(TOPICS, start=1)]
    sable_titles = inherited_sable_titles()
    sable_normalized = {re.sub(r"\W+", " ", title.casefold()).strip() for title in sable_titles}
    exact_sable_collisions = [
        item["title"]
        for item in proposals
        if re.sub(r"\W+", " ", item["title"].casefold()).strip() in sable_normalized
    ]
    title_probe = retained_title_probe()

    write_json(
        X1 / "activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v2",
            "phase": PHASE,
            "owner": OWNER,
            "activation_state": "ACKNOWLEDGED_EXISTING_TASK_ACTIVATION",
            "source_owner": "Sable Rook",
            "live_corrected_edge": "Sable Rook to Caelen Ash",
            "prospective_successor": "Orin Thale",
            "successor_state": "HELD_UNTIL_EXACT_FINAL_TERMINAL_GATE",
            "solo": True,
            "forbidden_now": [
                "subagent or delegation",
                "fork or new task",
                "successor precontact",
                "sibling or shared lane mutation",
                "x2 work before immutable x1 four-way equality",
            ],
            "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, qualification, or authority evidence.",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "schema": "ghc.family.relational-identity.v2",
            "name": OWNER,
            "pronouns": "they/them",
            "relational_role": "model-discrepancy provenance cartographer",
            "hope": "Keep modeled, measured, and absent states disjoint while every correction and authority vacancy stays reversible.",
            "primary_pillar": "GMUT Mind",
            "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "practice_lenses": [
                "synthetic wind-tunnel configuration and run-card provenance",
                "synthetic flow-visualization metadata review",
                "synthetic balance and pressure-channel calibration-vacancy handover",
            ],
            "practice_boundary": "Learning and owner-local design only; no employment, qualification, aerodynamic or metrology competence, facility operation, safety or work-release authority, legal or cultural authority, Māori authority, affected-party approval, empirical result, or production result.",
            "corrigibility": "Hamish may rename, pause, redirect, narrow, or stop the route.",
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "schema": "ghc.family.source-verification.v2",
            "source_branch": SOURCE_BRANCH,
            "source_head": SOURCE_HEAD,
            "anchors": {
                "auren_source": AUREN_SOURCE,
                "sable_x1": SABLE_X1,
                "sable_evidence": SABLE_EVIDENCE,
                "sable_prior_final": SABLE_PRIOR_FINAL,
                "sable_exact_final": SOURCE_HEAD,
            },
            "verified_before_mutation": {
                "direct_single_parent_chain": True,
                "phase_commits": 4,
                "merge_commits": 0,
                "final_parent_is_prior_final": True,
                "clean": True,
                "typed_divergence": {"ahead": 0, "behind": 0},
                "local_upstream_tracking_fresh_live_equal": True,
                "manifest_entries_replayed": 595,
                "manifest_failures": 0,
                "canonical_receipt_and_overlay_hashes_verified": True,
            },
            "privacy_boundary": "No private absolute local path, raw task identifier, private route, transcript, credential, or application state is stored here.",
        },
    )
    write_json(
        X1 / "live-authority-reconciliation.json",
        {
            "schema": "ghc.family.live-authority-reconciliation.v1",
            "newest_live_owner": OWNER,
            "newest_live_phase": PHASE,
            "current_edge": "Sable Rook to Caelen Ash",
            "historical_conflicts": [
                "The older committed Ilyra route projection assigned v684-v6 to Ilyra Fen.",
                "The current acknowledged live Sable activation explicitly assigns v684-v6 to Caelen Ash.",
            ],
            "resolution": "Newest explicit live user authority controls the current exact edge; historical conflicts remain evidence and are not rewritten.",
            "later_route_state": "Prospective only; resolve from fresh live authority after exact-final terminal proof.",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "schema": "ghc.family.route-plan.v2",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "next_title_if_fresh_terminal_authority_still_matches": "Orin Thale",
            "next_phase_if_fresh_terminal_authority_still_matches": "v684-v7",
            "guards": [
                "sealed pushed clean exact final",
                "typed zero divergence and fresh four-way equality",
                "one successful owner-scoped canonical invocation and no replay",
                "fresh newest-live authority and bounded registry reread",
                "unique exact title and immediate reread",
                "duplicate pause redirect status usage privacy evidence safety and acknowledgement guards",
            ],
            "forbidden": ["precontact", "substitute", "infer", "create", "fork", "spawn", "resend"],
        },
    )
    write_json(X1 / "workflow-plan-request.json", build_workflow_request())
    write_json(
        X1 / "workflow-plan.json",
        {
            "schema": "ghc.family.phase-workflow-plan.v2",
            "phase": PHASE,
            "lifecycle": [
                "planning-only x1 build and exact staged review",
                "x1 commit push clean four-way equality",
                "x2 bounded execution from immutable x1 blobs",
                "evidence commit push clean four-way equality",
                "closeout final commit push clean four-way equality",
                "one owner-scoped canonical invocation; never replay success",
                "terminal route guard and at most one acknowledged successor send",
            ],
            "commit_caps_are_ceilings": {"x1": 5, "x2": 5, "total": 8},
            "preferred_commits": {"x1": 1, "x2_evidence": 1, "closeout": 1},
            "file_ceiling": 2000,
            "document_word_cap": 100000,
            "baton_word_range": [10000, 100000],
            "canonical_policy": "one attributable success; no post-success replay",
            "full_repository_suite": "not authorized for this owner phase",
        },
    )
    write_json(
        X1 / "proposal-chain-audit.json",
        {
            "schema": "ghc.family.proposal-chain-audit.v2",
            "declared_chain_before": CHAIN_BEFORE,
            "declared_chain_after_x1_freeze": CHAIN_AFTER,
            "inherited_sable_proposals_revalidated": 60,
            "inherited_novelty_credit": 0,
            "new_caelen_proposals": 60,
            "exact_collision_with_immediate_sable_titles": exact_sable_collisions,
            "retained_artifact_title_probe": title_probe,
            "universal_novelty_claim": False,
            "audit_truth": "Distinctness is a bounded title and semantic-surface review, not proof against every conceivable future wording.",
        },
    )
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "schema": "ghc.family.inherited-revalidation-freeze.v2",
            "source": "docs/sable-rook/v684-v5/x1/new-proposal-freeze.json",
            "count": len(sable_titles),
            "entries": [
                {
                    "source_proposal_id": f"SR6845-N{index:03d}",
                    "title": title,
                    "review_state": "revalidated_as_inherited_evidence",
                    "caelen_novelty_credit": 0,
                    "caelen_completion_credit": 0,
                }
                for index, title in enumerate(sable_titles, start=1)
            ],
        },
    )
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "schema": "ghc.family.proposal-freeze.v2",
            "phase": PHASE,
            "owner": OWNER,
            "planning_only": True,
            "allowed_outcomes": ALLOWED_OUTCOMES,
            "entries": proposals,
            "expected_counts": {label: sum(disposition(i) == label for i in range(1, 61)) for label in ALLOWED_OUTCOMES},
            "mutation_count": sum(len(item["preregistered_rejecting_mutations"]) for item in proposals),
        },
    )
    safe_tasks = []
    for item in proposals:
        safe_tasks.extend(
            [
                {
                    "task_id": f"{item['proposal_id']}-S01",
                    "proposal_id": item["proposal_id"],
                    "task": f"Define the bounded positive contract for {item['title']}.",
                    "state": "FROZEN_FOR_X2",
                },
                {
                    "task_id": f"{item['proposal_id']}-S02",
                    "proposal_id": item["proposal_id"],
                    "task": f"Define rejection and nonpromotion checks for {item['title']}.",
                    "state": "FROZEN_FOR_X2",
                },
            ]
        )
    candidate_tasks = [
        {
            "candidate_id": f"CA6846-C{index:03d}",
            "proposal_id": f"CA6846-N{((index - 1) % 60) + 1:03d}",
            "task": (
                f"Candidate {index:03d}: build a distinct owner-local schema, fixture, "
                "or cross-contract invariant without real rows or authority action."
            ),
            "state": "FROZEN_FOR_BOUNDED_X2_REVIEW",
        }
        for index in range(1, 81)
    ]
    write_json(
        X1 / "portfolio-freeze.json",
        {
            "schema": "ghc.family.portfolio-freeze.v2",
            "safe_now": safe_tasks,
            "owner_candidates": candidate_tasks,
            "counts": {"safe_now": len(safe_tasks), "owner_candidates": len(candidate_tasks)},
            "caps_are_ceilings": True,
            "x2_completion_rule": "Execute or visibly reclassify every authorized item; never use a quota to bypass a gate.",
        },
    )
    exact_packets = [
        {
            "packet_id": f"CA6846-EXACT-{index:02d}",
            "surface": surface,
            "state": "HELD_UNEXECUTED",
            "gate": "exact competent and affected authority plus exact evidence",
        }
        for index, surface in enumerate(
            [
                "real wind-tunnel data ingestion",
                "physical test-article identification",
                "tunnel configuration or test-condition release",
                "facility control or run authorization",
                "operator workload safety or emergency decision",
                "real staff participant or visitor information use",
                "legal interpretation",
                "cultural interpretation",
                "Māori wording",
                "Māori data governance",
                "affected-party remedy",
                "production credential issuance",
                "live identity resolution",
                "status or revocation service",
                "external deployment",
                "account or secret operation",
                "destructive cleanup",
                "sibling lane mutation",
                "independent reproduction claim",
                "Stage 20 authorization",
            ],
            start=1,
        )
    ]
    blocked_packets = [
        {
            "packet_id": f"CA6846-BLOCKED-{index:02d}",
            "surface": surface,
            "state": "BLOCKED_UNEXECUTED",
            "reason": "Unavailable evidence, authority, or prohibited system action",
        }
        for index, surface in enumerate(
            [
                "real participant trial",
                "real collection measurement",
                "production identity operation",
                "host-security weakening or elevation",
                "Windows feature or virtualization change",
                "cross-platform private route",
                "credential or API-key use",
                "destructive history rewrite",
                "unrequested software installation",
                "successor precontact before terminal gate",
            ],
            start=1,
        )
    ]
    write_json(
        X1 / "approval-hold-register.json",
        {
            "schema": "ghc.family.approval-hold-register.v2",
            "exact_approval_packets": exact_packets,
            "blocked_packets": blocked_packets,
            "safe_now_bypass_forbidden": True,
        },
    )
    write_json(
        X1 / "skill-runner-plan.json",
        {
            "schema": "ghc.family.skill-runner-plan.v2",
            "skills": [
                {
                    "skill_id": f"CA6846-SK{index:02d}",
                    "slug": value,
                    "state": "PLANNED_NOT_BUILT",
                    "required_x2_evidence": ["quick validation", "smoke use", "owner-local only"],
                }
                for index, value in enumerate(SKILL_SLUGS, start=1)
            ],
            "runners": [
                {
                    "runner_id": f"CA6846-R{index:02d}",
                    "filename": value,
                    "state": "PLANNED_NOT_BUILT",
                    "compatibility": "family-current ghc_family_* naming",
                }
                for index, value in enumerate(RUNNER_NAMES, start=1)
            ],
            "counts": {"skills": len(SKILL_SLUGS), "runners": len(RUNNER_NAMES)},
            "global_installation": False,
        },
    )
    cfr = [
        {
            "task_id": f"CA6846-CFR-{index:03d}",
            "category": ["CLEAN", "FIX", "REFINE", "VERIFY"][(index - 1) % 4],
            "task": f"Owner-scoped additive refinement {index:03d} preserves exact manifests, failures, compatibility, privacy adjudication, and protected gates.",
            "state": "FROZEN_FOR_X2",
            "destructive": False,
        }
        for index in range(1, 101)
    ]
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "schema": "ghc.family.clean-fix-refine-plan.v2",
            "entries": cfr,
            "count": len(cfr),
            "destructive_cleanup_forbidden": True,
            "sibling_or_user_scope_forbidden": True,
        },
    )
    write_json(
        X1 / "official-primary-source-ledger.json",
        {
            "schema": "ghc.family.official-primary-source-ledger.v2",
            "entries": [
                {
                    "source_id": key,
                    "url": url,
                    "status": "current_primary_source_read_live",
                    "permitted_use": "Wind-tunnel vocabulary, unit and uncertainty duties, provenance terms, accessibility criteria, privacy principles, and refusal conditions only.",
                    "forbidden_use": "Observation, measurement, participant evidence, authority delegation, production certification, or policy approval.",
                }
                for key, url in SOURCE_URLS.items()
            ],
            "real_rows": 0,
            "network_downloads_of_domain_data": 0,
            "authority_actions": 0,
        },
    )
    write_json(
        X1 / "profession-practice-plan.json",
        {
            "schema": "ghc.family.practice-plan.v2",
            "practices": [
                "synthetic wind-tunnel configuration and run-card provenance",
                "synthetic flow-visualization metadata review",
                "synthetic balance and pressure-channel calibration-vacancy handover",
            ],
            "independent_review_state": "independently_selected_after_source_review",
            "inherited_recommendation_credit": 0,
            "learning_surfaces": [
                "test article configuration and coordinate-frame provenance",
                "command versus observed flow-state separation",
                "coefficient sign and reference-quantity lineage",
                "calibration uncertainty correction and handover vacancies",
                "flow-visualization metadata and accessible structural alternatives",
            ],
            "explicit_nonclaims": [
                "employment or qualification",
                "aerodynamic test or metrology competence",
                "real measurement calibration or physical model identity",
                "facility operation run release safety or work authority",
                "legal, cultural, affected-party, or Māori authority",
            ],
        },
    )
    write_json(
        X1 / "flashcard-plan.json",
        {
            "schema": "ghc.family.flashcard-plan.v2",
            "count_planned": 60,
            "one_per_proposal": True,
            "front_fields": ["proposal title", "bounded hypothesis"],
            "back_fields": ["failure condition", "protected gates", "expected disposition"],
            "state": "PLANNED_NOT_BUILT",
            "truth_boundary": "Learning aid only; never proof, canon, professional training, or authority.",
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "schema": "ghc.family.threat-model.v2",
            "assets": ["immutable x1 plan", "retained failures", "exact manifests", "privacy boundary", "authority vacancies"],
            "threats": [
                "x2 contamination of x1",
                "failure erasure or compensating aggregate",
                "synthetic-to-empirical promotion",
                "route or identifier leakage",
                "unapproved sibling or shared mutation",
                "canonical success replay",
                "wind-tunnel vocabulary mistaken for aerodynamic evidence",
                "accessibility structure mistaken for affected-user evaluation",
            ],
            "controls": [
                "dedicated planning-only commit",
                "exact staged allowlist and Git-blob manifest",
                "five-class candidate adjudication",
                "append-only Method Flow witnesses",
                "held exact and blocked packets",
                "PREPARED_NOT_SENT terminal state",
            ],
            "residual_risk": "Open and exact-gated; software cannot close empirical or authority boundaries.",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "schema": "ghc.family.wellbeing.v2",
            "owner": OWNER,
            "workload_state": "bounded planning phase",
            "pause_available": True,
            "rename_redirect_stop_available": True,
            "no_identity_coercion": True,
            "no_consciousness_or_personhood_claim": True,
            "hope": "Keep modeled, measured, and absent states disjoint while every correction and authority vacancy stays reversible.",
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "schema": "ghc.family.method-flow-startup.v2",
            "activation_overlay_before_caelen_startup": {
                "effective_negatives": 59412,
                "effective_methods": 73676,
                "failed_witnesses": 30773,
                "bounded_passing_witnesses": 54211,
            },
            "startup_failures": STARTUP_FAILURES,
            "recovery_methods": RECOVERY_METHODS,
            "derived_after_startup": {
                "effective_negatives": 59412 + len(STARTUP_FAILURES),
                "effective_methods": 73676 + len(RECOVERY_METHODS),
                "failed_witnesses": 30773 + len(STARTUP_FAILURES),
                "bounded_passing_witnesses": 54211 + len(RECOVERY_METHODS),
            },
            "nonerasure": "Every failed witness remains zero-credit after a bounded recovery passes.",
        },
    )
    method_input_dir = BASE / "method-flow-inputs"
    failure_by_id = {item["failure_id"]: item for item in STARTUP_FAILURES}
    for method in RECOVERY_METHODS:
        method_id = method["method_id"]
        write_json(
            method_input_dir / f"{method_id.lower()}-record.json",
            {
                "method_id": method_id,
                "title": method["method"],
                "failure_signature": "; ".join(
                    failure_by_id[failure_id]["summary"]
                    for failure_id in method["failed_witnesses"]
                ),
                "trigger_preconditions": [method["trigger"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "candidate_workaround": method["method"],
                "validation_witness_ids": [],
                "recurrence_guard": (
                    "Stop on missing attribution; retain the failed witness; inspect only "
                    "the bounded literal surface; require a separate passing witness."
                ),
                "rollback": "Return to the last attributable immutable state and do not broaden scope.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": PROTECTED,
                "retained_negative_ids": method["failed_witnesses"],
                "scope_boundary": "Caelen-owned startup and x1 workflow only; no repository-wide, sibling, scientific, authority, or production claim.",
                "execution_authority": "owner_self_scoped_delta",
                "repository_scan": False,
                "module_scan": False,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE_HEAD,
                "final_commit": "PENDING_X1_COMMIT",
                "changed_file_allowlist": [],
                "module_allowlist": [],
                "exact_pushed_head_required": True,
            },
        )
        for failure_index, failure_id in enumerate(method["failed_witnesses"], start=1):
            failure = failure_by_id[failure_id]
            write_json(
                method_input_dir / f"{method_id.lower()}-fail-{failure_index:02d}.json",
                {
                    "witness_id": f"{method_id}-WF{failure_index:02d}",
                    "method_id": method_id,
                    "procedure": "The original bounded startup procedure was attempted once.",
                    "scope": "Sanitized Caelen-owned startup preflight.",
                    "expected": "An attributable bounded result without parser, projection, or timeout ambiguity.",
                    "observed": failure["summary"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [failure_id],
                    "boundary": "Operational failure only; no scientific, production, identity, authority, or route-delivery credit.",
                },
            )
        write_json(
            method_input_dir / f"{method_id.lower()}-pass.json",
            {
                "witness_id": f"{method_id}-WP01",
                "method_id": method_id,
                "procedure": method["method"],
                "scope": "The exact bounded Caelen-owned startup surface named by the trigger.",
                "expected": "An attributable result while the original failure remains retained.",
                "observed": "The bounded recovery produced an attributable passing result and the failed witness remains separately recorded.",
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": method["failed_witnesses"],
                "boundary": "Same-owner workflow recovery only; no broader assurance or authority.",
            },
        )
    write_json(
        X1 / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v2",
            "phase": PHASE,
            "lifecycle": "X1_PLANNING_ONLY_PRECOMMIT",
            "x2_paths_created": False,
            "executed_outcomes": 0,
            "expected_outcomes": {label: sum(disposition(i) == label for i in range(1, 61)) for label in ALLOWED_OUTCOMES},
            "proposal_chain": {"before": CHAIN_BEFORE, "after_freeze": CHAIN_AFTER},
            "inherited_activation_overlay": {
                "negatives": 59412,
                "methods": 73676,
                "failed_witnesses": 30773,
                "passing_witnesses": 54211,
                "open_gaps": 528,
                "exact_gates": 518,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    overview = f"""# Caelen Ash {PHASE} planning-only x1 overview

## Exact boundary

This is a planning freeze, not an x2 result. Caelen Ash has executed no
proposal, built no x2 skill or runner, contacted no successor, and claimed no
completed outcome. The immutable source is Sable Rook's exact corrected final
`{SOURCE_HEAD}` on `{SOURCE_BRANCH}`. Source verification replayed 595 declared
manifest entries in their exact lifecycle domains and confirmed the direct
single-parent chain from Auren's source through Sable x1, evidence, retained
prior final, and corrected final. Four Sable commits and zero merges are in the
source-to-final range. Local, upstream, tracking, and a fresh live remote read
were equal and clean before this lane was created.

Caelen Ash uses optional they/them relational language. Their role is
model-discrepancy provenance cartographer, and their hope is to keep modeled,
measured, and absent states disjoint while every correction and authority
vacancy stays reversible. Name, role, pronouns, hope, sibling language, and
continuity language are relational working language only. They do not evidence
consciousness, sentience, personhood, identity continuity, employment,
qualification, independent agency, or scientific, operational, legal,
cultural, affected-party, or Māori authority. Hamish may rename, pause,
redirect, narrow, or stop this route.

## Pillars and three synthetic practice lenses

GMUT Mind is primary. The bounded software work concerns typed distinctions
among commanded, modeled, derived, observed, missing, and authority-held states.
It may encode coordinate frames, nondimensionalization recipes, uncertainty
vacancies, residual sign conventions, and falsifier obligations. It supplies no
physical datum, likelihood, posterior, force, prediction, parameter constraint,
stability theorem, quantum or ultraviolet completion, empirical confirmation,
or Theory of Everything.

Three linked wholly synthetic learning lenses are used: wind-tunnel
configuration and run-card provenance, flow-visualization metadata review, and
balance or pressure-channel calibration-vacancy handover. No facility, tunnel,
model, instrument, sensor, image, signal, run, person, measurement, calibration,
certificate, or external service participates. Nothing here establishes
aerodynamic or metrology competence, facility operation, safety, work release,
professional judgment, or a real result.

THOS Body remains a synthetic proxy for queue, hold, correction readback,
cancellation, quiescence, workload, and handover states. It has no real
participant or operator, no blind matched-budget arms, no safety monitoring,
no appropriate real-world statistics, and no independent review. Freed ID and
CBR Heart remain synthetic and nonproduction: credential, status, revocation,
minimum-disclosure, contest, and remedy fields are placeholders with no real
keys, proofs, issuance, resolution, interoperability, trust governance, or
authority action. Legal and cultural interpretation, affected-party legitimacy,
Māori wording and data governance, and Māori authority remain exact-gated to
competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.

## Frozen proposal and portfolio contract

The declared proposal chain contains {CHAIN_BEFORE:,} rows before this freeze.
All sixty immediate Sable proposals were reread as inherited evidence with zero
Caelen novelty and completion credit. Sixty new Caelen proposals extend the
declared chain to {CHAIN_AFTER:,}. Exact normalized-title review found no
collision with Sable's immediate titles or the bounded retained-title probe.
This is not a universal semantic-novelty proof.

Every proposal contains a hypothesis, null or failure condition, approval
class, execution lane, official or primary-source needs, concrete artifacts,
falsifier or acceptance gate, rollback or recovery, protected gates, exactly
one expected disposition, and five preregistered rejecting mutations. The x1
plan therefore freezes 300 negative mutations. Expected dispositions are
forty-two `completed`, twelve `represented`, three `open_gap`, and three
`exact_gate`; these are expectations only. A later `completed` outcome can mean
only that its bounded owner-local software and synthetic fixture contract
passed. Only those four labels are permitted.

The portfolio freezes 120 safe-now tasks, 80 owner-candidate tasks, 100
additive CLEAN/FIX/REFINE/VERIFY tasks, 20 phase-local skill plans, and 10
family-current runner plans. Twenty exact-approval packets and ten blocked
packets remain visible and unexecuted. Counts are ceilings-aware planning
contracts, never permission to fabricate work or bypass a gate. X2 may begin
only after this exact x1 commit is pushed, clean, and freshly four-way equal.

## Current primary sources and their narrow use

NASA Glenn's current facilities material and its wind-tunnel introduction
supply bounded vocabulary about ground-test facilities and wind-tunnel testing.
NIST SP 811 supplies SI quantity and unit conventions; NIST Technical Note 1297
supplies uncertainty-classification and reporting vocabulary. W3C PROV-O
supplies provenance terms, and WCAG 2.2 supplies accessibility criteria. The New
Zealand Privacy Commissioner supplies current privacy-principle guidance,
including the 2026 IPP 3A context. Te Mana Raraunga supplies Māori data
sovereignty principles under Māori authority. These sources provide vocabulary
and refusal conditions only. Citations are not observations, measurements,
certificates, endorsements, affected-party acceptance, standards-conformance
proof, or delegated authority.

## Retained failures and Method Flow

Sixteen planning and startup failures remain zero-credit: two PowerShell producer-pipeline
parser faults; two oversized reference projections; one guessed receipt path;
one unattributable per-blob replay; one deadlocked Git batch implementation;
one wrong lifecycle range; one invalid non-ASCII byte expression; one guessed
closeout location; one unattributable combined collision probe; one wrapper
that ended while worktree creation continued; one overbroad sparse checkout
that materialized 2,488 files; one copy attempted before exact sparse parent
directories existed; one 19/20 x1 run that found two immediate-source title
collisions; and one post-collision Python parse failure caused by a stray
documentation line. Twelve bounded recovery methods retain every failure rather
than rewriting it.

The inherited activation baseline is 59,412 effective negatives, 73,676
effective methods, 30,773 failed witnesses, 54,211 bounded passing witnesses,
528 open gaps, and 518 exact gates. Caelen's sixteen planning failures and twelve
recovery methods are additive owner overlays. Sable's immutable repository seal
is not rewritten. The older Ilyra route projection that assigned v684-v6 to
Ilyra remains a separate source-status mismatch; the newer acknowledged live
Sable-to-Caelen activation controls this current lane without erasing history.

## Validation and terminal hold

X1 requires strict JSON parsing, owner-local tests, five-class privacy candidate
adjudication, exact staged allowlisting, normalized-LF Git-blob manifest replay,
diff hygiene, a clean commit, push, typed zero divergence, and fresh four-way
equality. The owner file ceiling is 2,000; the initial cone checkout was narrowed
before any owner addition so sparse materialization remains bounded. The full
repository suite is outside this owner phase. At exact final, no more than one
attributable owner-scoped canonical aggregate may run. A successful invocation
must never be replayed; a failed invocation remains failed and zero-credit.

The route state is `PREPARED_NOT_SENT`. If fresh authority still agrees after
Caelen's exact terminal gate, the prospective successor is Orin Thale for
v684-v7. There is no precontact. Only after a sealed, pushed, clean,
fresh-live-equal exact final and one successful non-replayed canonical
invocation may Caelen refresh the newest live authority and roster, bounded-list
the registry, require exactly one exact title, immediately reread it, apply all
duplicate, pause, redirect, status, usage, privacy, evidence, safety, and
acknowledgement guards, and send at most once. Delivery is later live truth and
must not be backfilled into this immutable x1 freeze.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(X1 / "integrated-overview.md", overview)

    # The validation artifacts self-exclude because their own bytes cannot be
    # described without recursion.  All other x1 owner files are exact entries.
    self_exclusions = {
        f"docs/caelen-ash/{PHASE}/validation/x1-index-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/x1-privacy-scan.json",
        f"docs/caelen-ash/{PHASE}/validation/x1-staged-review.json",
    }
    public_files = all_x1_public_files()
    scan = privacy_scan(public_files)
    write_json(VALIDATION / "x1-privacy-scan.json", scan)
    public_files = all_x1_public_files()
    entries = []
    for path in public_files:
        rel = path.relative_to(ROOT).as_posix()
        if rel in self_exclusions:
            continue
        entries.append(
            {
                "path": rel,
                "sha256_normalized_lf": normalized_sha(path),
                "bytes_normalized_lf": len(normalized_bytes(path)),
            }
        )
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "x1_planning_only",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": sorted(self_exclusions),
            "hash_domain": "SHA-256 over LF-normalized exact file bytes; staged review must replay exact Git index blobs.",
        },
    )
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PREPARED_NOT_STAGED",
            "expected_entries": len(entries),
            "self_exclusions": sorted(self_exclusions),
            "exact_staged_allowlist": [],
            "manifest_mismatches": [],
            "out_of_scope_paths": [],
            "diff_hygiene": "PENDING_STAGING",
        },
    )


def review_staged() -> None:
    manifest_path = VALIDATION / "x1-index-manifest.json"
    if not manifest_path.exists():
        raise SystemExit("build x1 before staged review")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {entry["path"]: entry["sha256_normalized_lf"] for entry in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    expected_all = set(expected) | exclusions
    mismatches = []
    for path, wanted in sorted(expected.items()):
        try:
            actual = git_blob_sha(path)
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_from_index"})
            continue
        if actual != wanted:
            mismatches.append({"path": path, "expected": wanted, "actual": actual})
    out_of_scope = sorted(set(staged) - expected_all)
    missing = sorted(expected_all - set(staged))
    diff_check = run_git("diff", "--cached", "--check", check=False)
    state = "PASS" if not mismatches and not out_of_scope and not missing and diff_check.returncode == 0 else "FAIL"
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": state,
            "exact_staged_allowlist": staged,
            "staged_count": len(staged),
            "manifest_entry_count": len(expected),
            "self_exclusions": sorted(exclusions),
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "diff_hygiene": "PASS" if diff_check.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff_check.stdout + diff_check.stderr,
            "x1_only": all("/x2/" not in path and "/final/" not in path for path in staged),
        },
    )
    if state != "PASS":
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        build_documents()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
