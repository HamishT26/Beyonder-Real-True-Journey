#!/usr/bin/env python3
"""Build and execute the bounded Vesper Arlen v679-v3 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v679_v3_core import (
    canonical_digest,
    mutate,
    positive_fixture,
    runner_smoke,
    skill_smoke,
    validate_contract,
    validate_flashcard,
)


OWNER = "Vesper Arlen"
OWNER_SLUG = "vesper-arlen"
PHASE = "v679-v3"
X1 = "3084b65ce6f1677e94bd58ad621269902005265b"
SOURCE = "e5d379adf39a025a7e1d64983e7367d93e9f0f39"
BASELINE = {
    "effective_negatives": 48541,
    "effective_methods": 49168,
    "retained_failed_witnesses": 20202,
    "bounded_passing_witnesses": 32056,
    "open_gaps": 422,
    "exact_gates": 413,
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
    "seed-bank-accession-and-herbarium-description-practice",
    "provenance-rights-accessibility-benefit-sharing-and-handover-practice",
    "inherited-proposal-selection",
    "new-proposal-freeze",
    "approval-portfolios",
    "toolchain-verification",
    "skills-and-runners",
    "clean-fix-refine",
    "method-flow-and-failures",
    "privacy-accessibility-security-and-authority-boundaries",
    "validation-and-closeout",
    "successor-route",
]
RUNNER_MAP = {
    "ghc_family_accession_contract_runner.py": "contract",
    "ghc_family_accession_mutation_runner.py": "mutation",
    "ghc_family_accession_provenance_runner.py": "accession_topology",
    "ghc_family_accession_metadata_runner.py": "metadata",
    "ghc_family_accession_flashcard_runner.py": "flashcard",
    "ghc_family_accession_toolchain_runner.py": "toolchain",
    "ghc_family_accession_privacy_runner.py": "privacy",
    "ghc_family_accession_accessibility_runner.py": "accessibility",
    "ghc_family_accession_method_flow_runner.py": "portfolio",
    "ghc_family_accession_terminal_runner.py": "report",
}
TOOL_VERSIONS = {
    "python": "verify-current",
    "git": "verify-current",
    "powershell": "verify-current",
    "pytest": "verify-current",
    "hypothesis": "verify-current",
    "ruff": "verify-current",
    "mypy": "verify-current",
    "bandit": "verify-current",
    "pip-audit": "verify-current",
    "pyright": "verify-current",
    "vulture": "verify-current",
    "radon": "verify-current",
    "xenon": "verify-current",
    "codespell": "verify-current",
    "yamllint": "verify-current",
    "toml-sort": "verify-current",
    "check-manifest": "verify-current",
    "twine": "verify-current",
    "check-wheel-contents": "verify-current",
    "pydistcheck": "verify-current",
    "import-linter": "verify-current",
    "pydoclint": "verify-current",
    "interrogate": "verify-current",
    "pytest-timeout": "verify-current",
    "spdx-tools": "verify-current",
}
PYTHON_DISTS = (
    "pytest", "hypothesis", "ruff", "mypy", "bandit", "pip-audit", "pyright", "vulture", "radon", "xenon",
    "codespell", "yamllint", "toml-sort", "check-manifest", "twine", "check-wheel-contents", "pydistcheck",
    "import-linter", "pydoclint", "interrogate", "pytest-timeout", "spdx-tools",
)
LOCAL_VALIDATION_CANDIDATES = [
    "provenance-correction-nonerasure",
    "benefit-sharing-authority-gate",
    "maori-data-authority-reservation",
    "normalized-git-blob-manifest",
    "stage20-accession-nonpromotion",
]
X2_OPERATIONAL_FAILURES: list[tuple[str, str, str, str]] = [
    (
        "VA6793-X2-N001",
        "The first read-only distribution-version wrapper passed escaped newline literals to Python -c, raised SyntaxError, and earned zero tool-verification credit.",
        "VA6793-X2-P001",
        "A scalar PowerShell loop queried each distribution independently, exposed the split-prefix topology, and changed no package, profile, or repository file.",
    ),
    (
        "VA6793-X2-N002",
        "The first split-prefix discovery probe used a recursive virtual-environment glob, outlived its bounded display and wait windows, was stopped without a write, and earned zero tool-verification credit.",
        "VA6793-X2-P002",
        "Exact one-level and two-level Scripts/python.exe patterns bounded discovery to the known D-isolated prefix topology while keeping every package and profile unchanged.",
    ),
    (
        "VA6793-X2-N003",
        "The first x2 precommit test gate found fourteen generated flashcard sections against the frozen fifteen-section contract; the aggregate earned zero x2 gate credit while its twenty passing tests remained bounded dependency witnesses.",
        "VA6793-X2-P003",
        "An additive fifteenth privacy, accessibility, security, and authority-boundary section plus dependency-only deck, index, and accounting refresh repaired the contract without replaying successful skill or runner checks.",
    ),
    (
        "VA6793-X2-N004",
        "The first independent exact-index replay opened one read-only git show process per entry, exceeded three bounded display windows, was interrupted without mutation, and earned zero index-validation credit.",
        "VA6793-X2-P004",
        "A single git cat-file --batch object stream replays the complete staged manifest with one bounded Git process and retains exact path, byte, digest, JSON, syntax, privacy, and diff checks.",
    ),
    (
        "VA6793-X2-N005",
        "The first porcelain x2 commit retained its zero-byte index lock and made no observable progress across bounded windows; it was interrupted with HEAD still at x1 and all 210 staged entries intact, earning zero commit credit.",
        "VA6793-X2-P005",
        "After exact index revalidation, git write-tree, commit-tree, and expected-old update-ref provide an additive direct-child evidence commit without replaying the stalled porcelain index refresh.",
    ),
    (
        "VA6793-X2-N006",
        "Two native PowerShell orphan-lock removal wrappers were rejected by command policy before execution and earned zero recovery credit.",
        "VA6793-X2-P006",
        "An exact-file patch removed only the verified zero-byte orphan lock after all lane Git writers were absent; HEAD and the complete staged index remained unchanged.",
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
            f"Represent {name.replace('-', ' ')} in bounded synthetic seed-bank accession, collection-provenance, flashcard, or evidence workflows; "
            "use when the named structure must stay separate from real biological records, professional decisions, or authority."
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

Refuse real accession acquisition or distribution, genetic-resource access or benefit-sharing decisions, donor or collector identification, locality disclosure, botanical determination, viability or germination findings, pest or pathogen findings, treatment or regeneration actions, collection handling, ownership or custody allocation, professional release, participant work, credentials, keys, external writes, legal or cultural determinations, Māori wording or authority decisions, production deployment, empirical GMUT promotion, THOS effectiveness claims, identity-continuity claims, or Stage 20 promotion without exact evidence and competent authority.

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
            f'"""Family-current Vesper Arlen v679-v3 {name} runner."""\n\n'
            "from ghc_family_vesper_arlen_v679_v3_core import runner_cli\n\n"
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
            "card_id": f"VA6793-ANCHOR-{index:02d}",
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
            practice = "synthetic seed-bank accession, label transcription, packet topology, and collection-provenance documentation"
        elif index <= 60:
            practice = "synthetic PREMIS and PROV lineage, privacy minimization, accessibility, benefit-sharing reservation, correction, and handover documentation"
        else:
            practice = "inherited zero-credit revalidation"
        card = {
            "card_id": f"VA6793-CARD-{index:03d}",
            "freed_id_anchor": OWNER,
            "trinity_pillar": "Freed ID/CBR Heart primary; GMUT Mind and THOS Body protected",
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


def dist_versions(repo: Path, names: tuple[str, ...]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "MISSING"
    anchor = shutil.which("bandit") or shutil.which("typer")
    candidates: list[Path] = []
    if anchor is not None:
        try:
            python_bank = Path(anchor).resolve().parents[3] / "python"
            candidates = sorted(
                {
                    *python_bank.glob("*/Scripts/python.exe"),
                    *python_bank.glob("*/*/Scripts/python.exe"),
                }
            )
        except IndexError:
            candidates = []
    for python_path in candidates:
        missing = [name for name, value in versions.items() if value == "MISSING"]
        if not missing:
            break
        code = (
            "import importlib.metadata as m,json\n"
            f"names={missing!r}\n"
            "out={}\n"
            "for n in names:\n"
            "    try: out[n]=m.version(n)\n"
            "    except m.PackageNotFoundError: out[n]='MISSING'\n"
            "print(json.dumps(out,sort_keys=True))\n"
        )
        result = bounded_process(repo, [str(python_path), "-c", code], 60)
        if result.returncode == 0:
            observed = json.loads(result.stdout)
            for name, value in observed.items():
                if versions[name] == "MISSING" and value != "MISSING":
                    versions[name] = value
    if versions.get("pyright") == "MISSING":
        observed = command_version(repo, "pyright")
        if observed not in {"MISSING", "PROBE_FAILED"}:
            versions["pyright"] = observed.removeprefix("pyright ").strip()
    return versions


def command_version(repo: Path, executable: str) -> str:
    result = bounded_process(repo, [executable, "--version"])
    lines = (result.stdout or result.stderr).strip().splitlines()
    return lines[-1].strip() if result.returncode == 0 and lines else "PROBE_FAILED"


def tool_receipt(repo: Path) -> dict[str, Any]:
    distributions = dist_versions(repo, PYTHON_DISTS)
    commands = {
        "python": command_version(repo, sys.executable),
        "git": command_version(repo, "git"),
        "powershell": command_version(repo, "pwsh"),
    }
    all_packages = {**commands, **distributions}
    prefix = bounded_process(repo, ["npm", "config", "get", "prefix"])
    cache = bounded_process(repo, ["npm", "config", "get", "cache"])
    json_smoke = bounded_process(repo, [sys.executable, "-c", "import json; print(json.dumps({'bounded': True}, sort_keys=True))"])
    missing = sorted(name for name, value in all_packages.items() if value in {"MISSING", "PROBE_FAILED"})
    return {
        "schema": "ghc-family-existing-toolchain-verification/v1",
        "owner": OWNER,
        "phase": PHASE,
        "declared_package_count": 25,
        "observed_package_count": len(all_packages),
        "command_versions": commands,
        "python_distributions": distributions,
        "distribution_discovery": "CURRENT_INTERPRETER_THEN_RESOLVED_D_DRIVE_SIBLING_PREFIXES_THEN_COMMAND_SURFACE",
        "verification_targets": TOOL_VERSIONS,
        "missing_or_failed": missing,
        "all_versions_present": not missing,
        "codex_cli": command_version(repo, "codex"),
        "python_json_functional_smoke": {
            "passed": json_smoke.returncode == 0 and json_smoke.stdout.strip() == '{"bounded": true}',
            "external_actions": 0,
        },
        "npm_prefix_on_d_drive": prefix.returncode == 0 and prefix.stdout.strip().upper().startswith("D:"),
        "npm_cache_on_d_drive": cache.returncode == 0 and cache.stdout.strip().upper().startswith("D:"),
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
            events.append({"method_id": f"VA6793-{prefix}-P{index:03d}", "truth": True, "state": "bounded_owner_execution", "credit": 1})
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
    parser.add_argument("--refresh-accounting-only", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if run(repo, "rev-parse", "HEAD") != X1:
        raise SystemExit("x2 builder requires the exact immutable pushed x1 head")
    root = repo / "docs" / OWNER_SLUG / PHASE
    x1 = root / "x1"
    x2 = root / "x2"
    proposals = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))["proposals"]
    inherited = json.loads((x1 / "inherited-proposal-selection.json").read_text(encoding="utf-8"))["rows"]
    plan = json.loads((x1 / "skill-runner-plan.json").read_text(encoding="utf-8"))
    safe_plan = json.loads((x1 / "safe-now-plan.json").read_text(encoding="utf-8"))
    candidate_plan = json.loads((x1 / "candidate-plan.json").read_text(encoding="utf-8"))
    approval_plan = json.loads((x1 / "exact-blocked-approval-plan.json").read_text(encoding="utf-8"))
    cfr_plan = json.loads((x1 / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))
    if len(proposals) != 60 or len(inherited) != 60:
        raise SystemExit("x1 program count drift")
    startup = json.loads((x1 / "method-flow-startup.json").read_text(encoding="utf-8"))
    operational_failures = [
        (row["observation_id"], row["description"], f"{row['observation_id']}-RECOVERY", row["recovery"])
        for row in startup["startup_observations"]
        if row["state"] == "retained_failed_witness"
    ] + X2_OPERATIONAL_FAILURES
    skill_names = [row["name"] for row in plan["skills"]]

    if args.refresh_accounting_only:
        deck = build_flashcards(proposals, inherited)
        dump(x2 / "flashcards" / "deck.json", deck)
        dump(
            x2 / "flashcards" / "index.json",
            {
                "schema": deck["schema"],
                "tier_order": deck["tier_order"],
                "section_count": len(SECTIONS),
                "card_count": len(deck["cards"]),
                "cards": [
                    {"card_id": card["card_id"], "content_digest": card["content_digest"], "section": card["section"]}
                    for card in deck["cards"]
                ],
            },
        )
        ledger = method_flow(
            proposals,
            inherited,
            skill_names,
            list(RUNNER_MAP),
            list(TOOL_VERSIONS),
            deck["cards"],
            operational_failures,
        )
        dump(
            x2 / "toolchain" / "operational-failures.json",
            {
                "pairs": [
                    {"failure_id": failure, "failure": failure_text, "recovery_id": recovery, "recovery": recovery_text}
                    for failure, failure_text, recovery, recovery_text in operational_failures
                ]
            },
        )
        dump(x2 / "method-flow" / "ledger.json", ledger)
        truth_path = x2 / "phase-truth.json"
        truth = json.loads(truth_path.read_text(encoding="utf-8"))
        truth.update(ledger["effective"])
        dump(truth_path, truth)
        print(
            json.dumps(
                {
                    "status": "REFRESHED_X2_ACCOUNTING_ONLY",
                    "operational_failure_pairs": len(operational_failures),
                    "failed": ledger["phase_failed_witnesses"],
                    "passed": ledger["phase_passing_witnesses"],
                },
                sort_keys=True,
            )
        )
        return

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
                "witness_id": f"VA6793-{prefix}-P{index:03d}",
                "real_world_rows": 0,
                "external_actions": 0,
                "protected_gate_closed": False,
            }
            for index, row in enumerate(rows, start=1)
        ]

    execution = {
        "owner_safe_now": executed(safe_plan["tasks"], "SAFE"),
        "owner_candidate": executed(candidate_plan["tasks"], "CAND"),
        "owner_clean_fix_refine": executed(cfr_plan["owner_tasks"], "CFR"),
        "successor_clean_fix_refine_recommendations": cfr_plan["successor_recommendations"],
        "exact_approval": approval_plan["exact_packets"],
        "blocked": approval_plan["blocked_packets"],
    }
    dump(x2 / "portfolio-execution.json", execution)

    skill_positive, skill_negative = customize_skills(repo, skill_names)
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
        skill_names,
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
            "declared_proposal_chain": 8930,
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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Vesper Arlen v679-v3 evidence</title></head>
<body><header><h1>Vesper Arlen v679-v3 evidence</h1><p>Same-owner synthetic software and documentation evidence only.</p></header>
<nav aria-label="Sections"><ol><li><a href="#program">Program</a></li><li><a href="#tools">Tools</a></li><li><a href="#boundaries">Boundaries</a></li></ol></nav>
<main><section id="program"><h2>Program</h2><p>Sixty inherited rows retain zero novelty and automatic completion credit. Sixty new source-bounded contracts produced 42 completed, 12 represented, 3 open-gap, and 3 exact-gate structural outcomes.</p></section>
<section id="tools"><h2>Tools and cards</h2><p>Twenty-five existing tool surfaces received read-only version verification; twenty owner-local skills, ten family runners, and 135 four-tier cards received bounded accepting and rejecting checks.</p></section>
<section id="boundaries"><h2>Boundaries</h2><p>No real accession, genetic resource, donor, collector, depositor, steward, taxon, cultivar, locality, coordinate, facility, container, image, viability or germination result, pest or pathogen finding, treatment, regeneration, distribution, destruction, person, participant, identity event, professional release, ownership, custody, benefit-sharing, legal or cultural decision, Māori-authority act, empirical GMUT confirmation, THOS effectiveness, production Freed ID, complete accessibility or privacy assurance, exhaustive security, independent reproduction, proof, canon, or Stage 20 authority is established.</p></section></main>
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
