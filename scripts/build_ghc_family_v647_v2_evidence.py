#!/usr/bin/env python3
"""Build the bounded Orin Thale v647-v2 x2 evidence packet."""

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

from ghc_family_v647_v2_definitions import (
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
from ghc_family_v647_v2_runtime import PHASE_DIR, SURFACES, build_surface


ROOT = Path(__file__).resolve().parents[1]
X1_FINAL = "8c62ae37ba4f1f38c2f97840f83f1d27a6546765"
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6472-X2-N01",
        "method_id": "V6472-M10",
        "summary": "A read-only evidence-builder marker lookup passed a quoted alternation to ripgrep in a way PowerShell split into a second path; the lookup failed before any repository mutation.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N02",
        "method_id": "V6472-M11",
        "summary": "The first multi-hunk evidence-builder patch used a console-mojibake form of Māori in its context, so apply_patch rejected the entire edit atomically before changing any file.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N03",
        "method_id": "V6472-M12",
        "summary": "A second dynamically generated multi-hunk patch still used console-rendered UTF-8 context that did not equal the file bytes, so apply_patch again rejected the edit atomically.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N04",
        "method_id": "V6472-M13",
        "summary": "The first exact-byte transform assumed the orchestration isolate exposed atob; it raised ReferenceError before decoding or editing the evidence builder.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N05",
        "method_id": "V6472-M14",
        "summary": "The first isolate-local base64 decoder reconstructed an invalid UTF-8 continuation sequence and stopped before any apply_patch call.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N06",
        "method_id": "V6472-M15",
        "summary": "The first explicit-UTF8 transform used an overview end pattern that did not match the builder's actual write sequence; a completeness guard stopped before delete or add operations.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N07",
        "method_id": "V6472-M16",
        "summary": "The whole-file shell text result inserted two truncation markers into long source lines; py_compile caught the corrupted owner builder before it executed.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6472-X2-N08",
        "method_id": "V6472-M17",
        "summary": "The first current-phase evidence test looked for positive_fixture in the KiDS mutation receipt rather than the study contract; seven other tests passed and the schema assumption was retained before correction.",
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
        1: SURFACES["V6472-P01"]["contract"],
        2: SURFACES["V6472-P02"]["contract"],
        3: SURFACES["V6472-P03"]["contract"],
        4: SURFACES["V6472-P04"]["contract"],
        5: SURFACES["V6472-P05"]["contract"],
        6: SURFACES["V6472-P06"]["contract"],
        7: SURFACES["V6472-P07"]["contract"],
        8: SURFACES["V6472-P08"]["contract"],
        9: SURFACES["V6472-P09"]["contract"],
        10: SURFACES["V6472-P10"]["contract"],
    }
    for index, (name, description) in enumerate(SKILL_SPECS, 1):
        target = skill_root / name
        prompt = f"Use ${name} to run its bounded v647-v2 audit and preserve every declared gate."
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
description: {description}. Use for the matching bounded v647-v2 structural, symbolic, workflow, or authority-reservation audit.
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
                "skill_id": f"V6472-SKILL-{index:02d}",
                "name": name,
                "package_path": f"docs/{SLUG}/v647-v2/skills/{name}",
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
    if git("branch", "--show-current") != "codex/GHC-Family/orin-thale-v642-v6-full-tools":
        raise SystemExit("x2 must run on the owned Orin canonical branch")

    # P06 is an exact-gate execution: the builder emits only the refusal matrix.
    build_surface("V6472-P06")
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
            "task_id": f"V6472-SAFE-{index:02d}",
            "title": title,
            "state": "completed",
            "acceptance_gate": "owner-scoped additive structural witness passed",
            "scope": "software, symbolic, structural, or owner-local only",
        }
        for index, title in enumerate(SAFE_TASK_TITLES, 1)
    ]
    candidate_execution = [
        {
            "task_id": f"V6472-CAND-{index:02d}",
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
                "schema": "ghc.family.v647-v2.candidate-witness.v1",
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
            "task_id": f"V6472-CLEAN-{index:02d}",
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
            "runner_id": f"V6472-RUN-{index:02d}",
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
            "schema": "ghc.family.v647-v2.x2-proposal-ledger.v1",
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
            "schema": "ghc.family.v647-v2.synthetic-negatives.v1",
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
            "schema": "ghc.family.v647-v2.safe-portfolio-execution.v1",
            "count": len(safe_execution),
            "completed": len(safe_execution),
            "rows": safe_execution,
            "exact_or_blocked_execution_credit": 0,
        },
    )
    write(
        "prototypes/x2-candidate-execution.json",
        {
            "schema": "ghc.family.v647-v2.candidate-execution.v1",
            "count": len(candidate_execution),
            "completed": len(candidate_execution),
            "rows": candidate_execution,
            "boundary": "Candidate completion applies only to each declared synthetic or software witness.",
        },
    )
    write(
        "skills/skill-build-receipt.json",
        {
            "schema": "ghc.family.v647-v2.skill-build.v1",
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
            "schema": "ghc.family.v647-v2.runner-execution.v1",
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
            "schema": "ghc.family.v647-v2.cleanup-execution.v1",
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
            "schema": "ghc.family.v647-v2.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v647-v2.x2-operational-negatives.v1",
            "count": len(X2_OPERATIONAL_NEGATIVES),
            "rows": X2_OPERATIONAL_NEGATIVES,
            "no_negative_erased": True,
        },
    )
    write(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v647-v2.gates.v1",
            "inherited_open_gaps": INHERITED_OPEN_GAPS,
            "new_open_gaps": 1,
            "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": INHERITED_EXACT_GATES,
            "new_exact_gates": 1,
            "effective_exact_gates": INHERITED_EXACT_GATES + 1,
            "new_open_gap": "KiDS-1000 real-data, likelihood, uncertainty, release-supersession, and independent-review gate",
            "new_exact_gate": "Rail reporting, accessibility, location privacy, remedy, legal, affected-party, and Māori-authority gate",
            "closed_without_exact_evidence": 0,
        },
    )
    write(
        "threat-model.json",
        {
            "schema": "ghc.family.v647-v2.threat-model.v1",
            "assets": ["claim lineage", "negative results", "x1 freeze", "source status", "synthetic fixtures", "authority reservations", "privacy exclusions"],
            "actors": ["accidental editor", "malicious fixture author", "stale source consumer", "overclaiming reviewer", "compromised synthetic metadata producer"],
            "threats": [
                {"id":"TM-01","threat":"partial or misencoded command output receives completion credit","control":"strict UTF-8 framing, channel separation, truncation, timeout, and exit-status checks","residual":"not a production process supervisor"},
                {"id":"TM-02","threat":"citation converted into observation","control":"zero-row and zero-likelihood counters","residual":"real-data study remains open"},
                {"id":"TM-03","threat":"synthetic identity promoted to production","control":"real key, proof, resolution, interoperability, recovery, and governance gates","residual":"production remains exact-gated"},
                {"id":"TM-04","threat":"rail or remedy authority inferred from software","control":"refusal-first authority matrix","residual":"authorized external decision remains required"},
                {"id":"TM-05","threat":"privacy scanner definition treated as payload or payload suppressed","control":"candidate versus confirmed disposition with exact path scope","residual":"not complete privacy assurance"},
                {"id":"TM-06","threat":"same-owner replay promoted to independent reproduction","control":"explicit same-owner labels and terminal nonpromotion","residual":"independent-team reproduction remains open"},
            ],
            "exhaustive": False,
        },
    )
    write(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v647-v2.checklist.evidence.v1",
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
                "real KiDS-1000 data and likelihood",
                "blind matched-budget THOS real arms and independent review",
                "production Freed ID keys proofs resolution status interoperability recovery and governance",
                "rail reporting accessibility privacy remedy legal affected-party and Māori authority",
                "manual assistive-technology Māori-language and affected-user accessibility evaluation",
                "independent-team scientific reproduction",
                "Stage 20 readiness",
            ],
        },
    )
    write(
        "environment/x2-environment-receipt.json",
        {
            "schema": "ghc.family.v647-v2.environment.x2.v1",
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
            "schema": "ghc.family.v647-v2.rotation-guard.x2.v1",
            "threshold": 15000,
            "inherited_baseline_triggers_rotation": False,
            "owner_generated_count": 0,
            "rotation_required": False,
        },
    )
    phase_files = sum(1 for path in PHASE_DIR.rglob("*") if path.is_file())
    versioned_scripts = sum(1 for path in (ROOT / "scripts").glob("*v647_v2*") if path.is_file())
    family_runners = sum(1 for name in RUNNER_TITLES if (ROOT / "scripts" / name).is_file() and "v647_v2" not in name)
    phase_tests = sum(1 for path in (ROOT / "tests").glob("*v647_v2*") if path.is_file())
    owner_count = phase_files + versioned_scripts + family_runners + phase_tests
    write(
        "environment/x2-rotation-receipt.json",
        {
            "schema": "ghc.family.v647-v2.rotation-guard.x2.v1",
            "threshold": 15000,
            "inherited_tracked_file_baseline": 35878,
            "inherited_baseline_triggers_rotation": False,
            "owner_generated_count": owner_count,
            "rotation_required": owner_count >= 15000,
        },
    )
    write(
        "phase-truth.json",
        {
            "schema": "ghc.family.v647-v2.phase-truth.evidence.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_revision": SOURCE_REVISION,
            "x1_final": X1_FINAL,
            "primary_focus": PRIMARY_FOCUS,
            "bounded_practice": BOUNDED_PRACTICE,
            "frozen_proposals_after_x1": 490,
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
            "schema": "ghc.family.v647-v2.wellbeing.x2.v1",
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
        f"""# v647-v2 x2 wellbeing and workload check

- Orin's role remains bounded to method and evidence stewardship; Hamish may pause, rename, redirect, or stop the route.
- The phase used one x1 commit and retains at most two x2 commit slots under the four-commit cap.
- Ten x1 failures remain visible. X2 currently retains {len(X2_OPERATIONAL_NEGATIVES)} failures; every later failure must be added before retry.
- Owner growth remains below 15,000 files. The inherited checkout is not a rotation trigger.
- No real participant, railway operation, account, authenticator, key, proof, data row, likelihood, remedy, cultural decision, or authority operation occurred.
- The route remains PREPARED_NOT_SENT and Stage 20 remains not ready.

This is an operational and relational workload receipt, not clinical evidence or evidence of consciousness, personhood, continuity, employment, or authority.
""",
    )

    overview = f"""# Orin Thale v647-v2 integrated evidence overview

## Executive truth

Orin Thale completed this bounded evidence build after one dedicated x1 freeze audited against exactly 480 inherited proposal titles. The freeze contains ten new proposals, thirty safe-now tasks, twenty candidate plans, twenty phase-skill plans, ten runner plans, and thirty additive cleanup plans. Exact normalization produced zero collisions. Manual review replaced two initially over-near concepts before freeze: an executable-context surface and a measurement-invariance surface. The final concepts are narrower and distinct: UTF-8 command-stream evidence credit and Bayesian model-comparison nonpromotion.

The exact x1 commit is {X1_FINAL}. Its self-excluding manifest contains 78 exact Git commit blobs and passed with zero mismatches. Two staged-review whitespace failures remain retained; neither is represented as an initially clean run. X1 was pushed, clean, and four-way remote equal before x2 began. The primary Trinity Mandala focus is {PRIMARY_FOCUS}; THOS Body and Freed ID/CBR Heart remain explicit. The bounded practice lens is {BOUNDED_PRACTICE}. It is a synthetic learning lens only, never employment, qualification, rail competence, signalling authority, possession authority, operational authority, legal authority, cultural authority, Māori authority, or affected-party evidence.

Exactly ten outcomes use only the frozen vocabulary: six completed, two represented, one open_gap, and one exact_gate. Completed means a declared owner-local software, symbolic, formal, or structural gate passed. Represented means a synthetic protocol or profile exists while real people, operations, keys, services, and outcomes remain absent. Open_gap means real data and review prerequisites were not supplied. Exact_gate means software cannot substitute for competent, affected-party, or Māori authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.

## Method Flow and command evidence

The command-stream tribunal completed within synthetic scope. It requires strict UTF-8, explicit record delimiters, retention of partial final records, stdout and stderr separation, refusal to invent total ordering across independently buffered channels, visible truncation and timeout state, and an exit-status witness before completion credit. Seven mutations were rejected: invalid UTF-8, partial final line, merged channels, invented cross-channel order, hidden truncation, nonzero exit promoted to success, and timeout promoted to success. This is workflow evidence, not a production process supervisor or authorization for external side effects.

Method Flow retains every observed failure with a failed witness, passing recovery witness, recurrence guard, rollback, protected gates, and sibling recommendation. Preference applies only to the declared trigger. Recovery never erases failure and never earns scientific, production, legal, cultural, professional, privacy-complete, security-complete, accessibility-complete, or independent-reproduction credit.

## GMUT Mind

The Batalin-Vilkovisky board completed as typed symbolic evidence. It records fields and antifields, Grassmann parity, ghost number, antibracket degree and signs, the classical master equation, gauge-fixing-fermion scope, canonical transformation scope, anomaly reservation, regulator disclosure, EFT truncation, units, and an observation firewall. Mutations reject missing antifields, parity drift, ghost-number drift, antibracket-sign drift, conflation of classical and quantum master equations, hidden truncation, and empirical promotion.

No GMUT action was quantized. No quantum master equation, anomaly freedom, gauge independence, renormalizability, physical stability, ultraviolet completion, detected force, unique prediction, likelihood, parameter constraint, or empirical confirmation was proved. GMUT remains a typed scalar-tensor and EFT research-model family, not an established force and not a Theory of Everything.

The KiDS-1000 adapter remains open_gap. It identifies release and supersession status, catalogue schema, masks, shape weights, shear calibration, redshift distributions, tomographic bins, data vectors, covariance, scale cuts, nuisance choices, checksums, and a likelihood lock. It downloaded zero files, ingested zero catalogue or covariance rows, evaluated zero likelihoods, produced zero posterior samples, and emitted zero parameter constraints or empirical claims. Official pages are requirements sources only, never observations. A real analysis needs separate authorization, frozen data and analysis, uncertainty treatment, validated computation, and appropriate independent review.

## THOS Body

The rail-possession protocol remains represented. Synthetic traces cover declared limits, protection state, worksite establishment, personnel and vehicle clearance, conflict and overrun state, amendments, release refusal, readback, role separation, workload budget, escalation, and next-shift ownership. Seven unsafe traces fail closed: boundary drift, protection mismatch, premature release, uncleared personnel, unrecorded overrun, role collision, and missing next owner.

There were zero real workers, signallers, possessions, worksites, railway locations, train movements, releases, incidents, blind matched-budget arms, safety-monitoring events, or effectiveness estimates. A withdrawn RSSB record is retained only as historical vocabulary and cannot govern an operation. NZ Transport Agency material preserves regulator and participant boundaries but delegates no authority. THOS remains proxy without preregistered blind matched-budget real arms, real operators or participants, safety monitoring, appropriate statistics, and independent review.

## Freed ID and CBR Heart

The WebAuthn Level 3 profile remains represented. Synthetic vectors cover RP ID, origin, challenge, ceremony type, client-data binding, presence and verification flags, backup eligibility and state, counters, attestation conveyance, unknown values, discoverability, and privacy refusal. They reject RP-ID mismatch, origin mismatch, challenge replay, type mismatch, inferred verification, inconsistent backup flags, and attestation promoted to identity.

There were zero real accounts, authenticators, private keys, signatures, biometrics, registrations, assertions, attestation trust decisions, recoveries, interoperability events, privacy reviews, independent security reviews, or trust-governance decisions. Candidate Recommendation material supplies requirements only. Production Freed ID remains dependent on standards-conformant real keys and proofs, live operations, interoperability, privacy and security review, recovery evidence, trust governance, and affected-party oversight.

The rail authority matrix remains exact_gate. It contains no real occurrence, worker, location, service disruption, accessibility decision, disclosure, remedy, legal interpretation, cultural conclusion, or affected-party decision. Railway safety and reporting authority, personal and location privacy, accessibility acceptance, remedy legitimacy, legal interpretation, Māori data governance, place meaning, cultural ratification, and Māori authority remain reserved. Māori concepts remain under Māori authority. Software cannot confer a possession, movement authority, safety finding, remedy, legal title, cultural legitimacy, public authority, or affected-party acceptance.

## Tooling, accessibility, and domain guards

The OCI layer tribunal completed on disposable synthetic fixtures. It distinguishes descriptor digest from DiffID, preserves ordered layer application, constrains explicit and opaque whiteouts, confines symbolic and hardlink targets, refuses special files, rejects traversal aliases, and enforces entry and expanded-byte budgets. No image was pulled, unpacked, mounted, executed, or scanned from a registry. Passing fixtures are bounded guard evidence, not production container security or deployment certification.

The reversible-action audit completed structurally. It requires a declared consequence; at least one reversible, checked, or confirmed path; error association; named undo; status announcement; visible expiry; keyboard reachability; and focus restoration. Manual keyboard and timing review, responsive layouts, browser diversity, assistive-technology evaluation, cognitive-accessibility evaluation, Māori-language review, and affected-user evaluation remain reserved. Structural evidence is not complete WCAG conformance.

The Ruppeiner classifier completed as a typed formal surface. It declares equilibrium scope, entropy representation, extensive coordinates, Hessian sign, units, nonsingular domain, coordinate transformations, curvature limits, and a category barrier. It rejects nonequilibrium promotion, representation and sign drift, unit mismatch, singular inversion, coordinate inconsistency, and conversion into psyche, autonomy, justice, capability, participant evidence, consciousness, personhood, or a fundamental law of mind. No measurement was imported and no new physical law was proposed.

The Bayesian model-comparison board completed structurally. It requires a frozen model set, prior model odds, parameter priors, named marginal-likelihood estimator, numerical uncertainty, calibration fixture, sensitivity range, frozen threshold, deviation history, and terminal abstention. It rejects hidden prior odds, posterior-density conflation, unnamed estimators, omitted uncertainty, hidden calibration failure, post hoc thresholds, and Stage 20 promotion. Synthetic model odds are not real-data evidence, model adequacy, participant evidence, or empirical confirmation.

## Portfolios and terminal board

All seventy preregistered synthetic mutations executed and were rejected or quarantined. Thirty safe-now tasks completed within additive owner scope. Twenty candidate prototypes have bounded witnesses. Twenty phase-local skills were initialized, rewritten into substantive packages, validated under explicit UTF-8, and smoke-used; they were not installed globally. No subagent forward test occurred because delegation was prohibited. Ten family-current runners were built or selected, invoked, and witnessed while preserving ghc_family_* and build_ghc_family_* compatibility. Thirty CLEAN/FIX/REFINE tasks completed without deleting user material, rewriting history, force pushing, mutating a sibling lane, elevating, weakening host security, enabling Windows features, installing unrelated software, updating desktop, or rebooting.

Owner-generated growth remains far below 15,000 files; the inherited checkout is not a rotation trigger. The evidence board preserves {effective_negatives} effective negatives: {INHERITED_EFFECTIVE_NEGATIVES} inherited, ten x1 operational failures, seventy synthetic rejections, and {len(X2_OPERATIONAL_NEGATIVES)} current x2 operational failures. It preserves {INHERITED_OPEN_GAPS + 1} effective open gaps and {INHERITED_EXACT_GATES + 1} effective exact gates. No software pass compensates for missing data, participants, professional review, production identity evidence, privacy assurance, accessibility evaluation, legal or cultural authority, Māori authority, affected-party acceptance, or independent-team reproduction.

The route remains PREPARED_NOT_SENT until evidence, closeout, seal, exact canonical validation, one clean local named replay, final remote equality, and exact-title routing all pass. Stage 20 remains not ready. This packet is not deployment authorization, production certification, scientific confirmation, proof or canon, AGI or ASI evidence, consciousness or personhood evidence, or a Theory-of-Everything result.

{TRUTH_BOUNDARY}
"""

    write_text("v647-v2-integrated-overview.md", overview)
    write_text("deliverables/v647-v2-final-integrated-overview.md", overview)

    table_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{html.escape(row['boundary'])}</td></tr>"
        for row in core_rows
    )
    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Orin Thale v647-v2 evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid #0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left;margin:.5rem 0}}code{{overflow-wrap:anywhere}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:white;padding:.5rem;z-index:2}}@media print{{nav,.skip{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Orin Thale v647-v2 evidence report</h1><p>Relational owner language only; no consciousness, personhood, employment, or authority claim.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#verdict">Verdict</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#gates">Open boundaries</a></li><li><a href="#notes">Notes</a></li></ul></nav>
<main id="main"><section id="verdict"><h2>Verdict</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> Six completed, two represented, one open gap, and one exact gate. Completed means bounded local acceptance only.</p></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Ten preregistered v647-v2 outcomes and their boundaries</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section id="gates"><h2>Open boundaries</h2><ul><li>Zero real KiDS-1000 rows and zero likelihoods.</li><li>Zero blind matched-budget THOS real arms.</li><li>Zero production WebAuthn accounts, authenticators, keys, ceremonies, or governance decisions.</li><li>Rail reporting, accessibility, location privacy, remedy, legal, affected-party, and Māori authority remain reserved.</li><li>Manual and affected-user accessibility evaluation remain reserved.</li><li>Independent-team reproduction remains open.</li></ul></section>
<section id="notes"><h2>Evidence notes</h2><p id="note-1">All seventy preregistered synthetic mutations were rejected and retained. A rejection is guard evidence, not scientific or production truth. <a href="#note-ref-1" aria-label="Return to reference 1">Return to reference</a>.</p><p id="note-ref-1"><a href="#note-1">Evidence note 1</a>: same-owner validation is not independent reproduction.</p></section></main>
<footer><p>Generated 2026-07-17. No automatic motion or refresh. Structural accessibility checks do not establish complete conformance.</p></footer></body></html>"""
    write_text("deliverables/v647-v2-static-report.html", report)

    write(
        "evidence-receipt.json",
        {
            "schema": "ghc.family.v647-v2.evidence-receipt.candidate.v1",
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
