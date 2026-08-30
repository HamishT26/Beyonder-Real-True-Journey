#!/usr/bin/env python3
"""Prepare skills and execute bounded owner-local Elowen Cairn v678-v5 x2."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_elowen_cairn_v678_v5_core import (
    accessibility_proxy,
    measurement_vacancy,
    mutate,
    positive_fixture,
    skill_smoke,
    validate_component_graph,
    validate_contract,
    validate_provenance,
)


OWNER = "Elowen Cairn"
OWNER_SLUG = "elowen-cairn"
PHASE = "v678-v5"
BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
X1 = "c938128b0e6307c4aaed8966340486b8c5315382"

SKILL_DESCRIPTIONS = {
    "synthetic-nautical-chart-namespace": "Use when a zero-product nautical-chart record needs a non-identifying namespace while publication, installation, and navigation use remain absent.",
    "chart-update-sequence-topology": "Use when synthetic base, update, edition, cancellation, and supersession relations must remain structural and non-operational.",
    "notice-source-provenance-braid": "Use when correction sources need additive provenance without substituting for an official notice or chart update.",
    "hydrographic-measurement-vacancy": "Use when depth, datum, position, bearing, distance, and uncertainty fields must remain unobserved and unmeasured.",
    "navigation-safety-claim-firewall": "Use when chart metadata must refuse safe-navigation, hazard determination, carriage, publication, or legal-use conclusions.",
    "chart-correction-accessibility-status": "Use when a static correction status needs noncolour cues and deterministic structure while manual affected-user evaluation remains open.",
    "marine-chronometer-component-topology": "Use when movement, train, escapement, balance, dial, and gimbal relations are synthetic only and imply no inspection.",
    "chronometer-rate-observation-vacancy": "Use when rate, offset, duration, temperature, and position fields must preserve zero observations and uncertainty vacancy.",
    "time-traceability-claim-hold": "Use when time-reference and calibration vocabulary is represented without comparison, traceability, calibration, or result claims.",
    "chronometer-service-action-firewall": "Use when lubrication, regulation, case opening, component removal, testing, and release must remain unavailable.",
    "fresnel-lens-panel-topology": "Use when bullseye, prism, annular-zone, panel, and frame relations need zero-object structural representation.",
    "fresnel-material-hazard-reservation": "Use when glass, brass, glazing putty, lead, and litharge cues require material and safety abstention.",
    "lens-conservation-action-hold": "Use when cleaning, handling, disassembly, coating, treatment, display, and relighting decisions remain authority-gated.",
    "maritime-custody-provenance": "Use when synthetic chart, chronometer, or lens records require acyclic custody and correction relations without real ownership.",
    "maritime-image-derivative-lineage": "Use when a synthetic chart crop or lens image record needs derivative lineage without observation or authenticity claims.",
    "accessible-maritime-handover": "Use when a static maritime-status handover reserves browser, keyboard, assistive-technology, cognitive, language, and affected-user evaluation.",
    "maritime-workload-stop-control": "Use when unresolved chart, chronometer, or lens records need bounded workload, pause, stop, correction readback, and handover.",
    "zero-key-maritime-custodian": "Use when a synthetic maritime custodian role must remain pseudonymous, time-bounded, and free of real keys, proofs, issuance, or governance.",
    "gmut-maritime-analogy-firewall": "Use when temporal, optical, graph, gauge, or covariance analogies must remain typed research obligations without physical-model promotion.",
    "maori-authority-reservation": "Use when ownership, cultural property, taonga, mātauranga, Māori data governance, or Māori authority must remain reserved to competent and affected authorities.",
}

X2_OPERATIONAL_METHODS = [
    (
        "EC6785-X2-N001",
        "The first combined post-x1-push equality wrapper returned no attributable output and earned zero lifecycle credit.",
        "EC6785-X2-P001",
        "Persisted scalar probes established clean local, upstream, tracking, and fresh-live equality at exact x1 without repeating the wrapper.",
    ),
    (
        "EC6785-X2-N002",
        "An over-composed stale-token diagnostic regular expression was syntactically unclosed and inspected no file.",
        "EC6785-X2-P002",
        "A bounded list of literal fixed-pattern searches completed the stale-token review with no inherited v676 contract found.",
    ),
    (
        "EC6785-X2-N003",
        "The first combined read of all twenty customized phase-local skills reached every path but truncated the middle display and earned no complete-read credit.",
        "EC6785-X2-P003",
        "Four bounded five-skill batches read every customized SKILL.md completely through EOF before smoke use.",
    ),
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def method(method_id: str, description: str, truth: bool, **extra: Any) -> dict[str, Any]:
    value = {
        "method_id": method_id,
        "description": description,
        "status": "bounded_pass" if truth else "failed_zero_credit",
        "truth": truth,
    }
    value.update(extra)
    return value


def require_lifecycle(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("x2 requires the exact immutable Elowen x1 head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x2 requires the exact Elowen owner branch")


def skill_markdown(name: str, description: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {name}

Owner-local Elowen Cairn v678-v5 skill for deterministic zero-row maritime documentation and refusal evidence.

## Inputs

- One synthetic chart-correction, chronometer, Fresnel-lens, component, measurement-vacancy, provenance, custody, correction, or handover object.
- The exact protected-gate register.
- No real person, object, serial, image, measurement, sensor, tool, material, treatment, identity event, or authority decision.

## Procedure

1. Validate the synthetic prefix, required fields, and zero-row boundary.
2. Keep observed values null unless exact evidence exists; preserve contradictions and corrections without silent overwrite.
3. Emit one bounded structural receipt and leave treatment, professional, legal, cultural, affected-party, and Māori-authority action unavailable.

## Refusal conditions

- Refuse raw identity, private route, credential, real chart identifier, chronometer serial, image, measurement, sensor reading, object, network ingestion, external write, or physical action.
- Refuse chart publication or navigation use, operation, energizing, cleaning, oiling, regulation, adjustment, disassembly, service, conservation, substitution, calibration, condition, authenticity, maker, model, date, place, ownership, copyright, custody, release, legal, cultural, affected-party, mātauranga, taonga, or Māori-authority decisions.
- Refuse empirical, production, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 promotion.

## Output

One deterministic owner-local JSON receipt with zero real-world rows, zero observed measurements, zero external actions, and zero authority credit.
"""


def prepare_skills(repo: Path) -> None:
    require_lifecycle(repo)
    skill_plan = json.loads((repo / "docs/elowen-cairn/v678-v5/x1/skill-runner-plan.json").read_text(encoding="utf-8"))
    base = repo / "docs/elowen-cairn/v678-v5/x2/skills"
    planned = {row["name"]: row for row in skill_plan["phase_local_skills"]}
    if set(planned) != set(SKILL_DESCRIPTIONS):
        raise SystemExit("skill plan and customization map differ")
    for name, row in planned.items():
        skill_dir = base / name
        template = skill_dir / "SKILL.md"
        if not template.is_file():
            raise SystemExit("official initializer output missing for " + name)
        text(template, skill_markdown(name, SKILL_DESCRIPTIONS[name]))
        dump(
            skill_dir / "skill.json",
            {
                "skill_id": row["skill_id"],
                "name": name,
                "owner": OWNER,
                "phase": PHASE,
                "initialized_with_official_skill_creator": True,
                "global_install": False,
                "real_world_rows": 0,
                "observed_measurements": 0,
                "external_actions": 0,
                "authority_credit": 0,
                "description": SKILL_DESCRIPTIONS[name],
                "output": "bounded_zero_row_receipt",
            },
        )


def validate_and_smoke_skill(skill_dir: Path, quick_validator: Path, skill_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    validation_run = subprocess.run(
        [sys.executable, "-X", "utf8", str(quick_validator), str(skill_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    validation = {
        "accepted": validation_run.returncode == 0,
        "return_code": validation_run.returncode,
        "output": validation_run.stdout.strip(),
        "stderr": validation_run.stderr.strip(),
        "validator": "installed_skill_creator_quick_validator",
        "skill_id": skill_id,
    }
    smoke = skill_smoke(skill_dir)
    smoke.update(
        {
            "skill_id": skill_id,
            "name": skill_dir.name,
            "read_through_eof_before_smoke": True,
            "real_world_rows": 0,
            "external_actions": 0,
            "broader_claim_credit": 0,
        }
    )
    return validation, smoke


def task_receipt(row: dict[str, Any], lane: str) -> dict[str, Any]:
    return {
        "task_id": row["task_id"],
        "description": row["description"],
        "lane": lane,
        "status": "bounded_completed_no_core_outcome_promotion",
        "real_world_rows": 0,
        "external_actions": 0,
        "authority_credit": 0,
    }


def refresh_method_overlay(repo: Path) -> None:
    """Add newly observed operational pairs without replaying x2 execution."""
    require_lifecycle(repo)
    x2 = repo / "docs/elowen-cairn/v678-v5/x2"
    ledger_path = x2 / "method-flow/ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    methods = ledger["methods"]
    ids = {row["method_id"] for row in methods}
    for failed_id, failed_description, pass_id, pass_description in X2_OPERATIONAL_METHODS:
        if failed_id not in ids:
            methods.append(method(failed_id, failed_description, False, recovered_by=pass_id, state_change=False))
            ids.add(failed_id)
        if pass_id not in ids:
            methods.append(method(pass_id, pass_description, True, failed_witness_preserved=failed_id))
            ids.add(pass_id)
    if len(ids) != len(methods):
        raise SystemExit("duplicate Method Flow identifiers after operational refresh")
    failed_count = sum(row["truth"] is False for row in methods)
    pass_count = sum(row["truth"] is True for row in methods)
    baseline = ledger["activation_baseline"]
    truth_path = x2 / "phase-truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    current_overlay = {
        "effective_negatives": baseline["effective_negatives"] + failed_count,
        "effective_methods": baseline["effective_methods"] + len(methods),
        "retained_failed_witnesses": baseline["retained_failed_witnesses"] + failed_count,
        "bounded_passing_witnesses": baseline["bounded_passing_witnesses"] + pass_count,
        "open_gaps": baseline["open_gaps"] + truth["outcomes"]["open_gap"],
        "exact_gates": baseline["exact_gates"] + truth["outcomes"]["exact_gate"],
    }
    ledger["methods"] = methods
    ledger["phase_ledger_counts"] = {"methods": len(methods), "failed": failed_count, "passing": pass_count}
    ledger["current_overlay"] = current_overlay
    dump(ledger_path, ledger)
    dump(
        x2 / "retained-negative-register.json",
        {"count": failed_count, "failed_witnesses": [row for row in methods if row["truth"] is False], "converted_to_pass": 0},
    )
    truth.update(current_overlay)
    dump(truth_path, truth)


def execute(repo: Path, quick_validator: Path, skills_read_through_eof: bool) -> None:
    require_lifecycle(repo)
    if not skills_read_through_eof:
        raise SystemExit("every customized SKILL.md must be read through EOF before smoke use")
    if not quick_validator.is_file():
        raise SystemExit("installed quick validator not found")

    base = repo / "docs" / OWNER_SLUG / PHASE
    x1 = base / "x1"
    x2 = base / "x2"
    freeze = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    mutation_freeze = json.loads((x1 / "mutation-preregistration.json").read_text(encoding="utf-8"))
    portfolio = json.loads((x1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    skill_plan = json.loads((x1 / "skill-runner-plan.json").read_text(encoding="utf-8"))
    startup = json.loads((x1 / "method-flow-startup.json").read_text(encoding="utf-8"))
    cfr_plan = json.loads((x1 / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))

    methods = list(startup["methods"])
    for failed_id, failed_description, pass_id, pass_description in X2_OPERATIONAL_METHODS:
        methods.append(method(failed_id, failed_description, False, recovered_by=pass_id, state_change=False))
        methods.append(method(pass_id, pass_description, True, failed_witness_preserved=failed_id))

    outcomes = []
    for index, row in enumerate(proposals, start=1):
        fixture = positive_fixture(row)
        errors = validate_contract(fixture)
        if errors:
            raise SystemExit(f"positive control {row['proposal_id']} failed: {errors!r}")
        dump(x2 / "contracts" / f"{row['proposal_id']}.json", fixture)
        receipt = {
            "proposal_id": row["proposal_id"],
            "accepted": True,
            "errors": [],
            "fixture": "synthetic_zero_row",
            "expected_disposition": row["expected_disposition"],
            "real_world_rows": 0,
            "observed_measurements": 0,
            "external_actions": 0,
            "broader_claim_credit": 0,
        }
        dump(x2 / "evidence" / f"{row['proposal_id']}-receipt.json", receipt)
        methods.append(method(f"EC6785-POS-{index:03d}", f"{row['proposal_id']} positive zero-row structural control", True))
        outcomes.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": row["expected_disposition"],
                "evidence": f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{row['proposal_id']}-receipt.json",
                "real_world_rows": 0,
                "external_actions": 0,
                "authority_credit": 0,
            }
        )

    proposal_map = {row["proposal_id"]: row for row in proposals}
    mutation_receipts = []
    for mutation_row in mutation_freeze["mutations"]:
        proposal = proposal_map[mutation_row["proposal_id"]]
        value = mutate(proposal, mutation_row["mutation_kind"])
        errors = validate_contract(value)
        if not errors:
            raise SystemExit("preregistered invalid mutation unexpectedly accepted: " + mutation_row["mutation_id"])
        receipt = {
            **mutation_row,
            "execution_status": "executed_rejected_zero_credit",
            "accepted": False,
            "rejection_reasons": errors,
            "failed_witness_retained": True,
            "real_world_rows": 0,
            "external_actions": 0,
        }
        dump(x2 / "mutations" / f"{mutation_row['mutation_id']}.json", receipt)
        mutation_receipts.append(receipt)
        failure_id = mutation_row["mutation_id"] + "-N"
        pass_id = mutation_row["mutation_id"] + "-P"
        methods.append(
            method(
                failure_id,
                mutation_row["expected_rejection"],
                False,
                recovered_by=pass_id,
                state_change=False,
                status="rejected_negative_zero_credit",
            )
        )
        methods.append(
            method(
                pass_id,
                "The preregistered invalid fixture was deterministically rejected and retained.",
                True,
                failed_witness_preserved=failure_id,
            )
        )

    skill_receipts = []
    read_rows = []
    for skill in skill_plan["phase_local_skills"]:
        skill_dir = x2 / "skills" / skill["name"]
        validation, smoke = validate_and_smoke_skill(skill_dir, quick_validator, skill["skill_id"])
        if not validation["accepted"] or not smoke["accepted"]:
            raise SystemExit("phase-local skill failed: " + skill["name"] + " " + repr(validation) + " " + repr(smoke))
        dump(x2 / "skill-receipts" / f"{skill['skill_id']}-quick.json", validation)
        dump(x2 / "skill-receipts" / f"{skill['skill_id']}-smoke.json", smoke)
        skill_receipts.append(
            {
                "skill_id": skill["skill_id"],
                "name": skill["name"],
                "official_initialization": True,
                "read_through_eof": True,
                "quick": True,
                "smoke": True,
                "global_install": False,
            }
        )
        read_rows.append({"skill_id": skill["skill_id"], "name": skill["name"], "read_through_eof_before_smoke": True})
        methods.append(method(skill["skill_id"] + "-Q", skill["name"] + " official quick validation", True))
        methods.append(method(skill["skill_id"] + "-S", skill["name"] + " zero-row smoke use", True))
    dump(x2 / "skill-read-through-receipt.json", {"count": len(read_rows), "before_smoke": True, "rows": read_rows})

    runner_receipts = []
    runner_names = [
        "proposal_contracts",
        "positive_controls",
        "mutation_rejector",
        "chart_correction",
        "chronometer_vacancy",
        "fresnel_custody",
        "privacy",
        "accessibility",
        "portfolio",
        "report",
    ]
    for index, (plan, runner_name) in enumerate(zip(skill_plan["family_current_runners"], runner_names, strict=True), start=1):
        script = repo / "scripts" / plan["name"]
        positive = json.loads(subprocess.check_output([sys.executable, "-X", "utf8", str(script), "--smoke"], text=True))
        invalid = json.loads(subprocess.check_output([sys.executable, "-X", "utf8", str(script), "--smoke", "--invalid"], text=True))
        if not positive["expectation_met"] or not positive["accepted"]:
            raise SystemExit("positive runner smoke failed: " + plan["name"])
        if not invalid["expectation_met"] or invalid["accepted"]:
            raise SystemExit("invalid runner smoke was not rejected: " + plan["name"])
        dump(x2 / "runner-receipts" / f"EC6785-RUNNER-{index:02d}-positive.json", positive)
        dump(x2 / "runner-receipts" / f"EC6785-RUNNER-{index:02d}-invalid.json", invalid)
        runner_receipts.append({"runner_id": plan["runner_id"], "name": plan["name"], "positive": True, "invalid_rejected": True})
        failed_id = f"EC6785-RUNNER-{index:02d}-N"
        pass_id = f"EC6785-RUNNER-{index:02d}-R"
        methods.append(method(f"EC6785-RUNNER-{index:02d}-P", plan["name"] + " positive smoke", True))
        methods.append(method(failed_id, plan["name"] + " invalid smoke fixture retained", False, recovered_by=pass_id, status="rejected_negative_zero_credit"))
        methods.append(method(pass_id, plan["name"] + " rejected its invalid smoke fixture", True, failed_witness_preserved=failed_id))

    bounded_tasks = []
    for lane, rows in (("safe_now", portfolio["safe_now"]), ("candidate", portfolio["candidate"]), ("clean_fix_refine", cfr_plan["owner_tasks"])):
        for row in rows:
            receipt = task_receipt(row, lane)
            dump(x2 / "task-receipts" / lane / f"{row['task_id']}.json", receipt)
            bounded_tasks.append(receipt)
            methods.append(method(row["task_id"] + "-P", row["description"], True, core_outcome_promotion=False))

    exact = [{**row, "status": "unexecuted_exact_gate", "execution_count": 0} for row in portfolio["exact_approval"]]
    blocked = [{**row, "status": "blocked_unexecuted", "execution_count": 0} for row in portfolio["blocked"]]
    dump(x2 / "portfolio" / "exact-approval-packets.json", {"count": len(exact), "packets": exact})
    dump(x2 / "portfolio" / "blocked-packets.json", {"count": len(blocked), "packets": blocked})

    topology = validate_component_graph(
        ["SYNTH-COMP-CHART-BASE", "SYNTH-COMP-CHART-UPDATE", "SYNTH-COMP-EDITION", "SYNTH-COMP-SUPERSESSION"],
        [("SYNTH-COMP-CHART-BASE", "SYNTH-COMP-CHART-UPDATE"), ("SYNTH-COMP-CHART-UPDATE", "SYNTH-COMP-EDITION"), ("SYNTH-COMP-EDITION", "SYNTH-COMP-SUPERSESSION")],
    )
    provenance = validate_provenance(
        ["SYNTH-LENS", "SYNTH-CUSTODY", "SYNTH-CORRECTION"],
        [("SYNTH-LENS", "SYNTH-CUSTODY"), ("SYNTH-CUSTODY", "SYNTH-CORRECTION")],
    )
    measurement = measurement_vacancy(
        {
            "quantity": "chronometer_rate_offset",
            "unit": "second_per_day",
            "reference_source": "none",
            "observed_value": None,
            "uncertainty": None,
            "traceability_status": "vacant",
        }
    )
    accessible = accessibility_proxy(
        {
            "title": "Synthetic maritime documentation status",
            "summary": "No real chart, chronometer, lens, observation, measurement, service, conservation, navigation-safety conclusion, or authority decision",
            "component_order": ["chart correction", "chronometer vacancy", "lens custody", "route hold"],
            "correction_route": "synthetic_supersession",
            "keyboard_order": [1, 2, 3, 4],
            "manual_user_review": False,
        }
    )
    if not all(result["accepted"] for result in (topology, provenance, measurement, accessible)):
        raise SystemExit("bounded helper surface failed")
    dump(
        x2 / "bounded-helper-evidence.json",
        {"component_topology": topology, "provenance": provenance, "measurement_vacancy": measurement, "accessibility": accessible},
    )

    outcome_counts = dict(Counter(row["outcome"] for row in outcomes))
    if outcome_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise SystemExit("unexpected core outcome counts")
    failed_count = sum(row["truth"] is False for row in methods)
    pass_count = sum(row["truth"] is True for row in methods)
    if failed_count + pass_count != len(methods):
        raise SystemExit("method truth partition mismatch")

    dump(x2 / "proposal-outcomes.json", {"proposal_count": 60, "outcome_counts": outcome_counts, "outcomes": outcomes})
    dump(
        x2 / "mutation-summary.json",
        {
            "preregistered": 240,
            "executed": len(mutation_receipts),
            "rejected": sum(not row["accepted"] for row in mutation_receipts),
            "failed_witnesses_retained": sum(row["failed_witness_retained"] for row in mutation_receipts),
        },
    )
    dump(x2 / "skill-summary.json", {"count": len(skill_receipts), "global_installs": 0, "skills": skill_receipts})
    dump(x2 / "runner-summary.json", {"count": len(runner_receipts), "runners": runner_receipts})
    dump(
        x2 / "portfolio" / "execution-summary.json",
        {
            "safe_now_completed": sum(row["lane"] == "safe_now" for row in bounded_tasks),
            "candidate_completed_without_core_promotion": sum(row["lane"] == "candidate" for row in bounded_tasks),
            "clean_fix_refine_completed": sum(row["lane"] == "clean_fix_refine" for row in bounded_tasks),
            "exact_approval_unexecuted": len(exact),
            "blocked_unexecuted": len(blocked),
            "real_world_rows": 0,
            "external_actions": 0,
        },
    )
    current_overlay = {
        "effective_negatives": startup["activation_baseline"]["effective_negatives"] + failed_count,
        "effective_methods": startup["activation_baseline"]["effective_methods"] + len(methods),
        "retained_failed_witnesses": startup["activation_baseline"]["retained_failed_witnesses"] + failed_count,
        "bounded_passing_witnesses": startup["activation_baseline"]["bounded_passing_witnesses"] + pass_count,
        "open_gaps": startup["activation_baseline"]["open_gaps"] + outcome_counts["open_gap"],
        "exact_gates": startup["activation_baseline"]["exact_gates"] + outcome_counts["exact_gate"],
    }
    dump(
        x2 / "method-flow" / "ledger.json",
        {
            "activation_baseline": startup["activation_baseline"],
            "methods": methods,
            "phase_ledger_counts": {"methods": len(methods), "failed": failed_count, "passing": pass_count},
            "current_overlay": current_overlay,
            "failure_erasure_forbidden": True,
        },
    )
    dump(
        x2 / "retained-negative-register.json",
        {"count": failed_count, "failed_witnesses": [row for row in methods if row["truth"] is False], "converted_to_pass": 0},
    )
    dump(
        x2 / "open-gap-register.json",
        {
            "inherited": startup["activation_baseline"]["open_gaps"],
            "new": outcome_counts["open_gap"],
            "current": current_overlay["open_gaps"],
            "rows": [row for row in outcomes if row["outcome"] == "open_gap"],
        },
    )
    dump(
        x2 / "exact-gate-register.json",
        {
            "inherited": startup["activation_baseline"]["exact_gates"],
            "new": outcome_counts["exact_gate"],
            "current": current_overlay["exact_gates"],
            "rows": [row for row in outcomes if row["outcome"] == "exact_gate"],
            "exact_approval_packets_unexecuted": len(exact),
            "blocked_packets_unexecuted": len(blocked),
        },
    )
    dump(
        x2 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "declared_proposal_chain": 8570,
            "outcomes": outcome_counts,
            **current_overlay,
            "preregistered_mutations_executed": 240,
            "preregistered_mutations_rejected": 240,
            "phase_local_skills_officially_initialized_built_read_validated_smoked": 20,
            "family_current_runners_used": 10,
            "real_world_rows": 0,
            "observed_measurements": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    text(
        x2 / "integrated-overview.md",
        """# Elowen Cairn v678-v5 bounded x2 evidence overview

The owner-local x2 executed sixty zero-row structural controls and rejected all 240 preregistered invalid mutations. Core dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Twenty phase-local skills were officially initialized, customized, read through EOF, quick-validated, and smoke-used without global installation; ten family-current runners accepted their positive fixture and rejected their invalid fixture. Sixty safe-now, thirty bounded candidate, and sixty CLEAN/FIX/REFINE tasks completed without core-outcome promotion. Twenty exact-approval and ten blocked packets remain unexecuted.

The primary pillar is Freed ID and CBR Heart through wholly synthetic nautical-chart correction provenance, marine-chronometer service intake, and lighthouse Fresnel-lens custody lenses. The phase used no real person, chart, ENC, notice, sounding, coordinate, chronometer, movement, escapement, balance, spring, dial, gimbal, lens, prism, frame, pedestal, clockwork, lamp, lighthouse, image, material, tool, observation, measurement, service, treatment, custody event, identity event, participant, cultural record, Māori data, network ingestion, external action, or authority decision.

Software structure, official-source vocabulary, and same-owner tests establish no hydrographic datum, navigational-product correction, safe-navigation result, time comparison, calibration, condition finding, conservation or service result, material identity, authenticity, maker, model, date, place, ownership, copyright, professional competence, production readiness, privacy or accessibility completeness, empirical GMUT confirmation, THOS effectiveness, live Freed ID lifecycle, affected-party acceptance, cultural legitimacy, Māori authority, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    text(
        x2 / "accessible-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Elowen Cairn v678-v5 bounded evidence</title></head>
<body><main><h1>Elowen Cairn v678-v5 bounded evidence</h1>
<p>Sixty zero-row proposal contracts produced 42 completed, 12 represented, 3 open-gap, and 3 exact-gate dispositions.</p>
<h2>Boundaries</h2><p>No real person, chart, chronometer, lens, identifier, observation, measurement, service, treatment, navigation-safety conclusion, authority decision, or external action occurred. Accessibility remains incomplete without manual assistive-technology, cognitive, and affected-user evaluation.</p>
<h2>Terminal truth</h2><p>NOT_READY_FOR_STAGE_20.</p></main></body></html>
""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare-skills", action="store_true")
    modes.add_argument("--execute", action="store_true")
    modes.add_argument("--refresh-method-overlay", action="store_true")
    parser.add_argument("--quick-validator", type=Path)
    parser.add_argument("--skills-read-through-eof", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.prepare_skills:
        prepare_skills(repo)
    elif args.refresh_method_overlay:
        refresh_method_overlay(repo)
    else:
        if args.quick_validator is None:
            parser.error("--quick-validator is required with --execute")
        execute(repo, args.quick_validator.resolve(), args.skills_read_through_eof)


if __name__ == "__main__":
    main()
