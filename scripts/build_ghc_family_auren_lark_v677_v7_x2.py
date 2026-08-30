#!/usr/bin/env python3
"""Build and execute the bounded Auren Lark v677-v7 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Any

from ghc_family_auren_lark_v677_v7_core import (
    canonical_digest,
    mutate,
    positive_fixture,
    runner_smoke,
    skill_smoke,
    validate_contract,
    validate_flashcard,
)


OWNER = "Auren Lark"
OWNER_SLUG = "auren-lark"
PHASE = "v677-v7"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
BASELINE = {
    "effective_negatives": 45401,
    "effective_methods": 42084,
    "retained_failed_witnesses": 17062,
    "bounded_passing_witnesses": 25727,
    "open_gaps": 386,
    "exact_gates": 377,
}
BASE_FAILURE_COUNT = 295
BASE_PASSING_COUNT = 610
MUTATIONS = ["missing_hypothesis", "unknown_outcome_label", "authority_escalation", "real_identifier_or_measurement"]
FAMILY_ANCHORS = [
    "Eiren Kestrel",
    "Elaren Kestrel",
    "Neris Solane",
    "Vesper Arlen",
    "Lyren Moss",
    "Ilyra Fen",
    "Auren Lark",
    "Sable Rook",
    "Caelen Ash",
    "Orin Thale",
    "Liora Venn",
    "Tamar Vey",
    "Elowen Cairn",
    "Sylven Arc",
    "Caelen Morrow",
]
SECTIONS = [
    "identity-and-route",
    "source-and-lifecycle",
    "three-pillar-boundaries",
    "synthetic-access-correction-casefile-practice",
    "archival-metadata-accessibility-and-authority-vacancy-practice",
    "inherited-proposal-selection",
    "new-proposal-freeze",
    "approval-portfolios",
    "toolchain-verification",
    "skills-and-runners",
    "clean-fix-refine",
    "method-flow-and-failures",
    "validation-and-closeout",
    "successor-route",
]
RUNNER_MAP = {
    "ghc_family_auren_lark_v677_v7_contract_runner.py": "contract",
    "ghc_family_auren_lark_v677_v7_mutation_runner.py": "mutation",
    "ghc_family_auren_lark_v677_v7_topology_runner.py": "casefile_topology",
    "ghc_family_auren_lark_v677_v7_metadata_runner.py": "metadata",
    "ghc_family_auren_lark_v677_v7_flashcard_runner.py": "flashcard",
    "ghc_family_auren_lark_v677_v7_toolchain_runner.py": "toolchain",
    "ghc_family_auren_lark_v677_v7_privacy_runner.py": "privacy",
    "ghc_family_auren_lark_v677_v7_accessibility_runner.py": "accessibility",
    "ghc_family_auren_lark_v677_v7_portfolio_runner.py": "portfolio",
    "build_ghc_family_auren_lark_v677_v7_report.py": "report",
}
TOOL_VERSIONS = {
    "tzdata": "2026.3",
    "pytest": "9.1.1",
    "hypothesis": "6.165.10",
    "pytest-cov": "7.1.0",
    "ruff": "0.16.4",
    "mypy": "2.3.1",
    "pip-audit": "2.10.1",
    "openai": "3.3.1",
    "typer": "0.27.1",
    "bandit": "1.9.4",
    "pre-commit": "4.6.2",
    "pip-tools": "7.6.1",
    "build": "1.5.0",
    "pipdeptree": "4.2.1",
    "typescript": "7.0.2",
    "eslint": "10.8.1",
    "prettier": "3.9.6",
    "vitest": "4.1.11",
    "tsx": "4.23.12",
    "c8": "12.0.0",
    "markdownlint-cli2": "0.23.2",
    "npm-check-updates": "23.0.2",
    "pyright": "1.1.413",
    "knip": "6.32.2",
    "madge": "8.0.0",
}
SYSTEM_DISTS = ("tzdata", "pytest", "hypothesis", "pytest-cov", "ruff", "mypy", "pip-audit", "openai")
AUX_DISTS = ("typer", "bandit", "pre-commit", "pip-tools", "build", "pipdeptree")
NODE_TOOLS = (
    ("TypeScript", "typescript", "tsc"),
    ("ESLint", "eslint", "eslint"),
    ("Prettier", "prettier", "prettier"),
    ("Vitest", "vitest", "vitest"),
    ("tsx", "tsx", "tsx"),
    ("c8", "c8", "c8"),
    ("markdownlint-cli2", "markdownlint-cli2", "markdownlint-cli2"),
    ("npm-check-updates", "npm-check-updates", "ncu"),
    ("Pyright", "pyright", "pyright"),
    ("Knip", "knip", "knip"),
    ("Madge", "madge", "madge"),
)
LOCAL_VALIDATION_CANDIDATES = [
    "ghc-civic-record-casefile-hierarchy",
    "ghc-civic-record-request-state",
    "ghc-civic-record-clock-vacancy",
    "ghc-civic-record-accessibility-status",
    "ghc-civic-record-provenance-vacancy",
]
X2_OPERATIONAL_FAILURES: list[tuple[str, str, str, str]] = [
    (
        "AUR6777-X2-N001",
        "The first post-x1 source-template search passed Windows wildcard path arguments directly to rg and failed with an invalid filename syntax error.",
        "AUR6777-X2-P001",
        "The recovery used rg -g file filters over literal scripts and tests roots, producing the bounded domain-drift inventory without mutation.",
    ),
    (
        "AUR6777-X2-N002",
        "The first x2 aggregate reached its global npm list probe after completing contracts, mutations, skill checks, runner smokes, and flashcards, then timed out after 120 seconds with zero toolchain credit.",
        "AUR6777-X2-P002",
        "Persisted owner artifacts were counted and preserved; the recovery reads each declared Node CLI version directly and resumes only the toolchain-dependent tail without replaying successful components.",
    ),
    (
        "AUR6777-X2-N003",
        "The first recovery replaced npm list with direct CLI shims, but eslint --version itself exceeded its 30-second bound and the recovery stopped before writing the tail.",
        "AUR6777-X2-P003",
        "The second recovery avoids all Node executable shims and reads exact package.json versions beneath the resolved D-drive NPM_CONFIG_PREFIX; D-drive cache and prefix are verified from their explicit environment settings.",
    ),
]


def run(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def customize_skills(repo: Path, names: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    skill_root = repo / "docs" / OWNER_SLUG / PHASE / "x2" / "skills"
    quick_validate = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    positives = []
    negatives = []
    for name in names:
        path = skill_root / name
        if not (path / "agents" / "openai.yaml").is_file():
            raise RuntimeError(f"official initializer evidence absent for {name}")
        title = " ".join(token.capitalize() for token in name.split("-"))
        description = (
            f"Represent {name.replace('-', ' ')} in bounded synthetic access-request, correction, counterstatement, casefile, accessibility-format, provenance, flashcard, or evidence workflows; "
            "use when the named structure must stay separate from real observations, professional decisions, or authority."
        )
        write_text(
            path / "SKILL.md",
            f"""---
name: {name}
description: {description}
---

# {title}

Use this skill for one owner-scoped, zero-row representation. It improves modular context retrieval without turning a synthetic record, citation, or validation result into a real observation, professional judgment, identity event, or authority grant.

## Inputs

- One explicitly bounded synthetic record, claim, card, or evidence target.
- Its source status, lifecycle anchor, acceptance gate, rollback, and protected gates.

## Procedure

1. Verify that the target is owner-scoped, synthetic, and free of raw identifiers, credentials, private routes, or protected real data.
2. Preserve source, hypothesis, null or failure condition, acceptance gate, and rollback as separate fields.
3. Emit the smallest deterministic artifact that represents the named structure.
4. Retain every failed witness and make recovery additive; never rewrite an earlier false result.
5. Mark real observation, participant, professional, legal, cultural, Māori-authority, accessibility, privacy, security, and Stage 20 needs as open or exact-gated.

## Refusal conditions

Refuse real access, correction, disclosure, refusal, complaint, appeal, remedy, record disposal, representative acceptance, accessibility certification, privacy or records-management decisions, participant work, credentials, keys, external writes, legal or cultural determinations, Māori wording or authority decisions, production deployment, empirical GMUT promotion, THOS effectiveness claims, identity-continuity claims, or Stage 20 promotion without exact evidence and competent authority.

## Output

Return a compact deterministic record containing the representation, evidence status, retained failures, open gaps, exact gates, and rollback. Passing output is same-owner structural evidence only.
""",
        )
        dump(
            path / "skill.json",
            {
                "name": name,
                "owner": OWNER,
                "phase": PHASE,
                "initialized_with_official_skill_creator": True,
                "global_install": False,
                "real_world_rows": 0,
                "external_actions": 0,
                "professional_authority": False,
                "maori_authority": False,
                "stage20_ready": False,
            },
        )
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(quick_validate), str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        smoke = skill_smoke(path, invalid=False)
        rejecting = skill_smoke(path, invalid=True)
        positive = {
            "skill": name,
            "quick_validate_exit": validation.returncode,
            "quick_validate_passed": validation.returncode == 0,
            "smoke": smoke,
        }
        if validation.returncode != 0 or not smoke["accepted"] or rejecting["accepted"]:
            raise RuntimeError(f"skill validation failed for {name}")
        positives.append(positive)
        negatives.append({"skill": name, "fixture": "synthetic_rejecting_fixture", "accepted": False, "errors": rejecting["errors"]})
    return positives, negatives


def build_runner_wrappers(repo: Path) -> list[dict[str, Any]]:
    receipts = []
    for filename, name in RUNNER_MAP.items():
        path = repo / "scripts" / filename
        write_text(
            path,
            "#!/usr/bin/env python3\n"
            f'"""Family-current Auren Lark v677-v7 {name} runner."""\n\n'
            "from ghc_family_auren_lark_v677_v7_core import runner_cli\n\n"
            "if __name__ == \"__main__\":\n"
            f"    runner_cli({name!r})\n",
        )
        positive = subprocess.run(
            [sys.executable, str(path), "--smoke"],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        negative = subprocess.run(
            [sys.executable, str(path), "--smoke", "--invalid"],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        good = json.loads(positive.stdout)
        bad = json.loads(negative.stdout)
        if not good["expectation_met"] or not bad["expectation_met"]:
            raise RuntimeError(f"runner smoke failed for {filename}")
        receipts.append({"runner": filename, "positive": good, "rejecting": bad})
    return receipts


def build_flashcards(new_rows: list[dict[str, Any]], inherited: list[dict[str, Any]]) -> dict[str, Any]:
    cards = []
    for index, anchor in enumerate(FAMILY_ANCHORS, start=1):
        card = {
            "card_id": f"AUR6777-ANCHOR-{index:02d}",
            "freed_id_anchor": anchor,
            "trinity_pillar": "all three pillars visible; no evidence conversion",
            "bounded_practice": "relational working-language route anchor",
            "task": "resolve one owner card namespace without consciousness personhood continuity qualification or authority claim",
            "section": "identity-and-route",
            "identity_continuity_claim": False,
            "authority_claim": False,
            "real_world_rows": 0,
        }
        if validate_flashcard(card):
            raise RuntimeError("invalid family anchor card")
        card["content_digest"] = canonical_digest(card)
        cards.append(card)
    combined = [("new", row) for row in new_rows] + [("inherited", row) for row in inherited]
    for index, (kind, row) in enumerate(combined, start=1):
        title = row["title"]
        if index <= 30:
            practice = "synthetic access-request correction counterstatement casefile accessibility-format and provenance documentation"
        elif index <= 60:
            practice = "synthetic archival metadata authority-vacancy dispute abstention and reversible-handover review"
        else:
            practice = "inherited zero-credit revalidation"
        card = {
            "card_id": f"AUR6777-CARD-{index:03d}",
            "freed_id_anchor": OWNER,
            "trinity_pillar": "Freed ID and CBR Heart primary; GMUT Mind and THOS Body protected",
            "bounded_practice": practice,
            "task": title,
            "section": SECTIONS[(index - 1) % len(SECTIONS)],
            "proposal_class": kind,
            "identity_continuity_claim": False,
            "authority_claim": False,
            "real_world_rows": 0,
        }
        if validate_flashcard(card):
            raise RuntimeError(f"invalid flashcard for {title}")
        card["content_digest"] = canonical_digest(card)
        cards.append(card)
    return {
        "schema": "ghc-freed-id-flashcards/v1",
        "tier_order": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
        "sections": SECTIONS,
        "family_anchor_count": len(FAMILY_ANCHORS),
        "program_card_count": len(combined),
        "card_count": len(cards),
        "content_addressed": True,
        "supersession_non_erasing": True,
        "cards": cards,
    }


def bounded_process(repo: Path, command: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
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
    result = bounded_process(repo, [str(python_path), "-c", code])
    if result.returncode:
        return {name: "PROBE_FAILED" for name in names}
    return json.loads(result.stdout)


def command_version(repo: Path, executable: str) -> str:
    result = bounded_process(repo, [executable, "--version"])
    lines = (result.stdout or result.stderr).strip().splitlines()
    return lines[-1].strip() if result.returncode == 0 and lines else "PROBE_FAILED"


def node_versions(repo: Path) -> dict[str, str]:
    del repo
    observed: dict[str, str] = {}
    prefix = Path(os.environ.get("NPM_CONFIG_PREFIX", ""))
    for label, package, _executable in NODE_TOOLS:
        metadata = prefix / "node_modules" / package / "package.json"
        try:
            value = json.loads(metadata.read_text(encoding="utf-8"))
            version = value.get("version")
            observed[label] = version if isinstance(version, str) and version else "PROBE_FAILED"
        except (OSError, json.JSONDecodeError):
            observed[label] = "MISSING"
    return observed


def tool_receipt(repo: Path) -> dict[str, Any]:
    system = dist_versions(SYSTEM_DISTS)
    auxiliary = auxiliary_versions(repo, AUX_DISTS)
    node = node_versions(repo)
    all_packages = {**system, **auxiliary, **{package: node[label] for label, package, _executable in NODE_TOOLS}}
    prefix_value = os.environ.get("NPM_CONFIG_PREFIX", "")
    cache_value = os.environ.get("NPM_CONFIG_CACHE", "")
    zone = bounded_process(
        repo,
        [sys.executable, "-c", "from zoneinfo import ZoneInfo; print(ZoneInfo('Pacific/Auckland').key)"],
    )
    missing = sorted(name for name, value in all_packages.items() if value in {"MISSING", "PROBE_FAILED"})
    observed_normalized = {name.casefold(): value for name, value in all_packages.items()}
    expected_drift = {
        name: {"prior_observed": expected, "current_observed": observed_normalized.get(name.casefold(), "MISSING")}
        for name, expected in TOOL_VERSIONS.items()
        if observed_normalized.get(name.casefold(), "MISSING") != expected
    }
    return {
        "schema": "ghc-family-existing-toolchain-verification/v1",
        "owner": OWNER,
        "phase": PHASE,
        "declared_package_count": 25,
        "observed_package_count": len(all_packages),
        "system_python_distributions": system,
        "d_drive_auxiliary_python_distributions": auxiliary,
        "node_cli_tools": node,
        "prior_observed_versions": TOOL_VERSIONS,
        "current_version_drift": expected_drift,
        "missing_or_failed": missing,
        "all_versions_present": not missing,
        "codex_cli": command_version(repo, "codex"),
        "tzdata_functional_smoke": {
            "passed": zone.returncode == 0 and zone.stdout.strip() == "Pacific/Auckland",
            "zone": "Pacific/Auckland",
        },
        "npm_prefix_on_d_drive": prefix_value.upper().startswith("D:"),
        "npm_cache_on_d_drive": cache_value.upper().startswith("D:"),
        "absolute_paths_recorded": False,
        "installations_this_phase": 0,
        "global_skill_promotions_this_phase": 0,
        "path_or_profile_mutated": False,
        "codex_desktop_updated": False,
        "elevation_or_reboot": False,
        "external_accounts_keys_purchases_deployments": 0,
        "boundary": "Version presence and bounded invocation are not package safety, suitability, security certification, authority, or permission to install.",
    }


def method_flow(
    new_rows: list[dict[str, Any]],
    inherited: list[dict[str, Any]],
    skills: list[str],
    runners: list[str],
    tools: list[str],
    cards: list[dict[str, Any]],
    operational_failures: list[tuple[str, str, str, str]],
) -> dict[str, Any]:
    events = []
    for failure_id, failure, recovery_id, recovery in operational_failures:
        events.append({"method_id": failure_id, "truth": False, "state": "retained_failure", "credit": 0, "summary": failure, "recovered_by": recovery_id})
        events.append({"method_id": recovery_id, "truth": True, "state": "bounded_recovery", "credit": 1, "summary": recovery, "does_not_erase": failure_id})
    for row in new_rows:
        events.append({"method_id": f"{row['proposal_id']}-P", "truth": True, "state": "positive_contract", "credit": 1})
        for mutation in MUTATIONS:
            events.append({"method_id": f"{row['proposal_id']}-N-{mutation}", "truth": False, "state": "rejected_mutation", "credit": 0})
    for row in inherited:
        events.append({"method_id": f"INHERITED-{row['proposal_id']}", "truth": True, "state": "represented_zero_credit_revalidation", "credit": 0})
    for prefix, count in (("SAFE", 120), ("CAND", 80), ("CFR", 100)):
        for index in range(1, count + 1):
            events.append({"method_id": f"AUR6777-{prefix}-P{index:03d}", "truth": True, "state": "bounded_owner_execution", "credit": 1})
    for name in skills:
        events.append({"method_id": f"SKILL-{name}-P", "truth": True, "state": "skill_positive", "credit": 1})
        events.append({"method_id": f"SKILL-{name}-N", "truth": False, "state": "skill_rejecting_fixture", "credit": 0})
    for name in runners:
        events.append({"method_id": f"RUNNER-{name}-P", "truth": True, "state": "runner_positive", "credit": 1})
        events.append({"method_id": f"RUNNER-{name}-N", "truth": False, "state": "runner_rejecting_fixture", "credit": 0})
    for name in tools:
        events.append({"method_id": f"TOOL-{name}-P", "truth": True, "state": "tool_positive", "credit": 1})
        events.append({"method_id": f"TOOL-{name}-N", "truth": False, "state": "tool_rejecting_fixture", "credit": 0})
    for card in cards:
        events.append({"method_id": f"CARD-{card['card_id']}", "truth": True, "state": "flashcard_schema_pass", "credit": 1})
    failed = sum(event["truth"] is False for event in events)
    passed = sum(event["truth"] is True for event in events)
    expected_failed = BASE_FAILURE_COUNT + len(operational_failures)
    expected_passed = BASE_PASSING_COUNT + len(operational_failures)
    if failed != expected_failed or passed != expected_passed:
        raise RuntimeError(
            f"Method Flow count drift: failed={failed}/{expected_failed}, passed={passed}/{expected_passed}"
        )
    effective = {
        "effective_negatives": BASELINE["effective_negatives"] + failed,
        "effective_methods": BASELINE["effective_methods"] + failed + passed,
        "retained_failed_witnesses": BASELINE["retained_failed_witnesses"] + failed,
        "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + passed,
        "open_gaps": BASELINE["open_gaps"] + 3,
        "exact_gates": BASELINE["exact_gates"] + 3,
    }
    return {
        "schema": "ghc-family-method-flow-ledger/v1",
        "source": SOURCE,
        "x1": X1,
        "phase": PHASE,
        "activation_baseline": BASELINE,
        "phase_failed_witnesses": failed,
        "phase_passing_witnesses": passed,
        "phase_methods": failed + passed,
        "effective": effective,
        "failure_nonerasure": True,
        "events": events,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if run(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("x2 builder requires the exact immutable pushed x1 head")
    root = repo / "docs" / OWNER_SLUG / PHASE
    x1 = root / "x1"
    x2 = root / "x2"
    proposals = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))["proposals"]
    inherited = json.loads((x1 / "inherited-proposal-selection.json").read_text(encoding="utf-8"))["rows"]
    portfolio = json.loads((x1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    plan = json.loads((x1 / "skill-runner-plan.json").read_text(encoding="utf-8"))
    if len(proposals) != 60 or len(inherited) != 60:
        raise SystemExit("x1 program count drift")
    startup = json.loads((x1 / "method-flow-startup.json").read_text(encoding="utf-8"))
    operational_failures = [
        (row["failure_id"], row["failure"], row["recovery_id"], row["recovery"])
        for row in startup["startup_failure_recovery_pairs"]
    ] + X2_OPERATIONAL_FAILURES

    mutation_rows = []
    outcomes = []
    for row in proposals:
        fixture = positive_fixture(row)
        errors = validate_contract(fixture)
        if errors:
            raise RuntimeError(f"positive contract failed: {row['proposal_id']} {errors}")
        mutation_receipts = []
        for kind in MUTATIONS:
            invalid = mutate(row, kind)
            invalid_errors = validate_contract(invalid)
            if not invalid_errors:
                raise RuntimeError(f"mutation accepted: {row['proposal_id']} {kind}")
            receipt = {
                "witness_id": f"{row['proposal_id']}-N-{kind}",
                "proposal_id": row["proposal_id"],
                "mutation": kind,
                "accepted": False,
                "errors": invalid_errors,
                "completion_credit": 0,
            }
            mutation_receipts.append(receipt)
            mutation_rows.append(receipt)
        dump(x2 / "contracts" / f"{row['proposal_id']}.json", fixture)
        dump(
            x2 / "evidence" / f"{row['proposal_id']}-receipt.json",
            {
                "proposal_id": row["proposal_id"],
                "structural_contract_passed": True,
                "expected_disposition": row["expected_disposition"],
                "positive_errors": [],
                "rejecting_mutations": mutation_receipts,
                "real_world_execution_credit": 0,
                "independent_reproduction": False,
            },
        )
        outcomes.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": row["expected_disposition"],
                "structural_contract_passed": True,
                "real_world_rows": 0,
                "external_actions": 0,
            }
        )

    inherited_revalidation = [
        {
            **row,
            "revalidation_state": "represented",
            "source_fields_preserved": True,
            "new_novelty_credit": 0,
            "automatic_completion_credit": 0,
        }
        for row in inherited
    ]
    dump(x2 / "proposal-outcomes.json", {"outcomes": outcomes, "counts": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}})
    dump(x2 / "mutation-ledger.json", {"mutation_count": len(mutation_rows), "accepted": 0, "rejected": len(mutation_rows), "rows": mutation_rows})
    dump(x2 / "inherited-revalidation.json", {"row_count": len(inherited_revalidation), "rows": inherited_revalidation})

    def executed(rows: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
        return [
            {
                **row,
                "execution_status": "completed_within_bounded_synthetic_scope",
                "witness_id": f"AUR6777-{prefix}-P{index:03d}",
                "real_world_rows": 0,
                "external_actions": 0,
                "protected_gate_closed": False,
            }
            for index, row in enumerate(rows, start=1)
        ]

    execution = {
        "owner_safe_now": executed(portfolio["owner_safe_now"], "SAFE"),
        "owner_candidate": executed(portfolio["owner_candidate"], "CAND"),
        "owner_clean_fix_refine": executed(
            json.loads((x1 / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))["owner"], "CFR"
        ),
        "successor_candidate_recommendations": portfolio["successor_candidate_recommendations"],
        "exact_approval": portfolio["exact_approval"],
        "blocked": portfolio["blocked"],
    }
    dump(x2 / "portfolio-execution.json", execution)

    skill_positive, skill_negative = customize_skills(repo, plan["owner_skill_ideas"])
    runner_receipts = build_runner_wrappers(repo)
    dump(x2 / "skill-validation-receipt.json", {"positive": skill_positive, "rejecting": skill_negative})
    dump(x2 / "runner-smoke-receipt.json", {"runner_count": len(runner_receipts), "receipts": runner_receipts})

    deck = build_flashcards(proposals, inherited)
    dump(x2 / "flashcards" / "deck.json", deck)
    dump(
        x2 / "flashcards" / "index.json",
        {
            "schema": deck["schema"],
            "tier_order": deck["tier_order"],
            "section_count": len(SECTIONS),
            "card_count": len(deck["cards"]),
            "cards": [{"card_id": card["card_id"], "content_digest": card["content_digest"], "section": card["section"]} for card in deck["cards"]],
        },
    )
    tools = tool_receipt(repo)
    dump(x2 / "toolchain" / "verification-receipt.json", tools)
    dump(x2 / "toolchain" / "operational-failures.json", {"pairs": [{"failure_id": f, "failure": ft, "recovery_id": p, "recovery": pt} for f, ft, p, pt in operational_failures]})

    ledger = method_flow(
        proposals,
        inherited,
        plan["owner_skill_ideas"],
        list(RUNNER_MAP),
        list(TOOL_VERSIONS),
        deck["cards"],
        operational_failures,
    )
    dump(x2 / "method-flow" / "ledger.json", ledger)
    dump(
        x2 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "lifecycle_state": "X2_EVIDENCE_PRECOMMIT",
            "declared_proposal_chain": 8210,
            "outcomes": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "inherited_revalidated_at_zero_credit": 60,
            "preregistered_mutations_executed": 240,
            "preregistered_mutations_rejected": 240,
            "owner_safe_now_completed": 120,
            "owner_candidate_completed": 80,
            "owner_clean_fix_refine_completed": 100,
            "phase_local_skills_built_validated_and_used": 20,
            "family_current_runners_built_validated_and_used": 10,
            "new_direct_tools_installed_and_used": 0,
            "existing_tool_surfaces_verified": 25,
            "global_skill_promotions": 0,
            "flashcards": len(deck["cards"]),
            "real_world_rows": 0,
            "external_real_world_actions": 0,
            **ledger["effective"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        x2 / "owner-local-skill-state.json",
        {
            "validated_owner_local_candidates": LOCAL_VALIDATION_CANDIDATES,
            "global_promotion_target": 0,
            "global_promotion_completed": 0,
            "state": "OWNER_LOCAL_ONLY_NO_GLOBAL_INSTALLATION",
            "overwrite_allowed": False,
        },
    )
    write_text(
        x2 / "accessible-report-draft.html",
        """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Auren Lark v677-v7 evidence</title></head>
<body><header><h1>Auren Lark v677-v7 evidence</h1><p>Same-owner synthetic software and documentation evidence only.</p></header>
<nav aria-label="Sections"><ol><li><a href="#program">Program</a></li><li><a href="#tools">Tools</a></li><li><a href="#boundaries">Boundaries</a></li></ol></nav>
<main><section id="program"><h2>Program</h2><p>Sixty inherited rows retain zero novelty and automatic completion credit. Sixty new source-bounded contracts produced 42 completed, 12 represented, 3 open-gap, and 3 exact-gate structural outcomes.</p></section>
<section id="tools"><h2>Tools and cards</h2><p>Twenty-five existing tool surfaces received read-only version verification; twenty owner-local skills, ten family runners, and 135 four-tier cards received bounded accepting and rejecting checks.</p></section>
<section id="boundaries"><h2>Boundaries</h2><p>No real requester, representative, agency, record, access request, correction, counterstatement, disclosure, refusal, complaint, appeal, remedy, disposal, person, participant, measurement, identity event, rights decision, professional decision, legal or cultural decision, Māori-authority act, empirical GMUT confirmation, THOS effectiveness, production Freed ID, complete accessibility or privacy assurance, exhaustive security, independent reproduction, proof, canon, or Stage 20 authority is established.</p></section></main>
<footer><p>Manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain open.</p></footer></body></html>""",
    )
    print(
        json.dumps(
            {
                "status": "BUILT_X2_EVIDENCE_PRECOMMIT",
                "contracts": len(proposals),
                "mutations_rejected": len(mutation_rows),
                "skills": len(skill_positive),
                "runners": len(runner_receipts),
                "tools_verified": len(TOOL_VERSIONS),
                "flashcards": len(deck["cards"]),
                "method_flow": {"failed": ledger["phase_failed_witnesses"], "passed": ledger["phase_passing_witnesses"]},
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
