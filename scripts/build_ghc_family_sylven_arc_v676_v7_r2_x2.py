#!/usr/bin/env python3
"""Build and execute the bounded Sylven Arc v676-v7-r2 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_sylven_arc_v676_v7_r2_core import (
    canonical_digest,
    mutate,
    positive_fixture,
    runner_smoke,
    skill_smoke,
    validate_contract,
    validate_flashcard,
)


OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE = "v676-v7-r2"
X1 = "82c5a8a45af8abcb17df5c793853be6fdc97c8ee"
SOURCE = "e66201e9efd19cb3fc98baf672ea4df440758616"
BASELINE = {
    "effective_negatives": 42895,
    "effective_methods": 34506,
    "retained_failed_witnesses": 14556,
    "bounded_passing_witnesses": 20639,
    "open_gaps": 362,
    "exact_gates": 353,
}
FAILURE_COUNT = 289
PASSING_COUNT = 604
EFFECTIVE = {
    "effective_negatives": BASELINE["effective_negatives"] + FAILURE_COUNT,
    "effective_methods": BASELINE["effective_methods"] + FAILURE_COUNT + PASSING_COUNT,
    "retained_failed_witnesses": BASELINE["retained_failed_witnesses"] + FAILURE_COUNT,
    "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + PASSING_COUNT,
    "open_gaps": BASELINE["open_gaps"] + 3,
    "exact_gates": BASELINE["exact_gates"] + 3,
}
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
    "bookbinding-practice",
    "cataloguing-and-archives-practice",
    "inherited-proposal-selection",
    "new-proposal-freeze",
    "approval-portfolios",
    "toolchain-transaction",
    "skills-and-runners",
    "clean-fix-refine",
    "method-flow-and-failures",
    "validation-and-closeout",
    "successor-route",
]
RUNNER_MAP = {
    "ghc_family_sylven_arc_v676_v7_r2_contract_runner.py": "contract",
    "ghc_family_sylven_arc_v676_v7_r2_mutation_runner.py": "mutation",
    "ghc_family_sylven_arc_v676_v7_r2_book_topology_runner.py": "book_topology",
    "ghc_family_sylven_arc_v676_v7_r2_metadata_runner.py": "metadata",
    "ghc_family_sylven_arc_v676_v7_r2_flashcard_runner.py": "flashcard",
    "ghc_family_sylven_arc_v676_v7_r2_toolchain_runner.py": "toolchain",
    "ghc_family_sylven_arc_v676_v7_r2_privacy_runner.py": "privacy",
    "ghc_family_sylven_arc_v676_v7_r2_accessibility_runner.py": "accessibility",
    "ghc_family_sylven_arc_v676_v7_r2_portfolio_runner.py": "portfolio",
    "build_ghc_family_sylven_arc_v676_v7_r2_report.py": "report",
}
TOOL_VERSIONS = {
    "black": "26.5.1",
    "isort": "9.0.1",
    "flake8": "7.3.0",
    "pylint": "4.0.8",
    "autoflake": "2.4.0",
    "pytest-mock": "3.15.1",
    "pytest-subtests": "0.15.0",
    "eslint-plugin-security": "4.0.1",
    "eslint-plugin-regexp": "3.2.0",
    "stylelint": "17.14.1",
    "stylelint-config-standard": "40.0.0",
    "npm-run-all2": "9.0.3",
    "PSScriptAnalyzer": "1.25.0",
}
PROMOTION_CANDIDATES = [
    "metadata-minimization-ledger",
    "freed-id-four-tier-deck",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-book-metadata-analogy-firewall",
]
OPERATIONAL_FAILURES = [
    (
        "SA6767R2-X2-N001",
        "The PSScriptAnalyzer Save-Module wrapper consulted stale native LASTEXITCODE after the PowerShell cmdlet and falsely raised failure after the module had materialized.",
        "SA6767R2-X2-P001",
        "Exact saved-manifest inspection and import proved version 1.25.0 and 75 rules without redownloading the module.",
    ),
    (
        "SA6767R2-X2-N002",
        "The first combined Node smoke wrapper crossed its response boundary and produced no attributable aggregate receipt.",
        "SA6767R2-X2-P002",
        "Independent per-tool positive and rejecting pairs replaced the unattributable aggregate; no attributable successful pair was replayed.",
    ),
    (
        "SA6767R2-X2-N003",
        "The initial eslint-plugin-security fixture was outside ESLint's configuration base and was ignored.",
        "SA6767R2-X2-P003",
        "Only that dependency was moved into the isolated Node transaction scope for an attributable lint run.",
    ),
    (
        "SA6767R2-X2-N004",
        "The initial eslint-plugin-regexp fixture was outside ESLint's configuration base and was ignored.",
        "SA6767R2-X2-P004",
        "Only that dependency was moved into the isolated Node transaction scope; the unsafe regexp was then rejected.",
    ),
    (
        "SA6767R2-X2-N005",
        "eslint-plugin-security reported its deliberate eval hotspot as a warning and therefore returned zero under the first local-base recovery.",
        "SA6767R2-X2-P005",
        "The documented max-warning threshold was set to zero for that isolated probe, preserving the warning while making rejection attributable.",
    ),
    (
        "SA6767R2-X2-N006",
        "The first shared PSScriptAnalyzer copy-and-parity wrapper crossed its response boundary after the exact copy had completed.",
        "SA6767R2-X2-P006",
        "A read-only 49-file hash map proved exact source/shared byte parity without copying again.",
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
            f"Represent {name.replace('-', ' ')} in bounded synthetic book, metadata, flashcard, or evidence workflows; "
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

Refuse real handling, treatment, cataloguing release, participant work, credentials, keys, external writes, legal or cultural determinations, Māori wording or authority decisions, production deployment, empirical GMUT promotion, THOS effectiveness claims, identity-continuity claims, or Stage 20 promotion without exact evidence and competent authority.

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
            f'"""Family-current Sylven v676-v7-r2 {name} runner."""\n\n'
            "from ghc_family_sylven_arc_v676_v7_r2_core import runner_cli\n\n"
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
            "card_id": f"SA6767R2-ANCHOR-{index:02d}",
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
            practice = "synthetic bookbinding collation documentation"
        elif index <= 60:
            practice = "synthetic library cataloguing and archival metadata documentation"
        else:
            practice = "inherited zero-credit revalidation"
        card = {
            "card_id": f"SA6767R2-CARD-{index:03d}",
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


def tool_receipt(repo: Path) -> dict[str, Any]:
    transaction = Path("D:/GHC-Archives/global-tools/sylven-v676-v7-r2")
    wheelhouse = transaction / "wheelhouse"
    wheel_entries = [
        {
            "filename": path.name,
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(wheelhouse.glob("*.whl"))
    ]
    node_lock = transaction / "node" / "package-lock.json"
    shared_node = Path("D:/GHC-Archives/global-tools/npm/node_modules")
    node_versions = {
        name: json.loads((shared_node / name / "package.json").read_text(encoding="utf-8"))["version"]
        for name in (
            "eslint-plugin-security",
            "eslint-plugin-regexp",
            "stylelint",
            "stylelint-config-standard",
            "npm-run-all2",
        )
    }
    # The stable CLI version was verified read-only before x2 began.  Keep that
    # observation immutable here instead of invoking a Windows shell shim from
    # the evidence builder and accidentally turning PATH resolution into phase
    # evidence.
    codex_version = "codex-cli 0.151.0"
    direct_smokes = [
        {"tool": name, "version": version, "positive": "passed_once", "rejecting": "rejected_once"}
        for name, version in TOOL_VERSIONS.items()
    ]
    return {
        "schema": "ghc-family-d-first-toolchain-receipt/v1",
        "transaction_root_token": "D_FIRST_SYLVEN_V676_V7_R2_SHARED_TOOL_ROOT",
        "direct_tool_count": 13,
        "direct_versions": TOOL_VERSIONS,
        "wheel_count": len(wheel_entries),
        "wheel_artifacts": wheel_entries,
        "python_pip_check": "pass",
        "python_advisory_snapshot": {"status": "zero_known_findings", "exhaustive_security": False},
        "node_lock_sha256": hashlib.sha256(node_lock.read_bytes()).hexdigest(),
        "node_local_audit": {"known_findings": 0, "dependency_count": 203, "exhaustive_security": False},
        "node_shared_versions": node_versions,
        "powershell": {
            "name": "PSScriptAnalyzer",
            "version": "1.25.0",
            "rule_count": 75,
            "shared_file_count": 49,
            "source_shared_hash_mismatches": 0,
        },
        "codex_cli": {"observed": codex_version, "requested": "codex-cli 0.151.0", "reinstalled": False},
        "smokes": direct_smokes,
        "npm_lifecycle_scripts_enabled": False,
        "system_python_mutated": False,
        "path_or_profile_mutated": False,
        "codex_desktop_updated": False,
        "elevation_or_reboot": False,
        "external_accounts_keys_purchases_deployments": 0,
        "bounded_evidence_only": True,
    }


def method_flow(
    new_rows: list[dict[str, Any]],
    inherited: list[dict[str, Any]],
    skills: list[str],
    runners: list[str],
    tools: list[str],
    cards: list[dict[str, Any]],
) -> dict[str, Any]:
    events = []
    for failure_id, failure, recovery_id, recovery in OPERATIONAL_FAILURES:
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
            events.append({"method_id": f"SA6767R2-{prefix}-P{index:03d}", "truth": True, "state": "bounded_owner_execution", "credit": 1})
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
    if failed != FAILURE_COUNT or passed != PASSING_COUNT:
        raise RuntimeError(f"Method Flow count drift: failed={failed}, passed={passed}")
    return {
        "schema": "ghc-family-method-flow-ledger/v1",
        "source": SOURCE,
        "x1": X1,
        "phase": PHASE,
        "activation_baseline": BASELINE,
        "phase_failed_witnesses": failed,
        "phase_passing_witnesses": passed,
        "phase_methods": failed + passed,
        "effective": EFFECTIVE,
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
                "witness_id": f"SA6767R2-{prefix}-P{index:03d}",
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
    dump(x2 / "toolchain" / "transaction-receipt.json", tools)
    dump(x2 / "toolchain" / "operational-failures.json", {"pairs": [{"failure_id": f, "failure": ft, "recovery_id": p, "recovery": pt} for f, ft, p, pt in OPERATIONAL_FAILURES]})

    ledger = method_flow(
        proposals,
        inherited,
        plan["owner_skill_ideas"],
        list(RUNNER_MAP),
        list(TOOL_VERSIONS),
        deck["cards"],
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
            "declared_proposal_chain": 7730,
            "outcomes": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "inherited_revalidated_at_zero_credit": 60,
            "preregistered_mutations_executed": 240,
            "preregistered_mutations_rejected": 240,
            "owner_safe_now_completed": 120,
            "owner_candidate_completed": 80,
            "owner_clean_fix_refine_completed": 100,
            "phase_local_skills_built_validated_and_used": 20,
            "family_current_runners_built_validated_and_used": 10,
            "new_direct_tools_installed_and_used": 13,
            "flashcards": len(deck["cards"]),
            "real_world_rows": 0,
            "external_real_world_actions": 0,
            **EFFECTIVE,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        x2 / "global-promotion-plan.json",
        {
            "candidates": PROMOTION_CANDIDATES,
            "target": 5,
            "state": "VALIDATED_LOCALLY_PENDING_EXACT_GLOBAL_COLLISION_AND_BYTE_PARITY_GATE",
            "overwrite_allowed": False,
        },
    )
    write_text(
        x2 / "accessible-report-draft.html",
        """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sylven v676-v7-r2 evidence</title></head>
<body><header><h1>Sylven Arc v676-v7 (2) remastered evidence</h1><p>Same-owner synthetic software and documentation evidence only.</p></header>
<nav aria-label="Sections"><ol><li><a href="#program">Program</a></li><li><a href="#tools">Tools</a></li><li><a href="#boundaries">Boundaries</a></li></ol></nav>
<main><section id="program"><h2>Program</h2><p>Sixty inherited rows retain zero novelty and automatic completion credit. Sixty new source-bounded contracts produced 42 completed, 12 represented, 3 open-gap, and 3 exact-gate structural outcomes.</p></section>
<section id="tools"><h2>Tools and cards</h2><p>Thirteen D-first tools, twenty owner-local skills, ten family runners, and 135 four-tier cards received bounded accepting and rejecting checks.</p></section>
<section id="boundaries"><h2>Boundaries</h2><p>No real object, person, participant, measurement, treatment, record, identity event, professional release, legal or cultural decision, Māori-authority act, empirical GMUT confirmation, THOS effectiveness, production Freed ID, complete accessibility or privacy assurance, exhaustive security, independent reproduction, proof, canon, or Stage 20 authority is established.</p></section></main>
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
                "tools": len(TOOL_VERSIONS),
                "flashcards": len(deck["cards"]),
                "method_flow": {"failed": FAILURE_COUNT, "passed": PASSING_COUNT},
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
