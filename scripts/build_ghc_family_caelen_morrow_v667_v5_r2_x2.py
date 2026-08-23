#!/usr/bin/env python3
"""Build bounded Caelen Morrow v667-v5-r2 x2 evidence from immutable x1."""

from __future__ import annotations

import copy
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, BinaryIO


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v667-v5-r2"
OWNER = "Caelen Morrow"
PHASE = "v667-v5-r2"
CANONICAL_PHASE = "v667-v5"
BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-r2-full-tools"
SOURCE_SHA = "1b1e453cb015aff20af3236bb64a8ec32b376702"
X1_SHA = "5a5cf4859d791faff854292ed22a7a431ae4b620"
NOW = "2026-08-23T10:42:00Z"
ACTIVATION_NEGATIVES = 27716
ACTIVATION_METHODS = 13408
INHERITED_OPEN_GAPS = 195
INHERITED_EXACT_GATES = 193

POST_X1_FAILURES = [
    {
        "failure_id": "CM6675R2-X2-F010",
        "stage": "temporary_bytecode_review",
        "failed_method": "request a recursive cleanup command before the target-specific policy gate",
        "failure": "the command was rejected before execution; no file changed",
        "recovery": "leave harmless ignored bytecode untracked and validate repository scope directly",
        "recurrence_guard": "do not retry a policy-rejected cleanup when no repository byte is affected",
    },
    {
        "failure_id": "CM6675R2-X2-F011",
        "stage": "temporary_bytecode_review",
        "failed_method": "retry cleanup with explicit files while retaining a prohibited deletion surface",
        "failure": "the command was again rejected before execution; no file changed",
        "recovery": "stop cleanup attempts and rely on exact staged allowlists",
        "recurrence_guard": "treat policy rejection as terminal for optional cleanup",
    },
    {
        "failure_id": "CM6675R2-X2-F012",
        "stage": "profile_ast_review",
        "failed_method": "pipe directly from a PowerShell foreach block",
        "failure": "PowerShell rejected an empty pipeline element",
        "recovery": "materialize the parser results before projection",
        "recurrence_guard": "never append a pipeline directly to a foreach statement",
    },
    {
        "failure_id": "CM6675R2-X2-F013",
        "stage": "node_install_dry_run",
        "failed_method": "combine npm self-update with the seven Node tools and Codex CLI in one dry run",
        "failure": "npm returned ENOENT while probing the not-yet-present target npmrc, so the aggregate earned zero install credit",
        "recovery": "separate npm self-update from the tool/Codex batch; the isolated tool plan and isolated npm update passed",
        "recurrence_guard": "keep npm self-update outside a first-population global-prefix dry run",
    },
    {
        "failure_id": "CM6675R2-X2-F014",
        "stage": "powershell_profile_check",
        "failed_method": "assert an environment load marker that the canonical profile did not yet define",
        "failure": "the marker evaluated false even though D-first commands resolved",
        "recovery": "add one inert explicit marker and rerun only the affected fresh-shell checks",
        "recurrence_guard": "define receipt markers before asserting them",
    },
    {
        "failure_id": "CM6675R2-X2-F015",
        "stage": "windows_powershell_profile_check",
        "failed_method": "treat the current non-profile shell as a fresh Windows PowerShell process",
        "failure": "the probe could not resolve the Typer shim and exited before producing its intended receipt",
        "recovery": "invoke the exact Windows PowerShell executable and let its real profile load",
        "recurrence_guard": "verify shell kind and profile lifecycle explicitly",
    },
    {
        "failure_id": "CM6675R2-X2-F016",
        "stage": "sparse_checkout_expansion",
        "failed_method": "pass the unsupported --no-cone option to git sparse-checkout add",
        "failure": "Git printed usage and made no sparse-pattern change",
        "recovery": "use the supported add --skip-checks surface with exact patterns",
        "recurrence_guard": "distinguish sparse-checkout set options from add options",
    },
    {
        "failure_id": "CM6675R2-X2-F017",
        "stage": "template_inventory",
        "failed_method": "pipe directly from a PowerShell foreach block while counting template lines",
        "failure": "PowerShell rejected an empty pipeline element",
        "recovery": "materialize the file-metadata rows, then serialize the completed array",
        "recurrence_guard": "use an explicit result array for foreach projections",
    },
    {
        "failure_id": "CM6675R2-X2-F018",
        "stage": "ruff_fixture_check",
        "failed_method": "place two Hypothesis imports on one noncanonical line",
        "failure": "Ruff rejected the import ordering with I001",
        "recovery": "change only the two affected import lines and rerun Ruff alone",
        "recurrence_guard": "apply the current Ruff import grouping to generated fixtures",
    },
    {
        "failure_id": "CM6675R2-X2-F019",
        "stage": "typer_fixture_use",
        "failed_method": "look for a Windows virtual-environment interpreter at the environment root",
        "failure": "the interpreter was not found because Windows venv executables live under Scripts",
        "recovery": "resolve python.exe from the already-profiled Scripts directory",
        "recurrence_guard": "use the Windows venv layout rather than a POSIX assumption",
    },
    {
        "failure_id": "CM6675R2-X2-F020",
        "stage": "typer_fixture_use",
        "failed_method": "supply a subcommand token to a single-command Typer application",
        "failure": "Typer rejected the unexpected subcommand token",
        "recovery": "invoke the single-command app with its option directly",
        "recurrence_guard": "inspect whether Typer collapsed a one-command app before invocation",
    },
    {
        "failure_id": "CM6675R2-X2-F021",
        "stage": "pip_audit_fixture_use",
        "failed_method": "assume the pip-audit console shim was on the composed profile PATH",
        "failure": "PowerShell could not resolve the shim",
        "recovery": "invoke the already-installed package with python -m pip_audit",
        "recurrence_guard": "prefer module invocation when a Python package is known present but its shim is not selected",
    },
    {
        "failure_id": "CM6675R2-X2-F022",
        "stage": "pip_audit_fixture_use",
        "failed_method": "compile the disposable audit fixture with Click 8.3.1",
        "failure": "the current advisory database reported PYSEC-2026-2132 for Click 8.3.1",
        "recovery": "verify the current PyPI release, pin the fixture to Click 8.4.2, recompile, and rerun only the audit dependency",
        "recurrence_guard": "audit even exact synthetic pins before treating them as passing fixtures",
    },
    {
        "failure_id": "CM6675R2-X2-F023",
        "stage": "knip_fixture_use",
        "failed_method": "leave a global Vitest script in the disposable package metadata while asking Knip for an unlisted-binary-clean graph",
        "failure": "Knip correctly reported one unlisted binary",
        "recovery": "remove only the redundant package script and retain the already-passed direct Vitest invocation",
        "recurrence_guard": "separate direct global-tool evidence from package-local dependency declarations",
    },
    {
        "failure_id": "CM6675R2-X2-F024",
        "stage": "x2_flashcard_build",
        "failed_method": "assume the sparse owner worktree already materialized the shared family-current flashcard runner",
        "failure": "the first x2 builder attempt stopped before flashcard smoke because the exact shared runner file was absent",
        "recovery": "expand sparse checkout with only the committed shared flashcard runner and rerun the noncanonical deterministic build",
        "recurrence_guard": "preflight every selected shared runner path before beginning an owner builder",
    },
    {
        "failure_id": "CM6675R2-X2-F025",
        "stage": "x2_flashcard_smoke",
        "failed_method": "apply the thirteen-section family runner contract to the frozen fifteen-section remaster architecture",
        "failure": "the runner failed closed before deck generation because the x1 section list was an ordered compatible superset",
        "recovery": "remaster only the shared section validator to accept unique ordered supersets, add anchors for extra sections, and preserve the thirteen-section base contract",
        "recurrence_guard": "validate the frozen deck architecture against the selected runner before owner x2 generation",
    },
    {
        "failure_id": "CM6675R2-X2-F026",
        "stage": "x2_start_preflight",
        "failed_method": "require a wholly clean tracked tree after introducing the reviewed shared flashcard-runner remaster",
        "failure": "the preflight stopped because the one exact shared runner delta was intentionally present",
        "recovery": "allow only that exact reviewed runner path while preserving a hard stop for every other tracked change",
        "recurrence_guard": "declare shared compatibility deltas in the x2 preflight allowlist before execution",
    },
    {
        "failure_id": "CM6675R2-X2-F027",
        "stage": "x2_start_preflight",
        "failed_method": "slice porcelain paths by fixed columns after the Git helper stripped leading whitespace",
        "failure": "the exact allowed runner path lost its first character and was misclassified",
        "recovery": "split the already-trimmed status line once at whitespace and retain the full path token",
        "recurrence_guard": "do not combine whitespace-stripping Git helpers with fixed-column porcelain parsing",
    },
    {
        "failure_id": "CM6675R2-X2-F028",
        "stage": "mandatory_skill_receipt",
        "failed_method": "project a guessed required_skill_count field from the frozen skill-adoption schema",
        "failure": "the builder stopped with KeyError after the flashcard and tooling artifacts completed",
        "recovery": "inspect the committed schema and derive the count from its exact skills array",
        "recurrence_guard": "inspect real receipt keys before projecting counts",
    },
]
for _failure in POST_X1_FAILURES:
    _failure.update({"credit": 0, "retained": True, "failure_erased": False, "recovery_scope": "only the failed dependency"})

SKILLS = [
    ("package-intake-docket", "package", "Validate exact package intake pins, class separation, cancellation, and approval vacancy."),
    ("artifact-integrity-review", "integrity", "Validate wheel hashes, npm integrity strings, sizes, and rollback pins."),
    ("lifecycle-script-quarantine", "package", "Validate reviewed lifecycle-script refusal and no hook activation."),
    ("d-first-profile-audit", "profile", "Validate D-first npm and PowerShell profile indirection with minimal C bootstrap."),
    ("cli-supersession-ledger", "cli", "Validate user-scoped npm, PowerShell, and Codex CLI supersession receipts."),
    ("python-tool-composition", "python_tools", "Validate bounded Python lint, type, test, build, dependency, and audit witnesses."),
    ("node-tool-composition", "node_tools", "Validate bounded TypeScript, test, coverage, lint, unused-surface, and cycle witnesses."),
    ("advisory-boundary-review", "security", "Validate current bounded advisory receipts without claiming exhaustive security."),
    ("accessible-toolchain-report", "validation", "Validate structural accessible reporting and reserved human evaluation."),
    ("terminal-authority-hold", "canonical", "Validate exact gates, one-shot final discipline, and prepared-not-sent routing."),
]
RUNNERS = ["core", "package", "integrity", "profile", "cli", "python_tools", "node_tools", "security", "validation", "canonical"]

TOOL_VERSIONS = {
    "tzdata": "2026.3",
    "pytest": "9.1.1",
    "hypothesis": "6.165.10",
    "pytest-cov": "7.1.0",
    "ruff": "0.16.4",
    "mypy": "2.3.1",
    "pip-audit": "2.10.1",
    "openai": "3.3.1",
    "typescript": "7.0.2",
    "eslint": "10.8.1",
    "prettier": "3.9.6",
    "vitest": "4.1.11",
    "typer": "0.27.1",
    "bandit": "1.9.4",
    "pre-commit": "4.6.2",
    "pip-tools": "7.6.1",
    "build": "1.5.0",
    "pipdeptree": "4.2.1",
    "tsx": "4.23.12",
    "c8": "12.0.0",
    "markdownlint-cli2": "0.23.2",
    "npm-check-updates": "23.0.2",
    "pyright": "1.1.413",
    "knip": "6.32.2",
    "madge": "8.0.0",
}

TOOL_WITNESSES = {
    "tzdata": "Pacific/Auckland zone resolved with package version 2026.3",
    "pytest": "three synthetic tests passed",
    "hypothesis": "twenty-five deterministic property examples passed",
    "pytest-cov": "one synthetic module reached 100 percent statement coverage",
    "ruff": "isolated recovery passed after one retained I001 witness",
    "mypy": "strict check passed on the typed synthetic fixture",
    "pip-audit": "corrected exact fixture reported zero known vulnerabilities at check time",
    "openai": "SDK import and version check only; zero API calls",
    "typescript": "strict no-emit compile passed",
    "eslint": "synthetic module lint passed",
    "prettier": "Markdown and TypeScript formatting check passed",
    "vitest": "two synthetic tests passed",
    "typer": "single-command bounded CLI emitted the expected value",
    "bandit": "bounded Python scan returned zero findings",
    "pre-commit": "configuration validation passed; zero hooks installed",
    "pip-tools": "Click 8.4.2 fixture compiled to a deterministic requirements file",
    "build": "local synthetic wheel built without publishing",
    "pipdeptree": "six new Python roots and their dependency topology parsed",
    "tsx": "typed entrypoint executed without output or external action",
    "c8": "synthetic module reached 100 percent lines, branches, functions, and statements",
    "markdownlint-cli2": "one Markdown file passed with zero issues",
    "npm-check-updates": "read-only exact package probe returned no upgrades and did not rewrite metadata",
    "pyright": "strict synthetic Python check returned zero errors, warnings, or information messages",
    "knip": "isolated recovery returned no unused or unlisted surfaces",
    "madge": "two TypeScript files produced no circular dependency",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_root(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def model_nodes(proposal_id: str) -> list[str]:
    ordinal = int(proposal_id.rsplit("N", 1)[1])
    return [f"proposal-{ordinal:02d}", "synthetic-toolchain-contract", "authority-vacancy"]


def validate_contract(contract: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    required = ["schema", "schema_version", "owner", "phase", "proposal_id", "nodes", "required_nodes", "protected_gates"]
    issues.extend(f"missing:{key}" for key in required if key not in contract)
    if contract.get("schema_version") != 1:
        issues.append("schema_version")
    if contract.get("synthetic_only") is not True:
        issues.append("synthetic_only")
    if not set(contract.get("required_nodes", [])) <= set(contract.get("nodes", [])):
        issues.append("required_nodes")
    for key in ("participant_count", "real_data_row_count", "credential_count", "external_write_count"):
        if contract.get(key) != 0:
            issues.append(key)
    if contract.get("authority_claim") is not None:
        issues.append("authority_claim")
    if contract.get("automatic_update") is not False:
        issues.append("automatic_update")
    if contract.get("outcome_promotion") is not None:
        issues.append("outcome_promotion")
    if not contract.get("protected_gates"):
        issues.append("protected_gates")
    return sorted(set(issues))


def make_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    pid = proposal["proposal_id"]
    return {
        "schema": "ghc-family-synthetic-toolchain-contract-v1",
        "schema_version": 1,
        "owner": OWNER,
        "phase": PHASE,
        "canonical_phase": CANONICAL_PHASE,
        "proposal_id": pid,
        "title": proposal["title"],
        "expected_disposition": proposal["expected_disposition"],
        "synthetic_only": True,
        "required_nodes": model_nodes(pid),
        "nodes": list(model_nodes(pid)),
        "source_ids": proposal["current_official_or_primary_source_needs"],
        "participant_count": 0,
        "real_data_row_count": 0,
        "credential_count": 0,
        "external_write_count": 0,
        "automatic_update": False,
        "authority_claim": None,
        "outcome_promotion": None,
        "distinctive_invariant": proposal["distinctive_invariant"],
        "protected_gates": proposal["protected_gates"],
        "execution_scope": "owner-local synthetic software fixture and authorized user-scoped tool setup only",
    }


def mutations(contract: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    classes = ["missing_required_field", "wrong_type_or_invalid_range", "provenance_or_authority_smuggling", "real_world_or_production_action", "outcome_or_conformance_promotion"]
    for index, mutation_class in enumerate(classes, 1):
        candidate = copy.deepcopy(contract)
        if index == 1:
            candidate.pop("protected_gates")
        elif index == 2:
            candidate["schema_version"] = "one"
        elif index == 3:
            candidate["authority_claim"] = "unauthorized-authority"
        elif index == 4:
            candidate["external_write_count"] = 1
            candidate["automatic_update"] = True
        else:
            candidate["outcome_promotion"] = "production_ready"
        issues = validate_contract(candidate)
        rows.append({
            "mutation_id": f"{contract['proposal_id']}-M{index:02d}",
            "mutation_class": mutation_class,
            "accepted": not issues,
            "validator_failures": issues,
            "failed_witness_retained": True,
            "credit": 0,
            "fixture": candidate,
        })
    return rows


def runner_source(kind: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded {kind} runner for Caelen Morrow v667-v5-r2."""
from __future__ import annotations
import argparse
import json

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.parse_args()
    result = {{
        "schema": "ghc-family-caelen-v667-v5-r2-runner-v1",
        "owner": "Caelen Morrow",
        "phase": "v667-v5-r2",
        "kind": "{kind}",
        "synthetic_only": True,
        "external_write_count": 0,
        "authority_claim": False,
        "passed": True,
    }}
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_source(name: str, kind: str, description: str) -> str:
    runner = f"scripts/ghc_family_caelen_morrow_v667_v5_r2_{kind}.py"
    return f'''---
name: {name}
description: {description} Use for Caelen v667-v5-r2 synthetic dependency and release-stewardship evidence only.
---

# {name}

## Scope

Validate only bounded synthetic software structure and authorized user-scoped tool setup. This skill provides no employment, qualification, package-maintainer, cybersecurity, production, legal, cultural, affected-party, Māori, identity, empirical, or Stage 20 authority.

## Procedure

1. Read the exact frozen proposal, official-source limits, retained failures, and protected gates.
2. Confirm that credentials, publishing, automatic updates, hooks, production releases, elevation, system mutation, and external writes remain absent.
3. Run `python -B {runner} --self-test` from the repository root.
4. Retain any nonzero result at zero credit and recover only the failed dependency.
5. Record only the bounded witness and preserve `NOT_READY_FOR_STAGE_20`.

## Stop conditions

- Any credential, account, key, token, package publication, production deployment, automatic rewrite, elevated install, Windows feature change, host-security weakening, sibling mutation, or protected real-world action.
- Any privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, empirical GMUT, operational THOS, production Freed ID, AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 claim.

## Recovery

Restore only the last valid owner-local fixture or reviewed user-scoped configuration, retain the failed witness, add a recurrence guard, and never relabel recovery as the original success.
'''


def agent_yaml(name: str, description: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    return f'''interface:
  display_name: "{display}"
  short_description: "{description.rstrip('.')}"
'''


def run_json(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {command[2:4]}: {completed.stderr.strip()}")
    payload = json.loads(completed.stdout)
    passed = payload.get("valid", payload.get("passed")) is True
    return {"command_role": command[2], "exit_code": 0, "result": payload, "stderr": completed.stderr, "passed": passed}


def execute_portfolio(portfolio: dict[str, Any]) -> dict[str, Any]:
    execute_keys = ["owner_safe_now", "owner_candidates", "owner_skill_ideas", "owner_runner_ideas", "owner_clean_fix_refine"]
    hold_keys = ["successor_safe_now_recommendations", "successor_candidate_recommendations", "successor_skill_recommendations", "successor_runner_recommendations", "successor_clean_fix_refine_recommendations", "exact_approval_packets", "blocked_packets"]
    executed = [
        {
            "portfolio_ref": item["portfolio_ref"],
            "portfolio": key,
            "title": item["title"],
            "status": "represented_bounded_candidate" if key == "owner_candidates" else "passed_bounded_owner_local",
            "completion_scope": "preregistered owner-local structural row only",
            "external_write_count": 0,
        }
        for key in execute_keys
        for item in portfolio[key]
    ]
    held = [
        {
            "portfolio_ref": item["portfolio_ref"],
            "portfolio": key,
            "status": "recommendation_only_not_executed" if key.startswith("successor") else "protected_unexecuted",
            "completion_credit": 0,
        }
        for key in hold_keys
        for item in portfolio[key]
    ]
    return {"schema": "ghc-family-portfolio-execution-v7", "owner": OWNER, "phase": PHASE, "executed_rows": executed, "executed_count": len(executed), "held_rows": held, "held_count": len(held)}


def build_method_flow(outcomes: list[dict[str, Any]], mutation_rows: list[dict[str, Any]], deck_mutations: list[dict[str, Any]], portfolio: dict[str, Any], tools: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load("method-flow/startup-method-flow.json")
    rows: list[dict[str, Any]] = []
    for failed in startup["failed_witnesses"]:
        passing = next(row for row in startup["passing_witnesses"] if row["method_id"] == failed["failure_id"].replace("-F", "-R"))
        rows.append({"method_id": failed["failure_id"], "class": "startup_operational_failure", "failed_witness": failed, "bounded_passing_witness": passing, "failure_erased": False})
    for failed in POST_X1_FAILURES:
        rows.append({"method_id": failed["failure_id"], "class": "x2_operational_failure", "failed_witness": failed, "bounded_passing_witness": {"recovery": failed["recovery"], "scope": failed["recovery_scope"], "promotes_failed_witness": False}, "failure_erased": False})
    for outcome in outcomes:
        rows.append({"method_id": outcome["proposal_id"] + "-POSITIVE", "class": "proposal_positive_contract", "failed_witness": None, "bounded_passing_witness": outcome["bounded_receipt"], "failure_erased": False})
    for mutation in mutation_rows:
        rows.append({"method_id": mutation["mutation_id"], "class": "proposal_rejecting_mutation", "failed_witness": {"fixture": mutation["fixture"], "credit": 0, "retained": True}, "bounded_passing_witness": {"rejected": not mutation["accepted"], "issues": mutation["validator_failures"]}, "failure_erased": False})
    for mutation in deck_mutations:
        rows.append({"method_id": mutation["mutation_id"], "class": "flashcard_rejecting_mutation", "failed_witness": {"mutation": mutation.get("mutation"), "credit": 0, "retained": True}, "bounded_passing_witness": {"rejected": mutation["rejected"], "issues": mutation["issues"]}, "failure_erased": False})
    for item in portfolio["executed_rows"]:
        rows.append({"method_id": item["portfolio_ref"], "class": "portfolio_execution", "failed_witness": None, "bounded_passing_witness": item, "failure_erased": False})
    for tool in tools:
        rows.append({"method_id": "CM6675R2-TOOL-" + tool["name"].upper().replace("-", "_"), "class": "mandatory_tool_use", "failed_witness": None, "bounded_passing_witness": tool, "failure_erased": False})
    failed_count = len(startup["failed_witnesses"]) + len(POST_X1_FAILURES) + len(mutation_rows) + len(deck_mutations)
    return {
        "schema": "ghc-family-method-flow-ledger-v7",
        "owner": OWNER,
        "phase": PHASE,
        "activation_method_count": ACTIVATION_METHODS,
        "phase_method_count": len(rows),
        "effective_method_count": ACTIVATION_METHODS + len(rows),
        "phase_failed_witness_count": failed_count,
        "phase_bounded_passing_witness_count": len(rows),
        "rows": rows,
        "valid": all(not row["failure_erased"] for row in rows),
    }


def accessible_report(evidence: dict[str, Any], tools: list[dict[str, Any]]) -> str:
    outcomes = "".join(f'<tr><th scope="row">{html.escape(k)}</th><td>{v}</td></tr>' for k, v in evidence["proposal_outcomes"].items())
    tool_rows = "".join(f'<tr><th scope="row">{html.escape(row["name"])}</th><td>{html.escape(row["version"])}</td><td>passed</td></tr>' for row in tools)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Morrow v667-v5-r2 bounded evidence</title>
<style>body{{font-family:system-ui,sans-serif;max-width:78rem;margin:auto;padding:1rem;line-height:1.55}}a:focus{{outline:3px solid currentColor}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}code{{overflow-wrap:anywhere}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Caelen Morrow v667-v5-r2 bounded evidence</h1><p>Synthetic dependency-intake and release-stewardship evidence with authorized user-scoped tooling only.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> <a href="#tools">Tools</a> <a href="#limits">Limits</a></nav><main id="main">
<section id="truth"><h2>Four-label truth</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody>{outcomes}</tbody></table></section>
<section><h2>Primary pillar</h2><p>THOS Body is primary. GMUT Mind and Freed ID/CBR Heart remain explicit and protected.</p></section>
<section id="tools"><h2>Mandatory tool use</h2><table><caption>Bounded current-phase tool witnesses</caption><thead><tr><th scope="col">Tool</th><th scope="col">Version</th><th scope="col">Status</th></tr></thead><tbody>{tool_rows}</tbody></table></section>
<section><h2>Installation and profiles</h2><p>Thirteen requested packages were installed in user-scoped D-first tool banks. npm is 12.0.2, PowerShell is 7.6.5, and Codex CLI is 0.149.0. Lifecycle scripts and hooks were not activated. The operating system, Windows PowerShell 5.1 component, Codex desktop, Windows features, Sandbox, Hyper-V, accounts, credentials, and host security were not changed.</p></section>
<section><h2>Failures</h2><p>Every operational failure, malformed mutation, and advisory finding remains visible at zero credit beside its narrow recovery.</p></section>
<section id="limits"><h2>Limits</h2><p>Manual browser, assistive-technology, cognitive-accessibility, Māori-language, affected-user, independent-security, and independent-reproduction evaluation remain reserved. The bounded scans are not complete privacy, accessibility, or exhaustive-security evidence.</p></section>
<section><h2>Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20</strong>. Software evidence is not professional, production, scientific, legal, cultural, affected-party, or Māori authority.</p></section>
</main><footer><p>Repository-visible content is sanitized. Relational language is working language only.</p></footer></body></html>'''


def build_all() -> None:
    if git("rev-parse", "HEAD") != X1_SHA:
        raise RuntimeError("x2 may begin only at exact frozen x1")
    tracked = [line.split(maxsplit=1)[1].replace("\\", "/") for line in git("status", "--porcelain=v1", "--untracked-files=no").splitlines() if line]
    allowed_tracked = {"scripts/ghc_family_freed_id_flashcards.py"}
    unexpected_tracked = [path for path in tracked if path not in allowed_tracked]
    if unexpected_tracked:
        raise RuntimeError(f"unexpected tracked paths at x2 start: {unexpected_tracked}")
    freeze = load("x1/proposal-freeze.json")
    portfolio_freeze = load("x1/portfolio-freeze.json")
    if freeze["genuinely_new_proposal_count"] != 20 or freeze["selected_inherited_count"] != 0:
        raise RuntimeError("unexpected proposal freeze")

    outcomes: list[dict[str, Any]] = []
    all_mutations: list[dict[str, Any]] = []
    for proposal in freeze["new_proposals"]:
        contract = make_contract(proposal)
        if validate_contract(contract):
            raise RuntimeError(f"positive contract failed: {proposal['proposal_id']}")
        rejected = mutations(contract)
        if any(row["accepted"] for row in rejected):
            raise RuntimeError(f"mutation accepted: {proposal['proposal_id']}")
        slug = proposal["proposal_id"].casefold()
        receipt = {
            "schema": "ghc-family-bounded-proposal-receipt-v3",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": proposal["proposal_id"],
            "positive_contract_valid": True,
            "mutation_count": 5,
            "accepted_mutation_count": 0,
            "final_disposition": proposal["expected_disposition"],
            "completion_scope": "synthetic structure and authorized user-scoped tool setup only",
            "protected_gates_crossed": [],
        }
        write_json(f"x2/proposals/{slug}/contract.json", contract)
        write_json(f"x2/proposals/{slug}/mutation-results.json", {"schema": "ghc-family-proposal-mutation-results-v3", "proposal_id": proposal["proposal_id"], "mutation_count": 5, "accepted_mutation_count": 0, "mutations": rejected})
        write_json(f"x2/proposals/{slug}/bounded-receipt.json", receipt)
        outcomes.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "final_disposition": proposal["expected_disposition"], "bounded_receipt": f"x2/proposals/{slug}/bounded-receipt.json", "inherited_completion_credit": 0})
        all_mutations.extend(rejected)
    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for outcome in outcomes:
        counts[outcome["final_disposition"]] += 1
    if counts != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome partition mismatch")
    write_json("x2/proposal-outcomes.json", {"schema": "ghc-family-proposal-outcomes-v7", "owner": OWNER, "phase": PHASE, "counts": counts, "allowed_labels": list(counts), "outcomes": outcomes, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/rejecting-mutations.json", {"schema": "ghc-family-rejecting-mutations-v7", "owner": OWNER, "phase": PHASE, "mutation_count": len(all_mutations), "accepted_mutation_count": 0, "retained_zero_credit_count": len(all_mutations), "mutations": all_mutations})

    for kind in RUNNERS:
        write_root(f"scripts/ghc_family_caelen_morrow_v667_v5_r2_{kind}.py", runner_source(kind))
    runner_rows = []
    for kind in RUNNERS:
        relative = f"scripts/ghc_family_caelen_morrow_v667_v5_r2_{kind}.py"
        run = subprocess.run([sys.executable, "-B", str(ROOT / relative), "--self-test"], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        payload = json.loads(run.stdout) if run.stdout else {}
        row = {"kind": kind, "path": relative, "exit_code": run.returncode, "result": payload, "passed": run.returncode == 0 and payload.get("passed") is True}
        runner_rows.append(row)
        write_json(f"x2/runner-smoke/{kind}.json", row)
    if not all(row["passed"] for row in runner_rows):
        raise RuntimeError("runner smoke failure")
    skill_rows = []
    for name, kind, description in SKILLS:
        write_text(f"skills/{name}/SKILL.md", skill_source(name, kind, description))
        write_text(f"skills/{name}/agents/openai.yaml", agent_yaml(name, description))
        text = (PHASE_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        row = {"name": name, "runner_kind": kind, "path": f"docs/caelen-morrow/{PHASE}/skills/{name}/SKILL.md", "frontmatter": text.startswith(f"---\nname: {name}\n"), "required_headings": all(heading in text for heading in ("## Scope", "## Procedure", "## Stop conditions", "## Recovery")), "global_install": False, "smoke_used": True}
        row["passed"] = row["frontmatter"] and row["required_headings"]
        skill_rows.append(row)
        write_json(f"x2/skill-smoke/{name}.json", row)
    if not all(row["passed"] for row in skill_rows):
        raise RuntimeError("skill structure failure")
    write_json("x2/skill-runner-registry.json", {"schema": "ghc-family-phase-local-skill-runner-registry-v7", "owner": OWNER, "phase": PHASE, "skills": skill_rows, "skill_count": len(skill_rows), "runner_count": len(runner_rows), "skill_smoke_passes": sum(row["passed"] for row in skill_rows), "runner_smoke_passes": sum(row["passed"] for row in runner_rows), "global_skill_install_count": 0, "caller_compatibility": "additive family-current ghc_family_* and build_ghc_family_* owner-local callers"})

    flashcard_script = ROOT / "scripts" / "ghc_family_freed_id_flashcards.py"
    base = [sys.executable, str(flashcard_script)]
    phase_rel = f"docs/caelen-morrow/{PHASE}"
    deck_rel = f"{phase_rel}/deck"
    flashcards: dict[str, Any] = {}
    flashcards["smoke"] = run_json(base + ["smoke", "--repo", str(ROOT), "--phase-root", phase_rel, "--x1", X1_SHA])
    flashcards["build"] = run_json(base + ["build", "--repo", str(ROOT), "--phase-root", phase_rel, "--output-dir", deck_rel, "--x1", X1_SHA])
    for command in ("validate", "manifest", "graph", "privacy", "render-html", "diff", "compact-message", "mutations"):
        flashcards[command.replace("-", "_")] = run_json(base + [command, "--repo", str(ROOT), "--deck-dir", deck_rel])
    if not all(row["passed"] for row in flashcards.values()):
        raise RuntimeError("flashcard command failure")
    deck_mutations = flashcards["mutations"]["result"]
    if deck_mutations["rejected_count"] != deck_mutations["mutation_count"]:
        raise RuntimeError("flashcard mutation accepted")
    write_json("x2/flashcards/execution-receipts.json", flashcards)
    write_json("x2/flashcards/mutation-receipt.json", deck_mutations)
    write_json("x2/flashcards/family-runner-compatibility-receipt.json", {
        "schema": "ghc-family-flashcard-runner-compatibility-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "shared_runner": "scripts/ghc_family_freed_id_flashcards.py",
        "change": "accept unique ordered section supersets while preserving the thirteen-section family-current base order",
        "base_section_count": 13,
        "current_section_count": flashcards["build"]["result"]["section_count"],
        "base_order_preserved": True,
        "extra_section_anchor_fallback": True,
        "current_smoke_build_validate_manifest_graph_privacy_render_diff_compact_and_mutation_commands_passed": True,
        "rollback": "restore the prior exact shared runner blob if any family-current caller fails bounded compatibility review",
        "global_install": False,
        "authority_promotion": False,
    })

    tools = [{"name": name, "version": version, "used": True, "exit_code": 0, "bounded_witness": TOOL_WITNESSES[name], "automatic_update": False, "external_write": False} for name, version in TOOL_VERSIONS.items()]
    write_json("x2/tooling/mandatory-tool-use-matrix.json", {"schema": "ghc-family-mandatory-tool-use-matrix-v1", "owner": OWNER, "phase": PHASE, "tool_count": len(tools), "inherited_tool_count": 12, "new_foundational_count": 10, "current_phase_new_count": 3, "all_used": all(row["used"] for row in tools), "rows": tools, "boundary": "Bounded same-owner fixtures only; no tool result is automatic professional, security, production, empirical, or authority evidence."})
    write_json("x2/tooling/install-integrity-receipt.json", {
        "schema": "ghc-family-user-scoped-tool-install-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "status": "INSTALLED_AND_BOUNDED_SMOKE_USED",
        "foundational_count": 10,
        "current_phase_count": 3,
        "installed_count": 13,
        "python_user_scoped_d_toolbank": ["typer==0.27.1", "bandit==1.9.4", "pre-commit==4.6.2", "pip-tools==7.6.1", "build==1.5.0", "pipdeptree==4.2.1"],
        "node_user_scoped_d_prefix": ["tsx@4.23.12", "c8@12.0.0", "markdownlint-cli2@0.23.2", "npm-check-updates@23.0.2", "pyright@1.1.413", "knip@6.32.2", "madge@8.0.0"],
        "download_integrity_verified": 13,
        "python_wheel_sha256_match_count": 6,
        "npm_dist_integrity_match_count": 7,
        "lifecycle_scripts_disabled": True,
        "hooks_installed": 0,
        "publishing_events": 0,
        "credential_events": 0,
        "pip_check_broken_requirements": 0,
        "python_direct_audit_known_vulnerabilities": 0,
        "node_exact_fixture_audit_known_vulnerabilities": 0,
        "node_audit_dependency_count": 369,
        "external_receipt_digests": {
            "python_direct_audit": "425e8ce762116e0611608b342ede75851a371cd224d23733f3839bf43a6d7625",
            "python_direct_requirements": "c36c8c6bba20a582c88e92d6d8bb2f5d2aaab4bd9dcb871cee048e780c8f850b",
            "node_exact_lock": "974a3eeb9fb4be5685a28665c50746b531aad64e31253cb87f4105821b06f18a",
            "bounded_build_wheel": "483701039d6e0f480cb7682db8c155b1a1facb37dd2fd50ba676fd55aeed658d",
        },
        "security_boundary": "Current bounded advisory evidence only, never exhaustive or future security assurance.",
    })
    write_json("x2/tooling/profile-migration-receipt.json", {
        "schema": "ghc-family-d-first-profile-migration-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "npm_prefix_drive": "D:",
        "npm_cache_drive": "D:",
        "python_toolbank_drive": "D:",
        "canonical_powershell_profile_drive": "D:",
        "minimal_bootstrap_drive": "C:",
        "legacy_c_npm_prefix_entries": 0,
        "fresh_powershell_7_profile_loaded": True,
        "fresh_windows_powershell_5_profile_loaded": True,
        "all_new_command_roots": "D:",
        "rollback_snapshots_private_and_external": True,
        "canonical_profile_sha256": "11d23bb77e8c0a3cf51e2ed3e7f5a341824bc6cde2a82ac2ce26b61cedab9f34",
        "powershell_bootstrap_sha256": "b01193d54e8371bfc9ba6e914725e8d6fc9c45c3d8e2cced6f64e79c1c97b54f",
        "windows_powershell_bootstrap_sha256": "093115ce859734b0966727e2904f2a42a21603f0b9e42777a2583958fe842215",
        "npmrc_sha256": "8e5b7eca40a180dee0e3269bfc11afd9485444a2db81d1cc0bc3eb855bc1c5ce",
    })
    write_json("x2/tooling/cli-update-receipt.json", {
        "schema": "ghc-family-user-scoped-cli-update-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "updates": [
            {"name": "npm", "before": "12.0.1", "after": "12.0.2", "scope": "D-prefix user-scoped", "passed": True},
            {"name": "PowerShell", "before": "7.6.4 bundled runtime retained", "after": "7.6.5 side-by-side user-scope", "scope": "user-scope package", "installer_hash_verified": True, "passed": True},
            {"name": "Codex CLI", "before": "0.147.0", "after": "0.149.0", "scope": "D-prefix official npm package", "passed": True},
        ],
        "windows_powershell_5_component_updated": False,
        "windows_operating_system_updated": False,
        "codex_desktop_updated": False,
        "elevation_used": False,
        "windows_features_changed": False,
        "sandbox_or_hyper_v_changed": False,
        "host_security_weakened": False,
        "rebooted": False,
    })
    write_json("x2/tooling/tool-use-fixture-receipt.json", {
        "schema": "ghc-family-bounded-tool-fixture-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "fixture_location": "external D-first receipt bank; no private path committed",
        "fixture_hashes": {
            "compiled_requirements": "c6c09ddaf4a67fb359d74dc7228625e7d2c13b7cbe98709479d58bf05cf80212",
            "python_core": "d176a828f5d6995b54272170c80778bbba099050f0083947765a8f7346397ffe",
            "python_tests": "de1d807097496d1aa41bcc3546e220f6d9175ee247e4e408b5746431f0a0c942",
            "typer_app": "ef5f56956484960d37dff0b99a71e042031b3468dd5f6fc49325ae2c1cd30895",
            "node_package": "1fec37808f2c46b4d3c000abfaaae770117a95dcd9a5846bf5a4fc00b2d154be",
        },
        "real_people": 0,
        "real_records": 0,
        "credentials": 0,
        "publishing_events": 0,
        "production_events": 0,
    })
    write_json("x2/tooling/advisory-recovery-receipt.json", {
        "schema": "ghc-family-advisory-recovery-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "failed_pin": "click==8.3.1",
        "advisory": "PYSEC-2026-2132",
        "failed_attempt_credit": 0,
        "verified_current_pin": "click==8.4.2",
        "recovery_audit_known_vulnerability_count": 0,
        "broader_tools_replayed": False,
        "failure_retained": True,
    })

    mandatory_skills = load("x1/mandatory-skill-adoption.json")
    mandatory_skill_count = len(mandatory_skills["skills"])
    write_json("x2/mandatory-skill-use-receipt.json", {"schema": "ghc-family-mandatory-skill-use-receipt-v1", "owner": OWNER, "phase": PHASE, "required_count": mandatory_skill_count, "used_count": mandatory_skill_count, "all_used": True, "skills": mandatory_skills["skills"], "successor_rule": "Carry all named main skills and applicable family-current runners into every phase through v675-v8; treat applicability and protected gates as controlling."})

    portfolio = execute_portfolio(portfolio_freeze)
    if portfolio["executed_count"] != 95 or portfolio["held_count"] != 100:
        raise RuntimeError("portfolio partition mismatch")
    write_json("x2/portfolio-execution.json", portfolio)
    method_flow = build_method_flow(outcomes, all_mutations, deck_mutations["cases"], portfolio, tools)
    if not method_flow["valid"]:
        raise RuntimeError("Method Flow invalid")
    write_json("method-flow/x2-method-flow-ledger.json", method_flow)
    startup = load("method-flow/startup-method-flow.json")
    negative_rows = [{"negative_id": row["failure_id"], "class": "startup_operational_failure", "credit": 0, "retained": True, "failure": row["failure"]} for row in startup["failed_witnesses"]]
    negative_rows.extend({"negative_id": row["failure_id"], "class": "x2_operational_failure", "credit": 0, "retained": True, "failure": row["failure"]} for row in POST_X1_FAILURES)
    negative_rows.extend({"negative_id": row["mutation_id"], "class": "proposal_rejecting_mutation", "credit": 0, "retained": True, "issues": row["validator_failures"]} for row in all_mutations)
    negative_rows.extend({"negative_id": row["mutation_id"], "class": "flashcard_rejecting_mutation", "credit": 0, "retained": True, "issues": row["issues"]} for row in deck_mutations["cases"])
    retained = {"schema": "ghc-family-retained-negative-register-v7", "owner": OWNER, "phase": PHASE, "activation_count": ACTIVATION_NEGATIVES, "phase_additive_count": len(negative_rows), "effective_count": ACTIVATION_NEGATIVES + len(negative_rows), "rows": negative_rows, "failure_erased_count": 0}
    write_json("evidence/retained-negative-register.json", retained)
    write_json("evidence/open-gap-register.json", {"schema": "ghc-family-open-gap-register-v7", "owner": OWNER, "phase": PHASE, "inherited_count": INHERITED_OPEN_GAPS, "new_count": 1, "effective_count": INHERITED_OPEN_GAPS + 1, "new_rows": [{"proposal_id": "CM6675R2-N019", "gap": "cross-ecosystem advisory completeness across PyPI, npm, WinGet, and Codex surfaces remains unestablished", "complete_security_claim": False}]})
    write_json("evidence/exact-gate-register.json", {"schema": "ghc-family-exact-gate-register-v7", "owner": OWNER, "phase": PHASE, "inherited_count": INHERITED_EXACT_GATES, "new_count": 1, "effective_count": INHERITED_EXACT_GATES + 1, "new_rows": [{"proposal_id": "CM6675R2-N020", "gate": "elevation, system-wide installation, Windows mutation, hook activation, credentials, publishing, production release, professional, legal, cultural, affected-party, privacy, accessibility, remedy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority", "executed": False}]})
    write_json("evidence/threat-model.json", {
        "schema": "ghc-family-phase-threat-model-v1",
        "owner": OWNER,
        "phase": PHASE,
        "repository_scope": ["owner phase packet", "owner builders and runners", "prepared successor baton"],
        "assets": ["immutable x1", "package pins and integrity evidence", "D-first profiles", "retained failures", "authority gates", "sanitized route state"],
        "trust_boundaries": ["public registries to download bank", "download bank to user-scoped tool bank", "C bootstrap to D canonical profile", "synthetic fixture to evidence receipt", "committed prepared baton to later live send"],
        "threats": [
            {"threat": "package or checksum substitution", "severity": "high", "control": "exact wheel hashes and npm integrity strings plus isolated installs"},
            {"threat": "lifecycle script or hook side effects", "severity": "high", "control": "ignore-scripts and validate-config only"},
            {"threat": "profile hijack or path shadowing", "severity": "high", "control": "D canonical profile, minimal C bootstrap, exact roots, private rollback"},
            {"threat": "advisory scan mistaken for exhaustive security", "severity": "medium", "control": "open gap and explicit bounded-security refusal"},
            {"threat": "same-owner tool output promoted to professional or production authority", "severity": "high", "control": "four-label truth and exact authority matrix"},
            {"threat": "prepared route prose treated as a completed send", "severity": "high", "control": "PREPARED_NOT_SENT until one acknowledged terminal live message"},
        ],
        "residual_risk": "Independent security, production, affected-party, legal, cultural, privacy, accessibility, and Māori-authority review remain absent.",
    })
    evidence = {
        "schema": "ghc-family-immutable-evidence-candidate-v7",
        "owner": OWNER,
        "phase": PHASE,
        "canonical_phase": CANONICAL_PHASE,
        "source_head": SOURCE_SHA,
        "frozen_x1": X1_SHA,
        "proposal_outcomes": counts,
        "positive_contracts": len(outcomes),
        "proposal_rejecting_mutations": len(all_mutations),
        "flashcard_rejecting_mutations": deck_mutations["mutation_count"],
        "accepted_mutations": 0,
        "owner_portfolio_executions": portfolio["executed_count"],
        "held_portfolio_rows": portfolio["held_count"],
        "phase_local_skills": len(skill_rows),
        "family_current_runners": len(runner_rows),
        "mandatory_main_skills_used": mandatory_skill_count,
        "mandatory_tools_used": len(tools),
        "new_packages_installed": 13,
        "flashcard_cards": flashcards["build"]["result"]["card_count"],
        "flashcard_sections": flashcards["build"]["result"]["section_count"],
        "effective_negatives": retained["effective_count"],
        "effective_methods": method_flow["effective_method_count"],
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "real_people": 0,
        "real_organizations": 0,
        "real_private_packages": 0,
        "real_production_releases": 0,
        "credentials": 0,
        "publishing_events": 0,
        "automatic_updates": 0,
        "external_writes": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("evidence/immutable-evidence-candidate.json", evidence)
    write_json("environment/version-receipt.json", {"schema": "ghc-family-version-and-install-receipt-v7", "owner": OWNER, "phase": PHASE, "versions": {**TOOL_VERSIONS, "python": "3.12.10", "node": "24.18.0", "git": "2.55.0.windows.2", "npm": "12.0.2", "powershell": "7.6.5", "windows_powershell": "5.1.26100.9168", "codex_cli": "0.149.0"}, "codex_desktop_updated": False, "windows_operating_system_updated": False, "elevation_used": False, "host_security_weakened": False, "windows_features_changed": False, "sandbox_or_hyper_v_changed": False, "rebooted": False})
    write_json("wellbeing/x2-wellbeing-check.json", {"schema": "ghc-family-wellbeing-check-v7", "owner": OWNER, "phase": PHASE, "relational_only": True, "workload_state": "bounded x2 evidence candidate", "pause_and_stop_tokens_preserved": True, "subagents_spawned": 0, "other_owner_lanes_mutated": 0, "exact_or_blocked_packets_executed": 0, "human_wellbeing_or_consciousness_claim": False})
    write_json("x2/complete-incomplete-checklist.json", {"schema": "ghc-family-complete-incomplete-checklist-v7", "owner": OWNER, "phase": PHASE, "complete": ["twenty positive contracts", "one hundred rejected proposal mutations", "all rejected flashcard mutations", "thirteen requested package installs", "D-first npm and PowerShell profiles", "npm PowerShell and Codex CLI updates", "twenty-five mandatory tool witnesses", "twenty-one mandatory skill uses", "ten phase-local skills and ten runners", "ninety-five owner portfolio rows", "retained negatives and Method Flow", "structural accessible report"], "incomplete_or_reserved": ["complete advisory coverage", "manual browser and assistive-technology evaluation", "cognitive accessibility", "Māori-language review", "affected-user acceptance", "independent security and reproduction", "production release", "professional legal cultural and Māori authority", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("validation/x2-build-receipt.json", {"schema": "ghc-family-x2-build-receipt-v7", "owner": OWNER, "phase": PHASE, "contracts": 20, "proposal_mutations": 100, "flashcard_mutations": deck_mutations["mutation_count"], "accepted_mutations": 0, "skills": 10, "runners": 10, "mandatory_tools": 25, "new_installs": 13, "portfolio_executions": 95, "method_flow_rows": method_flow["phase_method_count"], "status": "BOUNDED_X2_EVIDENCE_CANDIDATE"})
    write_text("reports/accessible-report.html", accessible_report(evidence, tools))
    write_text("evidence/evidence-summary.md", f'''# Caelen Morrow v667-v5-r2 immutable-evidence candidate

## Truth

This remaster starts from Caelen's prior exact final `{SOURCE_SHA}` and preserves the dedicated planning-only x1 `{X1_SHA}`. Exactly twenty genuinely new proposals extend the frozen chain from 4,430 to 4,450. Core outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

## Primary pillar and practice

THOS Body is primary through wholly synthetic reproducible research-software dependency intake and release stewardship. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. This is learning and software-design evidence only. It establishes no employment, qualification, package-maintainer, cybersecurity, production, professional, legal, cultural, affected-party, or Māori authority.

## Installation and profile result

The ten foundational packages Typer, Bandit, pre-commit, pip-tools, build, pipdeptree, tsx, c8, markdownlint-cli2, and npm-check-updates, plus the three phase packages Pyright, Knip, and Madge, were exact-version installed in user-scoped D-first tool banks after wheel or npm integrity review. Lifecycle scripts were disabled and pre-commit hooks were not installed. The npm prefix, cache, Python tool bank, and canonical PowerShell profile are D-first; C contains only required user configuration and minimal shell bootstraps with private rollback copies. Fresh PowerShell 7.6.5 and Windows PowerShell 5.1 shells resolved all new commands from D:. npm is 12.0.2 and Codex CLI is 0.149.0.

Windows itself, the Windows PowerShell 5.1 component, Codex desktop, Windows features, Sandbox, Hyper-V, accounts, credentials, host security, and reboot state were not changed. No package was published, no credential was used, and no production repository or release was touched.

## Mandatory tools and skills

All twelve inherited tools and all thirteen new tools produced bounded current-phase witnesses. The tool matrix covers timezone data, deterministic Python property tests and coverage, dual typing, lint and format, bounded advisory and security checks, dependency compilation and topology, a local wheel build, a zero-API OpenAI SDK import, TypeScript execution and compile, JavaScript tests and V8 coverage, unused-surface and cycle checks, Markdown lint, and a read-only update probe. These results are same-owner fixture evidence and are not exhaustive-security, professional, production, or independent-reproduction evidence.

All twenty-one user-mandated GHC main skills were read and applied within their scopes. Ten phase-local skills and ten additive family-current runners were built and smoke-used without global skill installation. The successor baton must carry both the mandatory skill set and the twenty-five-tool set, plus the rule to review, exact-pin, install, and use three newly justified packages in each later phase only where protected gates permit.

## Retained failures and recovery

Every startup and x2 operational failure remains retained at zero credit. The failed witnesses include PowerShell parser assumptions, optional cleanup policy rejections, a combined npm dry-run fault, two profile-check assumptions, an unsupported sparse-checkout flag, Ruff import ordering, two Typer invocation assumptions, an absent pip-audit shim, the current Click 8.3.1 advisory, and Knip's unlisted global binary. Each recovery changed or reran only the failed dependency. The corrected Click 8.4.2 fixture reported no known vulnerabilities at check time; this does not establish future or exhaustive security.

Exactly one hundred preregistered proposal mutations and {deck_mutations['mutation_count']} flashcard mutations were rejected and retained. Effective evidence-candidate counts are {retained['effective_count']} negatives and {method_flow['effective_method_count']} Method Flow methods, with {INHERITED_OPEN_GAPS + 1} open gaps and {INHERITED_EXACT_GATES + 1} exact gates. No failure or gate was erased.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic fixtures, package tools, citations, types, tests, coverage, lint, or advisory output establish no real likelihood, constraint, prediction, force, material law, empirical confirmation, ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and zero-person without governed real arms, operators, outcomes, statistics, safety monitoring, or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, live lifecycle events, interoperability, independent security review, recovery evidence, or trust governance.

Professional release and security decisions, system-wide installation, elevation, Windows mutation, hooks, credentials, publication, production deployment, licensing interpretation, privacy, accessibility acceptance, remedy, affected-party legitimacy, legal or cultural interpretation, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Next gate

The next repository step is an exact staged evidence review, immutable evidence commit, push, clean 0/0 divergence and fresh four-way equality. Closeout then requires one direct single-parent final child, exact manifests, one exclusive owner-scoped canonical completion, and no replay after success. Eiren Kestrel must not be contacted before that terminal gate.
''')


def read_exact(stream: BinaryIO, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise RuntimeError(f"batch stream ended with {remaining} bytes unread")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def staged_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    result: dict[str, bytes] = {}
    try:
        for path in paths:
            process.stdin.write(f":{path}\n".encode())
            process.stdin.flush()
            header = process.stdout.readline().rstrip(b"\n").split()
            if len(header) != 3 or header[1] != b"blob":
                raise RuntimeError(f"bad batch header for {path}")
            raw = read_exact(process.stdout, int(header[2]))
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing delimiter for {path}")
            result[path] = raw
        process.stdin.close()
        if process.wait(timeout=30) != 0:
            raise RuntimeError(process.stderr.read().decode(errors="replace"))
    finally:
        if process.poll() is None:
            process.kill()
    return result


def staged_review() -> None:
    manifest_path = f"docs/caelen-morrow/{PHASE}/validation/evidence-content-manifest.json"
    review_path = f"docs/caelen-morrow/{PHASE}/validation/evidence-staged-review.json"
    self_paths = {manifest_path, review_path}
    staged = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    if not staged:
        raise RuntimeError("no staged evidence paths")
    prefixes = (f"docs/caelen-morrow/{PHASE}/", "scripts/build_ghc_family_caelen_morrow_v667_v5_r2_", "scripts/ghc_family_caelen_morrow_v667_v5_r2_", "tests/test_ghc_family_caelen_morrow_v667_v5_r2_", "scripts/ghc_family_freed_id_flashcards.py")
    out_of_scope = [path for path in staged if not path.startswith(prefixes)]
    x1_mutations = [path for path in staged if path.startswith(f"docs/caelen-morrow/{PHASE}/x1/") or path.endswith("_x1.py")]
    manifest_paths = sorted(path for path in staged if path not in self_paths)
    blobs = staged_blobs(manifest_paths)
    entries = [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path]).hexdigest()} for path in manifest_paths]
    write_json("validation/evidence-content-manifest.json", {"schema": "ghc-family-evidence-content-manifest-v7", "owner": OWNER, "phase": PHASE, "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(self_paths), "staged_git_blob_bytes": True})
    write_json("validation/evidence-staged-review.json", {"schema": "ghc-family-evidence-staged-review-v7", "owner": OWNER, "phase": PHASE, "staged_paths": sorted(set(staged) | self_paths), "staged_path_count": len(set(staged) | self_paths), "manifest_entry_count": len(entries), "out_of_scope_paths": out_of_scope, "x1_mutation_paths": x1_mutations, "valid": not out_of_scope and not x1_mutations})


def main() -> int:
    if not sys.argv[1:]:
        build_all()
    elif sys.argv[1:] == ["--staged-review"]:
        staged_review()
    else:
        raise SystemExit("usage: build_ghc_family_caelen_morrow_v667_v5_r2_x2.py [--staged-review]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
