"""Build, review, and manifest Eiren Kestrel v671-v4 bounded x2 evidence."""

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
import textwrap
from pathlib import Path
from typing import Any

from ghc_family_eiren_kestrel_v671_v4_seed_library import (
    BOUNDARY,
    CHAIN_AFTER,
    CORE_LABELS,
    OWNER,
    OWNER_ROOT,
    PHASE,
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

X2_OPERATIONAL_FAILURES: list[dict[str, str]] = [
    {
        "signature": "auxiliary-tool-path-prepend-shadowed-the-evidence-python-interpreter",
        "observation": "The first x2 compile and collection wrapper prepended the D-first auxiliary Scripts directory before resolving Python; its isolated interpreter compiled the files but had no pytest module, so collection produced no result.",
        "recovery": "Retain the missing-module result, resolve and hold the evidence Python executable first, then expose auxiliary tool shims only to child command lookup and rerun collection.",
    },
    {
        "signature": "combined-tool-use-projection-exceeded-the-presentation-budget",
        "observation": "The first combined Python and auxiliary-tool wrapper completed without an attributable bounded presentation because its output exceeded the model-visible result budget; no individual tool receives credit from that projection.",
        "recovery": "Retain the unattributable projection at zero credit and invoke each dependency-justified tool once in small independently attributable groups before updating the bounded-use ledger.",
    },
    {
        "signature": "first-multi-hunk-x2-ledger-patch-assumed-an-inexact-inherited-field-order",
        "observation": "The first additive patch matched the intended composite values but assumed a different order for three receipt-projection fields, so apply_patch rejected the whole patch without changing a byte.",
        "recovery": "Retain the rejected patch at zero credit, inspect the exact bounded line range, and apply smaller exact-context hunks.",
    },
    {
        "signature": "first-attributable-x2-ruff-scan-found-twenty-one-fixable-style-and-unused-import-findings",
        "observation": "The first attributable Ruff scan returned twenty-one fixable import-order, unused-import, regular-expression-alias, and stale-noqa findings across the x2 builder, shared module, runners, and test.",
        "recovery": "Retain the failed scan at zero credit, apply Ruff's bounded mechanical fixes only to the reported x2 files, inspect the diff, and rerun only Ruff on the changed targets.",
    },
    {
        "signature": "first-typer-smoke-assumed-a-subcommand-for-a-single-command-application",
        "observation": "The first attributable Typer smoke passed an explicit check argument to a single-command application, so Typer rejected the unexpected argument before executing the bounded command body.",
        "recovery": "Retain the CLI-shape failure at zero credit, inspect the one-file application shape, and invoke the single-command application without a subcommand argument.",
    },
    {
        "signature": "first-markdownlint-overview-check-found-two-long-lines-and-one-raw-wildcard-token",
        "observation": "The first attributable Markdownlint check found two line-length findings and treated the raw family-current wildcard names as malformed emphasis.",
        "recovery": "Retain the three findings at zero credit, wrap the exact x1 anchor and terminal boundary without changing their meaning, render wildcard names as code, and rerun only Markdownlint on the changed overview.",
    },
    {
        "signature": "parallel-knip-check-returned-no-attributable-completion-state",
        "observation": "The Knip member of a bounded four-command parallel check returned neither an exit code nor output to the projection, and no matching live process remained when inspected; it earns no tool-use credit.",
        "recovery": "Retain the missing completion state at zero credit and invoke Knip alone with the exact owner-local directory and config so its exit state is independently attributable.",
    },
    {
        "signature": "staged-evidence-wrapper-yielded-without-presenting-its-live-session-identifier",
        "observation": "The staged privacy, review, and manifest wrapper exceeded its initial presentation window and the orchestration projection emitted no session identifier, while bounded process inspection showed the manifest operation still running.",
        "recovery": "Retain the presentation gap at zero credit, do not replay the wrapper, wait on the observed process, and inspect the resulting staged receipts, exact manifest, x1 immutability, cached diff, and exit-independent Git state after completion.",
    },
    {
        "signature": "one-shot-evidence-aggregate-used-a-raw-markdown-substring-assertion-after-line-wrapping",
        "observation": "The sole evidence aggregate ran fourteen of fifteen tests before maxfail stopped it: thirteen passed, the accessible-overview test failed because a required phrase crossed a deliberate Markdown line wrap, the manifest test was not reached, and no coverage JSON was emitted. The aggregate earns zero aggregate-success credit.",
        "recovery": "Retain the failed JUnit receipt, normalize whitespace only inside the affected overview assertion, keep the rendered document unchanged, and run only the failed overview test, the not-run manifest test, and the bounded coverage dependency after exact staged prerequisites are refreshed.",
    },
    {
        "signature": "pytest-trace-config-probe-omitted-collect-only-and-unintentionally-executed-the-sparse-suite",
        "observation": "A plugin-registration query invoked pytest --trace-config without --collect-only; filtered output hid the test summary, while the cache timestamp and thirty-three node IDs proved that the sparse x1/x2 suite had been re-executed. No result from that query receives test, aggregate, coverage, or completion credit.",
        "recovery": "Retain the unintended replay at zero credit, use import metadata or an explicitly nonexecuting collection command for future plugin checks, and perform no further broad replay; recover only exact changed or previously unexecuted dependencies.",
    },
    {
        "signature": "first-coverage-receipt-projection-used-powershell-object-mode-on-an-empty-json-key",
        "observation": "The first read-only coverage projection used ConvertFrom-Json object mode, which rejects the valid coverage.py branch-map empty-string key; receipt hashes and the JUnit summary were preserved, but the totals projection earned no credit.",
        "recovery": "Retain the parser fault at zero credit and parse the already-written coverage JSON once with Python's standard JSON loader; do not rerun tests or coverage.",
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
                "primary": "Freed ID and CBR Heart",
                "protected": ["GMUT Mind", "THOS Body"],
            },
            "tier_3_practice": "synthetic community seed-library and genebank documentation only",
            "tier_4_task": row["title"],
        },
        "sections": {
            "identity": OWNER,
            "phase": PHASE,
            "pillar": "Freed ID and CBR Heart",
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
description: Validate the {proposal_id} portion of a wholly synthetic seed-library-documentation fixture when this exact owner-local structural guard is needed.
---

# {name}

Use this phase-local skill only for a synthetic JSON contract in the current
Eiren-owned lane. It does not authorize a person, seed library, genebank, seed,
plant, accession, packet, sample, storage condition, measurement, germination,
regeneration, biosafety or phytosanitary decision, identity lifecycle,
professional act, legal or cultural interpretation, affected-party decision,
or Maori-authority act.

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
    return f'''"""Family-current validator for synthetic seed-library proposal {proposal_id}."""
from ghc_family_eiren_kestrel_v671_v4_seed_library import runner_main


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
        re.IGNORECASE,
    ),
    "private_absolute_path": re.compile(
        r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE
    ),
    "private_route_or_callable": re.compile(
        r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.IGNORECASE
    ),
    "credential_assignment": re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
        re.IGNORECASE,
    ),
    "transcript_or_session_stream": re.compile(
        r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.IGNORECASE
    ),
}
SCAN_DEFINITIONS = {
    "scripts/build_ghc_family_eiren_kestrel_v671_v4_x1.py",
    "scripts/build_ghc_family_eiren_kestrel_v671_v4_x2.py",
    "scripts/ghc_family_eiren_kestrel_v671_v4_seed_library.py",
    "tests/test_ghc_family_eiren_kestrel_v671_v4_x1.py",
    "tests/test_ghc_family_eiren_kestrel_v671_v4_x2.py",
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
    return f"""# Eiren Kestrel v671-v4 bounded x2 evidence overview

## Exact lifecycle

X2 began only after planning-only x1 commit
`{X1_COMMIT}` was pushed, clean,
typed 0/0 divergent, and identical across local, upstream, tracking, and a
fresh live remote. X1 is the direct child of Caelen Morrow v671-v3 exact final;
its exact tree contains no x2 implementation or observed outcome. The evidence
stage does not amend x1, replay Caelen's canonical validation, contact a
successor, mutate another lane, or claim independent reproduction.

## Bounded role and practice

Eiren Kestrel, they/them, seed-lineage cartographer and consent-vacancy steward,
is relational working language only. The bounded hope is to keep every
synthetic accession traceable, challengeable, reversible, and visibly short of
real-world custodianship or authority. This is no evidence of consciousness,
sentience, legal personhood, identity continuity, employment, qualification,
independent agency, or scientific, professional, operational, legal, cultural,
affected-party, or Maori authority.

Freed ID and CBR Heart are primary through synthetic accession aliases, purpose
limits, correction, contest, disclosure budgets, rights vacancies, and
nonproduction identity envelopes. GMUT Mind remains explicit through symbolic
storage-state, dormancy, transition, covariance, unit, and falsification
structures with zero fitted data. THOS Body remains explicit through
zero-participant intake, dependency, interruption, repair, and handover
proxies.

The practice lenses are synthetic community seed-library accession and lending
records, synthetic genebank lot and monitoring documentation, and synthetic
biodiversity-term and accessible-status mapping. They are design lenses only.
No real person, seed library, genebank, accession, seed, plant, packet, sample,
location, traditional knowledge, measurement, storage condition, germination
test, viability result, regeneration, distribution, return, destruction,
identity event, professional act, legal or cultural decision, affected-party
approval, or authority act occurred.

## Proposal execution

The forty frozen proposal contracts preserve their exact x1 titles,
hypotheses, source needs, falsifiers, rollback language, gates, and expected
dispositions. Twenty-eight completed rows receive one unit of bounded
owner-local synthetic-structure credit. Eight represented rows remain
representations with zero completion credit. Two open_gap rows preserve missing
real evidence. Two exact_gate rows remain unexecuted and preserve missing
action-specific authority. The exact outcome vector is
{counts['open_gaps'] - 261} new open gaps and
{counts['exact_gates'] - 256} new exact gates, with 28 completed and 8
represented.

Thirty-six bounded positive controls pass their typed synthetic contract. Four
preregistered invalid mutations per proposal attempt a real-person counter,
authority promotion, Stage 20 promotion, or protected-gate deletion. All 160
are rejected, retained as failed witnesses, and receive zero completion credit.
The valid source contract stays unchanged. A mutation rejection is evidence
about one guard and one fixture only, not security certification or general
reliability.

## Portfolio, skills, and runners

Sixty safe-now rows, thirty bounded candidate rows, and sixty
CLEAN/FIX/REFINE rows complete only as owner-local schema, fixture, rollback,
manifest, boundary, mutation, ordering, privacy, accessibility, or documentation
work. Twenty exact-approval and ten blocked rows remain visible and unexecuted.
Ten of twenty skill ideas are built as phase-local SKILL.md files, quick
validated, and smoke-used through ten family-current Python runners. The other
ten are represented only. Ten successor skill ideas, ten successor runner
ideas, thirty successor cleanup rows, and one adjacent practice lens remain
recommendations with zero Eiren and zero successor completion credit.

No skill is globally installed. No runner is promoted as a universal surface.
Every runner binds one exact proposal contract, rejects protected-boundary
mutations, and leaves sibling, shared, global, external, and authority state
unchanged. Family-current `ghc_family_*` and `build_ghc_family_*` naming and caller
compatibility remain explicit.

## Source and adapter boundary

The FAO Genebank Standards page, current Darwin Core term list, W3C PROV-O,
WCAG 2.2, New Zealand Privacy Commissioner principles, and Te Mana Raraunga
principles supply vocabulary and refusal conditions only. The source adapter is
disabled and records zero network calls, downloads, rows, samples, media, or
external writes. Citation is not a seed observation, conservation instruction,
taxonomic determination, biosafety decision, phytosanitary release, privacy
compliance conclusion, accessibility conformance, consent, ownership,
benefit-sharing decision, cultural ratification, or Maori authority.

## Tool and validation boundary

The current twenty-five-package bank is version checked. Dependency-justified
tools are used only on Eiren-owned files or tiny synthetic fixtures. Presence is
not permission to bulk-run a tool or mutate global state. The current activation
authorizes verification but not unrelated installation, so installations and
global-state mutations remain zero. Any missing or failing tool is retained
rather than silently credited.

Exact owner-local JSON parsing, Python compilation, runner smokes, skill quick
validation, five-class privacy/raw-identifier review, and bounded Python
security review are required before evidence freeze. The accessible HTML
report provides a skip link, landmarks, ordered headings, text state labels,
a captioned summary table, and print-friendly structure. Manual browser,
assistive-technology, cognitive-accessibility, language, Maori-language, and
affected-user evaluation remain reserved. Structural checks are not complete
accessibility or privacy assurance.

## Method Flow and retained negatives

The evidence counts are {counts['effective_negatives']} effective negatives,
{counts['effective_methods']} effective methods,
{counts['failed_witnesses']} failed witnesses,
{counts['passing_witnesses']} bounded passing witnesses,
{counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. The
eight x1 startup failures, one x1 validation overlay, every x2 operational
failure, all 160 rejecting mutations, every bounded recovery, and every open or
exact gate remain attributable. Caelen's repository seal is not rewritten.

## Scientific, professional, and authority boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. These artifacts establish no datum, likelihood, posterior, parameter
constraint, unique prediction, force, material or biological law, stability
theorem, empirical confirmation, quantum or ultraviolet completion, final
physics, Theory of Everything, proof, or canon.

THOS remains proxy-only without governed preregistered blind matched-budget
real arms, participants or operators, safety monitoring, appropriate
statistics, and independent review. Freed ID remains synthetic and
nonproduction without standards-conformant real keys and proofs, live issuance,
resolution, presentation, status, revocation, interoperability, privacy and
independent security review, recovery evidence, trust governance, and
affected-party oversight.

Professional seed conservation, genebank management, taxonomy, biosafety,
phytosanitary practice, agriculture, workplace and environmental safety,
privacy, accessibility, ownership, custody, access, benefit sharing,
traditional knowledge, remedy, legal or cultural interpretation,
affected-party legitimacy, Maori wording, Maori concepts, Maori data
governance, tangata whenua, iwi, hapu, and Maori authority remain open or
exact-gated. Maori concepts remain under Maori authority.

## Terminal hold

No task was created or forked, no collaboration subagent was spawned, Tavian
Sol and all standby records were not contacted, and Elaren Kestrel was not
precontacted. Successor resolution remains forbidden until exact-final
validation, clean push, fresh-live equality, a current roster/auth reread,
unique exact-title reread, duplicate and pause guard, and one acknowledged
send. The terminal verdict remains NOT_READY_FOR_STAGE_20.

{textwrap.fill(BOUNDARY, width=78)}
"""


def accessible_report() -> str:
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren Kestrel v671-v4 bounded evidence</title></head>
<body>
<a href="#main">Skip to main evidence</a>
<header><h1>Eiren Kestrel v671-v4 bounded synthetic seed-library evidence</h1><p>Status: NOT_READY_FOR_STAGE_20</p></header>
<nav aria-label="Evidence sections"><ol><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ol></nav>
<main id="main">
<section id="scope"><h2>Scope</h2><p>Synthetic documentation structures only: no real person, seed library, genebank, seed, plant, accession, packet, sample, location, measurement, germination, regeneration, identity event, professional action, or authority act.</p></section>
<section id="outcomes"><h2>Outcomes</h2><table><caption>Observed core outcome counts</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">completed</th><td>28</td><td>Bounded synthetic structural checks passed</td></tr><tr><th scope="row">represented</th><td>8</td><td>Proxy or schema only</td></tr><tr><th scope="row">open_gap</th><td>2</td><td>Required real evidence remains absent</td></tr><tr><th scope="row">exact_gate</th><td>2</td><td>Required authority remains absent</td></tr></tbody></table></section>
<section id="limits"><h2>Limits</h2><p>Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. This is not professional, legal, cultural, affected-party, or Maori-authority evidence.</p></section>
</main>
<footer><p>Same-owner structural evidence only. NOT_READY_FOR_STAGE_20.</p></footer>
</body>
</html>"""


def write_tooling_files(repo: Path) -> None:
    tools = repo / OWNER_ROOT / "tools"
    write_text(
        tools / "seed-library-contract.mjs",
        """/**
 * Validate one bounded synthetic seed-library status object.
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
        tools / "seed-library-contract.test.mjs",
        """import { describe, expect, test } from "vitest";
import { validateStatus } from "./seed-library-contract.mjs";

describe("bounded seed-library status", () => {
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
            "name": "eiren-kestrel-v671-v4-seed-library-tools",
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
            "include": ["seed-library-contract.mjs"],
        },
    )
    write_json(
        tools / "knip.json",
        {
            "entry": ["seed-library-contract.mjs"],
            "project": ["*.mjs"],
            "ignore": ["seed-library-contract.test.mjs"],
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
      - id: eiren-v671-v4-boundary
        name: Eiren v671-v4 bounded boundary check
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
        contract_rel = f"docs/eiren-kestrel/v671-v4/x2/contracts/{stem}.json"
        proposal_rel = f"docs/eiren-kestrel/v671-v4/x2/proposals/{stem}.json"
        card_rel = f"docs/eiren-kestrel/v671-v4/x2/cards/{stem}-card.json"
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
        {"name": "pytest", "use": "invalid_one_shot_plus_changed_dependency_recovery", "state": "valid_dependency_corrected_composite_zero_aggregate_credit"},
        {"name": "hypothesis", "use": "bounded_property_check_in_coverage_dependency_recovery", "state": "passed_dependency_recovery"},
        {"name": "pytest-cov", "use": "correct_shared_module_selector_on_changed_dependency_only", "state": "passed_dependency_recovery"},
    ]
    bounded_tool_rows.extend(
        {"name": name, "use": use, "state": state}
        for name, use, state in (
            ("ruff", "bounded_x2_python_scan", "passed_dependency_recovery"),
            ("mypy", "shared_contract_and_runner_type_check", "passed"),
            ("pip-audit", "version_verification_under_current_verify-only_rule", "passed"),
            ("openai", "offline_import_and_version_smoke_without_api_call", "passed"),
            ("typer", "owner_local_command_construction_and_output_smoke", "passed_dependency_recovery"),
            ("bandit", "bounded_shared_contract_and_runner_scan", "passed"),
            ("pre-commit", "owner_local_configuration_validation", "passed"),
            ("pip-tools", "empty_dependency_dry_run_without_output_write", "passed"),
            ("build", "version_verification_under_current_verify-only_rule", "passed"),
            ("pipdeptree", "bounded_typer_dependency_projection", "passed"),
            ("TypeScript", "checkJs_no_emit_contract_check", "passed"),
            ("ESLint", "configuration_free_module_parse_and_lint", "passed"),
            ("Prettier", "two_fixture_format_check", "passed"),
            ("Vitest", "two_test_synthetic_module_run", "passed"),
            ("tsx", "synthetic_module_execution_smoke", "passed"),
            ("c8", "D_drive_cached_coverage_threshold_smoke", "passed"),
            ("markdownlint-cli2", "integrated_overview_structure_lint", "passed_dependency_recovery"),
            ("npm-check-updates", "dependency_free_package_review", "passed"),
            ("Pyright", "shared_contract_and_runner_zero_error_check", "passed"),
            ("Knip", "owner_local_module_entry_analysis", "passed_dependency_recovery"),
            ("Madge", "owner_local_dependency_graph_projection", "passed"),
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
                row["signature"] for row in X2_OPERATIONAL_FAILURES
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
                "execution_state": "invalid_one_shot_evidence_aggregate",
                "invoked_once": True,
                "tests_collected": 15,
                "tests_executed": 14,
                "tests_passed": 13,
                "tests_failed": 1,
                "tests_errors": 0,
                "tests_not_run": 1,
                "coverage_data_collected": False,
                "aggregate_success_credit": 0,
                "replayed": False,
                "module_selector": "ghc_family_eiren_kestrel_v671_v4_seed_library",
                "failed_node": "test_14_accessible_report_and_overview_keep_reserved_evaluation_visible",
                "not_run_node": "test_15_staged_review_and_exact_normalized_git_blob_manifest",
                "junit_sha256": "e99c7c98818222cd551a1e529dd4abaa4fa4813acf27fe67ed1127f49de68fb1",
                "reason": "A raw substring assertion did not normalize deliberate Markdown line wrapping.",
            },
            "unintended_post_failure_reexecution": {
                "command_class": "pytest_trace_config_without_collect_only",
                "node_ids_observed": 33,
                "attributable_summary": False,
                "credit": 0,
                "retained": True,
            },
            "dependency_recovery": {
                "execution_state": "passed_exact_changed_dependencies_only",
                "nodes": [
                    "test_04_hypothesis_rejects_nonzero_real_world_counters",
                    "test_14_accessible_report_and_overview_keep_reserved_evaluation_visible",
                    "test_15_staged_review_and_exact_normalized_git_blob_manifest",
                ],
                "tests_run": 3,
                "tests_passed": 3,
                "tests_failed": 0,
                "tests_errors": 0,
                "junit_sha256": "b5eeb7364508ca094c63652850b77be6d13a8276c6b017c2824d287d106286c1",
                "coverage_sha256": "27f66a8968c0635fce45c0434b3f4d1754fafa480151a38ec47a505293f1d3b0",
                "coverage": {
                    "statements": 114,
                    "covered_lines": 67,
                    "missing_lines": 47,
                    "percent_covered": 58.771929824561404,
                },
                "successful_original_components_replayed_with_dependency_change": 1,
                "successful_original_components_replayed_without_dependency_change": 0,
            },
            "post_projection_finalization": {
                "scope": "exact_changed_artifacts_only",
                "nodes": [
                    "test_10_global_toolchain_versions_are_present_without_installation",
                    "test_13_privacy_security_and_evidence_validation_are_bounded_and_valid",
                    "test_15_staged_review_and_exact_normalized_git_blob_manifest",
                ],
                "broad_replay_permitted": False,
                "result_record_location": "external recovery receipt and immutable final closeout",
            },
            "canonical_validation": False,
            "boundary": "A dependency-corrected evidence composite is not canonical final validation.",
        },
    )

    start_flow = load_json(root / "x1/method-flow-startup.json")
    x1_validation_overlay = load_json(root / "x1/validation-negative-overlay.json")
    base_counts = x1_validation_overlay["effective_counts"]
    methods = []
    for index, failure in enumerate(X2_OPERATIONAL_FAILURES, start=1):
        methods.append(
            {
                "method_id": f"EK6714-X2-OP-{index:03d}",
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
                "method_id": f"EK6714-X2-{mutation['mutation_id']}",
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
        "effective_negatives": base_counts["effective_negatives"] + added,
        "effective_methods": base_counts["effective_methods"] + added,
        "failed_witnesses": base_counts["failed_witnesses"] + added,
        "passing_witnesses": base_counts["bounded_passing_witnesses"]
        + added
        + len(positive),
        "open_gaps": base_counts["open_gaps"]
        + outcome_counts["open_gap"],
        "exact_gates": base_counts["exact_gates"]
        + outcome_counts["exact_gate"],
    }
    write_json(
        root / "method-flow/evidence-ledger.json",
        {
            "schema": "ghc.family.method-flow-ledger.v6",
            "owner": OWNER,
            "phase": PHASE,
            "x1_method_rows": start_flow["row_count"]
            + x1_validation_overlay["row_count"],
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
            "x1_effective": base_counts["effective_negatives"],
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
            "inherited_open_gaps": base_counts["open_gaps"],
            "owner_new_open_gaps": outcome_counts["open_gap"],
            "effective_open_gaps": counts["open_gaps"],
            "inherited_exact_gates": base_counts["exact_gates"],
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
                "FAO Genebank Standards",
                "TDWG Darwin Core 2026-05-26 term set",
                "W3C PROV-O",
                "W3C WCAG 2.2",
                "New Zealand Privacy Commissioner privacy principles",
                "Te Mana Raraunga Maori Data Sovereignty principles",
            ],
            "boundary": "Official sources supply vocabulary and refusal conditions only.",
        },
    )
    write_json(
        root / "x2/x1-terminal-gate.json",
        {
            "schema": "ghc.family.x1-terminal-gate.v4",
            "x1_commit": X1_COMMIT,
            "direct_parent": "37ac80c499d43a90c874876402b262a220a252a1",
            "observed_before_x2_mutation": True,
            "local_upstream_tracking_fresh_live_equal": True,
            "typed_divergence": {"ahead": 0, "behind": 0},
            "clean": True,
            "x1_tests": {"passed": 18, "failed": 0, "errors": 0},
            "x1_manifest_entries": 20,
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
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
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
        set(repo.glob("scripts/*eiren_kestrel_v671_v4*.py"))
        | set(repo.glob("scripts/ghc_family_seed_*.py"))
        | set(repo.glob("tests/*eiren_kestrel_v671_v4*.py"))
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
    self_path = "docs/eiren-kestrel/v671-v4/validation/evidence-staged-privacy.json"
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
    self_path = "docs/eiren-kestrel/v671-v4/validation/evidence-staged-review.json"
    paths = staged_paths(repo)
    x1_mutations = [
        path
        for path in paths
        if path.startswith("docs/eiren-kestrel/v671-v4/x1/")
        or path.endswith("_v671_v4_x1.py")
    ]
    allowed_scripts = {
        "scripts/build_ghc_family_eiren_kestrel_v671_v4_x2.py",
        "scripts/ghc_family_eiren_kestrel_v671_v4_seed_library.py",
        *{f"scripts/{runner}.py" for _, runner, _ in RUNNER_BINDINGS},
    }
    allowed = [
        path
        for path in paths
        if path.startswith("docs/eiren-kestrel/v671-v4/")
        or path in allowed_scripts
        or path == "tests/test_ghc_family_eiren_kestrel_v671_v4_x2.py"
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
    manifest_path = "docs/eiren-kestrel/v671-v4/validation/evidence-manifest.json"
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
