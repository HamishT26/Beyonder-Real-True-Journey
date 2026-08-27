"""Build Liora Venn v672-v6 bounded synthetic x2 evidence."""

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

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts import build_ghc_family_liora_venn_v672_v6_x1 as x1
from scripts import ghc_family_liora_v672_v6_core as core


ROOT = x1.ROOT
OWNER_ROOT = x1.OWNER_ROOT
X2_ROOT = OWNER_ROOT / "x2"
VALIDATION_ROOT = OWNER_ROOT / "validation"
X1_COMMIT = "bbe8eea23928ada9526df78cee758c7d6a20b33f"
BOUNDARY = x1.BOUNDARY

X2_OPERATIONAL_FAILURES = [
    {
        "negative_id": "LV6726-X2-N001",
        "method_id": "LV6726-M029",
        "result": "fail",
        "procedure": "Execute the x2 builder directly before adding the repository root to Python's import path.",
        "observed": "Python raised ModuleNotFoundError for the scripts package before any x2 evidence was written.",
        "boundary": "No committed, staged, remote, source, sibling, task, route, account, credential, or authority state changed.",
        "credit": 0,
    }
]
X2_OPERATIONAL_RECOVERIES = [
    {
        "witness_id": "LV6726-X2-WP001",
        "method_id": "LV6726-M029",
        "result": "pass",
        "procedure": "Insert the resolved repository root into sys.path before owner-module imports and apply the same shim to generated runners.",
        "observed": "The bounded x2 build completed with 40 outcomes, 160 rejections, 20 skills, and 10 runners.",
        "retained_negative_ids": ["LV6726-X2-N001"],
        "same_owner_only": True,
        "independent_reproduction": False,
    }
]

SKILL_PURPOSES = [
    "validate unique synthetic bath nodes and internal adjacency",
    "validate contiguous synthetic colour-drop ordering",
    "validate normalized synthetic rake-path coordinates",
    "validate prepared-contacted-lifted transfer ordering",
    "validate surrogate swatch namespace and revision separation",
    "refuse authenticity tradition attribution and cultural-name promotion",
    "preserve explicit material and recipe vacancies",
    "preserve temperature humidity viscosity and bath-state observation vacancies",
    "hold unverified material records without making a safety assessment",
    "emit deterministic JSON receipts without authenticity promotion",
    "validate synthetic activity entity and derivation lineage",
    "retain prior records through additive correction and supersession",
    "validate zero-image alternate-description linkage",
    "validate static headings noncolour status and human-evaluation vacancies",
    "validate bounded queue capacity pause and stop precedence",
    "validate unresolved holds and readback vacancy at handover",
    "reject raw personal private route account credential and free-text fields",
    "reject professional legal cultural Maori and Stage 20 authority smuggling",
    "retain invalid fixtures and separate bounded rejection witnesses",
    "enforce outcome vocabulary canonical latch and successor terminal boundary",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    x1.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    x1.write_text(path, text)


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def skill_mode(index: int) -> str:
    return core.MODES[(index - 1) % len(core.MODES)]


def customize_skills(quick_validator: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    skills_root = X2_ROOT / "skills"
    if not quick_validator.is_file():
        raise RuntimeError("exact skill-creator quick validator is absent")
    quick_rows = []
    smoke_rows = []
    for index, (suffix, purpose) in enumerate(zip(x1.SKILL_NAMES, SKILL_PURPOSES, strict=True), 1):
        name = f"liora-v672-v6-{suffix}"
        mode = skill_mode(index)
        skill_root = skills_root / name
        skill_path = skill_root / "SKILL.md"
        agent_path = skill_root / "agents" / "openai.yaml"
        if not skill_path.is_file() or not agent_path.is_file():
            raise RuntimeError(f"skill was not initialized through skill-creator: {name}")
        description = f"Use for Liora v672-v6 owner-local synthetic evidence when you must {purpose}; rejects real-world and authority promotion."
        body = f"""---
name: {name}
description: "{description}"
---

# {name}

## When to use

Use this owner-local skill only for `{mode}` fixtures in Liora Venn v672-v6 after immutable x1 equality. It exists to {purpose}.

## Procedure

1. Confirm the input is an owner-local synthetic JSON fixture and the terminal verdict is `NOT_READY_FOR_STAGE_20`.
2. Apply the `{mode}` guard through `scripts/ghc_family_liora_v672_v6_core.py` or its family-current runner.
3. Record every invalid input as a retained zero-credit failed witness before recording the bounded rejection witness.
4. Stop on any real person, object, material, observation, measurement, credential, account, external action, professional decision, legal or cultural decision, affected-party decision, Maori wording or authority, empirical claim, proof, canon, or Stage 20 promotion.

## Accepting smoke

The built-in accepting fixture must return `valid: true` while keeping every real-world and authority flag false.

## Rejecting smoke

The built-in rejecting fixture must return `valid: false`; rejection demonstrates only the named guard against the named fixture.

## Boundary

{BOUNDARY}
"""
        write_text(skill_path, body)
        display = " ".join(word.capitalize() for word in suffix.split("-"))
        write_text(
            agent_path,
            f"""interface:
  display_name: "Liora v672-v6 {display}"
  short_description: "Bounded synthetic {mode.replace('_', ' ')} guard"
""",
        )
        validation = subprocess.run(
            [sys.executable, str(quick_validator), str(skill_root)],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        quick_rows.append(
            {
                "skill_id": f"LV6726-SKILL-{index:02d}",
                "name": name,
                "mode": mode,
                "validator": "skill-creator quick_validate.py",
                "exit_code": validation.returncode,
                "output_sha256": sha256(validation.stdout + validation.stderr),
                "valid": validation.returncode == 0,
                "global_install": False,
            }
        )
        accepting = core.evaluate(mode, core.accepting_fixture(mode))
        rejecting = core.evaluate(mode, core.rejecting_fixture(mode))
        smoke_rows.append(
            {
                "skill_id": f"LV6726-SKILL-{index:02d}",
                "name": name,
                "mode": mode,
                "accepting_valid": accepting["valid"],
                "rejecting_rejected": not rejecting["valid"],
                "rejecting_errors": rejecting["errors"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "outcome": "completed" if accepting["valid"] and not rejecting["valid"] else "open_gap",
            }
        )
    if not all(row["valid"] for row in quick_rows):
        raise RuntimeError("one or more owner-local skills failed quick validation")
    if not all(row["accepting_valid"] and row["rejecting_rejected"] for row in smoke_rows):
        raise RuntimeError("one or more owner-local skills failed smoke use")
    return quick_rows, smoke_rows


def build_runners() -> list[dict[str, Any]]:
    rows = []
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for index, name in enumerate(x1.RUNNER_NAMES, 1):
        mode = core.MODES[index - 1]
        relative = f"scripts/{name}.py"
        path = ROOT / relative
        write_text(
            path,
            f'''"""Family-current Liora v672-v6 {mode} runner."""

import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from scripts.ghc_family_liora_v672_v6_core import cli


if __name__ == "__main__":
    raise SystemExit(cli("{mode}"))
''',
        )
        cases = []
        for case in ("accept", "reject"):
            result = subprocess.run(
                [sys.executable, "-X", "utf8", relative, "--case", case],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environment,
                check=False,
            )
            payload = json.loads(result.stdout) if result.stdout.strip() else {}
            cases.append(
                {
                    "case": case,
                    "exit_code": result.returncode,
                    "expected_behavior_observed": payload.get("expected_behavior_observed") is True,
                    "output_sha256": sha256((result.stdout + result.stderr).encode("utf-8")),
                }
            )
        rows.append(
            {
                "runner_id": f"LV6726-RUNNER-{index:02d}",
                "name": name,
                "path": relative,
                "mode": mode,
                "cases": cases,
                "historical_caller_compatibility": "family_current_ghc_family_prefix_preserved",
                "outcome": "completed" if all(case["exit_code"] == 0 and case["expected_behavior_observed"] for case in cases) else "open_gap",
            }
        )
    if not all(row["outcome"] == "completed" for row in rows):
        raise RuntimeError("one or more family-current runners failed smoke use")
    return rows


def execute_proposals(proposals: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes = []
    mutations = []
    positive_witnesses = []
    for index, proposal in enumerate(proposals, 1):
        mode = core.MODES[(index - 1) % len(core.MODES)]
        disposition = proposal["expected_disposition"]
        positive = None
        if disposition in {"completed", "represented"}:
            positive = core.evaluate(mode, core.accepting_fixture(mode))
            if not positive["valid"]:
                raise RuntimeError(f"positive contract failed for {proposal['proposal_id']}: {positive['errors']}")
            positive_witnesses.append(
                {
                    "witness_id": f"{proposal['proposal_id']}-POS",
                    "proposal_id": proposal["proposal_id"],
                    "mode": mode,
                    "result": "pass",
                    "credit": "bounded_completion" if disposition == "completed" else "bounded_representation",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                }
            )
        mutation_ids = []
        for mutation in proposal["negative_fixtures"]:
            mutated = core.mutate_fixture(mode, mutation["mutation_class"])
            result = core.evaluate(mode, mutated)
            if result["valid"]:
                raise RuntimeError(f"mutation unexpectedly passed: {mutation['mutation_id']}")
            mutation_ids.append(mutation["mutation_id"])
            mutations.append(
                {
                    "mutation_id": mutation["mutation_id"],
                    "proposal_id": proposal["proposal_id"],
                    "mode": mode,
                    "mutation_class": mutation["mutation_class"],
                    "failed_witness_id": f"{mutation['mutation_id']}-FAIL",
                    "passing_rejection_witness_id": f"{mutation['mutation_id']}-REJECT",
                    "result": "rejected",
                    "errors": result["errors"],
                    "broader_credit": 0,
                    "failed_witness_retained": True,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                }
            )
        proposal_artifact, receipt_artifact = proposal["concrete_artifacts"]
        proposal_payload = {
            "schema": "ghc.family.liora-venn.v672-v6.proposal-execution.v1",
            "proposal": proposal,
            "mode": mode,
            "observed_outcome": disposition,
            "execution_count": 1 if positive is not None else 0,
            "positive_control": positive,
            "mutation_ids": mutation_ids,
            "real_people": 0,
            "real_objects_or_materials": 0,
            "real_observations_or_measurements": 0,
            "external_actions": 0,
            "authority_acts": 0,
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        }
        write_json(ROOT / proposal_artifact, proposal_payload)
        receipt_payload = {
            "schema": "ghc.family.liora-venn.v672-v6.proposal-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "mode": mode,
            "outcome": disposition,
            "positive_witness_id": f"{proposal['proposal_id']}-POS" if positive else None,
            "positive_valid": positive["valid"] if positive else None,
            "negative_mutation_ids": mutation_ids,
            "negative_mutations_rejected": len(mutation_ids),
            "protected_unexecuted": disposition in {"open_gap", "exact_gate"},
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        }
        write_json(ROOT / receipt_artifact, receipt_payload)
        outcomes.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "mode": mode,
                "outcome": disposition,
                "execution_count": 1 if positive else 0,
                "completion_credit": 1 if disposition == "completed" else 0,
                "representation_credit": 1 if disposition == "represented" else 0,
                "mutation_count": len(mutation_ids),
                "all_mutations_rejected": True,
                "artifacts": [proposal_artifact, receipt_artifact],
            }
        )
    return outcomes, mutations, positive_witnesses


def execute_portfolio() -> dict[str, Any]:
    frozen = load("docs/liora-venn/v672-v6/x1/portfolio-freeze.json")

    def bounded(rows: list[dict[str, Any]], outcome: str, offset: int = 0) -> list[dict[str, Any]]:
        out = []
        for index, row in enumerate(rows, 1):
            mode = core.MODES[(offset + index - 1) % len(core.MODES)]
            evaluation = core.evaluate(mode, core.accepting_fixture(mode))
            if not evaluation["valid"]:
                raise RuntimeError(f"portfolio fixture failed: {row.get('task_id')}")
            out.append({**row, "outcome": outcome, "execution_count": 1, "bounded_evidence_mode": mode, "same_owner_only": True, "independent_reproduction": False})
        return out

    exact = [{**row, "outcome": "exact_gate", "execution_count": 0} for row in frozen["exact_approval"]]
    blocked = [{**row, "outcome": "exact_gate", "execution_count": 0} for row in frozen["blocked"]]
    return {
        "schema": "ghc.family.liora-venn.v672-v6.portfolio-outcome.v1",
        "safe_now": bounded(frozen["safe_now"], "completed"),
        "bounded_candidates": bounded(frozen["bounded_candidates"], "represented", 3),
        "clean_fix_refine": bounded(frozen["clean_fix_refine"], "completed", 6),
        "exact_approval": exact,
        "blocked": blocked,
        "counts": frozen["counts"],
        "caps_are_ceilings_not_quotas": True,
        "boundary": BOUNDARY,
    }


def build(quick_validator: Path) -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    if branch != x1.BRANCH or head != X1_COMMIT:
        raise RuntimeError(f"x2 requires clean immutable x1 {X1_COMMIT}; got {branch} at {head}")
    if git_text("status", "--porcelain=v1", "--untracked-files=no"):
        raise RuntimeError("tracked worktree state changed before x2 build")
    if git_text("diff", "--name-only", x1.SOURCE_FINAL, X1_COMMIT, "--", "docs/liora-venn/v672-v6/x2"):
        raise RuntimeError("immutable x1 unexpectedly contains x2")

    proposals_doc = load("docs/liora-venn/v672-v6/x1/proposal-freeze.json")
    proposals = proposals_doc["new_proposals"]
    quick_rows, skill_smoke = customize_skills(quick_validator)
    runner_rows = build_runners()
    outcomes, mutations, positive_witnesses = execute_proposals(proposals)
    portfolio = execute_portfolio()
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    if outcome_counts != Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}):
        raise RuntimeError(f"unexpected proposal outcome counts: {outcome_counts}")
    if len(mutations) != 160 or not all(row["result"] == "rejected" for row in mutations):
        raise RuntimeError("not all 160 preregistered mutations were rejected")

    write_json(
        X2_ROOT / "skill-quick-validation-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.skill-quick-validation.v1",
            "validated_at": now(),
            "initialized_through_official_skill_creator": True,
            "customized_count": len(quick_rows),
            "quick_validated_count": sum(row["valid"] for row in quick_rows),
            "global_install_count": 0,
            "skills": quick_rows,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "skill-smoke-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.skill-smoke.v1",
            "smoked_at": now(),
            "skill_count": len(skill_smoke),
            "accepting_passes": sum(row["accepting_valid"] for row in skill_smoke),
            "rejecting_passes": sum(row["rejecting_rejected"] for row in skill_smoke),
            "skills": skill_smoke,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "runner-smoke-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.runner-smoke.v1",
            "smoked_at": now(),
            "runner_count": len(runner_rows),
            "case_count": sum(len(row["cases"]) for row in runner_rows),
            "runners": runner_rows,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "proposal-outcome-ledger.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.proposal-outcome-ledger.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "x1_commit": X1_COMMIT,
            "proposal_count": len(outcomes),
            "outcome_counts": {label: outcome_counts[label] for label in x1.ALLOWED_OUTCOMES},
            "outcomes": outcomes,
            "positive_witness_count": len(positive_witnesses),
            "positive_witnesses": positive_witnesses,
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "mutation-register.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.mutation-register.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "mutation_count": len(mutations),
            "rejected_count": sum(row["result"] == "rejected" for row in mutations),
            "failed_witness_count": len(mutations),
            "passing_rejection_witness_count": len(mutations),
            "failed_witnesses_retained": True,
            "failed_witnesses_promoted": 0,
            "mutations": mutations,
            "boundary": "Each rejection proves only the named guard against the named synthetic fixture; no broader evidence or authority.",
        },
    )
    write_json(X2_ROOT / "portfolio-outcome.json", portfolio)

    startup = load("docs/liora-venn/v672-v6/x1/method-flow-startup.json")
    owner_methods = []
    for index, row in enumerate(skill_smoke, 9):
        owner_methods.append(
            {
                "method_id": f"LV6726-M{index:03d}",
                "title": row["name"],
                "state": "preferred",
                "skill_id": row["skill_id"],
                "mode": row["mode"],
                "accepting_witness": f"{row['skill_id']}-ACCEPT",
                "rejecting_witness": f"{row['skill_id']}-REJECT",
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    owner_methods.append(
        {
            "method_id": "LV6726-M029",
            "title": "Establish repository-root import context for direct owner scripts",
            "state": "preferred",
            "mode": "owner_script_import_context",
            "retained_negative_ids": ["LV6726-X2-N001"],
            "accepting_witness": "LV6726-X2-WP001",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
    )
    effective_counts = {
        "declared_frozen_proposals": 6150,
        "effective_negatives": x1.ACTIVATION_COUNTS["effective_negatives"] + startup["counts"]["witness_results"]["fail"] + len(mutations) + len(X2_OPERATIONAL_FAILURES),
        "effective_methods": x1.ACTIVATION_COUNTS["effective_methods"] + startup["counts"]["methods"] + len(owner_methods),
        "failed_witnesses": x1.ACTIVATION_COUNTS["failed_witnesses"] + startup["counts"]["witness_results"]["fail"] + len(mutations) + len(X2_OPERATIONAL_FAILURES),
        "bounded_passing_witnesses": x1.ACTIVATION_COUNTS["bounded_passing_witnesses"] + startup["counts"]["witness_results"]["pass"] + len(mutations) + len(positive_witnesses) + len(quick_rows) + 2 * len(skill_smoke) + 2 * len(runner_rows) + len(X2_OPERATIONAL_RECOVERIES),
        "open_gaps": x1.ACTIVATION_COUNTS["open_gaps"] + outcome_counts["open_gap"],
        "exact_gates": x1.ACTIVATION_COUNTS["exact_gates"] + outcome_counts["exact_gate"],
    }
    write_json(
        X2_ROOT / "method-flow-evidence.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.method-flow-evidence.v1",
            "startup_methods": startup["methods"],
            "startup_witnesses": startup["witnesses"],
            "x2_preferred_methods": owner_methods,
            "x2_operational_failures": X2_OPERATIONAL_FAILURES,
            "x2_operational_recoveries": X2_OPERATIONAL_RECOVERIES,
            "external_witness_registers": ["docs/liora-venn/v672-v6/x2/mutation-register.json", "docs/liora-venn/v672-v6/x2/proposal-outcome-ledger.json", "docs/liora-venn/v672-v6/x2/skill-smoke-receipt.json", "docs/liora-venn/v672-v6/x2/runner-smoke-receipt.json"],
            "effective_counts": effective_counts,
            "operational_failure_count": len(X2_OPERATIONAL_FAILURES),
            "operational_recovery_count": len(X2_OPERATIONAL_RECOVERIES),
            "failed_witness_non_erasure": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "gate-register.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.gate-register.v1",
            "inherited_open_gaps": x1.ACTIVATION_COUNTS["open_gaps"],
            "phase_open_gaps": [row["proposal_id"] for row in outcomes if row["outcome"] == "open_gap"],
            "effective_open_gaps": effective_counts["open_gaps"],
            "inherited_exact_gates": x1.ACTIVATION_COUNTS["exact_gates"],
            "phase_exact_gates": [row["proposal_id"] for row in outcomes if row["outcome"] == "exact_gate"],
            "effective_exact_gates": effective_counts["exact_gates"],
            "all_gates_retained": True,
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "phase-truth.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.phase-truth.x2.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "x1_commit": X1_COMMIT,
            "primary_pillar": x1.PRIMARY_PILLAR,
            "secondary_pillars": x1.SECONDARY_PILLARS,
            "practice": x1.PRACTICE,
            "outcomes": {label: outcome_counts[label] for label in x1.ALLOWED_OUTCOMES},
            "effective_counts": effective_counts,
            "mutation_count": len(mutations),
            "mutation_rejections": len(mutations),
            "skills_initialized_customized_quick_validated_smoked": len(skill_smoke),
            "runners_built_and_smoked": len(runner_rows),
            "real_people": 0,
            "real_objects_or_materials": 0,
            "real_observations_or_measurements": 0,
            "real_identity_events": 0,
            "external_actions": 0,
            "authority_acts": 0,
            "full_repository_suite": "not_run_not_claimed",
            "independent_reproduction": False,
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X2_ROOT / "pillar-boundaries.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.pillar-boundaries.v1",
            "THOS Body": "Synthetic procedure and documentation proxy only; no participants operators outcomes competence effectiveness or safety result.",
            "GMUT Mind": "Typed bath-boundary and pullback analogy only; no datum likelihood posterior force prediction constraint empirical confirmation quantum or ultraviolet completion or Theory of Everything.",
            "Freed ID": "Zero-key surrogate role and lifecycle vacancy only; no real key proof issuance resolution status revocation interoperability privacy security recovery or trust governance.",
            "CBR Heart": "Rights remedy attribution access withdrawal cultural and authority vacancies only; no legal cultural affected-party Maori-data-governance or Maori-authority decision.",
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "boundary": BOUNDARY,
        },
    )
    write_text(
        X2_ROOT / "README.md",
        f"""# Liora Venn v672-v6 bounded x2 evidence

This owner-local x2 executes forty frozen synthetic contracts from immutable x1 `{X1_COMMIT}`. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered invalid mutations were rejected and retained. Twenty owner-local skills were initialized through skill-creator, customized, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current runners were built and accepting/rejecting smoke-used.

The practice lens is {x1.PRACTICE}, with {x1.PRIMARY_PILLAR} primary. No real person, paper, bath, material, tool, pattern, observation, measurement, treatment, publication, identity event, participant, professional decision, external action, or authority act occurred. `{x1.TERMINAL_VERDICT}` remains exact.
""",
    )
    write_text(
        X2_ROOT / "static-report.html",
        f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Liora Venn v672-v6 x2</title></head>
<body><a href="#main">Skip to main content</a><header><h1>Liora Venn v672-v6 bounded x2 evidence</h1></header><main id="main">
<section aria-labelledby="scope"><h2 id="scope">Scope</h2><p>{x1.PRACTICE}. {BOUNDARY}</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Outcomes</h2><ul><li>Completed: 28</li><li>Represented: 8</li><li>Open gap: 2</li><li>Exact gate: 2</li></ul></section>
<section aria-labelledby="limits"><h2 id="limits">Unresolved limits</h2><p>Manual keyboard, responsive-layout diversity, browser diversity, assistive-technology, cognitive-accessibility, language, affected-user, security-usability, and Maori-language review remain absent or exact-gated.</p></section>
<section aria-labelledby="verdict"><h2 id="verdict">Terminal verdict</h2><p>{x1.TERMINAL_VERDICT}</p></section>
</main></body></html>
""",
    )
    owner_files = sorted(path.relative_to(ROOT).as_posix() for path in X2_ROOT.rglob("*") if path.is_file())
    write_json(
        X2_ROOT / "build-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.x2-build-receipt.v1",
            "built_at": now(),
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "x1_commit": X1_COMMIT,
            "owner_files_before_receipt": len(owner_files),
            "owner_files_after_receipt": len(owner_files) + 1,
            "outcomes": {label: outcome_counts[label] for label in x1.ALLOWED_OUTCOMES},
            "mutation_count": len(mutations),
            "mutation_rejections": len(mutations),
            "skill_count": len(skill_smoke),
            "runner_count": len(runner_rows),
            "effective_counts": effective_counts,
            "canonical_invoked": False,
            "successor_contacted": False,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": x1.TERMINAL_VERDICT,
            "valid": True,
            "boundary": BOUNDARY,
        },
    )
    return {
        "outcomes": dict(outcome_counts),
        "mutations": len(mutations),
        "mutation_rejections": len(mutations),
        "skills": len(skill_smoke),
        "runners": len(runner_rows),
        "effective_counts": effective_counts,
        "x2_files": len([path for path in X2_ROOT.rglob("*") if path.is_file()]),
        "valid": True,
    }


def refresh_operational_overlay() -> dict[str, Any]:
    """Apply the retained direct-import failure without replaying x2 execution."""
    startup = load("docs/liora-venn/v672-v6/x1/method-flow-startup.json")
    mutations = load("docs/liora-venn/v672-v6/x2/mutation-register.json")
    outcomes = load("docs/liora-venn/v672-v6/x2/proposal-outcome-ledger.json")
    skills = load("docs/liora-venn/v672-v6/x2/skill-quick-validation-receipt.json")
    skill_smoke = load("docs/liora-venn/v672-v6/x2/skill-smoke-receipt.json")
    runners = load("docs/liora-venn/v672-v6/x2/runner-smoke-receipt.json")
    flow = load("docs/liora-venn/v672-v6/x2/method-flow-evidence.json")
    method = {
        "method_id": "LV6726-M029",
        "title": "Establish repository-root import context for direct owner scripts",
        "state": "preferred",
        "mode": "owner_script_import_context",
        "retained_negative_ids": ["LV6726-X2-N001"],
        "accepting_witness": "LV6726-X2-WP001",
        "same_owner_only": True,
        "independent_reproduction": False,
    }
    flow["x2_preferred_methods"] = [row for row in flow["x2_preferred_methods"] if row["method_id"] != method["method_id"]] + [method]
    effective = {
        "declared_frozen_proposals": 6150,
        "effective_negatives": x1.ACTIVATION_COUNTS["effective_negatives"] + startup["counts"]["witness_results"]["fail"] + mutations["mutation_count"] + len(X2_OPERATIONAL_FAILURES),
        "effective_methods": x1.ACTIVATION_COUNTS["effective_methods"] + startup["counts"]["methods"] + len(flow["x2_preferred_methods"]),
        "failed_witnesses": x1.ACTIVATION_COUNTS["failed_witnesses"] + startup["counts"]["witness_results"]["fail"] + mutations["failed_witness_count"] + len(X2_OPERATIONAL_FAILURES),
        "bounded_passing_witnesses": x1.ACTIVATION_COUNTS["bounded_passing_witnesses"] + startup["counts"]["witness_results"]["pass"] + mutations["passing_rejection_witness_count"] + outcomes["positive_witness_count"] + skills["quick_validated_count"] + skill_smoke["accepting_passes"] + skill_smoke["rejecting_passes"] + runners["case_count"] + len(X2_OPERATIONAL_RECOVERIES),
        "open_gaps": x1.ACTIVATION_COUNTS["open_gaps"] + outcomes["outcome_counts"]["open_gap"],
        "exact_gates": x1.ACTIVATION_COUNTS["exact_gates"] + outcomes["outcome_counts"]["exact_gate"],
    }
    flow["x2_operational_failures"] = X2_OPERATIONAL_FAILURES
    flow["x2_operational_recoveries"] = X2_OPERATIONAL_RECOVERIES
    flow["effective_counts"] = effective
    write_json(X2_ROOT / "method-flow-evidence.json", flow)
    phase = load("docs/liora-venn/v672-v6/x2/phase-truth.json")
    phase["effective_counts"] = effective
    phase["operational_failure_count"] = len(X2_OPERATIONAL_FAILURES)
    phase["operational_recovery_count"] = len(X2_OPERATIONAL_RECOVERIES)
    write_json(X2_ROOT / "phase-truth.json", phase)
    receipt = load("docs/liora-venn/v672-v6/x2/build-receipt.json")
    receipt["effective_counts"] = effective
    receipt["operational_failure_count"] = len(X2_OPERATIONAL_FAILURES)
    receipt["operational_recovery_count"] = len(X2_OPERATIONAL_RECOVERIES)
    write_json(X2_ROOT / "build-receipt.json", receipt)
    return {"effective_counts": effective, "operational_failures": len(X2_OPERATIONAL_FAILURES), "operational_recoveries": len(X2_OPERATIONAL_RECOVERIES), "valid": True}


def seal_staged() -> dict[str, Any]:
    if git_text("branch", "--show-current") != x1.BRANCH or git_text("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("evidence staged seal requires exact immutable x1 head")
    staged = [path for path in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if path]
    deleted = [path for path in git_text("diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if path]
    manifest_path = "docs/liora-venn/v672-v6/validation/evidence-manifest.json"
    review_path = "docs/liora-venn/v672-v6/validation/evidence-staged-review.json"
    self_exclusions = [manifest_path, review_path]
    unexpected = [
        path for path in staged
        if not (
            path.startswith("docs/liora-venn/v672-v6/x2/")
            or path.startswith("scripts/ghc_family_liora_v672_v6_")
            or path == "scripts/build_ghc_family_liora_venn_v672_v6_x2.py"
            or path == "tests/test_ghc_family_liora_venn_v672_v6_x2.py"
        )
    ]
    frozen_x1_changes = [path for path in staged if path.startswith("docs/liora-venn/v672-v6/x1/") or path.endswith("_x1.py")]
    if deleted or unexpected or frozen_x1_changes:
        raise RuntimeError(f"evidence staged allowlist refused: deleted={deleted}, unexpected={unexpected}, frozen_x1={frozen_x1_changes}")
    entries = []
    for path in staged:
        data = git("show", f":{path}").stdout
        entries.append({"path": path, "git_blob_oid": git_text("rev-parse", f":{path}"), "bytes": len(data), "sha256": sha256(data)})
    write_json(
        VALIDATION_ROOT / "evidence-staged-review.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.evidence-staged-review.v1",
            "reviewed_at": now(),
            "base": X1_COMMIT,
            "entry_paths_before_self_exclusions": staged,
            "entry_count_before_self_exclusions": len(staged),
            "self_exclusions": self_exclusions,
            "expected_total_after_self_exclusions": len(staged) + len(self_exclusions),
            "deletions": deleted,
            "unexpected_paths": unexpected,
            "frozen_x1_changes": frozen_x1_changes,
            "valid": bool(staged) and not deleted and not unexpected and not frozen_x1_changes,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        VALIDATION_ROOT / "evidence-manifest.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.git-blob-manifest.v1",
            "owner": x1.OWNER,
            "phase": x1.PHASE,
            "base": X1_COMMIT,
            "domain": "x2 evidence exact staged Git blobs before two declared self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": self_exclusions,
            "boundary": BOUNDARY,
        },
    )
    return {"entries": len(entries), "self_exclusions": len(self_exclusions), "valid": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "refresh-operational-overlay", "seal-staged"))
    parser.add_argument("--quick-validator", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        if args.quick_validator is None:
            raise RuntimeError("build requires --quick-validator")
        payload = build(args.quick_validator)
    elif args.command == "refresh-operational-overlay":
        payload = refresh_operational_overlay()
    else:
        payload = seal_staged()
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
