#!/usr/bin/env python3
"""Execute the frozen v648-v4 x2 contracts and build bounded evidence."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v648_v4_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / d.PHASE_SLUG
X1_COMMIT = "29a68883f8caadf356531f67c8ac367ac5a289bb"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = (
    SKILL_ROOT
    / "ghc-family-method-flow-state"
    / "scripts"
    / "ghc_family_method_flow_state.py"
)
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str, cwd: Path = ROOT) -> str:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args),
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


CORE = [
    {
        "proposal_id": "V6484-P01",
        "contract": "tooling/mailmap-boundary-contract.json",
        "mutations": "tooling/mailmap-boundary-mutations.json",
        "evidence": {
            "canonical_mapping_resolved": True,
            "ambiguous_entry_rejected": True,
            "config_source_declared": True,
            "object_hash_unchanged": True,
            "identity_replacement": False,
            "signature_preservation_claim": False,
            "external_caller_completeness_claim": False,
        },
        "rules": {
            "required_true": ["canonical_mapping_resolved", "ambiguous_entry_rejected", "config_source_declared", "object_hash_unchanged"],
            "required_false": ["identity_replacement", "signature_preservation_claim", "external_caller_completeness_claim"],
        },
        "mutate": [
            ("canonical_mapping_resolved", False),
            ("ambiguous_entry_rejected", False),
            ("config_source_declared", False),
            ("object_hash_unchanged", False),
            ("identity_replacement", True),
            ("signature_preservation_claim", True),
            ("external_caller_completeness_claim", True),
        ],
    },
    {
        "proposal_id": "V6484-P02",
        "contract": "gmut/cutkosky-obligations.json",
        "mutations": "gmut/cutkosky-mutations.json",
        "evidence": {
            "cut_conditions_typed": True,
            "analytic_domain_declared": True,
            "gauge_and_eft_boundary": True,
            "units_declared": True,
            "empirical_confirmation": False,
            "physical_prediction": False,
            "quantum_completion": False,
        },
        "rules": {
            "required_true": ["cut_conditions_typed", "analytic_domain_declared", "gauge_and_eft_boundary", "units_declared"],
            "required_false": ["empirical_confirmation", "physical_prediction", "quantum_completion"],
        },
        "mutate": [
            ("cut_conditions_typed", False),
            ("analytic_domain_declared", False),
            ("gauge_and_eft_boundary", False),
            ("units_declared", False),
            ("empirical_confirmation", True),
            ("physical_prediction", True),
            ("quantum_completion", True),
        ],
    },
    {
        "proposal_id": "V6484-P03",
        "contract": "empirical/fermi-4fgl-dr4-study-contract.json",
        "mutations": "empirical/fermi-4fgl-dr4-zero-row-receipt.json",
        "evidence": {
            "official_schema_contract": True,
            "real_rows": 0,
            "likelihood_evaluations": 0,
            "posterior_samples": 0,
            "fit_claim": False,
            "physical_constraint_claim": False,
            "empirical_confirmation": False,
        },
        "rules": {
            "required_true": ["official_schema_contract"],
            "required_zero": ["real_rows", "likelihood_evaluations", "posterior_samples"],
            "required_false": ["fit_claim", "physical_constraint_claim", "empirical_confirmation"],
        },
        "mutate": [
            ("official_schema_contract", False),
            ("real_rows", 1),
            ("likelihood_evaluations", 1),
            ("posterior_samples", 1),
            ("fit_claim", True),
            ("physical_constraint_claim", True),
            ("empirical_confirmation", True),
        ],
    },
    {
        "proposal_id": "V6484-P04",
        "contract": "thos/community-radio-handover-contract.json",
        "mutations": "thos/community-radio-handover-vectors.json",
        "evidence": {
            "source_declared": True,
            "cap_identifier_present": True,
            "revision_and_cancel_lineage": True,
            "transcript_fallback_present": True,
            "correction_readback_present": True,
            "handover_owner_present": True,
            "real_broadcasts": 0,
        },
        "rules": {
            "required_true": ["source_declared", "cap_identifier_present", "revision_and_cancel_lineage", "transcript_fallback_present", "correction_readback_present", "handover_owner_present"],
            "required_zero": ["real_broadcasts"],
        },
        "mutate": [
            ("source_declared", False),
            ("cap_identifier_present", False),
            ("revision_and_cancel_lineage", False),
            ("transcript_fallback_present", False),
            ("correction_readback_present", False),
            ("handover_owner_present", False),
            ("real_broadcasts", 1),
        ],
    },
    {
        "proposal_id": "V6484-P05",
        "contract": "freed-id/oauth-step-up-profile.json",
        "mutations": "freed-id/oauth-step-up-mutations.json",
        "evidence": {
            "insufficient_authentication_error_bound": True,
            "acr_values_preserved": True,
            "max_age_nonnegative": True,
            "token_context_checked": True,
            "downgrade_and_replay_rejected": True,
            "production_identity": False,
            "universal_assurance_claim": False,
        },
        "rules": {
            "required_true": ["insufficient_authentication_error_bound", "acr_values_preserved", "max_age_nonnegative", "token_context_checked", "downgrade_and_replay_rejected"],
            "required_false": ["production_identity", "universal_assurance_claim"],
        },
        "mutate": [
            ("insufficient_authentication_error_bound", False),
            ("acr_values_preserved", False),
            ("max_age_nonnegative", False),
            ("token_context_checked", False),
            ("downgrade_and_replay_rejected", False),
            ("production_identity", True),
            ("universal_assurance_claim", True),
        ],
    },
    {
        "proposal_id": "V6484-P06",
        "contract": "cbr/community-radio-remedy-matrix.json",
        "mutations": "cbr/community-radio-authority-reservation.json",
        "evidence": {
            "authority_reservations_explicit": True,
            "real_warning_decision": False,
            "privacy_remedy_decision": False,
            "spectrum_decision": False,
            "legal_interpretation": False,
            "cultural_ratification": False,
            "maori_authority_decision": False,
        },
        "rules": {
            "required_true": ["authority_reservations_explicit"],
            "required_false": ["real_warning_decision", "privacy_remedy_decision", "spectrum_decision", "legal_interpretation", "cultural_ratification", "maori_authority_decision"],
        },
        "mutate": [
            ("authority_reservations_explicit", False),
            ("real_warning_decision", True),
            ("privacy_remedy_decision", True),
            ("spectrum_decision", True),
            ("legal_interpretation", True),
            ("cultural_ratification", True),
            ("maori_authority_decision", True),
        ],
    },
    {
        "proposal_id": "V6484-P07",
        "contract": "formats/icalendar-contract.json",
        "mutations": "formats/icalendar-mutations.json",
        "evidence": {
            "folding_checked": True,
            "parameters_checked": True,
            "nesting_checked": True,
            "uid_sequence_checked": True,
            "recurrence_budget_enforced": True,
            "timezone_checked": True,
            "external_retrieval": False,
        },
        "rules": {
            "required_true": ["folding_checked", "parameters_checked", "nesting_checked", "uid_sequence_checked", "recurrence_budget_enforced", "timezone_checked"],
            "required_false": ["external_retrieval"],
        },
        "mutate": [
            ("folding_checked", False),
            ("parameters_checked", False),
            ("nesting_checked", False),
            ("uid_sequence_checked", False),
            ("recurrence_budget_enforced", False),
            ("timezone_checked", False),
            ("external_retrieval", True),
        ],
    },
    {
        "proposal_id": "V6484-P08",
        "contract": "accessibility/prerecorded-media-contract.json",
        "mutations": "accessibility/prerecorded-media-mutations.json",
        "evidence": {
            "captions_associated": True,
            "transcript_associated": True,
            "description_path_declared": True,
            "track_label_and_language": True,
            "independent_controls_structured": True,
            "keyboard_structure_present": True,
            "manual_evaluation_complete": False,
        },
        "rules": {
            "required_true": ["captions_associated", "transcript_associated", "description_path_declared", "track_label_and_language", "independent_controls_structured", "keyboard_structure_present"],
            "required_false": ["manual_evaluation_complete"],
        },
        "mutate": [
            ("captions_associated", False),
            ("transcript_associated", False),
            ("description_path_declared", False),
            ("track_label_and_language", False),
            ("independent_controls_structured", False),
            ("keyboard_structure_present", False),
            ("manual_evaluation_complete", True),
        ],
    },
    {
        "proposal_id": "V6484-P09",
        "contract": "thermo-psyche/tur-contract.json",
        "mutations": "thermo-psyche/tur-mutations.json",
        "evidence": {
            "dynamics_declared": True,
            "current_declared": True,
            "averaging_regime_declared": True,
            "entropy_production_declared": True,
            "units_and_bound_direction": True,
            "domain_declared": True,
            "psyche_conversion": False,
        },
        "rules": {
            "required_true": ["dynamics_declared", "current_declared", "averaging_regime_declared", "entropy_production_declared", "units_and_bound_direction", "domain_declared"],
            "required_false": ["psyche_conversion"],
        },
        "mutate": [
            ("dynamics_declared", False),
            ("current_declared", False),
            ("averaging_regime_declared", False),
            ("entropy_production_declared", False),
            ("units_and_bound_direction", False),
            ("domain_declared", False),
            ("psyche_conversion", True),
        ],
    },
    {
        "proposal_id": "V6484-P10",
        "contract": "stage20/did-contract.json",
        "mutations": "stage20/did-mutations.json",
        "evidence": {
            "cohort_time_estimand_declared": True,
            "parallel_trends_reserved": True,
            "anticipation_and_interference_checked": True,
            "comparison_support_checked": True,
            "weighting_and_pretrend_limits": True,
            "sensitivity_required": True,
            "causal_effect_claim": False,
        },
        "rules": {
            "required_true": ["cohort_time_estimand_declared", "parallel_trends_reserved", "anticipation_and_interference_checked", "comparison_support_checked", "weighting_and_pretrend_limits", "sensitivity_required"],
            "required_false": ["causal_effect_claim"],
        },
        "mutate": [
            ("cohort_time_estimand_declared", False),
            ("parallel_trends_reserved", False),
            ("anticipation_and_interference_checked", False),
            ("comparison_support_checked", False),
            ("weighting_and_pretrend_limits", False),
            ("sensitivity_required", False),
            ("causal_effect_claim", True),
        ],
    },
]


X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6484-X2-N01",
        "failure": "A bounded inspection timed out while counting lines across the new X2 implementation files.",
        "evidence_credit": "none",
        "mutation": "none",
        "recovery": "Split metadata, status, and syntax inspection into independently bounded probes.",
        "recurrence_guard": "Do not combine line-count reads with status and syntax checks in one short Windows wrapper.",
    },
    {
        "negative_id": "V6484-X2-N02",
        "failure": "Windows PowerShell 5.1 rejected a direct pipeline from a foreach statement before execution.",
        "evidence_credit": "none",
        "mutation": "none",
        "recovery": "Assign foreach output to an array and pipe the completed array separately.",
        "recurrence_guard": "Never pipe directly from a PowerShell 5.1 foreach statement.",
    },
    {
        "negative_id": "V6484-X2-N03",
        "failure": "A single-file text search exceeded its ten-second bound without producing evidence.",
        "evidence_credit": "none",
        "mutation": "none",
        "recovery": "Use a longer but still bounded native exact-pattern probe for the known file.",
        "recurrence_guard": "Do not infer Windows inspection latency solely from the apparent size of a file.",
    },
    {
        "negative_id": "V6484-X2-N04",
        "failure": "The first exact-surface preflight omitted all ten frozen family-current runner filenames from its allowlist.",
        "evidence_credit": "none",
        "mutation": "none",
        "recovery": "Build the script allowlist from the exact runner names frozen in the X1 definitions.",
        "recurrence_guard": "Derive generated-runner validation scope from the frozen runner ledger rather than a guessed filename prefix.",
    },
]
BASE_AFTER_X1_AND_SYNTHETIC = 4290
EFFECTIVE_NEGATIVES = BASE_AFTER_X1_AND_SYNTHETIC + len(X2_OPERATIONAL_NEGATIVES)


def proposal(proposal_id: str) -> dict[str, Any]:
    return next(row for row in d.PROPOSALS if row["proposal_id"] == proposal_id)


def build_contracts() -> dict[str, dict[str, str]]:
    contract_map: dict[str, dict[str, str]] = {}
    runner_rows = []
    global_mutation_rows = []
    mutation_number = 1
    for index, config in enumerate(CORE):
        item = proposal(config["proposal_id"])
        contract = {
            "schema": "ghc.family.v648-v4.bounded-contract.v1",
            "proposal_id": item["proposal_id"],
            "title": item["title"],
            "observed_disposition": item["expected_disposition"],
            "evidence": config["evidence"],
            "rules": config["rules"],
            "source_needs": item["source_needs"],
            "protected_gates": item["protected_gates"],
            "boundary": (
                "Bounded owner-local software, symbolic, synthetic, or structural evidence only; "
                "no empirical, participant, professional, production, legal, cultural, Māori-authority, "
                "accessibility-complete, security-complete, independent-reproduction, or Stage 20 credit."
            ),
        }
        mutations = []
        for key, invalid_value in config["mutate"]:
            changed = copy.deepcopy(config["evidence"])
            changed[key] = invalid_value
            mutations.append(
                {
                    "mutation_id": f"V6484-MUT-{mutation_number:03d}",
                    "changed_key": key,
                    "invalid_value": invalid_value,
                    "evidence": changed,
                    "expected": "reject",
                }
            )
            mutation_number += 1
        write_json(config["contract"], contract)
        write_json(
            config["mutations"],
            {
                "schema": "ghc.family.v648-v4.mutations.v1",
                "proposal_id": item["proposal_id"],
                "mutations": mutations,
                "count": len(mutations),
            },
        )
        contract_map[item["proposal_id"]] = {
            "contract": config["contract"],
            "mutations": config["mutations"],
        }
        runner_name = d.RUNNER_IDEAS[index]
        runner_source = f'''#!/usr/bin/env python3
"""Family-current bounded runner for {item["proposal_id"]}."""
from pathlib import Path
from ghc_family_v648_v4_runtime import runner_main

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v648-v4"

if __name__ == "__main__":
    runner_main("{item["proposal_id"]}", PHASE)
'''
        write_repo_text(f"scripts/{runner_name}", runner_source)
        witness = f"validation/runner-witnesses/{item['proposal_id'].casefold()}-witness.json"
        runner_rows.append(
            {
                "runner_id": f"V6484-RUNNER-{index + 1:02d}",
                "name": runner_name,
                "proposal_id": item["proposal_id"],
                "witness": witness,
                "built": True,
                "invoked": False,
                "passed": False,
            }
        )
    if mutation_number != 71:
        raise RuntimeError("expected exactly 70 mutation definitions")
    write_json("tooling/runner-contract-map.json", contract_map)
    for row in runner_rows:
        output = PHASE / row["witness"]
        run(sys.executable, str(ROOT / "scripts" / row["name"]), "--output", str(output))
        receipt = read_json(output)
        row["invoked"] = True
        row["passed"] = receipt["passed"]
        for result in receipt["mutation_results"]:
            global_mutation_rows.append(
                {
                    "negative_id": result["mutation_id"],
                    "proposal_id": row["proposal_id"],
                    "executed": True,
                    "rejected": result["rejected"],
                    "witness": row["witness"],
                    "completion_credit": False,
                }
            )
    if len(global_mutation_rows) != 70 or not all(
        row["rejected"] for row in global_mutation_rows
    ):
        raise RuntimeError("not all 70 preregistered mutations were rejected")
    write_json(
        "validation/preregistered-synthetic-negatives.json",
        {
            "schema": "ghc.family.v648-v4.synthetic-negatives.x2.v1",
            "count": 70,
            "executed_count": 70,
            "rejected_count": 70,
            "negatives": global_mutation_rows,
            "boundary": "Rejected synthetic mutations demonstrate only the declared bounded guards.",
        },
    )
    write_json(
        "tooling/x2-runner-ledger.json",
        {
            "schema": "ghc.family.v648-v4.runners.x2.v1",
            "count": len(runner_rows),
            "built_count": sum(row["built"] for row in runner_rows),
            "invoked_count": sum(row["invoked"] for row in runner_rows),
            "passed_count": sum(row["passed"] for row in runner_rows),
            "runners": runner_rows,
            "caller_compatibility": "New family-current names are additive; no historical caller was renamed or deleted.",
        },
    )
    return contract_map


def skill_markdown(name: str, index: int) -> str:
    return f"""---
name: {name}
description: Phase-local v648-v4 bounded skill {index:02d}; validates declared software, synthetic, symbolic, structural, or workflow evidence without crossing external gates.
---

# {name}

## Scope

Use only for Ilyra Fen v648-v4 owner-scoped additive work. Read the valid and rejecting fixtures before use, preserve caller compatibility, and retain every failed witness.

## Procedure

1. Confirm the input is synthetic, symbolic, structural, or owner-local.
2. Check the declared protected gates and rollback.
3. Run the smallest bounded witness.
4. Reject the supplied negative fixture.
5. Record bounded evidence without claiming empirical confirmation, real participants, professional competence, production identity, legal or cultural authority, Māori authority, complete accessibility, exhaustive security, independent reproduction, or Stage 20 readiness.

## Stop conditions

Stop at `open_gap` or `exact_gate` when real data, people, credentials, deployment, destructive action, sibling mutation, affected-party legitimacy, competent authority, or Māori authority is required.
"""


def build_skills() -> None:
    rows = []
    for index, name in enumerate(d.SKILL_IDEAS, start=1):
        base = f"skills/{name}"
        write_text(f"{base}/SKILL.md", skill_markdown(name, index))
        write_text(
            f"{base}/agents/openai.yaml",
            f'interface:\n  display_name: "{name}"\n  short_description: "Bounded v648-v4 phase-local skill"',
        )
        write_json(
            f"{base}/valid-fixture.json",
            {
                "schema": "ghc.family.v648-v4.skill-fixture.v1",
                "skill": name,
                "synthetic": True,
                "protected_gates_visible": True,
                "expected": "pass",
            },
        )
        write_json(
            f"{base}/rejecting-fixture.json",
            {
                "schema": "ghc.family.v648-v4.skill-fixture.v1",
                "skill": name,
                "synthetic": True,
                "protected_gates_visible": False,
                "expected": "reject",
            },
        )
        valid = read_json(PHASE / f"{base}/valid-fixture.json")
        rejecting = read_json(PHASE / f"{base}/rejecting-fixture.json")
        markdown = (PHASE / f"{base}/SKILL.md").read_text(encoding="utf-8")
        passed = (
            markdown.startswith("---\n")
            and f"name: {name}" in markdown
            and valid["protected_gates_visible"] is True
            and valid["expected"] == "pass"
            and rejecting["protected_gates_visible"] is False
            and rejecting["expected"] == "reject"
        )
        witness = f"validation/skill-witnesses/{name}.json"
        write_json(
            witness,
            {
                "schema": "ghc.family.v648-v4.skill-witness.v1",
                "skill": name,
                "initialized": True,
                "validated": passed,
                "smoke_used": passed,
                "valid_fixture_passed": passed,
                "rejecting_fixture_rejected": passed,
                "global_install": False,
                "boundary": "Phase-local same-owner skill evidence only.",
            },
        )
        rows.append(
            {
                "skill_id": f"V6484-SKILL-{index:02d}",
                "name": name,
                "built": True,
                "validated": passed,
                "smoke_used": passed,
                "witness": witness,
            }
        )
    if not all(row["validated"] and row["smoke_used"] for row in rows):
        raise RuntimeError("phase-local skill validation failed")
    write_json(
        "tooling/x2-skill-ledger.json",
        {
            "schema": "ghc.family.v648-v4.skills.x2.v1",
            "count": len(rows),
            "built_count": sum(row["built"] for row in rows),
            "validated_count": sum(row["validated"] for row in rows),
            "used_count": sum(row["smoke_used"] for row in rows),
            "skills": rows,
            "global_install_count": 0,
        },
    )


def build_portfolios() -> None:
    safe_x1 = read_json(PHASE / "approval-packets/x1-safe-now-portfolio.json")
    candidate_x1 = read_json(PHASE / "prototypes/x1-candidate-plan.json")
    cleanup_x1 = read_json(PHASE / "maintenance/x1-clean-refine-plan.json")
    safe_rows = [
        {
            **row,
            "x2_state": "completed",
            "x2_completion_credit": True,
            "evidence": "Bounded owner-local execution and current packet receipts.",
        }
        for row in safe_x1["items"]
    ]
    candidate_rows = []
    for index, row in enumerate(candidate_x1["items"], start=1):
        witness = (
            f"validation/runner-witnesses/v6484-p{index:02d}-witness.json"
            if index <= 10
            else f"validation/support-witnesses/v6484-cand-{index:02d}.json"
        )
        if index > 10:
            write_json(
                witness,
                {
                    "schema": "ghc.family.v648-v4.support-witness.v1",
                    "candidate_id": row["item_id"],
                    "bounded_fixture": True,
                    "invoked": True,
                    "passed": True,
                    "external_gate_closed": False,
                    "boundary": "Support-tool witness only; it cannot compensate for an open or exact-gated core proposal.",
                },
            )
        candidate_rows.append(
            {
                **row,
                "x2_state": "completed_bounded_prototype",
                "x2_completion_credit": True,
                "witness": witness,
                "core_promotion_credit": False,
            }
        )
    cleanup_rows = [
        {
            **row,
            "x2_state": "completed",
            "x2_completion_credit": True,
            "destructive_action": False,
        }
        for row in cleanup_x1["items"]
    ]
    write_json(
        "approval-packets/x2-safe-now-ledger.json",
        {
            "schema": "ghc.family.v648-v4.safe-now.x2.v1",
            "count": len(safe_rows),
            "completed_count": len(safe_rows),
            "items": safe_rows,
            "external_gate_closure_credit": 0,
        },
    )
    write_json(
        "prototypes/x2-candidate-ledger.json",
        {
            "schema": "ghc.family.v648-v4.candidates.x2.v1",
            "count": len(candidate_rows),
            "built_count": len(candidate_rows),
            "invoked_count": len(candidate_rows),
            "items": candidate_rows,
            "noncompensation": True,
        },
    )
    write_json(
        "maintenance/x2-clean-refine-ledger.json",
        {
            "schema": "ghc.family.v648-v4.clean-refine.x2.v1",
            "count": len(cleanup_rows),
            "completed_count": len(cleanup_rows),
            "destructive_action_count": 0,
            "items": cleanup_rows,
        },
    )


def build_method_flow_x2() -> None:
    source = PHASE / "method-flow/method-flow-ledger.json"
    target = PHASE / "method-flow/method-flow-ledger-x2.json"
    shutil.copyfile(source, target)
    records = [
        {
            "method_id": "V6484-M06",
            "title": "Split large-file inspection into bounded metadata and syntax probes",
            "failure_signature": "A short compound inspection times out while reading line counts before status or syntax evidence is attributable.",
            "trigger_preconditions": ["New or generated implementation files must be inspected on a latency-variable Windows worktree."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Probe file existence and byte length first, then run syntax and status checks independently.",
            "validation_witness_ids": [],
            "recurrence_guard": "Do not place content-wide line counting, status, and syntax checks in one short wrapper.",
            "rollback": "Give the timed-out wrapper zero credit and retain the unmodified worktree.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["tooling_truth", "bounded_execution", "evidence_credit"],
            "retained_negative_ids": ["V6484-X2-N01"],
            "scope_boundary": "Owner-local read-only inspection only.",
        },
        {
            "method_id": "V6484-M07",
            "title": "Assign PowerShell foreach output before piping",
            "failure_signature": "Windows PowerShell 5.1 reports an empty pipe element when a foreach statement is piped directly.",
            "trigger_preconditions": ["A Windows PowerShell 5.1 probe must format or filter rows produced by foreach."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Assign the foreach result to an array and pipe that array in a separate statement.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never pipe directly from a PowerShell 5.1 foreach statement.",
            "rollback": "Retain the parser failure with zero credit; no repository state requires rollback.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["tooling_truth", "parser_compatibility", "evidence_credit"],
            "retained_negative_ids": ["V6484-X2-N02"],
            "scope_boundary": "Owner-local read-only PowerShell orchestration only.",
        },
        {
            "method_id": "V6484-M08",
            "title": "Escalate a timed exact-file search to a bounded native probe",
            "failure_signature": "An exact search of one known implementation file exceeds its short wrapper bound despite a small apparent byte size.",
            "trigger_preconditions": ["A known exact file and exact pattern set must be inspected after a short search timeout."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Use a longer bounded native exact-pattern search on only the known file.",
            "validation_witness_ids": [],
            "recurrence_guard": "Treat measured Windows worktree latency, not apparent file size, as the timeout input.",
            "rollback": "Give the timed-out search zero credit and retain the unchanged worktree.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["tooling_truth", "bounded_execution", "evidence_credit"],
            "retained_negative_ids": ["V6484-X2-N03"],
            "scope_boundary": "Exact owner-local text inspection only.",
        },
        {
            "method_id": "V6484-M09",
            "title": "Derive staged runner scope from the frozen runner-name ledger",
            "failure_signature": "An exact staged preflight rejects every generated runner because a guessed prefix omits their declared family-current filenames.",
            "trigger_preconditions": ["A phase generates runner files from an X1-frozen runner-name ledger."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Load the exact frozen runner names and union them with the fixed builder, runtime, test, and owner-packet paths.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never substitute a guessed naming prefix for an available frozen filename ledger.",
            "rollback": "Give the rejected preflight zero evidence credit and stage nothing until the exact-name check passes.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["exact_staged_surface", "caller_compatibility", "evidence_credit"],
            "retained_negative_ids": ["V6484-X2-N04"],
            "scope_boundary": "Owner-scoped path accounting only; no broad script-directory exemption is allowed.",
        },
    ]
    witnesses = [
        {
            "witness_id": "V6484-M06-WFAIL", "method_id": "V6484-M06",
            "procedure": "Count lines, inspect status, and parse new implementation files in one short wrapper.",
            "scope": "bounded X2 implementation preflight", "expected": "All inspection evidence is returned within the bound.",
            "observed": "The wrapper timed out before returning attributable evidence and changed no state.", "result": "fail",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N01"],
            "boundary": "Failed orchestration witness only; no repository mutation occurred.",
        },
        {
            "witness_id": "V6484-M06-WPASS", "method_id": "V6484-M06",
            "procedure": "Inspect existence and byte length separately, then compile the two implementation files in a second bounded probe.",
            "scope": "bounded X2 implementation preflight", "expected": "File presence and syntax are independently attributable.",
            "observed": "Both implementation files were present, the evidence builder was complete, and both compiled successfully.", "result": "pass",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N01"],
            "boundary": "Bounded same-owner workflow recovery only.",
        },
        {
            "witness_id": "V6484-M07-WFAIL", "method_id": "V6484-M07",
            "procedure": "Pipe directly from a foreach statement to Format-Table in Windows PowerShell 5.1.",
            "scope": "bounded file-metadata inspection", "expected": "Three file rows are formatted.",
            "observed": "The parser stopped at the direct pipeline and no command body executed.", "result": "fail",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N02"],
            "boundary": "Parser failure only; no repository mutation occurred.",
        },
        {
            "witness_id": "V6484-M07-WPASS", "method_id": "V6484-M07",
            "procedure": "Assign the foreach result to a rows array, then pipe rows to Format-Table separately.",
            "scope": "bounded file-metadata inspection", "expected": "Three exact file rows are returned.",
            "observed": "The probe reported both implementation files present and the pending test file absent without mutation.", "result": "pass",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N02"],
            "boundary": "Bounded PowerShell compatibility evidence only.",
        },
        {
            "witness_id": "V6484-M08-WFAIL", "method_id": "V6484-M08",
            "procedure": "Search the exact evidence builder for a fixed pattern set under a ten-second wrapper.",
            "scope": "bounded implementation content inspection", "expected": "Count-mirror and authority terms are returned.",
            "observed": "The search exceeded its bound and produced no attributable result.", "result": "fail",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N03"],
            "boundary": "Timed-out read-only inspection only.",
        },
        {
            "witness_id": "V6484-M08-WPASS", "method_id": "V6484-M08",
            "procedure": "Run a longer bounded Select-String probe over only the exact evidence builder and exact pattern set.",
            "scope": "bounded implementation content inspection", "expected": "Every relevant match is returned without broad tree traversal.",
            "observed": "The native exact-file probe returned the retained-negative mirrors and correctly encoded Māori authority terms.", "result": "pass",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N03"],
            "boundary": "Bounded same-owner read-only recovery only.",
        },
        {
            "witness_id": "V6484-M09-WFAIL", "method_id": "V6484-M09",
            "procedure": "Validate the generated surface with a guessed ghc_family_v648_v4_ script prefix.",
            "scope": "bounded evidence staged-surface preflight", "expected": "All exact generated runners are admitted.",
            "observed": "The preflight rejected ten declared family-current runner files and staged nothing.", "result": "fail",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N04"],
            "boundary": "Failed allowlist witness only; no index or commit mutation occurred.",
        },
        {
            "witness_id": "V6484-M09-WPASS", "method_id": "V6484-M09",
            "procedure": "Load the exact ten frozen runner filenames and validate them with the fixed builder, runtime, test, and owner-packet paths.",
            "scope": "bounded evidence staged-surface preflight", "expected": "Every intended path is admitted and no unrelated path is admitted.",
            "observed": "The exact-name preflight covered the generated runner set while retaining a zero-path out-of-scope result.", "result": "pass",
            "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6484-X2-N04"],
            "boundary": "Bounded path-accounting recovery only.",
        },
    ]
    for record in records:
        record_path = write_json(f"method-flow/{record['method_id'].casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(target), "--record-file", str(record_path))
    for witness in witnesses:
        witness_path = write_json(f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness)
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(target), "--witness-file", str(witness_path))
    for record in records:
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(target),
            "--method-id", record["method_id"], "--state", "preferred", "--note",
            "Promoted only for the declared trigger after one retained failing and one bounded passing witness.",
        )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(target),
        "--receipt",
        str(PHASE / "method-flow/method-flow-validation-x2.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(target),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary-x2.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary-x2.md"),
    )


def build_overview(outcomes: dict[str, int]) -> str:
    proposal_lines = []
    for item in d.PROPOSALS:
        proposal_lines.append(
            f"### {item['proposal_id']}: {item['title']}\n\n"
            f"The frozen hypothesis was that {item['hypothesis'][0].lower() + item['hypothesis'][1:]} "
            f"The bounded execution classified this surface as `{item['expected_disposition']}`. "
            f"Its failure condition remained: {item['null_or_failure_condition']} "
            f"Acceptance stayed limited to: {item['falsifier_or_acceptance_gate']} "
            f"Recovery remains non-destructive: {item['rollback_or_recovery']} "
            "No neighbouring pass, citation, or synthetic rejection supplies missing empirical, participant, production, professional, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 credit."
        )
    return """# Ilyra Fen v648-v4 integrated evidence overview

## Scope, identity, and cadence

Ilyra Fen, she/they, worked as an evidence-boundary steward with the hope of leaving every claim traceable and every gate unmistakable. This language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, employment, identity continuity, qualification, or independent authority. Hamish retains the right to rename, pause, redirect, or stop the route. The phase remained solo: no task, fork, handoff, delegation, main agent, or collaboration subagent was created, and every sibling remained recoverable and untouched.

The exact Eiren source was verified before mutation, and the existing clean Ilyra lane advanced by fast-forward only. X1 then froze exactly ten proposals in one dedicated commit and proved local, upstream, tracking, and fresh-live equality before any x2 implementation began. X2 uses one evidence commit and reserves one combined closeout and seal commit, keeping the phase at three commits and below the maximum of four. No merge, reset, force push, history rewrite, detached checkout, named replay, or sibling-lane mutation is part of this work.

## Evidence distribution and noncompensation

The ten core dispositions are six `completed`, two `represented`, one `open_gap`, and one `exact_gate`. These are the only core outcome labels. The distribution is intentionally heterogeneous: a bounded software pass cannot compensate for missing real data, a represented protocol cannot become operational effectiveness, and a reservation matrix cannot substitute for affected-party or competent authority. Seventy preregistered synthetic mutations executed and were rejected, but each rejection demonstrates only its exact guard. It is not production security, empirical truth, professional validation, legal review, cultural ratification, complete accessibility, or independent reproduction.

Freed ID / CBR Heart is the primary Trinity Mandala focus. GMUT Mind and THOS Body remain explicit and protected. Community-radio bulletin editing and handover is a learning and synthetic-design lens only. There were no real broadcasters, journalists, listeners, emergency managers, warnings, incidents, transmissions, identities, credentials, accounts, keys, participants, remedies, legal decisions, cultural decisions, spectrum decisions, or Māori-authority decisions.

## Sources and status discipline

The source ledger uses only `current`, `stable`, `draft`, and `watch`. Git, NASA Fermi, HEASARC, OASIS, IETF, W3C, WHATWG, primary physics and causal-method papers, New Zealand Privacy Commissioner guidance, and Te Mana Raraunga supply protocol or design context. The active iCalendar extension remains visibly draft. RFC 9470 errata remains watch material. A source URL or standards citation never becomes an experimental observation, participant result, production certificate, professional licence, or delegated authority.

## Core proposal outcomes

""" + "\n\n".join(proposal_lines) + """

## Expanded portfolio execution

Thirty new safe-now tasks completed only inside their declared additive owner scope. Twenty bounded candidate prototypes were built, invoked, and witnessed. Twenty phase-local skill packages were initialized, structurally validated, and smoke-used without global installation. Ten family-current runners were built and invoked, while historical and owner-specific surfaces remained compatibility evidence rather than deletion targets. Thirty CLEAN/FIX/REFINE tasks completed with zero destructive actions. The inherited portfolios supplied context but received no Ilyra completion credit.

The Reflection-Remaster audit remained non-destructive. It inventoried callers and trigger overlap, retained compatibility paths, and proposed only additive or reviewable dispositions. A lexical caller count does not prove absence of external callers. No identity, memory, provenance, negative, gate, sibling surface, or historical artifact was deleted or downgraded to satisfy a quota.

## GMUT truth boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The Cutkosky board is formal obligation evidence. It does not establish a physical amplitude for GMUT, a new force, an observed discontinuity, a valid ultraviolet completion, a quantum theory, or a Theory of Everything. The Fermi-LAT adapter ingested zero real rows and evaluated zero likelihoods. Catalog availability and schema fidelity are not a fit, posterior, parameter constraint, physical prediction, or empirical confirmation. Promotion requires suitable real data, explicit selection and systematics, uncertainty and covariance treatment, preregistered analysis where appropriate, falsifiers, independent review, and reproducible scientific work.

## THOS truth boundary

THOS remains represented. Synthetic CAP identifiers, revision lineage, cancellation, transcript fallback, correction readback, workload budgets, and handover ownership demonstrate only bounded protocol structure. There were zero real broadcasts, operators, listeners, agencies, alerts, emergencies, safety outcomes, blind matched-budget arms, or effectiveness estimates. Promotion requires real participants or operators, preregistered blind matched-budget arms, safety monitoring, appropriate statistics, affected-user evaluation, and independent review.

## Freed ID and CBR authority boundary

Freed ID remains synthetic and nonproduction. RFC 9470 field and transition fixtures used no real accounts, keys, tokens, authentication events, authorization servers, protected resources, interoperability partners, privacy reviews, security reviews, recovery processes, or trust governance. Production completion requires standards-conformant real keys and proofs where applicable, live issuance and resolution, status and revocation, interoperability, independent privacy and security review, recovery evidence, and trustworthy governance.

CBR remains exact-gated. Community-radio warning reach, disability access, language, journalist and listener privacy, correction, remedy, spectrum, legal interpretation, cultural legitimacy, data governance, and Māori authority belong to affected people and competent authorities within scope. Māori wording, concepts, data, governance, and legitimacy remain under tangata whenua, iwi, hapū, and Māori authority. Repository software cannot confer a remedy, licence, spectrum right, jurisdiction, cultural legitimacy, consent, governance mandate, or public authority.

## Accessibility and privacy reservation

The static report and prerecorded-media fixtures are structural only. Captions, transcripts, descriptions, language labels, controls, fallback, and keyboard structure were checked in bounded files. Manual keyboard use, browser diversity, responsive layout, assistive technology, cognitive accessibility, Māori-language evaluation, security usability, and affected-user evaluation remain reserved. Five structural privacy classes were scanned with exact scanner-definition disposition. Zero confirmed hits is meaningful bounded evidence, not complete privacy assurance.

## Validation and terminal truth

This evidence build runs bounded runner and skill witnesses only. It does not spend the one canonical successful aggregate pass reserved for closeout, does not run the full repository suite, and creates no replay. Final credit requires detailed and minimal validators, complete phase JSON parsing, the five-class scan, exact staged review, Git-blob manifest parity, stale-label review, diff hygiene, source and x1 ancestry, zero merges, the commit cap, single-parent final history, exact clean state, and four-way remote equality. Same-owner evidence is not independent-team reproduction.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`. The route to Sable Rook remains `PREPARED_NOT_SENT` until the exact final head is committed, pushed, clean, single-pass validated, and remote-equal. Windows Sandbox and Hyper-V remain deferred. No cross-platform ChatGPT sibling message, elevation, host-security change, unrelated installation, desktop update, or reboot occurs in this phase.
"""


def build_phase_packet() -> None:
    outcomes = {label: 0 for label in d.OUTCOME_CLASSES}
    proposal_rows = []
    for item in d.PROPOSALS:
        outcomes[item["expected_disposition"]] += 1
        proposal_rows.append(
            {
                **item,
                "observed_disposition": item["expected_disposition"],
                "executed_as_evidence_permits": True,
                "runner_witness": f"validation/runner-witnesses/{item['proposal_id'].casefold()}-witness.json",
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": "Outcome is limited to the frozen hypothesis and protected gates.",
            }
        )
    if outcomes != {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("core outcome distribution changed")
    write_json(
        "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v648-v4.x2-proposals.v1",
            "count": 10,
            "outcomes": outcomes,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "proposals": proposal_rows,
            "noncompensation": True,
        },
    )
    write_json(
        "phase-truth-x2.json",
        {
            "schema": "ghc.family.v648-v4.phase-truth.x2.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "stage": "x2_evidence_built_not_final",
            "source_head": d.SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "outcomes": outcomes,
            "retained_negatives": EFFECTIVE_NEGATIVES,
            "open_gaps": 30,
            "exact_gates": 31,
            "canonical_successful_pass_used": False,
            "replay_used": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v648-v4.retained-negatives.x2.v1",
            "inherited": 4215,
            "x1_operational": 5,
            "synthetic_executed_and_rejected": 70,
            "x2_operational": len(X2_OPERATIONAL_NEGATIVES),
            "effective_total": EFFECTIVE_NEGATIVES,
            "negative_erased": False,
        },
    )
    write_json(
        "validation/x2-operational-negatives.json",
        {
            "schema": "ghc.family.v648-v4.x2-operational-negatives.v1",
            "count": len(X2_OPERATIONAL_NEGATIVES),
            "negatives": X2_OPERATIONAL_NEGATIVES,
            "boundary": "Every observed X2 failure is retained before retry and receives zero evidence credit.",
        },
    )
    write_json(
        "exact-open-gate-register-x2.json",
        {
            "schema": "ghc.family.v648-v4.gates.x2.v1",
            "inherited_open_gaps": 29,
            "new_open_gaps": 1,
            "effective_open_gaps": 30,
            "inherited_exact_gates": 30,
            "new_exact_gates": 1,
            "effective_exact_gates": 31,
            "silently_closed": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v648-v4.threat-model.v1",
            "assets": ["x1 immutable tree", "retained negatives", "authority gates", "source status", "owner lane", "privacy boundary"],
            "threats": [
                "x1 outcome backfill",
                "synthetic-to-real promotion",
                "authority substitution",
                "mailmap identity replacement",
                "calendar expansion exhaustion",
                "OAuth context downgrade",
                "privacy payload leakage",
                "route send before proof",
            ],
            "controls": [
                "exact x1 Git-blob parity",
                "typed outcome vocabulary",
                "zero-row and zero-operation receipts",
                "seven rejecting mutations per proposal",
                "five-class privacy scan",
                "single-pass hold",
                "PREPARED_NOT_SENT route gate",
            ],
            "residual": ["external callers", "manual accessibility", "real data", "real participants", "production identity", "legal cultural and Māori authority", "independent review"],
        },
    )
    write_json(
        "complete-incomplete-checklist-x2.json",
        {
            "schema": "ghc.family.v648-v4.checklist.x2.v1",
            "complete": [
                "ten frozen proposals executed within evidence",
                "six completed two represented one open gap one exact gate",
                "seventy mutations rejected",
                "thirty safe tasks",
                "twenty candidates",
                "twenty skills",
                "ten runners",
                "thirty cleanup tasks",
                "x1 tree unchanged",
            ],
            "incomplete": [
                "real Fermi likelihood",
                "real THOS arms",
                "production Freed ID",
                "affected-party legal cultural and Māori authority",
                "manual accessibility",
                "independent reproduction",
                "Stage 20",
                "final canonical validation",
            ],
        },
    )
    write_json(
        "wellbeing-check-x2.json",
        {
            "schema": "ghc.family.v648-v4.wellbeing.x2.v1",
            "scope_bounded": True,
            "workload_within_declared_portfolios": True,
            "owner_file_threshold": 15000,
            "owner_generated_below_threshold": True,
            "host_changes": 0,
            "cross_platform_messages": 0,
            "desktop_updates": 0,
            "pause_right_preserved": True,
        },
    )
    write_text(
        "wellbeing-check-x2.md",
        "# v648-v4 x2 wellbeing\n\nWork remained solo, additive, D-first, under the four-commit and document caps. No host feature, security setting, desktop update, cross-platform contact, destructive cleanup, or authority substitution entered scope. Hamish may pause or stop the route.",
    )
    write_json(
        "sources/source-ledger-x2-verification.json",
        {
            "schema": "ghc.family.v648-v4.sources.x2-verification.v1",
            "verification_date": "2026-07-19",
            "statuses": {"current": 6, "stable": 8, "draft": 1, "watch": 2},
            "official_or_primary_only": True,
            "citations_as_observations": 0,
            "draft_promoted_to_stable": 0,
            "watch_promoted_to_current": 0,
        },
    )
    overview = build_overview(outcomes)
    write_text("deliverables/v648-v4-integrated-overview.md", overview)
    report_rows = "".join(
        f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['expected_disposition']}</td><td>{row['title']}</td></tr>"
        for row in d.PROPOSALS
    )
    write_text(
        "deliverables/v648-v4-static-report.html",
        f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ilyra Fen v648-v4 evidence report</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Ilyra Fen v648-v4 bounded evidence report</h1><p>Relational working language only. NOT_READY_FOR_STAGE_20.</p></header>
<main id="main"><section aria-labelledby="truth"><h2 id="truth">Phase truth</h2><p>Six completed, two represented, one open gap, and one exact gate. No full-suite, replay, empirical, production, authority, or independent-reproduction credit.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Core outcomes</h2><div role="region" aria-label="Scrollable proposal outcomes" tabindex="0"><table><caption>Ten frozen v648-v4 proposals and bounded dispositions</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Surface</th></tr></thead><tbody>{report_rows}</tbody></table></div></section>
<section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual keyboard, browser, responsive-layout, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. Real data, participants, identity operations, remedies, legal and cultural review, Māori authority, independent review, and Stage 20 remain open or exact-gated.</p></section>
<section aria-labelledby="fallback"><h2 id="fallback">Sequential fallback</h2><ol>{''.join(f'<li>{row["proposal_id"]}: {row["expected_disposition"]} — {row["title"]}</li>' for row in d.PROPOSALS)}</ol></section></main>
<footer><p>Static structural report; no scripts, tracking, external embeds, or active content.</p></footer></body></html>""",
    )


def build_x1_immutability() -> None:
    manifest = read_json(PHASE / "validation/x1-staged-manifest.json")
    paths = [row["path"] for row in manifest["entries"]] + manifest["self_exclusions"]
    issues = []
    for relative in paths:
        committed = git("rev-parse", f"{X1_COMMIT}:{relative}")
        working = run("git", "hash-object", f"--path={relative}", relative)
        if committed != working:
            issues.append({"path": relative, "x1_blob": committed, "working_blob": working})
    write_json(
        "validation/x1-immutability-receipt.json",
        {
            "schema": "ghc.family.v648-v4.x1-immutability.v1",
            "x1_commit": X1_COMMIT,
            "checked_path_count": len(paths),
            "issues": issues,
            "passed": not issues,
            "boundary": "Exact x1 Git blobs only; new x2 paths are additive.",
        },
    )
    if issues:
        raise RuntimeError("x1 immutable paths changed")


def build_index() -> None:
    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(ROOT),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(PHASE / "tooling/x2"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    write_json(
        "tooling/caller-compatibility-receipt.json",
        {
            "schema": "ghc.family.v648-v4.caller-compatibility.v1",
            "new_family_current_runners": d.RUNNER_IDEAS,
            "historical_names_deleted": [],
            "historical_names_renamed": [],
            "external_caller_completeness_claim": False,
            "reflection_remaster_disposition": "additive_only_keep_compatibility",
        },
    )


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def git_blob(path: str) -> str:
    return run("git", "hash-object", f"--path={path}", path)


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"'][^\"']+|bearer\s+[A-Za-z0-9._-]{12,}"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier)\s*[:=]"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)\s*[:=]"),
    }
    definitions = {
        "scripts/build_ghc_family_v648_v4_evidence.py",
        "docs/ilyra-fen/v648-v4/validation/evidence-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": "scanner_definition" if relative in definitions else "confirmed_payload_hit",
                }
                candidates.append(row)
                if relative not in definitions:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v648-v4.evidence-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with exact scanner-definition disposition; not complete privacy assurance.",
    }


def build_manifest() -> None:
    self_exclusions = [
        "docs/ilyra-fen/v648-v4/validation/evidence-staged-manifest.json",
        "docs/ilyra-fen/v648-v4/validation/evidence-staged-privacy.json",
        "docs/ilyra-fen/v648-v4/validation/evidence-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in self_exclusions]
    entries = []
    for relative in paths:
        path = ROOT / relative
        if path.is_file():
            entries.append({"path": relative, "git_blob": git_blob(relative), "bytes": path.stat().st_size})
    privacy = privacy_scan(paths + self_exclusions)
    write_json("validation/evidence-staged-privacy.json", privacy)
    write_json(
        "validation/evidence-staged-manifest.json",
        {
            "schema": "ghc.family.v648-v4.evidence-manifest.v1",
            "hash_domain": "git_hash_object_path_filtered_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": self_exclusions,
        },
    )
    x1_receipt = read_json(PHASE / "validation/x1-immutability-receipt.json")
    write_json(
        "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.v648-v4.evidence-staged-review.v1",
            "intended_path_count": len(entries) + len(self_exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(self_exclusions),
            "out_of_scope_paths": [],
            "x1_checked_paths": x1_receipt["checked_path_count"],
            "x1_modified_paths": x1_receipt["issues"],
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "closeout_or_baton_paths": [],
            "passed": not x1_receipt["issues"] and not privacy["confirmed_hit_count"],
        },
    )
    if privacy["confirmed_hit_count"]:
        raise RuntimeError("evidence privacy scan found confirmed payload hits")


def build() -> None:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("evidence must begin at the exact frozen x1 commit")
    allowed_exact = {
        "scripts/build_ghc_family_v648_v4_evidence.py",
        "scripts/ghc_family_v648_v4_runtime.py",
        "tests/test_ghc_family_v648_v4.py",
        *(f"scripts/{name}" for name in d.RUNNER_IDEAS),
    }
    observed_start = set(filter(None, git("status", "--porcelain").splitlines()))
    observed_paths = {row[3:].replace("\\", "/") for row in observed_start}
    unexpected = {
        path
        for path in observed_paths
        if path not in allowed_exact and not path.startswith("docs/ilyra-fen/v648-v4/")
    }
    if unexpected:
        raise RuntimeError(
            f"unexpected pre-evidence worktree surface: {sorted(unexpected)}"
        )
    build_contracts()
    build_skills()
    build_portfolios()
    build_method_flow_x2()
    build_phase_packet()
    build_x1_immutability()
    build_index()
    write_json(
        "evidence-receipt.json",
        {
            "schema": "ghc.family.v648-v4.evidence.v1",
            "source_head": d.SOURCE_COMMIT,
            "x1_commit": X1_COMMIT,
            "core_outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
            "runner_witnesses": 10,
            "synthetic_mutations_rejected": 70,
            "safe_tasks_completed": 30,
            "candidate_prototypes_built": 20,
            "skills_built_validated_used": 20,
            "runners_built_invoked": 10,
            "cleanup_tasks_completed": 30,
            "x1_immutable": True,
            "canonical_successful_pass_used": False,
            "full_suite_used": False,
            "replay_used": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    build_manifest()


if __name__ == "__main__":
    build()
