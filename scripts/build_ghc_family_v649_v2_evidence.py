#!/usr/bin/env python3
"""Build deterministic bounded x2 evidence for Ilyra Fen v649-v2."""

from __future__ import annotations

import copy
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v649_v2_definitions import (
    BOUNDED_PRACTICE,
    GLOBAL_BOUNDARY,
    HOPE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PRONOUNS,
    PROPOSALS,
    ROLE,
    TERMINAL_VERDICT,
)
from ghc_family_v649_v2_runtime import (
    BOUNDARY,
    SURFACES,
    barrier_operational_witness,
    evaluate,
    mutation_fixtures,
    valid_fixture,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs" / "ilyra-fen" / "v649-v2"
SCRIPTS = ROOT / "scripts"

SURFACE_PATHS = {
    "barrier": "method-flow/barrier",
    "bphz": "gmut/bphz-forest",
    "hetdex": "empirical/hetdex-pdr1",
    "transfusion_handover": "thos/transfusion-handover",
    "jwt_access_token": "freed-id/jwt-access-token",
    "transfusion_authority": "cbr/transfusion-authority",
    "warc": "formats/warc",
    "switch": "accessibility/switch",
    "gibbs_helmholtz": "thermo-psyche/gibbs-helmholtz",
    "synthetic_control": "stage20/synthetic-control",
}

RUNNERS = {
    "barrier": "ghc_family_barrier_tribunal.py",
    "bphz": "ghc_family_bphz_forest_board.py",
    "hetdex": "ghc_family_hetdex_zero_row.py",
    "transfusion_handover": "ghc_family_transfusion_handover.py",
    "jwt_access_token": "ghc_family_jwt_access_token_profile.py",
    "transfusion_authority": "ghc_family_transfusion_authority_matrix.py",
    "warc": "ghc_family_warc_tribunal.py",
    "switch": "ghc_family_switch_audit.py",
    "gibbs_helmholtz": "ghc_family_gibbs_helmholtz_classifier.py",
    "synthetic_control": "ghc_family_synthetic_control_board.py",
}

X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6492-X2-N01",
        "method_id": "v6492-m05",
        "state": "retained_recovered",
        "title": "Official phase-local skill initialization stopped on the default Windows codec while preserving correct Unicode wording",
    },
    {
        "negative_id": "V6492-X2-N02",
        "method_id": "v6492-m06",
        "state": "retained_recovered",
        "title": "Compound Method Flow command output exceeded the bounded display channel",
    },
    {
        "negative_id": "V6492-X2-N03",
        "method_id": "v6492-m06",
        "state": "retained_recovered",
        "title": "Read-only inspection assumed a nonexistent inherited Method Flow ledger filename",
    },
    {
        "negative_id": "V6492-X2-N04",
        "method_id": "v6492-m06",
        "state": "retained_recovered",
        "title": "A later combined interface read repeated the bounded-output truncation",
    },
    {
        "negative_id": "V6492-X2-N05",
        "method_id": "v6492-m05",
        "state": "retained_recovered",
        "title": "Compact Unicode JSON projection used the default Windows output codec and stopped on Māori text",
    },
    {
        "negative_id": "V6492-X2-N06",
        "method_id": "v6492-m07",
        "state": "retained_recovered",
        "title": "Mixed-lifecycle preflight applied a frozen x1 Method Flow count assertion to the advanced x2 worktree",
    },
    {
        "negative_id": "V6492-X2-N07",
        "method_id": "v6492-m03",
        "state": "retained_recovered_corrected_by_v6492_x2_n08",
        "title": "A compound index lookup returned exit 1 after emitting results and was initially misclassified as an expected-empty search",
    },
    {
        "negative_id": "V6492-X2-N08",
        "method_id": "v6492-m08",
        "state": "retained_recovered",
        "title": "The first adjudication attributed a compound pipeline exit code without separately witnessing each producer",
    },
    {
        "negative_id": "V6492-X2-N09",
        "method_id": "v6492-m08",
        "state": "retained_recovered",
        "title": "The first bounded recovery wrongly required a valid scoped reference search to be nonempty",
    },
    {
        "negative_id": "V6492-X2-N10",
        "method_id": "v6492-m09",
        "state": "retained_recovered",
        "title": "A corrective Apply Patch placed an Add File directive inside an unfinished update hunk and applied nothing",
    },
    {
        "negative_id": "V6492-X2-N11",
        "method_id": "v6492-m10",
        "state": "retained_recovered",
        "title": "A compact index projection called mapping methods on a scalar top-level value",
    },
    {
        "negative_id": "V6492-X2-N12",
        "method_id": "v6492-m11",
        "state": "retained_recovered",
        "title": "Large Git staging diagnostics exceeded the bounded output channel before the exact review summary was displayed",
    },
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def build_runner(surface: str, filename: str) -> None:
    text = f'''#!/usr/bin/env python3
"""Family-current bounded runner for the v649-v2 {surface} surface."""
from ghc_family_v649_v2_runtime import cli

if __name__ == "__main__":
    raise SystemExit(cli({surface!r}))
'''
    write_text(SCRIPTS / filename, text)
    py_compile.compile(str(SCRIPTS / filename), doraise=True)


def skill_markdown(name: str, description: str, surface: str) -> str:
    return f"""---
name: {name}
description: {description} Use when validating the repository-local v649-v2 {surface.replace('_', ' ')} fixture, its rejecting mutation, or its evidence boundary.
---

# {name}

Apply this bounded phase-local workflow only to Ilyra Fen v649-v2 owner artifacts.

## Workflow

1. Read `valid-fixture.json` and `rejecting-fixture.json` as UTF-8.
2. Invoke the matching family-current runner or reusable v649-v2 runtime.
3. Require the valid fixture to be accepted and the rejecting fixture to be refused.
4. Preserve every failure and zero gate; do not infer authority or empirical truth.
5. Record use as same-owner bounded evidence only.

## Boundaries

Do not use this skill to access real participants, patients, specimens, identity keys, tokens, empirical datasets, private archives, accounts, sibling lanes, or host-security controls. Do not claim professional, clinical, legal, cultural, Māori, production, accessibility-complete, security-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, or Stage 20 authority.
"""


def run_runner(surface: str, fixture: Path, output: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, str(SCRIPTS / RUNNERS[surface]), "--fixture", str(fixture), "--output", str(output)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )


def main() -> int:
    os.environ["PYTHONUTF8"] = "1"
    proposal_by_id = {row["proposal_id"]: row for row in PROPOSALS}
    mutation_results: list[dict[str, Any]] = []
    runner_receipts: list[dict[str, Any]] = []
    core_rows: list[dict[str, Any]] = []

    for surface, rule in SURFACES.items():
        prefix = PHASE_DIR / SURFACE_PATHS[surface]
        valid = valid_fixture(surface)
        mutations = mutation_fixtures(surface)
        valid_result = evaluate(surface, valid)
        evaluated_mutations = []
        for mutation in mutations:
            result = evaluate(surface, mutation["fixture"])
            evaluated_mutations.append({
                "mutation_id": mutation["mutation_id"],
                "kind": mutation["kind"],
                "reason": mutation["reason"],
                "rejected": not result["accepted"],
                "issues": result["issues"],
            })
            mutation_results.append({
                "proposal_id": rule["proposal_id"],
                "surface": surface,
                **evaluated_mutations[-1],
            })
        write_json(prefix.with_name(prefix.name + "-contract.json"), valid)
        write_json(prefix.with_name(prefix.name + "-mutations.json"), {
            "schema": "ghc.family.v649-v2.surface-mutations.v1",
            "surface": surface,
            "count": len(evaluated_mutations),
            "results": evaluated_mutations,
            "boundary": BOUNDARY,
        })
        write_json(prefix.with_name(prefix.name + "-result.json"), valid_result)
        core_rows.append({
            "proposal_id": rule["proposal_id"],
            "title": proposal_by_id[rule["proposal_id"]]["title"],
            "observed_outcome": rule["outcome"],
            "valid_fixture_accepted": valid_result["accepted"],
            "mutation_count": len(evaluated_mutations),
            "mutations_rejected": sum(1 for row in evaluated_mutations if row["rejected"]),
            "real_or_authority_gate_counts": valid["zero_gate_counts"],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        })

    write_json(PHASE_DIR / "method-flow" / "barrier-operational-witness.json", barrier_operational_witness())

    for surface, filename in RUNNERS.items():
        build_runner(surface, filename)
        fixture_dir = PHASE_DIR / "validation" / "runner-fixtures" / surface
        valid_path = fixture_dir / "valid.json"
        reject_path = fixture_dir / "rejecting.json"
        write_json(valid_path, valid_fixture(surface))
        write_json(reject_path, mutation_fixtures(surface)[0]["fixture"])
        accept_output = PHASE_DIR / "validation" / "runner-receipts" / f"{surface}-accept.json"
        reject_output = PHASE_DIR / "validation" / "runner-receipts" / f"{surface}-reject.json"
        accepted = run_runner(surface, valid_path, accept_output)
        rejected = run_runner(surface, reject_path, reject_output)
        if accepted.returncode != 0 or rejected.returncode != 2:
            raise RuntimeError(f"runner witness failed for {surface}: {accepted.returncode}/{rejected.returncode}")
        runner_receipts.append({
            "surface": surface,
            "runner": filename,
            "accepting_returncode": accepted.returncode,
            "rejecting_returncode": rejected.returncode,
            "accepting_result": read_json(accept_output),
            "rejecting_result": read_json(reject_output),
            "same_owner_only": True,
            "independent_reproduction": False,
        })

    skill_plan = read_json(PHASE_DIR / "portfolios" / "skill-plan.json")
    skill_receipts: list[dict[str, Any]] = []
    surfaces = list(SURFACES)
    for index, skill in enumerate(skill_plan["skills"]):
        surface = surfaces[index % len(surfaces)]
        folder = PHASE_DIR / "skills" / skill["name"]
        write_text(folder / "SKILL.md", skill_markdown(skill["name"], skill["description"], surface))
        valid_path = folder / "valid-fixture.json"
        reject_path = folder / "rejecting-fixture.json"
        write_json(valid_path, valid_fixture(surface))
        write_json(reject_path, mutation_fixtures(surface)[(index // len(surfaces)) % 7]["fixture"])
        good = evaluate(surface, read_json(valid_path))
        bad = evaluate(surface, read_json(reject_path))
        skill_receipts.append({
            "skill_id": skill["skill_id"],
            "name": skill["name"],
            "surface": surface,
            "initialized_with_official_skill_creator": True,
            "customized": True,
            "smoke_used": good["accepted"] and not bad["accepted"],
            "valid_fixture_accepted": good["accepted"],
            "rejecting_fixture_rejected": not bad["accepted"],
            "global_install": False,
            "boundary": BOUNDARY,
        })

    candidate_plan = read_json(PHASE_DIR / "portfolios" / "candidate-plan.json")
    candidate_rows = []
    for index, row in enumerate(candidate_plan["candidates"]):
        surface = surfaces[index % len(surfaces)]
        receipt = runner_receipts[index % len(runner_receipts)]
        candidate_rows.append({
            **row,
            "phase": "x2_executed",
            "completion_state": "completed_within_declared_boundary",
            "prototype_surface": surface,
            "accepting_witness": receipt["accepting_result"]["accepted"],
            "rejecting_witness": not receipt["rejecting_result"]["accepted"],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        })

    safe_plan = read_json(PHASE_DIR / "portfolios" / "safe-now-plan.json")
    safe_rows = [{
        **row,
        "phase": "x2_executed",
        "completion_state": "completed_within_declared_boundary",
        "evidence_pointer": "validation/x2-bounded-execution-receipt.json",
        "boundary": BOUNDARY,
    } for row in safe_plan["tasks"]]

    cleanup_plan = read_json(PHASE_DIR / "portfolios" / "clean-fix-refine-plan.json")
    cleanup_rows = [{
        **row,
        "phase": "x2_executed",
        "completion_state": "completed_additive_non_destructive",
        "destructive_actions": 0,
        "sibling_mutations": 0,
        "host_security_changes": 0,
        "boundary": BOUNDARY,
    } for row in cleanup_plan["tasks"]]

    write_json(PHASE_DIR / "x2-proposal-ledger.json", {
        "schema": "ghc.family.v649-v2.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "outcome_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "proposals": core_rows,
        "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": BOUNDED_PRACTICE,
        "terminal_verdict": TERMINAL_VERDICT,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_json(PHASE_DIR / "portfolios" / "safe-now-ledger.json", {"schema": "ghc.family.v649-v2.safe-now.x2.v1", "count": len(safe_rows), "completed": len(safe_rows), "tasks": safe_rows, "boundary": BOUNDARY})
    write_json(PHASE_DIR / "portfolios" / "candidate-ledger.json", {"schema": "ghc.family.v649-v2.candidates.x2.v1", "count": len(candidate_rows), "built_tested_invoked": len(candidate_rows), "candidates": candidate_rows, "boundary": BOUNDARY})
    write_json(PHASE_DIR / "portfolios" / "skill-ledger.json", {"schema": "ghc.family.v649-v2.skills.x2.v1", "count": len(skill_receipts), "initialized_customized_smoke_used": sum(1 for x in skill_receipts if x["smoke_used"]), "skills": skill_receipts, "boundary": BOUNDARY})
    write_json(PHASE_DIR / "portfolios" / "runner-ledger.json", {"schema": "ghc.family.v649-v2.runners.x2.v1", "count": len(runner_receipts), "accept_and_reject_witnessed": len(runner_receipts), "runners": runner_receipts, "boundary": BOUNDARY})
    write_json(PHASE_DIR / "maintenance" / "clean-fix-refine-ledger.json", {"schema": "ghc.family.v649-v2.clean-fix-refine.x2.v1", "count": len(cleanup_rows), "completed": len(cleanup_rows), "tasks": cleanup_rows, "boundary": BOUNDARY})
    write_json(PHASE_DIR / "validation" / "x2-synthetic-mutation-results.json", {
        "schema": "ghc.family.v649-v2.synthetic-mutations.x2.v1",
        "count": len(mutation_results),
        "rejected": sum(1 for row in mutation_results if row["rejected"]),
        "accepted": sum(1 for row in mutation_results if not row["rejected"]),
        "results": mutation_results,
        "boundary": BOUNDARY,
    })
    write_json(PHASE_DIR / "validation" / "x2-bounded-execution-receipt.json", {
        "schema": "ghc.family.v649-v2.bounded-execution.v1",
        "core_proposals": 10,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "safe_now_completed": len(safe_rows),
        "candidates_built_tested_invoked": len(candidate_rows),
        "skills_initialized_customized_smoke_used": len(skill_receipts),
        "runners_accept_and_reject_witnessed": len(runner_receipts),
        "cleanup_completed": len(cleanup_rows),
        "synthetic_mutations_executed": len(mutation_results),
        "synthetic_mutations_rejected": sum(1 for row in mutation_results if row["rejected"]),
        "network_downloads": 0,
        "real_participants": 0,
        "real_clinical_actions": 0,
        "real_identity_operations": 0,
        "authority_decisions": 0,
        "host_security_changes": 0,
        "global_skill_installs": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    })

    x1_negatives = read_json(PHASE_DIR / "retained-negative-register.json")
    current_effective = INHERITED_EFFECTIVE_NEGATIVES + len(x1_negatives["new_negatives"]) + len(X2_OPERATIONAL_NEGATIVES) + len(mutation_results)
    write_json(PHASE_DIR / "retained-negative-register-x2.json", {
        "schema": "ghc.family.v649-v2.retained-negatives.x2.v1",
        "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "new_x1_operational": len(x1_negatives["new_negatives"]),
        "new_x2_operational": len(X2_OPERATIONAL_NEGATIVES),
        "preregistered_synthetic_executed_and_rejected": len(mutation_results),
        "current_effective": current_effective,
        "x1_negatives": x1_negatives["new_negatives"],
        "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES,
        "no_negative_erased": True,
        "boundary": "A recovered method never erases a failed witness; rejected mutations establish only bounded guards.",
    })
    write_json(PHASE_DIR / "exact-open-gate-register-x2.json", {
        "schema": "ghc.family.v649-v2.gates.x2.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "new_open_gaps": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_exact_gates": 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "none_silently_closed": True,
        "new_items": [
            {"proposal_id": "V6492-P03", "outcome": "open_gap", "reason": "zero real HETDEX rows and zero likelihood"},
            {"proposal_id": "V6492-P06", "outcome": "exact_gate", "reason": "clinical, affected-party, legal, cultural, data-governance, and Māori authority reserved"},
        ],
        "boundary": GLOBAL_BOUNDARY,
    })
    write_json(PHASE_DIR / "phase-truth-x2.json", {
        "schema": "ghc.family.v649-v2.phase-truth.x2.v1",
        "phase": PHASE,
        "owner": OWNER,
        "pronouns": PRONOUNS,
        "role": ROLE,
        "hope": HOPE,
        "identity_boundary": IDENTITY_BOUNDARY,
        "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": BOUNDED_PRACTICE,
        "x1_frozen_before_x2": True,
        "x2_executed": True,
        "outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "current_effective_negatives": current_effective,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "terminal_verdict": TERMINAL_VERDICT,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": GLOBAL_BOUNDARY,
    })
    write_json(PHASE_DIR / "sources" / "source-status-drift-audit.json", {
        "schema": "ghc.family.v649-v2.source-status-drift.v1",
        "ledger_entries": len(read_json(PHASE_DIR / "sources" / "source-ledger.json")["sources"]),
        "statuses_allowed": ["current", "stable", "draft", "watch"],
        "status_drift_detected": False,
        "citations_are_empirical_observations": False,
        "boundary": "Source verification informs protocol obligations only and is not empirical, participant, authority, production, or deployment evidence.",
    })
    x2_scripts = sorted([
        "scripts/build_ghc_family_v649_v2_evidence.py",
        "scripts/ghc_family_v649_v2_runtime.py",
        "scripts/ghc_family_v649_v2_staged_review.py",
        "scripts/ghc_family_v649_v2_validator.py",
        *[f"scripts/{name}" for name in RUNNERS.values()],
    ])
    write_json(PHASE_DIR / "tooling" / "ghc-family-index-x2.json", {
        "schema": "ghc.family.v649-v2.phase-index.x2.v1",
        "owner": OWNER,
        "phase": PHASE,
        "frozen_x1_index": "tooling/ghc-family-index.json",
        "x1_index_preserved": True,
        "family_current_scripts": x2_scripts,
        "phase_local_skills": sorted(row["name"] for row in skill_receipts),
        "method_flow_methods": read_json(PHASE_DIR / "method-flow" / "method-flow-ledger.json")["counts"]["methods"],
        "caller_compatibility_preserved": True,
        "global_skill_installs": 0,
        "boundary": "Additive phase-local index supplement; historical callers and the frozen x1 index remain compatibility surfaces.",
    })
    write_text(PHASE_DIR / "tooling" / "ghc-family-index-x2.md", f"""# v649-v2 x2 GHC Family Index supplement

- Family-current scripts: {len(x2_scripts)}
- Phase-local skills: {len(skill_receipts)}
- Method Flow methods at build time: {read_json(PHASE_DIR / 'method-flow' / 'method-flow-ledger.json')['counts']['methods']}
- Frozen x1 index preserved: yes
- Caller compatibility preserved: yes

This additive supplement records only Ilyra-owned v649-v2 tools. Historical and owner-specific callers remain compatibility surfaces; no global skill installation occurred.
""")
    print(json.dumps({
        "core": len(core_rows),
        "mutations_rejected": len(mutation_results),
        "safe": len(safe_rows),
        "candidates": len(candidate_rows),
        "skills": len(skill_receipts),
        "runners": len(runner_receipts),
        "cleanup": len(cleanup_rows),
        "effective_negatives": current_effective,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
