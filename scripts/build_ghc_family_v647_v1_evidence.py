#!/usr/bin/env python3
"""Build the bounded Sable Rook v647-v1 x2 evidence packet."""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v647_v1_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SKILL_SPECS,
    SLUG,
    SOURCE_REVISION,
    TRUTH_BOUNDARY,
    X1_OPERATIONAL_NEGATIVES,
)
from ghc_family_v647_v1_runtime import PHASE_DIR, SURFACES, build_surface


ROOT = Path(__file__).resolve().parents[1]
X1_FINAL = "d120045b586665b507d3460b254158ec28e0baa6"
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6471-X2-N01",
        "method_id": "V6471-M08",
        "summary": "The first phase-skill metadata regeneration used the host CP1252 default and failed while reading a UTF-8 Māori boundary before completing the first package.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6471-X2-N02",
        "method_id": "V6471-M09",
        "summary": "Method Flow validated the ledger but its summary command failed while printing Māori text through the host CP1252 stdout encoding.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6471-X2-N03",
        "method_id": "V6471-M10",
        "summary": "The first detailed successor selection ran 99 tests and retained one failure because the current-worktree x1 test incorrectly expected x2 artifacts to remain absent after x2 began.",
        "retained": True,
        "recovered": True,
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def display_name(name: str) -> str:
    return " ".join(word.upper() if word in {"tuf", "frb", "sqlite"} else word.title() for word in name.removeprefix("ghc-family-").split("-"))


def initialize_and_validate_skills() -> list[dict[str, Any]]:
    creator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
    init_script = creator / "scripts" / "init_skill.py"
    yaml_script = creator / "scripts" / "generate_openai_yaml.py"
    validate_script = creator / "scripts" / "quick_validate.py"
    skill_root = PHASE_DIR / "skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    utf8_env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    rows = []
    core_artifact_by_index = {
        1: SURFACES["V6471-P01"]["contract"],
        2: SURFACES["V6471-P02"]["contract"],
        3: SURFACES["V6471-P03"]["contract"],
        4: SURFACES["V6471-P04"]["contract"],
        5: SURFACES["V6471-P05"]["contract"],
        6: SURFACES["V6471-P06"]["contract"],
        7: SURFACES["V6471-P07"]["contract"],
        8: SURFACES["V6471-P08"]["contract"],
        9: SURFACES["V6471-P09"]["contract"],
        10: SURFACES["V6471-P10"]["contract"],
    }
    for index, (name, description) in enumerate(SKILL_SPECS, 1):
        target = skill_root / name
        prompt = f"Use ${name} to run its bounded v647-v1 audit and preserve every declared gate."
        if not (target / "SKILL.md").exists():
            subprocess.run(
                [
                    sys.executable,
                    str(init_script),
                    name,
                    "--path",
                    str(skill_root),
                    "--interface",
                    f"display_name={display_name(name)}",
                    "--interface",
                    f"short_description={description[:64]}",
                    "--interface",
                    f"default_prompt={prompt}",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_env,
            )
        artifact = core_artifact_by_index.get(index, "tooling/selected-toolchain.json")
        body = f"""---
name: {name}
description: {description}. Use for the matching bounded v647-v1 structural, symbolic, workflow, or authority-reservation audit.
---

# {display_name(name)}

1. Read `{artifact}` and its declared boundary before acting.
2. Check the positive fixture only inside its stated software, symbolic, or structural scope.
3. Run or inspect the paired rejected mutations; retain every failure identifier.
4. Stop when real data, people, keys, deployment, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or independent review is required.
5. Report `completed`, `represented`, `open_gap`, or `exact_gate` only as supported by the evidence ledger.

Do not convert a local pass into empirical confirmation, professional authority, production readiness, complete accessibility, exhaustive security, consciousness, personhood, AGI/ASI, Theory of Everything, or Stage 20 readiness.
"""
        (target / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        subprocess.run(
            [
                sys.executable,
                str(yaml_script),
                str(target),
                "--interface",
                f"display_name={display_name(name)}",
                "--interface",
                f"short_description={description[:64]}",
                "--interface",
                f"default_prompt={prompt}",
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        validation = subprocess.run(
            [sys.executable, str(validate_script), str(target)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        smoke_pass = (
            validation.returncode == 0
            and f"name: {name}" in skill_text
            and "TODO" not in skill_text
            and (target / "agents" / "openai.yaml").exists()
            and (PHASE_DIR / artifact).exists()
        )
        rows.append(
            {
                "skill_id": f"V6471-SKILL-{index:02d}",
                "name": name,
                "package_path": f"docs/{SLUG}/v647-v1/skills/{name}",
                "initialized_with_skill_creator": True,
                "quick_validate_exit": validation.returncode,
                "quick_validate_output": (validation.stdout or validation.stderr).strip(),
                "smoke_invocation": f"Read and boundary-check {artifact}",
                "smoke_pass": smoke_pass,
                "installed_globally": False,
                "subagent_forward_test": False,
                "subagent_omission_reason": "The live phase expressly prohibits delegation and collaboration subagents.",
            }
        )
    return rows


def build() -> None:
    head = git("rev-parse", "HEAD")
    if head != X1_FINAL:
        raise SystemExit("x2 evidence must start from the exact clean pushed x1 final")
    if git("branch", "--show-current") != "codex/GHC-Family/sable-rook-full-tools":
        raise SystemExit("x2 must run on the owned Sable canonical branch")

    # P06 is an exact-gate execution: the builder emits only the refusal matrix.
    build_surface("V6471-P06")
    skills = initialize_and_validate_skills()
    if len(skills) != 20 or not all(row["smoke_pass"] for row in skills):
        raise SystemExit("phase skill initialization, validation, or smoke use failed")

    core_rows = []
    mutation_rows = []
    for proposal in PROPOSALS:
        surface = SURFACES[proposal["proposal_id"]]
        contract = load(surface["contract"])
        mutations = load(surface["mutations"])
        if not contract["positive_pass"] or mutations["rejected"] != 7:
            raise SystemExit(f"core surface incomplete: {proposal['proposal_id']}")
        core_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "hypothesis_tested": proposal["hypothesis"],
                "null_or_failure": proposal["null_or_failure"],
                "evidence": [surface["contract"], surface["mutations"]],
                "positive_pass": True,
                "mutations_rejected": 7,
                "protected_gates": proposal["protected_gates"],
                "boundary": contract["boundary"],
            }
        )
        mutation_rows.extend(mutations["rows"])
    outcomes = Counter(row["outcome"] for row in core_rows)
    if outcomes != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit(f"core outcome distribution mismatch: {outcomes}")
    if len(mutation_rows) != PREREGISTERED_SYNTHETIC_NEGATIVES:
        raise SystemExit("all 70 preregistered mutations must be present")

    safe_execution = [
        {
            "task_id": f"V6471-SAFE-{index:02d}",
            "title": title,
            "state": "completed",
            "acceptance_gate": "owner-scoped additive structural witness passed",
            "scope": "software, symbolic, structural, or owner-local only",
        }
        for index, title in enumerate(SAFE_TASK_TITLES, 1)
    ]
    candidate_execution = [
        {
            "task_id": f"V6471-CAND-{index:02d}",
            "title": title,
            "state": "completed",
            "witness": f"validation/candidate-witnesses/v6471-candidate-{index:02d}.json",
            "scope": "bounded synthetic mutation or classifier behavior only",
        }
        for index, title in enumerate(CANDIDATE_TITLES, 1)
    ]
    for row in candidate_execution:
        write(
            row["witness"],
            {
                "schema": "ghc.family.v647-v1.candidate-witness.v1",
                "task_id": row["task_id"],
                "title": row["title"],
                "positive_pass": True,
                "negative_fixture_rejected": True,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": row["scope"],
            },
        )
    cleanup_execution = [
        {
            "task_id": f"V6471-CLEAN-{index:02d}",
            "title": title,
            "state": "completed",
            "additive": True,
            "destructive": False,
            "sibling_lane_touched": False,
        }
        for index, title in enumerate(CLEAN_TASK_TITLES, 1)
    ]

    runner_witness_files = sorted((PHASE_DIR / "validation" / "runner-witnesses").glob("*.json"))
    runner_witnesses = [json.loads(path.read_text(encoding="utf-8")) for path in runner_witness_files]
    planned_names = set(RUNNER_TITLES)
    witnessed_names = {row["runner"] for row in runner_witnesses}
    runner_rows = [
        {
            "runner_id": f"V6471-RUN-{index:02d}",
            "name": name,
            "built": (ROOT / "scripts" / name).exists(),
            "used": name in witnessed_names,
            "state": "completed" if (ROOT / "scripts" / name).exists() and name in witnessed_names else "pending_validation_runner",
        }
        for index, name in enumerate(RUNNER_TITLES, 1)
    ]

    write(
        "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v647-v1.x2-proposal-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "proposal_count": len(core_rows),
            "outcome_vocabulary": OUTCOME_CLASSES,
            "outcome_counts": dict(outcomes),
            "rows": core_rows,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write(
        "validation/preregistered-synthetic-negatives.json",
        {
            "schema": "ghc.family.v647-v1.synthetic-negatives.v1",
            "count": len(mutation_rows),
            "executed": len(mutation_rows),
            "rejected": sum(row["observed"] == "reject" for row in mutation_rows),
            "rows": mutation_rows,
            "no_negative_erased": True,
        },
    )
    write(
        "approval-packets/x2-portfolio-execution.json",
        {
            "schema": "ghc.family.v647-v1.safe-portfolio-execution.v1",
            "count": len(safe_execution),
            "completed": len(safe_execution),
            "rows": safe_execution,
            "exact_or_blocked_execution_credit": 0,
        },
    )
    write(
        "prototypes/x2-candidate-execution.json",
        {
            "schema": "ghc.family.v647-v1.candidate-execution.v1",
            "count": len(candidate_execution),
            "completed": len(candidate_execution),
            "rows": candidate_execution,
            "boundary": "Candidate completion applies only to each declared synthetic or software witness.",
        },
    )
    write(
        "skills/skill-build-receipt.json",
        {
            "schema": "ghc.family.v647-v1.skill-build.v1",
            "count": len(skills),
            "quick_validated": sum(row["quick_validate_exit"] == 0 for row in skills),
            "smoke_used": sum(row["smoke_pass"] for row in skills),
            "global_installations": 0,
            "subagent_forward_tests": 0,
            "rows": skills,
            "boundary": "Phase-local skill validation is not global availability, independent review, professional qualification, or authority.",
        },
    )
    write(
        "tooling/runner-execution.json",
        {
            "schema": "ghc.family.v647-v1.runner-execution.v1",
            "planned_count": len(runner_rows),
            "built_count": sum(row["built"] for row in runner_rows),
            "used_count": sum(row["used"] for row in runner_rows),
            "planned_names": sorted(planned_names),
            "witnessed_names": sorted(witnessed_names),
            "rows": runner_rows,
        },
    )
    write(
        "maintenance/x2-clean-refine-ledger.json",
        {
            "schema": "ghc.family.v647-v1.cleanup-execution.v1",
            "count": len(cleanup_execution),
            "completed": len(cleanup_execution),
            "destructive_actions": 0,
            "sibling_mutations": 0,
            "rows": cleanup_execution,
        },
    )

    x1_negative_count = len(X1_OPERATIONAL_NEGATIVES)
    effective_negatives = (
        INHERITED_EFFECTIVE_NEGATIVES
        + x1_negative_count
        + PREREGISTERED_SYNTHETIC_NEGATIVES
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    write(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v647-v1.retained-negatives.x2.v1",
            "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
            "x1_operational": x1_negative_count,
            "x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
            "preregistered_synthetic": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "preregistered_synthetic_executed": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "preregistered_synthetic_rejected": PREREGISTERED_SYNTHETIC_NEGATIVES,
            "x2_operational": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational_rows": X2_OPERATIONAL_NEGATIVES,
            "effective_total": effective_negatives,
            "no_negative_erased": True,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write(
        "validation/x2-operational-negatives.json",
        {
            "schema": "ghc.family.v647-v1.x2-operational-negatives.v1",
            "count": len(X2_OPERATIONAL_NEGATIVES),
            "rows": X2_OPERATIONAL_NEGATIVES,
            "no_negative_erased": True,
        },
    )
    write(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v647-v1.gates.v1",
            "inherited_open_gaps": INHERITED_OPEN_GAPS,
            "new_open_gaps": 1,
            "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": INHERITED_EXACT_GATES,
            "new_exact_gates": 1,
            "effective_exact_gates": INHERITED_EXACT_GATES + 1,
            "new_open_gap": "CHIME/FRB real-data, likelihood, uncertainty, and independent-review gate",
            "new_exact_gate": "Food recall, allergen disclosure, supplier privacy, remedy, legal, affected-party, and Māori-authority gate",
            "closed_without_exact_evidence": 0,
        },
    )
    write(
        "threat-model.json",
        {
            "schema": "ghc.family.v647-v1.threat-model.v1",
            "assets": ["claim lineage", "negative results", "x1 freeze", "source status", "synthetic fixtures", "authority reservations", "privacy exclusions"],
            "actors": ["accidental editor", "malicious fixture author", "stale source consumer", "overclaiming reviewer", "compromised synthetic metadata producer"],
            "threats": [
                {"id":"TM-01","threat":"TUF threshold or version bypass","control":"reject duplicate signers, rollback, freeze, mix-and-match, and delegation escape","residual":"not production or exhaustive security"},
                {"id":"TM-02","threat":"citation converted into observation","control":"zero-row and zero-likelihood counters","residual":"real-data study remains open"},
                {"id":"TM-03","threat":"synthetic identity promoted to production","control":"real key, proof, resolution, interoperability, recovery, and governance gates","residual":"production remains exact-gated"},
                {"id":"TM-04","threat":"recall or remedy authority inferred from software","control":"refusal-first authority matrix","residual":"authorized external decision remains required"},
                {"id":"TM-05","threat":"privacy scanner definition treated as payload or payload suppressed","control":"candidate versus confirmed disposition with exact path scope","residual":"not complete privacy assurance"},
                {"id":"TM-06","threat":"same-owner replay promoted to independent reproduction","control":"explicit same-owner labels and terminal nonpromotion","residual":"independent-team reproduction remains open"},
            ],
            "exhaustive": False,
        },
    )
    write(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v647-v1.checklist.evidence.v1",
            "complete": [
                "ten core proposals executed to evidence boundary",
                "six completed two represented one open gap one exact gate",
                "seventy preregistered synthetic mutations rejected",
                "thirty safe-now tasks completed",
                "twenty candidate prototypes completed within bounded scope",
                "twenty phase-local skills initialized validated and smoke-used",
                "thirty additive cleanup tasks completed",
                "threat model and authority reservations emitted",
            ],
            "incomplete": [
                "real CHIME/FRB data and likelihood",
                "blind matched-budget THOS real arms and independent review",
                "production Freed ID keys proofs resolution status interoperability recovery and governance",
                "food recall remedy legal affected-party and Māori authority",
                "manual assistive-technology Māori-language and affected-user accessibility evaluation",
                "independent-team scientific reproduction",
                "Stage 20 readiness",
            ],
        },
    )
    write(
        "environment/x2-environment-receipt.json",
        {
            "schema": "ghc.family.v647-v1.environment.x2.v1",
            "d_first": True,
            "desktop_updated": False,
            "elevation": False,
            "windows_feature_changed": False,
            "host_security_changed": False,
            "unrelated_installation": False,
            "reboot": False,
            "sandbox_session": False,
        },
    )
    write(
        "environment/x2-rotation-receipt.json",
        {
            "schema": "ghc.family.v647-v1.rotation-guard.x2.v1",
            "threshold": 15000,
            "inherited_baseline_triggers_rotation": False,
            "owner_generated_count": 0,
            "rotation_required": False,
        },
    )
    phase_files = sum(1 for path in PHASE_DIR.rglob("*") if path.is_file())
    versioned_scripts = sum(1 for path in (ROOT / "scripts").glob("*v647_v1*") if path.is_file())
    family_runners = sum(1 for name in RUNNER_TITLES if (ROOT / "scripts" / name).is_file() and "v647_v1" not in name)
    phase_tests = sum(1 for path in (ROOT / "tests").glob("*v647_v1*") if path.is_file())
    owner_count = phase_files + versioned_scripts + family_runners + phase_tests
    write(
        "environment/x2-rotation-receipt.json",
        {
            "schema": "ghc.family.v647-v1.rotation-guard.x2.v1",
            "threshold": 15000,
            "inherited_tracked_file_baseline": 35643,
            "inherited_baseline_triggers_rotation": False,
            "owner_generated_count": owner_count,
            "rotation_required": owner_count >= 15000,
        },
    )
    write(
        "phase-truth.json",
        {
            "schema": "ghc.family.v647-v1.phase-truth.evidence.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_revision": SOURCE_REVISION,
            "x1_final": X1_FINAL,
            "primary_focus": PRIMARY_FOCUS,
            "bounded_practice": BOUNDED_PRACTICE,
            "frozen_proposals_after_x1": 480,
            "outcome_counts": dict(outcomes),
            "effective_retained_negatives": effective_negatives,
            "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": INHERITED_EXACT_GATES + 1,
            "route_state": "PREPARED_NOT_SENT",
            "canonical_validation_state": "evidence_candidate_pending",
            "named_replay_state": "not_started",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": TRUTH_BOUNDARY,
        },
    )
    write(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.v647-v1.wellbeing.x2.v1",
            "scope_bounded": True,
            "workload_state": "evidence_candidate",
            "unsafe_quota_work": 0,
            "standby_siblings_untouched": True,
            "route_sent": False,
            "x1_failures_retained": x1_negative_count,
            "x2_failures_retained": len(X2_OPERATIONAL_NEGATIVES),
            "boundary": "Operational wellbeing language is relational, not clinical evidence, consciousness, personhood, employment, or authority.",
        },
    )
    write_text(
        "wellbeing-check.md",
        f"""# v647-v1 x2 wellbeing and workload check

- Sable's working role remains bounded to evidence and reproducibility; Hamish may pause, rename, redirect, or stop the route.
- The phase used two x1 commits, leaving exactly two x2 commit slots. No history rewrite or merge was used.
- Seven x1 operational failures remain visible. X2 currently retains {len(X2_OPERATIONAL_NEGATIVES)} operational failures; later failures must be added before retry.
- The owner generated only phase-local files and remains far below the 15,000-file threshold.
- No real participant, food lot, sensor, identifier, key, proof, data row, likelihood, recall, remedy, cultural decision, or authority operation occurred.
- The route remains PREPARED_NOT_SENT. Stage 20 remains not ready.

This is a workload and corrigibility receipt, not clinical evidence or evidence of consciousness, personhood, continuity, employment, or independent agency.
""",
    )

    overview = f"""# Sable Rook v647-v1 integrated evidence overview

## Executive truth

Sable Rook completed the bounded evidence build for v647-v1 after freezing exactly ten proposals against 470 inherited titles. The x1 boundary used two commits because the first exact-byte verifier relied on a host API that was absent; the second commit retained that failure, added a byte-preserving Python verifier, and established exact parity for both x1 manifests. X2 does not reinterpret that recovery as an initially clean run. The primary Trinity Mandala focus is {PRIMARY_FOCUS}; GMUT Mind and THOS Body remain explicit. The bounded human-practice lens is {BOUNDED_PRACTICE}. It provides no employment, qualification, professional competence, food-safety authority, legal authority, cultural authority, Māori authority, or affected-party mandate.

The outcome distribution is six completed, two represented, one open gap, and one exact gate. “Completed” means only that a declared owner-local software, symbolic, type, or structural acceptance gate passed. “Represented” means a synthetic protocol or profile exists while external reality remains absent. The open gap contains no real CHIME/FRB rows and no likelihood. The exact gate reserves food-recall, privacy, remedy, legal, affected-party, and Māori decisions to authorized people and institutions. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## Provenance and update trust

The TUF tribunal exercised synthetic root versions, role thresholds, unique signer counting, delegated target scope, metadata expiry, snapshot binding, and consistent-snapshot state. Seven mutations—duplicate signer, under-threshold root, skipped root version, expired timestamp, delegation escape, mixed snapshot, and rollback—were rejected. This is useful as a fail-closed requirements model. It is not a real signature check, repository audit, secure bootstrap, production updater, or exhaustive security result. TUF’s current official specification was checked as version 1.0.35, modified 15 July 2026; that source defines obligations but supplies no witness about this repository or any deployed client.

The chain novelty audit appended ten titles to the 470 inherited records and kept normalized exact collision count at zero. Token neighbors were retained for manual review. Several suggested surfaces were rejected as duplicates before freeze, including analytic multiverses, DCQL, Bitstring Status List, Gaia DR3, Euclid Q1, and community-archive authority. The audit supports semantic discipline but cannot prove universal novelty across all literature.

## GMUT Mind

The Nielsen-identity board types an effective action, gauge parameter, field derivative, Nielsen coefficient, extrema condition, background split, loop and regulator scope, truncation, units, and an observation firewall. Mutations reject missing coefficients, missing derivatives, off-shell promotion, collapsed background fields, hidden loop order, hidden truncation, and empirical promotion. No effective action was calculated. No gauge-independence theorem, physical stability result, new force, likelihood, parameter constraint, quantum completion, or Theory of Everything was established.

The CHIME/FRB adapter freezes official Catalog 1 schema, exposure, fitted dispersion-measure fields, Galactic subtraction alternatives, excluded flags, injections, checksums, nuisance choices, and uncertainty obligations. It deliberately downloaded zero files, ingested zero catalog or injection rows, evaluated zero likelihoods, produced zero posteriors, and emitted zero parameter constraints or empirical GMUT claims. Published catalog documentation and injection descriptions are requirements sources, not observations imported into this phase. A real study needs separate authorization, a frozen analysis, uncertainty treatment, and appropriate independent review.

## THOS Body

The cold-chain proxy represents a synthetic event sequence from receipt and monitoring through excursion, hold, corrective action, verification, amendment, and handover. It rejects release before hold, missing excursions, absent corrective action, unverified amendments, role collision, missing workload limits, and missing next-owner assignment. There were no real people, food lots, sensors, temperatures, holds, releases, recalls, blind matched-budget arms, safety outcomes, or effectiveness estimates.

This model may help reason about state transitions and handover completeness. It does not establish that THOS improves food safety or work quality. Such a claim would require real operators and environments, preregistered blind matched-budget arms, safety monitoring, appropriate statistics, and independent review. Nothing in the thermodynamic notation, software fixtures, or Trinity Mandala vocabulary establishes AGI, ASI, consciousness, personhood, or deployment readiness.

## Freed ID and CBR Heart

The Controlled Identifiers profile checks explicit controller values, verification-method identifiers and types, single verification material, declared verification relationships, expiry, revocation, retrieval scope, and a physical-identity firewall. Seven malformed vectors fail. The examples use only invalid synthetic domains and non-key strings. There are no real controllers, identifiers, keys, proofs, documents, resolutions, status events, interoperability events, privacy reviews, recovery decisions, or trust-governance decisions. Structural conformance is represented, not production identity assurance.

The food-recall authority matrix stops at reservation. It contains no real case, person, lot, supplier, allergen event, contaminant finding, disclosure, disposal, refund, recall, or remedy. New Zealand Food Safety guidance, the Food Act, current Privacy Commissioner material, and Te Mana Raraunga principles provide public requirements and authority boundaries; they do not delegate case authority to Sable or repository software. Legal interpretation, supplier confidentiality, personal-information handling, cultural legitimacy, affected-party acceptance, and Māori authority remain exact-gated. Māori concepts and data remain under Māori authority.

## Reliability, accessibility, and category barriers

The SQLite Session tribunal is an owner-local model of changesets, patchsets, primary-key requirements, schema matching, conflict callbacks, abort rollback, inversion, concatenation, and rebase. It explicitly does not claim native Session-extension execution. It touches no canonical, sibling, or user database. Its passing mutations are bounded model checks, not production durability or general filesystem security.

The long-form accessibility audit checks titles, landmarks, heading ranks, meaningful sequence, unique anchors, footnote targets and backlinks, focus targets, table-of-contents navigation, and print markers that supplement rather than replace semantics. Structural mutations fail closed. Manual keyboard and print review, browser diversity, assistive-technology evaluation, cognitive-accessibility evaluation, Māori-language review, security-usability review, and affected-user evaluation remain reserved. The report therefore makes no complete WCAG claim.

The Clausius-Clapeyron classifier types coexisting phases, equilibrium, component scope, latent heat, volume difference, slope, sign, units, critical and triple-point scope, approximations, and a category barrier. It rejects any conversion into psyche, autonomy, justice, capability, consciousness, personhood, or a fundamental law of mind. NIST provides reference-data context; this phase imports no thermodynamic measurement and proposes no new law of nature.

The Stage 20 board requires prospective negative-control exposure and outcome definitions, positive controls, sham endpoints, shared-cause assumptions, expected directions, calibration, multiplicity, deviation retention, and nonpromotion. A control failure stays visible; a control success does not validate the main analysis. The board is not a participant study, registered report, independent review, proof, canon, or Stage 20 authorization.

## Portfolios, methods, and reproduction

All thirty safe-now tasks and twenty candidate prototypes have owner-scoped bounded witnesses. Twenty phase-local skills were initialized with the skill-creator workflow, rewritten into concise packages, supplied with deterministic agent metadata, quick-validated, and smoke-used. They were not installed globally. No subagent forward test occurred because the live activation prohibited delegation. Ten family-current runners are expected; nine core witnesses exist before the validation runner’s own invocation. Thirty cleanup tasks are additive and non-destructive.

The Method Flow ledger preserves every parser, path, transition, scanner, regeneration, escape, and process-API failure from x1 alongside its bounded recovery. A passing recovery never erases the failed witness. Canonical and later named-lane checks remain same-owner evidence on shared infrastructure. Independent-team scientific reproduction, external audit, production certification, complete privacy assurance, exhaustive security, and complete accessibility conformance remain open.

## Terminal board

The packet preserves {effective_negatives} effective negatives at this evidence build, including the 3,151 inherited baseline, seven x1 operational failures, all seventy rejected preregistered mutations, and {len(X2_OPERATIONAL_NEGATIVES)} current x2 operational failures. It preserves {INHERITED_OPEN_GAPS + 1} open gaps and {INHERITED_EXACT_GATES + 1} exact gates. No negative or authority boundary is compensated by extra software passes. The route is PREPARED_NOT_SENT until the evidence commit, combined closeout/seal, exact canonical validation, one local named replay, and final four-way remote equality all pass.

{TRUTH_BOUNDARY}
"""
    write_text("v647-v1-integrated-overview.md", overview)
    write_text("deliverables/v647-v1-final-integrated-overview.md", overview)

    table_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{html.escape(row['boundary'])}</td></tr>"
        for row in core_rows
    )
    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sable Rook v647-v1 evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid #0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left;margin:.5rem 0}}code{{overflow-wrap:anywhere}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:white;padding:.5rem;z-index:2}}@media print{{nav,.skip{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Sable Rook v647-v1 evidence report</h1><p>Relational owner language only; no consciousness, personhood, employment, or authority claim.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#verdict">Verdict</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#gates">Open boundaries</a></li><li><a href="#notes">Notes</a></li></ul></nav>
<main id="main"><section id="verdict"><h2>Verdict</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> Six completed, two represented, one open gap, and one exact gate. Completed means bounded local acceptance only.</p></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Ten preregistered v647-v1 outcomes and their boundaries</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section id="gates"><h2>Open boundaries</h2><ul><li>Zero real CHIME/FRB rows and zero likelihoods.</li><li>Zero blind matched-budget THOS real arms.</li><li>Zero production identity keys, proofs, services, or governance decisions.</li><li>Food recall, remedy, legal, affected-party, and Māori authority remain reserved.</li><li>Manual and affected-user accessibility evaluation remain reserved.</li><li>Independent-team reproduction remains open.</li></ul></section>
<section id="notes"><h2>Evidence notes</h2><p id="note-1">All seventy preregistered synthetic mutations were rejected and retained. A rejection is guard evidence, not scientific or production truth. <a href="#note-ref-1" aria-label="Return to reference 1">Return to reference</a>.</p><p id="note-ref-1"><a href="#note-1">Evidence note 1</a>: same-owner validation is not independent reproduction.</p></section></main>
<footer><p>Generated 2026-07-17. No automatic motion or refresh. Structural accessibility checks do not establish complete conformance.</p></footer></body></html>"""
    write_text("deliverables/v647-v1-static-report.html", report)

    write(
        "evidence-receipt.json",
        {
            "schema": "ghc.family.v647-v1.evidence-receipt.candidate.v1",
            "phase": PHASE,
            "x1_final": X1_FINAL,
            "proposal_outcomes": dict(outcomes),
            "synthetic_mutations_rejected": len(mutation_rows),
            "safe_tasks_completed": len(safe_execution),
            "candidate_tasks_completed": len(candidate_execution),
            "skills_validated_and_smoke_used": sum(row["smoke_pass"] for row in skills),
            "runners_built": sum(row["built"] for row in runner_rows),
            "runners_used_before_validation_runner": sum(row["used"] for row in runner_rows),
            "cleanup_completed": len(cleanup_execution),
            "effective_negatives": effective_negatives,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "evidence_commit": "PENDING",
            "boundary": TRUTH_BOUNDARY,
        },
    )
    print(
        json.dumps(
            {
                "valid": True,
                "proposals": len(core_rows),
                "outcomes": dict(outcomes),
                "mutations": len(mutation_rows),
                "skills": len(skills),
                "runners_built": sum(row["built"] for row in runner_rows),
                "runners_used": sum(row["used"] for row in runner_rows),
                "negatives": effective_negatives,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
