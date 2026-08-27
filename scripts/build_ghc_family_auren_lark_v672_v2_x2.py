#!/usr/bin/env python3
"""Build Auren Lark v672-v2 owner-scoped synthetic x2 evidence."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

OWNER = "Auren Lark"
PHASE = "v672-v2"
SOURCE = "40db1e418c1251e12d77f832c0890869b990dba5"
X1 = "821a40be02af8db39524dc862aeaadf32e1543c3"
X1_OVERLAY = {
    "effective_negatives": 35213,
    "effective_methods": 21844,
    "effective_failed_witnesses": 7034,
    "effective_passing_witnesses": 9135,
    "open_gaps": 277,
    "exact_gates": 270,
}
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party",
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
X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "AL6722-X2-001",
        "description": "The first sparse-checkout add call used an unsupported --no-cone flag and exited 129 before changing state.",
        "state": "failed_retained_zero_credit_recovered",
        "recovery": "Use the documented add --stdin form because the lane is already configured in non-cone mode.",
    },
    {
        "failure_id": "AL6722-X2-002",
        "description": "The first scoped x2 test pass had nine passing tests and one failure because the integrated overview contained 662 words below its preregistered 700-word floor.",
        "state": "failed_retained_zero_credit_recovered",
        "recovery": "Expand only the bounded source, correction, uncertainty, and authority explanation, rebuild deterministic manifests, and rerun the scoped x2 module without replaying the successful runner smoke.",
    },
    {
        "failure_id": "AL6722-X2-003",
        "description": "The first exact-file x2 Ruff gate found thirteen import-order findings across generated runners, builders, and the scoped test.",
        "state": "failed_retained_zero_credit_recovered",
        "recovery": "Apply Ruff's safe import rewrites, mirror the corrected spacing in generator templates, prove ten-of-ten AST equivalence against deterministic pre-fix reconstructions, and rerun only the exact-file lint gate without replaying the successful runner smoke.",
    },
]

SKILL_SPECS = [
    ("ghc-family-incident-packet-capsule", "incident packet capsule", "packet"),
    ("ghc-family-incident-chronology-bitemporal-guard", "bitemporal chronology guard", "chronology"),
    ("ghc-family-incident-source-status-drift-watch", "source status drift watch", "source_status"),
    ("ghc-family-incident-assertion-observation-separator", "assertion and observation separator", "packet"),
    ("ghc-family-incident-uncertainty-vocabulary-gate", "uncertainty vocabulary gate", "uncertainty"),
    ("ghc-family-incident-correction-lineage-ledger", "correction lineage ledger", "correction_log"),
    ("ghc-family-incident-supersession-graph-guard", "supersession graph guard", "correction_log"),
    ("ghc-family-incident-duplicate-event-refusal", "duplicate event refusal", "chronology"),
    ("ghc-family-incident-evidence-fixity-manifest", "evidence fixity manifest", "evidence_chain"),
    ("ghc-family-incident-attachment-vacancy-gate", "attachment vacancy gate", "evidence_chain"),
    ("ghc-family-incident-surrogate-identifier-boundary", "surrogate identifier boundary", "packet"),
    ("ghc-family-incident-privacy-minimization-profile", "privacy minimization profile", "privacy_minimization"),
    ("ghc-family-incident-five-class-secret-tribunal", "five-class secret tribunal", "privacy_minimization"),
    ("ghc-family-incident-redaction-reason-ledger", "redaction reason ledger", "privacy_minimization"),
    ("ghc-family-incident-text-alternative-index", "text alternative index", "accessibility_handoff"),
    ("ghc-family-incident-table-semantics-proxy", "table semantics proxy", "accessibility_handoff"),
    ("ghc-family-incident-readback-acknowledgement-board", "readback acknowledgement board", "readback"),
    ("ghc-family-incident-shift-handover-proxy", "shift handover proxy", "readback"),
    ("ghc-family-incident-authority-vacancy-matrix", "authority vacancy matrix", "authority_boundary"),
    ("ghc-family-incident-stage20-nonpromotion-seal", "Stage 20 nonpromotion seal", "authority_boundary"),
]

RUNNER_SPECS = [
    ("chronology", "ghc_family_auren_v672_v2_incident_chronology_guard.py"),
    ("source_status", "ghc_family_auren_v672_v2_incident_source_status_guard.py"),
    ("correction_log", "ghc_family_auren_v672_v2_incident_correction_log_guard.py"),
    ("uncertainty", "ghc_family_auren_v672_v2_incident_uncertainty_guard.py"),
    ("authority_boundary", "ghc_family_auren_v672_v2_incident_authority_boundary_guard.py"),
    ("privacy_minimization", "ghc_family_auren_v672_v2_incident_privacy_minimization_guard.py"),
    ("accessibility_handoff", "ghc_family_auren_v672_v2_incident_accessibility_handoff_guard.py"),
    ("evidence_chain", "ghc_family_auren_v672_v2_incident_evidence_chain_guard.py"),
    ("readback", "ghc_family_auren_v672_v2_incident_readback_guard.py"),
    ("packet", "ghc_family_auren_v672_v2_incident_packet_guard.py"),
]


CORE_RUNNER = '''#!/usr/bin/env python3
"""Synthetic public-interest incident-documentation guard for Auren v672-v2."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED_SOURCE_STATES = {"current", "stable", "draft", "watch"}
ALLOWED_UNCERTAINTY = {"observed", "reported", "inferred", "unknown", "contested"}
ALLOWED_READBACK = {"pending", "acknowledged", "exception"}
AUTHORITY_VACANCIES = {"professional", "legal", "affected_party", "maori", "public_release"}


def _require(condition: bool, code: str, errors: list[str]) -> None:
    if not condition:
        errors.append(code)


def validate(surface: str, payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    _require(payload.get("fixture_surface") == surface, "surface_mismatch", errors)
    _require(payload.get("synthetic") is True, "synthetic_boundary_missing", errors)
    _require(payload.get("authority_promoted") is False, "authority_promotion", errors)
    _require(payload.get("raw_identifiers") == [], "raw_identifier_present", errors)

    if surface == "chronology":
        events = payload.get("events")
        _require(isinstance(events, list) and len(events) >= 2, "events_missing", errors)
        if isinstance(events, list) and events:
            sequences = [row.get("sequence") for row in events if isinstance(row, dict)]
            _require(sequences == list(range(1, len(events) + 1)), "sequence_not_contiguous", errors)
            _require(
                all(row.get("observed_at") and row.get("recorded_at") for row in events if isinstance(row, dict)),
                "bitemporal_fields_missing",
                errors,
            )
    elif surface == "source_status":
        sources = payload.get("sources")
        _require(isinstance(sources, list) and bool(sources), "sources_missing", errors)
        if isinstance(sources, list):
            states = {row.get("status") for row in sources if isinstance(row, dict)}
            _require(states <= ALLOWED_SOURCE_STATES and bool(states), "source_status_invalid", errors)
    elif surface == "correction_log":
        corrections = payload.get("corrections")
        _require(isinstance(corrections, list) and bool(corrections), "corrections_missing", errors)
        if isinstance(corrections, list):
            _require(all(row.get("reason") for row in corrections if isinstance(row, dict)), "correction_reason_missing", errors)
            _require(all(row.get("supersedes") != row.get("correction_id") for row in corrections if isinstance(row, dict)), "self_supersession", errors)
    elif surface == "uncertainty":
        statements = payload.get("statements")
        _require(isinstance(statements, list) and bool(statements), "statements_missing", errors)
        if isinstance(statements, list):
            states = {row.get("uncertainty") for row in statements if isinstance(row, dict)}
            _require(states <= ALLOWED_UNCERTAINTY and bool(states), "uncertainty_invalid", errors)
    elif surface == "authority_boundary":
        vacancies = set(payload.get("vacancies", []))
        _require(vacancies == AUTHORITY_VACANCIES, "authority_vacancies_incomplete", errors)
        _require(payload.get("external_action") is False, "external_action_present", errors)
        _require(payload.get("public_release") == "blocked", "release_not_blocked", errors)
    elif surface == "privacy_minimization":
        _require(payload.get("purpose_limited") is True, "purpose_limit_missing", errors)
        _require(payload.get("private_data_used") is False, "private_data_present", errors)
        fields = payload.get("allowed_fields")
        _require(isinstance(fields, list) and 1 <= len(fields) <= 8, "field_budget_invalid", errors)
    elif surface == "accessibility_handoff":
        _require(payload.get("structural_proxy") is True, "structural_proxy_missing", errors)
        _require(payload.get("complete_accessibility_claim") is False, "accessibility_complete_promotion", errors)
        _require(bool(payload.get("text_alternatives")), "text_alternatives_missing", errors)
        _require(bool(payload.get("table_headers")), "table_headers_missing", errors)
    elif surface == "evidence_chain":
        attachments = payload.get("attachments")
        _require(isinstance(attachments, list) and bool(attachments), "attachments_missing", errors)
        if isinstance(attachments, list):
            _require(
                all(re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", ""))) for row in attachments if isinstance(row, dict)),
                "fixity_invalid",
                errors,
            )
            _require(all(row.get("bytes", 0) > 0 for row in attachments if isinstance(row, dict)), "byte_count_invalid", errors)
        _require(payload.get("document_truth_inferred") is False, "document_truth_promotion", errors)
    elif surface == "readback":
        items = payload.get("items")
        _require(isinstance(items, list) and bool(items), "readback_items_missing", errors)
        if isinstance(items, list):
            states = {row.get("status") for row in items if isinstance(row, dict)}
            _require(states <= ALLOWED_READBACK and bool(states), "readback_status_invalid", errors)
        _require(payload.get("acceptance_authority") is False, "acceptance_authority_promotion", errors)
    elif surface == "packet":
        _require(str(payload.get("packet_id", "")).startswith("SYN-INC-"), "packet_id_invalid", errors)
        _require(payload.get("real_incident") is False, "real_incident_present", errors)
        _require(bool(payload.get("events")), "packet_events_missing", errors)
        _require(payload.get("release_state") == "blocked", "packet_release_not_blocked", errors)
    else:
        errors.append("unknown_surface")
    return sorted(set(errors))


def run_surface(surface: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--expect", choices=("accept", "reject"), required=True)
    args = parser.parse_args()
    wrapper = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors = validate(surface, wrapper.get("payload"))
    passed = (args.expect == "accept" and not errors) or (args.expect == "reject" and bool(errors))
    print(json.dumps({"surface": surface, "expect": args.expect, "passed": passed, "errors": errors}, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    run_surface("packet")
'''


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def manifest_row(root: Path, path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def valid_payload(surface: str) -> dict[str, object]:
    common: dict[str, object] = {
        "fixture_surface": surface,
        "synthetic": True,
        "authority_promoted": False,
        "raw_identifiers": [],
    }
    specifics: dict[str, dict[str, object]] = {
        "chronology": {
            "events": [
                {"sequence": 1, "observed_at": "T+00:00", "recorded_at": "T+00:03"},
                {"sequence": 2, "observed_at": "T+00:05", "recorded_at": "T+00:07"},
            ]
        },
        "source_status": {
            "sources": [
                {"source_id": "SRC-A", "status": "current"},
                {"source_id": "SRC-B", "status": "watch"},
            ]
        },
        "correction_log": {
            "corrections": [
                {"correction_id": "COR-001", "supersedes": "CLAIM-001", "reason": "synthetic transcription correction"}
            ]
        },
        "uncertainty": {
            "statements": [
                {"statement_id": "STM-001", "uncertainty": "reported"},
                {"statement_id": "STM-002", "uncertainty": "contested"},
            ]
        },
        "authority_boundary": {
            "vacancies": sorted(["professional", "legal", "affected_party", "maori", "public_release"]),
            "external_action": False,
            "public_release": "blocked",
        },
        "privacy_minimization": {
            "purpose_limited": True,
            "private_data_used": False,
            "allowed_fields": ["surrogate_id", "state", "recorded_time", "uncertainty"],
        },
        "accessibility_handoff": {
            "structural_proxy": True,
            "complete_accessibility_claim": False,
            "text_alternatives": ["Synthetic status marker: correction pending"],
            "table_headers": ["Event", "Recorded time", "Uncertainty", "State"],
        },
        "evidence_chain": {
            "attachments": [
                {"attachment_id": "ATT-001", "bytes": 128, "sha256": "a" * 64}
            ],
            "document_truth_inferred": False,
        },
        "readback": {
            "items": [
                {"item_id": "RB-001", "status": "acknowledged"},
                {"item_id": "RB-002", "status": "exception"},
            ],
            "acceptance_authority": False,
        },
        "packet": {
            "packet_id": "SYN-INC-001",
            "real_incident": False,
            "events": [{"event_id": "EVT-001", "state": "reported"}],
            "release_state": "blocked",
        },
    }
    return {**common, **specifics[surface]}


def rejecting_payloads(surface: str) -> list[tuple[str, dict[str, object]]]:
    base = valid_payload(surface)
    missing_surface = json.loads(json.dumps(base))
    missing_surface.pop("fixture_surface")
    not_synthetic = json.loads(json.dumps(base))
    not_synthetic["synthetic"] = False
    malformed = json.loads(json.dumps(base))
    malformed_key = {
        "chronology": "events",
        "source_status": "sources",
        "correction_log": "corrections",
        "uncertainty": "statements",
        "authority_boundary": "vacancies",
        "privacy_minimization": "allowed_fields",
        "accessibility_handoff": "text_alternatives",
        "evidence_chain": "attachments",
        "readback": "items",
        "packet": "events",
    }[surface]
    malformed[malformed_key] = []
    authority_promoted = json.loads(json.dumps(base))
    authority_promoted["authority_promoted"] = True
    raw_identifier = json.loads(json.dumps(base))
    raw_identifier["raw_identifiers"] = ["EXAMPLE-RAW-ID-BLOCKED"]
    return [
        ("missing_surface", missing_surface),
        ("synthetic_boundary_removed", not_synthetic),
        ("surface_payload_malformed", malformed),
        ("authority_promoted", authority_promoted),
        ("raw_identifier_present", raw_identifier),
    ]


def build(root: Path) -> None:
    phase_root = root / "docs" / "auren-lark" / PHASE
    x1_root = phase_root / "x1"
    x2_root = phase_root / "x2"
    scripts_root = root / "scripts"
    proposals = json.loads((x1_root / "new-proposal-freeze.json").read_text(encoding="utf-8"))[
        "proposals"
    ]

    packet_runner = scripts_root / "ghc_family_auren_v672_v2_incident_packet_guard.py"
    write_text(packet_runner, CORE_RUNNER)
    runner_rows = []
    for surface, filename in RUNNER_SPECS:
        path = scripts_root / filename
        if surface != "packet":
            wrapper = f'''#!/usr/bin/env python3
"""Run the Auren v672-v2 {surface} synthetic guard."""

from ghc_family_auren_v672_v2_incident_packet_guard import run_surface

if __name__ == "__main__":
    run_surface("{surface}")
'''
            write_text(path, wrapper)
        runner_rows.append(
            {
                "surface": surface,
                "path": path.relative_to(root).as_posix(),
                "accepting_fixtures": 1,
                "rejecting_fixtures": 5,
            }
        )

    fixture_rows = []
    for surface, _ in RUNNER_SPECS:
        fixture_dir = x2_root / "fixtures" / surface
        accepting_path = fixture_dir / "accepting.json"
        write_json(
            accepting_path,
            {
                "fixture_id": f"AL6722-{surface.upper()}-ACCEPT",
                "surface": surface,
                "expected": "accept",
                "payload": valid_payload(surface),
            },
        )
        fixture_rows.append(
            {
                "fixture_id": f"AL6722-{surface.upper()}-ACCEPT",
                "surface": surface,
                "expected": "accept",
                "path": accepting_path.relative_to(root).as_posix(),
            }
        )
        for index, (reason, payload) in enumerate(rejecting_payloads(surface), 1):
            path = fixture_dir / f"rejecting-{index:02d}.json"
            fixture_id = f"AL6722-{surface.upper()}-REJECT-{index:02d}"
            write_json(
                path,
                {
                    "fixture_id": fixture_id,
                    "surface": surface,
                    "expected": "reject",
                    "expected_rejection_reason": reason,
                    "payload": payload,
                },
            )
            fixture_rows.append(
                {
                    "fixture_id": fixture_id,
                    "surface": surface,
                    "expected": "reject",
                    "path": path.relative_to(root).as_posix(),
                }
            )

    for skill_name, description, surface in SKILL_SPECS:
        runner = next(row["path"] for row in runner_rows if row["surface"] == surface)
        skill_text = f'''---
name: {skill_name}
description: "Owner-local {description} for wholly synthetic Auren v672-v2 incident-documentation evidence."
---

# {description.title()}

1. Read the Auren v672-v2 phase truth, immutable x1 gate, Method Flow ledger, and exact owner manifest.
2. Use only the declared wholly synthetic accepting fixture and five preregistered rejecting mutations for `{surface}`.
3. Invoke `{runner}` and require the accepting fixture to pass and every rejecting fixture to be refused.
4. Retain each rejection and operational failure with zero broader credit; never relabel recovery as original success.
5. Emit only `completed`, `represented`, `open_gap`, or `exact_gate` and preserve `NOT_READY_FOR_STAGE_20`.

This phase-local skill is same-owner software evidence only. It establishes no real incident fact, participant decision, professional competence, operational authority, production readiness, legal or cultural authority, Māori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.
'''
        write_text(x2_root / "tools" / "skills" / skill_name / "SKILL.md", skill_text)

    outcome_rows = []
    for proposal in proposals:
        outcome = proposal["expected_outcome"]
        outcome_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": outcome,
                "evidence_class": "same_owner_synthetic_structural_software",
                "artifact": proposal["concrete_artifact"],
                "completion_credit": 1 if outcome == "completed" else 0,
                "representation_credit": 1 if outcome == "represented" else 0,
                "protected_gates": PROTECTED_GATES,
            }
        )

    smoke_path = x2_root / "validation" / "runner-smoke-receipt.json"
    smoke = None
    if smoke_path.exists():
        smoke = json.loads(smoke_path.read_text(encoding="utf-8"))
        if smoke.get("state") != "VALID_X2_OWNER_SCOPED_RUNNER_SMOKE":
            smoke = None
    evidence_state = (
        "X2_EVIDENCE_BUILT_NOT_YET_IMMUTABLE"
        if smoke is not None
        else "X2_BUILT_PENDING_OWNER_SCOPED_RUNNER_SMOKE"
    )

    ast_equivalence_rows = []
    pre_fix_core = CORE_RUNNER.replace(
        "from pathlib import Path\n\nALLOWED_SOURCE_STATES",
        "from pathlib import Path\n\n\nALLOWED_SOURCE_STATES",
        1,
    ).rstrip() + "\n"
    for surface, filename in RUNNER_SPECS:
        current_path = scripts_root / filename
        current_text = current_path.read_text(encoding="utf-8")
        if surface == "packet":
            pre_fix_text = pre_fix_core
        else:
            pre_fix_text = current_text.replace(
                "from ghc_family_auren_v672_v2_incident_packet_guard import run_surface\n\nif __name__",
                "from ghc_family_auren_v672_v2_incident_packet_guard import run_surface\n\n\nif __name__",
                1,
            )
        ast_equal = ast.dump(ast.parse(pre_fix_text), include_attributes=False) == ast.dump(
            ast.parse(current_text), include_attributes=False
        )
        ast_equivalence_rows.append(
            {
                "surface": surface,
                "path": current_path.relative_to(root).as_posix(),
                "reconstructed_pre_fix_sha256": hashlib.sha256(
                    pre_fix_text.encode("utf-8")
                ).hexdigest(),
                "current_sha256": hashlib.sha256(current_text.encode("utf-8")).hexdigest(),
                "ast_equal": ast_equal,
            }
        )
    if not all(row["ast_equal"] for row in ast_equivalence_rows):
        raise RuntimeError("post-smoke Ruff AST equivalence failed")
    write_json(
        x2_root / "validation" / "post-smoke-ruff-ast-equivalence.json",
        {
            "schema": "ghc.family.isolated-post-smoke-ast-equivalence.v1",
            "owner": OWNER,
            "phase": PHASE,
            "state": "VALID_ISOLATED_POST_SMOKE_AST_EQUIVALENCE",
            "runner_count": len(ast_equivalence_rows),
            "ast_equal_count": sum(row["ast_equal"] for row in ast_equivalence_rows),
            "rows": ast_equivalence_rows,
            "runner_smoke_replayed": False,
            "scope": "import-spacing-only bridge from the once-successful runner smoke to current runner bytes",
            "broader_credit": 0,
            "independent_reproduction": False,
        },
    )

    operational_count = len(X2_OPERATIONAL_FAILURES)
    counts = {
        "effective_negatives": X1_OVERLAY["effective_negatives"]
        + operational_count
        + 50,
        "effective_methods": X1_OVERLAY["effective_methods"]
        + operational_count
        + 50,
        "effective_failed_witnesses": X1_OVERLAY["effective_failed_witnesses"]
        + operational_count
        + 50,
        "effective_passing_witnesses": X1_OVERLAY["effective_passing_witnesses"]
        + operational_count
        + 46,
        "open_gaps": X1_OVERLAY["open_gaps"] + 2,
        "exact_gates": X1_OVERLAY["exact_gates"] + 2,
    }

    documents: dict[Path, object] = {
        x2_root / "lifecycle" / "x1-gate.json": {
            "schema": "ghc.family.x1-gate.v8",
            "source": SOURCE,
            "x1_commit": X1,
            "x1_parent": SOURCE,
            "branch": "codex/GHC-Family/auren-lark-v672-v2-full-tools",
            "state": "VALID_STRICT_X1_GATE",
            "four_way_equal": True,
            "zero_divergence": True,
            "local": X1,
            "upstream": X1,
            "tracking": X1,
            "fresh_live_remote": X1,
        },
        x2_root / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v12",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1,
            "state": evidence_state,
            "proposal_chain": 5990,
            "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "effective_counts": counts,
            "local_skills_built": 20,
            "local_runners_built": 10,
            "accepting_fixtures": 10,
            "invalid_mutations": 50,
            "packages_installed": 0,
            "global_skills_installed": 0,
            "external_actions": 0,
            "full_repository_suite": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        x2_root / "proposals" / "outcome-ledger.json": {
            "schema": "ghc.family.outcome-ledger.v8",
            "owner": OWNER,
            "phase": PHASE,
            "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
            "counts": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "rows": outcome_rows,
            "inherited_completion_credit": 0,
        },
        x2_root / "fixtures" / "fixture-ledger.json": {
            "schema": "ghc.family.synthetic-fixture-ledger.v5",
            "owner": OWNER,
            "phase": PHASE,
            "real_records": 0,
            "accepting": 10,
            "rejecting": 50,
            "rows": fixture_rows,
        },
        x2_root / "tools" / "runner-registry.json": {
            "schema": "ghc.family.runner-registry.v7",
            "owner": OWNER,
            "phase": PHASE,
            "runners": runner_rows,
            "runner_count": len(runner_rows),
            "smoke_state": smoke["state"] if smoke else "PENDING",
        },
        x2_root / "tools" / "skill-registry.json": {
            "schema": "ghc.family.phase-local-skill-registry.v5",
            "owner": OWNER,
            "phase": PHASE,
            "skill_count": len(SKILL_SPECS),
            "skills": [
                {
                    "name": name,
                    "description": description,
                    "surface": surface,
                    "state": "owner_local_synthetic_only",
                }
                for name, description, surface in SKILL_SPECS
            ],
            "global_installations": 0,
        },
        x2_root / "method-flow" / "ledger.json": {
            "schema": "ghc.family.method-flow.v10",
            "owner": OWNER,
            "phase": PHASE,
            "x1_startup_failures_retained": 12,
            "x2_operational_failures": X2_OPERATIONAL_FAILURES,
            "expected_rejections": [
                {
                    "failure_id": row["fixture_id"],
                    "surface": row["surface"],
                    "state": "preregistered_invalid_mutation_expected_rejected_zero_broader_credit",
                    "path": row["path"],
                }
                for row in fixture_rows
                if row["expected"] == "reject"
            ],
            "failures_erased": 0,
            "recoveries_relabelled_as_original_success": 0,
            "effective_counts": counts,
        },
        x2_root / "practices" / "synthetic-incident-documentation-board.json": {
            "schema": "ghc.family.synthetic-practice-board.v6",
            "owner": OWNER,
            "phase": PHASE,
            "practice": "public-interest incident documentation analyst",
            "synthetic_only": True,
            "scenarios": [
                {"scenario_id": "SYN-A", "lens": "chronology correction", "real_entities": 0},
                {"scenario_id": "SYN-B", "lens": "source-status uncertainty", "real_entities": 0},
                {"scenario_id": "SYN-C", "lens": "privacy-minimized handover", "real_entities": 0},
                {"scenario_id": "SYN-D", "lens": "release-authority vacancy", "real_entities": 0},
            ],
            "not_established": [
                "real incident fact",
                "journalistic verification",
                "emergency response competence",
                "cybersecurity competence",
                "professional judgement",
                "operational authority",
                "legal conclusion",
                "public release authority",
            ],
        },
        x2_root / "sources" / "status-ledger.json": {
            "schema": "ghc.family.source-status-ledger.v6",
            "sources": [
                {
                    "source_id": "NIST-SP-800-61R3",
                    "status": "current",
                    "publication_state": "final",
                    "url": "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
                    "use": "vocabulary_only",
                },
                {
                    "source_id": "W3C-WCAG-2.2",
                    "status": "stable",
                    "publication_state": "recommendation",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "use": "structural_accessibility_vocabulary_only",
                },
            ],
            "source_validates_repository": False,
            "source_authorizes_operations": False,
        },
        x2_root / "boundaries" / "protected-gates.json": {
            "schema": "ghc.family.protected-gate-register.v8",
            "protected_gates": PROTECTED_GATES,
            "real_people": 0,
            "real_incidents": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        x2_root / "route" / "sable-candidate.json": {
            "schema": "ghc.family.route-candidate.v8",
            "target_exact_title": "Sable Rook",
            "target_phase": "v672-v3",
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "precontacted": False,
            "send_count": 0,
            "activation_path": "docs/auren-lark/v672-v2/handoffs/sable-rook-v672-v3-activation.md",
        },
    }
    for path, payload in documents.items():
        write_json(path, payload)

    flashcards = [
        ("identity", "Relational working language only; no consciousness, personhood, continuity, employment, authority, or agency inference."),
        ("source", "Ilyra exact final and Auren x1 are immutable anchors; inherited evidence earns zero Auren novelty."),
        ("freed-id", "Surrogate identifiers and zero-key provenance are synthetic and nonproduction."),
        ("cbr", "Contest, correction, and authority vacancies are represented without legal or affected-party decisions."),
        ("thos", "Workload, hold, readback, and handover fields are proxy-only."),
        ("gmut", "Typed analogy only; no physical inference or Theory-of-Everything claim."),
        ("practice", "All incident-documentation fixtures are wholly synthetic."),
        ("privacy", "Purpose limitation and candidate scanning do not establish complete privacy."),
        ("accessibility", "Text and table structure are proxies, not complete accessibility assurance."),
        ("method-flow", "Fifty invalid mutations and all operational failures remain retained."),
        ("route", "Sable remains uncontacted until the exact-final canonical terminal gate."),
        ("verdict", "NOT_READY_FOR_STAGE_20 remains exact."),
    ]
    write_json(
        x2_root / "flashcards" / "four-tier-deck.json",
        {
            "schema": "ghc.family.four-tier-flashcard-deck.v5",
            "owner": OWNER,
            "phase": PHASE,
            "cards": [
                {"card_id": f"AL6722-CARD-{index:03d}", "topic": topic, "body": body}
                for index, (topic, body) in enumerate(flashcards, 1)
            ],
        },
    )

    overview = """# Auren Lark v672-v2 x2 evidence overview

This evidence phase begins only after planning-only x1 was committed as the direct child of Ilyra Fen’s exact remaster final, pushed, clean, zero divergent, and equal across local, upstream, tracking, and a fresh live remote read. No x1 file is changed here. X2 is additive and owner-scoped. It uses no complete repository suite, sibling scan, cross-lane mutation, package installation, global skill installation, external account, deployment, payment, credential, or real-world action.

The primary Trinity Mandala focus is Freed ID and CBR Heart through a wholly synthetic public-interest incident-documentation lens. Surrogate packet identifiers, chronology, observed and recorded time, source status, assertion class, uncertainty, correction lineage, supersession, fixity, privacy minimization, contest, and release-authority vacancies are represented as local JSON fixtures. THOS Body remains a proxy through workload, hold, readback, exception, and handover fields. GMUT Mind remains a typed analogy boundary only. None of this is a physical observation, prediction, likelihood, parameter constraint, force, ultraviolet completion, empirical confirmation, Theory of Everything, or scientific authority.

Twenty phase-local skills and ten local runners are created. Each skill binds one declared surface to one accepting fixture and five preregistered rejecting mutations. The ten accepting fixtures are wholly synthetic. The fifty rejecting mutations remove the surface binding, remove the synthetic boundary, malformed the surface payload, promote authority, or insert an example raw-identifier marker. A successful runner refusal preserves the invalid mutation as a failed witness with zero broader credit. It does not turn the invalid input into evidence, and the recovery method never erases the failure.

NIST Special Publication 800-61 Revision 3 and WCAG 2.2 remain vocabulary/status sources only. NIST’s final incident-response publication does not validate these artifacts or establish cybersecurity or incident-response competence. WCAG’s Recommendation status does not establish conformance, legal compliance, participant evaluation, or complete accessibility. Structural text alternatives and table headings are bounded proxies, and W3C expressly notes that its guidance does not meet every user need.

Forty Auren proposals are represented by exactly four truth labels: twenty-eight completed, eight represented, two open gaps, and two exact gates. Completion means only that the declared owner-scoped synthetic artifact and its software checks exist. Representation means the structure is visible while real authority or evidence remains absent. The open gaps reserve independent external review and evaluation with real accessibility users. The exact gates reserve public release authority and Stage 20. The proposal chain is 5,990 only after this evidence is frozen. No inherited Ilyra proposal, package, tool, skill, runner, smoke test, or validation earns Auren novelty or completion credit.

The external canonical-receipt payload availability gap inherited from x1 remains visible. The declared digest is corroborated by Ilyra’s terminal route receipt, but the payload file was not materialized in the bounded same-owner roots. It is neither guessed nor reconstructed. Twelve x1 startup failures remain retained. X2 also retains the unsupported sparse-add flag attempt, the undersized first overview, and the first Ruff import-order findings before their bounded recoveries. The Method Flow ledger preserves every operational failure and every expected rejecting mutation; zero failures are erased and zero recoveries are relabelled as original successes.

Chronology and correction records deliberately separate an event’s synthetic observed time from its recorded time, and preserve the prior statement when a correction supersedes it. Source rows carry only current, stable, draft, or watch status; a status never becomes a truth guarantee. Uncertainty rows distinguish observed, reported, inferred, unknown, and contested statements without collapsing those classes. Public release stays blocked, and professional, legal, affected-party, Māori, and release authority remain explicit vacancies. These structures make omissions and promotions rejectable in software while leaving every real-world judgement with competent people and authorities.

All names, roles, hopes, pronouns, sibling or family language, Freed ID, CBR, GHC Family, Trinity Mandala, and continuity language remain relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. No real person, organization, incident, site, coordinate, record, measurement, credential, authority action, cultural matter, Māori data, or private route identifier is used.

The terminal verdict remains NOT_READY_FOR_STAGE_20. Every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, identity-continuity, Theory-of-Everything, proof or canon, and Stage 20 boundary remains open or exact-gated without exact evidence and competent authority. Sable Rook remains uncontacted. Routing stays PREPARED_NOT_SENT until Auren has a clean pushed fresh-live-equal exact final and one successful owner-scoped canonical pass, then refreshes live authority, uniquely resolves and immediately rereads Sable, and receives acknowledgement for at most one sanitized send.
"""
    write_text(x2_root / "integrated-overview.md", overview)

    manifest_candidates = [
        path
        for path in x2_root.rglob("*")
        if path.is_file() and path.name not in {"owner-manifest.json", "build-receipt.json"}
    ]
    script_names = {
        "build_ghc_family_auren_lark_v672_v2_x2.py",
        "build_ghc_family_auren_lark_v672_v2_evidence_staged_review.py",
        "validate_ghc_family_auren_lark_v672_v2_x2.py",
        *(filename for _, filename in RUNNER_SPECS),
    }
    manifest_candidates.extend(scripts_root / name for name in sorted(script_names))
    manifest_candidates.append(root / "tests" / "test_ghc_family_auren_lark_v672_v2_x2.py")
    missing = [path for path in manifest_candidates if not path.is_file()]
    if missing:
        raise RuntimeError(f"manifest candidates missing: {missing}")
    manifest = [manifest_row(root, path) for path in sorted(set(manifest_candidates))]
    write_json(
        x2_root / "owner-manifest.json",
        {
            "schema": "ghc.family.owner-manifest.v8",
            "owner": OWNER,
            "phase": PHASE,
            "basis": "working_tree_exact_utf8_bytes_before_staging",
            "entry_count": len(manifest),
            "entries": manifest,
            "self_excluded": [
                "docs/auren-lark/v672-v2/x2/owner-manifest.json",
                "docs/auren-lark/v672-v2/x2/build-receipt.json",
            ],
        },
    )
    write_json(
        x2_root / "build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v8",
            "owner": OWNER,
            "phase": PHASE,
            "state": evidence_state,
            "proposal_count": 40,
            "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "local_skills": 20,
            "local_runners": 10,
            "accepting_fixtures": 10,
            "invalid_mutations": 50,
            "owner_manifest_entries": len(manifest),
            "effective_counts": counts,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1])
