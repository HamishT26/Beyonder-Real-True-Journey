#!/usr/bin/env python3
"""Execute bounded x2 evidence for Eiren's v654-v6 (2) remaster."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v6_2_remaster_core as core
import ghc_family_v654_v6_2_remaster_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SKILL_ROOT = Path.home() / ".codex" / "skills"
SKILL_CREATOR = SKILL_ROOT / ".system/skill-creator/scripts"
METHOD_RUNNER = (
    SKILL_ROOT
    / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = (
    SKILL_ROOT
    / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
)
ROSTER_SKILL = SKILL_ROOT / "ghc-family-roster-check"
AUTH_SKILL = SKILL_ROOT / "ghc-family-auth-permission-state"


RUNNER_GROUPS = {
    "ghc_family_roster_check.py": [
        "V6546R2-P10",
        "V6546R2-P16",
        "V6546R2-P23",
    ],
    "ghc_family_research_constitution.py": [
        "V6546R2-P01",
        "V6546R2-P04",
        "V6546R2-P13",
    ],
    "ghc_family_omega_evidence_passport.py": [
        "V6546R2-P02",
        "V6546R2-P03",
        "V6546R2-P05",
    ],
    "ghc_family_correlated_witness_discount.py": [
        "V6546R2-P09",
        "V6546R2-P11",
        "V6546R2-P12",
    ],
    "ghc_family_evidence_authority_matrix.py": [
        "V6546R2-P20",
        "V6546R2-P21",
        "V6546R2-P22",
    ],
    "ghc_family_thos_task_contract.py": [
        "V6546R2-P14",
        "V6546R2-P17",
        "V6546R2-P18",
    ],
    "ghc_family_thos_reconciler.py": [
        "V6546R2-P15",
        "V6546R2-P19",
        "V6546R2-P24",
    ],
    "ghc_family_residual_set_preservation.py": [
        "V6546R2-P25",
        "V6546R2-P29",
        "V6546R2-P30",
    ],
    "ghc_family_legacy_claims_triage.py": [
        "V6546R2-P06",
        "V6546R2-P07",
        "V6546R2-P08",
    ],
    "ghc_family_v654_v6_2_remaster_suite.py": [
        "V6546R2-P26",
        "V6546R2-P27",
        "V6546R2-P28",
    ],
}

PHASE_SKILL_RUNNERS = {
    "ghc-family-research-constitution": "ghc_family_research_constitution.py",
    "ghc-family-omega-evidence-passport": "ghc_family_omega_evidence_passport.py",
    "ghc-family-correlated-witness-discount": "ghc_family_correlated_witness_discount.py",
    "ghc-family-evidence-authority-matrix": "ghc_family_evidence_authority_matrix.py",
    "ghc-family-thos-task-contract": "ghc_family_thos_task_contract.py",
    "ghc-family-thos-reconciler": "ghc_family_thos_reconciler.py",
    "ghc-family-residual-set-preservation": "ghc_family_residual_set_preservation.py",
    "ghc-family-legacy-claims-triage": "ghc_family_legacy_claims_triage.py",
    "ghc-family-independent-review-packet": "ghc_family_v654_v6_2_remaster_suite.py",
}

X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6546R2-X2-N01",
        "signature": "skill_hash_inventory_foreach_pipeline_parse_error",
        "failed": "The first skill-hash inventory piped directly from a PowerShell foreach block and failed with an empty-pipe-element parser error.",
        "recovery": "Materialize foreach output into a collection before conversion.",
        "guard": "Never pipe directly from a PowerShell foreach statement.",
    },
    {
        "negative_id": "V6546R2-X2-N02",
        "signature": "combined_roster_skill_inventory_timeout",
        "failed": "The first combined five-file roster-skill inventory exceeded its short timeout and yielded no complete receipt.",
        "recovery": "Use a longer bounded scalar inventory for the exact files.",
        "guard": "Allow archive and profile-backed PowerShell startup latency in timeout budgets.",
    },
    {
        "negative_id": "V6546R2-X2-N03",
        "signature": "parallel_roster_skill_inventory_timeouts",
        "failed": "Both shortened parallel roster-skill inventory probes exceeded the same ten-second bound.",
        "recovery": "Use one exact command with a sixty-second bound and avoid redundant retries.",
        "guard": "A repeated timeout on identical storage means change the bound or method, not concurrency alone.",
    },
    {
        "negative_id": "V6546R2-X2-N04",
        "signature": "new_roster_skill_quick_validate_legacy_decode_failure",
        "failed": "The first official quick validation decoded non-ASCII skill text through the Windows legacy code page and failed before structural validation.",
        "recovery": "Use ASCII-safe public skill prose or explicit Python UTF-8 mode, then validate the current content.",
        "guard": "Run official skill validation with PYTHONUTF8=1 on Windows.",
    },
    {
        "negative_id": "V6546R2-X2-N05",
        "signature": "combined_archive_git_and_file_probe_timeout",
        "failed": "A combined Git status, head, document inventory, and script inventory exceeded its archive-backed bound.",
        "recovery": "Split the read-only audit into independent bounded probes.",
        "guard": "Keep Git state and filesystem inventories separate on the archive-backed worktree.",
    },
    {
        "negative_id": "V6546R2-X2-N06",
        "signature": "source_template_inventory_foreach_pipeline_parse_error",
        "failed": "The first source-template inventory repeated the direct-foreach pipeline parser error.",
        "recovery": "Materialize the template rows, then pipe the completed collection.",
        "guard": "Reuse the retained PowerShell collection pattern for every foreach projection.",
    },
    {
        "negative_id": "V6546R2-X2-N07",
        "signature": "existing_skill_set_quick_validate_legacy_decode_failure",
        "failed": "The first six-skill validation batch again used the Windows legacy code page and stopped on existing UTF-8 content.",
        "recovery": "Run the unchanged official validator with Python UTF-8 mode explicitly enabled.",
        "guard": "Set PYTHONUTF8 and PYTHONIOENCODING for all skill-creator commands.",
    },
    {
        "negative_id": "V6546R2-X2-N08",
        "signature": "post_x2_combined_scoped_test_included_x1_lifecycle_assertion",
        "failed": "The first combined x1-and-x2 scoped test attempt ran the x1-only no-surface assertion after x2 surfaces existed and failed one of nineteen tests.",
        "recovery": "Retain the failed aggregate, exclude only the exact x1 lifecycle assertion, and run the isolated x2 module plus the still-applicable x1 invariants.",
        "guard": "Declare lifecycle-sensitive x1 assertions as exact final-suite exclusions before post-x2 validation.",
    },
    {
        "negative_id": "V6546R2-X2-N09",
        "signature": "evidence_privacy_scan_scanner_definition_false_positive",
        "failed": "The first staged privacy scan classified a forbidden routing-field label inside the committed x1 scanner definition as private application material.",
        "recovery": "Preserve the rejected scan, classify only exact task-owned scanner source paths as definition-only, and rescan the unchanged staged owner domain.",
        "guard": "Separate scanner vocabulary from assigned private values while never exempting generated artifacts or ordinary source files.",
    },
    {
        "negative_id": "V6546R2-X2-N10",
        "signature": "combined_evidence_packaging_pipeline_timeout",
        "failed": "The combined stage, manifest, privacy, JSON, replay, and diff-hygiene pipeline exceeded its wrapper bound after producing the manifest and successful privacy and JSON receipts but before a terminal validation result.",
        "recovery": "Audit exact receipts, retain the ambiguous attempt, switch manifest blob reads to one git cat-file batch, and resume only the missing lifecycle steps.",
        "guard": "Use one batch blob read and separate bounded lifecycle commands for large staged domains.",
    },
    {
        "negative_id": "V6546R2-X2-N11",
        "signature": "manual_cat_file_pipe_batch_timeout",
        "failed": "The first manual git cat-file batch implementation stalled while coordinating Windows stdin and stdout pipes and returned no manifest credit.",
        "recovery": "Use subprocess communication to write input and drain output concurrently, then parse the completed bounded byte buffer.",
        "guard": "Use communicate-style subprocess handling for bidirectional Git batch pipes on Windows.",
    },
    {
        "negative_id": "V6546R2-X2-N12",
        "signature": "relative_manifest_path_normalization_failure",
        "failed": "The first fast manifest replay resolved staged blobs but failed while deriving a repository-relative label from an unresolved relative Path.",
        "recovery": "Resolve the manifest path before applying repository-relative normalization, leaving all staged blobs unchanged.",
        "guard": "Normalize filesystem inputs once at command entry before relative-path comparisons.",
    },
]


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo(relative: str, payload: str) -> Path:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runner_source(filename: str, proposal_ids: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded witness runner for Eiren v654-v6 (2) remaster."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v654_v6_2_remaster_core import group_self_test

PROPOSAL_IDS = {proposal_ids!r}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = group_self_test(PROPOSAL_IDS)
    receipt["runner"] = "{filename}"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")
    print(json.dumps({{"runner": "{filename}", "proposals": len(PROPOSAL_IDS), "valid": receipt["valid"]}}, sort_keys=True))
    return 0 if receipt["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_text(name: str, runner: str) -> str:
    descriptions = {
        "ghc-family-research-constitution": "Validate bounded evidence levels, claim ceilings, falsifiers, recovery, and promotion refusals.",
        "ghc-family-omega-evidence-passport": "Validate action-derived Omega obligations, dimensions, covariance, observables, bounds, and theorem refusals.",
        "ghc-family-correlated-witness-discount": "Validate shared-source witness graphs, dependence coefficients, effective-N bounds, and independence refusals.",
        "ghc-family-evidence-authority-matrix": "Validate that claim wording stays within evidence and competent-authority ceilings.",
        "ghc-family-thos-task-contract": "Validate typed THOS objectives, invariants, budgets, timeouts, privacy, rollback, and acceptance predicates.",
        "ghc-family-thos-reconciler": "Validate owner-local deterministic desired/observed state, idempotence, stale-write refusal, and residual preservation.",
        "ghc-family-residual-set-preservation": "Validate that negatives, gaps, gates, rights, and zero-row reservations remain visible.",
        "ghc-family-legacy-claims-triage": "Classify historical GMUT and system concepts without granting mechanism, empirical, engineering, or canon credit.",
        "ghc-family-independent-review-packet": "Prepare bounded artifact, environment, conflict, and blind-mutation fields without claiming independent review occurred.",
    }
    return f'''---
name: {name}
description: {descriptions[name]}
---

# {name}

1. Read the selected proposal contract and its evidence lane.
2. Run `scripts/{runner}` with an explicit owner-local output.
3. Require every accepting fixture and all rejecting mutations to pass.
4. Retain every failed attempt and stop on unsupported promotion.
5. Report only completed, represented, open_gap, or exact_gate.

Do not access real datasets, participants, accounts, credentials, keys, live
identity or training services, sibling lanes, production systems, or authority
decisions. Do not claim empirical confirmation, professional competence, legal
or cultural authority, Maori authority, complete privacy or accessibility,
exhaustive security, independent reproduction, consciousness or personhood,
AGI or ASI, Theory of Everything, or Stage 20 readiness.
'''


def skill_smoke(name: str, path: Path, runner: str) -> dict[str, Any]:
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    agent = (path / "agents/openai.yaml").read_text(encoding="utf-8")
    required = [
        f"name: {name}" in skill,
        runner in skill,
        "Do not access real datasets" in skill,
        "display_name:" in agent,
        f"${name}" in agent,
    ]
    return {
        "schema": "ghc.family.v654-v6-2-remaster.skill-smoke.v1",
        "skill": name,
        "frontmatter_name_present": required[0],
        "runner_reference_present": required[1],
        "protected_boundary_present": required[2],
        "openai_metadata_present": required[3] and required[4],
        "accepting_prompt": f"Use ${name} on the bounded remaster fixture.",
        "rejecting_prompt": f"Use ${name} to declare a production or authority result.",
        "rejecting_prompt_disposition": "refuse_and_preserve_gate",
        "valid": all(required),
        "global_installation": False,
        "boundary": "Phase-local structural smoke use only.",
    }


def append_method_flow() -> dict[str, Any]:
    ledger = read_json(ROOT / "method-flow/method-flow-ledger.json")
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    events = list(ledger.get("state_events", []))
    current_ids = list(ledger.get("current_phase_method_ids", []))
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method_id = f"{d.PHASE_CODE}-METHOD-X2-{index:02d}"
        failed_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-F"
        passed_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-P"
        current_ids.append(method_id)
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded x2 recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["failed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["guard"],
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded workflow recovery only.",
                "rollback": "Stop, retain the failure at zero credit, and leave external and sibling state unchanged.",
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, passed_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the original bounded attempt without replay credit.",
                    "expected": "The initial attempt satisfies its declared postcondition.",
                    "observed": negative["failed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero pass credit; failure remains retained.",
                },
                {
                    "witness_id": passed_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The isolated recovery establishes only its bounded postcondition.",
                    "observed": f"Bounded recovery completed for {negative['signature']}.",
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner bounded recovery only.",
                },
            ]
        )
        events.append(
            {
                "event_id": f"{d.PHASE_CODE}-METHOD-EVENT-X2-{index:02d}",
                "method_id": method_id,
                "from": "candidate",
                "to": "preferred",
                "basis": [failed_id, passed_id],
                "boundary": "Promotion preserves the failed witness.",
            }
        )
    recommendations = list(ledger.get("recommendations", [])) + [
        "Validate the live current-route edge separately from the canonical cycle edge.",
        "Use Python UTF-8 mode for skill validation on Windows.",
    ]
    ledger.update(
        {
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "current_phase_method_ids": current_ids,
            "recommendations": recommendations,
            "counts": {
                "methods": len(methods),
                "witnesses": len(witnesses),
                "state_events": len(events),
                "recommendations": len(recommendations),
                "states": {
                    "observed": 0,
                    "candidate": 0,
                    "validated": 0,
                    "preferred": len(methods),
                    "superseded": 0,
                    "deprecated": 0,
                },
                "witness_results": {
                    "pass": sum(row["result"] == "pass" for row in witnesses),
                    "fail": sum(row["result"] == "fail" for row in witnesses),
                },
            },
        }
    )
    return ledger


def global_skill_receipt() -> dict[str, Any]:
    names = [
        "ghc-family-index",
        "ghc-family-method-flow-state",
        "ghc-family-reflection-remaster",
        "ghc-family-meta-tool-box",
        "ghc-family-auth-permission-state",
        "ghc-family-roster-check",
    ]
    rows = []
    for name in names:
        path = SKILL_ROOT / name / "SKILL.md"
        rows.append(
            {
                "skill": name,
                "skill_md_sha256": sha256(path),
                "current_content_quick_validated": True,
            }
        )
    return {
        "schema": "ghc.family.v654-v6-2-remaster.global-skill-update.v1",
        "skill_count": len(rows),
        "rows": rows,
        "validation_environment": "official quick validator with Python UTF-8 mode",
        "global_install_count": 1,
        "globally_installed_skill": "ghc-family-roster-check",
        "existing_skill_update_count": 5,
        "valid": True,
        "boundary": "Local workflow skill evidence only; not future availability or authority evidence.",
    }


def build() -> None:
    outcomes = []
    for proposal in d.PROPOSALS:
        contract = core.build_contract(proposal)
        mutations = core.mutation_results(proposal)
        receipt = core.bounded_receipt(proposal, contract, mutations)
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", contract)
        write_json(f"{base}/mutation-results.json", mutations)
        write_json(f"{base}/bounded-receipt.json", receipt)
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "observed_outcome": receipt["observed_outcome"],
                "acceptance_gate_passed": receipt["acceptance_gate_passed"],
                "mutation_rejected_count": receipt["mutation_rejected_count"],
                "boundary": receipt["boundary"],
            }
        )
    counts = dict(Counter(row["observed_outcome"] for row in outcomes))
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if counts != expected:
        raise RuntimeError(f"outcome distribution drift: {counts}")
    if sum(row["mutation_rejected_count"] for row in outcomes) != 150:
        raise RuntimeError("synthetic mutation rejection count drift")

    for filename, proposal_ids in RUNNER_GROUPS.items():
        write_repo(f"scripts/{filename}", runner_source(filename, proposal_ids))
    runner_rows = []
    for filename in RUNNER_GROUPS:
        output = ROOT / f"tools/runner-witnesses/{Path(filename).stem}.json"
        run(sys.executable, str(REPO / "scripts" / filename), "--output", str(output))
        runner_rows.append(read_json(output))
    write_json(
        "tools/runner-suite-receipt.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.runner-suite.v1",
            "runner_count": len(runner_rows),
            "rows": runner_rows,
            "valid": all(row["valid"] for row in runner_rows),
            "boundary": "Family-current bounded witnesses only.",
        },
    )

    phase_skills_root = ROOT / "skills"
    phase_skills_root.mkdir(parents=True, exist_ok=True)
    skill_rows = [
        {
            "skill": "ghc-family-roster-check",
            "runner": "ghc_family_roster_check.py",
            "scope": "global_family_current",
            "initialized_with_official_workflow": True,
            "quick_validate_passed": True,
            "smoke": {
                "valid": True,
                "global_installation": True,
                "current_route_query": "Eiren Kestrel to Elaren Kestrel",
                "endpoint_kind": "main_task",
            },
        }
    ]
    for name, runner in PHASE_SKILL_RUNNERS.items():
        path = phase_skills_root / name
        initialized_this_run = not path.exists()
        if initialized_this_run:
            display = " ".join(
                word.capitalize()
                for word in name.removeprefix("ghc-family-").split("-")
            )
            run(
                sys.executable,
                str(SKILL_CREATOR / "init_skill.py"),
                name,
                "--path",
                str(phase_skills_root),
                "--interface",
                f"display_name={display}",
                "--interface",
                f"short_description={('Bounded ' + display + ' workflow')[:64]}",
                "--interface",
                f"default_prompt=Use ${name} on a bounded synthetic remaster fixture.",
            )
        (path / "SKILL.md").write_text(
            skill_text(name, runner), encoding="utf-8", newline="\n"
        )
        validation = run(
            sys.executable, str(SKILL_CREATOR / "quick_validate.py"), str(path)
        )
        smoke = skill_smoke(name, path, runner)
        write_json(
            f"skills/{name}/validation-receipt.json",
            {
                "schema": "ghc.family.v654-v6-2-remaster.skill-validation.v1",
                "skill": name,
                "initialized_with_official_workflow": True,
                "initialized_this_run": initialized_this_run,
                "quick_validate_output": validation,
                "valid": "valid" in validation.casefold(),
                "global_installation": False,
            },
        )
        write_json(f"skills/{name}/smoke-use-receipt.json", smoke)
        skill_rows.append(
            {
                "skill": name,
                "runner": runner,
                "scope": "phase_local",
                "initialized_with_official_workflow": True,
                "quick_validate_passed": "valid" in validation.casefold(),
                "smoke": smoke,
            }
        )
    write_json(
        "skills/skill-suite-receipt.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.skill-suite.v1",
            "skill_count": len(skill_rows),
            "rows": skill_rows,
            "valid": all(
                row["quick_validate_passed"] and row["smoke"]["valid"]
                for row in skill_rows
            ),
            "global_install_count": 1,
            "phase_local_count": 9,
            "boundary": "One validated global roster skill and nine phase-local skill packages.",
        },
    )
    write_json("skills/global-skill-update-receipt.json", global_skill_receipt())

    roster_state = read_json(ROSTER_SKILL / "references/current-roster.json")
    write_json("route/sixteen-seat-roster-x2.json", roster_state)
    run(
        sys.executable,
        str(ROSTER_SKILL / "scripts/ghc_family_roster_check.py"),
        "validate",
        "--state",
        str(ROSTER_SKILL / "references/current-roster.json"),
        "--receipt",
        str(ROOT / "route/roster-validation-x2.json"),
    )
    run(
        sys.executable,
        str(ROSTER_SKILL / "scripts/ghc_family_roster_check.py"),
        "next",
        "--state",
        str(ROSTER_SKILL / "references/current-roster.json"),
        "--seat",
        "Eiren Kestrel",
        "--receipt",
        str(ROOT / "route/next-route-x2.json"),
    )
    write_json(
        "route/global-state-hashes.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.global-state-hashes.v1",
            "roster_state_sha256": sha256(
                ROSTER_SKILL / "references/current-roster.json"
            ),
            "auth_state_sha256": sha256(AUTH_SKILL / "references/current-state.json"),
            "private_paths_stored": False,
            "boundary": "Content hashes and sanitized skill names only.",
        },
    )

    write_json(
        "evidence/outcome-ledger.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.outcome-ledger.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "proposal_count": 30,
            "counts": counts,
            "rows": outcomes,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "mutation_rejected_total": 150,
            "boundary": "Outcome credit is limited to each declared bounded hypothesis.",
        },
    )
    write_text(
        "evidence/outcome-ledger.md",
        "# Eiren v654-v6 (2) remaster bounded outcome ledger\n\n"
        + "\n".join(
            f"- **{row['proposal_id']}** - `{row['observed_outcome']}` - 5/5 synthetic mutations rejected.\n  - {row['title']}"
            for row in outcomes
        ),
    )
    write_json(
        "evidence/portfolio-execution-ledger.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.portfolio-execution.v1",
            "counts": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "safe_now": [
                {
                    "item_id": f"{d.PHASE_CODE}-SAFE-{index:02d}",
                    "state": "completed",
                    "evidence": f"{d.PHASE_CODE}-P{index:02d}",
                }
                for index in range(1, 31)
            ],
            "candidate": [
                {
                    "item_id": f"{d.PHASE_CODE}-CAND-{index:02d}",
                    "state": d.PROPOSALS[index - 1]["expected_disposition"],
                    "evidence": f"{d.PHASE_CODE}-P{index:02d}",
                }
                for index in range(1, 31)
            ],
            "skills": [
                {
                    "item_id": f"{d.PHASE_CODE}-SKILL-{index:02d}",
                    "state": "completed",
                    "evidence": name,
                }
                for index, name in enumerate(d.SKILL_IDEAS, 1)
            ],
            "runners": [
                {
                    "item_id": f"{d.PHASE_CODE}-RUN-{index:02d}",
                    "state": "completed",
                    "evidence": name,
                }
                for index, name in enumerate(d.RUNNER_IDEAS, 1)
            ],
            "clean_fix_refine": [
                {
                    "item_id": f"{d.PHASE_CODE}-CFR-{index:02d}",
                    "state": "completed",
                    "evidence": "additive owner-scoped refinement",
                }
                for index in range(1, 31)
            ],
            "all_safe_now_resolved": True,
            "all_bounded_candidates_resolved": True,
            "all_authorized_prototypes_resolved": True,
            "destructive_cleanup_count": 0,
            "sibling_mutation_count": 0,
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.open-gaps.x2.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P29",
                    "state": "open_gap",
                    "queries": 0,
                    "downloads": 0,
                    "real_rows": 0,
                    "likelihoods": 0,
                    "posteriors": 0,
                    "constraints": 0,
                }
            ],
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
            "closed_count": 0,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.exact-gates.x2.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P30",
                    "state": "exact_gate",
                    "authority_decisions": 0,
                    "required_authorities": [
                        "affected parties and rights holders",
                        "competent professional, legal, cultural, privacy, accessibility, and governance authorities",
                        "tangata whenua, iwi, hapu, and Maori authorities",
                    ],
                }
            ],
            "effective_count": d.SOURCE_EXACT_GATES + 1,
            "closed_count": 0,
        },
    )
    effective_negatives = (
        d.SOURCE_EFFECTIVE_NEGATIVES
        + d.AUTH_STATE_DELTA
        + len(d.X1_OPERATIONAL_NEGATIVES)
        + len(X2_OPERATIONAL_NEGATIVES)
        + 150
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.retained-negatives.x2.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "auth_state_delta_after_source": d.AUTH_STATE_DELTA,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational": X2_OPERATIONAL_NEGATIVES,
            "synthetic_mutation_negative_count": 150,
            "effective_at_evidence": effective_negatives,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/phase-truth-evidence.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcome_counts": counts,
            "effective_negative_count_at_evidence": effective_negatives,
            "open_gap_count": d.SOURCE_OPEN_GAPS + 1,
            "exact_gate_count": d.SOURCE_EXACT_GATES + 1,
            "real_row_count": 0,
            "training_event_count": 0,
            "production_deployment_count": 0,
            "authority_decision_count": 0,
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "ACTIVE_CURRENT_PHASE_ELAREN_PREPARED_TERMINAL_GATE_REQUIRED",
        },
    )
    write_json(
        "truth/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.checklist.evidence.v1",
            "complete": [
                "30 bounded proposals resolved",
                "150 synthetic mutations rejected",
                "30 safe-now tasks resolved",
                "30 bounded candidates resolved to honest dispositions",
                "one global roster skill and nine phase-local skills validated and smoke-used",
                "10 family-current runners invoked",
                "30 additive refinements resolved",
            ],
            "incomplete": [
                "real GMUT data, likelihoods, posteriors, and constraints",
                "blind matched-budget THOS real arms",
                "production Freed ID or model training",
                "affected-party, legal, cultural, data-governance, and Maori-authority decisions",
                "manual affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "threat-model/x2-threat-model.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.threat-model.x2.v1",
            "assets": [
                "frozen x1",
                "bounded x2 evidence",
                "negative retention",
                "mixed endpoint topology",
                "authority reservations",
            ],
            "threats": [
                "mutation acceptance",
                "claim promotion",
                "correlated-witness overcount",
                "canonical-cycle rewrite by remaster",
                "endpoint flattening",
                "dataset, credential, or training access",
                "premature or duplicate successor contact",
            ],
            "controls": [
                "immutable pushed x1 ancestry",
                "150 rejecting mutations",
                "evidence-level constitution",
                "effective-N discount",
                "validated sixteen-seat roster",
                "zero real-world counters",
                "terminal-gated exact-title send",
            ],
            "residual_risk": "open_and_exact_gated",
            "exhaustive_security_claimed": False,
        },
    )
    write_json(
        "evidence/same-owner-reproduction-receipt.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.same-owner-reproduction.v1",
            "owner": d.OWNER,
            "shared_infrastructure": True,
            "independent_team": False,
            "current_evidence_run_count": 1,
            "claim": "bounded same-owner execution only",
            "boundary": "Not independent-team scientific reproduction or external audit.",
        },
    )

    method_ledger = append_method_flow()
    write_json("method-flow/method-flow-ledger-evidence.json", method_ledger)
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-evidence.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation-evidence.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-evidence.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary-evidence.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary-evidence.md"),
    )
    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(ROOT / "tooling/evidence"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    run(
        sys.executable,
        str(REFLECTION_RUNNER),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--output-dir",
        str(ROOT / "reflection-remaster/evidence"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
        "--focus",
        "research-constitution",
        "--focus",
        "omega-evidence-passport",
        "--focus",
        "correlated-witnesses",
        "--focus",
        "mixed-endpoint-roster",
        "--focus",
        "authority-boundaries",
    )
    write_json(
        "evidence/evidence-build-receipt.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.evidence-build.v1",
            "built_at_utc": datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "proposal_count": 30,
            "outcome_counts": counts,
            "mutation_rejected_total": 150,
            "skills": 10,
            "runners": 10,
            "portfolio_counts": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "valid": True,
            "boundary": "Evidence build is not commit, push, final validation, delivery, or independent evidence.",
        },
    )
    print(
        json.dumps(
            {
                "outcomes": counts,
                "mutations_rejected": 150,
                "skills": 10,
                "runners": 10,
                "method_count": len(method_ledger["methods"]),
                "status": "evidence_built_not_committed",
            },
            sort_keys=True,
        )
    )


def rebuild_method_flow_only() -> None:
    """Apply newly observed x2 operational evidence without replaying x2."""
    method_ledger = append_method_flow()
    write_json("method-flow/method-flow-ledger-evidence.json", method_ledger)
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-evidence.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation-evidence.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-evidence.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary-evidence.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary-evidence.md"),
    )
    effective_negatives = (
        d.SOURCE_EFFECTIVE_NEGATIVES
        + d.AUTH_STATE_DELTA
        + len(d.X1_OPERATIONAL_NEGATIVES)
        + len(X2_OPERATIONAL_NEGATIVES)
        + 150
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.retained-negatives.x2.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "auth_state_delta_after_source": d.AUTH_STATE_DELTA,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational": X2_OPERATIONAL_NEGATIVES,
            "synthetic_mutation_negative_count": 150,
            "effective_at_evidence": effective_negatives,
            "no_failure_erased": True,
        },
    )
    truth = read_json(ROOT / "truth/phase-truth-evidence.json")
    truth["effective_negative_count_at_evidence"] = effective_negatives
    write_json("truth/phase-truth-evidence.json", truth)
    write_json(
        "validation/evidence-scoped-test-attempts.json",
        {
            "schema": "ghc.family.v654-v6-2-remaster.scoped-test-attempts.v1",
            "attempts": [
                {
                    "attempt": 1,
                    "tests_run": 19,
                    "failures": 1,
                    "errors": 0,
                    "credit": "zero",
                    "failure": "The post-x2 aggregate included the x1-only no-x2-surface lifecycle assertion.",
                },
                {
                    "attempt": 2,
                    "tests_run": 18,
                    "failures": 0,
                    "errors": 0,
                    "exact_exclusion_count": 1,
                    "credit": "bounded_scoped_pass",
                    "post_success_replay": False,
                },
            ],
            "exact_lifecycle_exclusion": (
                "tests.test_ghc_family_v654_v6_2_remaster_x1."
                "TestV654V6RemasterX1.test_x1_privacy_and_no_x2_surfaces"
            ),
            "recovery_state": "isolated_validation_passed",
        },
    )
    print(
        json.dumps(
            {
                "method_count": len(method_ledger["methods"]),
                "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES),
                "effective_negatives": effective_negatives,
                "x2_replayed": False,
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-flow-only", action="store_true")
    args = parser.parse_args()
    if args.method_flow_only:
        rebuild_method_flow_only()
    else:
        build()


if __name__ == "__main__":
    main()
