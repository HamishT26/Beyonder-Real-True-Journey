#!/usr/bin/env python3
"""Build the planning-only Sable Rook v684-v5 x1 freeze.

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
PHASE = "v684-v5"
OWNER = "Sable Rook"
BASE = ROOT / "docs" / "sable-rook" / PHASE
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
SOURCE_HEAD = "73321b3ff077c3f33726562b8e9d5952608a060e"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v684-v4-remaster"
ILYRA_SOURCE = "0134e277a7f573e24e697037749d61d577163637"
AUREN_X1 = "d1ea9dba1fab7d6726f11a15caf67a8531b70e4a"
AUREN_EVIDENCE = "c41a5453dce2202324235bdcd820f52e846d834d"
FAILED_PREDECESSOR = "0b3a872d1c08a99cc7bc647944ef37e1d4010158"
BRANCH = "codex/GHC-Family/sable-rook-v684-v5-full-tools"
CHAIN_BEFORE = 10_910
CHAIN_AFTER = 10_970

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
    "cci_monitoring": "https://www.canada.ca/en/conservation-institute/services/agents-deterioration/humidity/video-monitoring-your-environment.html",
    "cci_climate": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/climate-guidelines/climate-guidelines-overview.html",
    "cci_humidity": "https://www.canada.ca/en/conservation-institute/services/agents-deterioration/humidity.html",
    "nps_museum": "https://www.nps.gov/subjects/museums/index.htm",
    "prov_o": "https://www.w3.org/TR/prov-o/",
    "wcag_22": "https://www.w3.org/TR/wcag/",
    "nz_privacy": "https://www.privacy.org.nz/privacy-principles/",
    "te_mana_raraunga": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
}

TOPICS = [
    "Synthetic sensor registry with every physical device absent",
    "Logger serial surrogate with no hardware identity claim",
    "Zone label vocabulary with every real location absent",
    "Temperature unit declaration without a measurement",
    "Relative-humidity unit declaration without a measurement",
    "Illuminance vocabulary without a lux reading",
    "Ultraviolet proxy vocabulary without a radiation reading",
    "Sampling-interval declaration without observed timestamps",
    "Clock timezone and calendar policy without real events",
    "Clock-drift uncertainty vacancy and refusal state",
    "Calibration-status vacancy without traceability promotion",
    "Calibration due-date hold without service authority",
    "Battery and service-state record without maintenance action",
    "Firmware and acquisition-software provenance without a device",
    "Acquisition-file format declaration without ingestion",
    "Checksum and fixity custody without authenticity promotion",
    "Import provenance contract with zero imported rows",
    "Gap and outage reason taxonomy without an incident claim",
    "Missing sample versus numeric zero separation",
    "Duplicate synthetic record quarantine without deletion",
    "Late-arrival correction lineage without a live stream",
    "Supersession and revision DAG without history erasure",
    "Annotation-agent vacancy without identity attribution",
    "Maintenance-event note boundary without real intervention",
    "Power-failure note boundary without a facility incident",
    "Sensor-relocation hold without a location decision",
    "Storage-zone versus display-zone semantic separation",
    "Enclosure and microclimate boundary without object custody",
    "External-weather covariate vacancy without data download",
    "HVAC-event correlation nonclaim and causal firewall",
    "Threshold-version provenance without conservation policy",
    "Threshold-exceedance class without an operational alert",
    "Persistence and duration rule without observed values",
    "Rolling-window definition without empirical calculation",
    "Aggregation-method provenance without aggregation",
    "Raw-field versus derived-field type separation",
    "Outlier annotation without deletion or data repair",
    "Censoring and detection-limit vacancy without imputation",
    "Uncertainty-component registry without a numerical budget",
    "Seasonal-baseline nonclaim and drift firewall",
    "Cumulative-light-dose formula with no exposure result",
    "Risk-decision nonpromotion board without collection authority",
    "THOS handover-state proxy for a synthetic monitoring queue",
    "THOS correction-readback proxy with no real operator",
    "THOS workload-budget proxy with no service-effect claim",
    "Freed ID synthetic logger-credential placeholder",
    "Freed ID synthetic status and revocation placeholder",
    "CBR minimum-disclosure profile with no personal record",
    "CBR access-request contest path without legal adjudication",
    "CBR remedy and appeal vacancy without beneficiary authority",
    "Accessible data-table alternative structural contract",
    "Plain-language anomaly-summary structural contract",
    "Non-colour-only status encoding structural contract",
    "Keyboard focus-order and reading-order structural plan",
    "Real environmental-monitoring dataset evidence vacancy",
    "Independent conservator review evidence vacancy",
    "Affected-user accessibility evaluation evidence vacancy",
    "Collection intervention and treatment authority gate",
    "Legal cultural and Māori authority decision gate",
    "Production deployment proof-canon and Stage 20 gate",
]

SKILL_SLUGS = [
    "synthetic-sensor-registry-guard",
    "measurement-absence-firewall",
    "unit-vocabulary-custodian",
    "clock-uncertainty-vacancy",
    "calibration-traceability-hold",
    "zero-row-import-refusal",
    "missing-versus-zero-separator",
    "duplicate-record-quarantine",
    "correction-dag-nonerasure",
    "threshold-version-provenance",
    "causal-correlation-nonpromotion",
    "uncertainty-budget-vacancy",
    "thos-handover-proxy",
    "freed-id-nonproduction-hold",
    "cbr-minimum-disclosure-boundary",
    "accessibility-structural-reservation",
    "maori-authority-exact-gate",
    "retained-failure-nonerasure",
    "four-label-outcome-linter",
    "stage20-nonpromotion-latch",
]

RUNNER_NAMES = [
    "ghc_family_synthetic_sensor_registry_runner.py",
    "ghc_family_measurement_absence_runner.py",
    "ghc_family_unit_and_clock_runner.py",
    "ghc_family_zero_row_import_runner.py",
    "ghc_family_correction_lineage_runner.py",
    "ghc_family_threshold_nonpromotion_runner.py",
    "ghc_family_thos_handover_proxy_runner.py",
    "ghc_family_identity_privacy_hold_runner.py",
    "ghc_family_accessibility_reservation_runner.py",
    "ghc_family_stage20_gate_runner.py",
]

STARTUP_FAILURES = [
    {
        "failure_id": "SR6845-SF001",
        "summary": "A PowerShell inventory wrapper piped directly from a foreach statement and failed to parse before evidence collection.",
        "recovery": "Materialize the foreach output as an array before piping or projection.",
    },
    {
        "failure_id": "SR6845-SF002",
        "summary": "A combined authorization-state display exceeded its bounded output projection.",
        "recovery": "Read the exact current-state document through EOF in bounded numbered windows.",
    },
    {
        "failure_id": "SR6845-SF003",
        "summary": "A predecessor-existence and ancestry wrapper stopped after the expected nonzero ancestry result.",
        "recovery": "Compare the scalar merge base with immutable evidence and retain the nonancestral predecessor truth separately.",
    },
    {
        "failure_id": "SR6845-SF004",
        "summary": "A branch-collision preflight embedded native command state inside a PowerShell expression and failed to parse.",
        "recovery": "Run literal path, local-ref, and remote-ref probes as separate scalar commands.",
    },
    {
        "failure_id": "SR6845-SF005",
        "summary": "The corrected combined collision wrapper returned no attributable output.",
        "recovery": "Use three exact bounded probes and require all three to show absence before lane creation.",
    },
    {
        "failure_id": "SR6845-SF006",
        "summary": "Sparse initialization and checkout crossed the wrapper output boundary while Git processes were still active.",
        "recovery": "Inspect the exact worktree lock and process state, wait without replay, then verify persisted patterns, head, branch, and clean state.",
    },
    {
        "failure_id": "SR6845-SF007",
        "summary": "A combined Git configuration probe produced an unusable truncated projection.",
        "recovery": "Read each configuration scalar separately and prove staged content from exact index blobs instead of inference.",
    },
    {
        "failure_id": "SR6845-SF008",
        "summary": "The first workflow-plan refinement request used an unsupported cross-platform messaging value and failed one structural policy check.",
        "recovery": "Retain the failed output and use the schema's exact user-mediated-file-relay-only value while keeping direct cross-platform execution unauthorized.",
    },
    {
        "failure_id": "SR6845-SF009",
        "summary": "The first reflection-remaster audit passed a comma-joined focus value to an append-style argument and produced a zero-surface audit.",
        "recovery": "Retain the unscoped receipt and pass each focus term with its own repeated argument.",
    },
]

RECOVERY_METHODS = [
    {
        "method_id": "SR6845-M001",
        "trigger": "PowerShell foreach output must feed another command",
        "method": "Materialize producer output before piping.",
        "failed_witnesses": ["SR6845-SF001"],
    },
    {
        "method_id": "SR6845-M002",
        "trigger": "A required document exceeds one display projection",
        "method": "Read deterministic numbered windows through EOF.",
        "failed_witnesses": ["SR6845-SF002"],
    },
    {
        "method_id": "SR6845-M003",
        "trigger": "An expected nonzero native status is evidence rather than wrapper failure",
        "method": "Separate native scalars and compare the exact merge base.",
        "failed_witnesses": ["SR6845-SF003"],
    },
    {
        "method_id": "SR6845-M004",
        "trigger": "Lane collision or long sparse checkout preflight",
        "method": "Use literal scalar probes; on wrapper timeout inspect persisted locks, processes, refs, patterns, and clean state before any retry.",
        "failed_witnesses": ["SR6845-SF004", "SR6845-SF005", "SR6845-SF006"],
    },
    {
        "method_id": "SR6845-M005",
        "trigger": "Git configuration or newline behavior must be established",
        "method": "Read one config scalar at a time and validate exact staged Git blobs.",
        "failed_witnesses": ["SR6845-SF007"],
    },
    {
        "method_id": "SR6845-M006",
        "trigger": "Workflow-plan policy values are machine validated",
        "method": "Retain the failed refinement packet, use the exact schema vocabulary, and rerun only the corrected sanitized request.",
        "failed_witnesses": ["SR6845-SF008"],
    },
    {
        "method_id": "SR6845-M007",
        "trigger": "A command-line option uses append semantics",
        "method": "Inspect the installed argument definition and repeat the option once per exact focus term.",
        "failed_witnesses": ["SR6845-SF009"],
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
    keys = ["cci_monitoring", "cci_climate", "prov_o"]
    if 4 <= index <= 42:
        keys.append("cci_humidity")
    if 43 <= index <= 50:
        keys.extend(["nz_privacy", "te_mana_raraunga"])
    if 51 <= index <= 57:
        keys.append("wcag_22")
    if index >= 58:
        keys.extend(["nps_museum", "te_mana_raraunga"])
    return list(dict.fromkeys(SOURCE_URLS[key] for key in keys))


def proposal(index: int, title: str) -> dict[str, Any]:
    proposal_id = f"SR6845-N{index:03d}"
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
            f"docs/sable-rook/{PHASE}/x2/proposals/{proposal_id.lower()}-{slug(title)}.json",
            f"docs/sable-rook/{PHASE}/x2/witnesses/{proposal_id.lower()}-witness.json",
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
        "primary_pillar": "THOS Body",
        "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "practice_lens": "synthetic museum environmental-monitoring data documentation analyst",
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


def inherited_auren_titles() -> list[str]:
    raw = run_git(
        "show",
        f"{SOURCE_HEAD}:docs/auren-lark/v684-v4/x1/new-proposal-freeze.json",
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
            "also compared all sixty immediate Auren titles; no universal novelty claim is made."
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
            if rel.startswith(f"docs/sable-rook/{PHASE}/"):
                paths.append(path)
            elif rel in {
                "scripts/build_ghc_family_sable_rook_v684_v5_x1.py",
                "tests/test_ghc_family_sable_rook_v684_v5_x1.py",
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
                    "build_ghc_family_sable_rook_v684_v5_x1.py"
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
        "plan_id": "sable-rook-v684-v5-live-corrected-plan",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no consciousness, continuity, qualification, or authority claim.",
        "route": {
            "cycle_order": ["Auren Lark", "Sable Rook", "Caelen Ash"],
            "endpoint_topology": [
                {
                    "seat": "Auren Lark",
                    "endpoint_kind": "main_task",
                    "endpoint_label": "Auren Lark",
                    "route_controller": "Ilyra Fen",
                },
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
            ],
            "phase_assignments": [
                {"phase": "v684-v4", "seat": "Auren Lark"},
                {"phase": PHASE, "seat": "Sable Rook"},
                {"phase": "v684-v6", "seat": "Caelen Ash"},
            ],
            "normalization": {
                "start_phase": "v684-v4",
                "start_seat": "Auren Lark",
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
    auren_titles = inherited_auren_titles()
    auren_normalized = {re.sub(r"\W+", " ", title.casefold()).strip() for title in auren_titles}
    exact_auren_collisions = [
        item["title"]
        for item in proposals
        if re.sub(r"\W+", " ", item["title"].casefold()).strip() in auren_normalized
    ]
    title_probe = retained_title_probe()

    write_json(
        X1 / "activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v2",
            "phase": PHASE,
            "owner": OWNER,
            "activation_state": "ACKNOWLEDGED_EXISTING_TASK_ACTIVATION",
            "source_owner": "Auren Lark",
            "live_corrected_edge": "Auren Lark to Sable Rook",
            "prospective_successor": "Caelen Ash",
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
            "relational_role": "Loan-Lineage Cartographer and Reversible Handover Steward",
            "hope": "Keep every synthetic transition, correction, and authority vacancy traceable without mistaking software for real work or authority.",
            "primary_pillar": "THOS Body",
            "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "practice_lens": "synthetic museum environmental-monitoring data documentation analyst",
            "practice_boundary": "Learning and owner-local design only; no employment, qualification, conservation competence, custody, intervention authority, legal or cultural authority, Māori authority, affected-party approval, empirical result, or production result.",
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
                "ilyra_source": ILYRA_SOURCE,
                "auren_x1": AUREN_X1,
                "auren_evidence": AUREN_EVIDENCE,
                "auren_exact_final": SOURCE_HEAD,
                "failed_predecessor_retained_not_ancestral": FAILED_PREDECESSOR,
            },
            "verified_before_mutation": {
                "direct_single_parent_chain": True,
                "phase_commits": 3,
                "merge_commits": 0,
                "final_parent_is_evidence": True,
                "clean": True,
                "typed_divergence": {"ahead": 0, "behind": 0},
                "local_upstream_tracking_fresh_live_equal": True,
                "manifest_entries_replayed": 249,
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
            "current_edge": "Auren Lark to Sable Rook",
            "historical_conflicts": [
                "The committed Auren candidate retained an unresolved historical Liora assignment.",
                "The current acknowledged live activation explicitly corrects the edge to Auren Lark to Sable Rook.",
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
            "next_title_if_fresh_terminal_authority_still_matches": "Caelen Ash",
            "next_phase_if_fresh_terminal_authority_still_matches": "v684-v6",
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
            "inherited_auren_proposals_revalidated": 60,
            "inherited_novelty_credit": 0,
            "new_sable_proposals": 60,
            "exact_collision_with_immediate_auren_titles": exact_auren_collisions,
            "retained_artifact_title_probe": title_probe,
            "universal_novelty_claim": False,
            "audit_truth": "Distinctness is a bounded title and semantic-surface review, not proof against every conceivable future wording.",
        },
    )
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "schema": "ghc.family.inherited-revalidation-freeze.v2",
            "source": "docs/auren-lark/v684-v4/x1/new-proposal-freeze.json",
            "count": len(auren_titles),
            "entries": [
                {
                    "source_proposal_id": f"AL6844-N{index:03d}",
                    "title": title,
                    "review_state": "revalidated_as_inherited_evidence",
                    "sable_novelty_credit": 0,
                    "sable_completion_credit": 0,
                }
                for index, title in enumerate(auren_titles, start=1)
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
            "candidate_id": f"SR6845-C{index:03d}",
            "proposal_id": f"SR6845-N{((index - 1) % 60) + 1:03d}",
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
            "packet_id": f"SR6845-EXACT-{index:02d}",
            "surface": surface,
            "state": "HELD_UNEXECUTED",
            "gate": "exact competent and affected authority plus exact evidence",
        }
        for index, surface in enumerate(
            [
                "real museum environmental data ingestion",
                "collection intervention decision",
                "environmental threshold policy",
                "facility control or alert",
                "staff workload or safety decision",
                "personal or visitor information use",
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
            "packet_id": f"SR6845-BLOCKED-{index:02d}",
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
                    "skill_id": f"SR6845-SK{index:02d}",
                    "slug": value,
                    "state": "PLANNED_NOT_BUILT",
                    "required_x2_evidence": ["quick validation", "smoke use", "owner-local only"],
                }
                for index, value in enumerate(SKILL_SLUGS, start=1)
            ],
            "runners": [
                {
                    "runner_id": f"SR6845-R{index:02d}",
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
            "task_id": f"SR6845-CFR-{index:03d}",
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
                    "status": "current_read_live" if key in {"cci_monitoring", "cci_climate", "nps_museum", "nz_privacy", "te_mana_raraunga"} else "stable_primary_reference_read_live",
                    "permitted_use": "Vocabulary, provenance duties, accessibility criteria, privacy principles, and refusal conditions only.",
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
            "practice": "synthetic museum environmental-monitoring data documentation analyst",
            "independent_review_state": "independently_selected_after_source_review",
            "inherited_recommendation_credit": 0,
            "learning_surfaces": [
                "instrument and zone metadata",
                "sampling and clock declarations",
                "gap, correction, supersession, and handover lineage",
                "threshold and uncertainty documentation",
                "accessible structural alternatives",
            ],
            "explicit_nonclaims": [
                "employment or qualification",
                "collection custody or conservation competence",
                "real measurement or calibration",
                "intervention, treatment, facility, alert, or safety authority",
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
                "threshold vocabulary mistaken for policy",
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
            "hope": "Keep synthetic work legible and reversible while every real-world authority vacancy remains unmistakable.",
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "schema": "ghc.family.method-flow-startup.v2",
            "activation_overlay_before_sable_startup": {
                "effective_negatives": 59094,
                "effective_methods": 73664,
                "failed_witnesses": 30755,
                "bounded_passing_witnesses": 54199,
            },
            "startup_failures": STARTUP_FAILURES,
            "recovery_methods": RECOVERY_METHODS,
            "derived_after_startup": {
                "effective_negatives": 59094 + len(STARTUP_FAILURES),
                "effective_methods": 73664 + len(RECOVERY_METHODS),
                "failed_witnesses": 30755 + len(STARTUP_FAILURES),
                "bounded_passing_witnesses": 54199 + len(RECOVERY_METHODS),
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
                "scope_boundary": "Sable-owned startup and x1 workflow only; no repository-wide, sibling, scientific, authority, or production claim.",
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
                    "scope": "Sanitized Sable-owned startup preflight.",
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
                "scope": "The exact bounded Sable-owned startup surface named by the trigger.",
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
                "negatives": 59094,
                "methods": 73664,
                "failed_witnesses": 30755,
                "passing_witnesses": 54199,
                "open_gaps": 525,
                "exact_gates": 515,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    overview = f"""# Sable Rook {PHASE} planning-only x1 overview

## Outcome at this boundary

This packet freezes the plan and nothing more. Sable Rook has not executed an x2
proposal, claimed a completed outcome, contacted a successor, or converted any
inherited evidence into owner credit. The immutable source is Auren Lark's
corrected remaster final `{SOURCE_HEAD}` on `{SOURCE_BRANCH}`. The exact Ilyra,
Auren x1, Auren evidence, and corrected-final ancestry was checked before this
lane was created. The failed predecessor final remains retained on its original
history and is not silently made ancestral.

The current owner is Sable Rook, using they/them in relational working language.
Their relational role is Loan-Lineage Cartographer and Reversible Handover
Steward. Their hope is to keep every synthetic transition, correction, and
authority vacancy traceable without mistaking software for real work or
authority. These words do not establish consciousness, personhood, continuity,
employment, qualification, independent agency, or any scientific, operational,
legal, cultural, affected-party, or Māori authority.

## Pillars and bounded learning practice

THOS Body is the primary pillar for this phase. It is represented through
synthetic queue, correction, readback, workload, exception, and handover states.
No real operator, museum, collection, object, logger, facility, measurement,
alarm, intervention, or service outcome is present. GMUT Mind remains explicit
as a typed scalar-tensor and effective-field-theory research-model family, with
analogy firewalls that refuse to turn metadata or thermodynamic vocabulary into
physical prediction, empirical confirmation, psyche, agency, consciousness,
personhood, or a Theory of Everything. Freed ID and CBR Heart remain explicit as
synthetic minimum-disclosure, contest, correction, status-vacancy, remedy, and
authority-hold structures. They are not production identity systems or public
authority.

The independently selected bounded practice is synthetic museum
environmental-monitoring data documentation analysis. The phase may model
instrument metadata, zones, units, sampling declarations, clock uncertainty,
calibration vacancies, gap classifications, correction lineage, threshold
versioning, accessible alternatives, and shift handover. It may not infer a real
reading, condition, risk, treatment, environmental policy, alert, facility
decision, conservation judgment, collection custody, or professional
competence. Cultural meaning, legal interpretation, affected-party legitimacy,
Māori wording, and Māori data governance remain with competent and affected
people and authorities.

## Frozen proposals and novelty boundary

The declared proposal chain contains {CHAIN_BEFORE:,} rows before this freeze.
Sixty immediate Auren proposals were re-read and retained as inherited evidence
with zero Sable novelty and zero Sable completion credit. Sixty Sable proposals
are frozen here, taking the declared chain to {CHAIN_AFTER:,}. Each proposal
records a bounded hypothesis, null or failure condition, approval class,
execution lane, current official or primary-source needs, concrete future
artifacts, acceptance or falsifier gate, rollback, protected gates, expected
disposition, and five invalid mutations. The plan therefore preregisters three
hundred rejecting mutations.

The expected disposition distribution is forty-two `completed`, twelve
`represented`, three `open_gap`, and three `exact_gate`. Those are planning
expectations, not observed x2 outcomes. Only these four labels are allowed. A
later `completed` label can mean only that the declared owner-local software,
schema, documentation, or synthetic fixture gate passed. It cannot mean the
real-world claim is complete. An admitted invalid mutation, erased failure,
missing required artifact, or promoted authority claim falsifies the bounded
contract and must be retained without compensating credit.

The exact-title probe covers retained proposal artifacts available at the
immutable source, and an immediate semantic review covers all sixty Auren
titles. No universal semantic-novelty claim is made. Distinctness here means the
new Sable surfaces are documented as different from the retained named
neighbors reviewed; it does not prove that no conceivable historical wording
or future idea overlaps.

## Portfolios, skills, and runners

The x1 packet freezes one hundred twenty safe-now tasks, eighty owner candidate
tasks, one hundred additive CLEAN/FIX/REFINE/VERIFY tasks, twenty phase-local
skill plans, and ten family-current runner plans. Numeric values are bounded
plans under the live ceilings, never authority to manufacture unsafe work.
Twenty exact-approval packets and ten blocked packets are separately visible and
unexecuted. Any task that encounters real data, participants, professional
practice, production identity, secrets, accounts, host security, destructive
cleanup, sibling state, law, culture, Māori authority, or affected-party
legitimacy must stay held or be reclassified; it cannot be smuggled through the
safe-now portfolio.

The phase-local skills and runners do not yet exist. X2 must build them only
after this x1 commit is pushed and freshly four-way equal. Each skill must have
substantive instructions, agent metadata, quick validation, and an actual
owner-local smoke-use receipt. Each runner must retain family-current
`ghc_family_*` naming, be invoked, and produce a bounded witness. No global
installation or shared-skill mutation is authorized.

## Source and evidence discipline

Current official and primary sources were consulted only for vocabulary and
refusal duties. Canadian Conservation Institute material supports the idea that
environmental monitoring requires deliberate instrument placement, collection,
processing, and interpretation of data, while its climate guidance emphasizes
collection-specific context rather than a universal threshold. NPS museum
materials identify official museum program guidance. W3C PROV-O supplies a
machine-readable provenance vocabulary, WCAG 2.2 supplies accessibility
criteria, the New Zealand Privacy Commissioner supplies privacy principles, and
Te Mana Raraunga supplies Māori data-sovereignty principles. Citations are not
observations, measurements, reviews, affected-party consent, delegated
authority, or production certification.

This planning packet contains zero real environmental rows, zero likelihood
evaluations, zero real participants or operators, zero real collection objects,
zero real keys or proofs, zero live identity events, and zero authority
decisions. THOS therefore remains synthetic and proxy-only. Freed ID remains
synthetic and nonproduction. GMUT remains a research-model family with every
empirical gate open. CBR and all legal, cultural, privacy-remedy,
affected-party, and Māori-authority surfaces remain exact-gated.

## Method Flow and retained failures

Seven Sable startup failures are retained at zero credit: a PowerShell producer
pipeline parse fault, an oversized authorization display, an expected-nonzero
ancestry wrapper, a branch-probe parse fault, an unattributable combined
collision wrapper, a sparse-checkout wrapper that crossed its output boundary
while Git still ran, and an unusable combined Git-configuration projection.
Five recovery methods use producer materialization, bounded window reads,
scalar native probes, persisted lock/process/ref inspection, and exact staged
Git-blob validation. A passing recovery never rewrites its paired failure.

The activation overlay before these startup events is 59,094 effective
negatives, 73,664 effective methods, 30,755 retained failed witnesses, and
54,199 bounded passing witnesses. Adding the seven failures and five recovery
methods yields the truthful current planning view recorded in the startup
ledger. Auren's repository seal remains unchanged; external route and Sable
startup facts are additive overlays only.

## Validation and route hold

X1 must undergo exact staged review, strict JSON parsing, five-class privacy
candidate adjudication, normalized-LF manifest construction, diff hygiene,
planning-only tests, clean state, and exact commit review. It must then be
committed and pushed. Local, upstream, tracking, and a fresh live remote read
must all equal the immutable x1 commit before any x2 path is created. The 2,000
owner-file ceiling, document cap, and commit budgets are ceilings rather than
targets.

The full repository suite is not authorized for this non-Eiren phase. At exact
final, one dependency-closed owner-scoped canonical aggregate may run once. If
it succeeds, it must not be replayed. Same-owner validation under shared
infrastructure is not independent reproduction, external audit, production
certification, exhaustive security, complete privacy, complete accessibility,
professional validation, legal review, cultural ratification, or Māori-authority
review.

The route state is `PREPARED_NOT_SENT`. Caelen Ash is only a prospective exact
title recorded from the live correction. Sable must not precontact it. Only
after a sealed, pushed, clean, fresh-live-equal exact final and one successful
non-replayed canonical invocation may Sable refresh the newest live authority,
bounded task registry, and immediate target state. Absence, ambiguity, pause,
redirect, rename, usage exhaustion, privacy or safety concern, protected gate,
or missing acknowledgement requires a stop. A successful acknowledged send is
a later live event and may never be backfilled into this x1 freeze.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(X1 / "integrated-overview.md", overview)

    # The validation artifacts self-exclude because their own bytes cannot be
    # described without recursion.  All other x1 owner files are exact entries.
    self_exclusions = {
        f"docs/sable-rook/{PHASE}/validation/x1-index-manifest.json",
        f"docs/sable-rook/{PHASE}/validation/x1-privacy-scan.json",
        f"docs/sable-rook/{PHASE}/validation/x1-staged-review.json",
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
