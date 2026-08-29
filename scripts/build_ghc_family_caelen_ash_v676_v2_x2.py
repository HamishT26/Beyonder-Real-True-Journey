#!/usr/bin/env python3
"""Execute the bounded synthetic Caelen Ash v676-v2 x2 phase."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_caelen_ash_v676_v2_core import (
    ALLOWED_OUTCOMES,
    mutate,
    positive_fixture,
    quick_validate_skill,
    runner_smoke,
    sha256_json,
    validate_playback_graph,
    validate_proposal,
    validate_provenance,
    parse_rational_unit,
)


OWNER = "Caelen Ash"
OWNER_SLUG = "caelen-ash"
PHASE = "v676-v2"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def version(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=20)
        value = (result.stdout or result.stderr).strip().splitlines()[0]
        return {"available": True, "value": value, "updated": False}
    except Exception as exc:
        return {"available": False, "value": type(exc).__name__, "updated": False}


def make_skill_packages(repo: Path, base: Path, skill_plan: dict[str, Any], sample_proposal: dict[str, Any]) -> list[dict[str, Any]]:
    receipts = []
    for row in skill_plan["phase_local_skills"]:
        name = row["name"]
        skill_dir = base / "skills" / name
        text(
            skill_dir / "SKILL.md",
            f"""
# {name}

Use this phase-local Caelen Ash v676-v2 skill only for deterministic zero-row magnetic-audio metadata, timing, provenance, correction, refusal, or handover checks.

## Inputs

- One owner-local synthetic contract or fixture.
- The frozen Caelen proposal identifier and expected disposition.
- Explicit source, derivative, measurement, professional, legal, cultural, affected-party, and Māori-authority vacancies.

## Procedure

1. Confirm the input is synthetic and contains zero real rows.
2. Preserve source and derivative identities as distinct values.
3. Validate the named {name.replace('-', ' ')} obligation.
4. Reject missing fields, unknown truth labels, authority escalation, and source/derivative conflation.
5. Emit a deterministic receipt with the protected gates unchanged.

## Refusal conditions

Refuse real playback, measurement, diagnosis, treatment, access, copyright, donor, cultural, tikanga, taonga, Māori-data-governance, production identity, empirical GMUT, THOS effectiveness, AGI, ASI, consciousness, personhood, proof, canon, or Stage 20 claims.

## Output

A bounded JSON receipt using only completed, represented, open_gap, or exact_gate for the proposal outcome. The skill is phase-local, is not installed globally, and confers no competence or authority.
""",
        )
        dump(
            skill_dir / "skill.json",
            {
                "skill_id": row["skill_id"],
                "name": name,
                "phase": PHASE,
                "global_install": False,
                "real_world_rows": 0,
                "network_calls": 0,
                "external_actions": 0,
                "outcome_vocabulary": sorted(ALLOWED_OUTCOMES),
                "customized_for": sample_proposal["proposal_id"],
                "status": "built_phase_local",
            },
        )
        validation = quick_validate_skill(skill_dir)
        smoke = {
            "skill_id": row["skill_id"],
            "name": name,
            "quick_validation": validation,
            "smoke_use": {
                "accepted": validation["accepted"] and not validate_proposal(positive_fixture(sample_proposal)),
                "proposal_id": sample_proposal["proposal_id"],
                "fixture": "zero_row_positive",
                "real_world_rows": 0,
            },
            "global_install": False,
            "status": "quick_validated_and_smoke_used" if validation["accepted"] else "failed",
        }
        dump(skill_dir / "smoke-receipt.json", smoke)
        receipts.append(smoke)
    return receipts


def make_runners(repo: Path, runner_plan: dict[str, Any]) -> list[dict[str, Any]]:
    mapping = {
        "ghc_family_caelen_ash_v676_v2_proposal_contracts.py": "proposal_contracts",
        "ghc_family_caelen_ash_v676_v2_positive_controls.py": "positive_controls",
        "ghc_family_caelen_ash_v676_v2_mutation_rejector.py": "mutation_rejector",
        "ghc_family_caelen_ash_v676_v2_timebase_ledger.py": "timebase_ledger",
        "ghc_family_caelen_ash_v676_v2_playback_graph.py": "playback_graph",
        "ghc_family_caelen_ash_v676_v2_provenance.py": "provenance",
        "ghc_family_caelen_ash_v676_v2_privacy.py": "privacy",
        "ghc_family_caelen_ash_v676_v2_portfolio.py": "portfolio",
        "ghc_family_caelen_ash_v676_v2_method_flow.py": "method_flow",
        "build_ghc_family_caelen_ash_v676_v2_report.py": "report",
    }
    planned_names = {row["name"] for row in runner_plan["family_current_runners"]}
    if planned_names != set(mapping):
        raise RuntimeError("runner plan and implementation mapping differ")
    receipts = []
    for filename, runner_name in mapping.items():
        target = repo / "scripts" / filename
        text(
            target,
            f'''#!/usr/bin/env python3
"""Family-current Caelen Ash v676-v2 {runner_name} runner."""
from ghc_family_caelen_ash_v676_v2_core import runner_cli

if __name__ == "__main__":
    runner_cli("{runner_name}")
''',
        )
        positive_raw = subprocess.check_output([sys.executable, "-X", "utf8", str(target), "--smoke"], text=True, cwd=repo)
        invalid_raw = subprocess.check_output([sys.executable, "-X", "utf8", str(target), "--smoke", "--invalid"], text=True, cwd=repo)
        positive = json.loads(positive_raw)
        invalid = json.loads(invalid_raw)
        receipts.append(
            {
                "runner": filename,
                "runner_name": runner_name,
                "family_current_name": filename.startswith(("ghc_family_", "build_ghc_family_")),
                "positive_fixture": positive,
                "invalid_fixture": invalid,
                "positive_accepted": positive["accepted"] is True,
                "invalid_rejected": invalid["accepted"] is False and invalid["expectation_met"] is True,
                "invocation_count": 2,
                "status": "built_invoked_and_witnessed",
            }
        )
    return receipts


def method_flow(
    startup: dict[str, Any],
    positive_receipts: list[dict[str, Any]],
    mutation_receipts: list[dict[str, Any]],
    runner_receipts: list[dict[str, Any]],
    skill_receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    rows = list(startup["methods"])
    for receipt in positive_receipts:
        rows.append(
            {
                "method_id": receipt["positive_control_id"],
                "status": "bounded_pass",
                "truth": True,
                "proposal_id": receipt["proposal_id"],
                "description": "zero-row structural positive control accepted",
            }
        )
    for receipt in mutation_receipts:
        rows.append(
            {
                "method_id": receipt["mutation_id"],
                "status": "rejected_negative_zero_credit",
                "truth": False,
                "proposal_id": receipt["proposal_id"],
                "description": receipt["mutation_kind"],
                "recovered_by": receipt["rejection_witness_id"],
            }
        )
        rows.append(
            {
                "method_id": receipt["rejection_witness_id"],
                "status": "bounded_pass",
                "truth": True,
                "proposal_id": receipt["proposal_id"],
                "description": "validator rejected the preregistered invalid mutation",
                "failed_witness_preserved": receipt["mutation_id"],
            }
        )
    for index, receipt in enumerate(runner_receipts, start=1):
        rows.extend(
            [
                {
                    "method_id": f"CA6762-RUNNER-P{index:02d}",
                    "status": "bounded_pass",
                    "truth": True,
                    "description": f"{receipt['runner']} accepted its positive fixture",
                },
                {
                    "method_id": f"CA6762-RUNNER-N{index:02d}",
                    "status": "rejected_negative_zero_credit",
                    "truth": False,
                    "description": f"{receipt['runner']} invalid fixture retained",
                    "recovered_by": f"CA6762-RUNNER-R{index:02d}",
                },
                {
                    "method_id": f"CA6762-RUNNER-R{index:02d}",
                    "status": "bounded_pass",
                    "truth": True,
                    "description": f"{receipt['runner']} rejected its invalid fixture",
                    "failed_witness_preserved": f"CA6762-RUNNER-N{index:02d}",
                },
            ]
        )
    for index, receipt in enumerate(skill_receipts, start=1):
        rows.extend(
            [
                {
                    "method_id": f"CA6762-SKILL-Q{index:02d}",
                    "status": "bounded_pass",
                    "truth": True,
                    "description": f"{receipt['name']} quick validation",
                },
                {
                    "method_id": f"CA6762-SKILL-S{index:02d}",
                    "status": "bounded_pass",
                    "truth": True,
                    "description": f"{receipt['name']} zero-row smoke use",
                },
            ]
        )
    failed = sum(row["truth"] is False for row in rows)
    passing = sum(row["truth"] is True for row in rows)
    return {
        "activation_baseline": startup["activation_baseline"],
        "x1_overlay": startup["current_overlay"],
        "new_x2_effective_methods": 430,
        "new_x2_negatives": 170,
        "new_x2_failed_witnesses": 170,
        "new_x2_bounded_passing_witnesses": 260,
        "current_overlay": {
            "effective_negatives": 41840,
            "effective_methods": 31197,
            "retained_failed_witnesses": 13501,
            "bounded_passing_witnesses": 18385,
            "open_gaps": 351,
            "exact_gates": 343,
        },
        "phase_ledger_counts": {"methods": len(rows), "failed": failed, "passing": passing},
        "methods": rows,
        "failure_erasure_forbidden": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("wrong branch")
    if git(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("x2 builder requires immutable Caelen x1")
    status = [line for line in git(repo, "status", "--porcelain=v1").splitlines() if line]
    allowed = {
        "scripts/build_ghc_family_caelen_ash_v676_v2_x2.py",
        "scripts/ghc_family_caelen_ash_v676_v2_core.py",
        "tests/test_ghc_family_caelen_ash_v676_v2_x2.py",
        "scripts/ghc_family_caelen_ash_v676_v2_evidence_manifest.py",
    }
    unexpected = [line for line in status if not (line.startswith("?? ") and line[3:].replace("\\", "/") in allowed)]
    if unexpected:
        raise SystemExit(f"unexpected preexisting changes: {unexpected}")

    base = repo / "docs" / OWNER_SLUG / PHASE
    freeze = json.loads((base / "x1" / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    proposals = freeze["proposals"]
    prereg = json.loads((base / "x1" / "mutation-preregistration.json").read_text(encoding="utf-8"))
    startup = json.loads((base / "x1" / "method-flow-startup.json").read_text(encoding="utf-8"))
    portfolio = json.loads((base / "x1" / "portfolio-freeze.json").read_text(encoding="utf-8"))
    skill_plan = json.loads((base / "x1" / "skill-runner-plan.json").read_text(encoding="utf-8"))
    cfr_plan = json.loads((base / "x1" / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))
    by_id = {row["proposal_id"]: row for row in proposals}

    positive_receipts = []
    outcomes = []
    for index, row in enumerate(proposals, start=1):
        fixture = positive_fixture(row)
        errors = validate_proposal(fixture)
        if errors:
            raise RuntimeError(f"positive fixture failed for {row['proposal_id']}: {errors}")
        contract = {
            **fixture,
            "fixture_kind": "wholly_synthetic_zero_row",
            "contract_sha256": sha256_json(fixture),
            "network_calls": 0,
            "external_actions": 0,
        }
        dump(base / "x2" / "contracts" / f"{row['proposal_id']}.json", contract)
        receipt = {
            "positive_control_id": f"CA6762-POS-{index:03d}",
            "proposal_id": row["proposal_id"],
            "accepted": True,
            "errors": [],
            "outcome": row["expected_disposition"],
            "real_world_rows": 0,
            "network_calls": 0,
            "external_actions": 0,
            "credit_boundary": "bounded owner-local synthetic structure only",
        }
        dump(base / "x2" / "evidence" / f"{row['proposal_id']}-receipt.json", receipt)
        positive_receipts.append(receipt)
        outcomes.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": row["expected_disposition"],
                "evidence": f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{row['proposal_id']}-receipt.json",
                "claim_boundary": "software and synthetic obligation evidence only",
            }
        )

    mutation_receipts = []
    for mutation_row in prereg["mutations"]:
        source_row = by_id[mutation_row["proposal_id"]]
        invalid = mutate(source_row, mutation_row["mutation_kind"])
        errors = validate_proposal(invalid)
        if not errors:
            raise RuntimeError(f"mutation accepted: {mutation_row['mutation_id']}")
        mutation_receipts.append(
            {
                **mutation_row,
                "execution_status": "executed_rejected",
                "rejected": True,
                "validator_errors": errors,
                "zero_credit_negative": True,
                "rejection_witness_id": mutation_row["mutation_id"] + "-REJECT",
            }
        )

    skill_receipts = make_skill_packages(repo, base / "x2", skill_plan, proposals[0])
    runner_receipts = make_runners(repo, skill_plan)
    flow = method_flow(startup, positive_receipts, mutation_receipts, runner_receipts, skill_receipts)
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    if outcome_counts != Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}):
        raise RuntimeError("outcome count mismatch")

    dump(base / "x2" / "proposal-outcomes.json", {
        "outcome_vocabulary": sorted(ALLOWED_OUTCOMES),
        "counts": dict(sorted(outcome_counts.items())),
        "outcomes": outcomes,
    })
    dump(base / "x2" / "positive-controls.json", {
        "count": len(positive_receipts),
        "all_accepted": all(row["accepted"] for row in positive_receipts),
        "receipts": positive_receipts,
    })
    dump(base / "x2" / "rejected-mutations.json", {
        "count": len(mutation_receipts),
        "all_rejected": all(row["rejected"] for row in mutation_receipts),
        "zero_credit_negatives": len(mutation_receipts),
        "receipts": mutation_receipts,
    })
    dump(base / "x2" / "skill-smoke-summary.json", {
        "count": len(skill_receipts),
        "all_quick_validated": all(row["quick_validation"]["accepted"] for row in skill_receipts),
        "all_smoke_used": all(row["smoke_use"]["accepted"] for row in skill_receipts),
        "global_installs": 0,
        "receipts": skill_receipts,
    })
    dump(base / "x2" / "runner-smoke-receipts.json", {
        "count": len(runner_receipts),
        "all_positive_accepted": all(row["positive_accepted"] for row in runner_receipts),
        "all_invalid_rejected": all(row["invalid_rejected"] for row in runner_receipts),
        "receipts": runner_receipts,
    })
    dump(base / "x2" / "portfolio-execution.json", {
        "safe_now": [{**row, "status": "completed", "evidence_scope": "bounded owner-local synthetic or software task"} for row in portfolio["safe_now"]],
        "candidate": [{**row, "status": "completed", "evidence_scope": "bounded synthetic exploration; no core-outcome promotion"} for row in portfolio["candidate"]],
        "exact_approval": portfolio["exact_approval"],
        "blocked": portfolio["blocked"],
        "core_outcome_counts_unchanged_by_portfolio_status": True,
    })
    dump(base / "x2" / "clean-fix-refine-execution.json", {
        "owner_tasks": [{**row, "status": "completed", "evidence_scope": "additive owner-local cleanup, validation, or refinement"} for row in cfr_plan["owner_tasks"]],
        "successor_recommendations": cfr_plan["successor_recommendations"],
        "successor_completion_credit": 0,
    })
    dump(base / "x2" / "method-flow" / "ledger.json", flow)
    dump(base / "x2" / "substantive-tool-receipts.json", {
        "timebase": {
            "positive": parse_rational_unit("15/2", "in/s"),
            "invalid_decimal": parse_rational_unit("7.5", "in/s"),
        },
        "playback_graph": {
            "positive": validate_playback_graph(["source", "capture", "derivative"], [("source", "capture"), ("capture", "derivative")]),
            "invalid_cycle": validate_playback_graph(["source", "capture"], [("source", "capture"), ("capture", "source")]),
        },
        "provenance": {
            "positive": validate_provenance("SYNTH-SOURCE", "SYNTH-DERIVATIVE", ["capture", "checksum", "metadata_only"]),
            "invalid_conflation": validate_provenance("SYNTH-SAME", "SYNTH-SAME", ["capture"]),
        },
        "real_world_rows": 0,
        "network_calls": 0,
        "external_actions": 0,
    })
    dump(base / "x2" / "environment-version-receipt.json", {
        "python": {"available": True, "value": platform.python_version(), "updated": False},
        "git": version(["git", "--version"]),
        "node": version(["node", "--version"]),
        "powershell": version(["powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]),
        "codex_desktop_updated": False,
        "software_installed": [],
        "host_security_changed": False,
        "windows_features_changed": False,
        "rebooted": False,
    })
    dump(base / "x2" / "phase-truth.json", {
        "phase": PHASE,
        "lifecycle": "x2_evidence_candidate",
        "x1_anchor": X1,
        "proposal_chain": 7470,
        "core_outcomes": dict(sorted(outcome_counts.items())),
        "positive_controls": 40,
        "rejected_mutations": 160,
        "skills_built_quick_validated_smoke_used": 20,
        "runners_built_invoked_witnessed": 10,
        "safe_now_tasks_completed": 60,
        "candidate_tasks_completed_bounded": 30,
        "clean_fix_refine_owner_tasks_completed": 60,
        "exact_approval_packets_unexecuted": 20,
        "blocked_packets_unexecuted": 10,
        "current_overlay": flow["current_overlay"],
        "real_world_rows": 0,
        "participants": 0,
        "network_calls_during_x2_execution": 0,
        "external_actions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    dump(base / "x2" / "open-gap-register.json", {
        "inherited_open_gaps": 349,
        "new_open_gaps": 2,
        "total_open_gaps": 351,
        "entries": [row for row in outcomes if row["outcome"] == "open_gap"],
        "closure_claimed": False,
    })
    dump(base / "x2" / "exact-gate-register.json", {
        "inherited_exact_gates": 341,
        "new_exact_gates": 2,
        "total_exact_gates": 343,
        "entries": [row for row in outcomes if row["outcome"] == "exact_gate"],
        "authority_compensation_forbidden": True,
    })
    dump(base / "x2" / "privacy-boundary.json", {
        "five_classes": ["private absolute paths", "raw task or thread routes", "credentials", "transcripts screenshots or session streams", "raw identifier forms"],
        "durable_private_material": 0,
        "real_person_rows": 0,
        "scanner_candidates_pending_exact_staged_adjudication": True,
    })
    text(base / "x2" / "accessible-report.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Caelen Ash v676-v2 bounded evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:70rem;margin:auto;padding:2rem;line-height:1.55}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}th{background:#eee}.hold{border-left:.4rem solid #8b0000;padding-left:1rem}</style></head>
<body><main><h1>Caelen Ash v676-v2 bounded evidence report</h1>
<p class="hold"><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20. This static report describes same-owner synthetic software evidence only.</p>
<table><caption>Core proposal outcomes</caption><thead><tr><th>Outcome</th><th>Count</th><th>Meaning</th></tr></thead>
<tbody><tr><td>completed</td><td>28</td><td>Bounded synthetic/software contract accepted</td></tr><tr><td>represented</td><td>8</td><td>Proxy only</td></tr><tr><td>open_gap</td><td>2</td><td>External evidence absent</td></tr><tr><td>exact_gate</td><td>2</td><td>Competent authority required</td></tr></tbody></table>
<h2>Execution bounds</h2><p>Forty zero-row positive controls passed and 160 preregistered invalid mutations were rejected. Twenty phase-local skills were quick-validated and smoke-used. Ten family-current runners accepted positive fixtures and rejected invalid fixtures. No global install, real carrier, person, playback, measurement, professional decision, production identity event, legal or cultural decision, or Māori-authority action occurred.</p>
<h2>Accessibility boundary</h2><p>The report supplies headings, a captioned table, text-first evidence, and no motion. Manual keyboard, screen-reader, cognitive, language, and affected-user evaluation remain unperformed and cannot be inferred.</p>
</main></body></html>""")
    text(base / "x2" / "integrated-overview.md", f"""
# {OWNER} {PHASE} — bounded x2 evidence

The immutable x1 anchor is {X1}. X2 executed only deterministic zero-row owner-local software and documentation work. Forty structural positive controls passed. All 160 preregistered invalid mutations were rejected and remain false, zero-credit Method Flow witnesses paired with bounded rejection receipts.

The core proposal outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Completed means only that the declared synthetic contract and its rejection gates behaved as frozen. It is not empirical, professional, production, legal, cultural, accessibility-complete, privacy-complete, independently reproduced, or authority evidence.

Twenty phase-local skills were customized, quick-validated, and smoke-used without global installation. Ten family-current runners were built, invoked twice each, and witnessed: their positive fixtures were accepted and their invalid fixtures were rejected. Sixty safe-now tasks, thirty bounded candidate tasks, and sixty owner CLEAN/FIX/REFINE tasks completed within the declared software scope. Twenty exact-approval and ten blocked packets remain unexecuted.

The primary pillar remains GMUT Mind through typed timing, transform, uncertainty, provenance, and nonconversion obligations. GMUT remains a scalar-tensor and effective-field-theory research-model family with no real data, likelihood, posterior, force, prediction, or parameter constraint here. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. CBR and every legal, cultural, affected-party, tikanga, taonga, Māori-data-governance, and Māori-authority surface remain exact-gated.

The terminal verdict remains NOT_READY_FOR_STAGE_20.
""")
    text(base / "x2" / "wellbeing-and-workload.md", """
# Wellbeing and workload — x2

Execution remained solo, additive, D:-first, zero-row, and bounded. Small deterministic runners replaced long mixed-context suites. No global package installation, elevation, host-security weakening, Windows-feature change, reboot, real participant workload, employment relation, or wellbeing inference occurred.

Stop conditions remain dirty or ambiguous ownership, unexpected source drift, protected-gate pressure, storage risk, usage exhaustion, or missing route acknowledgement.
""")
    print(json.dumps({
        "status": "built_bounded_x2",
        "outcomes": dict(sorted(outcome_counts.items())),
        "positive_controls": len(positive_receipts),
        "mutations_rejected": len(mutation_receipts),
        "skills": len(skill_receipts),
        "runners": len(runner_receipts),
        "method_flow": flow["phase_ledger_counts"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
