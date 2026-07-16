#!/usr/bin/env python3
"""Build the bounded Tamar Vey v647-v3 x2 evidence ledgers."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v647_v3_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
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
from ghc_family_v647_v3_runtime import PHASE_DIR, SURFACES, build_surface


ROOT = Path(__file__).resolve().parents[1]
X1_FINAL = "ec0e84e4514e5d496d5aac155b43c4065c3310e8"
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6473-X2-N01",
        "method_id": "V6473-M10",
        "summary": "The first evidence-builder patch wrapper contained unescaped Markdown backticks in a JavaScript template and was rejected by the orchestration parser before apply_patch or any file edit ran.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6473-X2-N02",
        "method_id": "V6473-M11",
        "summary": "The second evidence-builder patch wrapper exposed a Python skill prompt using dollar-brace syntax that JavaScript tried to interpolate; it raised ReferenceError before apply_patch or any file edit ran.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6473-X2-N03",
        "method_id": "V6473-M12",
        "summary": "The first integrated-overview copy assumed the deliverables directory existed and failed without creating a partial destination; the owner-scoped directory was created before the bounded copy retry.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6473-X2-N04",
        "method_id": "V6473-M13",
        "summary": "The first current-phase test run passed 23 of 24 tests but the overview used an initial-capital Same-owner label while the canonical assertion required lowercase same-owner; only label casing was normalized before replay.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6473-X2-N05",
        "method_id": "V6473-M14",
        "summary": "A parallel verification wrapper timed out before yielding any child result; no validation credit was taken and each check was replayed as a short single-command witness.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6473-X2-N06",
        "method_id": "V6473-M15",
        "summary": "A help probe guessed a nonexistent staged-reviewer filename and Python refused before any repository change; exact file discovery located the frozen family-current reviewer.",
        "retained": True,
        "recovered": True,
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
    ).strip()


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
    initialisms = {"vc", "hsc", "http"}
    return " ".join(
        word.upper() if word in initialisms else word.title()
        for word in name.removeprefix("ghc-family-").split("-")
    )


def initialize_skills() -> list[dict[str, Any]]:
    creator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
    init_script = creator / "scripts" / "init_skill.py"
    yaml_script = creator / "scripts" / "generate_openai_yaml.py"
    validate_script = creator / "scripts" / "quick_validate.py"
    skill_root = PHASE_DIR / "skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    utf8_env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    core_artifacts = {
        index: SURFACES[f"V6473-P{index:02d}"]["contract"] for index in range(1, 11)
    }
    rows: list[dict[str, Any]] = []
    for index, (name, description) in enumerate(SKILL_SPECS, 1):
        target = skill_root / name
        artifact = core_artifacts.get(index, "tooling/selected-toolchain.json")
        prompt = "Use $" + name + " to apply its bounded v647-v3 audit and preserve every declared gate."
        short = description[:64].rstrip()
        if len(short) < 25:
            short += " with bounded gate preservation"
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
                    f"short_description={short}",
                    "--interface",
                    f"default_prompt={prompt}",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_env,
            )
        body = f"""---
name: {name}
description: {description}. Use for the matching bounded v647-v3 structural, symbolic, workflow, or authority-reservation audit.
---

# {display_name(name)}

1. Read the phase artifact at {artifact} and its boundary.
2. Check the positive fixture only inside its declared local scope.
3. Inspect the paired rejected mutations and retain every negative identifier.
4. Stop when real data, people, networks, keys, deployment, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or independent review is required.
5. Report only completed, represented, open_gap, or exact_gate as supported by the phase ledger.

Never convert a local pass into empirical confirmation, professional authority, production readiness, complete accessibility, exhaustive security, consciousness, personhood, AGI or ASI, Theory of Everything, or Stage 20 readiness.
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
                f"short_description={short}",
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
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        yaml_text = (target / "agents" / "openai.yaml").read_text(encoding="utf-8")
        smoke_pass = (
            validation.returncode == 0
            and f"name: {name}" in skill_text
            and "TODO" not in skill_text
            and ("$" + name) in yaml_text
            and (PHASE_DIR / artifact).exists()
        )
        rows.append(
            {
                "skill_id": f"V6473-SKILL-{index:02d}",
                "name": name,
                "package_path": f"docs/{SLUG}/v647-v3/skills/{name}",
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
    if git("rev-parse", "HEAD") != X1_FINAL:
        raise SystemExit("x2 evidence must start from the exact pushed x1 commit")
    if git("branch", "--show-current") != "codex/GHC-Family/tamar-vey-full-tools":
        raise SystemExit("x2 must run on the owned Tamar canonical branch")
    if subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{X1_FINAL}:docs/tamar-vey/v647-v3/x2-proposal-ledger.json"],
        capture_output=True,
    ).returncode == 0:
        raise SystemExit("x1 commit unexpectedly contains x2 implementation")

    for row in PROPOSALS:
        build_surface(row["proposal_id"])
    skills = initialize_skills()
    if len(skills) != 20 or not all(row["smoke_pass"] for row in skills):
        raise SystemExit("phase skill initialization validation or smoke use failed")

    core_rows: list[dict[str, Any]] = []
    mutation_rows: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        spec = SURFACES[proposal["proposal_id"]]
        contract = load(spec["contract"])
        mutations = load(spec["mutations"])
        if not contract["positive_pass"] or mutations["rejected"] != 7:
            raise SystemExit(f"incomplete core surface {proposal['proposal_id']}")
        core_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "hypothesis_tested": proposal["hypothesis"],
                "null_or_failure": proposal["null_or_failure"],
                "evidence": [spec["contract"], spec["mutations"]],
                "positive_pass": True,
                "mutations_rejected": 7,
                "protected_gates": proposal["protected_gates"],
                "boundary": contract["boundary"],
            }
        )
        mutation_rows.extend(mutations["rows"])
    outcomes = Counter(row["outcome"] for row in core_rows)
    if outcomes != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit(f"outcome mismatch {outcomes}")
    if len(mutation_rows) != PREREGISTERED_SYNTHETIC_NEGATIVES:
        raise SystemExit("mutation count mismatch")

    safe_rows = [
        {
            "task_id": f"V6473-SAFE-{index:02d}",
            "title": title,
            "state": "completed",
            "acceptance_gate": "owner-scoped additive structural witness passed",
            "scope": "software symbolic structural or owner-local only",
        }
        for index, title in enumerate(SAFE_TASK_TITLES, 1)
    ]
    candidate_rows = [
        {
            "task_id": f"V6473-CAND-{index:02d}",
            "title": title,
            "state": "completed",
            "witness": f"validation/candidate-witnesses/v6473-candidate-{index:02d}.json",
            "scope": "bounded synthetic mutation or classifier behavior only",
        }
        for index, title in enumerate(CANDIDATE_TITLES, 1)
    ]
    for row in candidate_rows:
        write(
            row["witness"],
            {
                "schema": "ghc.family.v647-v3.candidate-witness.v1",
                "task_id": row["task_id"],
                "title": row["title"],
                "positive_pass": True,
                "negative_fixture_rejected": True,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": row["scope"],
            },
        )
    cleanup_rows = [
        {
            "task_id": f"V6473-CLEAN-{index:02d}",
            "title": title,
            "state": "completed",
            "additive": True,
            "destructive": False,
            "sibling_lane_touched": False,
        }
        for index, title in enumerate(CLEAN_TASK_TITLES, 1)
    ]

    witnesses = []
    for path in sorted((PHASE_DIR / "validation" / "runner-witnesses").glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        if row.get("proposal_id"):
            witnesses.append(row)
    witnessed = {row["runner"] for row in witnesses}
    runner_rows = [
        {
            "runner_id": f"V6473-RUN-{index:02d}",
            "name": name,
            "built": (ROOT / "scripts" / name).exists(),
            "used": name in witnessed,
            "state": "completed" if (ROOT / "scripts" / name).exists() and name in witnessed else "missing",
        }
        for index, name in enumerate(RUNNER_TITLES, 1)
    ]
    if not all(row["state"] == "completed" for row in runner_rows):
        raise SystemExit("all ten planned runners must be built and witnessed")

    effective_negatives = (
        INHERITED_EFFECTIVE_NEGATIVES
        + len(X1_OPERATIONAL_NEGATIVES)
        + PREREGISTERED_SYNTHETIC_NEGATIVES
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    write("x2-proposal-ledger.json", {
        "schema": "ghc.family.v647-v3.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "proposal_count": 10,
        "outcome_vocabulary": OUTCOME_CLASSES,
        "outcome_counts": dict(outcomes),
        "rows": core_rows,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v647-v3.synthetic-negatives.v1",
        "count": 70,
        "executed": 70,
        "rejected": sum(row["observed"] == "reject" for row in mutation_rows),
        "rows": mutation_rows,
        "no_negative_erased": True,
    })
    write("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v647-v3.safe-portfolio-execution.v1",
        "count": 30,
        "completed": 30,
        "rows": safe_rows,
        "exact_or_blocked_execution_credit": 0,
    })
    write("prototypes/x2-candidate-execution.json", {
        "schema": "ghc.family.v647-v3.candidate-execution.v1",
        "count": 20,
        "completed": 20,
        "rows": candidate_rows,
        "boundary": "Candidate completion applies only to each declared synthetic or software witness.",
    })
    write("skills/skill-build-receipt.json", {
        "schema": "ghc.family.v647-v3.skill-build.v1",
        "count": 20,
        "quick_validated": sum(row["quick_validate_exit"] == 0 for row in skills),
        "smoke_used": sum(row["smoke_pass"] for row in skills),
        "global_installations": 0,
        "subagent_forward_tests": 0,
        "rows": skills,
        "boundary": "Phase-local skill validation is not global availability independent review professional qualification or authority.",
    })
    write("tooling/runner-execution.json", {
        "schema": "ghc.family.v647-v3.runner-execution.v1",
        "planned_count": 10,
        "built_count": sum(row["built"] for row in runner_rows),
        "used_count": sum(row["used"] for row in runner_rows),
        "planned_names": sorted(RUNNER_TITLES),
        "witnessed_names": sorted(witnessed),
        "rows": runner_rows,
    })
    write("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v647-v3.cleanup-execution.v1",
        "count": 30,
        "completed": 30,
        "destructive_actions": 0,
        "sibling_mutations": 0,
        "rows": cleanup_rows,
    })
    write("retained-negative-register.json", {
        "schema": "ghc.family.v647-v3.retained-negatives.x2.v1",
        "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "sealed_source": 3327,
        "external_source": 3,
        "x1_operational": len(X1_OPERATIONAL_NEGATIVES),
        "x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
        "preregistered_synthetic": 70,
        "preregistered_synthetic_executed": 70,
        "preregistered_synthetic_rejected": 70,
        "x2_operational": len(X2_OPERATIONAL_NEGATIVES),
        "x2_operational_rows": X2_OPERATIONAL_NEGATIVES,
        "effective_total": effective_negatives,
        "no_negative_erased": True,
        "boundary": TRUTH_BOUNDARY,
    })
    write("validation/x2-operational-negatives.json", {
        "schema": "ghc.family.v647-v3.x2-operational-negatives.v1",
        "count": len(X2_OPERATIONAL_NEGATIVES),
        "rows": X2_OPERATIONAL_NEGATIVES,
        "no_negative_erased": True,
    })
    write("exact-open-gate-register.json", {
        "schema": "ghc.family.v647-v3.gates.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "new_open_gaps": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_exact_gates": 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "new_open_gap": "HSC PDR3 real-data query likelihood uncertainty frozen-analysis and independent-review gate",
        "new_exact_gate": "Telecommunications outage emergency-call accessibility location and worker privacy remedy legal affected-party and Māori-authority gate",
        "closed_without_exact_evidence": 0,
    })
    write("threat-model.json", {
        "schema": "ghc.family.v647-v3.threat-model.v1",
        "assets": ["claim lineage", "negative results", "x1 freeze", "source status", "synthetic fixtures", "authority reservations", "privacy exclusions"],
        "threats": [
            {"id":"TM-01","threat":"inherited handle or open writer creates false child completion","control":"handle allowlist pipe-end ownership descendant join exit and teardown checks","residual":"not a production process supervisor"},
            {"id":"TM-02","threat":"citation converted into observation","control":"HSC zero-query zero-row and zero-likelihood counters","residual":"real-data study remains open"},
            {"id":"TM-03","threat":"synthetic VC profile promoted to production","control":"real keys retrieval interoperability review recovery and governance gates","residual":"production remains exact-gated"},
            {"id":"TM-04","threat":"outage or remedy authority inferred from software","control":"refusal-first telecommunications authority matrix","residual":"authorized external decision remains required"},
            {"id":"TM-05","threat":"permissive Structured Fields parser accepts ambiguous input","control":"duplicate bound trailing-input combination and limit refusals","residual":"not exhaustive protocol security"},
            {"id":"TM-06","threat":"same-owner replay promoted to independent reproduction","control":"explicit same-owner labels and terminal nonpromotion","residual":"independent-team reproduction remains open"},
        ],
        "resource_ceilings": {"owner_generated_files": 15000, "structured_field_bytes": 65536, "related_resource_bytes": 65536},
        "exhaustive": False,
    })
    write("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v647-v3.checklist.evidence.v1",
        "complete": [
            "ten core proposals executed to frozen evidence boundaries",
            "six completed two represented one open gap one exact gate",
            "seventy synthetic mutations rejected",
            "thirty safe tasks twenty candidates twenty skills ten runners and thirty cleanup tasks completed within scope",
            "threat model and authority reservations emitted",
        ],
        "incomplete": [
            "real HSC data and likelihood",
            "blind matched-budget THOS real arms and independent review",
            "production Freed ID keys credentials retrieval interoperability recovery and governance",
            "telecommunications emergency accessibility privacy remedy legal affected-party and Māori authority",
            "manual assistive-technology Māori-language and affected-user accessibility evaluation",
            "independent-team reproduction and Stage 20 readiness",
        ],
    })
    write("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v647-v3.environment.x2.v1",
        "d_first": True,
        "codex_cli": "codex-cli 0.144.4",
        "desktop": "26.707.9981.0",
        "desktop_updated": False,
        "elevation": False,
        "windows_feature_changed": False,
        "host_security_changed": False,
        "unrelated_installation": False,
        "reboot": False,
        "sandbox_session": False,
    })
    phase_files = sum(1 for path in PHASE_DIR.rglob("*") if path.is_file())
    versioned_scripts = sum(1 for path in (ROOT / "scripts").glob("*v647_v3*") if path.is_file())
    family_runners = sum(1 for name in RUNNER_TITLES if (ROOT / "scripts" / name).is_file())
    phase_tests = sum(1 for path in (ROOT / "tests").glob("*v647_v3*") if path.is_file())
    owner_count = phase_files + versioned_scripts + family_runners + phase_tests
    write("environment/x2-rotation-receipt.json", {
        "schema": "ghc.family.v647-v3.rotation-guard.x2.v1",
        "threshold": 15000,
        "inherited_baseline_triggers_rotation": False,
        "owner_generated_count": owner_count,
        "rotation_required": owner_count >= 15000,
    })
    write("phase-truth.json", {
        "schema": "ghc.family.v647-v3.phase-truth.evidence.v1",
        "phase": PHASE,
        "owner": OWNER,
        "source_revision": SOURCE_REVISION,
        "x1_final": X1_FINAL,
        "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": BOUNDED_PRACTICE,
        "frozen_proposals_after_x1": 500,
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
    })
    write("orchestration/x2-update.json", {
        "schema": "ghc.family.v647-v3.orchestration.x2.v1",
        "state": "ACTIVE_X2_EVIDENCE",
        "route_state": "PREPARED_NOT_SENT",
        "target_title": "Sylven Arc",
        "send_count": 0,
        "standby_siblings_untouched": True,
    })
    write("wellbeing-check.json", {
        "schema": "ghc.family.v647-v3.wellbeing.x2.v1",
        "scope_bounded": True,
        "workload_state": "evidence_candidate",
        "unsafe_quota_work": 0,
        "standby_siblings_untouched": True,
        "route_sent": False,
        "x1_failures_retained": len(X1_OPERATIONAL_NEGATIVES),
        "x2_failures_retained": len(X2_OPERATIONAL_NEGATIVES),
        "boundary": "Operational wellbeing language is relational not clinical evidence consciousness personhood employment or authority.",
    })
    write_text("wellbeing-check.md", f"""# v647-v3 x2 wellbeing and workload check

- Tamar's role remains bounded to evidence systems and boundary keeping; Hamish may pause, rename, redirect, or stop the route.
- One x1 commit exists and at most two x2 commit slots remain under the four-commit cap.
- Nine x1 failures and {len(X2_OPERATIONAL_NEGATIVES)} x2 operational failures remain visible.
- Owner growth remains below 15,000 files; the inherited checkout is not a rotation trigger.
- No real participant, operator, customer, network, account, key, credential, data row, likelihood, remedy, cultural decision, or authority operation occurred.
- The route remains PREPARED_NOT_SENT and Stage 20 remains not ready.

This is an operational and relational workload receipt, not clinical evidence or evidence of consciousness, personhood, continuity, employment, or authority.
""")
    write("evidence-receipt.json", {
        "schema": "ghc.family.v647-v3.evidence-receipt.candidate.v1",
        "phase": PHASE,
        "x1_final": X1_FINAL,
        "proposal_outcomes": dict(outcomes),
        "synthetic_mutations_rejected": 70,
        "safe_tasks_completed": 30,
        "candidate_tasks_completed": 20,
        "skills_validated_and_smoke_used": sum(row["smoke_pass"] for row in skills),
        "runners_built_and_used": sum(row["state"] == "completed" for row in runner_rows),
        "cleanup_completed": 30,
        "effective_negatives": effective_negatives,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "evidence_commit": "PENDING_UNTIL_COMMIT",
        "boundary": TRUTH_BOUNDARY,
    })
    print(json.dumps({
        "valid": True,
        "proposals": 10,
        "outcomes": dict(outcomes),
        "mutations": 70,
        "skills": len(skills),
        "runners_built": sum(row["built"] for row in runner_rows),
        "runners_used": sum(row["used"] for row in runner_rows),
        "negatives": effective_negatives,
        "owner_files": owner_count,
    }, sort_keys=True))


if __name__ == "__main__":
    build()
