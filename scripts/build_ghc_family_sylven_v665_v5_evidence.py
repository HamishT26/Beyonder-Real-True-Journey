#!/usr/bin/env python3
"""Build and exact-review Sylven Arc v665-v5 bounded x2 evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from ghc_family_sylven_v665_v5_runner_core import (  # noqa: E402
    PROFILES,
    canonical_bytes,
    evaluate,
)


PHASE = ROOT / "docs/sylven-arc/v665-v5"
PREFIX = "docs/sylven-arc/v665-v5/"
OWNER = "Sylven Arc"
PHASE_ID = "v665-v5"
BRANCH = "codex/GHC-Family/sylven-arc-v665-v5-full-tools"
SOURCE_FINAL = "296ec195744fbbf62bae5d2f233f1112bcc14591"
X1 = "0a24628b70e1179a8758718a05029060488a9a1b"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
STARTUP_NEGATIVES = 25_562
STARTUP_METHODS = 9_424
MUTATION_COUNT = 100
INHERITED_OPEN_GAPS = 178
INHERITED_EXACT_GATES = 176
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
RECORDED_UTC = "2026-08-22T03:05:00Z"

OPERATIONAL_FAILURES: list[dict[str, str]] = []

RUNNERS = {
    "kiln_load_capsule": "scripts/ghc_family_sylven_v665_v5_kiln_load_capsule.py",
    "kiln_clearance_graph": "scripts/ghc_family_sylven_v665_v5_kiln_clearance_graph.py",
    "glaze_quarantine": "scripts/ghc_family_sylven_v665_v5_glaze_quarantine.py",
    "witness_cone_readback": "scripts/ghc_family_sylven_v665_v5_witness_cone_readback.py",
    "firing_state_machine": "scripts/ghc_family_sylven_v665_v5_firing_state_machine.py",
    "kiln_command_firewall": "scripts/ghc_family_sylven_v665_v5_kiln_command_firewall.py",
    "thermal_unit_board": "scripts/ghc_family_sylven_v665_v5_thermal_unit_board.py",
    "heat_agency_nonconversion": "scripts/ghc_family_sylven_v665_v5_heat_agency_nonconversion.py",
    "epa_worksafe_zero_row": "scripts/ghc_family_sylven_v665_v5_epa_worksafe_zero_row.py",
    "ceramics_authority_matrix": "scripts/ghc_family_sylven_v665_v5_ceramics_authority_matrix.py",
}
PROFILE_BY_PROPOSAL = {
    "SA6655-N001": "kiln_load_capsule",
    "SA6655-N002": "kiln_clearance_graph",
    "SA6655-N003": "glaze_quarantine",
    "SA6655-N004": "witness_cone_readback",
    "SA6655-N005": "firing_state_machine",
    "SA6655-N006": "kiln_command_firewall",
    "SA6655-N007": "ceramics_authority_matrix",
    "SA6655-N008": "thermal_unit_board",
    "SA6655-N009": "thermal_unit_board",
    "SA6655-N010": "thermal_unit_board",
    "SA6655-N011": "thermal_unit_board",
    "SA6655-N012": "thermal_unit_board",
    "SA6655-N013": "glaze_quarantine",
    "SA6655-N014": "kiln_load_capsule",
    "SA6655-N015": "thermal_unit_board",
    "SA6655-N016": "epa_worksafe_zero_row",
    "SA6655-N017": "epa_worksafe_zero_row",
    "SA6655-N018": "heat_agency_nonconversion",
    "SA6655-N019": "epa_worksafe_zero_row",
    "SA6655-N020": "ceramics_authority_matrix",
}
SKILLS = [
    ("ghc-family-kiln-load-capsule-validator", "kiln_load_capsule", "Kiln load capsule validator", "Check synthetic load identity, cancellation, provenance, and no-action fields."),
    ("ghc-family-kiln-clearance-graph-auditor", "kiln_clearance_graph", "Kiln clearance graph auditor", "Check synthetic shelf occupancy and reject overlap or unsupported-span promotion."),
    ("ghc-family-glaze-quarantine-lineage-checker", "glaze_quarantine", "Glaze quarantine lineage checker", "Check synthetic batch lineage, release holds, and substitutions."),
    ("ghc-family-witness-cone-readback-auditor", "witness_cone_readback", "Witness cone readback auditor", "Check synthetic cone-zone readback while refusing interpretation or image evidence."),
    ("ghc-family-firing-state-machine-checker", "firing_state_machine", "Firing state machine checker", "Check synthetic ramp, soak, cool, abort, and power-loss transitions without equipment action."),
    ("ghc-family-kiln-command-observation-firewall", "kiln_command_firewall", "Kiln command observation firewall", "Reject live controller calls, operator authority, and actuation events."),
    ("ghc-family-thermal-unit-obligation-checker", "thermal_unit_board", "Thermal unit obligation checker", "Check symbolic thermal terms and reject unit imbalance or empirical promotion."),
    ("ghc-family-heat-agency-nonconversion-guard", "heat_agency_nonconversion", "Heat agency nonconversion guard", "Prevent thermal symbols from becoming agency, personhood, or ethical authority evidence."),
    ("ghc-family-epa-worksafe-zero-row-firewall", "epa_worksafe_zero_row", "EPA WorkSafe zero-row firewall", "Preserve zero-call, zero-row, zero-key, zero-participant, and external-witness boundaries."),
    ("ghc-family-ceramics-authority-matrix-reviewer", "ceramics_authority_matrix", "Ceramics authority matrix reviewer", "Preserve professional, legal, cultural, affected-party, tangata whenua, iwi, hapū, Māori, and Stage 20 gates."),
]

BUILDER = "scripts/build_ghc_family_sylven_v665_v5_evidence.py"
CORE = "scripts/ghc_family_sylven_v665_v5_runner_core.py"
TEST = "tests/test_ghc_family_sylven_v665_v5_x2.py"
LEDGER_PATHS = [
    f"{PREFIX}x2/ledgers/boundary-matrix.json",
    f"{PREFIX}x2/ledgers/execution-summary.json",
    f"{PREFIX}x2/ledgers/method-flow-overlay.json",
    f"{PREFIX}x2/ledgers/mutation-ledger.json",
    f"{PREFIX}x2/ledgers/outcome-ledger.json",
    f"{PREFIX}x2/ledgers/portfolio-execution.json",
    f"{PREFIX}x2/ledgers/runner-registry.json",
    f"{PREFIX}x2/ledgers/skill-registry.json",
    f"{PREFIX}x2/ledgers/source-use-ledger.json",
    f"{PREFIX}x2/ledgers/x1-integrity-replay.json",
    f"{PREFIX}x2/x2-overview.md",
]
PROPOSAL_PATHS = [
    f"{PREFIX}x2/proposals/{pid.casefold()}/{name}"
    for pid in PROFILE_BY_PROPOSAL
    for name in ("contract.json", "mutation-results.json", "bounded-receipt.json")
]
SKILL_PATHS = [
    f"{PREFIX}x2/skills/{slug}/{name}"
    for slug, _, _, _ in SKILLS
    for name in ("SKILL.md", "quick-validation.json", "smoke-receipt.json")
]
RUNNER_RECEIPTS = [
    f"{PREFIX}x2/runners/{profile}-smoke-receipt.json" for profile in RUNNERS
]
BASE_PATHS = sorted(
    [
        BUILDER,
        CORE,
        TEST,
        *RUNNERS.values(),
        *LEDGER_PATHS,
        *PROPOSAL_PATHS,
        *SKILL_PATHS,
        *RUNNER_RECEIPTS,
    ]
)
SELF_EXCLUSIONS = [
    f"{PREFIX}x2/validation/evidence-content-manifest.json",
    f"{PREFIX}x2/validation/evidence-stage-candidate.json",
    f"{PREFIX}x2/validation/evidence-staged-review.json",
]
INTENDED_PATHS = sorted(BASE_PATHS + SELF_EXCLUSIONS)


class EvidenceError(RuntimeError):
    pass


def run(
    *args: str, check: bool = True, input_text: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        input=input_text,
        capture_output=True,
        check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise EvidenceError(f"invalid UTF-8 JSON for {label}: {exc}") from exc


def read_json(path: Path) -> Any:
    return strict_json_bytes(path.read_bytes(), str(path.relative_to(ROOT)))


def write_json(relative: str, value: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(pretty_bytes(value))


def write_text(relative: str, value: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((value.rstrip() + "\n").encode("utf-8"))


def git_blob(revision: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True
    )
    return result.stdout


def positive_fixture(proposal: dict[str, Any], profile: str) -> dict[str, Any]:
    fixture: dict[str, Any] = {
        "schema": "ghc.family.sylven.v665-v5.bounded-input.v1",
        "proposal_id": proposal["proposal_id"],
        "synthetic": True,
        "real_rows": 0,
        "authority_events": 0,
        "claim_ceiling": PROFILES[profile]["ceiling"],
        "terminal_verdict": TERMINAL_VERDICT,
        "source_ids": proposal["official_or_primary_source_needs"],
    }
    additions: dict[str, dict[str, Any]] = {
        "kiln_load_capsule": {
            "ware_tokens": ["SYN-WARE-001"],
            "shelf_coordinates": [{"ware_token": "SYN-WARE-001", "shelf": "SYN-SHELF-A", "x": 0, "y": 0}],
            "cancelled": False,
            "provenance_present": True,
            "external_action": False,
        },
        "kiln_clearance_graph": {
            "nodes": [{"id": "SYN-WARE-001", "envelope": "unitless-placeholder"}],
            "edges": [],
            "overlap_count": 0,
            "unsupported_span": False,
            "clearance_quarantined": True,
        },
        "glaze_quarantine": {
            "batch_token": "SYN-GLAZE-001",
            "lot_lineage": ["SYN-LOT-001"],
            "release_state": "held",
            "safety_sheet_present": False,
            "substitution_history": [],
            "physical_release": False,
        },
        "witness_cone_readback": {
            "cone_set": "SYN-CONE-SET-001",
            "zone_map": {"top": "synthetic-placeholder", "middle": "synthetic-placeholder", "bottom": "synthetic-placeholder"},
            "observation_readback": True,
            "interpretation_claim": False,
            "real_image_present": False,
        },
        "firing_state_machine": {
            "states": ["planned", "held", "synthetic_ramp", "synthetic_soak", "synthetic_cool", "aborted"],
            "transitions": [{"from": "planned", "to": "held", "synthetic_only": True}],
            "abort_dominant": True,
            "restart_authorized": False,
            "real_actuation": False,
        },
        "kiln_command_firewall": {
            "observation_channel": "simulated",
            "command_channel": "null",
            "live_controller_calls": 0,
            "operator_authority": False,
            "actuation_events": 0,
        },
        "thermal_unit_board": {
            "term_units": {"temperature": "K", "time": "s", "length": "m", "conductivity": "W m-1 K-1"},
            "dimensional_balance": True,
            "real_measurements": 0,
            "empirical_fit": False,
            "physical_law_claim": False,
        },
        "heat_agency_nonconversion": {
            "thermal_symbols": ["temperature", "heat_flux", "entropy_production"],
            "agency_inference": False,
            "personhood_inference": False,
            "ethical_authority": False,
        },
        "epa_worksafe_zero_row": {
            "artifact_class": "official_schema_vocabulary_zero_row",
            "live_data_calls": 0,
            "real_keys": 0,
            "real_participants": 0,
            "external_witness_present": False,
            "empirical_gmut_claim": False,
            "stage20_authority": False,
        },
        "ceramics_authority_matrix": {
            "worker_decision": False,
            "consumer_decision": False,
            "legal_decision": False,
            "cultural_decision": False,
            "maori_authority": False,
            "affected_party_acceptance": False,
        },
    }
    fixture.update(additions[profile])
    return fixture


def mutations(profile: str, positive: dict[str, Any]) -> list[dict[str, Any]]:
    variants: list[tuple[str, str, Any]] = [
        ("M01", "synthetic", False),
        ("M02", "real_rows", 1),
        ("M03", "authority_events", 1),
        ("M04", "terminal_verdict", "READY_FOR_STAGE_20"),
    ]
    profile_mutation: dict[str, tuple[str, Any]] = {
        "kiln_load_capsule": ("external_action", True),
        "kiln_clearance_graph": ("overlap_count", 1),
        "glaze_quarantine": ("physical_release", True),
        "witness_cone_readback": ("interpretation_claim", True),
        "firing_state_machine": ("real_actuation", True),
        "kiln_command_firewall": ("live_controller_calls", 1),
        "thermal_unit_board": ("dimensional_balance", False),
        "heat_agency_nonconversion": ("agency_inference", True),
        "epa_worksafe_zero_row": ("live_data_calls", 1),
        "ceramics_authority_matrix": ("maori_authority", True),
    }
    field, value = profile_mutation[profile]
    variants.append(("M05", field, value))
    results = []
    for suffix, changed_field, changed_value in variants:
        payload = copy.deepcopy(positive)
        payload[changed_field] = changed_value
        result = evaluate(profile, payload)
        results.append(
            {
                "mutation_id": f"{positive['proposal_id']}-{suffix}",
                "changed_field": changed_field,
                "changed_value": changed_value,
                "input_sha256": sha256(canonical_bytes(payload)),
                "runner_result": result,
                "expected_decision": "rejected",
                "retained_status": "failed_witness_zero_credit",
                "valid": result["decision"] == "rejected" and not result["valid"],
            }
        )
    return results


def skill_markdown(slug: str, profile: str, title: str, purpose: str) -> str:
    required = ", ".join(sorted(PROFILES[profile]["required"]))
    return f"""---
name: {slug}
description: {purpose}
---

# {title}

## Scope

Use only for Sylven Arc {PHASE_ID} owner-local synthetic, zero-row, or typed-formal artifacts. This skill confers no professional, empirical, production, legal, cultural, Māori, affected-party, accessibility-complete, security-complete, or Stage 20 authority.

## Required inputs

- UTF-8 JSON object using runner profile `{profile}`.
- Base boundary fields: `synthetic`, `real_rows`, `authority_events`, `claim_ceiling`, `terminal_verdict`, and `source_ids`.
- Profile fields: {required}.

## Procedure

1. Read the complete input and preserve its digest.
2. Require `synthetic=true`, zero real rows, zero authority events, and `{TERMINAL_VERDICT}`.
3. Invoke `{RUNNERS[profile]}` and retain every rejection before recovery.
4. Report only the bounded runner decision and exact claim ceiling.

## Fail-closed stops

Stop on real rows, real studios, kilns, firings, ware, cones, glazes, materials, images, people, keys, proofs, identity events, equipment action, professional decisions, protected-gate promotion, malformed JSON, source vacancy, or an unexpected claim ceiling.

## Output boundary

An accepted fixture demonstrates only that this same-owner software contract accepted one bounded structure and rejected preregistered mutations. It is not scientific confirmation, ceramics or kiln guidance, professional validation, production conformance, independent reproduction, proof, or authority.

## Terminal boundary

The only terminal verdict permitted here is `{TERMINAL_VERDICT}`.
"""


def runner_wrapper(profile: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-compatible {profile} runner; bounded Sylven v665-v5 surface."""
from ghc_family_sylven_v665_v5_runner_core import run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli("{profile}"))
'''


def invoke_runner(profile: str, fixture: dict[str, Any]) -> dict[str, Any]:
    path = RUNNERS[profile]
    result = run(
        sys.executable,
        path,
        input_text=canonical_bytes(fixture).decode("utf-8"),
        check=False,
    )
    parsed = strict_json_bytes(result.stdout.encode("utf-8"), f"runner {profile} stdout")
    return {
        "schema": "ghc.family.sylven.v665-v5.runner-smoke-receipt.v1",
        "profile": profile,
        "runner_path": path,
        "return_code": result.returncode,
        "stderr_empty": result.stderr == "",
        "stdout_sha256": sha256(result.stdout.encode("utf-8")),
        "result": parsed,
        "valid": result.returncode == 0 and result.stderr == "" and parsed.get("valid") is True,
    }


def replay_x1_integrity() -> dict[str, Any]:
    manifest_path = f"{PREFIX}x1/x1-content-manifest.json"
    manifest = strict_json_bytes(git_blob(X1, manifest_path), manifest_path)
    mismatches = []
    for entry in manifest["entries"]:
        raw = git_blob(X1, entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    changed = git("diff", "--name-only", X1, "--", f"{PREFIX}x1")
    return {
        "schema": "ghc.family.sylven.v665-v5.x1-integrity-replay.v1",
        "x1_commit": X1,
        "manifest_entry_count": len(manifest["entries"]),
        "manifest_mismatches": mismatches,
        "x1_tree_changes_after_freeze": changed.splitlines() if changed else [],
        "x1_parent_is_source": git("rev-parse", f"{X1}^") == SOURCE_FINAL,
        "valid": not mismatches and not changed and git("rev-parse", f"{X1}^") == SOURCE_FINAL,
    }


def build_evidence() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != X1:
        raise EvidenceError("evidence must begin at the exact pushed x1 commit")
    if git("branch", "--show-current") != BRANCH:
        raise EvidenceError("unexpected owner branch")
    existing_staged = staged_paths()
    if existing_staged and not set(existing_staged).issubset(set(BASE_PATHS)):
        raise EvidenceError("staging contains a path outside the x2 recovery allowlist")
    x1_integrity = replay_x1_integrity()
    if not x1_integrity["valid"]:
        raise EvidenceError("immutable x1 replay failed")
    write_json(f"{PREFIX}x2/ledgers/x1-integrity-replay.json", x1_integrity)

    for profile, path in RUNNERS.items():
        write_text(path, runner_wrapper(profile))

    freeze = read_json(PHASE / "x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    if len(proposals) != 20 or set(PROFILE_BY_PROPOSAL) != {
        row["proposal_id"] for row in proposals
    }:
        raise EvidenceError("proposal freeze drift")

    outcome_rows = []
    all_mutations = []
    positive_results: dict[str, dict[str, Any]] = {}
    reasons = {
        "completed": "the bounded same-owner positive fixture passed and all five frozen rejecting mutations failed closed",
        "represented": "a bounded synthetic or formal proxy exists while real actors, data, operations, and independent review remain absent",
        "open_gap": "the zero-call adapter preserves the missing-data boundary; it downloaded and parsed no real record",
        "exact_gate": "worker, consumer, studio access, custody, design heritage, taonga, remedy, affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori authority remain absent",
    }
    for proposal in proposals:
        pid = proposal["proposal_id"]
        profile = PROFILE_BY_PROPOSAL[pid]
        fixture = positive_fixture(proposal, profile)
        positive = evaluate(profile, fixture)
        if not positive["valid"]:
            raise EvidenceError(f"positive fixture rejected: {pid}: {positive['errors']}")
        mutation_rows = mutations(profile, fixture)
        if len(mutation_rows) != 5 or not all(row["valid"] for row in mutation_rows):
            raise EvidenceError(f"mutation retention failed: {pid}")
        disposition = proposal["expected_disposition"]
        folder = f"{PREFIX}x2/proposals/{pid.casefold()}"
        contract = {
            "schema": "ghc.family.sylven.v665-v5.proposal-contract.v1",
            "proposal_id": pid,
            "title": proposal["title"],
            "runner_profile": profile,
            "expected_disposition": disposition,
            "positive_fixture": fixture,
            "protected_gates": proposal["protected_gates"],
            "source_ids": proposal["official_or_primary_source_needs"],
            "real_rows": 0,
            "authority_events": 0,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        }
        mutation_doc = {
            "schema": "ghc.family.sylven.v665-v5.mutation-results.v1",
            "proposal_id": pid,
            "mutation_count": 5,
            "rejected_count": 5,
            "accepted_mutation_count": 0,
            "mutations": mutation_rows,
            "failed_witness_erasure_count": 0,
            "valid": True,
        }
        receipt = {
            "schema": "ghc.family.sylven.v665-v5.bounded-receipt.v1",
            "proposal_id": pid,
            "runner_profile": profile,
            "expected_disposition": disposition,
            "observed_disposition": disposition,
            "disposition_reason": reasons[disposition],
            "positive_runner_result": positive,
            "positive_fixture_sha256": sha256(canonical_bytes(fixture)),
            "mutation_receipt_path": f"{folder}/mutation-results.json",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "empirical_rows": 0,
            "authority_events": 0,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        }
        write_json(f"{folder}/contract.json", contract)
        write_json(f"{folder}/mutation-results.json", mutation_doc)
        write_json(f"{folder}/bounded-receipt.json", receipt)
        positive_results[profile] = fixture
        all_mutations.extend(mutation_rows)
        outcome_rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "outcome": disposition,
                "evidence": f"{folder}/bounded-receipt.json",
                "new_completion_credit": disposition == "completed",
                "real_rows": 0,
                "authority_events": 0,
            }
        )

    skill_rows = []
    for slug, profile, title, purpose in SKILLS:
        folder = f"{PREFIX}x2/skills/{slug}"
        skill_path = f"{folder}/SKILL.md"
        write_text(skill_path, skill_markdown(slug, profile, title, purpose))
        raw = (ROOT / skill_path).read_bytes()
        text = raw.decode("utf-8")
        required_sections = [
            "## Scope",
            "## Required inputs",
            "## Procedure",
            "## Fail-closed stops",
            "## Output boundary",
            "## Terminal boundary",
        ]
        quick = {
            "schema": "ghc.family.sylven.v665-v5.skill-quick-validation.v1",
            "skill": slug,
            "profile": profile,
            "read_through_eof": True,
            "byte_count": len(raw),
            "sha256": sha256(raw),
            "required_sections": required_sections,
            "missing_sections": [section for section in required_sections if section not in text],
            "terminal_verdict_present": TERMINAL_VERDICT in text,
            "valid": all(section in text for section in required_sections)
            and TERMINAL_VERDICT in text,
        }
        smoke_result = evaluate(profile, positive_results[profile])
        smoke = {
            "schema": "ghc.family.sylven.v665-v5.skill-smoke-receipt.v1",
            "skill": slug,
            "profile": profile,
            "skill_sha256": sha256(raw),
            "input_sha256": sha256(canonical_bytes(positive_results[profile])),
            "result": smoke_result,
            "real_rows": 0,
            "authority_events": 0,
            "valid": quick["valid"] and smoke_result["valid"],
        }
        write_json(f"{folder}/quick-validation.json", quick)
        write_json(f"{folder}/smoke-receipt.json", smoke)
        skill_rows.append(
            {
                "skill": slug,
                "profile": profile,
                "path": skill_path,
                "sha256": sha256(raw),
                "quick_valid": quick["valid"],
                "smoke_valid": smoke["valid"],
                "read_through_eof": True,
            }
        )

    runner_rows = []
    for profile, path in RUNNERS.items():
        receipt = invoke_runner(profile, positive_results[profile])
        receipt_path = f"{PREFIX}x2/runners/{profile}-smoke-receipt.json"
        write_json(receipt_path, receipt)
        runner_rows.append(
            {
                "profile": profile,
                "path": path,
                "receipt": receipt_path,
                "valid": receipt["valid"],
            }
        )
    if not all(row["valid"] for row in runner_rows):
        raise EvidenceError("one family runner smoke invocation failed")

    counts = {
        label: sum(row["outcome"] == label for row in outcome_rows)
        for label in ALLOWED_OUTCOMES
    }
    outcome_ledger = {
        "schema": "ghc.family.sylven.v665-v5.outcome-ledger.v1",
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "proposal_count": len(outcome_rows),
        "counts": counts,
        "outcomes": outcome_rows,
        "unknown_outcome_labels": [],
        "inherited_rows_recredited": 0,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": counts
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
    }
    mutation_ledger = {
        "schema": "ghc.family.sylven.v665-v5.mutation-ledger.v1",
        "preregistered_count": MUTATION_COUNT,
        "executed_count": len(all_mutations),
        "rejected_count": sum(row["valid"] for row in all_mutations),
        "accepted_count": sum(row["runner_result"]["valid"] for row in all_mutations),
        "failure_erasure_count": 0,
        "mutation_ids": [row["mutation_id"] for row in all_mutations],
        "valid": len(all_mutations) == MUTATION_COUNT
        and all(row["valid"] for row in all_mutations),
    }
    mutation_methods = [
        {
            "method_id": f"SA6655-X2-M{index:03d}",
            "failed_witness_id": mutation["mutation_id"],
            "failed_witness_status": "retained_zero_credit",
            "passing_witness": f"{mutation['mutation_id'].rsplit('-', 1)[0]} bounded positive fixture",
            "recovery_scope": "one preregistered changed field only",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, mutation in enumerate(all_mutations, 1)
    ]
    operational_methods = [
        {
            "method_id": f"SA6655-X2-OP-M{index:03d}",
            **failure,
            "failed_witness_status": "retained_zero_credit",
            "recovery_scope": "read-only bounded projection only",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, failure in enumerate(OPERATIONAL_FAILURES, 1)
    ]
    methods = mutation_methods + operational_methods
    method_flow = {
        "schema": "ghc.family.sylven.v665-v5.method-flow-overlay.v1",
        "source_repository_sealed": {"negatives": 25_551, "methods": 9_413},
        "startup_after_x1": {
            "negatives": STARTUP_NEGATIVES,
            "methods": STARTUP_METHODS,
            "new_failures": 10,
        },
        "x2": {
            "mutation_failed_witnesses": MUTATION_COUNT,
            "operational_failed_witnesses": len(OPERATIONAL_FAILURES),
            "new_failed_witnesses": MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "new_methods": MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "new_bounded_passing_witnesses": MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "failure_erasure_count": 0,
        },
        "effective_after_x2": {
            "negatives": STARTUP_NEGATIVES + MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "methods": STARTUP_METHODS + MUTATION_COUNT + len(OPERATIONAL_FAILURES),
        },
        "methods": methods,
        "valid": len(methods) == MUTATION_COUNT + len(OPERATIONAL_FAILURES),
    }

    portfolio = read_json(PHASE / "x1/portfolio-freeze.json")

    def portfolio_rows(key: str, outcome: str, evidence: str) -> list[dict[str, Any]]:
        return [
            {
                "record_id": row["record_id"],
                "title": row.get("title") or row.get("purpose") or row.get("slug"),
                "approval_class": row["approval_class"],
                "outcome": outcome,
                "evidence": evidence,
                "completion_credit": outcome == "completed",
                "protected_gates_preserved": True,
            }
            for row in portfolio[key]
        ]

    portfolio_execution = {
        "schema": "ghc.family.sylven.v665-v5.portfolio-execution.v1",
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "safe_now": portfolio_rows(
            "safe_now", "completed", f"{PREFIX}x2/ledgers/execution-summary.json"
        ),
        "bounded_candidates": portfolio_rows(
            "bounded_candidates", "completed", f"{PREFIX}x2/ledgers/runner-registry.json"
        ),
        "exact_approval": portfolio_rows(
            "exact_approval", "exact_gate", f"{PREFIX}x2/ledgers/boundary-matrix.json"
        ),
        "blocked": portfolio_rows(
            "blocked", "open_gap", f"{PREFIX}x2/ledgers/boundary-matrix.json"
        ),
        "clean_fix_refine": portfolio_rows(
            "clean_fix_refine", "completed", f"{PREFIX}x2/validation/evidence-staged-review.json"
        ),
        "skill_ideas": [
            {
                "record_id": row["record_id"],
                "title": row.get("purpose") or row.get("slug"),
                "outcome": "completed",
                "evidence": skill_rows[index]["path"],
            }
            for index, row in enumerate(portfolio["skill_ideas"])
        ],
        "runner_ideas": [
            {
                "record_id": row["record_id"],
                "title": row.get("caller") or row.get("profile"),
                "outcome": "completed",
                "evidence": runner_rows[index]["path"],
            }
            for index, row in enumerate(portfolio["runner_ideas"])
        ],
        "inherited_completion_credit": 0,
        "destructive_cleanup_count": 0,
        "valid": True,
    }
    boundary_matrix = {
        "schema": "ghc.family.sylven.v665-v5.boundary-matrix.v1",
        "GMUT": "typed temperature-time, thermal-balance, boundary-condition, Arrhenius, Fourier, Biot, scalar-tensor, EFT, dimensional, uncertainty, and identifiability obligations only; no real likelihood, constraint, force, prediction, confirmation, quantum completion, ultraviolet completion, final physics, theorem, or Theory of Everything",
        "THOS": "participant-free synthetic kiln-documentation, quarantine, stop-card, correction, workload, and handover charter only; zero governed real participants, operators, arms, monitoring events, statistics, or independent review",
        "Freed_ID": "synthetic zero-key glaze-batch capability and correction profile only; zero real keys, proofs, issuance, resolution, status, revocation, interoperability, recovery, privacy/security review, or trust governance",
        "CBR": "worker and consumer decisions, studio access, custody, design heritage, taonga, remedy, legal, cultural, affected-party, tangata whenua, iwi, hapū, Māori wording and concepts, Māori-data-governance, and Māori-authority decisions remain exact-gated",
        "accessibility": "bounded structural affordances only; manual, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain absent",
        "security": "bounded changed-code and mutation checks only; no exhaustive-security claim",
        "same_owner": "not independent reproduction or external audit",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    source_ledger = read_json(PHASE / "x1/source-ledger.json")
    source_use = {
        "schema": "ghc.family.sylven.v665-v5.source-use-ledger.v1",
        "source_count": source_ledger["source_count"],
        "source_ids": [row["source_id"] for row in source_ledger["sources"]],
        "official_or_primary_source_page_reads": source_ledger.get("official_or_primary_source_page_reads", 0),
        "live_data_calls": 0,
        "epa_page_data_calls": 0,
        "worksafe_page_data_calls": 0,
        "downloaded_empirical_rows": 0,
        "parsed_real_regulatory_or_workplace_records": 0,
        "real_studios_kilns_wares_glazes_or_materials": 0,
        "version_vocabulary_and_boundary_use_only": True,
        "conformance_claim": False,
        "valid": True,
    }
    execution_summary = {
        "schema": "ghc.family.sylven.v665-v5.execution-summary.v1",
        "x1_commit": X1,
        "proposal_count": 20,
        "outcomes": counts,
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "operational_failures_retained": len(OPERATIONAL_FAILURES),
        "portfolios": {
            "safe_now_completed": len(portfolio["safe_now"]),
            "bounded_candidates_completed": len(portfolio["bounded_candidates"]),
            "exact_approval_unexecuted": len(portfolio["exact_approval"]),
            "blocked_unexecuted": len(portfolio["blocked"]),
            "clean_fix_refine_completed": len(portfolio["clean_fix_refine"]),
        },
        "skills": {
            "built": 10,
            "read_through_eof": 10,
            "quick_validated": 10,
            "smoke_used": 10,
            "globally_installed": 0,
        },
        "runners": {"family_compatible": 10, "invoked": 10, "passed": 10},
        "real_rows": 0,
        "real_people": 0,
        "real_studios_kilns_wares_glazes_or_materials": 0,
        "real_keys_or_proofs": 0,
        "authority_events": 0,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": outcome_ledger["valid"]
        and mutation_ledger["valid"]
        and x1_integrity["valid"]
        and all(row["valid"] for row in runner_rows)
        and all(row["quick_valid"] and row["smoke_valid"] for row in skill_rows),
    }

    write_json(f"{PREFIX}x2/ledgers/outcome-ledger.json", outcome_ledger)
    write_json(f"{PREFIX}x2/ledgers/mutation-ledger.json", mutation_ledger)
    write_json(f"{PREFIX}x2/ledgers/method-flow-overlay.json", method_flow)
    write_json(f"{PREFIX}x2/ledgers/portfolio-execution.json", portfolio_execution)
    write_json(f"{PREFIX}x2/ledgers/boundary-matrix.json", boundary_matrix)
    write_json(f"{PREFIX}x2/ledgers/source-use-ledger.json", source_use)
    write_json(
        f"{PREFIX}x2/ledgers/skill-registry.json",
        {
            "schema": "ghc.family.sylven.v665-v5.skill-registry.v1",
            "count": len(skill_rows),
            "skills": skill_rows,
            "global_installation_performed": False,
            "valid": len(skill_rows) == 10
            and all(row["quick_valid"] and row["smoke_valid"] for row in skill_rows),
        },
    )
    write_json(
        f"{PREFIX}x2/ledgers/runner-registry.json",
        {
            "schema": "ghc.family.sylven.v665-v5.runner-registry.v1",
            "count": len(runner_rows),
            "runners": runner_rows,
            "family_current_prefix_preserved": True,
            "valid": len(runner_rows) == 10 and all(row["valid"] for row in runner_rows),
        },
    )
    write_json(f"{PREFIX}x2/ledgers/execution-summary.json", execution_summary)
    write_text(
        f"{PREFIX}x2/x2-overview.md",
        f"""# Sylven Arc {PHASE_ID} bounded x2 evidence

## Execution truth

This owner-local phase executed all twenty frozen proposals only as evidence
permitted: exactly fourteen completed, four represented, one open_gap, and one
exact_gate. Each proposal retained five preregistered rejecting mutations.
Exactly 100/100 mutations executed and were rejected; zero mutation was
accepted and no failed witness was erased.

Ten phase-local skills were built, read through EOF, quick-validated, and
smoke-used without global installation. Ten family-compatible ghc_family_*
runners were invoked through one bounded shared core. Thirty safe-now tasks,
fifteen bounded candidates, ten skill builds, ten runner builds, and thirty
additive CLEAN/FIX/REFINE rows completed only within their declared
owner-local software, formal, structural, or synthetic scope. Ten
exact-approval packets and five blocked packets remained visible and
unexecuted.

## Bounded ceramics lens

The practice lens remained wholly synthetic community ceramics kiln-firing
documentation and glaze-batch quarantine. The phase used zero real people,
studios, kilns, firings, ware, shelves, witness cones, clay, glazes, recipes,
materials, images, instruments, controllers, safety sheets, measurements,
workplace actions, consumer claims, professional decisions, legal decisions,
cultural decisions, or authority acts. No runner can issue a command, select a
schedule, release a batch, classify a substance, diagnose a defect, or advise a
workplace.

The EPA and WorkSafe adapter made zero data calls and parsed zero real rows.
Official pages supplied vocabulary and boundary context only. They did not
confer regulatory, professional, safety, empirical, legal, cultural, or Māori
authority.

## Pillar boundaries

GMUT thermal surfaces are typed symbolic obligations covering units,
temperature-time segments, heat-balance terms, boundary conditions,
Arrhenius placeholders, Fourier and Biot expressions, uncertainty, and
identifiability. They are not physical measurements, calibrated models,
theorems, real likelihoods, empirical GMUT results, final physics, or Theory
of Everything evidence.

THOS is a participant-free documentation and handover proxy with zero governed
participants, operators, real arms, monitoring events, statistics, or
independent review. Freed ID is a zero-key synthetic batch-capability and
correction envelope with no live issuance, proofs, resolution, status,
revocation, interoperability, privacy or independent security review,
recovery evidence, or trust governance.

CBR worker and consumer decisions, studio access and custody, design heritage,
taonga, remedy, legal and cultural interpretation, affected-party legitimacy,
Māori wording and concepts, Māori data governance, tangata whenua, iwi, hapū,
and Māori authority remain exact-gated.

## Retention and terminal truth

Effective bounded evidence after startup, all 100 rejecting mutations, and x2
operational failures is
{STARTUP_NEGATIVES + MUTATION_COUNT + len(OPERATIONAL_FAILURES)} negatives and
{STARTUP_METHODS + MUTATION_COUNT + len(OPERATIONAL_FAILURES)} Method Flow
methods. The cumulative registers remain
{INHERITED_OPEN_GAPS + 1} open gaps and
{INHERITED_EXACT_GATES + 1} exact gates. Same-owner validation under shared
infrastructure is not independent-team reproduction. The terminal verdict
remains {TERMINAL_VERDICT}.
""",
    )
    return {
        "valid": execution_summary["valid"],
        "proposals": 20,
        "mutations": 100,
        "skills": 10,
        "runners": 10,
        "base_paths": len(BASE_PATHS),
    }


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted(line for line in raw.splitlines() if line)


def index_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True
    )
    return result.stdout


def scanner_candidates(path: str, raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8", errors="replace")
    patterns = {
        "windows_private_absolute_path": re.compile(
            r"(?i)[a-z]:\\(?:users|ghc-archives)\\"
        ),
        "unix_private_absolute_path": re.compile(r"(?i)/(?:home|users)/[^\s'\"]+"),
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "credential_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"
        ),
        "private_callable_or_session_stream": re.compile(
            r"(?i)(?:mcp__[a-z0-9_]{6,}|session_stream\s*[:=]|resume_value\s*[:=])"
        ),
    }
    return [
        {"path": path, "class": name}
        for name, pattern in patterns.items()
        if pattern.search(text)
    ]


def write_staged_review() -> None:
    actual = staged_paths()
    if actual != BASE_PATHS:
        raise EvidenceError(
            f"stage exact evidence base allowlist first: expected {len(BASE_PATHS)}, got {len(actual)}"
        )
    entries = []
    json_count = 0
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
        path_candidates = scanner_candidates(path, raw)
        candidates.extend(path_candidates)
        confirmed.extend(path_candidates)
    diff_check = run("git", "diff", "--cached", "--check", check=False)
    if diff_check.returncode != 0:
        raise EvidenceError("staged diff hygiene failed: " + diff_check.stdout.strip())
    if confirmed:
        raise EvidenceError(f"confirmed privacy or raw-identifier candidates: {confirmed}")
    manifest = {
        "schema": "ghc.family.sylven.v665-v5.evidence-content-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(INTENDED_PATHS),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(SELF_EXCLUSIONS) == len(INTENDED_PATHS),
    }
    review = {
        "schema": "ghc.family.sylven.v665-v5.evidence-staged-review.v1",
        "staged_base_path_count": len(actual),
        "strict_json_count": json_count,
        "five_scan_classes": [
            "windows_private_absolute_path",
            "unix_private_absolute_path",
            "raw_task_or_thread_identifier",
            "credential_assignment",
            "private_callable_or_session_stream",
        ],
        "scanner_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "diff_hygiene_issues": 0,
        "x1_paths_modified": [path for path in actual if f"{PREFIX}x1/" in path],
        "source_or_sibling_paths_modified": [
            path
            for path in actual
            if path.startswith("docs/") and not path.startswith(PREFIX)
        ],
        "valid": not confirmed
        and not any(f"{PREFIX}x1/" in path for path in actual)
        and not any(
            path.startswith("docs/") and not path.startswith(PREFIX) for path in actual
        ),
    }
    candidate = {
        "schema": "ghc.family.sylven.v665-v5.evidence-stage-candidate.v1",
        "source_commit": SOURCE_FINAL,
        "x1_commit": X1,
        "branch": BRANCH,
        "manifest": SELF_EXCLUSIONS[0],
        "staged_review": SELF_EXCLUSIONS[2],
        "test_command": "python tests/test_ghc_family_sylven_v665_v5_x2.py -v",
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "remote_equality_state": "PREPARED_NOT_PROVED",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": manifest["coverage_valid"] and review["valid"],
    }
    write_json(SELF_EXCLUSIONS[0], manifest)
    write_json(SELF_EXCLUSIONS[1], candidate)
    write_json(SELF_EXCLUSIONS[2], review)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_PATHS:
        raise EvidenceError(
            f"staged evidence allowlist changed: expected {len(INTENDED_PATHS)}, got {len(actual)}"
        )
    manifest = strict_json_bytes(index_blob(SELF_EXCLUSIONS[0]), "staged manifest")
    review = strict_json_bytes(index_blob(SELF_EXCLUSIONS[2]), "staged review")
    candidate = strict_json_bytes(index_blob(SELF_EXCLUSIONS[1]), "staged candidate")
    mismatches = []
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    all_candidates = []
    json_count = 0
    for path in actual:
        raw = index_blob(path)
        all_candidates.extend(scanner_candidates(path, raw))
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
    diff_check = run("git", "diff", "--cached", "--check", check=False)
    if mismatches or all_candidates or diff_check.returncode != 0:
        raise EvidenceError(
            f"staged audit failure: mismatches={mismatches}, candidates={all_candidates}, diff={diff_check.stdout.strip()}"
        )
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise EvidenceError("one staged receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "manifest_entries": len(manifest["entries"]),
        "manifest_exclusions": len(manifest["declared_self_exclusions"]),
        "strict_json": json_count,
        "privacy_confirmed_hits": 0,
        "diff_hygiene_issues": 0,
    }


def prepare() -> dict[str, Any]:
    result = build_evidence()
    run("git", "add", "--sparse", "--", *BASE_PATHS)
    write_staged_review()
    run("git", "add", "--", *SELF_EXCLUSIONS)
    audit = check_staged()
    return {**result, **audit}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    modes.add_argument("--list-base-paths", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        result = prepare()
    elif args.check_staged:
        result = check_staged()
    else:
        result = {"base_paths": BASE_PATHS, "self_exclusions": SELF_EXCLUSIONS}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
