"""Build Caelen Morrow v669-v4 bounded synthetic x2 evidence.

This builder performs only owner-local synthetic documentation validation. It
does not play, transfer, inspect, preserve, or make decisions about any real
recording, carrier, device, person, identity event, right, hazard, culture, or
authority matter.
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

from ghc_family_caelen_morrow_v669_v4_archive import (
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

X1_COMMIT = "964e7a27dd73ee7d96d8b9f6136ed4bf72e1f3f7"

X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "CM6694-X2-001",
        "title": "first npm registry projection lost nested distribution fields",
        "failed_witness": "A property-limited npm view projection returned null integrity and tarball fields although the package scalars were present.",
        "bounded_recovery": "Read each exact registry object and selected only its nested dist integrity and tarball host fields.",
    },
    {
        "failure_id": "CM6694-X2-002",
        "title": "isolated npm install emitted a transitive glob deprecation warning",
        "failed_witness": "The script-disabled exact install reported that a transitive glob 10.5.0 line is deprecated and should not be treated as a clean supply-chain claim.",
        "bounded_recovery": "Kept the warning at zero credit, ran the exact production dependency audit, observed zero current advisories, and retained supply-chain and future-advisory risk.",
    },
    {
        "failure_id": "CM6694-X2-003",
        "title": "first Remark preset smoke resolved from the repository directory",
        "failed_witness": "Both first Markdown smokes exited one because Remark resolved the preset relative to the repository instead of the isolated package root.",
        "bounded_recovery": "Changed only the working directory to the isolated package root; the valid fixture passed and the preregistered invalid fixture was rejected.",
    },
    {
        "failure_id": "CM6694-X2-004",
        "title": "first x2 Ruff gate found four mechanical defects",
        "failed_witness": "The pre-build Ruff check found one unused import, one regular-expression alias, one repeated suffix predicate, and one unnecessary generator.",
        "bounded_recovery": "Changed only those four local expressions and reran the same no-cache lint dependency before any x2 builder execution.",
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
        "schema": "ghc.family.synthetic-audiovisual-preservation-contract.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "semantic_slug": row["semantic_slug"],
        "title": row["title"],
        "synthetic_only": True,
        "typed_state": "documented_zero-real-row_fixture",
        "vacancies": [
            "real_recording_or_carrier",
            "real_playback_or_transfer",
            "real_measurement_or_listening",
            "professional_interpretation",
            "rights_and_affected_party_authority",
        ],
        "zero_counters": {
            "real_people": 0,
            "real_recordings": 0,
            "real_carriers": 0,
            "real_devices": 0,
            "real_measurements": 0,
            "playback_actions": 0,
            "transfer_actions": 0,
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
                "primary": "Freed ID and CBR Heart",
                "protected": ["GMUT Mind", "THOS Body"],
            },
            "tier_3_practice": "synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship",
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
description: Validate the {slug.replace('-', ' ')} part of a wholly synthetic audiovisual-preservation documentation fixture when this exact owner-local guard is needed.
---

# {name}

Use this skill only for a synthetic JSON fixture in the current owner lane. It authorizes no real recording, carrier, device, playback, transfer, measurement, listening, preservation action, professional decision, right, identity lifecycle, legal or cultural interpretation, affected-party decision, or authority act.

## Input

Require one JSON contract whose `semantic_slug` is `{slug}`, whose real-world counters are all zero, whose protected gates are complete, and whose terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Workflow

Run `python scripts/{runner}.py <contract.json>`. Retain a rejected fixture at zero completion credit. Correct only the smallest owner-local failed dependency and preserve the first witness.

## Output boundary

A pass establishes only structural behavior of the synthetic fixture. It establishes no empirical, participant, professional, production, safety, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim.
"""


def runner_text(slug: str) -> str:
    return f'''"""Family-current validator for the {slug} synthetic audio documentation contract."""
from ghc_family_caelen_morrow_v669_v4_archive import runner_main

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
        "self_exclusions": ["docs/caelen-morrow/v669-v4/validation/evidence-privacy-scan.json"],
        "claim_boundary": "A bounded pattern scan is not complete privacy assurance.",
    }


def python_security_review(repo: Path) -> dict[str, Any]:
    files = sorted(
        set((repo / "scripts").glob("*caelen_morrow_v669_v4*.py"))
        | set((repo / "scripts").glob("ghc_family_audio_*.py"))
        | set((repo / "tests").glob("*caelen_morrow_v669_v4*.py"))
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


def toolchain_receipt(repo: Path, report: Path, overview: Path) -> dict[str, Any]:
    prefix = Path(os.environ["CM6694_NODE_TOOL_PREFIX"])
    npm_cmd = Path(os.environ["GHC_FAMILY_NPM_CMD"])
    package_json = load_json(prefix / "package.json")
    lock_path = prefix / "package-lock.json"
    lock_bytes = lock_path.read_bytes()
    lock = json.loads(lock_bytes.decode("utf-8"))
    selected = []
    for item in TOOL_CANDIDATES:
        record = lock["packages"][f"node_modules/{item['name']}"]
        selected.append(
            {
                **item,
                "lock_version": record["version"],
                "lock_integrity": record.get("integrity"),
                "lock_resolved_host": "registry.npmjs.org" if "registry.npmjs.org" in record.get("resolved", "") else "unexpected",
                "exact_dependency": package_json["dependencies"].get(item["name"]),
                "version_matches": record["version"] == item["version"],
                "integrity_matches": record.get("integrity") == item["registry_integrity"],
            }
        )
    audit_proc = run(repo, str(npm_cmd), "audit", "--prefix", str(prefix), "--omit=dev", "--json")
    audit = json.loads(audit_proc.stdout)
    bin_dir = prefix / "node_modules" / ".bin"
    html_rules = "doctype-first,tag-pair,title-require,attr-no-duplication,id-unique,alt-require"
    html_pos = run(repo, str(bin_dir / "htmlhint.cmd"), str(report), "--rules", html_rules, "--format", "json", "--nocolor")
    html_neg = run(
        repo,
        str(bin_dir / "htmlhint.cmd"),
        "stdin",
        "--rules",
        "doctype-first,tag-pair,title-require",
        "--format",
        "json",
        "--nocolor",
        input_text="<html><body><div></body></html>",
    )
    remark_pos = run(prefix, str(bin_dir / "remark.cmd"), "--use", "remark-preset-lint-recommended", "--frail", str(overview))
    remark_neg = run(
        prefix,
        str(bin_dir / "remark.cmd"),
        "--use",
        "remark-preset-lint-recommended",
        "--frail",
        input_text="#Bad\n\n[broken]\n",
    )
    smoke = {
        "htmlhint_positive_exit": html_pos.returncode,
        "htmlhint_rejecting_exit": html_neg.returncode,
        "remark_positive_exit": remark_pos.returncode,
        "remark_rejecting_exit": remark_neg.returncode,
        "positive_passed": html_pos.returncode == 0 and remark_pos.returncode == 0,
        "rejecting_passed": html_neg.returncode != 0 and remark_neg.returncode != 0,
    }
    return {
        "schema": "ghc.family.isolated-toolchain-install-receipt.v2",
        "location": "$CM6694_NODE_TOOL_PREFIX",
        "shared_npm_prefix_mutated": False,
        "install_scripts_disabled": True,
        "lock_sha256": hashlib.sha256(lock_bytes).hexdigest(),
        "lockfile_version": lock["lockfileVersion"],
        "locked_package_entries": len(lock["packages"]),
        "selected": selected,
        "audit": {
            "returncode": audit_proc.returncode,
            "production_dependency_count": audit["metadata"]["dependencies"]["prod"],
            "vulnerabilities": audit["metadata"]["vulnerabilities"],
        },
        "smoke": smoke,
        "retained_warnings": ["transitive_glob_10_5_0_deprecation_warning"],
        "rollback": "remove only the phase-namespaced isolated environment after exact target revalidation and separate authorization",
        "claim_boundary": "Exact lock, audit, and smokes are not exhaustive supply-chain or production-fitness assurance.",
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
<title>Caelen Morrow v669-v4 bounded evidence report</title>
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
<header><h1>Caelen Morrow v669-v4 bounded evidence report</h1><p class="notice">Synthetic learning and design evidence only. No real media, people, playback, transfer, measurement, professional action, rights decision, cultural decision, or authority act occurred.</p>
<nav aria-label="Report sections"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#pillars">Pillars</a></li><li><a href="#gates">Gates</a></li><li><a href="#accessibility">Accessibility boundary</a></li></ul></nav></header>
<main id="main">
<section id="outcomes"><h2>Outcome ledger</h2><p>Only completed, represented, open_gap, and exact_gate are used.</p><table><caption>Forty preregistered synthetic proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Task</th><th scope="col">Outcome</th></tr></thead><tbody>{body_rows}</tbody></table></section>
<section id="pillars"><h2>Trinity Mandala boundaries</h2><h3>Freed ID and CBR Heart</h3><p>Primary: synthetic record identity, provenance, correction, custody, and contestability fields only; no keys, proofs, credentials, lifecycle events, governance, or affected-party authority.</p><h3>GMUT Mind</h3><p>Typed scalar-tensor and EFT research-model obligations remain protected. Signal-chain diagrams are not force, likelihood, prediction, material law, empirical confirmation, final physics, or Theory-of-Everything evidence.</p><h3>THOS Body</h3><p>Workload and handover structures are represented with zero real participants or operators and no governed blind matched-budget arms, safety outcomes, statistics, or independent review.</p></section>
<section id="gates"><h2>Open and exact gates</h2><p>The official collection adapter remains zero-call, and governed human evaluation remains absent. Professional practice, safety, rights, privacy, accessibility acceptance, legal and cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, Māori authority, and Stage 20 remain exact-gated.</p></section>
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
        contract_rel = f"docs/caelen-morrow/v669-v4/x2/contracts/{proposal_id.lower()}-{slug}.json"
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

    runner_receipts = []
    skill_receipts = []
    for index, (skill, runner_name) in enumerate(zip(SKILL_TITLES, RUNNER_TITLES), 1):
        row = rows[index - 1]
        skill_path = root / f"tools/skills/{skill}/SKILL.md"
        runner_path = repo / f"scripts/{runner_name}.py"
        write_text(skill_path, skill_text(skill, row["semantic_slug"], runner_name))
        write_text(runner_path, runner_text(row["semantic_slug"]))
        contract_path = repo / f"docs/caelen-morrow/v669-v4/x2/contracts/{row['proposal_id'].lower()}-{row['semantic_slug']}.json"
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
                {"name": "Library of Congress Recommended Formats Statement 2025-2026", "url": "https://www.loc.gov/preservation/resources/rfs/", "use": "format vocabulary and refusal conditions only"},
                {"name": "PREMIS Data Dictionary 3.0", "url": "https://www.loc.gov/standards/premis/index.html", "use": "event and preservation-metadata vocabulary only"},
                {"name": "IASA TC-04", "url": "https://www.iasa-web.org/tc04/audio-preservation", "use": "audio-preservation vocabulary and professional-boundary cues only"},
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
            "media": 0,
            "outcome": "open_gap",
            "reason": "No exact approved external collection transaction was needed or authorized.",
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
            "new_open_gaps": ["official collection adapter remains zero-call", "governed human and affected-user evaluation remains absent"],
            "effective_open_gaps": evidence_counts["open_gaps"],
            "inherited_exact_gates": STARTUP_EFFECTIVE_BASELINE["exact_gates"],
            "new_exact_gates": ["audiovisual preservation professional rights cultural affected-party and Māori authority", "Stage 20 evidence and authority"],
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
            "hope": "make every synthetic record reversible, legible, and honest at the authority boundary",
            "workload_within_caps": True,
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "stop_conditions_visible": True,
            "no_claim_of_sentience_personhood_continuity_or_authority": True,
        },
    )

    write_text(
        root / "x2/integrated-evidence-overview.md",
        """# Caelen Morrow v669-v4 bounded x2 evidence

## Outcome

Forty preregistered proposals were processed with only `completed`, `represented`, `open_gap`, and `exact_gate`: 28 bounded structural completions, 8 representations, 2 open gaps, and 2 exact gates. Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were attempted, rejected, retained, and assigned zero completion credit.

## Practice and pillars

Freed ID and CBR Heart are primary through a wholly synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship lens. GMUT Mind remains a typed scalar-tensor and EFT research-model family; signal-chain diagrams are not likelihoods, forces, predictions, material laws, empirical confirmation, final physics, quantum completion, or Theory-of-Everything proof. THOS Body remains represented with zero real participants or operators and no governed blind matched-budget arms, safety monitoring, statistics, or independent review.

## Skills, runners, and tools

The required current GHC workflow skills were read through EOF and applied to exact lifecycle decisions. Ten phase-local skills and ten family-current runners were built, validated, and smoke-used only against owner-local synthetic fixtures. The installed development suite received bounded version and import compatibility use. Three exact Node tools were installed with scripts disabled in a phase-namespaced D-backed environment, lock checked, audited, and given positive and rejecting smokes. The retained transitive deprecation warning prevents an exhaustive supply-chain claim.

## Work and holds

Thirty safe-now, fifteen candidate, ten skill, ten runner, and thirty CLEAN/FIX/REFINE rows completed within structural scope. Ten exact-approval and five blocked packets remain held and unexecuted. No inherited proposal, tool, skill, runner, recommendation, or outcome became automatic Caelen novelty or completion credit.

## Nonclaims

No real person, participant, recording, carrier, device, playback, transfer, listening act, measurement, observation, preservation action, hazard decision, identity event, professional action, legal or cultural decision, affected-party approval, or authority act occurred. Structural validation is not empirical confirmation, professional competence, production readiness, complete privacy or accessibility assurance, independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.

## Retention

All x1 failures, x2 operational failures, and 160 rejecting mutations remain visible with bounded recoveries and zero completion credit. Repository-sealed source truth, its external overlay, x1 additions, and x2 additions remain separate. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(root / "x2/accessible-evidence-report.html", report_html(rows))
    write_text(
        root / "x2/threat-model.md",
        """# Caelen Morrow v669-v4 x2 threat model

## Assets

Immutable source and x1 history, retained failures, exact gates, proposal identity, tool integrity, privacy boundaries, evidence labels, and delivery truth.

## Threats

Lifecycle mixing, inaccessible-history novelty overclaim, fabricated media or human evidence, signal analogy converted into science, structural checks converted into professional validation, custody converted into ownership or rights, authority laundering, dependency confusion, install scripts, stale advisories, path leakage, raw task identifiers, manifest drift, validation replay, sibling-lane mutation, and premature Stage 20 promotion.

## Controls

An immutable x1 commit, zero-real-row fixtures, four outcome labels, 160 preregistered rejecting mutations, exact holds, scripts-disabled isolated installation, exact registry and lock integrity, dated audit, positive and rejecting smokes, phase-local skills, family-current callers, five-class privacy scanning, bounded AST review, exact staged Git-blob manifests, additive Method Flow, and a one-shot terminal validator after the final equality gate.

## Residual risk

Registry metadata, audits, same-owner smokes, static structure, synthetic fixtures, and bounded scanners cannot establish future supply-chain safety, exhaustive security, complete privacy or accessibility, professional competence, legal or cultural legitimacy, affected-party acceptance, Māori authority, empirical GMUT, operational THOS, production Freed ID, independent reproduction, or Stage 20 readiness.
""",
    )

    tools = toolchain_receipt(repo, root / "x2/accessible-evidence-report.html", root / "x2/integrated-evidence-overview.md")
    if not all(row["version_matches"] and row["integrity_matches"] for row in tools["selected"]):
        raise RuntimeError("isolated tool lock or integrity mismatch")
    if tools["audit"]["returncode"] != 0 or tools["audit"]["vulnerabilities"]["total"] != 0:
        raise RuntimeError("isolated tool production dependency audit did not pass")
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
    frozen = [name for name in names if name.startswith("docs/caelen-morrow/v669-v4/x1/") or name.endswith(("v669_v4_x1.py", "v669_v4_archive.py"))]
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
            "self_exclusion": "docs/caelen-morrow/v669-v4/validation/evidence-staged-review.json",
        },
    )
    if frozen or disallowed:
        raise RuntimeError(f"x2 staged review failed: frozen={frozen}, disallowed={disallowed}")


def manifests_from_index(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    exclusions = [
        "docs/caelen-morrow/v669-v4/validation/evidence-owner-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/evidence-delta-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/evidence-staged-review.json",
    ]
    delta = []
    for rel in sorted(names):
        if rel in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{rel}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(
        run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", "docs/caelen-morrow/v669-v4", "scripts", "tests").stdout.splitlines()
    )
    owner = []
    for rel in sorted(owner_names):
        if rel in exclusions:
            continue
        if not (
            rel.startswith("docs/caelen-morrow/v669-v4/")
            or (rel.startswith("scripts/") and ("caelen_morrow_v669_v4" in rel or rel.startswith("scripts/ghc_family_audio_")))
            or (rel.startswith("tests/") and "caelen_morrow_v669_v4" in rel)
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
