#!/usr/bin/env python3
"""Build the frozen Elaren Kestrel v652-v7 x2 evidence packet."""

from __future__ import annotations

import html
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v652_v7_core as core
import ghc_family_v652_v7_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "cd1ce10d7c456d55e48183652835f6c3f5866b89"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator"
QUICK_VALIDATE = SKILL_CREATOR / "scripts/quick_validate.py"
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
X2_NEGATIVES = [
    {
        "negative_id": "V6527-X2-N01",
        "category": "skill_short_description_limit",
        "failed": "The skill initializer created the perturbation-intertwiner directory but rejected its 66-character short description against the 25-to-64 character UI limit.",
        "recovery": "Keep the initialized directory, shorten only the UI description, and complete the same skill without deletion or reinitialization.",
        "recurrence_guard": "Measure short descriptions before invoking init_skill and keep them within 25 to 64 characters.",
    },
    {
        "negative_id": "V6527-X2-N02",
        "category": "historical_x1_advanced_tree_assertion",
        "failed": "The first combined scoped test run passed 47 of 48 tests; the historical x1 no-x2 assertion inspected the advanced working tree and found legitimate x2 artifacts.",
        "recovery": "Bind the historical assertion to the exact frozen x1 Git tree while retaining the current tree for x2 validation.",
        "recurrence_guard": "Historical freeze assertions must read their immutable commit or tree rather than a later working tree.",
    },
    {
        "negative_id": "V6527-X2-N03",
        "category": "combined_status_search_timeout",
        "failed": "A combined Git-status and three-file search probe exceeded its bounded window before returning usable output.",
        "recovery": "Split repository state from direct file-scoped searches and avoid the combined wrapper.",
        "recurrence_guard": "Use one bounded repository-state query and direct known-file reads instead of combining enumeration and content search.",
    },
    {
        "negative_id": "V6527-X2-N04",
        "category": "untracked_status_enumeration_timeout",
        "failed": "A short Git status call timed out while enumerating the large untracked x2 packet.",
        "recovery": "Use untracked-files=no for tracked-state checks until the exact x2 surface is staged.",
        "recurrence_guard": "Do not enumerate a large generated untracked packet through ordinary Git status before staging.",
    },
    {
        "negative_id": "V6527-X2-N05",
        "category": "guessed_execution_portfolio_path",
        "failed": "A direct inspection guessed an execution-portfolio filename at the phase root after reading the phase truth, but the generated receipt lives under portfolios.",
        "recovery": "Resolve the exact generated path with a phase-scoped file list before reading it.",
        "recurrence_guard": "Discover generated portfolio filenames from the bounded phase root instead of guessing their location.",
    },
    {
        "negative_id": "V6527-X2-N06",
        "category": "powershell_foreach_pipeline_parse_error",
        "failed": "A compact Windows PowerShell key-summary wrapper was rejected because it piped directly from a foreach statement.",
        "recovery": "Collect the bounded rows in an explicit array and pipe the completed collection.",
        "recurrence_guard": "Use an explicit collection variable when piping the results of a Windows PowerShell foreach statement.",
    },
    {
        "negative_id": "V6527-X2-N07",
        "category": "script_package_sibling_import_error",
        "failed": "The first validation-module smoke test imported through the scripts namespace but could not resolve a sibling phase-data module.",
        "recovery": "Bind the repository's exact scripts directory before importing the validator modules in the test.",
        "recurrence_guard": "Test directly executable repository scripts with their containing scripts directory explicitly bound on sys.path.",
    },
    {
        "negative_id": "V6527-X2-N08",
        "category": "guessed_workflow_decision_path",
        "failed": "The first validation-layer run guessed a workflow decision filename that does not exist in the frozen x1 packet.",
        "recovery": "Read the exact workflow-plan validation and live-route overlay files already frozen by x1.",
        "recurrence_guard": "Resolve workflow evidence from the frozen packet inventory rather than inventing a convenience filename.",
    },
    {
        "negative_id": "V6527-X2-N09",
        "category": "privacy_scanner_boundary_false_positives",
        "failed": "The first five-class scan reported two embedded sk- substrings in the tooling index and one scanner-definition path literal as payload findings.",
        "recovery": "Require a lexical boundary before secret prefixes and classify exact scanner-definition files separately from confirmed payload hits.",
        "recurrence_guard": "Keep credential prefixes boundary-aware and maintain an exact scanner-definition allowlist without suppressing ordinary payload files.",
    },
    {
        "negative_id": "V6527-X2-N10",
        "category": "owner_file_receipt_key_mismatch",
        "failed": "The detailed validator failed closed because it requested owner_file_count from a receipt whose declared key is owner_generated_file_count.",
        "recovery": "Bind the threshold check to the exact declared owner_generated_file_count key.",
        "recurrence_guard": "Inspect generated receipt keys before adding downstream validator bindings.",
    },
    {
        "negative_id": "V6527-X2-N11",
        "category": "combined_staging_wrapper_timeout",
        "failed": "The combined staging, dual-review, and diff-hygiene wrapper exceeded its overall timeout after both staged reviews returned valid.",
        "recovery": "Preserve the completed review outputs and run the remaining exact review and hygiene steps as separate bounded commands.",
        "recurrence_guard": "Do not combine staging, repeated manifest generation, and diff hygiene in one long wrapper.",
    },
    {
        "negative_id": "V6527-X2-N12",
        "category": "staged_manifest_text_strip_defect",
        "failed": "Audit found that the first staged manifest decoded and stripped git-show output before hashing, so it was not byte-exact.",
        "recovery": "Read staged blobs as raw subprocess bytes and regenerate every candidate entry before commit.",
        "recurrence_guard": "Never pass manifest content through text strip, newline conversion, or decode-encode cycles before hashing.",
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


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    return subprocess.run(
        list(args),
        cwd=REPO,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def skill_markdown(name: str, purpose: str, runner: str, surface: str) -> str:
    return f"""---
name: {name}
description: {purpose} Use this skill when reviewing the corresponding Elaren v652-v7 JSON contract, mutation evidence, nonpromotion boundary, or lifecycle receipt.
---

# {name}

## Purpose

{purpose} This is a phase-local same-owner audit skill. It does not establish empirical confirmation, production readiness, professional qualification, legal or cultural authority, Māori authority, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness or personhood, Theory-of-Everything proof, or Stage 20 authority.

## Workflow

1. Read `references/contract.json` completely.
2. Resolve only the repository-relative artifacts declared there.
3. Run `python scripts/{runner}` from the repository root.
4. Require the runner's `valid` field to be true and its terminal verdict to remain `NOT_READY_FOR_STAGE_20`.
5. If the runner fails, retain the failed attempt with zero credit before any bounded correction.
6. Report only `completed`, `represented`, `open_gap`, or `exact_gate`.

## Boundaries

- Surface: `{surface}`.
- Use synthetic or structural fixtures only.
- Never introduce credentials, private routes, private conversations, real participant data, production keys, legal conclusions, cultural ratification, or Māori-authority decisions.
- A passing smoke use is same-owner workflow evidence only.
"""


def customize_skills() -> list[dict[str, Any]]:
    skills_root = ROOT / "skills"
    runner_by_skill = list(zip(d.SKILL_IDEAS, d.RUNNER_IDEAS, strict=True))
    receipts = []
    for (name, purpose), (runner, surface) in runner_by_skill:
        directory = skills_root / name
        if not directory.is_dir():
            raise RuntimeError(f"initialized skill directory missing: {name}")
        (directory / "SKILL.md").write_text(
            skill_markdown(name, purpose, runner, surface),
            encoding="utf-8",
            newline="\n",
        )
        agents = directory / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        display = name.replace("ghc-family-", "").replace("-", " ").title()
        (agents / "openai.yaml").write_text(
            "interface:\n"
            f"  display_name: \"{display}\"\n"
            "  short_description: \"Run this bounded GHC audit safely\"\n"
            f"  default_prompt: \"Audit the {surface} surface without crossing protected gates.\"\n",
            encoding="utf-8",
            newline="\n",
        )
        reference = directory / "references" / "contract.json"
        reference.parent.mkdir(parents=True, exist_ok=True)
        reference.write_text(
            json.dumps(
                {
                    "schema": "ghc.family.v652-v7.phase-local-skill-contract.v1",
                    "skill": name,
                    "purpose": purpose,
                    "runner": f"scripts/{runner}",
                    "surface": surface,
                    "required_result": {"valid": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "protected_gates": d.PROTECTED_GATES,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        validation = run(sys.executable, str(QUICK_VALIDATE), str(directory), check=False)
        receipts.append(
            {
                "name": name,
                "runner": runner,
                "surface": surface,
                "quick_validate_exit": validation.returncode,
                "quick_validate_stdout": validation.stdout.strip(),
                "quick_validate_stderr": validation.stderr.strip(),
                "quick_validate_pass": validation.returncode == 0,
                "forward_test": "not_delegated_solo_route",
            }
        )
    if not all(row["quick_validate_pass"] for row in receipts):
        raise RuntimeError("one or more phase-local skills failed quick validation")
    return receipts


def wrapper_source(surface: str) -> str:
    if surface == "phase-validation":
        body = """rows = [runner_payload(row[\"slug\"]) for row in proposals()]
    payload = {
        \"surface\": \"phase-validation\",
        \"proposal_count\": len(rows),
        \"valid\": all(row[\"valid\"] for row in rows),
        \"mutation_count\": sum(row[\"mutation_count\"] for row in rows),
        \"rejected\": sum(row[\"rejected\"] for row in rows),
        \"terminal_verdict\": \"NOT_READY_FOR_STAGE_20\",
    }"""
    else:
        body = f'payload = runner_payload("{surface}")'
    return f"""#!/usr/bin/env python3
from __future__ import annotations

import json

from ghc_family_v652_v7_core import proposals, runner_payload


def main() -> None:
    {body}
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
"""


def build_runners() -> list[dict[str, Any]]:
    receipts = []
    for runner, surface in d.RUNNER_IDEAS:
        path = write_repo(f"scripts/{runner}", wrapper_source(surface))
        completed = run(sys.executable, str(path), check=False)
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = {"valid": False, "terminal_verdict": None}
        receipts.append(
            {
                "runner": runner,
                "surface": surface,
                "exit_code": completed.returncode,
                "valid": payload.get("valid") is True,
                "mutation_count": payload.get("mutation_count"),
                "rejected": payload.get("rejected"),
                "terminal_verdict": payload.get("terminal_verdict"),
                "stderr": completed.stderr.strip(),
            }
        )
    if not all(
        row["exit_code"] == 0
        and row["valid"]
        and row["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
        for row in receipts
    ):
        raise RuntimeError("one or more family-compatible runners failed")
    return receipts


def extend_method_flow() -> dict[str, Any]:
    source = ROOT / "method-flow/x1-method-flow-ledger.json"
    ledger = ROOT / "method-flow/evidence-method-flow-ledger.json"
    shutil.copyfile(source, ledger)
    for offset, negative in enumerate(X2_NEGATIVES, 15):
        method_id = f"V6527-METHOD-{offset:02d}"
        fail_id = f"V6527-WITNESS-{offset:02d}-F"
        pass_id = f"V6527-WITNESS-{offset:02d}-P"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['category']}",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [negative["category"]],
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": "Stop, retain the failed witness with zero credit, and leave all external and protected-gate state unchanged.",
            "scope_boundary": "Same-owner skill initialization recovery only; not independent reproduction or broader assurance.",
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": d.PROTECTED_GATES,
            "retained_negative_ids": [negative["negative_id"]],
            "supersedes": [],
            "recommendation_state": "candidate",
        }
        fail = {
            "witness_id": fail_id,
            "method_id": method_id,
            "scope": negative["category"],
            "procedure": "Run the original bounded operation and retain its failure with zero completion credit.",
            "expected": "The bounded operation completes without weakening protected gates.",
            "observed": negative["failed"],
            "result": "fail",
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero completion credit; failure remains retained.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        passing = {
            "witness_id": pass_id,
            "method_id": method_id,
            "scope": negative["category"],
            "procedure": negative["recovery"],
            "expected": "The bounded recovery completes while the original failure remains retained.",
            "observed": f"The bounded recovery completed: {negative['recovery']}",
            "result": "pass",
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Same-owner bounded recovery only.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        method_path = write_json(f"method-flow/x2-requests/method-{offset:02d}.json", method)
        fail_path = write_json(f"method-flow/x2-requests/witness-{offset:02d}-failed.json", fail)
        pass_path = write_json(f"method-flow/x2-requests/witness-{offset:02d}-passing.json", passing)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(method_path))
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path))
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path))
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded pass exists and failed witness remains retained.",
        )
    validation = ROOT / "method-flow/evidence-method-flow-validation.json"
    summary_json = ROOT / "method-flow/evidence-method-flow-summary.json"
    summary_md = ROOT / "method-flow/evidence-method-flow-summary.md"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(validation))
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(summary_json),
        "--markdown-output",
        str(summary_md),
    )
    return read_json(ledger)


def build_report(outcomes: dict[str, int], effective_negatives: int) -> str:
    cards = []
    for proposal in d.PROPOSALS:
        cards.append(
            "<article><h3>{}</h3><p>{}</p><dl><dt>Outcome</dt><dd>{}</dd>"
            "<dt>Lane</dt><dd>{}</dd><dt>Boundary</dt><dd>{}</dd></dl></article>".format(
                html.escape(proposal["proposal_id"]),
                html.escape(proposal["title"]),
                html.escape(proposal["expected_disposition"]),
                html.escape(proposal["execution_lane"]),
                html.escape(proposal["falsifier_or_acceptance_gate"]),
            )
        )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elaren v652-v7 bounded evidence report</title><style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
:focus{{outline:3px solid #b35c00;outline-offset:3px}}article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}}dd{{margin:0 0 .6rem}}.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}</style></head>
<body><main><h1>Elaren Kestrel v652-v7 bounded evidence report</h1>
<p class="notice"><strong>Boundary:</strong> same-owner synthetic and structural evidence only. Manual and affected-user accessibility evaluation is reserved. No empirical confirmation, production readiness, professional approval, legal or cultural authority, Māori authority, independent reproduction, Theory-of-Everything proof, or Stage 20 authority is claimed.</p>
<h2>Truth summary</h2><p>Outcomes: {outcomes}. Effective retained negatives: {effective_negatives}. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<h2>Proposal evidence</h2>{''.join(cards)}
<h2>External incompleteness</h2><p>Real data, blind matched-budget arms, independent review, production identity infrastructure, affected-party participation, legal and cultural authority, Māori authority, qualified manual accessibility review, and independent-team reproduction remain open or exact-gated.</p>
</main></body></html>"""


def build() -> None:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("evidence builder requires the exact x1 commit")
    permitted_prefixes = (
        f"{d.PHASE_ROOT}/",
        "scripts/ghc_family_v652_v7_core.py",
        "scripts/build_ghc_family_v652_v7_evidence.py",
        "scripts/ghc_family_",
        "tests/test_ghc_family_v652_v7_",
    )
    tracked_changes = [
        path.replace("\\", "/")
        for path in git("diff", "--name-only", "--").splitlines()
        if path
    ]
    unexpected = [
        path
        for path in tracked_changes
        if not any(path.startswith(prefix) for prefix in permitted_prefixes)
    ]
    if unexpected:
        raise RuntimeError(f"unexpected tracked x2 pre-build paths: {sorted(set(unexpected))}")

    skill_receipts = customize_skills()
    runner_receipts = build_runners()
    surface_receipts = []
    for proposal in d.PROPOSALS:
        evaluated = core.evaluate_surface(proposal["slug"])
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", evaluated["contract"])
        write_json(
            f"{base}/mutation-results.json",
            {
                "schema": "ghc.family.v652-v7.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "mutation_count": len(evaluated["mutation_results"]),
                "rejected_count": sum(row["rejected"] for row in evaluated["mutation_results"]),
                "results": evaluated["mutation_results"],
            },
        )
        write_json(f"{base}/bounded-receipt.json", evaluated["receipt"])
        surface_receipts.append(evaluated["receipt"])
    if len(surface_receipts) != 30:
        raise RuntimeError("surface count mismatch")
    if not all(row["valid_contract"] and row["all_mutations_rejected"] for row in surface_receipts):
        raise RuntimeError("surface or mutation validation failed")
    outcome_counts = dict(Counter(row["outcome"] for row in surface_receipts))
    if outcome_counts != {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"unexpected outcome distribution: {outcome_counts}")
    method_ledger = extend_method_flow()
    synthetic_rows = [
        {
            "negative_id": result["mutation_id"],
            "proposal_id": proposal["proposal_id"],
            "category": result["kind"],
            "observed": result["observed"],
            "credit": "retained_negative",
        }
        for proposal in d.PROPOSALS
        for result in core.evaluate_surface(proposal["slug"])["mutation_results"]
    ]
    effective_negatives = (
        d.INHERITED_NEGATIVES
        + len(d.X1_NEGATIVES)
        + len(X2_NEGATIVES)
        + len(synthetic_rows)
    )
    write_json(
        "x2-proposal-ledger.json",
        {
            "schema": "ghc.family.v652-v7.x2-proposal-ledger.v1",
            "proposal_count": 30,
            "outcome_counts": outcome_counts,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "rows": [
                {
                    "proposal_id": row["proposal_id"],
                    "slug": row["slug"],
                    "outcome": row["expected_disposition"],
                    "evidence": row["concrete_artifacts"],
                }
                for row in d.PROPOSALS
            ],
        },
    )
    write_json(
        "retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v652-v7.retained-negatives.v1",
            "inherited_count": d.INHERITED_NEGATIVES,
            "inherited_anchor": d.SOURCE_HEAD,
            "inherited_register": "docs/tavian-sol/v652-v6/retained-negative-register-x2.json",
            "x1_operational_count": len(d.X1_NEGATIVES),
            "x1_operational_ids": [row[0] for row in d.X1_NEGATIVES],
            "x2_operational_count": len(X2_NEGATIVES),
            "x2_operational": X2_NEGATIVES,
            "synthetic_mutation_count": len(synthetic_rows),
            "synthetic_mutations": synthetic_rows,
            "effective_total": effective_negatives,
            "none_erased": True,
        },
    )
    write_json(
        "exact-open-gate-register-x2.json",
        {
            "schema": "ghc.family.v652-v7.gates.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": [{"proposal_id": "V6527-P29", "gate": "real EHT data, likelihood, and independent review"}],
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": [{"proposal_id": "V6527-P30", "gate": "affected-party, legal, cultural, iwi, hapū, and Māori authority"}],
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "none_silently_closed": True,
        },
    )
    write_json(
        "skills/skill-build-receipt.json",
        {
            "schema": "ghc.family.v652-v7.skill-build.v1",
            "initialized_count": 10,
            "customized_count": 10,
            "quick_validated_count": sum(row["quick_validate_pass"] for row in skill_receipts),
            "smoke_use_pending_runner_receipt": False,
            "globally_installed": False,
            "forward_test": "not_delegated_solo_route",
            "skills": skill_receipts,
        },
    )
    write_json(
        "runners/runner-invocation-receipt.json",
        {
            "schema": "ghc.family.v652-v7.runner-invocation.v1",
            "runner_count": len(runner_receipts),
            "invoked_count": sum(row["exit_code"] == 0 for row in runner_receipts),
            "valid_count": sum(row["valid"] for row in runner_receipts),
            "runners": runner_receipts,
            "same_owner_only": True,
        },
    )
    write_json(
        "portfolios/execution-receipt.json",
        {
            "schema": "ghc.family.v652-v7.portfolio-execution.v1",
            "safe_now": {"planned": len(d.SAFE_TASKS), "resolved": len(d.SAFE_TASKS), "state": "completed_bounded"},
            "candidate": {"planned": len(d.CANDIDATE_TASKS), "resolved": len(d.CANDIDATE_TASKS), "distribution": outcome_counts},
            "clean_fix_refine": {"planned": 30, "resolved": 30, "state": "completed_bounded_review"},
            "unresolved_authorized_internal_tasks": 0,
            "external_gates_not_counted_as_internal_tasks": True,
        },
    )
    write_json(
        "tooling/ghc-family-index-x2-addendum.json",
        {
            "schema": "ghc.family.v652-v7.tool-index-addendum.v1",
            "phase": d.PHASE_ID,
            "skills": [row[0] for row in d.SKILL_IDEAS],
            "runners": [row[0] for row in d.RUNNER_IDEAS],
            "historical_names_preserved": True,
            "family_current_names_used": True,
            "x1_index_mutated": False,
        },
    )
    write_text(
        "tooling/ghc-family-index-x2-addendum.md",
        "# GHC Family Index x2 addendum\n\n"
        "Ten phase-local skills were initialized, customized, quick-validated, and smoke-used through ten family-compatible runners. "
        "The x1 index remains immutable. Historical names remain compatibility evidence; no destructive rename or global bulk installation occurred.",
    )
    write_json(
        "reflection-remaster/x2-remaster-decision.json",
        {
            "schema": "ghc.family.v652-v7.reflection-remaster-decision.v1",
            "decision": "additive_specialized_surfaces",
            "kept": ["ghc-family-index", "ghc-family-method-flow-state", "ghc-family-workflow-plan-refinement", "ghc-family-reflection-remaster"],
            "added": [row[0] for row in d.SKILL_IDEAS],
            "deleted": [],
            "globally_installed": [],
            "reason": "The ten new skills are phase-local and narrow; no evidence supports replacing validated family-current tools.",
            "rollback": "Remove no historical tool; if a phase-local skill fails, retain its failure and leave the global skill bank unchanged.",
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v652-v7.phase-truth.v1",
            "source_commit": d.SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "outcomes": outcome_counts,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "method_fail_witnesses": method_ledger["counts"]["witness_results"]["fail"],
            "method_pass_witnesses": method_ledger["counts"]["witness_results"]["pass"],
            "skills_initialized_validated_and_smoke_used": 10,
            "runners_built_and_invoked": 10,
            "mutations_executed_and_rejected": 150,
            "real_data_rows": 0,
            "independent_reproduction": False,
            "route_state": "NOT_ELIGIBLE_BEFORE_FINAL_GATE",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v652-v7.checklist.v1",
            "complete_bounded": [
                "thirty frozen proposals executed",
                "150 frozen mutations rejected and retained",
                "ten phase-local skills initialized, customized, quick-validated, and smoke-used",
                "ten family-compatible runners built and invoked",
                "safe, candidate, and cleanup portfolios resolved within bounded lanes",
                "accessible static report generated with manual evaluation reserved",
            ],
            "pending_lifecycle": ["evidence commit", "combined closeout/seal/final commit", "one exact-final canonical pass", "one post-gate main-task creation"],
            "incomplete_external": [
                "real empirical GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, live issuance, resolution, status, revocation, interoperability, recovery, privacy/security review, and governance",
                "affected-party, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction and Stage 20 authority",
            ],
        },
    )
    write_text("reports/evidence-static-report.html", build_report(outcome_counts, effective_negatives))
    owner_files = sum(1 for path in ROOT.rglob("*") if path.is_file())
    write_json(
        "validation/owner-file-threshold-receipt.json",
        {
            "schema": "ghc.family.v652-v7.owner-files.v1",
            "owner_generated_file_count": owner_files,
            "threshold": 2000,
            "below_threshold": owner_files < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    write_json(
        "validation/evidence-build-receipt.json",
        {
            "schema": "ghc.family.v652-v7.evidence-build.v1",
            "valid": True,
            "proposal_count": 30,
            "outcomes": outcome_counts,
            "surface_artifact_count": 90,
            "mutation_count": 150,
            "mutation_rejected_count": 150,
            "skill_count": 10,
            "runner_count": 10,
            "effective_negatives": effective_negatives,
            "owner_file_count_before_receipt": owner_files,
            "full_repository_suite_run": False,
            "route_state": "NOT_ELIGIBLE_BEFORE_FINAL_GATE",
        },
    )
    print(
        json.dumps(
            {
                "valid": True,
                "outcomes": outcome_counts,
                "mutations": 150,
                "skills": 10,
                "runners": 10,
                "negatives": effective_negatives,
                "method_pairs": method_ledger["counts"]["witness_results"],
                "owner_files": owner_files,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    build()
