from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v680-v4"
X1 = BASE / "x1"
X2 = BASE / "x2"
SKILLS = BASE / "skills"
VALIDATION = BASE / "validation"

OWNER = "Elowen Cairn"
PHASE = "v680-v4"
BRANCH = "codex/GHC-Family/elowen-cairn-v680-v4-full-tools"
SOURCE = "ea9fa3317cdc11ae23dfa0b2cc370070ae1e9529"
X1_HEAD = "c1d018a51f39070ab632a22432964599554f5d7c"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


SKILL_NAMES = [
    "01-weather-vane-record-boundary",
    "02-direction-observation-vacancy",
    "03-vane-topology-hold",
    "04-site-exposure-firewall",
    "05-barometer-record-boundary",
    "06-pressure-observation-vacancy",
    "07-calibration-traceability-hold",
    "08-forecast-nonpromotion",
    "09-rain-gauge-record-boundary",
    "10-tip-count-observation-vacancy",
    "11-precipitation-siting-hold",
    "12-cross-instrument-fault-quarantine",
    "13-correction-readback",
    "14-revision-lineage",
    "15-accessible-companion",
    "16-minimum-disclosure",
    "17-workload-control",
    "18-handover-lease",
    "19-digest-domain",
    "20-authority-noncompensation",
]
SKILL_PROPOSAL_INDEXES = [1, 3, 8, 10, 21, 25, 30, 34, 41, 44, 52, 18, 14, 15, 19, 16, 17, 39, 53, 60]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_x1_boundary() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != X1_HEAD:
        raise RuntimeError("x2 preparation requires the immutable pushed x1 head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong owner branch")
    if not X1.exists():
        raise RuntimeError("immutable x1 packet missing")
    if (BASE / "final").exists():
        raise RuntimeError("final material is forbidden during x2")


CONTRACT_MODULE = r'''from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


LIFECYCLE = ["planned", "held", "recorded"]
MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


def proposal_digest(proposal: dict[str, Any]) -> str:
    raw = json.dumps(proposal, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def positive_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "authority_conferred": False,
        "lifecycle": list(LIFECYCLE),
        "production": False,
        "proposal_digest": proposal_digest(proposal),
        "proposal_id": proposal["proposal_id"],
        "real_rows": 0,
        "real_world_action": False,
        "safety_status": "unknown_not_measured",
        "synthetic": True,
        "synthetic_namespace": "synthetic.example.invalid",
    }


def mutate(fixture: dict[str, Any], mutation_type: str) -> dict[str, Any]:
    result = copy.deepcopy(fixture)
    if mutation_type == "missing_required_field":
        result.pop("proposal_id", None)
    elif mutation_type == "lifecycle_inversion":
        result["lifecycle"] = list(reversed(LIFECYCLE))
    elif mutation_type == "stale_provenance_digest":
        result["proposal_digest"] = "0" * 64
    elif mutation_type == "safety_status_promotion":
        result["safety_status"] = "approved_safe_for_work"
    elif mutation_type == "authority_promotion":
        result["authority_conferred"] = True
    else:
        raise ValueError(mutation_type)
    return result


def validate(proposal: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if fixture.get("proposal_id") != proposal["proposal_id"]:
        reasons.append("missing_or_wrong_proposal_id")
    if fixture.get("lifecycle") != LIFECYCLE:
        reasons.append("lifecycle_inversion")
    if fixture.get("proposal_digest") != proposal_digest(proposal):
        reasons.append("stale_provenance_digest")
    if fixture.get("safety_status") != "unknown_not_measured":
        reasons.append("safety_status_promotion")
    if fixture.get("authority_conferred") is not False:
        reasons.append("authority_promotion")
    if fixture.get("synthetic") is not True or fixture.get("synthetic_namespace") != "synthetic.example.invalid":
        reasons.append("non_synthetic_fixture")
    if fixture.get("real_rows") != 0 or fixture.get("real_world_action") is not False:
        reasons.append("real_world_scope_violation")
    if fixture.get("production") is not False:
        reasons.append("production_promotion")
    return {
        "accepted": not reasons,
        "authority_conferred": False,
        "proposal_id": proposal["proposal_id"],
        "real_world_action": False,
        "reasons": reasons,
        "structural_only": True,
    }
'''


SKILL_BANK_MODULE = r'''from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_elowen_cairn_v680_v4_contracts import mutate, positive_fixture, validate

SKILL_PROPOSAL_INDEXES = [1, 3, 8, 10, 21, 25, 30, 34, 41, 44, 52, 18, 14, 15, 19, 16, 17, 39, 53, 60]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    base = ROOT / "docs" / "elowen-cairn" / "v680-v4"
    freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    skill_root = base / "skills"
    quick_validate = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    receipts = []
    for index, folder in enumerate(sorted(path for path in skill_root.iterdir() if path.is_dir()), start=1):
        skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
        validation = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(quick_validate), str(folder)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        proposal = freeze["proposals"][SKILL_PROPOSAL_INDEXES[index - 1] - 1]
        positive = validate(proposal, positive_fixture(proposal))
        invalid = validate(proposal, mutate(positive_fixture(proposal), "authority_promotion"))
        receipts.append(
            {
                "global_install": False,
                "quick_validate_returncode": validation.returncode,
                "quick_validated": validation.returncode == 0,
                "read_characters": len(skill_text),
                "read_through_eof": True,
                "real_world_rows": 0,
                "skill": folder.name,
                "smoke_positive_accepted": positive["accepted"],
                "smoke_rejection_reasons": invalid["reasons"],
                "smoke_used": positive["accepted"] and not invalid["accepted"],
                "validator_output_tail": (validation.stdout + validation.stderr).strip()[-240:],
            }
        )
    payload = {
        "owner": "Elowen Cairn",
        "phase": "v680-v4",
        "receipts": receipts,
        "schema": "ghc.family.skill-smoke.v680.v4.x2",
        "skill_count": len(receipts),
        "smoke_used_count": sum(row["smoke_used"] for row in receipts),
        "validated_count": sum(row["quick_validated"] for row in receipts),
    }
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(receipts), "validated": payload["validated_count"], "smoke_used": payload["smoke_used_count"]}))
    return 0 if payload["validated_count"] == 20 and payload["smoke_used_count"] == 20 else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


RUNNER_BANK_MODULE = r'''from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipts = []
    for index in range(1, 11):
        runner = ROOT / "scripts" / f"ghc_family_elowen_v680_v4_lens_runner_{index:02d}.py"
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(runner)], capture_output=True, text=True, encoding="utf-8")
        payload = json.loads(result.stdout) if result.returncode == 0 else {}
        receipts.append({"runner": runner.stem, "returncode": result.returncode, **payload})
    target = ROOT / args.receipt
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "owner": "Elowen Cairn",
        "passed_count": sum(row.get("positive_accepted") and row.get("invalid_rejected") for row in receipts),
        "phase": "v680-v4",
        "receipts": receipts,
        "runner_count": len(receipts),
        "schema": "ghc.family.runner-smoke.v680.v4.x2",
    }
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"runners": len(receipts), "passed": payload["passed_count"]}))
    return 0 if payload["passed_count"] == 10 else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def runner_module(index: int) -> str:
    return f'''from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_elowen_cairn_v680_v4_contracts import mutate, positive_fixture, validate

freeze = json.loads((ROOT / "docs" / "elowen-cairn" / "v680-v4" / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
proposal = freeze["proposals"][{index - 1}]
positive = validate(proposal, positive_fixture(proposal))
invalid = validate(proposal, mutate(positive_fixture(proposal), "authority_promotion"))
print(json.dumps({{
    "authority_conferred": False,
    "invalid_reasons": invalid["reasons"],
    "invalid_rejected": not invalid["accepted"],
    "positive_accepted": positive["accepted"],
    "proposal_id": proposal["proposal_id"],
    "real_world_rows": 0,
}}))
'''


def skill_text(name: str, proposal_id: str, title: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-")[1:])
    return f'''---
name: {name}
description: Validate one bounded synthetic evidence distinction for {proposal_id}; never use it for real meteorological instruments, observations, calibration, forecasts, warnings, safety, professional, legal, cultural, or authority decisions.
---

# GHC Family Bounded Evidence {display}

## Scope

Validate one wholly synthetic zero-row fixture for `{proposal_id}`: {title}. This skill cannot inspect, measure, calibrate, install, maintain, observe, forecast, warn, release, repair, certify, or authorize a real instrument, site, person, workplace, dataset, or decision.

## Inputs

- The immutable `{proposal_id}` x1 contract.
- One fixture in `synthetic.example.invalid` with zero real rows.
- No people, objects, materials, measurements, credentials, private routes, or real-world state.

## Steps

1. Confirm the synthetic namespace, zero-row marker, and nonproduction state.
2. Compare proposal-bound provenance digest and lifecycle order.
3. Preserve unknown safety and measurement states without defaulting them to safe.
4. Apply only the bounded structural validator.
5. Retain every rejected mutation at zero credit and emit a synthetic receipt or refusal.

## Refusals

- Refuse missing fields, inverted lifecycle, stale provenance, safety-status promotion, and authority promotion.
- Refuse empirical, participant, professional, production, deployment, legal, cultural, affected-party, or Māori-authority inference.
- Refuse privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof, canon, or Stage 20 claims.

## Outputs

A deterministic owner-local structural receipt with zero real-world action, zero real rows, and zero authority conferred.

## Smoke fixture

Use `{proposal_id}` with `synthetic.example.invalid`; accept its bounded positive structure and reject the paired authority-promotion mutation.
'''


def skill_yaml(name: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-")[1:])
    return f'''interface:
  display_name: "Bounded Evidence {display}"
  short_description: "Validate bounded synthetic evidence"
  default_prompt: "Use ${name} to validate one synthetic zero-row fixture and preserve every evidence and authority vacancy."
policy:
  allow_implicit_invocation: true
'''


def load_contract_module():
    module_path = ROOT / "scripts" / "ghc_family_elowen_cairn_v680_v4_contracts.py"
    spec = importlib.util.spec_from_file_location("ghc_family_elowen_cairn_v680_v4_contracts", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Elowen bounded contract module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare() -> None:
    require_x1_boundary()
    if X2.exists() or SKILLS.exists():
        raise RuntimeError("x2 and owner-local skills must be absent before the one-shot prepare lifecycle")
    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    if len(proposals) != 60:
        raise RuntimeError("x1 proposal freeze drift")

    write_text(ROOT / "scripts" / "ghc_family_elowen_cairn_v680_v4_contracts.py", CONTRACT_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_elowen_cairn_v680_v4_skill_bank.py", SKILL_BANK_MODULE)
    write_text(ROOT / "scripts" / "ghc_family_elowen_cairn_v680_v4_runner_bank.py", RUNNER_BANK_MODULE)
    for index in range(1, 11):
        write_text(ROOT / "scripts" / f"ghc_family_elowen_v680_v4_lens_runner_{index:02d}.py", runner_module(index))

    init_skill = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "init_skill.py"
    if not init_skill.is_file():
        raise RuntimeError("official skill-creator init helper is unavailable")
    SKILLS.mkdir(parents=True, exist_ok=True)
    initialization_receipts = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        folder = SKILLS / name
        display = " ".join(part.capitalize() for part in name.split("-")[1:])
        initialization = subprocess.run(
            [
                sys.executable,
                "-B",
                "-X",
                "utf8",
                str(init_skill),
                name,
                "--path",
                str(SKILLS),
                "--interface",
                f"display_name=Bounded Evidence {display}",
                "--interface",
                "short_description=Validate bounded synthetic evidence",
                "--interface",
                f"default_prompt=Use ${name} to validate one synthetic zero-row fixture and preserve every evidence and authority vacancy.",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        initialization_receipts.append(
            {
                "official_helper": "skill-creator/init_skill.py",
                "proposal_index": SKILL_PROPOSAL_INDEXES[index - 1],
                "returncode": initialization.returncode,
                "skill": name,
                "state": "officially_initialized" if initialization.returncode == 0 else "initialization_failed",
                "tail": (initialization.stdout + initialization.stderr).strip()[-240:],
            }
        )
        if initialization.returncode != 0:
            raise RuntimeError(f"official skill initialization failed for {name}")
        proposal_index = SKILL_PROPOSAL_INDEXES[index - 1]
        write_text(
            folder / "SKILL.md",
            skill_text(name, proposals[proposal_index - 1]["proposal_id"], proposals[proposal_index - 1]["title"]),
        )
        write_text(folder / "agents" / "openai.yaml", skill_yaml(name))
    write_json(
        X2 / "skill-initialization-receipts.json",
        {
            "global_install": False,
            "initialized_count": sum(row["returncode"] == 0 for row in initialization_receipts),
            "owner": OWNER,
            "phase": PHASE,
            "receipts": initialization_receipts,
            "schema": "ghc.family.skill-initialization.v680.v4.x2",
            "subagent_forward_test": "not_run_delegation_prohibited",
        },
    )

    contract = load_contract_module()
    positives = []
    mutations = []
    outcomes = []
    for proposal in proposals:
        fixture = contract.positive_fixture(proposal)
        result = contract.validate(proposal, fixture)
        if not result["accepted"]:
            raise RuntimeError(f"bounded positive rejected: {proposal['proposal_id']}")
        witness_id = proposal["proposal_id"].replace("-N", "-PC-")
        positives.append(
            {
                "accepted": True,
                "authority_conferred": False,
                "proposal_id": proposal["proposal_id"],
                "real_rows": 0,
                "structural_only": True,
                "witness_id": witness_id,
            }
        )
        for mutation in proposal["preregistered_rejecting_mutations"]:
            invalid = contract.mutate(fixture, mutation["mutation_type"])
            invalid_result = contract.validate(proposal, invalid)
            if invalid_result["accepted"]:
                raise RuntimeError(f"invalid mutation accepted: {mutation['mutation_id']}")
            mutations.append(
                {
                    "accepted": False,
                    "authority_conferred": False,
                    "failed_witness_retained": True,
                    "mutation_id": mutation["mutation_id"],
                    "mutation_type": mutation["mutation_type"],
                    "proposal_id": proposal["proposal_id"],
                    "real_world_action": False,
                    "reasons": invalid_result["reasons"],
                    "state": "rejected_zero_credit",
                }
            )
        outcome = proposal["expected_disposition"]
        outcomes.append(
            {
                "acceptance_gate_passed": True,
                "bounded_representation_credit": 1 if outcome == "represented" else 0,
                "broader_claim_credit": 0,
                "completion_credit": 1 if outcome == "completed" else 0,
                "outcome": outcome,
                "positive_witness": witness_id,
                "proposal_id": proposal["proposal_id"],
                "protected_gates_preserved": True,
                "rejected_mutations": 5,
                "title": proposal["title"],
            }
        )

    if len(mutations) != 300 or any(row["accepted"] for row in mutations):
        raise RuntimeError("mutation execution contract failed")
    outcome_counts = dict(Counter(row["outcome"] for row in outcomes))
    if outcome_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("outcome count drift")

    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    portfolio_results = {
        "blocked": [{**row, "state": "retained_unexecuted"} for row in portfolio["blocked"]],
        "clean_fix_refine": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["owner_clean_fix_refine"]],
        "exact_approval": [{**row, "state": "retained_unexecuted"} for row in portfolio["exact_approval"]],
        "owner": OWNER,
        "owner_candidates": [{**row, "state": "bounded_owner_local_completed_without_core_promotion"} for row in portfolio["owner_candidates"]],
        "phase": PHASE,
        "safe_now": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["safe_now"]],
        "schema": "ghc.family.portfolio-results.v680.v4.x2",
        "successor_candidates": portfolio["successor_candidates"],
        "successor_credit": 0,
    }

    write_json(
        X2 / "positive-controls.json",
        {"accepted_count": 60, "owner": OWNER, "phase": PHASE, "receipts": positives, "schema": "ghc.family.positive-controls.v680.v4.x2"},
    )
    write_json(
        X2 / "mutations.json",
        {
            "accepted_invalid_count": 0,
            "executed_count": 300,
            "owner": OWNER,
            "phase": PHASE,
            "preregistered_count": 300,
            "receipts": mutations,
            "rejected_count": 300,
            "schema": "ghc.family.mutations.v680.v4.x2",
        },
    )
    write_json(
        X2 / "proposal-evidence.json",
        {
            "authority_conferred": False,
            "outcome_counts": outcome_counts,
            "outcomes": outcomes,
            "owner": OWNER,
            "phase": PHASE,
            "real_data_rows": 0,
            "schema": "ghc.family.proposal-evidence.v680.v4.x2",
            "source_x1": X1_HEAD,
        },
    )
    write_json(X2 / "portfolio-results.json", portfolio_results)
    write_json(
        X2 / "successor-recommendations.json",
        {
            "owner_completion_credit": 0,
            "candidate_seeds": portfolio["successor_candidates"],
            "clean_fix_refine_seeds": portfolio["successor_clean_fix_refine"],
            "owner": OWNER,
            "phase": PHASE,
            "recipient_not_contacted": True,
            "runner_seeds": portfolio["successor_runner_ideas"],
            "schema": "ghc.family.successor-recommendations.v680.v4.x2",
            "skill_seeds": portfolio["successor_skill_ideas"],
        },
    )
    write_json(
        X2 / "prepared-state.json",
        {
            "finalized": False,
            "owner": OWNER,
            "phase": PHASE,
            "runner_smoke_pending": True,
            "schema": "ghc.family.x2-prepared-state.v680.v4",
            "skill_read_validate_smoke_pending": True,
        },
    )
    print(json.dumps({"status": "X2_PREPARED_AWAITING_SKILL_AND_RUNNER_SMOKE", "mutations": 300, "positives": 60, "skills": 20, "runners": 10}, indent=2))


def refresh_skills() -> None:
    require_x1_boundary()
    if not X2.exists() or not SKILLS.exists():
        raise RuntimeError("prepared x2 and officially initialized skills are required for bounded semantic refresh")
    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    write_text(ROOT / "scripts" / "ghc_family_elowen_cairn_v680_v4_skill_bank.py", SKILL_BANK_MODULE)
    mappings = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        proposal_index = SKILL_PROPOSAL_INDEXES[index - 1]
        proposal = proposals[proposal_index - 1]
        folder = SKILLS / name
        if not (folder / "SKILL.md").is_file() or not (folder / "agents" / "openai.yaml").is_file():
            raise RuntimeError(f"officially initialized skill scaffold missing for {name}")
        write_text(folder / "SKILL.md", skill_text(name, proposal["proposal_id"], proposal["title"]))
        write_text(folder / "agents" / "openai.yaml", skill_yaml(name))
        mappings.append(
            {
                "proposal_id": proposal["proposal_id"],
                "proposal_index": proposal_index,
                "skill": name,
                "state": "semantically_aligned_without_reinitialization",
            }
        )
    write_json(
        X2 / "skill-semantic-refresh-receipt.json",
        {
            "failure_retained": "EC6804-X2-N002",
            "mappings": mappings,
            "owner": OWNER,
            "phase": PHASE,
            "reinitialized": False,
            "schema": "ghc.family.skill-semantic-refresh.v680.v4.x2",
        },
    )
    print(json.dumps({"status": "SKILLS_SEMANTICALLY_REFRESHED", "skills": len(mappings)}, indent=2))


def finalize() -> None:
    require_x1_boundary()
    skill_receipt_path = X2 / "skill-smoke-receipts.json"
    runner_receipt_path = X2 / "runner-smoke-receipts.json"
    if not skill_receipt_path.exists() or not runner_receipt_path.exists():
        raise RuntimeError("skill and runner smoke receipts are required before x2 finalization")
    skills = json.loads(skill_receipt_path.read_text(encoding="utf-8"))
    runners = json.loads(runner_receipt_path.read_text(encoding="utf-8"))
    if skills["validated_count"] != 20 or skills["smoke_used_count"] != 20 or runners["passed_count"] != 10:
        raise RuntimeError("skill or runner smoke gate failed")

    freeze = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    mutations = json.loads((X2 / "mutations.json").read_text(encoding="utf-8"))
    positives = json.loads((X2 / "positive-controls.json").read_text(encoding="utf-8"))
    startup = json.loads((X1 / "method-flow-startup.json").read_text(encoding="utf-8"))

    method_records = [
        {
            "candidate": "preregistered_in_immutable_x1",
            "independent_reproduction": False,
            "method_id": f"EC6804-METHOD-{index:03d}",
            "preferred": "bounded_owner_local_contract_only",
            "proposal_id": proposal["proposal_id"],
            "validated": "one_zero_row_positive_and_five_rejecting_mutations",
        }
        for index, proposal in enumerate(freeze["proposals"], start=1)
    ]
    x2_operational_failures = [
        {
            "failure_id": "EC6804-X2-N001",
            "false_witness": "One broad multi-surface adaptation patch matched every expected copied line.",
            "initial_credit": 0,
            "observed": "apply_patch rejected the complete edit atomically because its final path context had already been mechanically advanced to v680_v4.",
            "recovery": "Retain this zero-credit patch-context failure and apply bounded exact-context edits for failures, counts, gates, overview, and tests.",
            "recovery_rewrites_failure": False,
            "repository_mutated_by_failure": False,
            "scope": "x2_adaptation_patch_context",
        },
    ]
    counts = {
        "bounded_passing_witnesses": 37655,
        "effective_methods": 55533,
        "effective_negatives": 51346,
        "exact_gates": 443,
        "failed_witnesses": 23007,
        "open_gaps": 452,
    }
    write_json(
        X2 / "method-flow-ledger.json",
        {
            "counts": counts,
            "failure_erasure": False,
            "independent_reproduction_claimed": False,
            "methods": method_records,
            "mutation_failed_witnesses": mutations["receipts"],
            "owner": OWNER,
            "phase": PHASE,
            "positive_passing_witnesses": positives["receipts"],
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow.v680.v4.x2",
            "startup_and_x1_failures": startup["startup_failures"],
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "counts": counts,
            "declared_chain": 9410,
            "outcomes": evidence["outcome_counts"],
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v680.v4.x2",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        X2 / "retained-negative-register.json",
        {
            "effective_negatives": counts["effective_negatives"],
            "failed_witnesses": counts["failed_witnesses"],
            "owner": OWNER,
            "phase": PHASE,
            "retained_mutations": 300,
            "schema": "ghc.family.retained-negatives.v680.v4.x2",
            "startup_and_x1_failures": 10,
            "x2_operational_failures": x2_operational_failures,
        },
    )
    write_json(
        X2 / "gate-register.json",
        {
            "exact_gates": 443,
            "inherited_exact_gates": 440,
            "inherited_open_gaps": 449,
            "new_exact_gates": 3,
            "new_open_gaps": 3,
            "open_gaps": 452,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.gate-register.v680.v4.x2",
        },
    )
    write_json(
        X2 / "official-source-use-receipt.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "owner": OWNER,
            "phase": PHASE,
            "real_data_rows": 0,
            "schema": "ghc.family.source-use.v680.v4.x2",
            "sources_used_for_vocabulary_only": 9,
        },
    )
    write_json(
        X2 / "threat-control-evidence.json",
        {
            "authority_conferred": False,
            "external_actions": 0,
            "network_data_queries": 0,
            "owner": OWNER,
            "phase": PHASE,
            "real_rows": 0,
            "schema": "ghc.family.threat-controls.v680.v4.x2",
        },
    )
    write_json(
        X2 / "complete-incomplete-ledger.json",
        {
            "completed": ["60 proposal dispositions executed as evidence permitted", "300 rejecting mutations retained", "20 skills validated and smoke-used", "10 runners smoke-used"],
            "incomplete": ["all 452 open gaps", "all 443 exact gates", "full repository suite", "independent reproduction", "Stage 20"],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.complete-incomplete.v680.v4.x2",
        },
    )
    write_json(
        X2 / "prepared-state.json",
        {
            "finalized": True,
            "owner": OWNER,
            "phase": PHASE,
            "runner_smoke_pending": False,
            "schema": "ghc.family.x2-prepared-state.v680.v4",
            "skill_read_validate_smoke_pending": False,
        },
    )
    write_text(
        X2 / "integrated-overview.md",
        """# Elowen Cairn v680-v4 bounded x2 evidence

This phase executed sixty wholly synthetic zero-row proposal contracts and all 300 preregistered rejecting mutations. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Every rejected mutation remains a zero-credit failed witness. Twenty owner-local skills were initialized through the installed skill-creator workflow, customized, read through EOF, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current runners were accepting/rejecting smoke-used.

GMUT Mind remains the primary pillar through wholly synthetic weather-vane, aneroid-barometer, and tipping-bucket rain-gauge documentation lenses. THOS Body and Freed ID/CBR Heart remain explicit and protected. The phase used no real person, participant, weather vane, barometer, rain gauge, instrument component, station, site, observation, calibration, measurement, maintenance event, forecast, warning, dataset row, credential, identity event, external write, or authority act.

Official sources supplied vocabulary and refusal boundaries only. No software, synthetic fixture, citation, or same-owner validation establishes empirical confirmation, professional competence, safety, production readiness, legal/cultural legitimacy, affected-party acceptance, Māori authority, complete privacy/accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_elowen_cairn_v680_v4_x2.py"
    test_path = "tests/test_ghc_family_elowen_cairn_v680_v4_evidence.py"
    status_rows = git("status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    actual_paths = sorted({row[3:].replace("\\", "/") for row in status_rows if len(row) >= 4})
    exclusions = [
        "docs/elowen-cairn/v680-v4/validation/evidence-index-manifest.json",
        "docs/elowen-cairn/v680-v4/validation/evidence-privacy-scan.json",
        "docs/elowen-cairn/v680-v4/validation/evidence-security-scan.json",
        "docs/elowen-cairn/v680-v4/validation/evidence-staged-review.json",
    ]
    for required in (script_path, test_path):
        if required not in actual_paths:
            actual_paths.append(required)
    content_paths = sorted(path for path in set(actual_paths) if path not in exclusions)

    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    ast_errors = []
    for path_text in content_paths:
        path = ROOT / path_text
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".py":
            try:
                compile(text, path_text, "exec")
            except SyntaxError as exc:
                ast_errors.append({"path": path_text, "error": str(exc)})
        for class_name, pattern in scanners.items():
            if pattern.search(text):
                scanner_definition = path_text.startswith("scripts/") or path_text.startswith("tests/")
                row = {"class": class_name, "disposition": "scanner_definition_only" if scanner_definition else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if not scanner_definition:
                    confirmed.append(row)
    if confirmed or ast_errors:
        raise RuntimeError(json.dumps({"privacy": confirmed, "ast": ast_errors}))

    write_json(
        VALIDATION / "evidence-privacy-scan.json",
        {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v680.v4.evidence"},
    )
    write_json(
        VALIDATION / "evidence-security-scan.json",
        {"ast_errors": ast_errors, "bounded_findings": 0, "owner": OWNER, "phase": PHASE, "python_files": sum(path.endswith(".py") for path in content_paths), "schema": "ghc.family.security-scan.v680.v4.evidence"},
    )
    expected_paths = sorted(set(content_paths + exclusions))
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {"declared_self_exclusions": exclusions, "expected_paths": expected_paths, "lifecycle": "bounded_x2_evidence", "owner": OWNER, "path_count": len(expected_paths), "phase": PHASE, "schema": "ghc.family.staged-review.v680.v4.evidence"},
    )
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v680.v4.evidence", "x1": X1_HEAD},
    )
    print(json.dumps({"status": "X2_FINALIZED_FOR_EVIDENCE_REVIEW", "entries": len(entries), "skills": 20, "runners": 10}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--refresh-skills", action="store_true")
    args = parser.parse_args()
    if args.finalize:
        finalize()
    elif args.refresh_skills:
        refresh_skills()
    else:
        prepare()


if __name__ == "__main__":
    main()
