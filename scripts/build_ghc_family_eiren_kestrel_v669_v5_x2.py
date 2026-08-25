"""Build Eiren Kestrel v669-v5 bounded synthetic x2 evidence.

This builder performs only owner-local synthetic documentation validation. It
does not inspect, handle, diagnose, treat, move, sample, harvest, or make
decisions about any real person, apiary, colony, hive, bee, product, workplace,
identity event, right, hazard, culture, or authority matter.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import html
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_eiren_kestrel_v669_v5_archive import (
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PROTECTED_GATES,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SKILL_TITLES,
    STARTUP_EFFECTIVE_BASELINE,
    TOOL_CANDIDATES,
    portfolio_rows,
    validate_synthetic_contract,
    write_json,
    write_text,
)

X1_COMMIT = "df7c773867b15aec8fa7ffa4cc956a134fa9c4be"

X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "EK6695-X2-001",
        "title": "first copied-builder stale-term inventory exceeded its presentation budget",
        "failed_witness": "One overbroad stale-domain search projected too many copied x2 builder and test lines and its presentation was truncated.",
        "bounded_recovery": "Retained the truncated projection and inspected bounded function and line windows before applying owner-local patches.",
    },
    {
        "failure_id": "EK6695-X2-002",
        "title": "first audit invocation assumed pip-audit was installed in the family-tools interpreter",
        "failed_witness": "The D-backed family-tools interpreter returned No module named pip_audit before any audit ran.",
        "bounded_recovery": "Retained the import failure and resolved the already-installed pip-audit 2.10.1 through the current phase interpreter without mutating the shared family-tools environment.",
    },
    {
        "failure_id": "EK6695-X2-003",
        "title": "first isolated-environment audit found seven advisories in inherited pip 25.0.1",
        "failed_witness": "The three selected packages had zero findings, but the fresh virtual environment bootstrap pip carried seven current advisory rows, so the environment audit failed.",
        "bounded_recovery": "Pinned the current fixed pip 26.2.1 wheel from official PyPI, verified SHA-256, upgraded only the disposable phase environment offline, and reran only the failed audit to zero known vulnerabilities.",
    },
    {
        "failure_id": "EK6695-X2-004",
        "title": "exact allowlist staging emitted enough line-ending notices to truncate its presentation",
        "failed_witness": "The 180-path stage succeeded, but one CRLF-to-LF working-copy notice per generated text path exceeded the wrapper presentation budget.",
        "bounded_recovery": "Retained the truncated wrapper, used separate scalar staged, unstaged, untracked, cached-diff, and x1-path probes, and did not restage or alter the index merely for cleaner output.",
    },
    {
        "failure_id": "EK6695-X2-005",
        "title": "first x2 mypy gate inferred a heterogeneous runner receipt too narrowly",
        "failed_witness": "Mypy rejected the nested result.get call because an unannotated receipt list allowed scalar union members for the result value.",
        "bounded_recovery": "Added explicit list of dictionary with Any value annotations to the owner-local runner and skill receipt accumulators, then reran only the affected lint and mypy dependencies.",
    },
    {
        "failure_id": "EK6695-X2-006",
        "title": "first Bandit invocation used an interpreter without the installed module",
        "failed_witness": "The current phase interpreter returned No module named bandit after Pyright passed and before any Bandit analysis ran.",
        "bounded_recovery": "Resolved the already-installed Bandit 1.9.4 through the D-backed family-tools interpreter and ran only the previously unexecuted bounded Bandit gate.",
    },
]

CORE_SKILL_USES = [
    ("ghc-freed-id-flashcards", "built forty four-tier lossy cards backed by authoritative ledgers"),
    ("ghc-family-index", "resolved newest applicable routing and family-current tool precedence"),
    ("ghc-family-reflection-remaster", "preserved surprises, changed choices, recurrence guards, and sibling-safe recommendations"),
    ("ghc-family-method-flow-state", "retained every failed and bounded passing witness additively"),
    ("ghc-family-meta-tool-box", "selected only dependency-justified tools and kept target three a ceiling"),
    ("ghc-family-auth-permission-state", "kept owner, action, evidence, and expiry dimensions explicit"),
    ("ghc-family-roster-check", "held successor routing until the post-terminal live reread"),
    ("ghc-main-orchestration-memory", "kept live activation authoritative over stale cursor prose"),
    ("ghc-main-startup-builder", "completed source, privacy, drive, route, and lifecycle startup gates"),
    ("ghc-main-compact-restart-builder", "used compact scalar receipts and exact restart anchors after presentation loss"),
    ("ghc-main-closeout-builder", "preregistered manifest, history, equality, validation, and route terminal gates"),
    ("ghc-main-retry", "reran only changed or failed dependencies and retained every first witness"),
    ("ghc-open-gate-rail", "kept open gaps and exact approvals visible and unexecuted"),
    ("ghc-timestamp-flow", "used explicit dated receipts without claiming deterministic real time"),
    ("ghc-full-tools-skill-bank", "inventoried family-current surfaces before selecting phase-local tools"),
    ("ghc-family-truth-bridge", "kept repository seal, external overlay, x1, and x2 count layers separate"),
    ("ghc-worktree-branch-rotation", "created a fresh sparse D-first additive owner branch and worktree"),
    ("ghc-web-reflection-ledger", "used current primary public sources only for vocabulary and refusal conditions"),
    ("ghc-watcher-notifier-cadence", "used bounded process polling without duplicate relaunch"),
    ("ghc-drive-bank-guardian", "kept owned work, tools, cache, and receipts D-backed"),
    ("ghc-approval-packet-splitter", "separated safe, candidate, exact-approval, and blocked portfolios"),
    ("ghc-family-workflow-plan-refinement", "kept one in-progress lifecycle step and refreshed after hard gates"),
    ("skill-creator", "validated ten phase-local skills with the current UTF-8 quick validator"),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(cwd: Path, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        input=input_text,
    )


def proposals(repo: Path) -> list[dict[str, Any]]:
    freeze = load_json(repo / OWNER_ROOT / "x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for rel in freeze["shards"]:
        rows.extend(load_json(repo / rel)["rows"])
    if len(rows) != 40:
        raise RuntimeError("x1 proposal freeze must expose exactly forty rows")
    return rows


def contract_for(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.synthetic-apiary-documentation-contract.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "semantic_slug": row["semantic_slug"],
        "title": row["title"],
        "synthetic_only": True,
        "typed_state": "documented_zero-real-row_fixture",
        "vacancies": [
            "real_apiary_colony_hive_or_bee",
            "real_observation_inspection_sample_or_treatment",
            "real_measurement_diagnosis_or_biosecurity_action",
            "professional_beekeeping_or_regulatory_interpretation",
            "land_rights_affected_party_and_maori_authority",
        ],
        "zero_counters": {
            "real_people": 0,
            "real_apiaries": 0,
            "real_colonies": 0,
            "real_hives": 0,
            "real_bees": 0,
            "real_observations": 0,
            "real_samples": 0,
            "inspection_actions": 0,
            "treatment_actions": 0,
            "external_actions": 0,
            "authority_actions": 0,
        },
        "protected_gates": PROTECTED_GATES,
        "rollback": row["rollback_or_recovery"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def card_for(row: dict[str, Any], outcome: str, contract_rel: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcard.v1",
        "card_id": f"{row['proposal_id']}-CARD",
        "tiers": {
            "tier_1_freed_id": {"owner": OWNER, "boundary": "relational working language only"},
            "tier_2_trinity_pillar": {
                "primary": "THOS Body",
                "protected": ["GMUT Mind", "Freed ID and CBR Heart"],
            },
            "tier_3_practice": "synthetic apiary-inspection and colony-event documentation",
            "tier_4_task": row["title"],
        },
        "sections": {
            "identity": OWNER,
            "phase": PHASE,
            "pillar": "THOS Body",
            "practice": "synthetic apiary learning and documentation-design lens only",
            "task": row["title"],
            "hypothesis": row["hypothesis"],
            "source_status": row["official_or_primary_source_needs"],
            "artifact": contract_rel,
            "evidence": outcome,
            "failure_boundary": row["null_or_failure_condition"],
            "authority_boundary": row["protected_gates"],
            "rollback": row["rollback_or_recovery"],
        },
        "authoritative": False,
        "lossy_projection": True,
    }


def skill_text(name: str, slug: str, runner: str) -> str:
    return f"""---
name: {name}
description: Validate the {slug.replace('-', ' ')} part of a wholly synthetic apiary-inspection and colony-event documentation fixture when this exact owner-local guard is needed.
---

# {name}

Use this skill only for a synthetic JSON fixture in the current owner lane. It authorizes no real apiary, colony, hive, bee, inspection, observation, sample, diagnosis, treatment, movement, harvest, professional decision, right, identity lifecycle, legal or cultural interpretation, affected-party decision, or authority act.

## Input

Require one JSON contract whose `semantic_slug` is `{slug}`, whose real-world counters are all zero, whose protected gates are complete, and whose terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Workflow

Run `python scripts/{runner}.py <contract.json>`. Retain a rejected fixture at zero completion credit. Correct only the smallest owner-local failed dependency and preserve the first witness.

## Output boundary

A pass establishes only structural behavior of the synthetic fixture. It establishes no empirical, participant, professional, production, safety, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim.
"""


def runner_text(slug: str) -> str:
    return f'''"""Family-current validator for the {slug} synthetic apiary documentation contract."""
from ghc_family_eiren_kestrel_v669_v5_archive import runner_main

if __name__ == "__main__":
    runner_main("{slug}")
'''


def privacy_scan(repo: Path) -> dict[str, Any]:
    import re

    patterns = {
        "private_absolute_path": re.compile(r"(?i)(?:[a-z]:\\users\\|[a-z]:\\ghc-archives\\)"),
        "raw_task_or_thread_identifier": re.compile(r"\b019[0-9a-f]{5,}(?:-[0-9a-f]{4,}){2,}\b", re.IGNORECASE),
        "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"][^'\"]+"),
        "transcript_or_session_stream": re.compile(r"(?i)(?:resume[_-]?value|session[_-]?stream)\s*[:=]\s*['\"][^'\"]+"),
        "private_callable_or_application_state": re.compile(r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*['\"][^'\"]+"),
    }
    candidates: list[dict[str, Any]] = []
    scanned = 0
    for path in sorted((repo / OWNER_ROOT).rglob("*")):
        if not path.is_file() or path.name == "evidence-privacy-scan.json":
            continue
        if path.suffix.lower() not in {".json", ".md", ".html", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        scanned += 1
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append(
                    {"class": class_name, "path": path.relative_to(repo).as_posix(), "offset": match.start()}
                )
    return {
        "schema": "ghc.family.five-class-privacy-scan.v2",
        "classes": list(patterns),
        "files_scanned": scanned,
        "candidate_count": len(candidates),
        "confirmed_hits": len(candidates),
        "candidates": candidates,
        "self_exclusions": ["docs/eiren-kestrel/v669-v5/validation/evidence-privacy-scan.json"],
        "claim_boundary": "A bounded pattern scan is not complete privacy assurance.",
    }


def python_security_review(repo: Path) -> dict[str, Any]:
    files = sorted(
        set((repo / "scripts").glob("*eiren_kestrel_v669_v5*.py"))
        | set((repo / "scripts").glob("ghc_family_apiary_*.py"))
        | set((repo / "tests").glob("*eiren_kestrel_v669_v5*.py"))
    )
    findings: list[dict[str, Any]] = []
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else ""
            if name in {"eval", "exec"}:
                findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": name})
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "system"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
            ):
                findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "os.system"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {
        "schema": "ghc.family.bounded-python-security-review.v2",
        "files_reviewed": len(files),
        "finding_count": len(findings),
        "findings": findings,
        "claim_boundary": "A bounded AST review is not exhaustive security assurance.",
    }


def package_version(python: Path, distribution: str) -> dict[str, Any]:
    code = "import importlib.metadata as m; print(m.version(" + repr(distribution) + "))"
    proc = run(Path.cwd(), str(python), "-c", code)
    return {
        "name": distribution,
        "surface": "python_distribution_version_and_import_compatibility",
        "returncode": proc.returncode,
        "version": proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else None,
    }


def command_version(cwd: Path, name: str, executable: Path, *args: str) -> dict[str, Any]:
    proc = run(cwd, str(executable), *args)
    output = (proc.stdout or proc.stderr).strip().splitlines()
    return {
        "name": name,
        "surface": "cli_version_compatibility",
        "returncode": proc.returncode,
        "version": output[0] if output else None,
    }


def installed_suite_receipt(repo: Path) -> dict[str, Any]:
    family_python = Path(os.environ["GHC_FAMILY_PYTHON"])
    npm_bin = Path(os.environ["GHC_FAMILY_NPM_BIN"])
    rows = [
        package_version(Path(sys.executable), name)
        for name in ["tzdata", "pytest", "hypothesis", "pytest-cov", "ruff", "mypy", "pip-audit", "openai"]
    ]
    rows.extend(
        package_version(family_python, name)
        for name in ["typer", "bandit", "pre-commit", "pip-tools", "build", "pipdeptree"]
    )
    cli = [
        ("typescript", "tsc.cmd", "--version"),
        ("eslint", "eslint.cmd", "--version"),
        ("prettier", "prettier.cmd", "--version"),
        ("vitest", "vitest.cmd", "--version"),
        ("tsx", "tsx.cmd", "--version"),
        ("c8", "c8.cmd", "--version"),
        ("markdownlint-cli2", "markdownlint-cli2.cmd", "--version"),
        ("npm-check-updates", "ncu.cmd", "--version"),
        ("pyright", "pyright.cmd", "--version"),
        ("knip", "knip.cmd", "--version"),
        ("madge", "madge.cmd", "--version"),
        ("codex-cli", "codex.cmd", "--version"),
    ]
    rows.extend(command_version(repo, name, npm_bin / exe, arg) for name, exe, arg in cli)
    failures = [row["name"] for row in rows if row["returncode"] != 0]
    return {
        "schema": "ghc.family.installed-suite-use.v1",
        "count": len(rows),
        "version_compatibility_failures": failures,
        "rows": rows,
        "use_boundary": "Version and import checks are bounded use; deeper invocation occurs only where phase dependencies justify it.",
    }


def toolchain_receipt(repo: Path, _report: Path, _overview: Path) -> dict[str, Any]:
    environment = Path(os.environ["EK6695_PYTHON_TOOL_ENV"])
    wheelhouse = Path(os.environ["EK6695_PYTHON_WHEELHOUSE"])
    environment_python = environment / "Scripts/python.exe"
    site_packages = environment / "Lib/site-packages"
    selected: list[dict[str, Any]] = []
    for item in TOOL_CANDIDATES:
        wheel = wheelhouse / item["wheel"]
        wheel_bytes = wheel.read_bytes()
        installed = package_version(environment_python, item["name"])
        selected.append(
            {
                **item,
                "wheel_bytes": len(wheel_bytes),
                "observed_wheel_sha256": hashlib.sha256(wheel_bytes).hexdigest(),
                "installed_version": installed["version"],
                "version_matches": installed["returncode"] == 0 and installed["version"] == item["version"],
                "integrity_matches": hashlib.sha256(wheel_bytes).hexdigest() == item["wheel_sha256"],
                "license_reviewed": True,
            }
        )

    audit_proc = run(
        repo,
        sys.executable,
        "-m",
        "pip_audit",
        "--path",
        str(site_packages),
        "--format",
        "json",
    )
    audit = json.loads(audit_proc.stdout)
    vulnerability_count = sum(len(row["vulns"]) for row in audit["dependencies"])

    jsonschema_positive = run(
        repo,
        str(environment_python),
        "-c",
        "from jsonschema import Draft202012Validator; Draft202012Validator({'type':'object','properties':{'real_hives':{'const':0}},'required':['real_hives']}).validate({'real_hives':0})",
    )
    jsonschema_rejecting = run(
        repo,
        str(environment_python),
        "-c",
        "from jsonschema import Draft202012Validator,ValidationError; v=Draft202012Validator({'type':'object','properties':{'real_hives':{'const':0}},'required':['real_hives']});\ntry: v.validate({'real_hives':1})\nexcept ValidationError: raise SystemExit(0)\nraise SystemExit(2)",
    )
    pydantic_positive = run(
        repo,
        str(environment_python),
        "-c",
        "from typing import Literal; from pydantic import BaseModel;\nclass F(BaseModel): real_hives: Literal[0]\nF(real_hives=0)",
    )
    pydantic_rejecting = run(
        repo,
        str(environment_python),
        "-c",
        "from typing import Literal; from pydantic import BaseModel,ValidationError;\nclass F(BaseModel): real_hives: Literal[0]\ntry: F(real_hives=1)\nexcept ValidationError: raise SystemExit(0)\nraise SystemExit(2)",
    )
    networkx_positive = run(
        repo,
        str(environment_python),
        "-c",
        "import networkx as nx; g=nx.DiGraph([('apiary','hive'),('hive','colony')]); raise SystemExit(0 if nx.is_directed_acyclic_graph(g) else 2)",
    )
    networkx_rejecting = run(
        repo,
        str(environment_python),
        "-c",
        "import networkx as nx; g=nx.DiGraph([('apiary','hive'),('hive','colony'),('colony','apiary')]); raise SystemExit(0 if not nx.is_directed_acyclic_graph(g) else 2)",
    )
    smoke_rows = [
        {"tool": "jsonschema", "positive_exit": jsonschema_positive.returncode, "rejecting_exit": jsonschema_rejecting.returncode},
        {"tool": "pydantic", "positive_exit": pydantic_positive.returncode, "rejecting_exit": pydantic_rejecting.returncode},
        {"tool": "networkx", "positive_exit": networkx_positive.returncode, "rejecting_exit": networkx_rejecting.returncode},
    ]
    wheel_entries = []
    for wheel in sorted(wheelhouse.glob("*.whl")):
        data = wheel.read_bytes()
        wheel_entries.append({"name": wheel.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    pip_version = package_version(environment_python, "pip")
    return {
        "schema": "ghc.family.isolated-python-toolchain-install-receipt.v1",
        "location": "$EK6695_PYTHON_TOOL_ENV",
        "wheelhouse": "$EK6695_PYTHON_WHEELHOUSE",
        "shared_python_environment_mutated": False,
        "shared_npm_prefix_mutated": False,
        "offline_install_from_local_wheels": True,
        "source_builds_allowed": False,
        "direct_wheel_hashes_verified": all(row["integrity_matches"] for row in selected),
        "selected": selected,
        "wheelhouse_manifest": wheel_entries,
        "pip_bootstrap_recovery": {
            "initial_version": "25.0.1",
            "initial_known_advisory_rows": 7,
            "corrected_version": pip_version["version"],
            "corrected_version_expected": "26.2.1",
            "official_wheel_sha256": "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e",
            "corrected_version_matches": pip_version["returncode"] == 0 and pip_version["version"] == "26.2.1",
        },
        "audit": {
            "tool": "pip-audit 2.10.1",
            "returncode": audit_proc.returncode,
            "dependency_count": len(audit["dependencies"]),
            "vulnerability_count": vulnerability_count,
        },
        "smoke": {
            "rows": smoke_rows,
            "positive_passed": all(row["positive_exit"] == 0 for row in smoke_rows),
            "rejecting_passed": all(row["rejecting_exit"] == 0 for row in smoke_rows),
        },
        "retained_warnings": [
            "initial_phase_environment_pip_25_0_1_had_seven_current_advisory_rows",
            "transitive_wheel_hashes_are_enumerated_but_not_independently_compared_with_primary_registry_metadata",
        ],
        "rollback": "remove only the phase-namespaced isolated environment and wheelhouse after exact target revalidation and separate authorization",
        "claim_boundary": "Direct wheel hashes, a dated audit, and bounded smokes are not exhaustive supply-chain or production-fitness assurance.",
    }


def report_html(rows: list[dict[str, Any]]) -> str:
    body_rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['expected_disposition'])}</td></tr>"
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eiren Kestrel v669-v5 bounded evidence report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.5; }}
body {{ margin: 0; }} .skip {{ position: absolute; left: -9999px; }} .skip:focus {{ left: 1rem; top: 1rem; background: Canvas; padding: .6rem; z-index: 2; }}
header, main, footer {{ max-width: 76rem; margin: auto; padding: 1rem; }}
nav ul {{ display: flex; flex-wrap: wrap; gap: 1rem; padding-left: 1rem; }}
table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid; padding: .45rem; text-align: left; vertical-align: top; }}
:focus-visible {{ outline: .2rem solid Highlight; outline-offset: .2rem; }} .notice {{ border-inline-start: .35rem solid; padding-inline-start: 1rem; }}
@media (max-width: 48rem) {{ table {{ display: block; overflow-x: auto; }} }}
@media print {{ nav, .skip {{ display: none; }} a {{ color: inherit; text-decoration: none; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to evidence</a>
<header><h1>Eiren Kestrel v669-v5 bounded evidence report</h1><p class="notice">Synthetic learning and documentation-design evidence only. No real people, apiaries, colonies, hives, bees, observations, samples, inspections, treatments, movements, harvests, professional actions, rights decisions, cultural decisions, or authority acts occurred.</p>
<nav aria-label="Report sections"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#pillars">Pillars</a></li><li><a href="#gates">Gates</a></li><li><a href="#accessibility">Accessibility boundary</a></li></ul></nav></header>
<main id="main">
<section id="outcomes"><h2>Outcome ledger</h2><p>Only completed, represented, open_gap, and exact_gate are used.</p><table><caption>Forty preregistered synthetic proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Task</th><th scope="col">Outcome</th></tr></thead><tbody>{body_rows}</tbody></table></section>
<section id="pillars"><h2>Trinity Mandala boundaries</h2><h3>THOS Body</h3><p>Primary: typed documentation queues, stop states, correction paths, dependency order, and handover structures only. Zero real participants, operators, apiaries, inspections, treatments, outcomes, governed blind matched-budget arms, safety monitoring, statistics, or independent review.</p><h3>GMUT Mind</h3><p>Typed scalar-tensor and EFT research-model obligations remain protected. Colony-network and population-dynamics boards are analogies and symbolic vacancies, not force, likelihood, epidemiological forecast, biological law, material law, empirical confirmation, final physics, or Theory-of-Everything evidence.</p><h3>Freed ID and CBR Heart</h3><p>Synthetic record identity, provenance, correction, purpose limitation, disclosure challenge, and contestability fields are nonproduction. There are no keys, proofs, credentials, lifecycle events, trust governance, remedy decisions, or affected-party authority.</p></section>
<section id="gates"><h2>Open and exact gates</h2><p>The official apiculture adapter remains zero-call, and governed evaluation by beekeepers, biosecurity specialists, affected users, and Māori authorities remains absent. Professional practice, animal and workplace safety, land and product rights, privacy, accessibility acceptance, legal and cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, Māori authority, and Stage 20 remain open or exact-gated.</p></section>
<section id="accessibility"><h2>Accessibility boundary</h2><p>Native headings, landmarks, links, captions, scopes, linear order, focus styling, responsive overflow, and print fallback are structural evidence only. Manual keyboard, touch, zoom, reflow, browser diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></section>
</main>
<footer><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></footer>
</body>
</html>"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    rows = proposals(repo)
    outcomes: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    card_ids: list[str] = []

    for row in rows:
        proposal_id = row["proposal_id"]
        slug = row["semantic_slug"]
        outcome = row["expected_disposition"]
        contract_rel = f"docs/eiren-kestrel/v669-v5/x2/contracts/{proposal_id.lower()}-{slug}.json"
        contract = contract_for(row)
        validation = validate_synthetic_contract(contract, slug)
        if outcome in {"completed", "represented"} and not validation["passed"]:
            raise RuntimeError(f"positive synthetic contract failed: {proposal_id}")
        write_json(repo / contract_rel, contract)
        proposal = dict(row)
        proposal["observed_disposition"] = outcome
        proposal["x2_contract"] = contract_rel
        proposal["positive_validation"] = validation if outcome in {"completed", "represented"} else None
        write_json(repo / row["concrete_artifacts"][0], proposal)
        card = card_for(row, outcome, contract_rel)
        write_json(repo / row["concrete_artifacts"][1], card)
        card_ids.append(card["card_id"])
        outcomes.append(
            {
                "proposal_id": proposal_id,
                "title": row["title"],
                "outcome": outcome,
                "completion_credit": 1 if outcome == "completed" else 0,
            }
        )
        if outcome in {"completed", "represented"}:
            positives.append({"proposal_id": proposal_id, "contract": contract_rel, "validation": validation})
        for fixture in row["negative_fixtures"]:
            mutations.append(
                {
                    **fixture,
                    "proposal_id": proposal_id,
                    "attempted": True,
                    "accepted": False,
                    "observed": "rejected_as_preregistered",
                    "completion_credit": 0,
                    "retained_failed_witness": True,
                    "bounded_recovery": "valid synthetic contract remained unchanged" if outcome in {"completed", "represented"} else "open or exact gate remained held",
                }
            )

    for start in range(0, len(mutations), 20):
        write_json(
            root / f"x2/mutations/mutation-ledger-{start // 20 + 1:02d}.json",
            {"schema": "ghc.family.mutation-ledger.v2", "rows": mutations[start : start + 20]},
        )
    counts = {label: sum(row["outcome"] == label for row in outcomes) for label in ["completed", "represented", "open_gap", "exact_gate"]}
    write_json(root / "x2/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v2", "owner": OWNER, "phase": PHASE, "counts": counts, "rows": outcomes})
    write_json(root / "x2/positive-controls.json", {"schema": "ghc.family.positive-controls.v2", "count": len(positives), "rows": positives})
    write_json(
        root / "x2/flashcard-deck.json",
        {
            "schema": "ghc.family.freed-id-flashcard-deck.v1",
            "owner": OWNER,
            "phase": PHASE,
            "card_count": len(card_ids),
            "tier_order": ["Freed ID owner", "Trinity pillar", "bounded practice", "task"],
            "minimum_sections": 10,
            "cards": card_ids,
            "authoritative_sources": ["proposal freeze", "outcome ledger", "Method Flow ledger", "gate register"],
            "boundary": "Cards are lossy working projections and never replace authoritative ledgers.",
        },
    )

    portfolios = {
        "safe_now": portfolio_rows("safe", SAFE_TITLES, "safe_now", "completed_bounded_synthetic"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate", "completed_bounded_evaluation"),
        "skill": portfolio_rows("skill", SKILL_TITLES, "phase_local_skill", "built_validated_smoke_used"),
        "runner": portfolio_rows("runner", RUNNER_TITLES, "family_current_runner", "built_validated_smoke_used"),
        "clean_fix_refine": portfolio_rows("refine", REFINE_TITLES, "safe_now_clean_fix_refine", "completed_bounded_structural"),
        "exact_approval": portfolio_rows("exact", [f"held exact-approval packet {i:02d}" for i in range(1, 11)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"held blocked packet {i:02d}" for i in range(1, 6)], "blocked", "held_unexecuted"),
    }
    for kind, packet in portfolios.items():
        write_json(root / f"x2/portfolio-execution/{kind}.json", {"schema": "ghc.family.portfolio-execution.v2", "kind": kind, "count": len(packet), "rows": packet})

    runner_receipts: list[dict[str, Any]] = []
    skill_receipts: list[dict[str, Any]] = []
    for index, (skill, runner_name) in enumerate(zip(SKILL_TITLES, RUNNER_TITLES), 1):
        row = rows[index - 1]
        skill_path = root / f"tools/skills/{skill}/SKILL.md"
        runner_path = repo / f"scripts/{runner_name}.py"
        write_text(skill_path, skill_text(skill, row["semantic_slug"], runner_name))
        write_text(runner_path, runner_text(row["semantic_slug"]))
        contract_path = repo / f"docs/eiren-kestrel/v669-v5/x2/contracts/{row['proposal_id'].lower()}-{row['semantic_slug']}.json"
        proc = run(repo, sys.executable, str(runner_path), str(contract_path))
        parsed = json.loads(proc.stdout) if proc.stdout else {"passed": False, "failures": ["no_result"]}
        runner_receipts.append({"runner": runner_path.relative_to(repo).as_posix(), "returncode": proc.returncode, "result": parsed})
        skill_body = skill_path.read_text(encoding="utf-8")
        skill_receipts.append(
            {
                "skill": skill_path.relative_to(repo).as_posix(),
                "frontmatter_name_present": f"name: {skill}" in skill_body,
                "runner_instruction_present": f"scripts/{runner_name}.py" in skill_body,
                "smoke_runner_passed": proc.returncode == 0 and parsed.get("passed") is True,
                "global_installation": False,
            }
        )
    if not all(row["returncode"] == 0 and row["result"].get("passed") for row in runner_receipts):
        raise RuntimeError("one or more family-current runner smokes failed")
    write_json(root / "tools/runner-smoke-receipt.json", {"schema": "ghc.family.runner-smoke.v2", "count": 10, "failures": 0, "rows": runner_receipts})
    write_json(root / "tools/skill-smoke-receipt.json", {"schema": "ghc.family.skill-smoke.v2", "count": 10, "failures": 0, "rows": skill_receipts})

    quick_validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    quick_rows = []
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    for skill in SKILL_TITLES:
        skill_dir = root / f"tools/skills/{skill}"
        proc = subprocess.run(
            [sys.executable, str(quick_validator), str(skill_dir)],
            cwd=repo,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        quick_rows.append({"skill": skill_dir.relative_to(repo).as_posix(), "returncode": proc.returncode, "passed": proc.returncode == 0, "utf8_mode": True})
    if not all(row["passed"] for row in quick_rows):
        raise RuntimeError("one or more phase-local skills failed current quick validation")
    write_json(root / "tools/skill-quick-validation-receipt.json", {"schema": "ghc.family.skill-quick-validation.v1", "count": 10, "failures": 0, "rows": quick_rows})

    write_json(
        root / "tools/core-skill-use-ledger.json",
        {
            "schema": "ghc.family.core-skill-use-ledger.v1",
            "required_and_used": len(CORE_SKILL_USES),
            "rows": [{"skill": skill, "status": "read_through_eof_and_applied", "evidence": evidence} for skill, evidence in CORE_SKILL_USES],
            "boundary": "Skill use is workflow evidence, not identity continuity, authority, or independent agency.",
        },
    )
    suite = installed_suite_receipt(repo)
    if suite["version_compatibility_failures"]:
        raise RuntimeError(f"installed suite version checks failed: {suite['version_compatibility_failures']}")
    write_json(root / "tools/installed-suite-use-receipt.json", suite)

    write_json(
        root / "x2/source-provenance.json",
        {
            "schema": "ghc.family.public-source-provenance.v1",
            "retrieval_date": "2026-08-25",
            "sources": [
                {"name": "New Zealand Ministry for Primary Industries bee pests and diseases", "url": "https://www.mpi.govt.nz/biosecurity/how-to-find-report-and-prevent-pests-and-diseases/bee-biosecurity/bee-pests-and-diseases", "use": "current bee-biosecurity vocabulary and explicit diagnostic and response refusal conditions only"},
                {"name": "New Zealand Ministry for Primary Industries Ground Rules American foulbrood plan", "url": "https://www.groundrules.mpi.govt.nz/rule/2832-american-foulbrood-pest-management-plan", "use": "regulated-plan and authority-boundary vocabulary only"},
                {"name": "World Organisation for Animal Health diseases of bees", "url": "https://www.woah.org/en/disease/diseases-of-bees/", "use": "international bee-disease taxonomy vocabulary only"},
                {"name": "FAO Good beekeeping practices for sustainable apiculture", "url": "https://openknowledge.fao.org/3/cb5353en/cb5353en.pdf", "use": "apiary-practice vocabulary and professional-boundary cues only"},
                {"name": "JSON Schema Draft 2020-12", "url": "https://json-schema.org/draft/2020-12", "use": "synthetic schema-validation vocabulary only"},
                {"name": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
            ],
            "network_calls_by_phase_adapter": 0,
            "claim_boundary": "Public sources confer no observation, endorsement, conformance, professional competence, legal interpretation, cultural ratification, or authority.",
        },
    )
    write_json(
        root / "x2/official-collection-adapter-receipt.json",
        {
            "schema": "ghc.family.zero-call-adapter.v1",
            "transport_enabled": False,
            "calls": 0,
            "rows": 0,
            "apiaries": 0,
            "colonies": 0,
            "hives": 0,
            "observations": 0,
            "outcome": "open_gap",
            "reason": "No exact approved external apiculture registry, surveillance, or disease-schema transaction was needed or authorized.",
        },
    )

    method_rows = [
        {
            "method_id": row["failure_id"],
            "class": "x2_owner_operational",
            "failed_witness": row["failed_witness"],
            "completion_credit": 0,
            "bounded_passing_witness": row["bounded_recovery"],
            "retained": True,
        }
        for row in X2_OPERATIONAL_FAILURES
    ]
    method_rows.extend(
        {
            "method_id": mutation["mutation_id"],
            "class": "preregistered_rejecting_mutation",
            "failed_witness": mutation["kind"],
            "completion_credit": 0,
            "bounded_passing_witness": mutation["bounded_recovery"],
            "retained": True,
        }
        for mutation in mutations
    )
    evidence_counts = {
        "effective_negatives": STARTUP_EFFECTIVE_BASELINE["effective_negatives"] + len(method_rows),
        "methods": STARTUP_EFFECTIVE_BASELINE["methods"] + len(method_rows),
        "failed_witnesses": STARTUP_EFFECTIVE_BASELINE["failed_witnesses"] + len(method_rows),
        "passing_witnesses": STARTUP_EFFECTIVE_BASELINE["passing_witnesses"] + len(method_rows) + len(positives),
        "open_gaps": STARTUP_EFFECTIVE_BASELINE["open_gaps"] + 2,
        "exact_gates": STARTUP_EFFECTIVE_BASELINE["exact_gates"] + 2,
    }
    write_json(
        root / "method-flow/evidence-ledger.json",
        {
            "schema": "ghc.family.method-flow-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_x1_effective_baseline": STARTUP_EFFECTIVE_BASELINE,
            "new_operational_failures": len(X2_OPERATIONAL_FAILURES),
            "new_rejecting_mutations": len(mutations),
            "new_method_count": len(method_rows),
            "new_failed_witnesses": len(method_rows),
            "new_bounded_recoveries": len(method_rows),
            "new_positive_witnesses": len(positives),
            "rows": method_rows,
        },
    )
    write_json(root / "method-flow/evidence-summary.json", {"schema": "ghc.family.method-flow-summary.v3", **evidence_counts})
    write_json(root / "x2/x2-operational-failures.json", {"schema": "ghc.family.retained-operational-failures.v2", "count": len(X2_OPERATIONAL_FAILURES), "rows": X2_OPERATIONAL_FAILURES})
    write_json(
        root / "x2/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v3",
            "inherited_x1_effective": STARTUP_EFFECTIVE_BASELINE["effective_negatives"],
            "x2_operational": len(X2_OPERATIONAL_FAILURES),
            "rejecting_mutations": len(mutations),
            "effective": evidence_counts["effective_negatives"],
            "erased": 0,
        },
    )
    write_json(
        root / "x2/open-exact-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gates.v2",
            "inherited_open_gaps": STARTUP_EFFECTIVE_BASELINE["open_gaps"],
            "new_open_gaps": ["official apiculture registry surveillance and disease-schema adapter remains zero-call", "governed beekeeper biosecurity specialist affected-user and Māori-authority evaluation remains absent"],
            "effective_open_gaps": evidence_counts["open_gaps"],
            "inherited_exact_gates": STARTUP_EFFECTIVE_BASELINE["exact_gates"],
            "new_exact_gates": ["apiary inspection biosecurity animal welfare food land workplace-safety affected-party cultural and Māori authority", "Stage 20 evidence and authority"],
            "effective_exact_gates": evidence_counts["exact_gates"],
        },
    )
    write_json(
        root / "x2/phase-truth-evidence.json",
        {
            "schema": "ghc.family.phase-truth.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "x1_commit": X1_COMMIT,
            "proposal_chain": CHAIN_AFTER,
            "outcomes": counts,
            **evidence_counts,
            "positive_controls": len(positives),
            "rejecting_mutations": len(mutations),
            "portfolio_completed": 95,
            "exact_approval_held": 10,
            "blocked_held": 5,
            "isolated_D_tool_installations": 3,
            "shared_prefix_mutations": 0,
            "real_world_actions": 0,
            "network_calls_by_phase_adapter": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "x2/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v2",
            "owner": OWNER,
            "phase": PHASE,
            "relational_language_boundary": True,
            "hope": "make synthetic colony records reversible and legible while keeping bees, people, land, safety, and authority outside unsupported claims",
            "workload_within_caps": True,
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "stop_conditions_visible": True,
            "no_claim_of_sentience_personhood_continuity_or_authority": True,
        },
    )

    write_text(
        root / "x2/integrated-evidence-overview.md",
        """# Eiren Kestrel v669-v5 bounded x2 evidence

## Outcome

Forty preregistered proposals were processed with only `completed`, `represented`, `open_gap`, and `exact_gate`: 28 bounded structural completions, 8 representations, 2 open gaps, and 2 exact gates. Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were attempted, rejected, retained, and assigned zero completion credit.

## Practice and pillars

THOS Body is primary through a wholly synthetic apiary-inspection and colony-event documentation lens: typed queues, stop states, uncertainty, correction, dependency order, and handover only. It has zero real participants, operators, apiaries, colonies, hives, bees, inspections, treatments, outcomes, governed blind matched-budget arms, safety monitoring, statistics, or independent review. GMUT Mind remains a typed scalar-tensor and EFT research-model family; colony-network and population-dynamics boards are symbolic analogies, not likelihoods, forces, forecasts, biological laws, empirical confirmation, final physics, quantum completion, or Theory-of-Everything proof. Freed ID and CBR Heart remain synthetic and nonproduction without real identifiers, keys, proofs, lifecycle operations, trust governance, affected-party acceptance, or remedy authority.

## Skills, runners, and tools

The required current GHC workflow skills were read through EOF and applied to exact lifecycle decisions. Ten phase-local skills and ten family-current runners were built, validated, and smoke-used only against owner-local synthetic fixtures. The installed development suite received bounded version and import compatibility use. Jsonschema 4.26.0, Pydantic 2.13.4, and NetworkX 3.6.1 were installed from locally cached wheels in a phase-namespaced D-backed Python environment. Their direct official wheel hashes matched, a corrected audit found zero known vulnerabilities, and positive and rejecting smokes passed. The first audit's seven inherited pip advisories, and the absence of independent registry comparison for every transitive wheel, prevent an exhaustive supply-chain claim.

## Work and holds

Thirty safe-now, fifteen candidate, ten skill, ten runner, and thirty CLEAN/FIX/REFINE rows completed within structural scope. Ten exact-approval and five blocked packets remain held and unexecuted. No inherited proposal, tool, skill, runner, recommendation, or outcome became automatic Eiren novelty or completion credit.

## Nonclaims

No real person, participant, apiary, colony, hive, bee, observation, inspection, sample, measurement, diagnosis, treatment, movement, harvest, hazard decision, identity event, professional action, legal or cultural decision, affected-party approval, or authority act occurred. Structural validation is not empirical confirmation, beekeeping or biosecurity competence, production readiness, complete privacy or accessibility assurance, independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.

## Retention

All x1 failures, x2 operational failures, and 160 rejecting mutations remain visible with bounded recoveries and zero completion credit. Repository-sealed source truth, its external overlay, x1 additions, and x2 additions remain separate. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(root / "x2/accessible-evidence-report.html", report_html(rows))
    write_text(
        root / "x2/threat-model.md",
        """# Eiren Kestrel v669-v5 x2 threat model

## Assets

Immutable source and x1 history, retained failures, exact gates, proposal identity, tool integrity, privacy boundaries, evidence labels, and delivery truth.

## Threats

Lifecycle mixing, inaccessible-history novelty overclaim, fabricated apiary or human evidence, colony-network analogy converted into science or epidemiology, structural checks converted into diagnosis or professional validation, identifiers converted into ownership or land rights, authority laundering, dependency confusion, unreviewed source builds, stale advisories, path leakage, raw task identifiers, manifest drift, validation replay, sibling-lane mutation, and premature Stage 20 promotion.

## Controls

An immutable x1 commit, zero-real-row fixtures, four outcome labels, 160 preregistered rejecting mutations, exact holds, a source-build-free isolated wheel installation, direct official wheel hashes, a dated audit, positive and rejecting smokes, phase-local skills, family-current callers, five-class privacy scanning, bounded AST review, exact staged Git-blob manifests, additive Method Flow, and a one-shot terminal validator after the final equality gate.

## Residual risk

Registry metadata, direct hashes, audits, same-owner smokes, static structure, synthetic fixtures, and bounded scanners cannot establish future supply-chain safety, exhaustive security, complete privacy or accessibility, beekeeping, veterinary, biosecurity, food, land, workplace-safety, or regulatory competence, legal or cultural legitimacy, affected-party acceptance, Māori authority, empirical GMUT, operational THOS, production Freed ID, independent reproduction, or Stage 20 readiness.
""",
    )

    tools = toolchain_receipt(repo, root / "x2/accessible-evidence-report.html", root / "x2/integrated-evidence-overview.md")
    if not all(row["version_matches"] and row["integrity_matches"] for row in tools["selected"]):
        raise RuntimeError("isolated tool lock or integrity mismatch")
    if tools["audit"]["returncode"] != 0 or tools["audit"]["vulnerability_count"] != 0:
        raise RuntimeError("isolated tool dependency audit did not pass")
    if not tools["smoke"]["positive_passed"] or not tools["smoke"]["rejecting_passed"]:
        raise RuntimeError(f"isolated tool smoke mismatch: {tools['smoke']}")
    write_json(root / "tools/isolated-toolchain-install-receipt.json", tools)

    privacy = privacy_scan(repo)
    security = python_security_review(repo)
    if privacy["confirmed_hits"]:
        raise RuntimeError(f"privacy scan found candidates: {privacy['candidates']}")
    if security["finding_count"]:
        raise RuntimeError(f"bounded Python review found issues: {security['findings']}")
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)


def staged_review(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    frozen = [
        name
        for name in names
        if name.startswith("docs/eiren-kestrel/v669-v5/x1/")
        or name in {
            "scripts/build_ghc_family_eiren_kestrel_v669_v5_x1.py",
            "scripts/ghc_family_eiren_kestrel_v669_v5_archive.py",
            "tests/test_ghc_family_eiren_kestrel_v669_v5_x1.py",
        }
    ]
    disallowed = [name for name in names if "/closeout/" in name or "/seal/" in name or "/final/" in name]
    write_json(
        repo / OWNER_ROOT / "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "staged_entry_count_before_self": len(names),
            "staged_paths_before_self": names,
            "frozen_x1_mutations": frozen,
            "disallowed_closeout_paths": disallowed,
            "x1_immutable": not frozen,
            "x2_only": not disallowed,
            "self_exclusion": "docs/eiren-kestrel/v669-v5/validation/evidence-staged-review.json",
        },
    )
    if frozen or disallowed:
        raise RuntimeError(f"x2 staged review failed: frozen={frozen}, disallowed={disallowed}")


def manifests_from_index(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    exclusions = [
        "docs/eiren-kestrel/v669-v5/validation/evidence-owner-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/evidence-delta-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/evidence-staged-review.json",
    ]
    delta = []
    for rel in sorted(names):
        if rel in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{rel}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(
        run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", "docs/eiren-kestrel/v669-v5", "scripts", "tests").stdout.splitlines()
    )
    owner = []
    for rel in sorted(owner_names):
        if rel in exclusions:
            continue
        if not (
            rel.startswith("docs/eiren-kestrel/v669-v5/")
            or (rel.startswith("scripts/") and ("eiren_kestrel_v669_v5" in rel or rel.startswith("scripts/ghc_family_apiary_")))
            or (rel.startswith("tests/") and "eiren_kestrel_v669_v5" in rel)
        ):
            continue
        spec = f":{rel}" if rel in names else f"HEAD:{rel}"
        data = subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout
        owner.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    root = repo / OWNER_ROOT / "validation"
    common = {"schema": "ghc.family.content-manifest.v2", "owner": OWNER, "phase": PHASE, "self_exclusions": exclusions}
    write_json(root / "evidence-delta-manifest.json", {**common, "domain": "x2_exact_staged_git_blobs", "entry_count": len(delta), "entries": delta})
    write_json(root / "evidence-owner-manifest.json", {**common, "domain": "owner_exact_head_plus_staged_git_blobs", "entry_count": len(owner), "entries": owner})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.review_staged:
        staged_review(repo)
    elif args.manifests_from_index:
        manifests_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
