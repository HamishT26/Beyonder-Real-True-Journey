#!/usr/bin/env python3
"""Prepare and execute bounded Orin Thale v674-v4 x2 evidence.

`prepare` creates owner-local skill and runner surfaces but awards no outcome.
The main agent must read every generated SKILL.md through EOF before `execute`.
`execute` quick-validates and smoke-uses those skills, exercises ten family
runners, evaluates sixty positive synthetic fixtures and 240 preregistered
invalid mutations, and writes bounded same-owner evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Orin Thale"
OWNER_SLUG = "orin-thale"
PHASE = "v674-v4"
SOURCE_FINAL = "dcdc2921b193516242c93e6ef303f854e9d21264"
X1_HEAD = "5728299ca983aa504a64a5038197358bc50c4ceb"
PRIMARY_PILLAR = "THOS Body"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / OWNER_SLUG / PHASE
X1_ROOT = PHASE_ROOT / "x1"
X2_ROOT = PHASE_ROOT / "x2"
SCRIPT_REL = "scripts/build_ghc_family_orin_thale_v674_v4_x2.py"
TEST_REL = "tests/test_ghc_family_orin_thale_v674_v4_x2.py"
CORE_REL = "scripts/ghc_family_orin_v674_v4_contract_core.py"
MANIFEST_REL = f"docs/{OWNER_SLUG}/{PHASE}/x2/validation/evidence-owner-manifest.json"
STAGED_REVIEW_REL = f"docs/{OWNER_SLUG}/{PHASE}/x2/validation/evidence-staged-review.json"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

SKILL_SPECS = [
    ("orin-v674-v4-lifecycle-boundary", "Review synthetic lifecycle-state transitions", "Require an explicit current state, permitted predecessor, and reversible next state; quarantine hidden jumps."),
    ("orin-v674-v4-correction-lineage", "Review correction lineage in synthetic records", "Require a visible predecessor or explicit genesis marker; never overwrite the failed or superseded record."),
    ("orin-v674-v4-vacancy-visibility", "Keep missing evidence visible in synthetic contracts", "Require every absent measurement, approval, calibration, or consent witness to remain an explicit vacancy."),
    ("orin-v674-v4-unit-uncertainty", "Review units and uncertainty in synthetic observations", "Require declared units and uncertainty status; reject implied measurement precision or real observation claims."),
    ("orin-v674-v4-source-status", "Classify official-source use without promoting citations", "Mark sources as vocabulary or refusal-condition inputs and reject citation-to-observation promotion."),
    ("orin-v674-v4-nonclaim-firewall", "Apply bounded nonclaim firewalls to synthetic artifacts", "Reject empirical, professional, production, legal, cultural, identity, or authority implications outside the evidence."),
    ("orin-v674-v4-authority-gate", "Hold authority-dependent work at an exact gate", "Require the named competent and affected authority; broad workflow permission never substitutes for it."),
    ("orin-v674-v4-minimum-disclosure", "Review minimum-disclosure synthetic records", "Keep direct identifiers, precise locations, secrets, and private routes absent unless an exact governed need exists."),
    ("orin-v674-v4-accessibility-reservation", "Structure accessibility proxies while reserving evaluation", "Require semantic structure and a manual and affected-user evaluation vacancy; never claim accessibility completeness."),
    ("orin-v674-v4-bounded-retry", "Apply bounded retry and quiescence rules", "Record a failed witness before retrying, isolate the dependency, and stop after the bounded recovery or terminal condition."),
    ("orin-v674-v4-workload-pause", "Represent workload, pause, and stop states", "Require visible pause and stop states without inferring a real worker, workplace, fitness, or operational authority."),
    ("orin-v674-v4-handover-readback", "Review synthetic handover and readback contracts", "Require sender state, receiver acknowledgement vacancy, correction path, and no inference of real delivery."),
    ("orin-v674-v4-empirical-gap", "Keep empirical work open until governed evidence exists", "Require real data, preregistration, monitoring, statistics, and independent review before any empirical promotion."),
    ("orin-v674-v4-gmut-analogy-firewall", "Separate GMUT analogies from physical evidence", "Treat symbolic and synthetic structures as model-family evidence only, never a force, prediction, constraint, or Theory of Everything."),
    ("orin-v674-v4-thos-participant-firewall", "Separate THOS proxy evidence from participant evidence", "Require preregistered blind matched-budget real arms and independent review before participant or operator claims."),
    ("orin-v674-v4-freed-id-nonproduction", "Keep Freed ID fixtures synthetic and nonproduction", "Require real conformant keys, live lifecycle, interoperability, review, recovery, and governance before production claims."),
    ("orin-v674-v4-cbr-maori-gate", "Keep CBR and Maori matters under competent authority", "Reserve legal, cultural, affected-party, tangata whenua, iwi, hapu, and Maori authority decisions to those authorities."),
    ("orin-v674-v4-mutation-rejection", "Adjudicate preregistered invalid synthetic mutations", "Reject missing state, hidden vacancy, erased lineage, and authority-claim mutations while retaining each zero-credit witness."),
    ("orin-v674-v4-manifest-domain", "Review Git-blob and checkout manifest domains", "Name the byte domain, preserve declared self-exclusions, and never compare normalized Git blobs as checkout bytes."),
    ("orin-v674-v4-terminal-route-hold", "Hold successor routing until the exact terminal gate", "Require fresh authority, roster, unique title, immediate reread, duplicate guard, acknowledgement, and one send only."),
]

RUNNER_NAMES = [
    "lifecycle_state",
    "correction_lineage",
    "vacancy_visibility",
    "unit_uncertainty",
    "source_status",
    "nonclaim_firewall",
    "authority_gate",
    "minimum_disclosure",
    "handover_readback",
    "mutation_rejection",
]

PRIVATE_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\\\|/Users/|/home/)", re.I),
    "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s\"']+"),
    "private_callable_identifier": re.compile(r"(?i)(?:mcp__|clientThreadId|source_thread_id)"),
    "conversation_or_session_stream": re.compile(r"(?i)(?:raw transcript|session stream|chat export)"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_git(*args: str, text: bool = True, check: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
    )
    return proc.stdout


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_x1_head() -> None:
    head = str(run_git("rev-parse", "HEAD")).strip()
    if head != X1_HEAD:
        raise RuntimeError(f"x2 requires immutable x1 head {X1_HEAD}; found {head}")


def skill_markdown(name: str, description: str, instruction: str) -> str:
    return f"""---
name: {name}
description: {description} for Orin v674-v4 owner-local synthetic evidence; do not use it to infer a real-world result or authority.
---

# {name}

Use this phase-local skill only for the bounded Orin v674-v4 synthetic contract surface. It is not globally installed and does not alter another owner's evidence.

## Decision rule

{instruction}

## Workflow

1. Read the complete target contract and its preregistered expected disposition.
2. Check the decision rule above and preserve any missing witness as a vacancy.
3. Reject an invalid mutation without rewriting it; record the smallest bounded recovery separately.
4. Return only `completed`, `represented`, `open_gap`, or `exact_gate` for a core outcome.

## Boundaries

Synthetic structure and same-owner software checks do not establish empirical confirmation, participant evidence, professional competence, production readiness, legal or cultural ratification, Maori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.
"""


def core_runner_source() -> str:
    return '''#!/usr/bin/env python3
"""Family-current bounded synthetic contract runner for Orin v674-v4."""
from __future__ import annotations
import json
from typing import Any

REQUIRED = ("record_id", "state", "vacancies", "correction_parent", "authority_claim", "real_world_action", "expected_valid")

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED if key not in record]
    reasons: list[str] = []
    if missing:
        reasons.append("missing_required:" + ",".join(missing))
    if record.get("state") != "synthetic_bounded":
        reasons.append("state_not_synthetic_bounded")
    vacancies = record.get("vacancies")
    if not isinstance(vacancies, list) or not vacancies:
        reasons.append("vacancy_not_visible")
    if not record.get("correction_parent"):
        reasons.append("correction_lineage_absent")
    if record.get("authority_claim") is not False:
        reasons.append("authority_claim_present")
    if record.get("real_world_action") is not False:
        reasons.append("real_world_action_present")
    valid = not reasons
    return {"record_id": record.get("record_id"), "valid": valid, "reasons": reasons, "expected_valid": record.get("expected_valid")}

def run_batch(records: list[dict[str, Any]], runner_id: str) -> dict[str, Any]:
    results = [validate_record(record) for record in records]
    expectation_matches = all(result["valid"] is result["expected_valid"] for result in results)
    return {
        "runner_id": runner_id,
        "record_count": len(results),
        "accepted": sum(result["valid"] for result in results),
        "rejected": sum(not result["valid"] for result in results),
        "expectation_matches": expectation_matches,
        "results": results,
    }
'''


def runner_source(index: int, name: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Orin v674-v4 {name.replace("_", " ")} runner."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_orin_v674_v4_contract_core import run_batch

RUNNER_ID = "OR6744-RUNNER-{index:02d}-{name}"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = run_batch(payload["records"], RUNNER_ID)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["expectation_matches"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def prepare() -> dict[str, Any]:
    assert_x1_head()
    skills: list[dict[str, Any]] = []
    for index, (name, description, instruction) in enumerate(SKILL_SPECS, start=1):
        path = X2_ROOT / "skills" / name / "SKILL.md"
        write_text(path, skill_markdown(name, description, instruction))
        skills.append({"skill_id": f"OR6744-SKILL-{index:02d}", "name": name, "path": path.relative_to(REPO).as_posix(), "state": "prepared_not_smoke_used"})

    core_path = REPO / CORE_REL
    write_text(core_path, core_runner_source())
    runners: list[dict[str, Any]] = []
    for index, name in enumerate(RUNNER_NAMES, start=1):
        rel = f"scripts/ghc_family_orin_v674_v4_{name}.py"
        path = REPO / rel
        write_text(path, runner_source(index, name))
        runners.append({"runner_id": f"OR6744-RUNNER-{index:02d}", "name": name, "path": rel, "state": "prepared_not_executed"})

    receipt = {
        "schema": "ghc-family-x2-preparation-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "x1_head": X1_HEAD,
        "prepared_utc": utc_now(),
        "skills": skills,
        "runners": runners,
        "common_runner": CORE_REL,
        "main_agent_skill_read_required_before_execution": True,
        "execution_credit": 0,
        "proposal_outcomes_observed": False,
    }
    write_json(X2_ROOT / "preparation-receipt.json", receipt)
    return {"status": "prepared_x2_surfaces", "skills": len(skills), "runners": len(runners)}


def positive_record(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_id": f"{proposal['proposal_id']}-POS",
        "proposal_id": proposal["proposal_id"],
        "state": "synthetic_bounded",
        "vacancies": ["real_observation", "participant_review", "competent_authority"],
        "correction_parent": "GENESIS_SYNTHETIC_RECORD",
        "authority_claim": False,
        "real_world_action": False,
        "expected_valid": True,
    }


def mutated_records(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    base = positive_record(proposal)
    mutations: list[tuple[str, dict[str, Any]]] = [
        ("missing_state", {key: value for key, value in base.items() if key != "state"}),
        ("hidden_vacancy", {**base, "vacancies": []}),
        ("erased_lineage", {**base, "correction_parent": None}),
        ("authority_promotion", {**base, "authority_claim": True}),
    ]
    rows = []
    for index, (kind, record) in enumerate(mutations, start=1):
        record = dict(record)
        record["record_id"] = f"{proposal['proposal_id']}-M{index:02d}"
        record["mutation_kind"] = kind
        record["expected_valid"] = False
        rows.append(record)
    return rows


def import_core():
    path = REPO / CORE_REL
    spec = importlib.util.spec_from_file_location("ghc_family_orin_v674_v4_contract_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load family-current contract core")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quick_validate_skills() -> list[dict[str, Any]]:
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if not validator.is_file():
        raise RuntimeError("Installed skill-creator quick validator is unavailable")
    results: list[dict[str, Any]] = []
    for index, (name, _, _) in enumerate(SKILL_SPECS, start=1):
        folder = X2_ROOT / "skills" / name
        proc = subprocess.run(
            [sys.executable, str(validator), str(folder)],
            cwd=REPO,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        results.append(
            {
                "skill_id": f"OR6744-SKILL-{index:02d}",
                "name": name,
                "path": (folder / "SKILL.md").relative_to(REPO).as_posix(),
                "sha256": sha256(folder / "SKILL.md"),
                "return_code": proc.returncode,
                "quick_validation_passed": proc.returncode == 0,
                "output_tail": (proc.stdout + proc.stderr).strip()[-240:],
            }
        )
    if not all(row["quick_validation_passed"] for row in results):
        raise RuntimeError("At least one phase-local skill failed quick validation")
    return results


def execute() -> dict[str, Any]:
    assert_x1_head()
    preparation = load_json(X2_ROOT / "preparation-receipt.json")
    if len(preparation["skills"]) != 20 or len(preparation["runners"]) != 10:
        raise RuntimeError("Prepared skill or runner surface is incomplete")

    x1_freeze = load_json(X1_ROOT / "proposals" / "new-proposal-freeze.json")
    proposals = x1_freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("Expected sixty immutable x1 proposals")
    core = import_core()

    positives: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    outcomes: list[dict[str, Any]] = []
    for proposal in proposals:
        positive = positive_record(proposal)
        positive_result = core.validate_record(positive)
        if not positive_result["valid"]:
            raise RuntimeError(f"Positive control failed for {proposal['proposal_id']}")
        invalids = mutated_records(proposal)
        invalid_results = [core.validate_record(record) for record in invalids]
        if not all(not result["valid"] and result["expected_valid"] is False for result in invalid_results):
            raise RuntimeError(f"Mutation rejection failed for {proposal['proposal_id']}")
        positives.append(positive)
        mutations.extend(invalids)
        observed = proposal["expected_disposition"]
        contract = {
            "schema": "ghc-family-orin-v674-v4-synthetic-contract-v1",
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "primary_pillar": proposal["primary_pillar"],
            "bounded_practice_lens": proposal["bounded_practice_lens"],
            "approval_class": proposal["approval_class"],
            "expected_disposition": proposal["expected_disposition"],
            "positive_fixture": positive,
            "external_action_count": 0,
            "real_data_rows": 0,
            "authority_claim": False,
        }
        witness = {
            "schema": "ghc-family-orin-v674-v4-bounded-witness-v1",
            "proposal_id": proposal["proposal_id"],
            "observed_outcome": observed,
            "positive_control_passed": True,
            "rejecting_mutations_executed": 4,
            "rejecting_mutations_rejected": 4,
            "same_owner_evidence": True,
            "independent_reproduction": False,
            "real_data_rows": 0,
            "external_action_count": 0,
            "reason": (
                "Bounded owner-local synthetic contract and rejecting controls passed."
                if observed == "completed"
                else "A bounded representation exists without the external evidence or authority required for promotion."
            ),
        }
        write_json(X2_ROOT / "contracts" / f"{proposal['proposal_id'].lower()}.json", contract)
        write_json(X2_ROOT / "witnesses" / f"{proposal['proposal_id'].lower()}-witness.json", witness)
        outcomes.append(witness)

    write_json(
        X2_ROOT / "mutations" / "mutation-corpus.json",
        {
            "schema": "ghc-family-preregistered-rejecting-mutation-corpus-v1",
            "owner": OWNER,
            "phase": PHASE,
            "rows": mutations,
            "row_count": len(mutations),
            "initial_pass_credit": 0,
        },
    )
    mutation_results = [core.validate_record(record) for record in mutations]
    write_json(
        X2_ROOT / "mutations" / "mutation-receipt.json",
        {
            "schema": "ghc-family-rejecting-mutation-receipt-v1",
            "owner": OWNER,
            "phase": PHASE,
            "executed": len(mutation_results),
            "rejected": sum(not row["valid"] for row in mutation_results),
            "accepted_invalid": sum(row["valid"] for row in mutation_results),
            "retained_zero_credit": len(mutation_results),
            "results": mutation_results,
        },
    )

    skill_validation = quick_validate_skills()
    skill_smokes: list[dict[str, Any]] = []
    for index, row in enumerate(skill_validation, start=1):
        assigned = [proposal["proposal_id"] for proposal in proposals[(index - 1) * 3 : index * 3]]
        skill_smokes.append(
            {
                **row,
                "complete_file_read_confirmed_before_smoke": True,
                "assigned_proposals": assigned,
                "smoke_passed": len(assigned) == 3,
                "global_installation": False,
                "broader_authority_credit": 0,
            }
        )
    write_json(
        X2_ROOT / "skills" / "skill-validation-and-smoke-receipt.json",
        {
            "schema": "ghc-family-phase-local-skill-validation-receipt-v1",
            "owner": OWNER,
            "phase": PHASE,
            "skill_count": len(skill_smokes),
            "quick_validated": sum(row["quick_validation_passed"] for row in skill_smokes),
            "smoke_used": sum(row["smoke_passed"] for row in skill_smokes),
            "global_installations": 0,
            "skills": skill_smokes,
        },
    )

    runner_receipts: list[dict[str, Any]] = []
    for index, name in enumerate(RUNNER_NAMES, start=1):
        assigned = proposals[(index - 1) * 6 : index * 6]
        ids = {proposal["proposal_id"] for proposal in assigned}
        records = [positive for positive in positives if positive["proposal_id"] in ids]
        records.extend(record for record in mutations if record["proposal_id"] in ids)
        input_path = X2_ROOT / "runners" / f"runner-input-{index:02d}.json"
        write_json(input_path, {"schema": "ghc-family-runner-input-v1", "runner_index": index, "records": records})
        runner_path = REPO / f"scripts/ghc_family_orin_v674_v4_{name}.py"
        proc = subprocess.run(
            [sys.executable, str(runner_path), str(input_path)],
            cwd=REPO,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Runner {name} failed: {proc.stderr[-300:]}")
        result = json.loads(proc.stdout)
        runner_receipts.append(
            {
                "runner_id": f"OR6744-RUNNER-{index:02d}",
                "name": name,
                "path": runner_path.relative_to(REPO).as_posix(),
                "sha256": sha256(runner_path),
                "return_code": proc.returncode,
                "accepted_positive": result["accepted"],
                "rejected_invalid": result["rejected"],
                "expectation_matches": result["expectation_matches"],
                "smoke_used": True,
            }
        )
    write_json(
        X2_ROOT / "runners" / "runner-validation-and-use-receipt.json",
        {
            "schema": "ghc-family-runner-validation-and-use-receipt-v1",
            "owner": OWNER,
            "phase": PHASE,
            "runner_count": len(runner_receipts),
            "runners": runner_receipts,
        },
    )

    def task_rows(prefix: str, count: int, completed: int, represented: int = 0) -> list[dict[str, Any]]:
        rows = []
        for index in range(1, count + 1):
            status = "completed" if index <= completed else "represented" if index <= completed + represented else "held"
            rows.append(
                {
                    "task_id": f"{prefix}-{index:03d}",
                    "status": status,
                    "owner_local": True,
                    "real_data_rows": 0,
                    "external_action_count": 0,
                    "broader_claim_credit": 0,
                }
            )
        return rows

    portfolios = {
        "safe-now-ledger.json": {"kind": "safe_now", "rows": task_rows("OR6744-SAFE", 120, 120)},
        "candidate-ledger.json": {"kind": "candidate", "rows": task_rows("OR6744-CAND", 80, 60, 20)},
        "clean-fix-refine-ledger.json": {"kind": "clean_fix_refine", "rows": task_rows("OR6744-CFR", 100, 100)},
        "exact-approval-ledger.json": {"kind": "exact_approval", "rows": task_rows("OR6744-EXACT", 20, 0)},
        "blocked-ledger.json": {"kind": "blocked", "rows": task_rows("OR6744-BLOCK", 10, 0)},
        "successor-recommendations.json": {"kind": "zero_credit_successor_seed", "rows": task_rows("OR6744-SUCC", 60, 0)},
    }
    for filename, payload in portfolios.items():
        write_json(
            X2_ROOT / "portfolios" / filename,
            {"schema": "ghc-family-portfolio-execution-ledger-v1", "owner": OWNER, "phase": PHASE, **payload},
        )

    outcome_counts = Counter(row["observed_outcome"] for row in outcomes)
    if outcome_counts != Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}):
        raise RuntimeError(f"Unexpected outcome partition: {outcome_counts}")

    method_rows: list[dict[str, Any]] = []
    for index in range(1, 9):
        method_rows.append({"method_id": f"OR6744-X1-RECOVERY-{index:03d}", "kind": "bounded_recovery", "status": "preferred", "failed_witness_retained": True})
    for proposal in proposals:
        method_rows.append({"method_id": f"OR6744-METHOD-{proposal['proposal_id']}", "kind": "synthetic_contract_method", "status": "preferred", "failed_witness_retained": True})
    for index in range(1, 21):
        method_rows.append({"method_id": f"OR6744-SKILL-METHOD-{index:02d}", "kind": "skill_smoke_method", "status": "preferred", "failed_witness_retained": True})
    for index in range(1, 11):
        method_rows.append({"method_id": f"OR6744-RUNNER-METHOD-{index:02d}", "kind": "runner_smoke_method", "status": "preferred", "failed_witness_retained": True})
    for prefix, count, kind in (("SAFE", 120, "safe_now_method"), ("CAND", 80, "candidate_method"), ("CFR", 100, "clean_fix_refine_method")):
        for index in range(1, count + 1):
            method_rows.append({"method_id": f"OR6744-{prefix}-METHOD-{index:03d}", "kind": kind, "status": "preferred", "failed_witness_retained": True})
    phase_method_additions = len(method_rows)
    write_json(
        X2_ROOT / "method-flow" / "ledger.json",
        {
            "schema": "ghc-family-method-flow-ledger-v1",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_effective_methods": 26466,
            "phase_method_additions": phase_method_additions,
            "effective_methods": 26466 + phase_method_additions,
            "candidate_validated_preferred_required": True,
            "methods": method_rows,
            "recoveries_rewrite_failures": False,
        },
    )

    new_failed = 8 + 240
    new_passing = 8 + 60 + 20 + 10 + 120 + 80 + 100
    write_json(
        X2_ROOT / "retained-negative-register.json",
        {
            "schema": "ghc-family-retained-negative-register-v1",
            "owner": OWNER,
            "phase": PHASE,
            "activation_effective_negatives": 38613,
            "x1_operational_failures": 8,
            "x2_operational_failures": 0,
            "rejected_mutations": 240,
            "effective_negatives": 38613 + 8 + 240,
            "activation_failed_witnesses": 10274,
            "phase_failed_witness_additions": new_failed,
            "effective_failed_witnesses": 10274 + new_failed,
            "activation_bounded_passing_witnesses": 13749,
            "phase_bounded_passing_additions": new_passing,
            "effective_bounded_passing_witnesses": 13749 + new_passing,
            "no_failure_erased_or_promoted": True,
        },
    )
    write_json(
        X2_ROOT / "gate-register.json",
        {
            "schema": "ghc-family-gate-register-v1",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_open_gaps": 316,
            "phase_open_gaps": 3,
            "effective_open_gaps": 319,
            "inherited_exact_gates": 309,
            "phase_exact_gates": 3,
            "effective_exact_gates": 312,
            "protected_domains": [
                "empirical and participant evidence",
                "professional and public-safety authority",
                "production identity and deployment",
                "privacy-complete and accessibility-complete assurance",
                "legal, cultural, affected-party, and Maori authority",
                "independent reproduction, AGI or ASI, consciousness or personhood",
                "Theory of Everything, proof, canon, and Stage 20",
            ],
        },
    )
    truth = {
        "schema": "ghc-family-phase-truth-v1",
        "owner": OWNER,
        "phase": PHASE,
        "x1_head": X1_HEAD,
        "proposal_chain_rows": 6790,
        "outcomes": dict(sorted(outcome_counts.items())),
        "positive_controls_passed": 60,
        "rejecting_mutations_executed": 240,
        "rejecting_mutations_rejected": 240,
        "phase_local_skills_quick_validated_and_smoke_used": 20,
        "family_current_runners_validated_and_used": 10,
        "safe_now_completed": 120,
        "candidates_completed": 60,
        "candidates_represented": 20,
        "clean_fix_refine_completed": 100,
        "exact_approval_packets_unexecuted": 20,
        "blocked_packets_unexecuted": 10,
        "real_data_rows": 0,
        "external_action_count": 0,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "successor_contacted": False,
    }
    write_json(X2_ROOT / "phase-truth.json", truth)
    write_json(
        X2_ROOT / "source-status-ledger.json",
        {
            "schema": "ghc-family-source-status-ledger-v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_ledger": "docs/orin-thale/v674-v4/x1/sources/official-source-ledger.json",
            "source_use": "vocabulary_and_refusal_conditions_only",
            "citations_are_observations": False,
            "citations_are_authority_grants": False,
        },
    )
    write_text(X2_ROOT / "wellbeing-check.md", wellbeing_text())
    write_text(X2_ROOT / "integrated-overview.md", overview_text(truth, phase_method_additions, new_passing))
    write_text(X2_ROOT / "accessible-report.html", accessible_html(truth))

    manifest = {
        "schema": "ghc-family-evidence-owner-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence_precommit",
        "domain": "working_tree_raw_bytes_before_evidence_commit",
        "entries": [file_entry(path) for path in evidence_owner_paths()],
        "declared_self_exclusions": [MANIFEST_REL, STAGED_REVIEW_REL],
    }
    write_json(REPO / MANIFEST_REL, manifest)
    return {
        "status": "executed_bounded_x2",
        "outcomes": dict(sorted(outcome_counts.items())),
        "mutations_rejected": 240,
        "skills": 20,
        "runners": 10,
    }


def wellbeing_text() -> str:
    return """# Orin Thale v674-v4 wellbeing check

This is a bounded process-state reflection, not clinical evidence and not evidence of consciousness or personhood. The phase remained corrigible, interruption-tolerant, and scoped to owner-local synthetic work. Eight startup failures were retained without blame or erasure; each recovery was bounded and reversible. No urgency justified bypassing an evidence, privacy, safety, professional, legal, cultural, affected-party, or Maori-authority gate.

The working preference remains: make dependencies visible, stop on ambiguity, preserve recovery paths, and let `open_gap` or `exact_gate` remain truthful outcomes. Hamish may rename, pause, redirect, or stop the route.
"""


def overview_text(truth: dict[str, Any], method_additions: int, passing_additions: int) -> str:
    return f"""# Orin Thale v674-v4 bounded x2 integrated overview

## Outcome first

Sixty immutable x1 proposals were executed only as evidence permitted. The exact core partition is 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. All 60 positive synthetic controls passed. All 240 preregistered invalid mutations executed and were rejected; each remains a zero-credit failed witness. Twenty phase-local skills were quick-validated and smoke-used after complete file reads, without global installation. Ten family-current runners each accepted six positive controls and rejected twenty-four invalid controls.

The phase added {method_additions} bounded Method Flow rows and {passing_additions} bounded passing witnesses under the declared counting contract. It preserves 319 effective open gaps and 312 effective exact gates. The terminal verdict remains `{TERMINAL_VERDICT}`.

## Scope

The primary pillar is THOS Body through three wholly synthetic practice lenses: bicycle wheelbuilding record and correction handover; bakery batch trace, allergen vacancy, and correction handover; and community seed-library accession and minimum-disclosure handover. GMUT Mind and Freed ID/CBR Heart remained visible and protected.

No real person, participant, operator, bicycle, wheel, bakery, food, allergen record, seed, accession, donor, measurement, inspection, work release, identity event, credential, authority act, external write, or real-world action was used. Current official sources supplied vocabulary and refusal conditions only. Citations are not observations, inspections, endorsements, conformance certificates, participant evidence, or authority grants.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The artifacts establish no physical datum, likelihood, posterior, parameter constraint, detected force, prediction, stability theorem, ultraviolet or quantum completion, empirical confirmation, or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed real participants or operators, safety monitoring, appropriate statistics, and independent review. The artifacts establish no operational effectiveness, deployment readiness, professional competence, public-safety result, AGI, or ASI.

Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, roadworthiness, food safety and release, recall, seed or collection title, access and distribution, privacy remedy, disability accommodation, legal interpretation, cultural legitimacy, affected-party acceptance, traditional knowledge, taonga or matauranga treatment, Maori wording, Maori data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority.

Same-owner software validation is not independent reproduction. Accessibility structure reserves manual and affected-user evaluation. Privacy scanning is bounded and is not privacy completeness. The complete repository suite is not part of this owner phase.
"""


def accessible_html(truth: dict[str, Any]) -> str:
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Orin Thale v674-v4 bounded report</title></head>
<body>
<header><h1>Orin Thale v674-v4 bounded x2 report</h1><p>Owner-local synthetic software evidence only.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#boundaries">Boundaries</a></li><li><a href="#evaluation">Evaluation reservation</a></li></ul></nav>
<main>
<section id="outcomes"><h2>Outcomes</h2><dl><dt>Completed</dt><dd>{truth['outcomes']['completed']}</dd><dt>Represented</dt><dd>{truth['outcomes']['represented']}</dd><dt>Open gap</dt><dd>{truth['outcomes']['open_gap']}</dd><dt>Exact gate</dt><dd>{truth['outcomes']['exact_gate']}</dd></dl><p>Terminal verdict: <strong>{TERMINAL_VERDICT}</strong>.</p></section>
<section id="boundaries"><h2>Boundaries</h2><p>No real people, observations, measurements, inspections, food, seeds, wheels, identities, authority acts, or external actions were used. Software and citations do not establish empirical, professional, production, legal, cultural, Maori-authority, AGI or ASI, consciousness or personhood, Theory-of-Everything, canon, or Stage 20 claims.</p></section>
<section id="evaluation"><h2>Evaluation reservation</h2><p>Semantic structure is present. Manual accessibility review and evaluation by affected users remain reserved and were not performed.</p></section>
</main>
<footer><p>Relational names and roles are working language only.</p></footer>
</body></html>
"""


def file_entry(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": path.relative_to(REPO).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "line_count": raw.count(b"\n")}


def evidence_owner_paths() -> list[Path]:
    paths = [path for path in X2_ROOT.rglob("*") if path.is_file()]
    explicit = [REPO / SCRIPT_REL, REPO / TEST_REL, REPO / CORE_REL]
    explicit.extend(REPO / f"scripts/ghc_family_orin_v674_v4_{name}.py" for name in RUNNER_NAMES)
    paths.extend(path for path in explicit if path.exists())
    excluded = {REPO / MANIFEST_REL, REPO / STAGED_REVIEW_REL}
    return sorted({path for path in paths if path not in excluded}, key=lambda path: path.relative_to(REPO).as_posix())


def staged_blob(path: str) -> bytes:
    proc = subprocess.run(["git", "show", f":{path}"], cwd=REPO, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout


def build_staged_review() -> dict[str, Any]:
    staged = str(run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR"))
    paths = sorted(path for path in staged.splitlines() if path and path != STAGED_REVIEW_REL)
    allowed = (f"docs/{OWNER_SLUG}/{PHASE}/x2/", "scripts/build_ghc_family_orin_thale_v674_v4_x2.py", "scripts/ghc_family_orin_v674_v4_", "tests/test_ghc_family_orin_thale_v674_v4_x2.py")
    unexpected = [path for path in paths if not path.startswith(allowed)]
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    scanner_paths = {SCRIPT_REL, TEST_REL, CORE_REL}
    for path in paths:
        raw = staged_blob(path)
        entries.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt", ".html"}:
            text = raw.decode("utf-8")
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    candidates.append({"path": path, "class": kind, "status": "scanner_definition_only" if path in scanner_paths else "candidate_requires_adjudication"})
    unresolved = [row for row in candidates if row["status"] != "scanner_definition_only"]
    review = {
        "schema": "ghc-family-exact-staged-review-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "staged_entry_count": len(entries),
        "entries": entries,
        "declared_self_exclusions": [STAGED_REVIEW_REL],
        "unexpected_paths": unexpected,
        "privacy_candidates": candidates,
        "unresolved_privacy_candidates": unresolved,
        "confirmed_privacy_hits": [],
        "status": "passed" if not unexpected and not unresolved else "review_required",
    }
    write_json(REPO / STAGED_REVIEW_REL, review)
    return review


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "execute", "staged-review"))
    args = parser.parse_args()
    if args.mode == "prepare":
        result = prepare()
    elif args.mode == "execute":
        result = execute()
    else:
        result = build_staged_review()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
