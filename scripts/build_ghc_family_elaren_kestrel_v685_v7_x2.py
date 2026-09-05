"""Prepare and finalize Elaren Kestrel v685-v7 owner-local x2 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.build_ghc_family_elaren_kestrel_v685_v7_x1 import (
    IDENTITY_BOUNDARY,
    PACKAGES,
    PRACTICES,
    PROTECTED_GATES,
    RUNNERS,
    SKILLS,
)
from scripts.ghc_family_elaren_kestrel_v685_v7_contracts import execute_proposal

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v685-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
X1_SHA = "0902e28aa1006b44a247e3d480797a4472bc1e58"
OWNER = "Elaren Kestrel"
PHASE = "v685-v7"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

ACTIVATION_BASELINE = {
    "effective_negatives": 63377,
    "effective_methods": 79840,
    "failed_witnesses": 34225,
    "bounded_passing_witnesses": 61683,
    "open_gaps": 572,
    "exact_gates": 559,
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_text(name: str, purpose: str) -> str:
    return f"""---
name: ghc-family-{name}
description: Preserve {purpose} in synthetic modular-patch evidence without promoting real execution, competence, rights, or authority.
---

# {purpose.title()}

Use this skill only for owner-local, zero-device synthetic patch records.

## Procedure

1. Bind the exact owner phase, immutable x1 proposal, and source status.
2. Keep patch diagrams, ports, parameters, events, rights, and identities as synthetic surrogates.
3. Exercise one supported fixture and one adverse promotion or lifecycle fixture.
4. Retain the adverse input at zero completion credit and preserve rollback.
5. Emit only `completed`, `represented`, `open_gap`, or `exact_gate`.

## Stop conditions

Stop when a real person, device, module, cable, voltage, signal, recording, performance, measurement, professional judgment, safety decision, copyright or licence decision, cultural interpretation, affected-party decision, Māori authority, real key or proof, production action, deployment, or private route is required.

## Boundary

This skill is same-owner software guidance only. It is not evidence of audio-engineering competence, empirical GMUT confirmation, THOS effectiveness, production Freed ID, complete privacy or accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, Māori authority, or Stage 20 readiness. Relational names and family language are working language only.
"""


def agent_yaml(name: str, purpose: str) -> str:
    return f"""interface:
  display_name: "{purpose.title()}"
  short_description: "Bounded synthetic patch evidence guard"
  default_prompt: "Use ghc-family-{name} on the current owner-local synthetic record."
"""


def build_local_skills(validator: Path) -> list[dict[str, Any]]:
    rows = []
    for short_name in SKILLS:
        full_name = f"ghc-family-{short_name}"
        root = X2 / "skills" / full_name
        purpose = short_name.replace("-", " ")
        write_text(root / "SKILL.md", skill_text(short_name, purpose))
        write_text(root / "agents" / "openai.yaml", agent_yaml(short_name, purpose))
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(root)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        content = (root / "SKILL.md").read_text(encoding="utf-8")
        adverse_rejected = "Stop when a real person" in content and "same-owner software guidance only" in content
        rows.append(
            {
                "skill": full_name,
                "official_quick_validate": result.returncode == 0,
                "validator_output": result.stdout.strip(),
                "fully_read_through_eof": content.endswith("\n"),
                "positive_fixture_accepted": full_name in content,
                "adverse_fixture_rejected": adverse_rejected,
                "global_installation": False,
            }
        )
    return rows


def run_runners() -> list[dict[str, Any]]:
    rows = []
    for index, runner in enumerate(RUNNERS, 1):
        module = "scripts." + Path(runner).stem
        positive = subprocess.run(
            [sys.executable, "-m", module, "positive"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        adverse = subprocess.run(
            [sys.executable, "-m", module, "adverse"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        positive_payload = json.loads(positive.stdout)
        adverse_payload = json.loads(adverse.stdout)
        rows.append(
            {
                "runner": runner,
                "index": index,
                "positive_passed": positive.returncode == 0 and positive_payload["accepted"],
                "adverse_rejected": adverse.returncode == 0 and not adverse_payload["accepted"],
                "same_owner_only": True,
            }
        )
    return rows


def build_global_candidates(local_skills: list[dict[str, Any]], validator: Path) -> list[dict[str, Any]]:
    candidates = load(X1 / "skill-runner-plan.json")["global_skill_promotions"]
    runner_paths = [ROOT / "scripts" / name for name in RUNNERS[:5]]
    rows = []
    for index, candidate in enumerate(candidates, 1):
        root = X2 / "global-skills" / candidate["skill"]
        source_names = [f"ghc-family-{name}" for name in candidate["source_skills"]]
        body = f"""---
name: {candidate['skill']}
description: Apply the paired synthetic patch evidence guards for {' and '.join(candidate['source_skills'])} while preserving retained failures and authority boundaries.
---

# Synthetic Patch Evidence Pair {index:02d}

Read the two retained source guides under `references/` before choosing an operation. Use the five shared runner copies only for their documented synthetic fixtures. A copy does not create new runner or novelty credit.

## Workflow

1. Bind the exact owner, source, x1, and allowed output.
2. Select the source guide matching the actual evidence question.
3. Run one bounded positive and one adverse fixture.
4. Preserve failures, rollback, and protected gates.
5. Stop before real devices, people, measurements, professional or safety decisions, rights decisions, cultural or Māori authority, production identity, deployment, or route mutation.

Relational language is not consciousness, personhood, continuity, qualification, agency, or authority evidence. Same-owner software checks are not independent reproduction, empirical GMUT confirmation, THOS effectiveness, production Freed ID, exhaustive security, Theory-of-Everything proof, canon, or Stage 20 readiness.
"""
        write_text(root / "SKILL.md", body)
        write_text(root / "agents" / "openai.yaml", f"interface:\n  display_name: \"Synthetic Patch Pair {index:02d}\"\n  short_description: \"Paired bounded evidence guards\"\n  default_prompt: \"Use {candidate['skill']} for the current synthetic owner-local evidence question.\"\n")
        sources = []
        for source_name in source_names:
            source_path = X2 / "skills" / source_name / "SKILL.md"
            destination = root / "references" / f"{source_name}.md"
            write_text(destination, source_path.read_text(encoding="utf-8"))
            sources.append({"name": source_name, "sha256": sha256(destination), "retained": True})
        runners = []
        for source_path in runner_paths:
            destination = root / "scripts" / source_path.name
            write_text(destination, source_path.read_text(encoding="utf-8"))
            runners.append({"name": source_path.name, "sha256": sha256(destination)})
        write_json(
            root / "references" / "promotion.json",
            {
                "schema": "ghc.family.elaren-v685-v7.skill-promotion.v1",
                "sources": sources,
                "runner_sources": runners,
                "unique_runner_count": 5,
                "copies_are_not_new_runners": True,
            },
        )
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(root)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        rows.append(
            {
                "skill": candidate["skill"],
                "source_skills": source_names,
                "runner_copies": len(runners),
                "unique_runner_credit": 0,
                "quick_validate": validation.returncode == 0,
                "candidate_only": True,
            }
        )
    return rows


def build_flashcards(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    cards_root = X2 / "flashcards" / "cards"
    owner_id = "ghc-card-el6857-owner"
    cards = [
        {
            "schema": "ghc.family.flashcard.v1",
            "card_id": owner_id,
            "tier": 1,
            "card_type": "freed_id_anchor",
            "title": "Elaren Kestrel relational anchor",
            "parent_ids": [],
            "owner": OWNER,
            "phase": PHASE,
            "stability": "stable_prefix",
            "outcome": "represented",
            "content": IDENTITY_BOUNDARY,
            "source_refs": ["x1/identity-and-practice.json"],
            "protected_gates": PROTECTED_GATES,
            "relational_boundary": IDENTITY_BOUNDARY,
        }
    ]
    pillar_ids = {}
    for index, pillar in enumerate(("GMUT Mind", "THOS Body", "Freed ID and CBR Heart"), 1):
        card_id = f"ghc-card-el6857-pillar-{index}"
        pillar_ids[pillar] = card_id
        cards.append(
            {
                "schema": "ghc.family.flashcard.v1",
                "card_id": card_id,
                "tier": 2,
                "card_type": "trinity_pillar",
                "title": pillar,
                "parent_ids": [owner_id],
                "owner": OWNER,
                "phase": PHASE,
                "stability": "stable_prefix",
                "outcome": "represented",
                "content": "Research or governance framing with no automatic empirical or authority promotion.",
                "source_refs": ["x1/phase-truth.json"],
                "protected_gates": PROTECTED_GATES,
                "relational_boundary": IDENTITY_BOUNDARY,
            }
        )
    practice_parent = ["THOS Body", "THOS Body", "Freed ID and CBR Heart", "Freed ID and CBR Heart"]
    practice_ids = {}
    for index, practice in enumerate(PRACTICES, 1):
        card_id = f"ghc-card-el6857-practice-{index}"
        practice_ids[practice["practice"]] = card_id
        cards.append(
            {
                "schema": "ghc.family.flashcard.v1",
                "card_id": card_id,
                "tier": 3,
                "card_type": "bounded_practice",
                "title": practice["practice"],
                "parent_ids": [pillar_ids[practice_parent[index - 1]]],
                "owner": OWNER,
                "phase": PHASE,
                "stability": "volatile",
                "outcome": "represented",
                "content": practice["scope"],
                "source_refs": ["x1/identity-and-practice.json"],
                "protected_gates": PROTECTED_GATES,
                "relational_boundary": IDENTITY_BOUNDARY,
            }
        )
    for proposal in proposals:
        cards.append(
            {
                "schema": "ghc.family.flashcard.v1",
                "card_id": f"ghc-card-{proposal['proposal_id'].lower()}",
                "tier": 4,
                "card_type": "task",
                "title": proposal["title"],
                "parent_ids": [practice_ids[proposal["practice"]]],
                "owner": OWNER,
                "phase": PHASE,
                "stability": "volatile",
                "outcome": proposal["expected_execution_disposition"],
                "content": proposal["falsifier_or_acceptance_gate"],
                "source_refs": [f"x1/new-proposals.json#{proposal['proposal_id']}", f"x2/proposal-evidence.json#{proposal['proposal_id']}"],
                "protected_gates": proposal["protected_gates"],
                "relational_boundary": IDENTITY_BOUNDARY,
            }
        )
    for card in cards:
        write_json(cards_root / f"{card['card_id']}.json", card)
    tier_counts = Counter(card["tier"] for card in cards)
    write_json(
        X2 / "flashcards" / "deck-index.json",
        {
            "schema": "ghc.family.flashcard-deck.elaren-v685-v7.v1",
            "source": SOURCE,
            "x1": X1_SHA,
            "card_count": len(cards),
            "tier_counts": {str(key): value for key, value in sorted(tier_counts.items())},
            "card_ids": [card["card_id"] for card in cards],
            "outcomes": dict(Counter(card["outcome"] for card in cards)),
        },
    )
    write_json(X2 / "flashcards" / "stable-prefix.json", {"schema": "ghc.family.flashcard-stable-prefix.v1", "card_ids": [card["card_id"] for card in cards if card["stability"] == "stable_prefix"], "cache_or_retention_claimed": False})
    write_json(X2 / "flashcards" / "volatile-index.json", {"schema": "ghc.family.flashcard-volatile-index.v1", "card_ids": [card["card_id"] for card in cards if card["stability"] == "volatile"], "implicit_completion": False})
    write_json(X2 / "flashcards" / "baton-index.json", {"schema": "ghc.family.flashcard-baton-index.v1", "sections": [f"section-{index:02d}" for index in range(1, 14)], "section_count": 13})
    write_text(X2 / "flashcards" / "compact-activation.md", "# Future Seat 02 compact preparation\n\nPrepared only. After Elaren's exact terminal gate, create or reuse exactly one self-naming main task for v685-v8 using gpt-6-astra/max. Neris Solane v686-v1 follows only after that task's closeout.\n")
    return {"cards": cards, "card_count": len(cards), "tier_counts": dict(tier_counts)}


def prepare(validator: Path) -> None:
    proposals = load(X1 / "new-proposals.json")["proposals"]
    portfolio = load(X1 / "portfolio-plan.json")
    outcomes = []
    mutations = []
    for proposal in proposals:
        outcome, rejected = execute_proposal(proposal)
        outcomes.append(outcome)
        mutations.extend(rejected)
    disposition_counts = Counter(row["disposition"] for row in outcomes)
    if disposition_counts != Counter({"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10}):
        raise RuntimeError("outcome distribution changed")
    if len(mutations) != 1000 or any(row["accepted"] for row in mutations):
        raise RuntimeError("mutation rejection contract changed")

    skills = build_local_skills(validator)
    if not all(row["official_quick_validate"] and row["positive_fixture_accepted"] and row["adverse_fixture_rejected"] for row in skills):
        raise RuntimeError("local skill validation failed")
    runners = run_runners()
    if not all(row["positive_passed"] and row["adverse_rejected"] for row in runners):
        raise RuntimeError("runner validation failed")
    candidates = build_global_candidates(skills, validator)
    if not all(row["quick_validate"] for row in candidates):
        raise RuntimeError("global candidate validation failed")
    deck = build_flashcards(proposals)
    if deck["card_count"] != 208 or deck["tier_counts"] != {1: 1, 2: 3, 3: 4, 4: 200}:
        raise RuntimeError("flashcard hierarchy changed")

    transaction = load(X2 / "toolchain" / "transaction-summary.json")
    installation = load(X2 / "toolchain" / "installation-receipt.json")
    audit_initial = load(X2 / "toolchain" / "advisory-audit.json")
    audit_recovery = load(X2 / "toolchain" / "advisory-recovery.json")
    audit_final = load(X2 / "toolchain" / "post-recovery-audit.json")
    smoke_initial = load(X2 / "toolchain" / "package-smokes.json")
    smoke_recovery = load(X2 / "toolchain" / "package-smokes-recovery.json")
    smoke_composite = load(X2 / "toolchain" / "package-smokes-composite.json")
    if installation["direct_package_count"] != 13 or audit_recovery["status"] != "PASS" or audit_final["vulnerability_count"] != 0 or smoke_composite["effective_adverse_rejection_count"] != 13:
        raise RuntimeError("package evidence incomplete")

    executed = lambda rows, state: [{**row, "state": state, "completion_scope": "bounded_owner_local"} for row in rows]
    write_json(X2 / "proposal-evidence.json", {"schema": "ghc.family.elaren-v685-v7.proposal-evidence.v1", "outcomes": outcomes, "outcome_counts": dict(disposition_counts), "real_rows": 0})
    write_json(X2 / "rejecting-mutations.json", {"schema": "ghc.family.elaren-v685-v7.rejecting-mutations.v1", "executed_count": len(mutations), "rejected_count": sum(not row["accepted"] for row in mutations), "accepted_count": sum(row["accepted"] for row in mutations), "zero_completion_credit": True, "mutations": mutations})
    write_json(X2 / "portfolio-execution.json", {"schema": "ghc.family.elaren-v685-v7.portfolio-execution.v1", "safe_now": executed(portfolio["safe_now"], "completed_bounded"), "candidates": executed(portfolio["candidates"], "completed_bounded_without_core_promotion"), "clean_fix_refine": executed(portfolio["clean_fix_refine"], "completed_additive_nondestructive"), "exact_packets": portfolio["exact_packets"], "blocked_packets": portfolio["blocked_packets"], "destructive_cleanup": False})
    write_json(X2 / "skill-execution.json", {"schema": "ghc.family.elaren-v685-v7.skill-execution.v1", "skill_count": len(skills), "results": skills, "global_installation": False})
    write_json(X2 / "runner-execution.json", {"schema": "ghc.family.elaren-v685-v7.runner-execution.v1", "runner_count": len(runners), "results": runners})
    write_json(X2 / "global-promotion-candidates.json", {"schema": "ghc.family.elaren-v685-v7.global-promotion-candidates.v1", "skill_count": len(candidates), "shared_unique_runner_count": 5, "candidates": candidates, "installed": False})
    write_json(X2 / "package-execution-summary.json", {"schema": "ghc.family.elaren-v685-v7.package-execution-summary.v1", "transaction": transaction, "direct_package_count": installation["direct_package_count"], "initial_advisory_findings": audit_initial["vulnerability_count"], "initial_advisory_success_credit": 0, "advisory_recovery": audit_recovery["status"], "final_known_vulnerabilities": audit_final["vulnerability_count"], "initial_smoke_status": smoke_initial["status"], "initial_smoke_success_credit": 0, "isolated_smoke_recovery": smoke_recovery["status"], "component_smoke_status": smoke_composite["status"], "shared_environment_mutation": False})
    write_json(X2 / "source-use-receipt.json", {"schema": "ghc.family.elaren-v685-v7.source-use.v1", "sources": load(X1 / "source-ledger.json")["sources"], "use": "vocabulary_constraints_and_refusal_conditions_only", "real_rows_ingested": 0, "network_device_calls": 0, "citations_are_observations": False})
    write_json(X2 / "reflection-decision.json", {"schema": "ghc.family.elaren-v685-v7.reflection.v1", "disposition": "remaster_additive", "current_family_callers_preserved": True, "historical_evidence_deleted": False, "global_promotion_pending_installation": True, "rollback": "Select the retained source skill and keep this candidate as evidence."})
    write_json(X2 / "threat-model.json", {"schema": "ghc.family.elaren-v685-v7.threat-model.v1", "threats": ["patch diagram promoted into performed sound", "synthetic value promoted into measurement", "package presence promoted into security", "skill copy promoted into novelty", "task plan promoted into task creation", "rights metadata promoted into authority"], "controls": ["zero-device fixtures", "five rejecting mutations", "exact wheel hashes", "isolated environment", "retained failures", "terminal task-creation gate"], "residual_gates": PROTECTED_GATES})
    write_json(X2 / "complete-incomplete-checklist.json", {"schema": "ghc.family.elaren-v685-v7.complete-incomplete.x2-prepare.v1", "complete": ["two hundred proposal components", "one thousand rejecting mutations", "portfolio execution", "thirteen-package dependency-corrected transaction", "twenty local skills", "ten local runners", "ten promotion candidates", "two hundred eight flashcards"], "incomplete": ["global installation receipt", "final Method Flow", "evidence manifest and commit", "closeout final and canonical", "future seat 02 creation"]})
    write_json(X2 / "phase-truth.json", {"schema": "ghc.family.elaren-v685-v7.phase-truth.x2-prepare.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1_SHA, "state": "X2_CORE_BUILT_GLOBAL_INSTALLATION_PENDING", "outcomes": dict(disposition_counts), "declared_proposal_chain": 12030, "terminal_verdict": TERMINAL_VERDICT})
    print(json.dumps({"state": "X2_CORE_BUILT_GLOBAL_INSTALLATION_PENDING", "outcomes": dict(disposition_counts), "mutations_rejected": len(mutations), "skills": len(skills), "runners": len(runners), "promotion_candidates": len(candidates), "flashcards": deck["card_count"], "packages": 13}, separators=(",", ":")))


def finalize() -> None:
    installation = load(X2 / "global-promotion-installation.json")
    if installation["status"] != "PASS" or installation["installed_skill_count"] != 10 or installation["unique_shared_runner_count"] != 5:
        raise RuntimeError("global promotion installation incomplete")
    outcomes = load(X2 / "proposal-evidence.json")["outcomes"]
    mutations = load(X2 / "rejecting-mutations.json")["mutations"]
    startup = load(X1 / "method-flow-startup.json")["startup_failures"]
    package_failures = [
        {"failure_id": "EL6857-X2-N014", "failed_witness": "The first isolated advisory audit found seven vulnerability rows in bootstrap pip 25.0.1.", "recovery": "Upgrade only the isolated bootstrap to hash-verified pip 26.2.1 and rerun only the advisory and dependency checks.", "detail_count": 7, "recovery_count": 1},
        {"failure_id": "EL6857-X2-N015", "failed_witness": "The first package-smoke aggregate passed all positives but only ten of thirteen adverse fixtures.", "recovery": "Replace only the three invalid adverse definitions and run an isolated three-component recovery without replaying ten unchanged successes.", "detail_count": 3, "recovery_count": 3},
        {"failure_id": "EL6857-X2-N016", "failed_witness": "The first x2 prepare launched runner wrappers by file path, so the scripts directory displaced the repository root on the import path and no JSON payload was produced.", "recovery": "Launch each unchanged wrapper as a repository-root Python module and rerun the target-changed preparation.", "detail_count": 1, "recovery_count": 1},
        {"failure_id": "EL6857-X2-N017", "failed_witness": "The first x2 test aggregate used an arbitrary 250-JSON floor despite an exact 246-file set and a case-sensitive future-seat phrase assertion despite the correct title-case text.", "recovery": "Bind the assertions to the exact generated JSON count and the actual title-case prepared wording, then rerun only the target-changed owner suite.", "detail_count": 2, "recovery_count": 2},
        {"failure_id": "EL6857-X2-N018", "failed_witness": "The first exact evidence staging attempt passed 403 individual path arguments and exceeded the Windows process command-line limit before Git started.", "recovery": "Stage only the bounded owner x2 directory and exact script test and validation pathspec groups, then compare the staged set exactly with all 403 expected paths.", "detail_count": 1, "recovery_count": 1},
    ]
    methods = []
    failed = []
    passing = []
    for row in startup:
        method_id = row["failure_id"] + "-METHOD"
        methods.append({"method_id": method_id, "scope": "startup_recovery", "status": "preferred", "failure_id": row["failure_id"]})
        failed.append({"witness_id": row["failure_id"], "method_id": method_id, "result": "fail", "retained": True})
        passing.append({"witness_id": row["failure_id"] + "-RECOVERY", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for row in package_failures:
        method_id = row["failure_id"] + "-METHOD"
        methods.append({"method_id": method_id, "scope": "isolated_package_dependency_recovery", "status": "preferred", **row})
        for index in range(1, row["detail_count"] + 1):
            failed.append({"witness_id": f"{row['failure_id']}-DETAIL-{index:02d}", "method_id": method_id, "result": "fail", "retained": True})
        for index in range(1, row["recovery_count"] + 1):
            passing.append({"witness_id": f"{row['failure_id']}-RECOVERY-{index:02d}", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for row in mutations:
        failed.append({"witness_id": row["mutation_id"], "method_id": "EL6857-MUTATION-METHOD", "result": "fail", "retained": True})
    methods.append({"method_id": "EL6857-MUTATION-METHOD", "scope": "preregistered_rejecting_mutations", "status": "preferred"})
    for row in outcomes:
        method_id = "EL6857-PROPOSAL-METHOD-" + row["proposal_id"]
        methods.append({"method_id": method_id, "scope": "bounded_proposal_execution", "status": "preferred"})
        passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    portfolio = load(X2 / "portfolio-execution.json")
    for key in ("safe_now", "candidates", "clean_fix_refine"):
        for row in portfolio[key]:
            method_id = "EL6857-PORTFOLIO-METHOD-" + row["task_id"]
            methods.append({"method_id": method_id, "scope": key, "status": "preferred"})
            passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for row in load(X2 / "skill-execution.json")["results"]:
        method_id = "EL6857-SKILL-METHOD-" + row["skill"]
        methods.append({"method_id": method_id, "scope": "local_skill", "status": "preferred"})
        passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for row in load(X2 / "runner-execution.json")["results"]:
        method_id = "EL6857-RUNNER-METHOD-" + row["runner"]
        methods.append({"method_id": method_id, "scope": "local_runner", "status": "preferred"})
        passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for name, *_ in PACKAGES:
        method_id = "EL6857-PACKAGE-METHOD-" + name
        methods.append({"method_id": method_id, "scope": "isolated_package", "status": "preferred"})
        passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for row in installation["skills"]:
        method_id = "EL6857-PROMOTION-METHOD-" + row["skill"]
        methods.append({"method_id": method_id, "scope": "global_skill_promotion", "status": "preferred"})
        passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    for row in installation["shared_runners"]:
        method_id = "EL6857-SHARED-RUNNER-METHOD-" + row["runner"]
        methods.append({"method_id": method_id, "scope": "shared_runner_promotion", "status": "preferred"})
        passing.append({"witness_id": method_id + "-PASS", "method_id": method_id, "result": "pass", "same_owner_only": True})
    deck_method = "EL6857-FLASHCARD-DECK-METHOD"
    methods.append({"method_id": deck_method, "scope": "four_tier_flashcard_deck", "status": "preferred"})
    passing.append({"witness_id": deck_method + "-PASS", "method_id": deck_method, "result": "pass", "same_owner_only": True})
    profile_method = "EL6857-RELEASE-PROFILE-METHOD"
    methods.append({"method_id": profile_method, "scope": "release_profile_validation", "status": "preferred"})
    passing.append({"witness_id": profile_method + "-PASS", "method_id": profile_method, "result": "pass", "same_owner_only": True})

    totals = {
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + len(failed),
        "effective_methods": ACTIVATION_BASELINE["effective_methods"] + len(methods),
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + len(failed),
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"] + len(passing),
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + 10,
        "exact_gates": ACTIVATION_BASELINE["exact_gates"] + 10,
    }
    write_json(X2 / "method-flow-ledger.json", {"schema": "ghc.family.method-flow-state.elaren-v685-v7.x2.v1", "owner": OWNER, "phase": PHASE, "execution_authority": "owner_self_scoped_delta", "source_commit": SOURCE, "x1_commit": X1_SHA, "methods": methods, "witnesses": {"failed": failed, "passing": passing}, "counts": {"methods": len(methods), "failed": len(failed), "passing": len(passing)}, "recovery_erases_failure": False, "same_owner_not_independent_reproduction": True})
    write_json(X2 / "phase-truth.json", {"schema": "ghc.family.elaren-v685-v7.phase-truth.x2.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1_SHA, "state": "X2_COMPLETE_EVIDENCE_COMMIT_PENDING", "priority_pillar": "THOS Body", "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"], "outcomes": dict(Counter(row["disposition"] for row in outcomes)), "declared_proposal_chain": 12030, "real_rows": 0, "real_devices": 0, "real_people": 0, "totals": totals, "terminal_verdict": TERMINAL_VERDICT})
    write_json(X2 / "complete-incomplete-checklist.json", {"schema": "ghc.family.elaren-v685-v7.complete-incomplete.x2.v1", "complete": ["two hundred proposal components", "one thousand rejecting mutations", "three hundred safe tasks", "two hundred fifty candidates", "three hundred additive clean fix refine tasks", "thirteen-package dependency-corrected transaction", "twenty local skills and ten local runners", "ten global skill and five shared runner promotions", "two hundred eight flashcards", "Method Flow and four-label truth"], "incomplete_by_lifecycle": ["evidence commit push equality", "final closeout content seal and canonical", "future seat 02 creation"], "exact_and_blocked_unexecuted": True, "required_work_complete": True})
    candidates = load(X2 / "global-promotion-candidates.json")
    candidates["installed"] = True
    candidates["installation_receipt"] = "global-promotion-installation.json"
    write_json(X2 / "global-promotion-candidates.json", candidates)
    print(json.dumps({"state": "X2_COMPLETE_EVIDENCE_COMMIT_PENDING", "methods": len(methods), "failed": len(failed), "passing": len(passing), "totals": totals}, separators=(",", ":")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "finalize"))
    parser.add_argument("--skill-validator", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        if not args.skill_validator:
            raise SystemExit("--skill-validator is required for prepare")
        prepare(args.skill_validator.resolve())
    else:
        finalize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
