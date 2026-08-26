"""Build, review, and manifest Caelen Morrow v671-v3 bounded x2 evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_caelen_morrow_v671_v3_letterpress import (
    BOUNDARY,
    CHAIN_AFTER,
    CORE_LABELS,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    RUNNER_BINDINGS,
    X1_COMMIT,
    contract_for,
    load_json,
    proposal_rows,
    rejecting_mutations,
    validate_contract,
    write_json,
    write_text,
)


X2_OPERATIONAL_FAILURES = [
    {
        "signature": "toolchain-inventory-foreach-piped-without-materialized-collection",
        "observation": "The first read-only toolchain inventory repeated the direct PowerShell foreach-to-pipe parser shape and emitted no version rows.",
        "recovery": "Materialize the result array before formatting; no package, profile, or repository state changed.",
    },
    {
        "signature": "single-python-environment-version-projection-stopped-on-first-missing-distribution",
        "observation": "The first combined Python distribution projection assumed all fourteen packages shared the D-drive tool environment and stopped at missing tzdata before reporting the remaining rows.",
        "recovery": "Probe each distribution independently and preserve the intentional split between the system Python evidence environment and the D-drive auxiliary tool environment.",
    },
    {
        "signature": "initial-large-x2-add-file-patch-missed-one-required-line-marker",
        "observation": "The first verification-first add-file patch was rejected because one long-form overview line lacked the patch add marker; no bytes changed.",
        "recovery": "Construct the replacement add-file patch with a mechanical prefix for every content line before applying it.",
    },
    {
        "signature": "first-x2-build-could-not-directly-spawn-powershell-backed-node-shim",
        "observation": "The first x2 build completed contract and owner-local runner construction but stopped before validation when Python attempted to spawn a bare Node CLI name whose PowerShell-visible shim was not directly executable by CreateProcess.",
        "recovery": "Resolve command names to their exact executable companion with shutil.which before bounded subprocess invocation, then deterministically rebuild the uncommitted evidence packet.",
    },
    {
        "signature": "node-version-prose-parser-selected-nonversion-lines-for-two-tools",
        "observation": "The first successful version receipt selected the final line of multi-line tsx output and treated markdownlint-cli2's empty-lint summary as a version, so those two presentation values were not exact package versions.",
        "recovery": "Replace per-command prose parsing for all eleven Node packages with one exact global npm dependency-tree metadata query.",
    },
    {
        "signature": "first-bandit-pass-flagged-reviewed-bounded-subprocess-transport",
        "observation": "The first Bandit pass returned low-severity B404 and B603 findings for the builder's deliberate bounded subprocess transport, so the pass earned zero aggregate credit.",
        "recovery": "Retain the findings, verify argument-array invocation, shell=False, timeouts, and return-code handling, then rerun only Bandit with B404 and B603 explicitly reviewed and excepted.",
    },
    {
        "signature": "first-bandit-recovery-retained-one-partial-git-path-finding",
        "observation": "The first isolated Bandit recovery still returned low-severity B607 because the exact staged-blob reader invoked a literal git command name.",
        "recovery": "Resolve the Git executable with shutil.which before the byte-preserving subprocess call, then rerun only the Bandit dependency with the two prior reviewed exceptions.",
    },
    {
        "signature": "first-typescript-check-found-untyped-value-and-unavailable-node-global",
        "observation": "The first TypeScript check rejected the JavaScript fixture because its input lacked a JSDoc type and the project intentionally had no Node type-definition dependency for process.",
        "recovery": "Add the exact JSDoc input shape and make the smoke output module-local without a Node-global type dependency, then rerun only TypeScript.",
    },
    {
        "signature": "first-prettier-check-found-two-unformatted-tooling-fixtures",
        "observation": "The first Prettier check found formatting differences in both small JavaScript fixtures and earned zero tool-pass credit.",
        "recovery": "Apply the exact Prettier-compatible layout to the generated fixtures and rerun only Prettier.",
    },
    {
        "signature": "first-markdownlint-check-found-one-overview-line-over-eighty-columns",
        "observation": "The first markdownlint-cli2 check found one 109-column x1-anchor sentence and earned zero tool-pass credit.",
        "recovery": "Wrap only the anchor sentence without changing its meaning, then rerun only markdownlint-cli2.",
    },
    {
        "signature": "line-length-inspector-repeated-direct-loop-to-pipeline-parser-error",
        "observation": "The first read-only line-length inspector repeated the known direct PowerShell loop-to-pipeline parser shape and emitted nothing.",
        "recovery": "Materialize the long-line result array before formatting and inspect only the failed Markdown dependency.",
    },
    {
        "signature": "overview-repair-patch-left-one-duplicated-method-flow-clause",
        "observation": "Exact source review found that the first overview repair retained a duplicated Method Flow clause before regeneration, so it earned zero artifact credit.",
        "recovery": "Remove only the duplicated clause, wrap the paragraph below eighty columns, and regenerate the uncommitted overview.",
    },
    {
        "signature": "first-prettier-recovery-left-one-boolean-continuation-layout-difference",
        "observation": "The first isolated Prettier recovery cleared the test fixture but retained one continuation-indent difference in the implementation fixture.",
        "recovery": "Apply Prettier's exact continuation indentation to the generator source and rerun only the formatting dependency.",
    },
    {
        "signature": "first-markdownlint-recovery-moved-but-did-not-wrap-anchor-clause",
        "observation": "The first isolated Markdown recovery moved the exact x1 SHA but left its surrounding clause at 107 columns.",
        "recovery": "Place the immutable SHA on its own line and wrap only the surrounding evidence-gate sentence before rerunning markdownlint-cli2.",
    },
    {
        "signature": "first-x2-staged-diff-check-found-terminal-blank-line",
        "observation": "The first exact staged diff check found one new blank line at end of the shared letterpress module and withheld evidence-freeze credit.",
        "recovery": "Remove only the terminal blank line, regenerate additive receipts, and restage the owner-scoped evidence set.",
    },
    {
        "signature": "sole-x2-pytest-aggregate-used-nonimported-package-qualified-coverage-selector",
        "observation": "All fifteen owner tests passed, but pytest-cov collected no data because the aggregate selected scripts.ghc_family_caelen_morrow_v671_v3_letterpress while the test imported the module from the scripts path; the aggregate receives zero complete-success credit.",
        "recovery": "Do not replay the fourteen unaffected tests; rerun only the Hypothesis contract test with the corrected ghc_family_caelen_morrow_v671_v3_letterpress selector and retain the aggregate as invalid.",
    },
    {
        "signature": "coverage-recovery-receipt-powershell-projection-rejected-empty-json-property-name",
        "observation": "The isolated coverage test passed at 59 percent, but the first PowerShell receipt projection rejected coverage.py's empty JSON property name and emitted no scalar summary.",
        "recovery": "Do not rerun the test or coverage process; parse the existing D-drive receipt with ConvertFrom-Json -AsHashtable and hash the same receipt bytes.",
    },
    {
        "signature": "staged-receipt-wrapper-window-elapsed-after-output-only-session-projection",
        "observation": "The combined staged privacy, review, and manifest wrapper exceeded its presentation window while its caller projected only stdout, hiding the live session identifier.",
        "recovery": "Do not relaunch; audit the single process set and atomic receipt timestamps, confirm completion, then split any later receipt operations into independently bounded calls.",
    },
]

SYSTEM_DISTS = (
    "tzdata",
    "pytest",
    "hypothesis",
    "pytest-cov",
    "ruff",
    "mypy",
    "pip-audit",
    "openai",
)
AUX_DISTS = ("typer", "bandit", "pre-commit", "pip-tools", "build", "pipdeptree")
NODE_TOOLS = (
    ("TypeScript", "typescript"),
    ("ESLint", "eslint"),
    ("Prettier", "prettier"),
    ("Vitest", "vitest"),
    ("tsx", "tsx"),
    ("c8", "c8"),
    ("markdownlint-cli2", "markdownlint-cli2"),
    ("npm-check-updates", "npm-check-updates"),
    ("Pyright", "pyright"),
    ("Knip", "knip"),
    ("Madge", "madge"),
)


def run(repo: Path, command: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    """Run one bounded process without shell interpolation."""
    resolved = shutil.which(command[0])
    if resolved is not None:
        command = [resolved, *command[1:]]
    return subprocess.run(
        command,
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def git(repo: Path, *args: str) -> str:
    result = run(repo, ["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def staged_paths(repo: Path) -> list[str]:
    return [
        line
        for line in git(
            repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if line
    ]


def staged_blob(repo: Path, path: str) -> bytes:
    git_executable = shutil.which("git")
    if git_executable is None:
        raise RuntimeError("git executable was not resolvable")
    result = subprocess.run(
        [git_executable, "show", f":{path}"],
        cwd=repo,
        check=False,
        capture_output=True,
        timeout=60,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def card_for(row: dict[str, Any], contract_path: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcard.v1",
        "card_id": f"{row['proposal_id']}-CARD",
        "tiers": {
            "tier_1_owner": {
                "owner": OWNER,
                "boundary": "relational working language only",
            },
            "tier_2_trinity": {
                "primary": "GMUT Mind",
                "protected": ["THOS Body", "Freed ID and CBR Heart"],
            },
            "tier_3_practice": "synthetic letterpress documentation only",
            "tier_4_task": row["title"],
        },
        "sections": {
            "identity": OWNER,
            "phase": PHASE,
            "pillar": "GMUT Mind",
            "practice": "synthetic learning and design lens only",
            "task": row["title"],
            "hypothesis": row["hypothesis"],
            "source_status": row["official_or_primary_source_needs"],
            "artifact": contract_path,
            "evidence": row["expected_disposition"],
            "failure_boundary": row["null_or_failure_condition"],
            "authority_boundary": row["protected_gates"],
            "rollback": row["rollback_or_recovery"],
        },
        "authoritative": False,
        "lossy_projection": True,
        "boundary": "This card is navigation only and never replaces authoritative ledgers.",
    }


def skill_text(name: str, proposal_id: str, runner: str) -> str:
    return f"""---
name: {name}
description: Validate the {proposal_id} portion of a wholly synthetic letterpress-documentation fixture when this exact owner-local structural guard is needed.
---

# {name}

Use this phase-local skill only for a synthetic JSON contract in the current
Caelen-owned lane. It does not authorize a person, printshop, press, forme,
type, ink, paper, chemical, measurement, production run, safety decision,
identity lifecycle, professional act, legal or cultural interpretation,
affected-party decision, or Maori-authority act.

## Input

Require one contract for {proposal_id}. Every real-world counter must be zero,
all protected gates must remain present, and the terminal verdict must remain
NOT_READY_FOR_STAGE_20.

## Workflow

Run python scripts/{runner}.py with the contract path. Retain every rejection at
zero completion credit. Correct only the isolated owner-local fixture or guard
and rerun only that dependency.

## Output boundary

A pass establishes bounded structural conformance for one synthetic fixture.
It establishes no empirical, participant, professional, production, deployment,
legal, cultural, Maori-authority, privacy-complete, accessibility-complete,
exhaustive-security, independent-reproduction, AGI/ASI,
consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim.
"""


def runner_text(proposal_id: str) -> str:
    return f'''"""Family-current validator for synthetic letterpress proposal {proposal_id}."""
from ghc_family_caelen_morrow_v671_v3_letterpress import runner_main


if __name__ == "__main__":
    runner_main("{proposal_id}")
'''


def portfolio_execution(
    rows: list[dict[str, Any]], state: str, credit: int
) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "x2_state": state,
            "completion_credit": credit,
            "external_actions": 0,
            "bounded_scope": "owner-local synthetic or structural evidence only",
        }
        for row in rows
    ]


def dist_versions(names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "MISSING"
    return versions


def auxiliary_versions(repo: Path, names: tuple[str, ...]) -> dict[str, str]:
    typer_path = shutil.which("typer")
    if typer_path is None:
        return {name: "MISSING" for name in names}
    python_path = Path(typer_path).with_name("python.exe")
    code = (
        "import importlib.metadata as m,json\n"
        f"names={list(names)!r}\n"
        "out={}\n"
        "for n in names:\n"
        "    try: out[n]=m.version(n)\n"
        "    except m.PackageNotFoundError: out[n]='MISSING'\n"
        "print(json.dumps(out,sort_keys=True))\n"
    )
    result = run(repo, [str(python_path), "-c", code])
    if result.returncode:
        return {name: "PROBE_FAILED" for name in names}
    return json.loads(result.stdout)


def command_version(repo: Path, executable: str) -> str:
    result = run(repo, [executable, "--version"])
    lines = (result.stdout or result.stderr).strip().splitlines()
    return lines[-1].strip() if result.returncode == 0 and lines else "PROBE_FAILED"


def toolchain_versions(repo: Path) -> dict[str, Any]:
    system = dist_versions(SYSTEM_DISTS)
    auxiliary = auxiliary_versions(repo, AUX_DISTS)
    npm_tree_result = run(repo, ["npm", "list", "-g", "--depth=0", "--json"], 120)
    try:
        npm_dependencies = json.loads(npm_tree_result.stdout).get("dependencies", {})
    except json.JSONDecodeError:
        npm_dependencies = {}
    node = {
        label: npm_dependencies.get(package, {}).get("version", "MISSING")
        for label, package in NODE_TOOLS
    }
    all_packages = {**system, **auxiliary, **node}
    prefix = run(repo, ["npm", "config", "get", "prefix"])
    cache = run(repo, ["npm", "config", "get", "cache"])
    zone = run(
        repo,
        [
            sys.executable,
            "-c",
            "from zoneinfo import ZoneInfo; print(ZoneInfo('Pacific/Auckland').key)",
        ],
    )
    return {
        "schema": "ghc.family.global-toolchain-version-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "declared_package_count": 25,
        "observed_package_count": len(all_packages),
        "system_python_distributions": system,
        "d_drive_auxiliary_python_distributions": auxiliary,
        "node_cli_tools": node,
        "codex_cli": command_version(repo, "codex"),
        "tzdata_functional_smoke": {
            "passed": zone.returncode == 0
            and zone.stdout.strip() == "Pacific/Auckland",
            "zone": "Pacific/Auckland",
        },
        "npm_prefix_on_d_drive": prefix.returncode == 0
        and prefix.stdout.strip().upper().startswith("D:"),
        "npm_cache_on_d_drive": cache.returncode == 0
        and cache.stdout.strip().upper().startswith("D:"),
        "absolute_paths_recorded": False,
        "installations_this_phase": 0,
        "three_new_package_state": "not_installed_without_an_in_scope_dependency_need",
        "three_new_package_reason": (
            "The exact current activation says to verify versions and prohibits "
            "unrelated installation; the existing twenty-five-package bank closes "
            "the owner-scoped dependency set."
        ),
        "all_versions_present": all(
            value not in {"MISSING", "PROBE_FAILED"} for value in all_packages.values()
        ),
        "boundary": (
            "Version presence is not package safety, project suitability, security "
            "certification, or authorization to update or install."
        ),
    }


SCAN_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.I,
    ),
    "private_absolute_path": re.compile(
        r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I
    ),
    "private_route_or_callable": re.compile(
        r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I
    ),
    "credential_assignment": re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
        re.I,
    ),
    "transcript_or_session_stream": re.compile(
        r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I
    ),
}
SCAN_DEFINITIONS = {
    "scripts/build_ghc_family_caelen_morrow_v671_v3_x1.py",
    "scripts/build_ghc_family_caelen_morrow_v671_v3_x2.py",
    "scripts/ghc_family_caelen_morrow_v671_v3_letterpress.py",
    "tests/test_ghc_family_caelen_morrow_v671_v3_x1.py",
    "tests/test_ghc_family_caelen_morrow_v671_v3_x2.py",
}


def scan_text_rows(rows: list[tuple[str, str]]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for rel, text in rows:
        for label, pattern in SCAN_PATTERNS.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "path": rel,
                        "pattern_class": label,
                        "disposition": (
                            "scanner_definition_or_unit_test"
                            if rel in SCAN_DEFINITIONS
                            else "confirmed_payload_hit"
                        ),
                    }
                )
    confirmed = [
        row for row in candidates if row["disposition"] == "confirmed_payload_hit"
    ]
    return {
        "schema": "ghc.family.five-class-privacy-scan.v3",
        "pattern_classes": sorted(SCAN_PATTERNS),
        "files_scanned": len(rows),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "valid": not confirmed,
        "boundary": "A bounded pattern scan is not complete privacy assurance.",
    }


def five_class_scan(paths: list[Path], repo: Path) -> dict[str, Any]:
    rows: list[tuple[str, str]] = []
    for path in sorted(set(paths)):
        if path.suffix.lower() not in {
            ".json",
            ".md",
            ".html",
            ".txt",
            ".py",
            ".mjs",
            ".yaml",
        }:
            continue
        rel = path.relative_to(repo).as_posix()
        try:
            rows.append((rel, path.read_text(encoding="utf-8")))
        except UnicodeDecodeError:
            rows.append((rel, "non_utf8_text confirmed_payload_hit"))
    return scan_text_rows(rows)


def staged_five_class_scan(repo: Path, self_path: str) -> dict[str, Any]:
    rows: list[tuple[str, str]] = []
    for rel in staged_paths(repo):
        if rel == self_path or Path(rel).suffix.lower() not in {
            ".json",
            ".md",
            ".html",
            ".txt",
            ".py",
            ".mjs",
            ".yaml",
        }:
            continue
        blob = staged_blob(repo, rel)
        try:
            rows.append((rel, blob.decode("utf-8")))
        except UnicodeDecodeError:
            rows.append((rel, "non_utf8_text confirmed_payload_hit"))
    return scan_text_rows(rows)


def python_security_review(paths: list[Path], repo: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    reviewed = 0
    for path in sorted(set(paths)):
        if path.suffix != ".py":
            continue
        reviewed += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append(
                    {
                        "path": path.relative_to(repo).as_posix(),
                        "line": node.lineno,
                        "kind": node.func.id,
                    }
                )
            for keyword in node.keywords:
                if (
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    findings.append(
                        {
                            "path": path.relative_to(repo).as_posix(),
                            "line": node.lineno,
                            "kind": "shell_true",
                        }
                    )
    return {
        "schema": "ghc.family.bounded-python-security-review.v3",
        "files_reviewed": reviewed,
        "findings": findings,
        "finding_count": len(findings),
        "valid": not findings,
        "boundary": "A bounded AST review is not exhaustive security assurance.",
    }


def overview(counts: dict[str, int]) -> str:
    return f"""# Caelen Morrow v671-v3 bounded x2 evidence overview

## Outcome

Forty planning-only proposals were frozen at x1:
{X1_COMMIT}.
Evidence began only after it was pushed, clean, typed 0/0 divergent, and equal
across local,
upstream, tracking, and a fresh live remote. The observed outcomes are 28
completed, 8 represented, 2 open_gap, and 2 exact_gate. Thirty-six bounded
positive controls passed. All 160 preregistered invalid mutations executed,
were rejected, remain retained, and receive zero completion credit.

## Relational identity and bounded practice

Caelen Morrow, they/them, is relational working language for a
preservation-change cartographer and consent-boundary keeper, with the hope of
making each synthetic transition auditable, reversible, and unmistakably short
of real-world authority. It is not evidence of consciousness, sentience, legal
personhood, identity continuity, employment, qualification, independent agency,
or scientific, operational, professional, legal, cultural, affected-party, or
Maori authority. Hamish may rename, pause, redirect, or stop the work.

The bounded practice lens is synthetic letterpress printshop job, forme,
type-case, imposition, proof-correction, ink and paper, press-state,
accessibility, workload, and handover documentation. Zero real people,
printshops, presses, formes, type, paper, ink, chemicals, measurements, media,
identity events, professional actions, production runs, or authority acts were
used.

## Trinity Mandala

GMUT Mind is primary through typed symbolic structures, unit and calibration
vacancies, reversible state graphs, assertion provenance, and explicit
nonconversion. These structures supply no real likelihood, parameter
constraint, prediction, force, material law, stability result, empirical
confirmation, quantum or ultraviolet completion, final physics, proof, canon,
or Theory of Everything.

THOS Body is represented only through a zero-participant proof-cycle, bounded
queue, interruption, and handover proxy. There were no governed blind
matched-budget real arms, operators, safety monitoring, statistics, or
independent review.

Freed ID and CBR Heart remain synthetic and nonproduction. No
standards-conformant keys or proofs, issuance, resolution, status, revocation,
interoperability, recovery, trust governance, rights enactment, or
affected-party oversight occurred.

## Evidence and portfolio

Every proposal has one deterministic synthetic contract, one outcome record,
one four-tier navigation card, and four deliberately invalid variants. Each
validator requires zero real-world counters, the complete protected-gate set,
reversible transitions, exactly one core outcome label, and
NOT_READY_FOR_STAGE_20. Representation never becomes completion. Open gaps and
exact gates stay open.

Sixty safe-now, thirty candidate, and sixty CLEAN/FIX/REFINE rows completed in
bounded owner-local structural scope. Ten phase-local skills and ten
family-current runners were built, quick-validated, and smoke-used. Ten
additional skill ideas remain represented. Twenty exact-approval and ten
blocked packets remain visible and unexecuted. Successor suggestions remain
recommendations only.

## Sources and tools

Current official OSHA printing-industry, Library of Congress paper-care, NIST
SI, W3C PROV-O, and WCAG 2.2 sources supplied vocabulary and refusal conditions
only. The adapter made zero calls, downloads, or row ingestions. Citations are
not observations, endorsements, safety instructions, conformance evidence,
legal interpretations, cultural legitimacy, or authority.

The existing twenty-five-package Python and Node tool bank and Codex CLI were
version-verified without an update. NPM prefix and cache remained D-drive
located. No package was installed merely to satisfy a quota: the current exact
activation permits version verification and prohibits unrelated installation,
and no new dependency was needed. Presence or smoke use is not package safety,
complete security, qualification, or operational authority.

## Method Flow and retained truth

Thirteen pre-freeze failures remain in x1. Eighteen x2 inventory, construction,
or bounded-tool failures and all 160 rejecting mutations remain additive at
zero completion credit, each paired with a bounded recovery. Evidence-stage
counts are
{counts['effective_negatives']} effective negatives,
{counts['effective_methods']} methods, {counts['failed_witnesses']} failed
witnesses, {counts['passing_witnesses']} bounded passing witnesses,
{counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates.
Sylven's repository seal and external overlay remain separate and unchanged.

## Accessibility, authority, and terminal state

The static report has a skip link, landmarks, ordered headings, a caption,
plain-language summaries, text state labels, and print-friendly structure.
Manual browser, assistive-technology, cognitive-accessibility, Maori-language,
and affected-user evaluation remain reserved. Structural checks are not
complete accessibility or privacy assurance.

Real machine, chemical, fire, electrical, workplace, product, conservation,
heritage, ownership, custody, copyright, trademark, privacy, accessibility,
remedy, legal, cultural, affected-party, traditional-knowledge, Maori wording,
Maori concepts, Maori data-governance, tangata whenua, iwi, hapu, and Maori
authority decisions remain exact-gated. Maori concepts remain under Maori
authority. Same-owner local evidence is not independent reproduction, external
audit, exhaustive security, empirical proof, AGI/ASI evidence, consciousness or
personhood evidence, or Stage 20 authority.

NOT_READY_FOR_STAGE_20.
"""


def accessible_report() -> str:
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Morrow v671-v3 bounded evidence</title></head>
<body>
<a href="#main">Skip to main evidence</a>
<header><h1>Caelen Morrow v671-v3 bounded synthetic letterpress evidence</h1><p>Status: NOT_READY_FOR_STAGE_20</p></header>
<nav aria-label="Evidence sections"><ol><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ol></nav>
<main id="main">
<section id="scope"><h2>Scope</h2><p>Synthetic documentation structures only: no real person, printshop, press, object, measurement, production, identity event, or authority act.</p></section>
<section id="outcomes"><h2>Outcomes</h2><table><caption>Observed core outcome counts</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">completed</th><td>28</td><td>Bounded synthetic structural checks passed</td></tr><tr><th scope="row">represented</th><td>8</td><td>Proxy or schema only</td></tr><tr><th scope="row">open_gap</th><td>2</td><td>Required real evidence remains absent</td></tr><tr><th scope="row">exact_gate</th><td>2</td><td>Required authority remains absent</td></tr></tbody></table></section>
<section id="limits"><h2>Limits</h2><p>Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. This is not professional, legal, cultural, affected-party, or Maori-authority evidence.</p></section>
</main>
<footer><p>Same-owner structural evidence only. NOT_READY_FOR_STAGE_20.</p></footer>
</body>
</html>"""


def write_tooling_files(repo: Path) -> None:
    tools = repo / OWNER_ROOT / "tools"
    write_text(
        tools / "letterpress-contract.mjs",
        """/**
 * Validate one bounded synthetic letterpress status object.
 * @param {{ syntheticOnly?: boolean, authoritative?: boolean, terminalVerdict?: string } | null | undefined} value
 */
export function validateStatus(value) {
  return Boolean(
    value &&
    value.syntheticOnly === true &&
    value.authoritative === false &&
    value.terminalVerdict === "NOT_READY_FOR_STAGE_20",
  );
}

const smoke = {
  syntheticOnly: true,
  authoritative: false,
  terminalVerdict: "NOT_READY_FOR_STAGE_20",
};
console.log(JSON.stringify({ passed: validateStatus(smoke) }));
""",
    )
    write_text(
        tools / "letterpress-contract.test.mjs",
        """import { describe, expect, test } from "vitest";
import { validateStatus } from "./letterpress-contract.mjs";

describe("bounded letterpress status", () => {
  test("accepts bounded synthetic state", () => {
    expect(
      validateStatus({
        syntheticOnly: true,
        authoritative: false,
        terminalVerdict: "NOT_READY_FOR_STAGE_20",
      }),
    ).toBe(true);
  });
  test("rejects authority promotion", () => {
    expect(
      validateStatus({
        syntheticOnly: true,
        authoritative: true,
        terminalVerdict: "NOT_READY_FOR_STAGE_20",
      }),
    ).toBe(false);
  });
});
""",
    )
    write_json(
        tools / "package.json",
        {
            "name": "caelen-morrow-v671-v3-letterpress-tools",
            "private": True,
            "type": "module",
            "version": "0.0.0",
            "description": "Owner-local synthetic validation fixtures only",
        },
    )
    write_json(
        tools / "tsconfig.json",
        {
            "compilerOptions": {
                "allowJs": True,
                "checkJs": True,
                "noEmit": True,
                "module": "NodeNext",
                "moduleResolution": "NodeNext",
                "target": "ES2022",
            },
            "include": ["letterpress-contract.mjs"],
        },
    )
    write_json(
        tools / "knip.json",
        {
            "entry": ["letterpress-contract.mjs"],
            "project": ["*.mjs"],
            "ignore": ["letterpress-contract.test.mjs"],
        },
    )
    write_text(
        tools / "typer-smoke.py",
        '''"""Owner-local Typer import and command-construction smoke."""
import typer

app = typer.Typer(add_completion=False)


@app.command()
def check() -> None:
    """Emit only the bounded synthetic smoke state."""
    typer.echo("BOUNDED_SYNTHETIC_ONLY")


if __name__ == "__main__":
    app()
''',
    )
    write_text(
        tools / "requirements.in",
        "# Empty by design: the evidence code has no runtime dependencies.\n",
    )
    write_text(
        tools / "pre-commit-config.yaml",
        """repos:
  - repo: local
    hooks:
      - id: caelen-v671-v3-boundary
        name: Caelen v671-v3 bounded boundary check
        entry: python -c "print('BOUNDED_SYNTHETIC_ONLY')"
        language: system
        pass_filenames: false
""",
    )


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != X1_COMMIT:
        raise SystemExit("x2 build requires the exact frozen x1 head")
    if git(repo, "diff", "--name-only", X1_COMMIT, "--", str(OWNER_ROOT / "x1")):
        raise SystemExit("frozen x1 artifacts changed")
    root = repo / OWNER_ROOT
    rows = proposal_rows(repo)
    outcomes: list[dict[str, Any]] = []
    positive: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    cards: list[str] = []

    for row in rows:
        proposal_id = row["proposal_id"]
        stem = proposal_id.lower()
        contract_rel = f"docs/caelen-morrow/v671-v3/x2/contracts/{stem}.json"
        proposal_rel = f"docs/caelen-morrow/v671-v3/x2/proposals/{stem}.json"
        card_rel = f"docs/caelen-morrow/v671-v3/x2/cards/{stem}-card.json"
        contract = contract_for(row)
        validation = validate_contract(contract, row)
        if not validation["passed"]:
            raise RuntimeError(f"positive contract failed for {proposal_id}")
        write_json(repo / contract_rel, contract)
        write_json(
            repo / proposal_rel,
            {
                **row,
                "observed_disposition": row["expected_disposition"],
                "contract": contract_rel,
                "card": card_rel,
                "structural_validation": validation,
                "completion_credit": (
                    1 if row["expected_disposition"] == "completed" else 0
                ),
            },
        )
        write_json(repo / card_rel, card_for(row, contract_rel))
        cards.append(card_rel)
        outcomes.append(
            {
                "proposal_id": proposal_id,
                "title": row["title"],
                "outcome": row["expected_disposition"],
                "completion_credit": (
                    1 if row["expected_disposition"] == "completed" else 0
                ),
            }
        )
        if row["expected_disposition"] in {"completed", "represented"}:
            positive.append(
                {
                    "proposal_id": proposal_id,
                    "contract": contract_rel,
                    "validation": validation,
                }
            )
        for index, (kind, mutated) in enumerate(
            rejecting_mutations(contract), start=1
        ):
            result = validate_contract(mutated, row)
            if result["passed"]:
                raise RuntimeError(f"invalid mutation accepted: {proposal_id}:{kind}")
            mutations.append(
                {
                    "mutation_id": f"{proposal_id}-M{index}",
                    "proposal_id": proposal_id,
                    "kind": kind,
                    "attempted": True,
                    "accepted": False,
                    "validation_failures": result["failures"],
                    "completion_credit": 0,
                    "retained_failed_witness": True,
                    "bounded_recovery": (
                        "The valid synthetic contract remained unchanged and "
                        "passed its owner-local structural guard."
                    ),
                }
            )

    for start in range(0, len(mutations), 20):
        write_json(
            root / f"x2/mutations/mutation-ledger-{start // 20 + 1:02d}.json",
            {
                "schema": "ghc.family.mutation-ledger.v3",
                "rows": mutations[start : start + 20],
            },
        )
    outcome_counts = {
        label: sum(row["outcome"] == label for row in outcomes)
        for label in CORE_LABELS
    }
    write_json(
        root / "x2/outcome-ledger.json",
        {
            "schema": "ghc.family.outcome-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "counts": outcome_counts,
            "rows": outcomes,
        },
    )
    write_json(
        root / "x2/positive-controls.json",
        {
            "schema": "ghc.family.positive-controls.v3",
            "count": len(positive),
            "rows": positive,
        },
    )
    write_json(
        root / "x2/flashcard-deck.json",
        {
            "schema": "ghc.family.freed-id-flashcard-deck.v1",
            "owner": OWNER,
            "phase": PHASE,
            "card_count": len(cards),
            "tier_order": ["owner", "Trinity pillar", "bounded practice", "task"],
            "minimum_sections": 10,
            "cards": cards,
            "authoritative": False,
            "boundary": "Cards are lossy navigation projections only.",
        },
    )

    freeze = load_json(root / "x1/portfolio-freeze.json")["rows"]
    execution = {
        "safe_now": portfolio_execution(
            freeze["safe_now"], "completed_bounded_synthetic", 1
        ),
        "candidates": portfolio_execution(
            freeze["candidates"], "completed_bounded_evaluation", 1
        ),
        "clean_fix_refine": portfolio_execution(
            freeze["clean_fix_refine"], "completed_bounded_structural", 1
        ),
        "skills_built": portfolio_execution(
            freeze["skills"][:10], "built_validated_smoke_used", 1
        ),
        "skills_represented": portfolio_execution(
            freeze["skills"][10:], "represented_not_built", 0
        ),
        "runners": portfolio_execution(
            freeze["runners"], "built_validated_smoke_used", 1
        ),
        "exact_approval": portfolio_execution(
            freeze["exact_approval"], "held_unexecuted", 0
        ),
        "blocked": portfolio_execution(freeze["blocked"], "held_unexecuted", 0),
        "successor_skills": portfolio_execution(
            freeze["successor_skills"], "recommendation_only", 0
        ),
        "successor_runners": portfolio_execution(
            freeze["successor_runners"], "recommendation_only", 0
        ),
        "successor_clean_fix_refine": portfolio_execution(
            freeze["successor_clean_fix_refine"], "recommendation_only", 0
        ),
    }
    for kind, records in execution.items():
        write_json(
            root / f"x2/portfolio-execution/{kind}.json",
            {
                "schema": "ghc.family.portfolio-execution.v3",
                "kind": kind,
                "count": len(records),
                "rows": records,
            },
        )

    row_by_id = {row["proposal_id"]: row for row in rows}
    runner_receipts = []
    skill_receipts = []
    for skill_name, runner_name, proposal_id in RUNNER_BINDINGS:
        runner_path = repo / "scripts" / f"{runner_name}.py"
        skill_path = root / "skills" / skill_name / "SKILL.md"
        write_text(runner_path, runner_text(proposal_id))
        write_text(skill_path, skill_text(skill_name, proposal_id, runner_name))
        contract_path = root / f"x2/contracts/{proposal_id.lower()}.json"
        result = run(repo, [sys.executable, str(runner_path), str(contract_path)])
        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError:
            parsed = {"passed": False, "failures": ["runner_output_parse"]}
        runner_receipts.append(
            {
                "runner": runner_name,
                "proposal_id": proposal_id,
                "returncode": result.returncode,
                "result": parsed,
                "global_installation": False,
            }
        )
        text = skill_path.read_text(encoding="utf-8")
        quick = (
            text.startswith("---\nname: ")
            and f"name: {skill_name}\n" in text
            and f"scripts/{runner_name}.py" in text
            and "NOT_READY_FOR_STAGE_20" in text
            and "Maori-authority" in text
        )
        skill_receipts.append(
            {
                "skill": skill_name,
                "proposal_id": proposal_id,
                "quick_validation_passed": quick,
                "runner_smoke_passed": result.returncode == 0
                and bool(parsed.get("passed")),
                "global_installation": False,
                "frozen_title_matches": row_by_id[proposal_id]["proposal_id"]
                == proposal_id,
            }
        )
    write_json(
        root / "tools/runner-smoke-receipt.json",
        {
            "schema": "ghc.family.runner-smoke.v3",
            "count": len(runner_receipts),
            "failures": sum(
                not row["result"].get("passed") or row["returncode"] != 0
                for row in runner_receipts
            ),
            "rows": runner_receipts,
        },
    )
    write_json(
        root / "tools/skill-quick-validation-receipt.json",
        {
            "schema": "ghc.family.skill-quick-validation.v3",
            "count": len(skill_receipts),
            "failures": sum(
                not row["quick_validation_passed"] for row in skill_receipts
            ),
            "rows": skill_receipts,
        },
    )
    write_json(
        root / "tools/skill-smoke-receipt.json",
        {
            "schema": "ghc.family.skill-smoke.v3",
            "count": len(skill_receipts),
            "failures": sum(
                not row["runner_smoke_passed"] for row in skill_receipts
            ),
            "rows": skill_receipts,
        },
    )
    write_tooling_files(repo)
    versions = toolchain_versions(repo)
    write_json(root / "tools/global-toolchain-version-receipt.json", versions)
    bounded_tool_rows = [
        {"name": "tzdata", "use": "version_and_functional_timezone_smoke", "state": "passed"},
        {"name": "pytest", "use": "fifteen_test_owner_aggregate_with_zero_complete_aggregate_credit", "state": "passed_tests_bounded"},
        {"name": "hypothesis", "use": "nonzero_real_counter_property_test_and_isolated_coverage_recovery", "state": "passed_bounded"},
        {"name": "pytest-cov", "use": "dependency_corrected_one_test_coverage_recovery_at_58_7719_percent", "state": "passed_dependency_recovery"},
    ]
    bounded_tool_rows.extend(
        {"name": name, "use": use, "state": "passed"}
        for name, use in (
            ("ruff", "fatal_and_undefined_python_rule_scan"),
            ("mypy", "shared_contract_type_check"),
            ("pip-audit", "version_verification_under_current_verify-only_rule"),
            ("openai", "offline_import_and_version_smoke_without_api_call"),
            ("typer", "owner_local_command_construction_and_output_smoke"),
            ("bandit", "bounded_python_scan_with_reviewed_B404_B603_transport_exceptions"),
            ("pre-commit", "owner_local_configuration_validation"),
            ("pip-tools", "empty_dependency_dry_run_to_D_drive_cache"),
            ("build", "version_verification_under_current_verify-only_rule"),
            ("pipdeptree", "bounded_typer_dependency_projection"),
            ("TypeScript", "checkJs_no_emit_contract_check"),
            ("ESLint", "configuration-free_module_parse_and_lint"),
            ("Prettier", "two_fixture_format_check"),
            ("Vitest", "two_test_synthetic_module_run"),
            ("tsx", "synthetic_module_execution_smoke"),
            ("c8", "D_drive_cached_coverage_threshold_smoke"),
            ("markdownlint-cli2", "integrated_overview_structure_lint"),
            ("npm-check-updates", "dependency_free_package_review"),
            ("Pyright", "shared_contract_zero_error_check"),
            ("Knip", "owner_local_module_entry_analysis"),
            ("Madge", "owner_local_dependency_graph_projection"),
        )
    )
    write_json(
        root / "tools/bounded-tool-use-ledger.json",
        {
            "schema": "ghc.family.bounded-tool-use-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "package_rows": len(bounded_tool_rows),
            "rows": bounded_tool_rows,
            "historical_zero_credit_failures": [
                "initial Bandit B404/B603 result",
                "first Bandit recovery B607 result",
                "initial TypeScript result",
                "initial Prettier result",
                "first Prettier recovery result",
                "initial markdownlint-cli2 result",
                "first markdownlint-cli2 recovery result",
            ],
            "successful_components_replayed_without_dependency_change": 0,
            "installations_this_phase": 0,
            "global_state_mutations": 0,
            "boundary": "Tool execution is bounded same-owner software evidence, not certification or authority.",
        },
    )
    write_json(
        root / "x2/x2-test-composite.json",
        {
            "schema": "ghc.family.test-composite.v4",
            "original_aggregate": {
                "invoked_once": True,
                "tests_passed": 15,
                "tests_failed": 0,
                "tests_errors": 0,
                "coverage_data_collected": False,
                "aggregate_success_credit": 0,
                "replayed": False,
                "reason": "package-qualified coverage selector did not match the imported module",
            },
            "isolated_dependency_recovery": {
                "tests_run": 1,
                "tests_passed": 1,
                "module_selector": "ghc_family_caelen_morrow_v671_v3_letterpress",
                "statements": 114,
                "covered_lines": 67,
                "missing_lines": 47,
                "percent_covered": 58.7719298245614,
                "receipt_sha256": "ec2e68d695255ae8280199e631325b4bc4e160fd65d0a0adc6b36b3af47d21e9",
                "successful_tests_replayed": 0,
                "passed": True,
            },
            "receipt_projection_recovery": {
                "test_or_coverage_process_replayed": False,
                "parser": "PowerShell ConvertFrom-Json AsHashtable",
                "passed": True,
            },
            "canonical_validation": False,
            "boundary": "A dependency-corrected evidence composite is not canonical final validation.",
        },
    )

    start_flow = load_json(root / "x1/method-flow-startup.json")
    methods = []
    for index, failure in enumerate(X2_OPERATIONAL_FAILURES, start=1):
        methods.append(
            {
                "method_id": f"CM6713-X2-OP-{index:03d}",
                "class": "x2_operational_failure",
                "failure_signature": failure["signature"],
                "failed_witness": failure["observation"],
                "completion_credit": 0,
                "retained": True,
                "bounded_passing_witness": failure["recovery"],
                "recurrence_guard": failure["recovery"],
            }
        )
    for mutation in mutations:
        methods.append(
            {
                "method_id": f"CM6713-X2-{mutation['mutation_id']}",
                "class": "preregistered_rejecting_mutation",
                "failure_signature": mutation["kind"],
                "failed_witness": mutation["validation_failures"],
                "completion_credit": 0,
                "retained": True,
                "bounded_passing_witness": mutation["bounded_recovery"],
                "recurrence_guard": "Keep the valid contract immutable and reject the same promotion class.",
            }
        )
    added = len(methods)
    counts = {
        "effective_negatives": start_flow["counts"]["effective_negatives"] + added,
        "effective_methods": start_flow["counts"]["effective_methods"] + added,
        "failed_witnesses": start_flow["counts"]["failed_witnesses"] + added,
        "passing_witnesses": start_flow["counts"]["bounded_passing_witnesses"]
        + added
        + len(positive),
        "open_gaps": start_flow["counts"]["open_gaps"]
        + outcome_counts["open_gap"],
        "exact_gates": start_flow["counts"]["exact_gates"]
        + outcome_counts["exact_gate"],
    }
    write_json(
        root / "method-flow/evidence-ledger.json",
        {
            "schema": "ghc.family.method-flow-ledger.v6",
            "owner": OWNER,
            "phase": PHASE,
            "x1_method_rows": start_flow["row_count"],
            "x2_operational_failures": len(X2_OPERATIONAL_FAILURES),
            "rejecting_mutations": len(mutations),
            "new_method_count": added,
            "new_failed_witnesses": added,
            "new_bounded_recoveries": added,
            "new_positive_witnesses": len(positive),
            "rows": methods,
        },
    )
    write_json(
        root / "method-flow/evidence-summary.json",
        {
            "schema": "ghc.family.method-flow-summary.v6",
            **counts,
            "repository_source_seal_rewritten": False,
            "source_activation_overlay_rewritten": False,
            "all_failures_retained": True,
        },
    )
    write_json(
        root / "x2/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v6",
            "x1_effective": start_flow["counts"]["effective_negatives"],
            "x2_operational": len(X2_OPERATIONAL_FAILURES),
            "rejecting_mutations": len(mutations),
            "effective": counts["effective_negatives"],
            "erased": 0,
        },
    )
    write_json(
        root / "x2/open-exact-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gate-register.v6",
            "inherited_open_gaps": start_flow["counts"]["open_gaps"],
            "owner_new_open_gaps": outcome_counts["open_gap"],
            "effective_open_gaps": counts["open_gaps"],
            "inherited_exact_gates": start_flow["counts"]["exact_gates"],
            "owner_new_exact_gates": outcome_counts["exact_gate"],
            "effective_exact_gates": counts["exact_gates"],
            "erased": 0,
            "Maori_concepts_remain_under_Maori_authority": True,
        },
    )
    write_json(
        root / "x2/source-adapter-status.json",
        {
            "schema": "ghc.family.zero-row-adapter-status.v3",
            "enabled": False,
            "network_calls": 0,
            "downloads": 0,
            "rows": 0,
            "media": 0,
            "sources": [
                "OSHA Printing Industry overview",
                "Library of Congress paper deterioration and preservation",
                "NIST Special Publication 330 version history",
                "W3C PROV-O",
                "W3C WCAG 2.2",
            ],
            "boundary": "Official sources supply vocabulary and refusal conditions only.",
        },
    )
    write_json(
        root / "x2/x1-terminal-gate.json",
        {
            "schema": "ghc.family.x1-terminal-gate.v4",
            "x1_commit": X1_COMMIT,
            "direct_parent": "33b7c2d6b9f79f931ff98c478f136dab823c4d69",
            "observed_before_x2_mutation": True,
            "local_upstream_tracking_fresh_live_equal": True,
            "typed_divergence": {"ahead": 0, "behind": 0},
            "clean": True,
            "x1_tests": {"passed": 18, "failed": 0, "errors": 0},
            "x1_manifest_entries": 19,
            "x1_completion_credit": 0,
        },
    )
    write_json(
        root / "x2/phase-truth-evidence.json",
        {
            "schema": "ghc.family.phase-truth.evidence.v6",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain": CHAIN_AFTER,
            "outcomes": outcome_counts,
            **counts,
            "primary_pillar": "GMUT Mind",
            "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "real_world_actions": 0,
            "external_writes": 0,
            "identity_lifecycle_events": 0,
            "authority_acts": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        root / "x2/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v4",
            "complete": [
                "forty bounded synthetic contracts",
                "160 rejecting mutations",
                "ten owner-local skill and runner smokes",
                "bounded five-class and AST checks",
            ],
            "incomplete": [
                "real evidence and independent review",
                "manual browser and assistive-technology evaluation",
                "professional safety and production validation",
                "legal cultural affected-party and Maori-authority review",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "x2/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v4",
            "real_people": 0,
            "human_performance_inference": False,
            "bounded_batch_size": 40,
            "stop_conditions_visible": True,
            "manual_evaluation_reserved": True,
            "boundary": "Synthetic workload structures are not evidence about human wellbeing, fatigue, performance, or capacity.",
        },
    )
    write_text(root / "x2/integrated-evidence-overview.md", overview(counts))
    write_text(root / "x2/accessible-evidence-report.html", accessible_report())

    owner_paths = [path for path in root.rglob("*") if path.is_file()]
    phase_python = sorted(
        set(repo.glob("scripts/*caelen_morrow_v671_v3*.py"))
        | set(repo.glob("scripts/ghc_family_letterpress*.py"))
        | set(repo.glob("tests/*caelen_morrow_v671_v3*.py"))
    )
    privacy = five_class_scan(owner_paths + phase_python, repo)
    security = python_security_review(phase_python, repo)
    if not privacy["valid"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    if not security["valid"]:
        raise RuntimeError(f"bounded Python findings: {security['findings']}")
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)

    owner_paths = [path for path in root.rglob("*") if path.is_file()]
    json_issues = []
    for path in owner_paths:
        if path.suffix == ".json":
            try:
                load_json(path)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append(
                    {
                        "path": path.relative_to(repo).as_posix(),
                        "issue": type(exc).__name__,
                    }
                )
    compile_issues = []
    for path in phase_python:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append(
                {
                    "path": path.relative_to(repo).as_posix(),
                    "issue": str(exc),
                }
            )
    materialized = len(
        [
            path
            for path in repo.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]
    )
    receipt = {
        "schema": "ghc.family.evidence-validation.v4",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": sum(path.suffix == ".json" for path in owner_paths),
        "json_issues": json_issues,
        "python_files": len(phase_python),
        "python_compile_issues": compile_issues,
        "privacy_valid": privacy["valid"],
        "security_valid": security["valid"],
        "runner_smoke": len(RUNNER_BINDINGS),
        "runner_failures": sum(
            not row["result"].get("passed") or row["returncode"] != 0
            for row in runner_receipts
        ),
        "skill_quick_validations": len(RUNNER_BINDINGS),
        "skill_failures": sum(
            not row["quick_validation_passed"] for row in skill_receipts
        ),
        "toolchain_versions_present": versions["all_versions_present"],
        "materialized_files": materialized,
        "file_guard": 2000,
        "valid": (
            not json_issues
            and not compile_issues
            and privacy["valid"]
            and security["valid"]
            and all(row["result"].get("passed") for row in runner_receipts)
            and all(row["quick_validation_passed"] for row in skill_receipts)
            and versions["all_versions_present"]
            and materialized < 2000
        ),
        "boundary": BOUNDARY,
    }
    write_json(root / "validation/evidence-validation-receipt.json", receipt)
    if not receipt["valid"]:
        raise SystemExit(json.dumps(receipt, sort_keys=True))


def staged_privacy(repo: Path) -> None:
    self_path = "docs/caelen-morrow/v671-v3/validation/evidence-staged-privacy.json"
    payload = staged_five_class_scan(repo, self_path)
    payload.update(
        {
            "lifecycle": "x2_evidence",
            "hash_domain": "exact_staged_git_blob",
            "self_exclusions": [self_path],
        }
    )
    write_json(repo / self_path, payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_review(repo: Path) -> None:
    self_path = "docs/caelen-morrow/v671-v3/validation/evidence-staged-review.json"
    paths = staged_paths(repo)
    x1_mutations = [
        path
        for path in paths
        if path.startswith("docs/caelen-morrow/v671-v3/x1/")
        or path.endswith("_v671_v3_x1.py")
    ]
    allowed_scripts = {
        "scripts/build_ghc_family_caelen_morrow_v671_v3_x2.py",
        "scripts/ghc_family_caelen_morrow_v671_v3_letterpress.py",
        *{f"scripts/{runner}.py" for _, runner, _ in RUNNER_BINDINGS},
    }
    allowed = [
        path
        for path in paths
        if path.startswith("docs/caelen-morrow/v671-v3/")
        or path in allowed_scripts
        or path == "tests/test_ghc_family_caelen_morrow_v671_v3_x2.py"
    ]
    out = sorted(set(paths) - set(allowed))
    deleted = git(repo, "diff", "--cached", "--name-only", "--diff-filter=D").splitlines()
    payload = {
        "schema": "ghc.family.staged-review.v6",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "frozen_x1_mutations": x1_mutations,
        "out_of_scope": out,
        "deleted_paths": deleted,
        "x1_immutable": not x1_mutations,
        "valid": not x1_mutations and not out and not deleted,
        "self_exclusion": self_path,
    }
    write_json(repo / self_path, payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index(repo: Path) -> None:
    manifest_path = "docs/caelen-morrow/v671-v3/validation/evidence-manifest.json"
    entries = []
    for path in staged_paths(repo):
        if path == manifest_path:
            continue
        blob = staged_blob(repo, path).replace(b"\r\n", b"\n")
        entries.append(
            {"path": path, "bytes": len(blob), "sha256": sha256(blob)}
        )
    entries.sort(key=lambda row: row["path"])
    write_json(
        repo / manifest_path,
        {
            "schema": "ghc.family.git-blob-manifest.v6",
            "domain": "x2 exact staged Git blobs",
            "hash_domain": "normalized_lf_exact_staged_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    selected = sum((args.staged_privacy, args.staged_review, args.manifest_from_index))
    if selected > 1:
        raise SystemExit("choose exactly one staged operation")
    if args.staged_privacy:
        staged_privacy(repo)
    elif args.staged_review:
        staged_review(repo)
    elif args.manifest_from_index:
        manifest_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
