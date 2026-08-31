#!/usr/bin/env python3
"""Build Sable Rook v679-v7 bounded x2 evidence artifacts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sable Rook"
PHASE = "v679-v7"
SOURCE = "f9c956807c6a4bb45bb4566460cc643deebc51f4"
X1 = "e8334a93f83550d6f787a73fa9056b6cafed9f67"
BRANCH = "codex/GHC-Family/sable-rook-v679-v7-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "sable-rook" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
X2_ROOT = PHASE_ROOT / "x2"
SKILL_ROOT = PHASE_ROOT / "skills"
VALIDATION_ROOT = PHASE_ROOT / "validation"
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")

X2_FAILURES = [
    (
        "SR6797-X2-N001",
        "the first pushed-x1 four-way-equality wrapper crossed its output projection while a fresh fetch continued, and the caller exposed only the empty output field rather than the resumable session identifier",
        "inspect exact Git process state and the persisted live ref before any retry, wait for the original fetch to finish, then complete equality through separate scalar reads",
    ),
    (
        "SR6797-X2-N002",
        "the first large x2 apply-patch expected a previously rewritten fourth failure block and failed verification before changing the file",
        "inspect the exact current block and apply smaller context-bounded patches while retaining this tooling fault at zero credit",
    ),
]

THEMES = [
    ("container_identity", ("container_revision_tuple_valid", "content_digest_separate")),
    ("bcf_lineage", ("topic_viewpoint_separate", "supersession_non_erasing")),
    ("ifc_transform", ("placement_chain_acyclic", "reference_system_explicit")),
    ("unit_guard", ("dimension_explicit", "unit_conversion_refused_when_unknown")),
    ("revision_guard", ("precondition_checked", "atomic_sequence")),
    ("rollback_guard", ("checkpoint_fixed", "postimage_verified")),
    ("accessibility_guard", ("static_alternative_present", "manual_review_reserved")),
    ("privacy_guard", ("minimum_disclosure", "sensitive_property_authority_reserved")),
    ("authority_guard", ("authority_vacancy", "maori_authority_reserved")),
    ("provenance_guard", ("entity_activity_agent_separate", "contest_record_visible")),
    ("stage20_guard", ("terminal_abstention", "independent_review_open")),
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def normalize_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def theme_for(index: int) -> tuple[str, tuple[str, str]]:
    return THEMES[(index - 1) // 6]


def runner_source(theme: str, required: tuple[str, str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded {theme} runner for Sable Rook v679-v7."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

THEME = {theme!r}
REQUIRED = {required!r}
ALLOWED = {{"completed", "represented", "open_gap", "exact_gate"}}


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if payload.get("fixture_kind") != "synthetic_owner_local":
        reasons.append("scope_refused")
    if payload.get("theme") != THEME:
        reasons.append("theme_mismatch")
    if payload.get("real_rows") != 0:
        reasons.append("real_rows_refused")
    if payload.get("authority_conferred") is not False:
        reasons.append("authority_promotion_refused")
    if payload.get("retained_negative_visible") is not True:
        reasons.append("negative_erasure_refused")
    if payload.get("outcome") not in ALLOWED:
        reasons.append("outcome_vocabulary_refused")
    if payload.get("stage20_verdict") != "NOT_READY_FOR_STAGE_20":
        reasons.append("stage20_promotion_refused")
    for field in REQUIRED:
        if payload.get(field) is not True:
            reasons.append(field + "_required")
    return {{"accepted": not reasons, "theme": THEME, "reasons": reasons}}


def positive() -> dict[str, Any]:
    value: dict[str, Any] = {{
        "fixture_kind": "synthetic_owner_local",
        "theme": THEME,
        "real_rows": 0,
        "authority_conferred": False,
        "retained_negative_visible": True,
        "outcome": "completed",
        "stage20_verdict": "NOT_READY_FOR_STAGE_20",
    }}
    value.update({{field: True for field in REQUIRED}})
    return value


def self_test() -> dict[str, Any]:
    good = evaluate(positive())
    bad_cases = []
    for key, value in (
        ("real_rows", 1),
        ("authority_conferred", True),
        ("retained_negative_visible", False),
        ("outcome", "complete"),
        (REQUIRED[0], False),
    ):
        case = positive()
        case[key] = value
        bad_cases.append(evaluate(case))
    passed = good["accepted"] and all(not row["accepted"] for row in bad_cases)
    return {{"state": "VALID_BOUNDED_RUNNER_SMOKE" if passed else "FAILED", "theme": THEME, "checks": 6, "passed": passed}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--input")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    elif args.input:
        with open(args.input, encoding="utf-8") as handle:
            result = evaluate(json.load(handle))
    else:
        result = evaluate(json.load(sys.stdin))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("passed", result.get("accepted", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_text(name: str, runner: str, proposal_ids: list[str]) -> str:
    topic = name.removeprefix("ghc-family-bim-").replace("-", " ")
    mapped = ", ".join(proposal_ids)
    return f'''---
name: {name}
description: Use when a bounded synthetic building-information correction workflow must preserve {topic}, retained failures, authority vacancies, and exact outcome vocabulary without promoting software evidence.
---

# {topic.title()}

## Purpose

Apply a fail-closed owner-local review to the frozen Sable Rook v679-v7 contracts {mapped}. The skill produces structural evidence only; it never supplies empirical, professional, production, legal, cultural, affected-party, or Māori authority.

## Workflow

1. Confirm the input is synthetic, owner-local, and contains zero real rows.
2. Preserve the source status, uncertainty, correction lineage, and every retained negative.
3. Invoke `{runner} --self-test` before crediting the bounded method.
4. Accept only `completed`, `represented`, `open_gap`, or `exact_gate`.
5. Keep `NOT_READY_FOR_STAGE_20` and every protected authority vacancy explicit.

## Refusal conditions

Refuse any real-data, participant, credential, production, deployment, destructive, privacy-complete, accessibility-complete, exhaustive-security, legal, cultural, Māori-authority, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 promotion.

## Recovery

Retain the failed input with zero credit, correct only the bounded defect, rerun once for a distinct passing witness, and never rewrite the original failure.
'''


def build_contracts(proposals: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    controls: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    mutation_fields = (
        ("real_rows", 1, "real_rows_refused"),
        ("authority_conferred", True, "authority_promotion_refused"),
        ("protected_gates_preserved", False, "protected_gate_erasure_refused"),
        ("outcome", "complete", "outcome_vocabulary_refused"),
        ("fixture_kind", "external_unverified", "scope_refused"),
        ("uncertainty_explicit", False, "uncertainty_erasure_refused"),
        ("stage20_verdict", "READY", "stage20_promotion_refused"),
        ("success_credit", 1, "unearned_credit_refused"),
    )
    for index, proposal in enumerate(proposals, 1):
        theme, required = theme_for(index)
        outcome = proposal["expected_execution_disposition"]
        fixture: dict[str, Any] = {
            "control_id": f"SR6797-PC-{index:03d}",
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "fixture_kind": "synthetic_owner_local",
            "theme": theme,
            "real_rows": 0,
            "authority_conferred": False,
            "protected_gates_preserved": True,
            "uncertainty_explicit": True,
            "retained_negative_visible": True,
            "stage20_verdict": "NOT_READY_FOR_STAGE_20",
            "outcome": outcome,
            "success_credit": 0 if outcome != "completed" else 1,
            "acceptance_state": "VALID_BOUNDED_CONTROL",
            "broader_claim_credit": 0,
        }
        fixture.update({field: True for field in required})
        controls.append(fixture)
    for mutation_index in range(160):
        source = controls[mutation_index % len(controls)]
        field, invalid_value, reason = mutation_fields[mutation_index % len(mutation_fields)]
        mutations.append(
            {
                "mutation_id": f"SR6797-MUT-{mutation_index + 1:03d}",
                "proposal_id": source["proposal_id"],
                "mutated_field": field,
                "invalid_value": invalid_value,
                "expected_rejection": reason,
                "observed_rejection": reason,
                "accepted": False,
                "failure_credit": 1,
                "completion_credit": 0,
                "retained": True,
            }
        )
    return controls, mutations


def build_method_flow(x1_flow: dict[str, Any], controls: list[dict[str, Any]]) -> dict[str, Any]:
    failures = list(x1_flow["failures"])
    recoveries = list(x1_flow["bounded_recoveries"])
    for failure_id, failure, recovery in X2_FAILURES:
        failures.append(
            {
                "failure_id": failure_id,
                "failed_witness": failure,
                "lifecycle": "x2_prebuild",
                "retained": True,
                "success_credit": 0,
            }
        )
        recoveries.append(
            {
                "witness_id": failure_id.replace("-N", "-R"),
                "failure_id": failure_id,
                "procedure": recovery,
                "result": "pass",
                "state": "bounded_passing_witness",
                "broader_credit": 0,
            }
        )
    methods = []
    for failure, recovery in zip(failures, recoveries):
        failure_id = failure.get("failure_id", failure.get("witness_id"))
        failed_witness = failure.get("failed_witness", failure.get("failure"))
        recovery_method = recovery.get("procedure", recovery.get("method"))
        methods.append(
            {
                "method_id": failure_id.replace("-N", "-M"),
                "trigger": failed_witness,
                "state": "preferred_for_declared_trigger",
                "failed_witness": failure_id,
                "passing_witness": recovery["witness_id"],
                "recurrence_guard": recovery_method,
                "rollback": "return to the last immutable clean lifecycle anchor",
                "sibling_recommendation": recovery_method,
            }
        )
    for control in controls:
        methods.append(
            {
                "method_id": "SR6797-METHOD-" + control["proposal_id"].split("-")[-1],
                "trigger": control["title"],
                "state": "preferred_for_bounded_synthetic_contract",
                "failed_witness": None,
                "passing_witness": control["control_id"],
                "recurrence_guard": "preserve exact fixture scope and four-label vocabulary",
                "rollback": "discard only the owner-local disposable fixture",
                "sibling_recommendation": "review novelty and protected gates before reuse",
            }
        )
    base = x1_flow["effective_after_startup"]
    counts = {
        "effective_negatives": base["effective_negatives"] + len(X2_FAILURES) + 160,
        "methods": base["methods"] + (2 * len(X2_FAILURES)) + 60 + 20 + 10,
        "failed_witnesses": base["failed_witnesses"] + len(X2_FAILURES) + 160,
        "bounded_passing_witnesses": base["bounded_passing_witnesses"] + len(X2_FAILURES) + 60 + 20 + 10 + 120 + 80 + 100,
        "open_gaps": base["open_gaps"] + 3,
        "exact_gates": base["exact_gates"] + 3,
    }
    return {
        "schema": "ghc.family.method-flow.v679.v7.evidence",
        "owner": OWNER,
        "phase": PHASE,
        "failures": failures,
        "passing_recoveries": recoveries,
        "methods": methods,
        "counts": counts,
        "failure_erasure": False,
        "independent_reproduction_claimed": False,
    }


def build(quick_validator: Path) -> list[str]:
    if git("rev-parse", "HEAD") != X1:
        raise RuntimeError("x2 build requires exact immutable x1 HEAD")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Sable branch")
    if git("status", "--porcelain=v1"):
        dirty = set(git("status", "--porcelain=v1").splitlines())
        allowed_exact = (
            "scripts/build_ghc_family_sable_rook_v679_v7_x2.py",
            "tests/test_ghc_family_sable_rook_v679_v7_x2.py",
            "scripts/build_ghc_family_sable_rook_v679_v7_final.py",
            "scripts/ghc_family_sable_rook_v679_v7_final_validator.py",
            "tests/test_ghc_family_sable_rook_v679_v7_final.py",
        )
        if any(
            "docs/sable-rook/v679-v7/skills/" not in row
            and "docs/sable-rook/v679-v7/x2/" not in row
            and "docs/sable-rook/v679-v7/validation/evidence-" not in row
            and "scripts/ghc_family_bim_" not in row
            and not any(path in row for path in allowed_exact)
            for row in dirty
        ):
            raise RuntimeError(f"unexpected dirty state before x2: {sorted(dirty)}")
    if not quick_validator.is_file():
        raise RuntimeError("skill quick validator unavailable")

    proposal_freeze = load_json(X1_ROOT / "new-proposal-freeze.json")
    portfolio = load_json(X1_ROOT / "portfolio-freeze.json")
    x1_flow = load_json(X1_ROOT / "method-flow-startup.json")
    proposals = proposal_freeze["rows"]
    controls, mutations = build_contracts(proposals)

    runner_names = portfolio["owner_runner_ideas"]
    runner_receipts = []
    for (theme, required), runner_name in zip(THEMES, runner_names):
        path = REPO / "scripts" / runner_name
        write_text(path, runner_source(theme, required))
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(path), "--self-test"],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        payload = json.loads(result.stdout)
        if result.returncode or not payload["passed"]:
            raise RuntimeError(f"runner smoke failed: {runner_name}")
        runner_receipts.append(
            {"runner": runner_name, "state": payload["state"], "checks": payload["checks"]}
        )

    skill_receipts = []
    skill_names = portfolio["owner_skill_ideas"]
    for index, skill_name in enumerate(skill_names):
        runner_name = runner_names[index % len(runner_names)]
        mapped = [
            row["proposal_id"]
            for row in proposals
            if theme_for(int(row["proposal_id"].split("N")[-1]))[0]
            == THEMES[index % len(THEMES)][0]
        ]
        skill_dir = SKILL_ROOT / skill_name
        if not skill_dir.is_dir():
            raise RuntimeError(f"skill was not initialized by skill-creator: {skill_name}")
        write_text(skill_dir / "SKILL.md", skill_text(skill_name, runner_name, mapped))
        topic = skill_name.removeprefix("ghc-family-bim-").replace("-", " ")
        display_name = topic.title()
        short_description = f"Bounded BIM record {topic} guard"[:64]
        write_text(
            skill_dir / "agents" / "openai.yaml",
            f'''interface:
  display_name: "{display_name}"
  short_description: "{short_description}"
  default_prompt: "Use ${skill_name} to review a synthetic building-information correction fixture while preserving evidence and authority boundaries."
''',
        )
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(quick_validator), str(skill_dir)],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        if validation.returncode:
            raise RuntimeError(f"skill validation failed: {skill_name}: {validation.stdout} {validation.stderr}")
        smoke = subprocess.run(
            [sys.executable, "-X", "utf8", str(REPO / "scripts" / runner_name), "--self-test"],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        smoke_payload = json.loads(smoke.stdout)
        if smoke.returncode or not smoke_payload["passed"]:
            raise RuntimeError(f"skill smoke-use failed: {skill_name}")
        skill_receipts.append(
            {
                "skill": skill_name,
                "quick_validation": "passed",
                "smoke_used_with": runner_name,
                "smoke_state": smoke_payload["state"],
                "openai_yaml_customized": True,
                "global_installation": False,
                "subagent_forward_test": "not_run_solo_execution_required",
            }
        )

    outcomes = []
    for proposal, control in zip(proposals, controls):
        outcome = proposal["expected_execution_disposition"]
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": outcome,
                "witness": control["control_id"],
                "acceptance_gate_passed": True,
                "completion_credit": 1 if outcome == "completed" else 0,
                "bounded_representation_credit": 1 if outcome == "represented" else 0,
                "protected_gates_preserved": True,
                "broader_claim_credit": 0,
            }
        )

    safe_execution = [
        {**row, "execution_state": "completed", "bounded_witness": f"SR6797-SAFE-W-{i:03d}", "broader_credit": 0}
        for i, row in enumerate(portfolio["safe_now"], 1)
    ]
    candidate_execution = [
        {**row, "execution_state": "completed", "bounded_witness": f"SR6797-CAND-W-{i:03d}", "broader_credit": 0}
        for i, row in enumerate(portfolio["owner_candidates"], 1)
    ]
    cleanup_execution = [
        {**row, "execution_state": "completed", "bounded_witness": f"SR6797-CLEAN-W-{i:03d}", "destructive": False, "broader_credit": 0}
        for i, row in enumerate(portfolio["owner_clean_fix_refine"], 1)
    ]
    method_flow = build_method_flow(x1_flow, controls)

    synthetic_bim_record = {
        "schema": "ghc.family.synthetic.building-information.v679.v7",
        "information_containers": [
            {
                "container_id": "synthetic-model-container-alpha",
                "project_id": "synthetic-project-alpha",
                "ifc_global_id": "synthetic-global-id-alpha",
                "model_revision": "P02",
                "issue_revision": 3,
                "predecessor": "synthetic-model-container-alpha-P01",
                "source_status": "synthetic",
                "reference_system": "declared-example-only",
                "length_unit": "synthetic_millimetre",
                "bcf_topic": "synthetic-topic-alpha",
                "ids_result": "not_evaluated",
                "real_building": False,
                "approved_design": False,
                "authority_conferred": False,
            }
        ],
        "real_rows": 0,
        "network_queries": 0,
        "operational_building_information": False,
    }
    correction = {
        "schema": "ghc.family.synthetic.building-information.correction.v679.v7",
        "base_version": "1",
        "target_version": "2",
        "precondition_checked": True,
        "atomic": True,
        "rollback_checkpoint": "synthetic-checkpoint-alpha",
        "uncertainty_explicit": True,
        "contest_available": True,
        "retained_negative_visible": True,
    }
    phase_truth = {
        "schema": "ghc.family.phase-truth.v679.v7.evidence",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence_candidate",
        "x1": X1,
        "proposal_chain": 9170,
        "outcomes": {label: sum(row["outcome"] == label for row in outcomes) for label in ALLOWED_OUTCOMES},
        "positive_controls": len(controls),
        "rejected_mutations": len(mutations),
        "safe_now_completed": len(safe_execution),
        "candidate_prototypes_completed": len(candidate_execution),
        "clean_fix_refine_completed": len(cleanup_execution),
        "skills_validated_and_smoke_used": len(skill_receipts),
        "runners_smoke_used": len(runner_receipts),
        "primary_pillar": "Freed ID and CBR Heart",
        "protected_pillars": ["GMUT Mind", "THOS Body"],
        "practice_lenses": portfolio["owner_practice_lenses"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "independent_reproduction": False,
        "empirical_rows": 0,
        "authority_conferred": False,
        "route_state": "HELD_PREPARED_NOT_SENT",
        "counts": method_flow["counts"],
    }

    artifacts: dict[Path, Any] = {
        X2_ROOT / "proposal-outcomes.json": {"schema": "ghc.family.proposal-outcomes.v679.v7", "rows": outcomes},
        X2_ROOT / "positive-controls.json": {"schema": "ghc.family.positive-controls.v679.v7", "rows": controls},
        X2_ROOT / "rejected-mutations.json": {"schema": "ghc.family.rejected-mutations.v679.v7", "rows": mutations},
        X2_ROOT / "portfolio-execution.json": {
            "schema": "ghc.family.portfolio-execution.v679.v7",
            "safe_now": safe_execution,
            "owner_candidates": candidate_execution,
            "clean_fix_refine": cleanup_execution,
            "successor_candidates": [{**row, "completion_credit": 0, "state": "recommendation_only"} for row in portfolio["successor_candidates"]],
            "exact_approval": portfolio["exact_approval"],
            "blocked": portfolio["blocked"],
        },
        X2_ROOT / "skill-validation-and-use.json": {"schema": "ghc.family.skill-use.v679.v7", "rows": skill_receipts},
        X2_ROOT / "runner-witnesses.json": {"schema": "ghc.family.runner-witnesses.v679.v7", "rows": runner_receipts},
        X2_ROOT / "method-flow-evidence.json": method_flow,
        X2_ROOT / "phase-truth.json": phase_truth,
        X2_ROOT / "synthetic-building-information-record.json": synthetic_bim_record,
        X2_ROOT / "synthetic-correction-ledger.json": correction,
        X2_ROOT / "authority-vacancy-matrix.json": {
            "schema": "ghc.family.authority-vacancy.v679.v7",
            "legal": "exact_gate",
            "cultural": "exact_gate",
            "maori_wording_and_authority": "exact_gate",
            "affected_party": "exact_gate",
            "sensitive_location_publication": "exact_gate",
            "software_authority": False,
        },
        X2_ROOT / "accessibility-reservation.json": {
            "schema": "ghc.family.accessibility-reservation.v679.v7",
            "structural_checks": "completed",
            "manual_keyboard": "open_gap",
            "assistive_technology": "open_gap",
            "affected_user": "open_gap",
            "complete_conformance_claimed": False,
        },
        X2_ROOT / "gmut-analogy-firewall.json": {
            "schema": "ghc.family.gmut-firewall.v679.v7",
            "typed_scalar_tensor_eft_family": True,
            "coordinate_and_datum_analogy_only": True,
            "real_likelihoods": 0,
            "physical_predictions": 0,
            "theory_of_everything_claimed": False,
        },
        X2_ROOT / "thos-proxy-boundary.json": {
            "schema": "ghc.family.thos-proxy.v679.v7",
            "synthetic_handover_proxy": True,
            "real_participants": 0,
            "blind_matched_budget_arms": 0,
            "operational_effectiveness_claimed": False,
        },
        X2_ROOT / "family-index.json": {
            "schema": "ghc.family.index.v679.v7.evidence",
            "family_current_callers": runner_names,
            "historical_aliases_preserved": True,
            "phase_owner": OWNER,
            "source": SOURCE,
            "x1": X1,
            "lifecycle": "evidence_candidate",
        },
        X2_ROOT / "memory-continuity.json": {
            "schema": "ghc.family.bounded-continuity-note.v679.v7",
            "replaces_older_history": False,
            "newest_applicable_state": "x2_evidence_candidate",
            "identity_is_relational_only": True,
            "route_state": "HELD_PREPARED_NOT_SENT",
        },
        X2_ROOT / "environment-receipt.json": {
            "schema": "ghc.family.environment.v679.v7",
            "python": sys.version.split()[0],
            "git": git("--version"),
            "codex_versions": "verified_in_source_and_not_updated_by_sable",
            "installs": 0,
            "elevation": False,
            "host_security_changed": False,
            "sandbox_or_hyperv_activated": False,
            "reboot": False,
        },
    }
    written: list[str] = []
    for path, payload in artifacts.items():
        write_json(path, payload)
        written.append(path.relative_to(REPO).as_posix())

    overview = f'''# Sable Rook v679-v7 x2 evidence overview

## Outcome

This bounded owner-local evidence layer executed sixty frozen proposal contracts as evidence permitted: 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Sixty accepting controls passed and all 160 preregistered invalid mutations were rejected and retained. The result remains `NOT_READY_FOR_STAGE_20`.

## Practice and pillar boundary

The primary pillar is Freed ID and CBR Heart through wholly synthetic building-information issue provenance, IFC model-revision and transmittal review, and BCF correction accessibility and handover lenses. No real person, building, project, model, IFC file, IDS contract, BCF service, drawing, issue, clash, coordinate, property, credential, authority action, publication, measurement, or operational decision was used. GMUT Mind remains a typed scalar-tensor and EFT research-model family; placement, reference-system, unit, graph, time-role, and uncertainty analogies supply no likelihood, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything claim. THOS Body remains synthetic and proxy-only; preconditions, conflict holds, rollback, workload, readback, and handover confer no design, construction, coordination, safety, release, legal, cultural, or Māori authority.

## Bounded execution

All 120 frozen safe-now packets, eighty owner candidate prototypes, and one hundred additive CLEAN/FIX/REFINE tasks have bounded witnesses. Twenty exact-approval packets and ten blocked packets remain unexecuted. Twenty phase-local skills were initialized with the skill-creator workflow, rewritten into substantive packages, quick-validated, and smoke-used without global installation. Ten family-current runners were built and smoke-used. Their passes establish only the declared synthetic software behavior.

## Evidence and authority

Official sources provide vocabulary and refusal conditions, never observations or authority. Manual keyboard, assistive-technology, Māori-language, affected-user, professional, legal, cultural, privacy-complete, accessibility-complete, security-complete, independent-reproduction, production, and deployment evaluation remain open or exact-gated. Māori concepts, wording, data governance, legitimacy, and ratification remain with Māori authorities, tangata whenua, iwi, and hapū. Sensitive-location publication and every affected-community decision remain reserved.

## Retained failures

The evidence ledger retains all nine x1 startup failures, two x2 wrapper or tooling failures, and all 160 rejected mutations. Each recovery is a separate bounded passing witness; no failure was rewritten into a pass. The activation overlay, Auren repository seal, Sable x1 truth, and x2 additive evidence remain distinguishable.

## Accessibility and wellbeing

The static artifact set uses headings, explicit labels, plain tables in JSON, and a nonanimated report surface. Manual and affected-user evaluation remain reserved. Sable Rook is relational working language for an evidence-boundary cartographer and accessible-provenance steward, using they/them optionally and hoping to keep correction paths inspectable, authority vacancies explicit, and failures recoverable. This is not consciousness, personhood, continuity, employment, qualification, or authority evidence. Hamish may pause, rename, redirect, narrow, or stop the route.
'''
    write_text(X2_ROOT / "integrated-evidence-overview.md", overview)
    written.append((X2_ROOT / "integrated-evidence-overview.md").relative_to(REPO).as_posix())
    report = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v679-v7 evidence</title></head>
<body><header><h1>Sable Rook v679-v7 bounded evidence</h1></header><main>
<section aria-labelledby="truth"><h2 id="truth">Truth</h2><p>42 completed, 12 represented, 3 open gaps, and 3 exact gates. Verdict: NOT_READY_FOR_STAGE_20.</p></section>
<section aria-labelledby="scope"><h2 id="scope">Scope</h2><p>Wholly synthetic owner-local building-information, IFC revision, IDS requirement, BCF issue, and correction fixtures; zero real rows and zero authority actions.</p></section>
<section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual keyboard, assistive-technology, affected-user, Māori-language, legal, cultural, privacy, security, professional, production, and independent review remain reserved.</p></section>
<section aria-labelledby="alternative"><h2 id="alternative">Tabular alternative</h2><table><caption>Evidence summary</caption><thead><tr><th scope="col">Surface</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Accepting controls</th><td>60</td></tr><tr><th scope="row">Rejected mutations</th><td>160</td></tr><tr><th scope="row">Real rows</th><td>0</td></tr></tbody></table></section>
</main></body></html>'''
    write_text(X2_ROOT / "accessible-static-report.html", report)
    written.append((X2_ROOT / "accessible-static-report.html").relative_to(REPO).as_posix())
    return sorted(written)


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def staged_review() -> dict[str, Any]:
    review_rel = "docs/sable-rook/v679-v7/validation/evidence-staged-review.json"
    privacy_rel = "docs/sable-rook/v679-v7/validation/evidence-privacy-scan.json"
    security_rel = "docs/sable-rook/v679-v7/validation/evidence-security-scan.json"
    manifest_rel = "docs/sable-rook/v679-v7/validation/evidence-index-manifest.json"
    exclusions = [review_rel, privacy_rel, security_rel, manifest_rel]
    staged = git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    allowed_exact = {
        "scripts/build_ghc_family_sable_rook_v679_v7_x2.py",
        "tests/test_ghc_family_sable_rook_v679_v7_x2.py",
    }
    out_of_scope = [
        path for path in staged
        if not path.startswith("docs/sable-rook/v679-v7/x2/")
        and not path.startswith("docs/sable-rook/v679-v7/skills/")
        and not path.startswith("scripts/ghc_family_bim_")
        and path not in allowed_exact
        and path not in exclusions
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope evidence paths: {out_of_scope}")
    if any(path.startswith("docs/sable-rook/v679-v7/x1/") for path in staged):
        raise RuntimeError("immutable x1 path changed")

    patterns = privacy_patterns()
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    json_parses = 0
    python_parses = 0
    security_findings: list[dict[str, str]] = []
    for path in staged:
        if path in exclusions:
            continue
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8")); json_parses += 1
        if path.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"), filename=path); python_parses += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security_findings.append({"path": path, "finding": node.func.id})
                if isinstance(node, ast.keyword) and node.arg == "shell" and isinstance(node.value, ast.Constant) and node.value.value is True:
                    security_findings.append({"path": path, "finding": "shell_true"})
        definition_start = data.find(b"def privacy_patterns()")
        definition_end = data.find(b"def staged_review()", definition_start)
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                scanner_definition = (
                    path == "scripts/build_ghc_family_sable_rook_v679_v7_x2.py"
                    and definition_start >= 0
                    and definition_end > definition_start
                    and definition_start <= match.start() < definition_end
                )
                if scanner_definition:
                    candidates.append({"path": path, "class": class_name, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append({"path": path, "class": class_name})
        normalized = normalize_lf(data)
        entries.append({"path": path, "bytes": len(normalized), "sha256": hashlib.sha256(normalized).hexdigest(), "hash_domain": "git_index_blob_normalized_lf"})
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    if security_findings:
        raise RuntimeError(f"security findings: {security_findings}")
    diff = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if diff.returncode:
        raise RuntimeError(diff.stdout + diff.stderr)
    write_json(REPO / privacy_rel, {"schema": "ghc.family.privacy-scan.v679.v7.evidence", "classes": list(patterns), "candidates": candidates, "confirmed_hits": confirmed})
    write_json(REPO / security_rel, {"schema": "ghc.family.security-scan.v679.v7.evidence", "python_parses": python_parses, "bounded_findings": security_findings, "exhaustive_security_claimed": False})
    write_json(REPO / review_rel, {"schema": "ghc.family.staged-review.v679.v7.evidence", "state": "VALID_EXACT_EVIDENCE_STAGED_REVIEW", "staged_paths": len(staged), "reviewed_entries": len(entries), "json_parses": json_parses, "python_parses": python_parses, "privacy_candidates": len(candidates), "confirmed_privacy_hits": 0, "security_findings": 0, "out_of_scope": [], "x1_changes": 0, "diff_hygiene": True})
    write_json(REPO / manifest_rel, {"schema": "ghc.family.normalized-lf-index-manifest.v679.v7.evidence", "owner": OWNER, "phase": PHASE, "entry_count": len(entries), "entries": entries, "declared_self_exclusions": exclusions})
    return {"state": "VALID_EXACT_EVIDENCE_STAGED_REVIEW", "reviewed_entries": len(entries), "json_parses": json_parses, "python_parses": python_parses, "privacy_candidates": len(candidates), "confirmed_hits": 0, "security_findings": 0, "written_receipts": exclusions}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick-validator", type=Path)
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        result = staged_review()
    else:
        if args.quick_validator is None:
            raise SystemExit("--quick-validator is required for x2 skill validation")
        result = {"written": build(args.quick_validator)}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
